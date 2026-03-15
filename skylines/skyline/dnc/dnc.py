import operator
from typing import override

import numpy as np

from skylines.common.utils import time_function
from skylines.dataset import Dataset
from skylines.skyline import Skyline


class DnCSkyline(Skyline):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)
        self.time_handled = True
        self.merge_mode = False
        self.merge_time = (0, 0, 0, 0)

    @property
    def total_time(self):
        return self.cluster_time \
            + sum(sum(t) for t in self.compute_time) \
            + sum(self.merge_time)

    @property
    def parallel_time(self):
        return self.cluster_time \
            + max(t[0] + max(t[1], t[2]) + t[3] for t in self.compute_time) \
            + self.merge_time[0] + max(self.merge_time[1], self.merge_time[2]) + self.merge_time[3]

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        data = self.data[np.ix_(index, list(self.preferences.values()))]
        skyline = self.find_skyline_recursive(data, np.arange(len(index)), len(self.dataset.preference) - 1, 0)
        return index[skyline]

    def find_skyline_trivial(self, data, index: np.ndarray) -> np.ndarray:
        data = data[index]
        skyline = dict()

        for relative_i, row_i in enumerate(data):
            i = index[relative_i]

            for j, row_j in list(skyline.items()):
                if self.is_dominating(row_j, row_i):
                    break
                elif self.is_dominating(row_i, row_j):
                    del skyline[j]
            else:
                skyline[i] = row_i

        return np.array(list(skyline.keys()))

    def _add_compute_time(self, timing):
        if self.merge_mode:
            self.merge_time = timing
        else:
            self.compute_time.append(timing)

    def find_skyline_recursive(self, data: np.ndarray, index: np.ndarray, dimension: int, depth: int) -> np.ndarray:
        # trivial case: only one tuple
        if len(index) == 1 or dimension == -1:
            return index

        # trivial case: very few tuples
        if len(index) < 100:
            result, elapsed = time_function(self.find_skyline_trivial, data, index)
            if depth == 0:
                self._add_compute_time((elapsed, 0, 0, 0))
            return result

        # record the common time
        common_time = 0

        # compute the pivot
        pivot, elapsed = time_function(self.mean, data[index, dimension])
        common_time += elapsed

        # partition the data
        (left, right), elapsed = time_function(self.partition, data, index, dimension, pivot)
        common_time += elapsed

        # all elements are equal for dimension
        if len(left) == 0 or len(right) == 0:
            skyline, elapsed = time_function(self.find_skyline_recursive, data, index, dimension - 1, depth + 1)
            if depth == 0:
                self._add_compute_time((common_time, 0, 0, elapsed))
            return skyline

        # dimension is low, directly eliminate
        if dimension == 0:
            skyline, elapsed = time_function(self.find_skyline_recursive, data, right, dimension, depth + 1)
            if depth == 0:
                self._add_compute_time((common_time, 0, 0, elapsed))
            return skyline

        # compute skyline recursively
        left_skyline, left_elapsed = time_function(self.find_skyline_recursive, data, left, dimension, depth + 1)
        right_skyline, right_elapsed = time_function(self.find_skyline_recursive, data, right, dimension, depth + 1)

        # merge skyline
        merged, merge_elapsed = time_function(self.merge, data, left_skyline, right_skyline, dimension)
        skyline, concat_elapsed = time_function(np.concatenate, (merged, right_skyline))

        if depth == 0:
            self._add_compute_time((common_time, left_elapsed, right_elapsed, merge_elapsed + concat_elapsed))

        return skyline

    def merge(self, data: np.ndarray, left_skyline: np.ndarray, right_skyline: np.ndarray, dimension: int) -> np.ndarray:
        skyline = []

        # trivial case: right skyline is empty
        if len(right_skyline) == 0:
            skyline = left_skyline

        # trivial case: left skyline is empty
        elif len(left_skyline) == 0:
            pass

        # trivial case: right skyline has only one element
        elif len(right_skyline) == 1:
            right_value = data[right_skyline[0]]
            left_values = data[left_skyline]
            for relative_i, row_i in enumerate(left_values):
                i = left_skyline[relative_i]
                if not self.is_dominating(right_value, row_i):
                    skyline.append(i)

        # trivial case: left skyline has only one element
        elif len(left_skyline) == 1:
            left_value = data[left_skyline[0]]
            right_values = data[right_skyline]
            for row_i in right_values:
                if self.is_dominating(row_i, left_value):
                    break
            else:
                skyline = left_skyline

        # trivial case: dimension is low
        elif dimension == 1:
            right_max = data[right_skyline, dimension - 1].max()
            left_values = data[left_skyline, dimension - 1]
            for relative_i, row_i in enumerate(left_values):
                i = left_skyline[relative_i]
                self.comparisons += 1
                if row_i > right_max:
                    skyline.append(i)

        else:
            # find pivot for next dimension of right skyline
            pivot = self.mean(data[right_skyline, dimension - 1])

            # partition the skyline
            left_left_skyline, right_left_skyline = self.partition(data, left_skyline, dimension - 1, pivot)
            left_right_skyline, right_right_skyline = self.partition(data, right_skyline, dimension - 1, pivot)

            # edge case: cannot partition by next dimension, skip
            if len(left_left_skyline) == 0 and len(left_right_skyline) == 0:
                left_left_skyline, right_left_skyline = self.partition(data, left_skyline, dimension - 1, pivot, operator.le)
                skyline_1 = self.merge(data, left_left_skyline, right_right_skyline, dimension - 1)
                skyline = np.concatenate((skyline_1, right_left_skyline))

            # recursively merge
            else:
                skyline_1 = self.merge(data, left_left_skyline, left_right_skyline, dimension)
                skyline_2 = self.merge(data, right_left_skyline, right_right_skyline, dimension)
                skyline_3 = self.merge(data, skyline_1, right_right_skyline, dimension - 1)
                skyline = np.concatenate((skyline_2, skyline_3))

        return np.array(skyline, dtype=int)

    def mean(self, data: np.ndarray) -> float:
        return data[0] if np.all(data == data[0]) else data.mean()

    def partition(self, data: np.ndarray, index: np.ndarray, dimension: int, pivot, comparator: operator = operator.lt) -> (np.ndarray, np.ndarray):
        self.comparisons += len(index)
        mask = comparator(data[index, dimension], pivot)
        return index[mask], index[~mask]
