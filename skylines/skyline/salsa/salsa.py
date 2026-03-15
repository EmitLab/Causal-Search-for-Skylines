from typing import override

import numpy as np

from skylines.dataset import *
from skylines.skyline import Skyline
from skylines.common.utils import scale_minmax


class SaLSaSkyline(Skyline):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        data = self.data[np.ix_(index, list(self.preferences.values()))]
        data = scale_minmax(data)

        monotonic_scores = np.column_stack((data.max(axis=1), data.sum(axis=1)))
        sort_order = np.lexsort(-monotonic_scores.T[::-1])

        monotonic_scores = monotonic_scores[sort_order]
        index = index[sort_order]
        data = data[sort_order]

        skyline = dict()
        pstop = None

        for relative_i, row_i in enumerate(data):
            i = index[relative_i]

            for j, row_j in list(skyline.items()):
                if self.is_dominating(row_j, row_i):
                    break
            else:
                skyline[i] = row_i
                if pstop is None or row_i.min() > pstop.min():
                    pstop = row_i

            if self._check_pstop(monotonic_scores[relative_i], pstop):
                break

        return np.array(list(skyline.keys()))

    def _check_pstop(self, monotonic_score, pstop):
        for score in monotonic_score:
            if score < pstop.min():
                return True
            elif score > pstop.min():
                return False
        return False
