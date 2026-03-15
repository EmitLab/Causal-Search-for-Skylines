from .synthetic import SyntheticDataset, Dominance


class XYZ_CD_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  0.5, 'D':  0.5},
                                 'Y': {'C': -0.2, 'D':  0.5},
                                 'Z': {'C':  0.7, 'D': -0.3}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XYZ_CD_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  0.1, 'D': -0.9},
                                 'Y': {'C': -0.2, 'D':  0.5},
                                 'Z': {'C':  0.7, 'D': -0.3}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[frozenset({'C', 'D'})])

class XYZ_CD_3(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XXX, NNN
                         #     frozenset({'C'})
                         # ])

class XYZ_CD_4(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XNX, NXN
                         #     frozenset({'D'})
                         # ])

class XYZ_CD_5(SyntheticDataset): # XNX

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XXN, NXX, NNX, XNN
                         #     frozenset({'C', 'D'})
                         # ])

class XYZ_CD_6(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'Z'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XX, NN
                         #     frozenset({'C'}),
                         #     frozenset({'C', 'Z'})
                         # ])

class XYZ_CD_7(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'Z'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XN, NX
                         #     frozenset({'D'}),
                         #     frozenset({'D', 'Z'})
                         # ])

class XYZ_CD_8(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'Y'],
                         preference=['X', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XX, NN
                         #     frozenset({'Y'})
                         # ])

class XYZ_CD_9(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'Y'],
                         preference=['X', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XN, NX
                         #     frozenset({'C', 'D'}),
                         #     frozenset({'C', 'D', 'Y'})
                         # ])

class XYZ_CD_10(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'X'],
                         preference=['Y', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XX, NN
                         #     frozenset({'C'}),
                         #     frozenset({'C', 'X'})
                         # ])

class XYZ_CD_11(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'X'],
                         preference=['Y', 'Z'],
                         effect={'X': {'C':  1, 'D':  1},
                                 'Y': {'C': -1, 'D':  1},
                                 'Z': {'C':  1, 'D':  1}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
                         # constant_controls=[ # XN, NX
                         #     frozenset({'D'}),
                         #     frozenset({'D', 'X'})
                         # ])

class XYZ_CD_12_a(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'D': {'C': 1, 'Z': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_CD_12_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'D': {'C': 1, 'Z': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_CD_13(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'D': {'C': 1, 'Z': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_CD_14(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D'],
                         preference=['X', 'Y', 'Z'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'D': {'C': 1, 'Z': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)
