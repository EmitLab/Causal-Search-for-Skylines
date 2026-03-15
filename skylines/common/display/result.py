import numpy as np
import pandas as pd
from matplotlib import cm, pyplot as plt
from tabulate import tabulate

from skylines.common.excel import Excel
from skylines.dataset import Dataset


def display_results(dataset: Dataset, results: dict[str, pd.DataFrame], excel: Excel = None):
    column = dataset.data.shape[1] + 10

    for title, result in results.items():
        # change title for utils
        if title.endswith('_timing'):
            title = title[:-7] + ', utils in seconds'

        # display the results
        if excel is None:
            print(f'Benchmark ({title})')
            table = tabulate(result, tablefmt='Block Nested', headers=result.columns)
            print(table)
            print()
            print()

        else:
            excel.write_dataframe(result,
                                  startrow=0,
                                  startcol=column,
                                  title=f'Benchmark ({title})',
                                  color=True,
                                  invert_color=True,
                                  color_axis='row')

        column += result.shape[1] + 2


def display_algorithm_results(dataset: Dataset, results: dict[str, pd.DataFrame], algo_results: dict[str, (pd.DataFrame, float)], excel: Excel = None):
    column = dataset.data.shape[1] + 10
    for title, result in results.items():
        column += result.shape[1] + 2

    for index, (title, (algo_result, algo_time)) in enumerate(algo_results.items()):
        # display the results
        if excel is None:
            print(f'{title} (Time = {algo_time:.4f}s)')
            table = tabulate(algo_result, tablefmt='Block Nested', headers=algo_result.columns)
            print(table)
            print()
            print()

        else:
            excel.write_dataframe(algo_result,
                                  startrow=0,
                                  startcol=column,
                                  title=f'{title} (Time = {algo_time:.4f}s)',
                                  color=True,
                                  invert_color=False,
                                  color_axis='column')

        column += algo_result.shape[1] + 2


def display_ensemble_results(results: dict[str, pd.DataFrame], excel: Excel = None):
    column = 3

    for index, (title, result) in enumerate(results.items()):
        # change title for utils
        if title.endswith('_timing'):
            title = title[:-7] + ', utils in seconds'

        # display the results
        if excel is None:
            print(f'Average Benchmark ({title})')
            table = tabulate(result, tablefmt='Block Nested', headers=result.columns)
            print(table)
            print()
            print()

        else:
            excel.write_dataframe(result,
                                  startrow=0,
                                  startcol=column,
                                  title=f'Average Benchmark ({title})',
                                  color=True,
                                  invert_color=True,
                                  color_axis='row')

        column += result.shape[1] + 2


def display_ensemble_algorithm_results(results: dict[str, pd.DataFrame], algo_results: dict[str, (pd.DataFrame, float)], excel: Excel = None):
    column = 3
    for title, result in results.items():
        column += result.shape[1] + 2

    for index, (title, (algo_result, algo_time)) in enumerate(algo_results.items()):
        # display the results
        if excel is None:
            print(f'Average {title} (Avg Time = {algo_time:.4f}s)')
            table = tabulate(algo_result, tablefmt='Block Nested', headers=algo_result.columns)
            print(table)
            print()
            print()

        else:
            excel.write_dataframe(algo_result,
                                  startrow=0,
                                  startcol=column,
                                  title=f'Average {title} (Avg Time = {algo_time:.4f}s)',
                                  color=True,
                                  invert_color=False,
                                  color_axis='column')

        column += algo_result.shape[1] + 2
