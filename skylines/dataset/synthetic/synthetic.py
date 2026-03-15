import json
import networkx as nx
import numpy as np
import pandas as pd

from skylines import infer_graph, skip_inference
from skylines.common.state import get_state
from skylines.dataset import Dataset, Dominance


class SyntheticDataset(Dataset):

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
                 seed: int = 42,
                 noise: float = 0.1,
                 actual_name: str = None):

        self.noise = noise

        super().__init__(control=control,
                         preference=preference,
                         effect=effect,
                         dominance=dominance,
                         infer_controls=infer_controls,
                         masked_nodes=masked_nodes,
                         masked_edges=masked_edges,
                         infer_graph=infer_graph,
                         size=size,
                         seed=seed)

        if not skip_inference and self.infer_controls is not None:
            dataset: Dataset = SyntheticDataset(control=self.control,
                                                preference=self.preference,
                                                effect=self.effect,
                                                dominance=self.infer_controls,
                                                infer_controls=None,
                                                masked_nodes=self.masked_nodes,
                                                masked_edges=self.masked_edges,
                                                infer_graph=infer_graph,
                                                size=self.size,
                                                seed=self.seed,
                                                noise=self.noise,
                                                actual_name=self.name)
 
            from skylines.common.heuristic import best_controls
            self.constant_controls = best_controls(dataset)

        self._data = self._generate()

        if not skip_inference and self.infer_graph:
            self._graph = None
            self._masked_graph = None
            if actual_name is None:
                actual_name = self.name
            with open(f'graphs/{actual_name}.json', 'r') as f:
                self.effect = json.load(f)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    def _generate(self) -> pd.DataFrame:
        # specify seed for reproducibility
        np.random.seed(seed=self.seed)

        # create empty dataframe
        df = pd.DataFrame()

        # compute the standard deviation
        std = dict()
        for var in self.variates:
            # high standard deviation if no parents
            if self.graph.in_degree(var) == 0:
                std[var] = 1.0

            # low standard deviation otherwise
            else:
                std[var] = self.noise

        # generate the confounding variates
        for cont in self.control:
            df[cont] = np.random.normal(size=self.size, scale=std[cont])

        # generate the preference variates
        for pref in self.preference:
            df[pref] = np.random.normal(size=self.size, scale=std[pref])

        # adjust based on effects
        for effect in nx.topological_sort(self.graph):
            for cause in self.graph.predecessors(effect):
                df[effect] += df[cause] * self.graph[cause][effect]['weight']

        # fill NaNs
        df = df.fillna(df.max() + df.std())

        # store the data
        # file_path = get_state().get_file('data', f'{self.name}.csv')
        # df.to_csv(file_path)

        return df
