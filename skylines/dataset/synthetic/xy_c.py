from .synthetic import SyntheticDataset, Dominance


class XY_C_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XY_C_1_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN
                         },
                         size=size,
                         seed=seed)


class XY_C_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'C': {'X': -1.0, 'Y': 1.0}},
                         dominance=dominance,
                         infer_controls={
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XY_C_3(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'C': {'X': 2.0},
                                 'Y': {'C': 1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)

class XY_C_4(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'X': {'C': 1},
                                 'Y': {'C': 1}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         noise=0)

class XY_C_5(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C'],
                         preference=['X', 'Y'],
                         effect={'X': {'C':  1},
                                 'Y': {'C': -1}},
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         noise=0)
