from .synthetic import SyntheticDataset, Dominance


class XY_CD_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D': -0.5},
                                 'Y': {'C': -1, 'D':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XY_CD_1_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D': -0.5},
                                 'Y': {'C': -1, 'D':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN
                         },
                         size=size,
                         seed=seed)


class XY_CD_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'C': {'X':  1, 'Y': -0.5},
                                 'D': {'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)

class XY_CD_3(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'D': {'C': 1},
                                 'Y': {'D': -1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)

class XY_CD_4(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'D': {'C': -1},
                                 'Y': {'D': 1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)

class XY_CD_5(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': -1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XY_CD_6(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'D': {'C': 1},
                                 'Y': {'D': -1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'D'})
                         ])


class XY_CD_7(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'D': {'C': -1},
                                 'Y': {'D': 1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XY_CD_8(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': -1},
                                 'D': {'C': 1},
                                 'Y': {'D': 1, 'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XY_CD_9(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D': 1},
                                 'Y': {'C': -1, 'D': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XX, NN
                         #     frozenset({'C'})
                         # ])

class XY_CD_10(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D': 1},
                                 'Y': {'C': -1, 'D': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XN, NX
                         #     frozenset({'D'})
                         # ])
