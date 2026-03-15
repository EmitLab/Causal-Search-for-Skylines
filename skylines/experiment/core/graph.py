import json
import os
from skylines import n_samples, n_runs, leakage, complete_decorrelation, experiment_type

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import traceback

from tqdm import tqdm
from skylines.common.causal.dag import learn_dag
from skylines.common.constants.constants import get_experiments
from skylines.common.state import set_state
from skylines.common.state.state import State
from skylines.common.utils.utils import format_num
from skylines.dataset import *


def learn_seed(state, dataset_class, dominance, n_samples, seed):
    set_state(state)

    dataset: Dataset = dataset_class(dominance=dominance, size=n_samples, seed=seed)

    effects = learn_dag(dataset.data)

    with open(f'graphs/{dataset.name}.json', 'w') as f:
        json.dump(effects, f, indent=4)


def learn_graphs(state, position, dataset_class, dominance, n_samples, n_runs, max_sub_workers):
    set_state(state)

    dataset: Dataset = dataset_class(dominance=dominance, size=n_samples)

    futures = []

    with tqdm(total=n_runs, desc=f'{dataset.__class__.__name__} ({dataset.dominance_key})', position=position, leave=False) as progress:
        with ProcessPoolExecutor(max_workers=max_sub_workers) as executor:
            for seed in list(range(n_runs)) + [42]:
                future = executor.submit(learn_seed,
                                         state=state,
                                         dataset_class=dataset_class,
                                         dominance=dominance,
                                         n_samples=n_samples,
                                         seed=seed)

                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

    # handle response
    for future in as_completed(futures):
        exception = future.exception()
        if exception:
            traceback.print_exception(exception)


def run_batch(state: State, run_experiments: list[int], n_samples: int = 100_000, n_runs: int = 5, max_workers: int = None, max_sub_workers: int = None):
    # determine actual max number of workers
    if max_workers is None:
        max_workers = cpu_count() // 2
    max_workers = min(cpu_count(), max(max_workers, 1))

    # execute the experiment
    futures = []

    n_experiment = sum([len(get_experiments()[experiment_no]) for experiment_no in run_experiments])

    with tqdm(total=n_experiment, desc='Batch', position=0) as progress:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            samples = format_num(n_samples)
            position = 2

            for experiment_no in run_experiments:
                # output details
                datasets = get_experiments()[experiment_no]

                for dataset_class, dominance in datasets:
                    # execute the experiment asynchronously
                    future = executor.submit(learn_graphs,
                                             state=state,
                                             position=position,
                                             dataset_class=dataset_class,
                                             dominance=dominance,
                                             n_samples=n_samples,
                                             n_runs=n_runs,
                                             max_sub_workers=max_sub_workers)

                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                    position += 1
    
    # handle exceptions
    for future in as_completed(futures):
        exception = future.exception()
        if exception:
            traceback.print_exception(exception)


def main():
    # Initialize state
    state: State = State(n_samples)
    set_state(state)

    # Refresh state
    state.refresh()

    os.makedirs("graphs", exist_ok=True)
    
    # Select experiments to run
    if experiment_type == 'Synthetic (Z != P)':
        run_experiments = [136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155]
    
    elif experiment_type == 'Synthetic (Z = P)':
        run_experiments = [1, 2, 3, 91, 92, 93, 102, 103, 104, 105, 106, 107, 108, 113, 116, 117, 120, 121]
    
    elif experiment_type == 'Real (Z != P)':
        run_experiments = [156, 157, 158, 159, 160]
    
    elif experiment_type == 'Real (Z = P)':
        run_experiments = [75, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
    
    else:
        print('Invalid experiment type')
        exit(1)

    run_batch(
        state = state,
        run_experiments = run_experiments,
        n_samples = n_samples,
        n_runs = n_runs,
        max_workers = 20,
        max_sub_workers = 5
    )


if __name__ == "__main__":
    main()
