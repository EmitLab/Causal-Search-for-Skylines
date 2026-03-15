from typing import override

import numpy as np

from skylines import n_bins
from skylines.dataset import Dataset
from skylines.skyline import CausalSkyline
from skylines.skyline.bnl import BNLSkyline


class BNLCausalSkyline(CausalSkyline, BNLSkyline):

    def __init__(self, dataset: Dataset, clusterby: frozenset, bins: int = n_bins):
        super().__init__(dataset, clusterby, bins)

    @override
    def _merge(self, skylines: list[np.ndarray]) -> np.ndarray:
        skyline = dict()

        for index in skylines:
            if len(index) == 0:
                continue

            selected = dict()

            data = self.data[np.ix_(index, list(self.preferences.values()))]

            for relative_i, row_i in enumerate(data):
                i = index[relative_i]

                for j, row_j in list(skyline.items()):
                    if self.is_dominating(row_j, row_i):
                        break
                    elif self.is_dominating(row_i, row_j):
                        del skyline[j]
                else:
                    selected[i] = row_i

            skyline.update(selected)

        return np.array(list(skyline.keys()))



class BNLCausalHMSkyline(CausalSkyline, BNLSkyline):

    def __init__(self, dataset: Dataset, clusterby: frozenset, bins: int = n_bins):
        super().__init__(dataset, clusterby, bins)

    @override
    def _merge(self, skylines: list[np.ndarray]) -> np.ndarray:
        # only one skyline
        if len(skylines) == 1:
            return skylines[0]

        # two skyline, merge
        if len(skylines) == 2:
            skyline = {skylines[0][i]: row_i for i, row_i in enumerate(self.data[np.ix_(skylines[0], list(self.preferences.values()))])}

            data = self.data[np.ix_(skylines[1], list(self.preferences.values()))]
            selected = dict()

            for relative_i, row_i in enumerate(data):
                i = skylines[1][relative_i]

                for j, row_j in list(skyline.items()):
                    if self.is_dominating(row_j, row_i):
                        break
                    elif self.is_dominating(row_i, row_j):
                        del skyline[j]
                else:
                    selected[i] = row_i

            skyline.update(selected)

            return np.array(list(skyline.keys()))

        # more than two skyline, partition
        mid = len(skylines) // 2
        left = skylines[:mid]
        right = skylines[mid:]

        merged_left = self._merge(left)
        merged_right = self._merge(right)

        # merge left and right partitions
        return self._merge([merged_left, merged_right])
