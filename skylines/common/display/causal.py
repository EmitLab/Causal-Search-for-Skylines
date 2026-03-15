import contextlib
import os

import pandas as pd
from tabulate import tabulate

from skylines.common.excel import Excel, formula
from skylines.common.utils import list_of_sets_repr, set_repr
from skylines.dataset import Dataset
from skylines.common.display.graph import plot_graph

# force to allow keyboard interrupts
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

# disable error logging for gcastle import
with contextlib.redirect_stderr(None):
    from castle.algorithms import GES


def causal_graph_GES(dataset: Dataset) -> pd.DataFrame:
    # train the GES model
    model = GES()
    model.learn(dataset.data)

    # get the causal matrix
    matrix = model.causal_matrix

    # convert to dataframe
    matrix = pd.DataFrame(matrix, columns=dataset.data.columns, index=dataset.data.columns)

    # orient the edges
    # for col in matrix.columns:
    #     for row in matrix.index:
    #         if matrix.at[row, col] == 1:
    #             if (row in dataset.preference and (col in dataset.preference or col in dataset.control)) or \
    #                     (row in dataset.control and col in dataset.control and matrix.at[col, row] == 1):
    #                 matrix.at[row, col] = 0

    return matrix


def plot_causal_graph(dataset: Dataset, excel: Excel = None):
    matrix = causal_graph_GES(dataset)

    plot_graph(dataset,
               matrix,
               title='Discovered Causal Graph',
               edge_label=False,
               excel=excel,
               startrow=dataset.data.shape[1] + len(dataset.preference) + 10,
               startcol=7)


def display_minimal_sets(dataset: Dataset,
                         minimal_sets: pd.DataFrame,
                         combined_minimal_sets: list[frozenset],
                         best_minimal_sets: list[frozenset],
                         excel: Excel = None):
    display_minimal_sets_data(dataset, minimal_sets, best_minimal_sets, excel=excel)
    # display_minimal_sets_stats(dataset, combined_minimal_sets, excel=excel)


def display_minimal_sets_data(dataset: Dataset,
                              minimal_sets: pd.DataFrame,
                              best_minimal_sets: list[frozenset],
                              excel: Excel = None):
    # convert to string representation
    minimal_sets = minimal_sets.copy()
    minimal_sets['Minimal Sets'] = [list_of_sets_repr(x) for x in minimal_sets['Minimal Sets']]
    best_minimal_sets = list_of_sets_repr(best_minimal_sets)

    if excel is None:
        print('[Minimal D-separators]')
        table = tabulate(minimal_sets, tablefmt='Block Nested', headers=minimal_sets.columns, showindex=False)
        print(table)
        print(f'Combined Minimal D-separators: {best_minimal_sets}')
        print()
        print()

    else:
        excel.write_dataframe(minimal_sets,
                              startrow=0,
                              startcol=dataset.data.shape[1] + 5,
                              title='Minimal D-separators',
                              index=False,
                              color=True,
                              invert_color=True)

        excel.write_text('Combined Minimal D-separators',
                         bold=True,
                         startrow=minimal_sets.shape[0] + 3,
                         startcol=dataset.data.shape[1] + 5,
                         colspan=2)

        excel.write_text(best_minimal_sets,
                         startrow=minimal_sets.shape[0] + 3,
                         startcol=dataset.data.shape[1] + 7,
                         colspan=2)


def display_minimal_sets_stats(dataset: Dataset,
                               combined_minimal_sets: list[frozenset],
                               excel: Excel = None):
    result_index = []
    result = []
    for index, minimal_set in enumerate(combined_minimal_sets):
        result_index.append(set_repr(minimal_set))
        with contextlib.redirect_stderr(None):
            sum_i = '=' + \
                    formula.sum_if(criteria_range=(3,
                                                   dataset.data.shape[1] + 9,
                                                   len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                                   dataset.data.shape[1] + 9),
                                   criteria=(
                                   len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                   dataset.data.shape[1] + 6),
                                   sum_range=(3,
                                              dataset.data.shape[1] + 8,
                                              len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                              dataset.data.shape[1] + 8))

            mean_i = sum_i + '/' + \
                     formula.count_if(criteria_range=(3,
                                                      dataset.data.shape[1] + 9,
                                                      len(dataset.preference) * (
                                                                  len(dataset.preference) - 1) // 2 + 2,
                                                      dataset.data.shape[1] + 9),
                                      criteria=(
                                      len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                      dataset.data.shape[1] + 6))

            max_i = '=' + \
                    formula.max_ifs(max_range=(3,
                                               dataset.data.shape[1] + 8,
                                               len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                               dataset.data.shape[1] + 8),
                                    criteria_range=(3,
                                                    dataset.data.shape[1] + 9,
                                                    len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                                    dataset.data.shape[1] + 9),
                                    criteria=(
                                    len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                    dataset.data.shape[1] + 6))

            min_i = '=' + \
                    formula.min_ifs(min_range=(3,
                                               dataset.data.shape[1] + 8,
                                               len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                               dataset.data.shape[1] + 8),
                                    criteria_range=(3,
                                                    dataset.data.shape[1] + 9,
                                                    len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                                    dataset.data.shape[1] + 9),
                                    criteria=(
                                    len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                    dataset.data.shape[1] + 6))

            min_max_i = '=-' + \
                        formula.get_cell(
                            cell=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                  dataset.data.shape[1] + 10)) + \
                        '/' + \
                        formula.get_cell(
                            cell=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                  dataset.data.shape[1] + 9))

            sum_pos = '=' + \
                      formula.sum_ifs(sum_range=(3,
                                                 dataset.data.shape[1] + 8,
                                                 len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                                 dataset.data.shape[1] + 8),
                                      criteria_range_1=(3,
                                                        dataset.data.shape[1] + 9,
                                                        len(dataset.preference) * (
                                                                    len(dataset.preference) - 1) // 2 + 2,
                                                        dataset.data.shape[1] + 9),
                                      criteria_1=(
                                      len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                      dataset.data.shape[1] + 6),
                                      criteria_range_2=(3,
                                                        dataset.data.shape[1] + 8,
                                                        len(dataset.preference) * (
                                                                    len(dataset.preference) - 1) // 2 + 2,
                                                        dataset.data.shape[1] + 8),
                                      criteria_2='>0')

            sum_neg = '=' + \
                      formula.sum_ifs(sum_range=(3,
                                                 dataset.data.shape[1] + 8,
                                                 len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 2,
                                                 dataset.data.shape[1] + 8),
                                      criteria_range_1=(3,
                                                        dataset.data.shape[1] + 9,
                                                        len(dataset.preference) * (
                                                                    len(dataset.preference) - 1) // 2 + 2,
                                                        dataset.data.shape[1] + 9),
                                      criteria_1=(
                                      len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                      dataset.data.shape[1] + 6),
                                      criteria_range_2=(3,
                                                        dataset.data.shape[1] + 8,
                                                        len(dataset.preference) * (
                                                                    len(dataset.preference) - 1) // 2 + 2,
                                                        dataset.data.shape[1] + 8),
                                      criteria_2='<0')

            pos_neg_i = '=-' + \
                        formula.get_cell(
                            cell=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                  dataset.data.shape[1] + 13)) + \
                        '/' + \
                        formula.get_cell(
                            cell=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                  dataset.data.shape[1] + 12))

            is_minimal_i = '=' + \
                           formula.check_presence(
                               criteria=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 10 + index,
                                         dataset.data.shape[1] + 6),
                               cell=(len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 4,
                                     dataset.data.shape[1] + 8))

            result.append((sum_i, mean_i, max_i, min_i, min_max_i, sum_pos, sum_neg, pos_neg_i, is_minimal_i))

    result = pd.DataFrame(result,
                          columns=['Sum', 'Mean', 'Max', 'Min', '-Min/Max', 'SumPos', 'SumNeg', '-SumNeg/SumPos',
                                   'Is Minimal'],
                          index=result_index)
    result.index.name = 'Minimal Set'

    if excel is None:
        print('[Statistics of Minimal D-separators]')
        print('No representation for "stdout" implemented')
        print()
        print()

    else:
        excel.write_dataframe(result,
                              startrow=len(dataset.preference) * (len(dataset.preference) - 1) // 2 + 7,
                              startcol=dataset.data.shape[1] + 5,
                              title='Statistics of Minimal D-separators',
                              color=True,
                              invert_color=[True, True, True, True, True, True, True, False, False],
                              color_axis='column')
