from .real import RealDataset, Dominance


class DryBean_1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='drybean',
                         control=['MajorAxisLength', 'MinorAxisLength', 'Area', 'Perimeter', 'AspectRatio', 'EquivDiameter', 'Roundness'],
                         preference=['Compactness', 'Eccentricity'],
                         effect={
                             'Area': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'Perimeter': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'AspectRatio': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Eccentricity': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Roundness': {'Area': 1, 'Perimeter': -1},
                             'Compactness': {'Perimeter': -1, 'EquivDiameter': 1},
                             'EquivDiameter': {'AspectRatio': -1},
                         },
                         dominance=dominance,
                         infer_controls={
                             'Compactness': Dominance.MAX,
                             'Eccentricity': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)



class DryBean_2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='drybean',
                         control=['MajorAxisLength', 'MinorAxisLength', 'Perimeter', 'AspectRatio', 'EquivDiameter', 'Roundness'],
                         preference=['Compactness', 'Eccentricity', 'Area'],
                         effect={
                             'Area': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'Perimeter': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'AspectRatio': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Eccentricity': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Roundness': {'Area': 1, 'Perimeter': -1},
                             'Compactness': {'Perimeter': -1, 'EquivDiameter': 1},
                             'EquivDiameter': {'AspectRatio': -1},
                         },
                         dominance=dominance,
                         infer_controls={
                             'Area': Dominance.MIN,
                             'Compactness': Dominance.MAX,
                             'Eccentricity': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)



class DryBean_3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='drybean',
                         control=['MajorAxisLength', 'MinorAxisLength', 'Area', 'Eccentricity', 'EquivDiameter', 'Compactness'],
                         preference=['Perimeter', 'AspectRatio', 'Roundness'],
                         effect={
                             'Area': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'Perimeter': {'MajorAxisLength': 1, 'MinorAxisLength': 1},
                             'AspectRatio': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Eccentricity': {'MajorAxisLength': 1, 'MinorAxisLength': -1},
                             'Roundness': {'Area': 1, 'Perimeter': -1},
                             'Compactness': {'Perimeter': -1, 'EquivDiameter': 1},
                             'EquivDiameter': {'AspectRatio': -1},
                         },
                         dominance=dominance,
                         infer_controls={
                             'AspectRatio': Dominance.MAX,
                             'Perimeter': Dominance.MAX,
                             'Roundness': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)
