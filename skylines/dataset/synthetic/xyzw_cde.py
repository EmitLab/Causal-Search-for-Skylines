from .synthetic import SyntheticDataset, Dominance


class XYZW_CDE_1(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)
                         # constant_controls=[
                         #     frozenset({'C'}),
                         #     frozenset({'X', 'Y'}),
                         #     frozenset({'Z', 'Y'}),
                         #     frozenset({'W', 'Y'}),
                         #     frozenset({'C', 'X', 'Y'}),
                         #     frozenset({'C', 'Z', 'Y'}),
                         #     frozenset({'C', 'W', 'Y'}),
                         #     frozenset({'X', 'Z', 'Y'}),
                         #     frozenset({'W', 'X', 'Y'}),
                         #     frozenset({'W', 'Z', 'Y'}),
                         #     frozenset({'C', 'X', 'Z', 'Y'}),
                         #     frozenset({'C', 'W', 'X', 'Y'})
                         # ])

class XYZW_CDE_2(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_3_a(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_3_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_4(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_12(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)


class XYZW_CDE_10(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_11(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'C': {'E': 1},
                             'D': {'E': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)


class XYZW_CDE_5_a(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_5_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_6(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_7(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MAX
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_8_a(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_8_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_9_a(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MIN,
                             'Y': Dominance.MAX,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)

class XYZW_CDE_9_b(SyntheticDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(control=['C', 'D', 'E'],
                         preference=['X', 'Y', 'Z', 'W'],
                         effect={
                             'X': {'C': 1},
                             'Y': {'C': -1},
                             'Z': {'D': 1},
                             'W': {'D': 1},
                             'E': {'C': 1, 'D': 1}
                         },
                         noise=0.3,
                         dominance=dominance,
                         infer_controls={
                             'W': Dominance.MAX,
                             'X': Dominance.MAX,
                             'Y': Dominance.MIN,
                             'Z': Dominance.MIN
                         },
                         size=size,
                         seed=seed)
