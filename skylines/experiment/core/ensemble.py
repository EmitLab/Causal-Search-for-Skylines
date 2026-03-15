from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import cpu_count

import pandas as pd

from .experiment import Experiment
from skylines.common.display.data import display_info
from skylines.common.display.result import display_ensemble_results, display_ensemble_algorithm_results
from skylines.common.excel import Excel, merge_workbooks
from skylines.dataset import Dataset, Dominance
from skylines.common.state import State, set_state, get_state


class EnsembleExperiment:

    def __init__(self,
                 experiment_no: int,
                 dataset_class: Dataset.__class__,
                 dominance: dict[str, Dominance] | None,
                 excel_book: str,
                 n_samples: int = 10000,
                 n_runs: int = 5,
                 leakage: tuple[float, float] = (1.0, 0.0),
                 complete_decorrelation: bool = False):
        self.experiment_no = experiment_no
        self.dataset_class = dataset_class
        self.dominance = dominance
        self.excel_book = excel_book
        self.n_samples = n_samples
        self.n_runs = n_runs
        self.leakage = leakage
        self.complete_decorrelation = complete_decorrelation

    def execute(self, state: State, position: int = 0, silent: bool = False, max_workers: int = None) -> dict[str, pd.DataFrame]:
        # set the state
        set_state(state)

        # determine actual max number of workers
        if max_workers is None:
            max_workers = cpu_count() // 2
        max_workers = min(cpu_count(), max(max_workers, 1))

        # execute the experiment
        average_results = None
        average_algo_results = None

        dataset: Dataset = self.dataset_class(dominance=self.dominance, size=self.n_samples)

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for seed in range(self.n_runs):
                curr_dataset: Dataset = self.dataset_class(dominance=self.dominance, size=self.n_samples, seed=seed)

                experiment: Experiment = Experiment(dataset=curr_dataset,
                                                    excel_book=f'{self.excel_book}_{seed}',
                                                    excel_sheet=f'Seed {seed}',
                                                    complete_decorrelation=self.complete_decorrelation,
                                                    leakage=self.leakage)

                future = executor.submit(experiment.execute, state=state, experiment_no=self.experiment_no, seed=seed, position=position + seed, silent=silent)
                futures.append(future)

            for future in as_completed(futures):
                average_result, average_algo_result = future.result()

                if average_results is None:
                    average_results = average_result
                else:
                    average_results['results'] += average_result['results']
                    average_results['timing'] += average_result['timing']
                    average_results['parallel_time'] += average_result['parallel_time']
                    average_results['cluster_time'] += average_result['cluster_time']

                if average_algo_results is None:
                    average_algo_results = average_algo_result
                else:
                    for key in average_algo_results.keys():
                        average_algo_results[key] = (average_algo_results[key][0] + average_algo_result[key][0], average_algo_results[key][1] + average_algo_result[key][1])

        average_results['results'] = average_results['results'].astype(float) / self.n_runs
        average_results['timing'] = average_results['timing'].astype(float) / self.n_runs
        average_results['parallel_time'] = average_results['parallel_time'].astype(float) / self.n_runs
        average_results['cluster_time'] = average_results['cluster_time'].astype(float) / self.n_runs

        for key in average_algo_results.keys():
            average_algo_results[key] = (average_algo_results[key][0] / self.n_runs, average_algo_results[key][1] / self.n_runs)

        if not silent:
            self._save(dataset, average_results, average_algo_results)

        return average_results

    def _save(self, dataset: Dataset, average_results: dict[str, pd.DataFrame], average_algo_results: (pd.DataFrame, float)) -> None:
        # open excel
        with Excel(book_name=f'{self.excel_book}_summary', folder_name='results/intermediate') as excel:
            excel.worksheet = 'Summary'

            display_info(dataset, n_runs=self.n_runs, excel=excel)

            display_ensemble_results(average_results, excel=excel)

            display_ensemble_algorithm_results(average_results, average_algo_results, excel=excel)

        # merge workbooks
        out_file = self.excel_book
        in_files = [f'{self.excel_book}_summary'] + [f'{self.excel_book}_{seed}' for seed in range(self.n_runs)]
        merge_workbooks(out_file=out_file, in_files=in_files)
