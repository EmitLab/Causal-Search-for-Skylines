from typing import override

from skylines.dataset import Dataset
from skylines.skyline import Skyline
from .rtree import *


class BBSSkyline(Skyline):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)

    @override
    def is_dominating(self, mbr1: MBR, mbr2: MBR) -> bool:
        self.comparisons += 1
        dominating = False
        for i in range(len(self.dataset.preference)):
            if mbr1.min_dim[i] < mbr2.max_dim[i]:
                return False
            elif mbr1.min_dim[i] > mbr2.max_dim[i]:
                dominating = True
        return dominating

    @override
    def preprocess(self, index: np.ndarray) -> list:
        return [self.form_rtree(index)]

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        rtree: RTree = args[0]

        data = self.data[np.ix_(index, list(self.preferences.values()))]

        heap = Heap(data)
        heap.push(rtree.root)

        skyline = []

        while not heap.empty():
            entry: Entry = heap.pop()

            for item in skyline:
                if self.is_dominating(item.mbr, entry.mbr):
                    break
            else:
                if entry.node.is_leaf():
                    skyline.append(entry)
                else:
                    heap.push(entry.child)

        skyline = [entry.child for entry in skyline]

        return np.array(skyline)

    def form_rtree(self, index: np.ndarray) -> RTree:
        data = self.data[np.ix_(index, list(self.preferences.values()))]
        M = 4096 // (16 * len(self.preferences) + 8)
        rtree: RTree = RTree(M, M // 2)
        for relative_i, row_i in enumerate(data):
            i = index[relative_i]
            rtree.insert(Entry(MBR(row_i.tolist(), row_i.tolist()), i))
        return rtree
