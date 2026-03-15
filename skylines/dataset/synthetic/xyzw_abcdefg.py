from .synthetic import SyntheticDataset, Dominance


class XYZW_ABCDEFG_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
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
                             frozenset({'A', 'G'}),
                             frozenset({'B', 'D'}),
                             frozenset({'B', 'G'}),
                             frozenset({'D', 'G'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'A', 'B', 'G'}),
                             frozenset({'A', 'D', 'G'}),
                             frozenset({'B', 'D', 'G'}),
                             frozenset({'A', 'B', 'D', 'G'})
                         ])


class XYZW_ABCDEFG_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
                                 'C': {'A':  1.0, 'G': 1.0},
                                 'D': {'B':  1.0},
                                 'E': {'C':  1.0},
                                 'F': {'C':  1.0},
                                 'X': {'D': -1.0},
                                 'Y': {'E':  1.0},
                                 'Z': {'C':  1.0},
                                 'W': {'F':  1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)

class XYZW_ABCDEFG_2_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Z', 'W'],
                         preference=['X', 'Y'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
                                 'C': {'A':  1.0, 'G': 1.0},
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
                             frozenset({'B'}),
                             frozenset({'C'}),
                             frozenset({'D'}),
                             frozenset({'E'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'C'}),
                             frozenset({'A', 'D'}),
                             frozenset({'A', 'E'}),
                             frozenset({'A', 'G'}),
                             frozenset({'B', 'C'}),
                             frozenset({'B', 'D'}),
                             frozenset({'B', 'E'}),
                             frozenset({'B', 'F'}),
                             frozenset({'B', 'G'}),
                             frozenset({'B', 'Z'}),
                             frozenset({'B', 'W'}),
                             frozenset({'C', 'D'}),
                             frozenset({'C', 'E'}),
                             frozenset({'C', 'F'}),
                             frozenset({'C', 'G'}),
                             frozenset({'C', 'Z'}),
                             frozenset({'C', 'W'}),
                             frozenset({'D', 'E'}),
                             frozenset({'D', 'F'}),
                             frozenset({'D', 'G'}),
                             frozenset({'D', 'Z'}),
                             frozenset({'D', 'W'}),
                             frozenset({'E', 'F'}),
                             frozenset({'E', 'G'}),
                             frozenset({'E', 'Z'}),
                             frozenset({'E', 'W'})
                         ])

class XYZW_ABCDEFG_2_c(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
                                 'C': {'A':  1.0, 'G': 1.0},
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
                         masked_nodes=['G'],
                         constant_controls=[
                             frozenset({'A'}),
                             frozenset({'B'}),
                             frozenset({'D'}),
                             frozenset({'A', 'B'}),
                             frozenset({'A', 'D'}),
                             frozenset({'A', 'G'}),
                             frozenset({'B', 'D'}),
                             frozenset({'B', 'G'}),
                             frozenset({'D', 'G'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'A', 'B', 'G'}),
                             frozenset({'A', 'D', 'G'}),
                             frozenset({'B', 'D', 'G'}),
                             frozenset({'A', 'B', 'D', 'G'})
                         ])

class XYZW_ABCDEFG_2_d(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
                                 'C': {'A':  1.0, 'G': 1.0},
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
                         masked_edges=[('A', 'B'), ('A', 'C')],
                         constant_controls=[
                                frozenset({'B'}),
                                frozenset({'D'}),
                                frozenset({'G'}),
                                frozenset({'A', 'B'}),
                                frozenset({'A', 'D'}),
                                frozenset({'A', 'G'}),
                                frozenset({'B', 'D'}),
                                frozenset({'B', 'G'}),
                                frozenset({'D', 'G'}),
                                frozenset({'A', 'B', 'D'}),
                                frozenset({'A', 'B', 'G'}),
                                frozenset({'A', 'D', 'G'}),
                                frozenset({'B', 'D', 'G'}),
                                frozenset({'A', 'B', 'D', 'G'})
                         ])


class XYZW_ABCDEFG_3(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0},
                                 'C': {'A':  1.0, 'G': 1.0},
                                 'D': {'B':  1.0},
                                 'E': {'C':  1.0},
                                 'F': {'C':  1.0},
                                 'X': {'D': -1.0},
                                 'Y': {'E':  1.0},
                                 'Z': {'C':  1.0},
                                 'W': {'F':  1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XYZW_ABCDEFG_4(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={'B': {'A':  1.0, 'G': 1.0},
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
                             frozenset({'A', 'G'}),
                             frozenset({'B', 'D'}),
                             frozenset({'B', 'G'}),
                             frozenset({'D', 'G'}),
                             frozenset({'A', 'B', 'D'}),
                             frozenset({'A', 'B', 'G'}),
                             frozenset({'A', 'D', 'G'}),
                             frozenset({'B', 'D', 'G'}),
                             frozenset({'A', 'B', 'D', 'G'})
                         ])
