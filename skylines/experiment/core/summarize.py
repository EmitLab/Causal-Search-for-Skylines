import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed

from skylines import n_samples, n_runs, complete_decorrelation, experiment_type
from skylines.common.state import State, set_state, get_state

import pandas as pd
from tqdm import tqdm

from skylines.common.constants import get_experiments
from skylines.common.excel import Excel
from skylines.common.index import Index
from skylines.common.utils import find_powerset, set_repr, format_num
from skylines.dataset import Dataset


def dfs_average(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    stacked = pd.concat(dfs)
    average = stacked.groupby(stacked.index).mean()
    return average


def summarize_seed(state, experiment_no, dataset_class, dominance, samples, seed):
    set_state(state)

    dataset: Dataset = dataset_class(dominance=dominance, size=n_samples, seed=seed)

    # aggregate the results
    excel_book = f'Experiment_{experiment_no}_{dataset.dominance_key}_{samples}_{seed}'

    # if complete_decorrelation:
    #     controls = [frozenset({i for i in dataset.preference})]
    # elif dataset.constant_controls:
    #     controls = dataset.constant_controls
    # else:
    #     controls = find_powerset(dataset.variates)

    # controls_str = [set_repr(x) for x in controls]

    out_file = get_state().get_file('results/raw/comparisons', f'{excel_book}.csv')
    seed_results = pd.read_csv(out_file, index_col=0)

    out_file = get_state().get_file('results/raw/timing', f'{excel_book}.csv')
    seed_timing = pd.read_csv(out_file, index_col=0)

    out_file = get_state().get_file('results/raw/parallel_time', f'{excel_book}.csv')
    seed_parallel_time = pd.read_csv(out_file, index_col=0)

    out_file = get_state().get_file('results/raw/cluster_time', f'{excel_book}.csv')
    seed_cluster_time = pd.read_csv(out_file, index_col=0)

    out_file = get_state().get_file('results/raw/gain', f'{excel_book}_gain0.csv')
    seed_gain_0 = pd.read_csv(out_file, index_col=0)
    seed_gain_0.columns = ['Gain 0']

    gain_cols = []
    seed_unweighted_gain = []
    seed_weighted_gain = []

    for i in [4]:
        out_file = get_state().get_file('results/raw/gain', f'{excel_book}_gain{i}.csv')
        seed_gain_i = pd.read_csv(out_file, index_col=0)

        gain_cols.append(f'Gain {i}')

        seed_unweighted_gain.append(seed_gain_i['Unweighted Gain'])
        seed_weighted_gain.append(seed_gain_i['Weighted Gain'])

    for i in [4]:
        out_file = get_state().get_file('results/raw/gain', f'{excel_book}_leaky_gain{i}.csv')
        seed_gain_i = pd.read_csv(out_file, index_col=0)

        gain_cols.append(f'Leaky Gain {i}')

        seed_unweighted_gain.append(seed_gain_i['Unweighted Gain'])
        seed_weighted_gain.append(seed_gain_i['Weighted Gain'])

    seed_unweighted_gain = pd.concat(seed_unweighted_gain, axis=1)
    seed_unweighted_gain.columns = gain_cols
    # seed_unweighted_gain = seed_unweighted_gain.loc[controls_str]

    seed_weighted_gain = pd.concat(seed_weighted_gain, axis=1)
    seed_weighted_gain.columns = gain_cols
    # seed_weighted_gain = seed_weighted_gain.loc[controls_str]

    # # aggregate the clusters
    # seed_correl = dataset.data.corr()

    # seed_post_correl = None

    # for clusterby in controls:
    #     index: Index = Index(dataset, clusterby)

    #     cluster_correl = None

    #     for cluster in index.index:
    #         if len(cluster) > 1:
    #             if cluster_correl is None:
    #                 cluster_correl = dataset.data.iloc[cluster].corr()
    #             else:
    #                 cluster_correl += dataset.data.iloc[cluster].corr()

    #     cluster_correl /= len(index.index)

    #     if seed_post_correl is None:
    #         seed_post_correl = cluster_correl
    #     else:
    #         seed_post_correl += cluster_correl

    # seed_post_correl /= len(controls)

    # compute averages
    seed_results = pd.DataFrame([seed_results.mean(axis=0)], index=['Average'])
    seed_timing = pd.DataFrame([seed_timing.mean(axis=0)], index=['Average'])
    seed_parallel_time = pd.DataFrame([seed_parallel_time.mean(axis=0)], index=['Average'])
    seed_cluster_time = pd.DataFrame([seed_cluster_time.mean(axis=0)], index=['Average'])
    seed_gain_0 = pd.DataFrame([seed_gain_0.mean(axis=0)], index=['Average'])
    seed_unweighted_gain = pd.DataFrame([seed_unweighted_gain.mean(axis=0)], index=['Average'])
    seed_weighted_gain = pd.DataFrame([seed_weighted_gain.mean(axis=0)], index=['Average'])

    return seed_results, seed_timing, seed_parallel_time, seed_cluster_time, seed_gain_0, seed_unweighted_gain, seed_weighted_gain#, seed_correl, seed_post_correl


def summarize(state, position, experiment_index, experiment_no, experiment_set, dataset_class, dominance, samples, max_sub_workers):
    set_state(state)

    results = []
    timing = []
    parallel_time = []
    cluster_time = []
    gain_0 = []
    unweighted_gain = []
    weighted_gain = []
    # correl = []
    # post_correl = []

    dataset: Dataset = dataset_class(dominance=dominance, size=n_samples)

    # execute the experiment
    futures = []

    with tqdm(total=n_runs, desc=f'Experiment {experiment_no} ({dataset.dominance_key})', position=position, leave=False) as progress:
        with ProcessPoolExecutor(max_workers=max_sub_workers) as executor:
            for seed in range(n_runs):
                future = executor.submit(summarize_seed,
                                         state=state,
                                         experiment_no=experiment_no,
                                         dataset_class=dataset_class,
                                         dominance=dominance,
                                         samples=samples,
                                         seed=seed)

                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

    # handle response
    for future in as_completed(futures):
        exception = future.exception()
        if exception:
            traceback.print_exception(exception)

        result = future.result()
        if result:
            seed_results, seed_timing, seed_parallel_time, seed_cluster_time, seed_gain_0, seed_unweighted_gain, seed_weighted_gain = result

            results.append(seed_results)
            timing.append(seed_timing)
            parallel_time.append(seed_parallel_time)
            cluster_time.append(seed_cluster_time)
            gain_0.append(seed_gain_0)
            unweighted_gain.append(seed_unweighted_gain)
            weighted_gain.append(seed_weighted_gain)
            
            # correl.append(seed_correl)
            # post_correl.append(seed_post_correl)

    # mean across seeds
    results = dfs_average(results)
    timing = dfs_average(timing)
    parallel_time = dfs_average(parallel_time)
    cluster_time = dfs_average(cluster_time)
    gain_0 = dfs_average(gain_0)
    unweighted_gain = dfs_average(unweighted_gain)
    weighted_gain = dfs_average(weighted_gain)

    # correl = sum(correl) / n_runs
    # post_correl = sum(post_correl) / n_runs

    # mean across conditioning sets
    results = results.mean(axis=0)
    timing = timing.mean(axis=0)
    parallel_time = parallel_time.mean(axis=0)
    cluster_time = cluster_time.mean(axis=0)
    gain_0 = gain_0.mean(axis=0)
    unweighted_gain = unweighted_gain.mean(axis=0)
    weighted_gain = weighted_gain.mean(axis=0)

    experiment_name = f'{experiment_no}{dataset.dominance_key}'
    dataset_name = dataset.__class__.__name__
    preferences = set_repr(frozenset(dataset.preference))

    return experiment_index, experiment_name, experiment_set, dataset_name, preferences, results, timing, parallel_time, cluster_time, gain_0, unweighted_gain, weighted_gain #, correl, post_correl


def run_batch(state: State, run_experiment_sets: dict[int, list[int]], max_workers=None, max_sub_workers=None):
    samples = format_num(n_samples)

    agg_results = dict()
    agg_timing = dict()
    agg_parallel_time = dict()
    agg_cluster_time = dict()
    agg_gain_0 = dict()
    agg_unweighted_gain = dict()
    agg_weighted_gain = dict()
    agg_correl = dict()
    dataset_name = dict()
    preferences = dict()

    reverse_lookup = {value: key for key, values in run_experiment_sets.items() for value in values}
    run_experiments = [item for sublist in run_experiment_sets.values() for item in sublist]
    name_set_map = dict()
    name_index_map = dict()

    # execute the experiment
    futures = []

    n_experiment = sum([len(get_experiments()[experiment_no]) for experiment_no in run_experiments])

    with tqdm(total=n_experiment, desc='Batch', position=0) as progress:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            position = 2
            experiment_index = 0

            for experiment_no in run_experiments:
                # output details
                datasets = get_experiments()[experiment_no]
                experiment_set = reverse_lookup[experiment_no]

                for dataset_class, dominance in datasets:
                    # execute the experiment asynchronously
                    future = executor.submit(summarize,
                                             state=state,
                                             position=position,
                                             experiment_index=experiment_index,
                                             experiment_no=experiment_no,
                                             experiment_set=experiment_set,
                                             dataset_class=dataset_class,
                                             dominance=dominance,
                                             samples=samples,
                                             max_sub_workers=max_sub_workers)

                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                    position += 1
                    experiment_index += 1

    # handle response
    for future in as_completed(futures):
        exception = future.exception()
        if exception:
            traceback.print_exception(exception)

        result = future.result()
        if result:
            experiment_index, experiment_name, experiment_set, curr_dataset_name, curr_preferences, results, timing, parallel_time, cluster_time, gain_0, unweighted_gain, weighted_gain = result

            name_index_map[experiment_name] = experiment_index
            name_set_map[experiment_name] = experiment_set

            dataset_name[experiment_name] = curr_dataset_name
            preferences[experiment_name] = curr_preferences

            agg_results[experiment_name] = results
            agg_timing[experiment_name] = timing
            agg_parallel_time[experiment_name] = parallel_time
            agg_cluster_time[experiment_name] = cluster_time
            agg_gain_0[experiment_name] = gain_0
            agg_unweighted_gain[experiment_name] = unweighted_gain
            agg_weighted_gain[experiment_name] = weighted_gain

            # agg_correl[experiment_name] = (correl, post_correl)

    # aggregate the results
    agg_results = pd.DataFrame.from_dict(agg_results, orient='index')
    agg_timing = pd.DataFrame.from_dict(agg_timing, orient='index')
    agg_parallel_time = pd.DataFrame.from_dict(agg_parallel_time, orient='index')
    agg_cluster_time = pd.DataFrame.from_dict(agg_cluster_time, orient='index')
    agg_gain_0 = pd.DataFrame.from_dict(agg_gain_0, orient='index')
    agg_unweighted_gain = pd.DataFrame.from_dict(agg_unweighted_gain, orient='index')
    agg_weighted_gain = pd.DataFrame.from_dict(agg_weighted_gain, orient='index')

    # sort the results
    sort_order = pd.Series(name_index_map).sort_values().index
    agg_results = agg_results.loc[sort_order]
    agg_timing = agg_timing.loc[sort_order]
    agg_parallel_time = agg_parallel_time.loc[sort_order]
    agg_cluster_time = agg_cluster_time.loc[sort_order]
    agg_gain_0 = agg_gain_0.loc[sort_order]
    agg_unweighted_gain = agg_unweighted_gain.loc[sort_order]
    agg_weighted_gain = agg_weighted_gain.loc[sort_order]

    # agg_correl = dict(sorted(agg_correl.items(), key=lambda item: name_index_map[item[0]]))

    # generate result analysis
    causal_cols = [col for col in agg_results.columns if 'Causal' in col]
    agg_results_perc = pd.DataFrame()
    for col in causal_cols:
        base_col = col.split(' Causal')[0]
        if base_col in agg_results:
            agg_results_perc[col] = ((agg_results[col] - agg_results[base_col]) / agg_results[base_col])

    causal_cols = [col for col in agg_timing.columns if 'Causal' in col]
    agg_timing_perc = pd.DataFrame()
    for col in causal_cols:
        base_col = col.split(' Causal')[0]
        if base_col in agg_timing:
            agg_timing_perc[col] = ((agg_timing[col] - agg_timing[base_col]) / agg_timing[base_col])

    causal_cols = [col for col in agg_parallel_time.columns if 'Causal' in col]
    agg_parallel_time_perc = pd.DataFrame()
    for col in causal_cols:
        base_col = col.split(' Causal')[0]
        if base_col in agg_parallel_time:
            agg_parallel_time_perc[col] = ((agg_parallel_time[col] - agg_parallel_time[base_col]) / agg_parallel_time[base_col])

    with Excel('Summary') as excel:
        excel.worksheet = 'Summary'

        for row, name in enumerate(agg_results.index):
            excel.write_text(name_set_map[name], startrow=row + 2, startcol=0)
            excel.write_text(name, startrow=row + 2, startcol=1)
            excel.write_text(dataset_name[name], startrow=row + 2, startcol=2)
            excel.write_text(preferences[name], startrow=row + 2, startcol=3)
        excel.write_dataframe(agg_results, 0, 5, index=False, title='Average Benchmark (results)', color=True, invert_color=True)
        excel.write_dataframe(agg_timing, 0, agg_results.shape[1] + 6, index=False, title='Average Benchmark (timing)', color=True, invert_color=True)
        excel.write_dataframe(agg_parallel_time, 0, agg_results.shape[1] + agg_timing.shape[1] + 7, index=False, title='Average Benchmark (parallel timing)', color=True, invert_color=True)
        excel.write_dataframe(agg_cluster_time, 0, agg_results.shape[1] + agg_timing.shape[1] + agg_parallel_time.shape[1] + 8, index=False, title='Average Benchmark (cluster time)', color=True, invert_color=True)

        for row, name in enumerate(agg_results.index):
            excel.write_text(name_set_map[name], startrow=agg_results.shape[0] + row + 7, startcol=0)
            excel.write_text(name, startrow=agg_results.shape[0] + row + 7, startcol=1)
            excel.write_text(dataset_name[name], startrow=agg_results.shape[0] + row + 7, startcol=2)
            excel.write_text(preferences[name], startrow=agg_results.shape[0] + row + 7, startcol=3)
        excel.write_dataframe(agg_results_perc, agg_results.shape[0] + 5, 5, index=False, title='Average Benchmark (results, % diff. from baseline)', percentage=True, color=True, invert_color=True)
        excel.write_dataframe(agg_timing_perc, agg_results.shape[0] + 5, agg_results_perc.shape[1] + 6, index=False, title='Average Benchmark (timing, % diff. from baseline)', percentage=True, color=True, invert_color=True)
        excel.write_dataframe(agg_parallel_time_perc, agg_results.shape[0] + 5, agg_results_perc.shape[1] + agg_timing_perc.shape[1] + 7, index=False, title='Average Benchmark (parallel timing, % diff. from baseline)', percentage=True, color=True, invert_color=True)
        excel.write_dataframe(agg_gain_0, agg_results.shape[0] + 5, agg_results_perc.shape[1] + agg_timing_perc.shape[1] + agg_parallel_time_perc.shape[1] + 8, index=False, title='Average Gain (data driven)', color=True)
        excel.write_dataframe(agg_unweighted_gain, agg_results.shape[0] + 5, agg_results_perc.shape[1] + agg_timing_perc.shape[1] + agg_parallel_time_perc.shape[1] + agg_gain_0.shape[1] + 9, index=False, title='Average Gain (unweighted)', color=True)
        excel.write_dataframe(agg_weighted_gain, agg_results.shape[0] + 5, agg_results_perc.shape[1] + agg_timing_perc.shape[1] + agg_parallel_time_perc.shape[1] + agg_gain_0.shape[1] + agg_unweighted_gain.shape[1] + 10, index=False, title='Average Gain (weighted)', color=True)

        # excel.worksheet = 'Correlations'

        # row = 0
        # for name, (correl, post_correl) in agg_correl.items():
        #     excel.write_text(name, startrow=row + 1, startcol=0)
        #     excel.write_dataframe(correl, row, 2, index=True, title='Original Correlation', color=True)
        #     excel.write_dataframe(post_correl, row, correl.shape[1] + 4, index=True, title='Average Post-Clustering Correlation', color=True)
        #     row += correl.shape[1] + 5



def main():
    # Initialize state
    state: State = State(n_samples)
    set_state(state)

    # Select experiments to run
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

    # Run the experiments
    run_batch(state=state,
              run_experiment_sets=run_experiment_sets,
              max_workers=20,
              max_sub_workers=5)


if __name__ == '__main__':
    main()
