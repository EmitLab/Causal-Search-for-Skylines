from .entry import *
from .node import *


class RTree:

    def __init__(self, M, m):
        self.M = M
        self.m = m
        self.root = Node()

    '''
    K = Key()
    Insert new tuple Key in tree
    '''
    def insert(self, entry: Entry):
        # Find position for new record
        leaf_node = self.choose_leaf(self.root, entry)
        entry.node = leaf_node

        # add record to leaf if it has space
        if not leaf_node.is_full(self.M):
            leaf_node.entries.append(entry)
            node_1, node_2 = leaf_node, None

        # else make a split after adding node to leaf
        else:
            leaf_node.entries.append(entry)
            node_1, node_2 = leaf_node.split(self.m)

        # now adjust the tree
        self.adjust_tree(node_1, node_2)

    '''
    K = Key()
    Find leaf node for new Key in tree
    '''
    def choose_leaf(self, node: Node, entry: Entry):
        if node.is_leaf():
            return node

        # initialization
        min_expandable_area = float("inf")
        new_node: Node = Node()

        for entry in node.entries:
            combined_area = entry.mbr.combine(entry.mbr)
            expandable_area = combined_area.area - entry.mbr.area

            if min_expandable_area is None or min_expandable_area > expandable_area:
                min_expandable_area = expandable_area
                new_node = entry.child

            elif min_expandable_area == expandable_area:
                if new_node.MBR().area > entry.mbr.area:
                    new_node = entry.child

        return self.choose_leaf(new_node, entry)

    '''
    N = leafNode
    NN = if N was previously splitted
    Ascend from a leaf node L to the root, adjusting covering rectangles,
    and propagating node splits if necessary
    '''
    def adjust_tree(self, node_1: Node, node_2: Node = None):
        # check if done
        if node_1.is_root():
            # reached at root
            if node_2 is not None:
                # root was split
                self.make_root(node_1, node_2)
            return

        # update the parents mbr for N1
        node_1.parent.mbr = node_1.MBR()

        # get the parent node
        parent_node = node_1.parent.node

        # if previously node was split, make a new parent node and
        # then do some adjustment
        if node_2 is not None:
            # make a new entry which is parent of split node
            new_key = Entry(mbr=node_2.MBR(), node=parent_node)
            node_2.parent = new_key
            new_key.child = node_2

            # add this new entry to parent of N1 if it is not full
            if not parent_node.is_full(self.M):
                parent_node.entries.append(new_key)
                return self.adjust_tree(parent_node, None)

            # else add and split parent
            else:
                parent_node.entries.append(new_key)
                node_a, node_b = parent_node.split(self.m)
                return self.adjust_tree(node_a, node_b)

        # else adjust the parent node
        else:
            return self.adjust_tree(parent_node, None)

    '''
    Make a root with given two nodes which are result of a split
    '''
    def make_root(self, node_1: Node, node_2: Node):
        if not node_1.is_leaf():
            node_1.node_type = NodeType.INTERMEDIATE
        if not node_2.is_leaf():
            node_2.node_type = NodeType.INTERMEDIATE

        # create a new node
        self.root = Node(node_type=NodeType.ROOT)

        # create entry for node_1
        new_key = Entry(mbr=node_1.MBR(), node=self.root)
        node_1.parent = new_key
        new_key.child = node_1
        self.root.entries.append(new_key)

        # create entry for node_2
        new_key = Entry(mbr=node_2.MBR(), node=self.root)
        node_2.parent = new_key
        new_key.child = node_2
        self.root.entries.append(new_key)

    '''
    Delete an entry K
    '''
    def delete(self, entry: Entry):
        if self.is_empty():
            print("Tree is empty")
            return

        # find leaf node that contains this entry
        leaf_node = self.find_leaf(self.root, entry)
        if not leaf_node:
            print("Entry not present in Tree")
            return

        # remove entry from leaf node
        num_keys = len(leaf_node.entries)
        entry_found = False

        for i in range(num_keys):
            # if id is provided, delete using this
            if entry.child:
                if leaf_node.entries[i].child == entry.child:
                    entry_found = True
                    leaf_node.entries.pop(i)
                    break

            # else delete using mbr.Equals by comparing MBRs
            else:
                if leaf_node.entries[i].mbr == entry.mbr:
                    entry_found = True
                    leaf_node.entries.pop(i)
                    break

        if not entry_found:
            print("Entry not present")
            return

        # propagate MBR changes upwards
        self.condense_tree(leaf_node, [])

        # update root if it is not leaf and don't have entries >= 2
        if not self.root.is_leaf() and len(self.root.entries) == 1:
            child = self.root.entries[0].child
            self.root = child
            self.root.parent = None

            # update node attribute for entries
            for entry in self.root.entries:
                entry.node = self.root

            # update new root node type if it's not leaf
            if not self.root.is_leaf():
                self.root.node_type = NodeType.ROOT

    """
    Find leafnode that contains K in subtree rooted at N
    """
    def find_leaf(self, node: Node, entry: Entry):
        # return for recursive calls if we are at leaf
        if node.is_leaf():
            if node.MBR().contains(entry.mbr):
                # resolve equal mbr dimensions
                if entry.child:
                    for entry in node.entries:
                        if entry.child == entry.child:
                            # this node contains entry
                            return node

                    # this node doesn't contain this entry
                    return None
                else:
                    return node
            else:
                return None

        # else iterate through all the entries in N find K if it is there
        entries = node.entries
        for entry in entries:
            if entry.mbr.overlaps(entry.mbr):
                leaf = self.find_leaf(entry.child, entry)
                if leaf:
                    return leaf

        # entry not found in N, return None
        return None

    """
    Adjust Tree by condensing it's height after any deletion operation
    @params: N: node where entries have been modified
    @params: EN: list of eliminated nodes during adjustment (if it's size goes below m)
    """
    def condense_tree(self, node: Node, eliminated: list[Node]):
        # until we are at root
        if not node.is_root():
            # get the parent of node
            parent_entry = node.parent
            parent_node = parent_entry.node

            # check if node underflows or not
            if node.underflows(self.m):
                parent_node.entries.remove(parent_entry)
                eliminated.append(node)
            else:
                parent_entry.mbr = node.MBR()

            # condense upwards
            self.condense_tree(parent_node, eliminated)

        # we are at root node
        elif len(eliminated) != 0:
            # eliminated is not empty
            while len(eliminated) != 0:
                # we are looping in reverse direction because items are inserted in
                # order of increasing height, and we want none leaf node to place at the height
                # where they were previously
                node = eliminated.pop()

                # if node N was from a leaf, then insert at leaf
                if node.is_leaf():
                    for entry in node.entries:
                        self.insert(entry)

                else:
                    # insert at the same height as it was removed to maintain its leaves at the same height as main tree
                    # the parent entry of the node was removed because of underflow, so search in its siblings where we can add it
                    # so the area expansion is minimum
                    parent_node = node.parent.node
                    min_expandable_area = float("inf")
                    friend_node = None

                    for entry in parent_node.entries:
                        node_mbr = node.MBR()
                        entry_mbr = entry.mbr
                        combined_area = entry_mbr.Combine(node_mbr).area
                        expandable_area = combined_area - entry_mbr.area - node_mbr.area
                        if min_expandable_area > expandable_area:
                            min_expandable_area = expandable_area
                            friend_node = entry.child

                    if friend_node:
                        # add node to friend node (add entries of node into friend node)
                        # check the node attribute of entry from node to friend_node
                        for entry in node.entries:
                            entry.node = friend_node

                        friend_node.entries = friend_node.entries + node.entries
                        if friend_node.Overflows(self.M):
                            print("Node goes overflow after adding deleted, so doing adjustment")
                            node_a, node_b = friend_node.split(self.m)
                            self.adjust_tree(node_a, node_b)

                    else:
                        # there is no entries left in parent node
                        # this case won't arise, just to see if it does
                        print("Unable to get friend node for removed node")

    def is_empty(self):
        return len(self.root.entries) == 0

    def __str__(self):
        return f'{self.root}'
