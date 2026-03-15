from .synthetic import SyntheticDataset, Dominance


class Collider_XYZW_ABCD_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  0.2, 'C': 0.8},
                                 'C': {'A':  1.0},
                                 'D': {'B':  0.6, 'C': 0.4},
                                 'X': {'D': 1.0, 'B': 0.2, 'C': 0.4},
                                 'Y': {'C':  0.2, 'W': 0.8},
                                 'Z': {'B':  0.1, 'C': 0.4, 'X': 0.5},
                                 'W': {'D':  0.5, 'A': 0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class Collider_XYZW_ABCD_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A': 0.2, 'C': -0.8},
                                 'C': {'A': -1.0},
                                 'D': {'B': -0.6, 'C': 0.4},
                                 'X': {'D': -1.0, 'B': 0.2, 'C': -0.4},
                                 'Y': {'C': 0.2, 'W': -0.8},
                                 'Z': {'B': -0.1, 'C': -0.4, 'X': 0.5},
                                 'W': {'D': -0.5, 'A': 0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
