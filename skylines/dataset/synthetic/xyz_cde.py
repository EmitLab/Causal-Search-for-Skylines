from .synthetic import SyntheticDataset, Dominance


class XYZ_CDE(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z'],
                         effect={'D': {'C': 0.6},
                                 'E': {'C': 0.7},
                                 'X': {'D': 0.6},
                                 'Y': {'E': 0.9},
                                 'Z': {'C': -0.8}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
