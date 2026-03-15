from .synthetic import SyntheticDataset, Dominance


class XYZ_C_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'Z'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_c(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_d(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_e(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MIN,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_f(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'Z'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_g(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'X'],
                         preference=['Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_h(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'X'],
                         preference=['Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_i(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'Y'],
                         preference=['X', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZ_C_1_j(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'Y'],
                         preference=['X', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZ_C_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1, 'X': 1, 'Z': 1},
                                 'Z': {'C':  0.5}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class XYZ_C_3(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y', 'Z'],
                         effect={'X': {'C': 1},
                                 'Y': {'X': 1},
                                 'Z': {'C': 1, 'Y': -1}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         constant_controls=[
                             frozenset({'C'})
                         ])
