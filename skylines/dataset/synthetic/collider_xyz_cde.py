from .synthetic import SyntheticDataset, Dominance


class Collider_XYZ_CDE_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z'],
                         effect={'D': {'C': 0.6, 'Y': -0.7},
                                 'E': {'C': 0.7},
                                 'X': {'D': 0.6},
                                 'Y': {'E': 0.9},
                                 'Z': {'C': -0.8, 'E': 0.9}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class Collider_XYZ_CDE_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z'],
                         effect={'D': {'C': 0.6, 'Y': -0.7},
                                 'E': {'C': -1},
                                 'X': {'D': 0.6},
                                 'Y': {'E': -0.9},
                                 'Z': {'C': -0.8, 'E': 0.9}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[
                         #     frozenset({'C', 'D', 'E'})
                         # ])

class Collider_XYZ_CDE_2_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E', 'Z'],
                         preference=['X', 'Y'],
                         effect={'D': {'C': 0.6, 'Y': -0.7},
                                 'E': {'C': -1},
                                 'X': {'D': 0.6},
                                 'Y': {'E': -0.9},
                                 'Z': {'C': -0.8, 'E': 0.9}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[frozenset({'C', 'D', 'E', 'Z'}),
                         #                    frozenset({'C', 'D', 'E'}),
                         #                    frozenset({'D', 'E', 'Z'}),
                         #                    frozenset({'C', 'D', 'Z'}),
                         #                    frozenset({'D', 'Z'}),
                         #                    frozenset({'D', 'E'}),
                         #                    frozenset({'C', 'D'}),
                         #                    frozenset({'D'})])

class Collider_XYZ_CDE_2_c(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z'],
                         effect={'D': {'C': 0.6, 'Y': -0.7},
                                 'E': {'C': -1},
                                 'X': {'D': 0.6},
                                 'Y': {'E': -0.9},
                                 'Z': {'C': -0.8, 'E': 0.9}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         masked_nodes=['D'])
                         # constant_controls=[frozenset({'C', 'D', 'E'}),
                         #                    frozenset({'C', 'E'}),
                         #                    frozenset({'D', 'E'}),
                         #                    frozenset({'E'}),])

class Collider_XYZ_CDE_2_d(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z'],
                         effect={'D': {'C': 0.6, 'Y': -0.7},
                                 'E': {'C': -1},
                                 'X': {'D': 0.6},
                                 'Y': {'E': -0.9},
                                 'Z': {'C': -0.8, 'E': 0.9}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         masked_edges=[('C', 'Z'), ('E', 'Y')])
                         # constant_controls=[frozenset({'C', 'D', 'E'}),
                         #                    frozenset({'C', 'D'}),
                         #                    frozenset({'D', 'E'})])
