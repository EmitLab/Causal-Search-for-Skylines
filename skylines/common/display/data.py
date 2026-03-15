import numpy as np
import pandas as pd
from tabulate import tabulate

from skylines.common.excel import Excel
from skylines.common.index import Index
from skylines.dataset import Dataset
from skylines.common.display.graph import plot_heatmap, plot_graph
from skylines.common.utils import set_repr


def display_info(dataset: Dataset, n_runs: int = None, excel: Excel = None):
    info = dict()

    info['Dataset'] = dataset.__class__.__name__

    info['Control variates'] = ', '.join(dataset.control)

    info['Preference variates'] = ', '.join(dataset.preference)

    info['Dominance'] = ''
    for pref, dom in dataset.dominance.items():
        info[pref] = dom.name

    info['Data shape'] = dataset.data.shape

    if n_runs is not None:
        info['No. of runs'] = n_runs

    info = pd.DataFrame.from_dict(info, orient='index').reset_index()
    info.columns = ['Information', 'Details']

    if excel is None:
        table = tabulate(info, tablefmt='Block Nested', headers=info.columns, showindex=False)
        print(table)
        print()
        print()

    else:
        excel.write_dataframe(info,
                              startrow=0,
                              startcol=0,
                              index=False)


def plot_correlation(dataset: Dataset, excel: Excel = None):
    matrix = dataset.data.corr()
    np.fill_diagonal(matrix.values, np.nan)

    plot_heatmap(dataset,
                 matrix,
                 title='Correlation Matrix',
                 excel=excel,
                 startrow=0,
                 startcol=3,
                 invert_color=True)


def plot_correlation_preferences(dataset: Dataset, excel: Excel = None):
    matrix = dataset.data[dataset.preference].corr()
    np.fill_diagonal(matrix.values, np.nan)

    plot_heatmap(dataset,
                 matrix,
                 title='Correlation Matrix (Preference Variates)',
                 excel=excel,
                 startrow=dataset.data.shape[1] + 5,
                 startcol=3,
                 invert_color=True)


def plot_dataset_graph(dataset: Dataset, excel: Excel = None):
    matrix = dataset.adjmat

    plot_graph(dataset,
               matrix,
               title='Ground Truth Graph',
               edge_label=True,
               excel=excel,
               startrow=dataset.data.shape[1] + len(dataset.preference) + 10,
               startcol=0)
