from .synthetic import SyntheticDataset, Dominance


class XYZWPQRSTU_ABCDEF(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F'],
                         preference=['X', 'Y', 'Z', 'W', 'P', 'Q', 'R', 'S', 'T', 'U'],
                         effect={'P': {'Q':  -1.0, 'Y': -0.5, 'Z': 1.0},
                                 'Q': {'A':  -0.5},
                                 'R': {'C':  0.5},
                                 'T': {'W':  1.0},
                                 'U': {'W':  -0.5},
                                 'X': {'W': 1.0},
                                 'Y': {'F':  1.0, 'X': 1.0},
                                 'Z': {'D':  -1.0},
                                 'A': {'F':  1.0},
                                 'F': {'U': -0.5, 'W': -0.5, 'X': -1.0},
                                 'B': {'S': -0.5},
                                 'C': {'S': 0.5, 'T': -1.0},
                                 'D': {'F': 0.5},
                                 'E': {'R': -1.0, 'C': 1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A', 'C'}),
                             frozenset({'A', 'B', 'C'}),
                             frozenset({'A', 'C', 'E'}),
                             frozenset({'A', 'B', 'C', 'E'})
                         ])
