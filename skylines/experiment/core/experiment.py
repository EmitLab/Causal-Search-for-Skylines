import pandas as pd
from bunch_py3 import Bunch
from matplotlib import pyplot as plt
from tqdm import tqdm

from skylines.common.display.data import display_info, plot_correlation, plot_correlation_preferences, plot_dataset_graph
from skylines.common.display.result import display_results, display_algorithm_results
from skylines.common.excel import Excel
from skylines.common.state import State, set_state, get_state
from skylines.common.utils import find_powerset, set_repr, time_function
from skylines.dataset import Dataset
from skylines.heuristic import *
from skylines.skyline import Skyline
from skylines.skyline.bbs import BBSSkyline, BBSCausalSkyline
from skylines.skyline.bnl import BNLSkyline, BNLCausalSkyline, BNLCausalHMSkyline
from skylines.skyline.dnc import DnCSkyline, DnCCausalSkyline
from skylines.skyline.less import LESSSkyline, LESSCausalSkyline
from skylines.skyline.salsa import SaLSaSkyline, SaLSaCausalSkyline
from skylines.skyline.sfs import SFSSkyline, SFSCausalSkyline


class Experiment:

    def __init__(self, dataset: Dataset, excel_book: str, excel_sheet: str, leakage: tuple[float, float], complete_decorrelation: bool = False):
        self.dataset = dataset
        self.excel_book = excel_book
        self.excel_sheet = excel_sheet
        self.memoise = Bunch()
        self.leakage = leakage
        self.complete_decorrelation = complete_decorrelation

    def execute(self, state: State, experiment_no: int = 1, seed: int = 0, position: int = 0, silent: bool = False) -> (dict[str, pd.DataFrame], pd.DataFrame, float):
        # set the state
        set_state(state)

        # run sub-experiment for each confounder
        results: dict = {'results': None, 'timing': None, 'parallel_time': None, 'cluster_time': None}
        algo_results = dict()

        # get control sets
        if self.complete_decorrelation:
            controls = [frozenset({i for i in self.dataset.preference})]
        elif self.dataset.constant_controls is not None:
            controls = self.dataset.constant_controls
        else:
            controls = find_powerset(self.dataset.control)

        # skip zero gains
        if not isinstance(controls, list):
            cluster_result = self._execute(clusterby=None)
            
            if results['results'] is None:
                results['results'] = pd.DataFrame(columns=cluster_result['results']['Model'].values)
                results['results'].index.name = 'Cluster'
            results['results'].loc['<skipped>'] = cluster_result['results']['Comparisons'].values
            
            if results['timing'] is None:
                results['timing'] = pd.DataFrame(columns=cluster_result['timing']['Model'].values)
                results['timing'].index.name = 'Cluster'
            results['timing'].loc['<skipped>'] = cluster_result['timing']['Time (seconds)'].values

            if results['parallel_time'] is None:
                results['parallel_time'] = pd.DataFrame(columns=cluster_result['parallel_time']['Model'].values)
                results['parallel_time'].index.name = 'Cluster'
            results['parallel_time'].loc['<skipped>'] = cluster_result['parallel_time']['Time (seconds)'].values

            if results['cluster_time'] is None:
                results['cluster_time'] = pd.DataFrame(columns=['KMeans Time (seconds)'])
                results['cluster_time'].index.name = 'Cluster'
            results['cluster_time'].loc['<skipped>'] = [cluster_result['cluster_time']]

            columns = ['Gain']
            out = pd.DataFrame([[controls] * len(columns)], index=['<skipped>'], columns=columns)
            algo_results['Gain 0'] = (out.copy(), 0)

            columns = ['Unweighted Gain', 'Weighted Gain']
            out = pd.DataFrame([[controls] * len(columns)], index=['<skipped>'], columns=columns)
            algo_results['Gain 4'] = (out.copy(), 0)
            algo_results['Leaky Gain 4'] = (out.copy(), 0)
        
        else:
            # execute experiments
            for subindex, clusterby in enumerate(tqdm(controls, desc=f'Experiment {experiment_no} ({self.dataset.dominance_key}) seed={seed}', position=position, leave=False)):
                # execute the experiment
                cluster_result: dict[str, pd.DataFrame] = self._execute(clusterby=clusterby)

                # close all plots to reduce resource consumption
                plt.close('all')

                # add cluster results to all results
                if results['results'] is None:
                    results['results'] = pd.DataFrame(columns=cluster_result['results']['Model'].values)
                    results['results'].index.name = 'Cluster'
                results['results'].loc[set_repr(clusterby)] = cluster_result['results']['Comparisons'].values
                
                if results['timing'] is None:
                    results['timing'] = pd.DataFrame(columns=cluster_result['timing']['Model'].values)
                    results['timing'].index.name = 'Cluster'
                results['timing'].loc[set_repr(clusterby)] = cluster_result['timing']['Time (seconds)'].values

                if results['parallel_time'] is None:
                    results['parallel_time'] = pd.DataFrame(columns=cluster_result['parallel_time']['Model'].values)
                    results['parallel_time'].index.name = 'Cluster'
                results['parallel_time'].loc[set_repr(clusterby)] = cluster_result['parallel_time']['Time (seconds)'].values

                if results['cluster_time'] is None:
                    results['cluster_time'] = pd.DataFrame(columns=['KMeans Time (seconds)'])
                    results['cluster_time'].index.name = 'Cluster'
                results['cluster_time'].loc[set_repr(clusterby)] = [cluster_result['cluster_time']]

            # run the heuristic
            gain, elapsed = time_function(algorithm0.gain, self.dataset, controls)
            algo_results['Gain 0'] = (gain, elapsed)

            gain, elapsed = time_function(algorithm4.gain_all, self.dataset, controls)
            algo_results['Gain 4'] = (gain, elapsed)

            gain, elapsed = time_function(algorithm4_leaky.gain_all, self.dataset, controls, self.leakage)
            algo_results['Leaky Gain 4'] = (gain, elapsed)

        # compute averages
        average_results: dict = dict()
        for key in ['results', 'timing', 'parallel_time', 'cluster_time']:
            average_results[key] = pd.DataFrame([results[key].mean(axis=0)], index=['Average'])

        average_algo_results = dict()
        for key in ['Gain 0', 'Gain 4', 'Leaky Gain 4']:
            gain, elapsed = algo_results[key]
            average_algo_results[key] = (pd.DataFrame([gain.mean(axis=0)], index=['Average']), elapsed)

        # save the results
        if not silent:
            self._save(results, average_results, algo_results, average_algo_results)

        return average_results, average_algo_results

    def _save(self, results: dict[str, pd.DataFrame], average_results: dict[str, pd.DataFrame], algo_results: dict[str, tuple[pd.DataFrame, float]], average_algo_results: dict[str, tuple[pd.DataFrame, float]]):

        combined_results = dict()
        for key in ['results', 'timing', 'parallel_time', 'cluster_time']:
            combined_results[key] = pd.concat([results[key], average_results[key]], axis=0)

        combined_algo_results = dict()
        for key in ['Gain 0', 'Gain 4', 'Leaky Gain 4']:
            combined_algo_results[key] = (pd.concat([algo_results[key][0], average_algo_results[key][0]], axis=0), algo_results[key][1])

        with Excel(book_name=self.excel_book, folder_name='results/intermediate') as excel:
            excel.worksheet = self.excel_sheet

            display_info(self.dataset, excel=excel)

            plot_correlation(self.dataset, excel=excel)
            plot_correlation_preferences(self.dataset, excel=excel)

            plot_dataset_graph(self.dataset, excel=excel)

            display_results(self.dataset, combined_results, excel=excel)

            display_algorithm_results(self.dataset, combined_results, combined_algo_results, excel=excel)

            out_file = get_state().get_file('results/raw/comparisons', f'{self.excel_book}.csv')
            results['results'].to_csv(out_file)

            out_file = get_state().get_file('results/raw/timing', f'{self.excel_book}.csv')
            results['timing'].to_csv(out_file)

            out_file = get_state().get_file('results/raw/parallel_time', f'{self.excel_book}.csv')
            results['parallel_time'].to_csv(out_file)

            out_file = get_state().get_file('results/raw/cluster_time', f'{self.excel_book}.csv')
            results['cluster_time'].to_csv(out_file)

            for key, value in algo_results.items():
                if key.startswith('Gain '):
                    gain_algo = f"gain{key.removeprefix('Gain ')}"
                elif key.startswith('Leaky Gain '):
                    gain_algo = f"leaky_gain{key.removeprefix('Leaky Gain ')}"

                out_file = get_state().get_file('results/raw/gain', f'{self.excel_book}_{gain_algo}.csv')
                value[0].to_csv(out_file)

                out_file = get_state().get_file('results/raw/gain', f'{self.excel_book}_{gain_algo}.time')
                with open(out_file, 'w') as file:
                    file.write(f'{value[1]}\n')

    def _execute(self, clusterby: frozenset) -> dict[str, pd.DataFrame]:
        results = []
        timing = []
        parallel = []
        skylines = []

        cluster_time = 0

        # find the skyline using block nested loop approach
        points, comparisons, duration, p_duration, _ = self._compute_skyline(BNLSkyline, 'BNL', memoise=True)
        skylines.append(points)
        results.append(('BNL', comparisons))
        timing.append(('BNL', duration))
        parallel.append(('BNL', p_duration))

        # find the skyline after de-correlating
        if clusterby is not None:
            points, comparisons, duration, p_duration, cluster_time = self._compute_skyline(BNLCausalSkyline, 'BNL Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('BNL Causal', comparisons))
        timing.append(('BNL Causal', duration))
        parallel.append(('BNL Causal', p_duration))

        # find the skyline after de-correlating with hierarchical merging
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(BNLCausalHMSkyline, 'BNL Causal HM', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('BNL Causal HM', comparisons))
        timing.append(('BNL Causal HM', duration))
        parallel.append(('BNL Causal HM', p_duration))

        # find the skyline using SFS approach
        points, comparisons, duration, p_duration, _ = self._compute_skyline(SFSSkyline, 'SFS', memoise=True)
        skylines.append(points)
        results.append(('SFS', comparisons))
        timing.append(('SFS', duration))
        parallel.append(('SFS', p_duration))

        # find the skyline after de-correlating using SFS
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(SFSCausalSkyline, 'SFS Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('SFS Causal', comparisons))
        timing.append(('SFS Causal', duration))
        parallel.append(('SFS Causal', p_duration))

        # find the skyline using LESS approach
        points, comparisons, duration, p_duration, cluster_time = self._compute_skyline(LESSSkyline, 'LESS', memoise=True)
        skylines.append(points)
        results.append(('LESS', comparisons))
        timing.append(('LESS', duration))
        parallel.append(('LESS', p_duration))

        # find the skyline after de-correlating using LESS
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(LESSCausalSkyline, 'LESS Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('LESS Causal', comparisons))
        timing.append(('LESS Causal', duration))
        parallel.append(('LESS Causal', p_duration))

        # find the skyline using SaLSa approach
        points, comparisons, duration, p_duration, _ = self._compute_skyline(SaLSaSkyline, 'SaLSa', memoise=True)
        skylines.append(points)
        results.append(('SaLSa', comparisons))
        timing.append(('SaLSa', duration))
        parallel.append(('SaLSa', p_duration))

        # find the skyline after de-correlating using SaLSa
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(SaLSaCausalSkyline, 'SaLSa Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('SaLSa Causal', comparisons))
        timing.append(('SaLSa Causal', duration))
        parallel.append(('SaLSa Causal', p_duration))

        # find the skyline using divide and conquer approach
        points, comparisons, duration, p_duration, _ = self._compute_skyline(DnCSkyline, 'D&C', memoise=True)
        skylines.append(points)
        results.append(('D&C', comparisons))
        timing.append(('D&C', duration))
        parallel.append(('D&C', p_duration))

        # find the skyline after de-correlating using DNC
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(DnCCausalSkyline, 'D&C Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('D&C Causal', comparisons))
        timing.append(('D&C Causal', duration))
        parallel.append(('D&C Causal', p_duration))

        # find the skyline using branch and bound approach
        points, comparisons, duration, p_duration, _ = self._compute_skyline(BBSSkyline, 'BBS', memoise=True)
        skylines.append(points)
        results.append(('BBS', comparisons))
        timing.append(('BBS', duration))
        parallel.append(('BBS', p_duration))

        # find the skyline after de-correlating using BBS
        if clusterby is not None:
            points, comparisons, duration, p_duration, _ = self._compute_skyline(BBSCausalSkyline, 'BBS Causal', memoise=False, clusterby=clusterby)
        skylines.append(points)
        results.append(('BBS Causal', comparisons))
        timing.append(('BBS Causal', duration))
        parallel.append(('BBS Causal', p_duration))

        # verify computed skyline
        verified = [df.equals(skylines[0]) for df in skylines]
        if not all(verified):
            raise AssertionError(f'The computed skylines are not identical: {verified}')

        # convert to dataframe
        results = pd.DataFrame(results, columns=['Model', 'Comparisons'])
        timing = pd.DataFrame(timing, columns=['Model', 'Time (seconds)'])
        parallel = pd.DataFrame(parallel, columns=['Model', 'Time (seconds)'])

        # create the results dictionary
        results = {'results': results, 'timing': timing, 'parallel_time': parallel, 'cluster_time': cluster_time}

        return results

    def _compute_skyline(self, skyline_class: Skyline.__class__, title: str, memoise: bool = False, *args, **kwargs):
        def _compute():
            skyline: Skyline = skyline_class(self.dataset, *args, **kwargs)
            points: pd.DataFrame = skyline.compute()
            return points, skyline.comparisons, skyline.total_time, skyline.parallel_time, skyline.cluster_time

        if memoise:
            if title not in self.memoise:
                memoir = Bunch()
                memoir.points, memoir.comparisons, memoir.total_time, memoir.parallel_time, memoir.cluster_time = _compute()
                self.memoise[title] = memoir

            memoir = self.memoise[title]
            return memoir.points, memoir.comparisons, memoir.total_time, memoir.parallel_time, memoir.cluster_time

        return _compute()
