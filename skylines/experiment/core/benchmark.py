from skylines import n_samples, n_runs, leakage, complete_decorrelation, experiment_type
from skylines.common.state import State, set_state

import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

from tqdm import tqdm

from skylines.common.constants import get_experiments
from skylines.common.utils import format_num
from skylines.dataset import Dataset
from skylines.experiment.core import EnsembleExperiment


def run_batch(state: State, run_experiments: list[int], n_samples: int = 100_000, n_runs: int = 5, max_workers: int = None, max_sub_workers: int = None, leakage: tuple[float, float] = (1.0, 0.0), complete_decorrelation: bool = False):
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
                    # create an instance of the dataset
                    dataset: Dataset = dataset_class(dominance=dominance, size=n_samples)

                    # create excel book name
                    book_name = f'Experiment_{experiment_no}_{dataset.dominance_key}_{samples}'

                    # create the experiment
                    experiment: EnsembleExperiment = EnsembleExperiment(experiment_no=experiment_no,
                                                                        dataset_class=dataset_class,
                                                                        dominance=dominance,
                                                                        excel_book=book_name,
                                                                        n_samples=n_samples,
                                                                        n_runs=n_runs,
                                                                        leakage=leakage,
                                                                        complete_decorrelation=complete_decorrelation)

                    # execute the experiment asynchronously
                    future = executor.submit(experiment.execute,
                                             state=state,
                                             position=position,
                                             silent=False,
                                             max_workers=max_sub_workers)

                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                    position += n_runs + 1

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

    # Run the experiments
    run_batch(state=state,
              run_experiments=run_experiments,
              n_samples=n_samples,
              n_runs=n_runs,
              max_workers=20,
              max_sub_workers=5,
              leakage=leakage,
              complete_decorrelation=complete_decorrelation)


if __name__ == '__main__':
    main()
