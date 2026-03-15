import bisect
import heapq
from typing import override

import numpy as np

from skylines.dataset import *
from skylines.skyline import Skyline
from skylines.common.utils import scale_minmax


class LESSSkyline(Skyline):

    def __init__(self, dataset: Dataset, page_size: int = 16, buffer_size: int = 64, window_size: int = 4):
        super().__init__(dataset)

        # page size and window size are needed in terms of tuples
        self.buffer_size = buffer_size * page_size
        self.window_size = window_size * page_size

        # merge fanin is needed in terms of pages
        self.merge_fanin = buffer_size

    def pass_0(self, data: np.ndarray, index: np.ndarray):
        ef_window = []
        blocks = []

        for i in range(0, data.shape[0], self.buffer_size):
            # slice the data and compute entropy
            block = {index[j]: (data[j], np.sum(np.log1p(data[j]))) for j in range(i, min(i + self.buffer_size, data.shape[0]))}
            # block = {index[j]: (data[j], np.sum(data[j])) for j in range(i, min(i + self.buffer_size, data.shape[0]))}

            # discard tuples from input stream
            for idx, (entry, _) in list(block.items()):
                for ef, _ in ef_window:
                    if self.is_dominating(ef, entry):
                        del block[idx]
                        break

            # sort by entropy
            sorted_keys = sorted(block, key=lambda k: block[k][1], reverse=True)
            block = {k: block[k] for k in sorted_keys}

            if block:
                # clean up window
                highest = block[next(iter(block))]
                ef_window = [ef for ef in ef_window if not self.is_dominating(highest[0], ef[0])]

                # add to window, sorted in descending order of entropy
                insert_pos = bisect.bisect_left([-e for (_, e) in ef_window], -highest[1])
                ef_window.insert(insert_pos, highest)

                # remove worst on overflow
                if self.window_size and len(ef_window) > self.window_size:
                    worst_idx = min(range(len(ef_window)), key=lambda i: ef_window[i][1])
                    ef_window.pop(worst_idx)

                # add to list
                blocks.append(block)
        
        return [[(idx, entry, entropy) for idx, (entry, entropy) in block.items()] for block in blocks]
    
    def pass_i(self, blocks: list[list[tuple[int, np.ndarray, float]]]):
        while len(blocks) > self.merge_fanin:
            new_blocks = []

            # process blocks in chunks of size fanin
            for start in range(0, len(blocks), self.merge_fanin):
                group = blocks[start : start + self.merge_fanin]

                # m-way merge over this group
                pointers = [0] * len(group)
                heap = []

                # init heap with first element from each non-empty block in group
                for b_id, block in enumerate(group):
                    if not block:
                        continue
                    idx, row, entropy = block[0]
                    heapq.heappush(heap, (-entropy, b_id, idx, row))

                # merge
                merged = []
                while heap:
                    # globally next-highest tuple
                    neg_entropy, b_id, idx, row = heapq.heappop(heap)
                    entropy = -neg_entropy

                    # append
                    merged.append((idx, row, entropy))

                    # move pointer for this block
                    pointers[b_id] += 1
                    p = pointers[b_id]

                    # if block still has elements, push next one
                    if p < len(group[b_id]):
                        next_idx, next_row, next_entropy = group[b_id][p]
                        heapq.heappush(heap, (-next_entropy, b_id, next_idx, next_row))

                new_blocks.append(merged)

            # repeat the process
            blocks = new_blocks

        return blocks

    def pass_f(self, blocks: list[list[tuple[int, np.ndarray, float]]]):
        # pointers for each block
        pointers = [0] * len(blocks)

        # heap will contain: (-entropy, block_id, idx, row)
        heap = []

        # initialize heap with the first element of each non-empty block
        for b_id, block in enumerate(blocks):
            if len(block) == 0:
                continue
            idx, row, entropy = block[0]
            heapq.heappush(heap, (-entropy, b_id, idx, row))

        skyline = dict()   # will contain (idx, row)

        # merge
        while heap:
            # globally next-highest tuple
            neg_entropy, b_id, idx, row = heapq.heappop(heap)
            entropy = -neg_entropy

            # append if not dominated
            for idx_s, row_s in list(skyline.items()):
                if self.is_dominating(row_s, row):
                    break
            else:
                skyline[idx] = row

            # move pointer for this block
            pointers[b_id] += 1
            p = pointers[b_id]

            # if block still has elements, push next one
            if p < len(blocks[b_id]):
                next_idx, next_row, next_entropy = blocks[b_id][p]
                heapq.heappush(heap, (-next_entropy, b_id, next_idx, next_row))

        return skyline

    @override
    def find_skyline(self, index: np.ndarray, *args) -> np.ndarray:
        data = self.data[np.ix_(index, list(self.preferences.values()))]
        data = scale_minmax(data)

        # split and sort
        blocks = self.pass_0(data, index)

        # intermediate merge
        blocks = self.pass_i(blocks)

        # final merge
        skyline = self.pass_f(blocks)

        return np.array(list(skyline.keys()))
