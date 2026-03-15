from skylines import n_bins
from skylines.dataset import Dataset
from skylines.skyline import CausalSkyline
from skylines.skyline.sfs import SFSSkyline


class SFSCausalSkyline(CausalSkyline, SFSSkyline):

    def __init__(self, dataset: Dataset, clusterby: frozenset, bins: int = n_bins):
        super().__init__(dataset, clusterby, bins)
