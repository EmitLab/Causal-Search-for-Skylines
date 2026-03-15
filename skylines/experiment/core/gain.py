import traceback
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd

from skylines import n_samples, n_runs, experiment_type
from skylines.common.excel import Excel
from skylines.common.state import State, set_state

from tqdm import tqdm

from skylines.common.constants import get_experiments
from skylines.common.utils import find_powerset, set_repr, time_function
from skylines.heuristic import *
from skylines.dataset import Dataset, Dominance


def summarize(state: State, experiment_index, experiment_no, experiment_set, dataset_class: Dataset.__class__, dominance: dict[str, Dominance]):
    set_state(state)

    gains = defaultdict(int)
    dominance_key = None
    controls = None

    for seed in range(n_runs):
        dataset: Dataset = dataset_class(dominance=dominance, size=n_samples, seed=seed)

        if dominance_key is None:
            dominance_key = dataset.dominance_key

        if controls is None:
            controls = find_powerset(dataset.variates)

        # compute the correlations
        # corr: pd.DataFrame = dataset.data.corr()

        # compute gains
        gain, elapsed = time_function(algorithm0.gain, dataset, controls)
        gains['ddSkyline'] += elapsed

        gain, elapsed = time_function(algorithm4_leaky.gain, dataset, True, controls, (1.0, 0.0))
        gains['gnSkyline'] += elapsed

        gain, elapsed = time_function(algorithm4_leaky.gain, dataset, True, controls, (0.9, 0.1))
        gains['lnSkyline (0.9, 0.1)'] += elapsed

        gain, elapsed = time_function(algorithm4_leaky.gain, dataset, True, controls, (0.8, 0.2))
        gains['lnSkyline (0.8, 0.2)'] += elapsed

        gain, elapsed = time_function(algorithm4_leaky.gain, dataset, True, controls, (0.7, 0.3))
        gains['lnSkyline (0.7, 0.3)'] += elapsed

        gain, elapsed = time_function(algorithm4_leaky.gain, dataset, True, controls, (0.6, 0.4))
        gains['lnSkyline (0.6, 0.4)'] += elapsed

    # compute average across seeds
    gains['ddSkyline'] /= n_runs
    gains['gnSkyline'] /= n_runs
    gains['lnSkyline (0.9, 0.1)'] /= n_runs
    gains['lnSkyline (0.8, 0.2)'] /= n_runs
    gains['lnSkyline (0.7, 0.3)'] /= n_runs
    gains['lnSkyline (0.6, 0.4)'] /= n_runs

    experiment_name = f'{experiment_no}{dominance_key}'

    return experiment_index, experiment_name, experiment_set, gains


def summarize_batch(state: State, run_experiment_sets: dict[int, list[int]], max_workers: int = 20):
    agg_gains = pd.DataFrame(columns=['ddSkyline', 'gnSkyline', 'lnSkyline (0.9, 0.1)', 'lnSkyline (0.8, 0.2)', 'lnSkyline (0.7, 0.3)', 'lnSkyline (0.6, 0.4)'])
    dataset_name = dict()
    preferences = dict()

    reverse_lookup = {value: key for key, values in run_experiment_sets.items() for value in values}
    run_experiments = [item for sublist in run_experiment_sets.values() for item in sublist]
    name_set_map = dict()
    name_index_map = dict()

    futures = []

    n_experiment = sum([len(get_experiments()[experiment_no]) for experiment_no in run_experiments])

    with tqdm(total=n_experiment, desc='Batch', position=0) as progress:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            experiment_index = 0

            for experiment_no in run_experiments:
                # output details
                datasets = get_experiments()[experiment_no]
                experiment_set = reverse_lookup[experiment_no]

                for dataset_class, dominance in datasets:
                    # execute the experiment asynchronously
                    future = executor.submit(summarize,
                                             state=state,
                                             experiment_index=experiment_index,
                                             experiment_no=experiment_no,
                                             experiment_set=experiment_set,
                                             dataset_class=dataset_class,
                                             dominance=dominance)

                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                    experiment_index += 1

        # handle response
        for future in as_completed(futures):
            exception = future.exception()
            if exception:
                traceback.print_exception(exception)

            result = future.result()
            if result:
                experiment_index, experiment_name, experiment_set, gains = result

                name_index_map[experiment_name] = experiment_index
                name_set_map[experiment_name] = experiment_set

                agg_gains.loc[experiment_name] = list(gains.values())

                dataset: Dataset = dataset_class(dominance=dominance, size=n_samples)
                dataset_name[experiment_name] = dataset.__class__.__name__
                preferences[experiment_name] = set_repr(frozenset(dataset.preference))

    # sort the results
    sort_order = pd.Series(name_index_map).sort_values().index
    agg_gains = agg_gains.loc[sort_order]

    # generate result analysis
    with Excel('Gain') as excel:
        excel.worksheet = 'Gain'

        for row, name in enumerate(agg_gains.index):
            excel.write_text(name_set_map[name], startrow=row + 2, startcol=0)
            excel.write_text(name, startrow=row + 2, startcol=1)
            excel.write_text(dataset_name[name], startrow=row + 2, startcol=2)
            excel.write_text(preferences[name], startrow=row + 2, startcol=3)

        excel.write_dataframe(agg_gains, 0, 5, index=False, title='Average Timing', color=True, invert_color=True)



def main():
    # Initialize state
    state: State = State(n_samples)
    set_state(state)

    # Refresh state
    state.refresh()

    # Experiment set
    if experiment_type == 'Synthetic (Z != P)':
        run_experiment_sets = {
            16: [140, 141, 142, 143],
            17: [144, 145, 146, 147, 148, 149],
            18: [150, 151, 152, 153, 154, 155],
            19: [136, 137, 138, 139]
        }

    elif experiment_type == 'Synthetic (Z = P)':
        run_experiment_sets = {
            1: [1, 91, 102, 103],
            2: [2, 92, 104, 105],
            3: [3, 106, 107, 108, 93, 113, 116, 117, 120, 121]
        }

    elif experiment_type == 'Real (Z != P)':
        run_experiment_sets = {
            21: [156],
            22: [157],
            23: [158],
            24: [159, 160]
        }

    elif experiment_type == 'Real (Z = P)':
        run_experiment_sets = {
            4: [75],
            5: [78, 79, 80],
            6: [81],
            7: [82, 83],
            8: [84],
            9: [85],
            10: [86],
            11: [87, 88],
            12: [89, 90],
        }
    
    else:
        print('Invalid experiment type')
        exit(1)

    summarize_batch(state=state,
                    run_experiment_sets=run_experiment_sets,
                    max_workers=50)


if __name__ == '__main__':
    main()
