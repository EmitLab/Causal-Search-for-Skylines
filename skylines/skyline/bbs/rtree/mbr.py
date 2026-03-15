import math


class MBR:

    def __init__(self, min_dim: list, max_dim: list):
        self.min_dim = min_dim if min_dim is not None else []
        self.max_dim = max_dim if max_dim is not None else []

        if len(self.min_dim) != len(self.max_dim):
            raise ValueError('min_dim and max_dim must have the same length')
    
    @property
    def area(self):
        return math.prod([a - b for a, b in zip(self.max_dim, self.min_dim)])

    @property
    def priority(self):
        return sum(self.max_dim)
    
    def combine(self, other):
        min_dim = [min(a, b) for a, b in zip(self.min_dim, other.min_dim)]
        max_dim = [max(a, b) for a, b in zip(self.max_dim, other.max_dim)]
        return MBR(min_dim, max_dim)

    def overlaps(self, other):
        for dim in range(len(self.max_dim)):
            if (self.min_dim[dim] <= other.min_dim[dim] <= self.max_dim[dim] or
                    other.min_dim[dim] <= self.min_dim[dim] <= other.max_dim[dim]):
                return True
        return False

    def contains(self, other):
        for dim in range(len(self.max_dim)):
            if not (self.min_dim[dim] <= other.min_dim[dim] <= self.max_dim[dim] and
                    self.min_dim[dim] <= other.max_dim[dim] <= self.max_dim[dim]):
                return False
        return True

    def __eq__(self, other):
        for dim in range(len(self.max_dim)):
            if not (self.min_dim[dim] == other.min_dim[dim] and other.max_dim[dim] == self.max_dim[dim]):
                return False
        return True

    def __str__(self):
        return f'min_dim={self.min_dim}, max_dim={self.max_dim}'
