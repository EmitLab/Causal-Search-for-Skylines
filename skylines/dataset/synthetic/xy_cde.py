from skylines.dataset import SyntheticDataset, Dominance


class XY_CDE_1(SyntheticDataset):
    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'E': {'C': 1},
                                 'D': {'E': 1},
                                 'Y': {'D': -1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'D'}),
                             frozenset({'E'}),
                             frozenset({'D', 'E'})
                         ])

class XY_CDE_2(SyntheticDataset):
    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'E': {'C': 1},
                                 'D': {'E': 1},
                                 'Y': {'D': -1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
