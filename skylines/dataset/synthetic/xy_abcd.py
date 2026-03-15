from .synthetic import SyntheticDataset, Dominance


class XY_ABCD(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'B': {'A': -0.5},
                                 'C': {'A': 0.5},
                                 'D': {'A': 0.5},
                                 'X': {'B': 0.5, 'C': 0.5},
                                 'Y': {'C': 0.5, 'D': -0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'D'}),
                             frozenset({'B', 'D'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'C'})
                         ])

class XY_ABCD_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'B': {'A': -0.5},
                                 'C': {'A': 0.5},
                                 'D': {'A': 0.5},
                                 'X': {'B': 0.5, 'C': 0.5},
                                 'Y': {'C': 0.5, 'D': -0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[frozenset({'C'})],
                         masked_nodes=['C'])

class XY_ABCD_c(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'B': {'A': -0.5},
                                 'C': {'A': 0.5},
                                 'D': {'A': 0.5},
                                 'X': {'B': 0.5, 'C': 0.5},
                                 'Y': {'C': 0.5, 'D': -0.5}},
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
                         ],
                         masked_edges=[('A', 'B'), ('A', 'D')])

class XY_ABCD_1_LN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': -1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.1,
                         size=size,
                         seed=seed)

class XY_ABCD_1_HN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': -1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.3,
                         size=size,
                         seed=seed)


class XY_ABCD_2_LN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': -5},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.1,
                         size=size,
                         seed=seed)


class XY_ABCD_2_HN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': -5},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.3,
                         size=size,
                         seed=seed)

class XY_ABCD_3_LN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': -1},
                                 'C': {'B': 1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.1,
                         size=size,
                         seed=seed)

class XY_ABCD_3_HN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': -1},
                                 'C': {'B': 1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.3,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'B'}),
                             frozenset({'C'}),
                             frozenset({'D'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'C'}),
                             frozenset({'A', 'D'}),
                             frozenset({'B', 'C'}),
                             frozenset({'B', 'D'}),
                             frozenset({'C', 'D'}),
                             frozenset({'A', 'B', 'C'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'A', 'C', 'D'}),
                             frozenset({'B', 'C', 'D'}),
                             frozenset({'A', 'B', 'C', 'D'})
                         ])

class XY_ABCD_4_LN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': 1},
                                 'D': {'C': -1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.1,
                         size=size,
                         seed=seed)

class XY_ABCD_4_HN(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D'],
                         preference=['X', 'Y'],
                         effect={'A': {'X': 1},
                                 'B': {'A': 1},
                                 'C': {'B': 1},
                                 'D': {'C': -1},
                                 'Y': {'D': 1}},
                         dominance=dominance,
                         noise=0.3,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'B'}),
                             frozenset({'C'}),
                             frozenset({'D'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'C'}),
                             frozenset({'A', 'D'}),
                             frozenset({'B', 'C'}),
                             frozenset({'B', 'D'}),
                             frozenset({'C', 'D'}),
                             frozenset({'A', 'B', 'C'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'A', 'C', 'D'}),
                             frozenset({'B', 'C', 'D'}),
                             frozenset({'A', 'B', 'C', 'D'})
                         ])
