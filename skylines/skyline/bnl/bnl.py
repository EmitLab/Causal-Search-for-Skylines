from typing import override

import numpy as np

from skylines.dataset import *
from skylines.skyline import Skyline


class BNLSkyline(Skyline):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        data = self.data[np.ix_(index, list(self.preferences.values()))]

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
