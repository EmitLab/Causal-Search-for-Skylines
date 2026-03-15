import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from skylines.common.excel import Excel
from skylines.dataset import Dataset


def plot_heatmap(dataset: Dataset,
                 matrix: pd.DataFrame,
                 title: str = None,
                 xlabel: str = None,
                 ylabel: str = None,
                 excel: Excel = None,
                 startrow: int = 0,
                 startcol: int = 0,
                 invert_color: bool = False):
    if excel is None:
        plt.figure(dpi=150)

        # plot heatmap
        ax = sns.heatmap(matrix, annot=True)

        # mark confounders on x-axis
        for tick_label in ax.get_xticklabels():
            if tick_label.get_text() in dataset.control:
                tick_label.set_color('red')
                tick_label.set_fontweight('bold')

        # mark confounders on y-axis
        for tick_label in ax.get_yticklabels():
            if tick_label.get_text() in dataset.control:
                tick_label.set_color('red')
                tick_label.set_fontweight('bold')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()

    else:
        excel.write_dataframe(matrix, startrow, startcol, title, color=True, invert_color=invert_color)


def plot_graph(dataset: Dataset,
               matrix: pd.DataFrame,
               title: str = None,
               edge_label: bool = True,
               excel: Excel = None,
               startrow: int = 0,
               startcol: int = 0):
    plt.figure(dpi=150)

    edges = matrix.where(matrix != 0).stack().index.tolist()
    node_labels = {column: column for column in matrix.columns}
    edge_labels = {edge: round(matrix.at[edge[0], edge[1]], 2) for edge in edges}

    graph = nx.DiGraph()
    graph.add_nodes_from(matrix.columns)
    graph.add_edges_from(edges)

    pos = nx.shell_layout(graph)

    nx.draw_networkx_nodes(graph, pos,
                           node_size=[max(len(node) * 500, 2000) for node in graph.nodes],
                           node_color=['#F08080' if node in dataset.control else '#5F9EA0' for node in graph.nodes])
    nx.draw_networkx_edges(graph, pos,
                           node_size=[max(len(node) * 500, 2000) for node in graph.nodes],
                           edge_color='#AAAAAA',
                           arrowsize=20)
    nx.draw_networkx_labels(graph, pos, node_labels,
                            font_color='white',
                            font_weight='bold')
    if edge_label:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)

    plt.title(label=title)
    plt.axis('off')
    plt.tight_layout()

    if excel is None:
        plt.show()
    else:
        excel.write_image(startrow, startcol)
