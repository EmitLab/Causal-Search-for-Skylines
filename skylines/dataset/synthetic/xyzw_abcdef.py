from .synthetic import SyntheticDataset, Dominance


class XYZW_ABCDEF_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0},
                                 'C': {'A':  1.0},
                                 'D': {'B':  1.0},
                                 'E': {'C':  1.0},
                                 'F': {'C':  1.0},
                                 'X': {'D': -1.0},
                                 'Y': {'E':  1.0},
                                 'Z': {'C':  1.0},
                                 'W': {'F': -1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A', 'F'}),
                             frozenset({'B', 'F'}),
                             frozenset({'D', 'F'}),
                             frozenset({'A', 'B', 'F'}),
                             frozenset({'A', 'D', 'F'}),
                             frozenset({'B', 'D', 'F'}),
                             frozenset({'A', 'B', 'D', 'F'})
                         ])


class XYZW_ABCDEF_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0},
                                 'C': {'A':  1.0},
                                 'D': {'B':  1.0},
                                 'E': {'C':  1.0},
                                 'F': {'C':  1.0},
                                 'X': {'D': -1.0},
                                 'Y': {'E':  1.0},
                                 'Z': {'C':  1.0},
                                 'W': {'F':  1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'B'}),
                             frozenset({'D'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'D'}),
                             frozenset({'B', 'D'}),
                             frozenset({'A', 'B', 'D'})
                         ])
