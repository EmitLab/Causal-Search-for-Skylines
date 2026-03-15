from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from skylines.common import utils
from skylines.common.index import Index
from skylines.common.utils import time_function
from skylines.dataset import Dataset
from skylines.dataset import Dominance


class Skyline(ABC):

    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.data, self.variates, self.preferences = dataset.to_numpy()

        self.comparisons = 0

        self.cluster_time = 0
        self.compute_time = []
        self.merge_time = 0
        self.time_handled = False

    @property
    def total_time(self):
        return self.cluster_time + sum(self.compute_time) + self.merge_time

    @property
    def parallel_time(self):
        return self.cluster_time + max(self.compute_time) + self.merge_time

    def is_dominating(self, row1, row2) -> bool:
        self.comparisons += 1
        dominating = False
        for i in range(len(self.preferences)):
            if row1[i] < row2[i]:
                return False
            elif row1[i] > row2[i]:
                dominating = True
        return dominating

    def compute(self) -> pd.DataFrame:
        # get the index
        index: np.ndarray = np.arange(len(self.data))

        # preprocess
        args = self.preprocess(index)

        # find the skyline for the entire data
        skyline, elapsed = time_function(self.find_skyline, index, *args)
        if not self.time_handled:
            self.compute_time.append(elapsed)

        # convert indices back to data
        skyline = self.dataset.data.iloc[skyline]
        skyline = skyline.sort_index().sort_values(by=self.dataset.preference)

        return skyline

    def preprocess(self, index: np.ndarray) -> list:
        return []

    @abstractmethod
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        pass



class CausalSkyline(Skyline, ABC):

    def __init__(self, dataset: Dataset, clusterby: frozenset, bins: int):
        super().__init__(dataset)
        self.clusterby = clusterby
        self.bins = bins

    def compute(self) -> pd.DataFrame:
        # group based on clusterby
        groups, elapsed = time_function(utils.cluster, self.data, list(self.preferences.values()), [self.variates[col] for col in self.clusterby], self.bins)
        self.cluster_time = elapsed

        # store indices
        index = Index(self.dataset, self.clusterby, 'w')
        index.write_index(groups)

        # find skyline for each group
        group_skylines = []
        for group in groups:
            # preprocess
            args = self.preprocess(group)

            # find skyline for group
            group_skyline, elapsed = time_function(self.find_skyline, group, *args)
            if not self.time_handled:
                self.compute_time.append(elapsed)

            group_skylines.append(group_skyline)

        # find the actual skyline
        skyline, elapsed = time_function(self._merge, group_skylines)
        if not self.time_handled:
            self.merge_time = elapsed

        # write the skyline
        index.write_skyline(skyline, group_skylines)

        # convert indices back to data
        skyline = self.dataset.data.iloc[skyline]
        skyline = skyline.sort_index().sort_values(by=self.dataset.preference)

        return skyline

    def _merge(self, group_skylines: list[np.ndarray]) -> np.ndarray:
        # concatenate group skyline
        rough_skyline = []
        for group_skyline in group_skylines:
            rough_skyline.extend(group_skyline)
        rough_skyline = np.array(rough_skyline)

        # preprocess
        args = self.preprocess(rough_skyline)

        # find the actual skyline
        skyline = self.find_skyline(rough_skyline, *args)

        return skyline
