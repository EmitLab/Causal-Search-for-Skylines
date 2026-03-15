from .synthetic import SyntheticDataset, Dominance


class XY_ABC_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C'],
                         preference=['X', 'Y'],
                         effect={'X': {'A':  0.5, 'B': -0.5},
                                 'Y': {'B': -0.5, 'C': -0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'C'}),
                             frozenset({'A', 'C'})
                         ])
