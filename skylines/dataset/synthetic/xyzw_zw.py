from .synthetic import SyntheticDataset, Dominance


class XYZW_ZW(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['Z', 'W'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'Z': {'X': 0.9},
                                 'W': {'Z': -1},
                                 'Y': {'W': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
