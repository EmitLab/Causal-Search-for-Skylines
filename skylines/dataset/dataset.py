from abc import ABC, abstractmethod
from enum import Enum

import networkx as nx
import numpy as np
import pandas as pd

from skylines import infer_graph
from skylines.common.utils import format_num, safe_str


class Dominance(Enum):
    MIN = 'min'
    MAX = 'max'


class Dataset(ABC):

    def __init__(self,
                 control: list[str],
                 preference: list[str],
                 effect: dict[str, dict[str, float]],
                 dominance: dict[str, Dominance] = None,
                 infer_controls: dict[str, Dominance] = None,
                 masked_nodes: list[str] = None,
                 masked_edges: list[tuple[str, str]] = None,
                 infer_graph: bool = infer_graph,
                 size: int = 10000,
                 seed: int = 42):

        self.control = [safe_str(c) for c in control]
        self.preference = [safe_str(p) for p in preference]
        self.effect = {safe_str(snk): {safe_str(src): eff for src, eff in srcs.items()} for snk, srcs in effect.items()}

        if dominance is None:
            self.dominance = {safe_str(pref): Dominance.MAX for pref in self.preference}
        else:
            self.dominance = {safe_str(v): d for v, d in dominance.items()}

        if infer_controls is None:
            self.infer_controls = None
        else:
            self.infer_controls = {safe_str(v): d for v, d in infer_controls.items()}

        self.constant_controls: list[frozenset[str]] | None = None

        if masked_nodes is None:
            self.masked_nodes = None
        else:
            self.masked_nodes = [safe_str(n) for n in masked_nodes]

        if masked_edges is None:
            self.masked_edges = None
        else:
            self.masked_edges = [(safe_str(src), safe_str(snk)) for src, snk in masked_edges]

        if size is None:
            self.size = 10000
        else:
            self.size = size
        
        if seed is None:
            self.seed = 42
        else:
            self.seed = seed

        # self.strength = strength
        self.infer_graph = infer_graph

        self._graph = None
        self._masked_graph = None

    @property
    def name(self) -> str:
        return f'{self.__class__.__name__}_{self.dominance_key}_{format_num(self.size)}_{self.seed}'

    @property
    def variates(self) -> list[str]:
        return self.control + self.preference

    @property
    def dominance_key(self) -> str:
        return ''.join(['X' if self.dominance[pref] == Dominance.MAX else 'N' for pref in sorted(self.preference)])

    @property
    def graph(self) -> nx.DiGraph:
        if self._graph is None:
            # form the adjacency matrix
            matrix = pd.DataFrame(0.0, columns=self.variates, index=self.variates)

            # set weights based on effect
            for effect, causes in self.effect.items():
                for cause, weight in causes.items():
                    matrix.at[cause, effect] = weight

            # generate the weighted edge list
            edges = [(*k, v) for k, v in matrix.where(matrix != 0).stack().to_dict().items()]

            # generate the graph
            graph = nx.DiGraph()
            graph.add_nodes_from(matrix.columns)
            graph.add_weighted_edges_from(edges)

            # # changed weights to those found by CATE if available
            # if self.strength:
            #     # remove unobserved nodes
            #     sparse = graph.copy()
            #     for node in list(graph.nodes):
            #         if node not in self.variates:
            #             sparse.remove_node(node)

            #     # update weights
            #     edge_weights = arrow_strength(self.data, sparse)
            #     for (src, snk), value in edge_weights.items():
            #         graph[src][snk]['weight'] = value

            self._graph = graph

        return self._graph

    @property
    def masked_graph(self):
        if self._masked_graph is None:
            self._masked_graph = self.graph.copy()

            if self.masked_nodes is not None:
                self._masked_graph.remove_nodes_from(self.masked_nodes)

            if self.masked_edges is not None:
                self._masked_graph.remove_edges_from(self.masked_edges)

        return self._masked_graph

    @property
    def adjmat(self) -> pd.DataFrame:
        return nx.to_pandas_adjacency(self.graph, weight='weight')

    @property
    @abstractmethod
    def data(self) -> pd.DataFrame:
        raise NotImplementedError

    def to_numpy(self) -> (np.ndarray, dict[str, int], dict[str, int]):
        # create a copy to prevent tampering the original data
        df: pd.DataFrame = self.data.copy()

        # invert data for MIN preference attributes
        for pref in self.preference:
            if self.dominance[pref] == Dominance.MIN:
                df[pref] = df[pref].max() - df[pref]

        # column index for variates and preferences
        variates: dict[str, int] = {column: index for index, column in enumerate(df.columns)}
        preferences: dict[str, int] = {column: index for index, column in enumerate(df.columns) if column in self.preference}

        return df.values, variates, preferences
