from .mbr import MBR
from .node import Node


class Entry:

    def __init__(self, mbr: MBR = None, child: Node | int = None, node: Node = None):
        self.mbr = mbr
        self.child = child
        self.node = node

    def __lt__(self, other):
        return self.mbr.priority > other.mbr.priority

    def __gt__(self, other):
        return self.mbr.priority < other.mbr.priority
