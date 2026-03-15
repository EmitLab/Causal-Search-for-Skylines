from enum import Enum
from typing import Self

from .mbr import MBR


class NodeType(Enum):
    ROOT = 1
    INTERMEDIATE = 2
    LEAF = 3


class Node:

    def __init__(self, node_type = NodeType.LEAF):
        self.parent = None
        self.entries = []
        self.node_type = node_type

    '''
    Split the current node to resolve the overflow
    Using Quadratic split
    '''
    def split(self, m: int):
        # split into entry_1 and entry_2
        entry_1, entry_2 = self.pick_seed()
        self.entries.remove(entry_1)
        self.entries.remove(entry_2)

        # create two nodes
        node_1 = Node(self.node_type)
        node_1.entries.append(entry_1)
        node_1.parent = self.parent
        if self.parent is not None:
            self.parent.child = node_1

        node_2 = Node(self.node_type)
        node_2.entries.append(entry_2)

        while len(self.entries) > 0:
            # check for shortage in any group
            if len(node_1.entries) + len(self.entries) < m:
                for entry in self.entries:
                    node_1.entries.append(entry)
                self.entries = []
                break
            elif len(node_2.entries) + len(self.entries) < m:
                for entry in self.entries:
                    node_2.entries.append(entry)
                self.entries = []
                break

            # get the next entry for insertion in a group    
            next_key = self.pick_next(node_1, node_2)

            # get the enlargement in both groups after adding new entry
            enlargement_node_1 = node_1.MBR().combine(next_key.mbr).area
            enlargement_node_2 = node_2.MBR().combine(next_key.mbr).area

            # add the new entry to the group with least enlargement
            if enlargement_node_1 <= enlargement_node_2:
                next_key.node = node_1
                node_1.entries.append(next_key)
            else:
                next_key.node = node_2
                node_2.entries.append(next_key)

            self.entries.remove(next_key)

        # update node property for all entries in node_1 and node_2
        for entry in node_1.entries:
            entry.node = node_1
        for entry in node_2.entries:
            entry.node = node_2

        # return the split two nodes
        return [node_1, node_2]

    '''
    PickSeed Subroutine for Quadratic split
    Return two seed entries
    '''
    def pick_seed(self):
        # initialize entries to empty nodes
        entry_1 = None
        entry_2 = None
        
        # initialize max expandable area to minimum
        max_expandable_area = -float("inf")

        # get some values from self node for use
        for i in range(0, len(self.entries)):
            entry_i = self.entries[i]
            for j in range(i + 1, len(self.entries)):
                entry_j = self.entries[j]

                # get the combined region of entry_i and entry_j
                combined_region = entry_i.mbr.combine(entry_j.mbr)

                # calculate the expandable area b
                expandable_area = combined_region.area - entry_i.mbr.area - entry_j.mbr.area

                # update area and nodes for output
                if expandable_area > max_expandable_area:
                    max_expandable_area = expandable_area
                    entry_1 = entry_i
                    entry_2 = entry_j

        # return Node list
        return [entry_1, entry_2]

    '''
    Subroutine for Quadratic split
    N = 
    '''
    def pick_next(self, node_1: Self, node_2: Self):
        # initialize max expandable area to minimum
        max_expandable_area = -float("inf")
        max_entry = None

        # get mbr for N1 and N2
        node_1_mbr = node_1.MBR()
        node_2_mbr = node_2.MBR()

        for entry in self.entries:
            # get the combined area by adding entry to both N1 and N2
            node_1_combined = node_1_mbr.combine(entry.mbr)
            node_2_combined = node_2_mbr.combine(entry.mbr)

            # get area difference of areas after addition and before addition 
            d1 = node_1_combined.area - node_1_mbr.area
            d2 = node_2_combined.area - node_2_mbr.area

            # get the difference of these expandable areas
            expandable_area = abs(d1 - d2)

            # update return entry value if necessary
            if max_expandable_area < expandable_area:
                max_expandable_area = expandable_area
                max_entry = entry

        return max_entry

    '''
    Is Node full
    '''
    def is_full(self, M: int):
        return len(self.entries) == M

    '''
    Get the mbr for Node
    '''
    def MBR(self):
        entries = self.entries
        if len(entries) > 0:
            mbr = MBR(entries[0].mbr.min_dim, entries[0].mbr.max_dim)
            for entry in entries[1:]:
                mbr = mbr.combine(entry.mbr)
            return mbr
        return None

    """
    Return whether a node underflows or not
    """
    def underflows(self, m: int):
        return len(self.entries) < m

    """
    Returns whether node overflows or not
    """
    def overflows(self, M: int):
        return len(self.entries) > M

    """
    Return whether node is leaf or not
    """
    def is_leaf(self):
        return self.node_type == NodeType.LEAF

    """
    Return whether node is root or not
    """
    def is_root(self):
        return self.parent is None

    @property
    def level(self) -> int:
        i = 0
        node: Node = self
        while not node.is_root():
            node = node.parent.node
            i += 1
        return i

    def __str__(self):
        s: str = f'node_type={self.node_type.name}, level={self.level}'
        if self.is_leaf():
            index = []
            for entry in self.entries:
                index.append(str(entry.child))
            s += f', index=[{", ".join(index)}]'
            s += '\n'
        else:
            s += '\n'
            for entry in self.entries:
                s += f'{entry.child}'
        return s
