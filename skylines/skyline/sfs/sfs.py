from typing import override

import numpy as np

from skylines.dataset import *
from skylines.skyline import Skyline
from skylines.common.utils import scale_minmax


class SFSSkyline(Skyline):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        data = self.data[np.ix_(index, list(self.preferences.values()))]
        data = scale_minmax(data)

        sort_order = np.argsort(-data.sum(axis=1))
        # sort_order = np.argsort(-np.sum(np.log1p(data), axis=1))

        index = index[sort_order]
        data = data[sort_order]

        skyline = dict()

        for relative_i, row_i in enumerate(data):
            i = index[relative_i]

            for j, row_j in list(skyline.items()):
                if self.is_dominating(row_j, row_i):
                    break
            else:
                skyline[i] = row_i

        return np.array(list(skyline.keys()))
