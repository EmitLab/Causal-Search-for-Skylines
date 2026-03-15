from typing import override

import numpy as np

from skylines import n_bins
from skylines.dataset import Dataset
from skylines.skyline import CausalSkyline
from skylines.skyline.dnc import DnCSkyline


class DnCCausalSkyline(CausalSkyline, DnCSkyline):

    def __init__(self, dataset: Dataset, clusterby: frozenset, bins: int = n_bins):
        super().__init__(dataset, clusterby, bins)

    @override
    def _merge(self, group_skylines: list[np.ndarray]) -> np.ndarray:
        self.merge_mode = True
        return super()._merge(group_skylines)
