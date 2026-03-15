from .real import RealDataset, Dominance

"""Not using"""
class WineQualityWhite1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='wine_quality_white',
                         control=['fixed acidity','residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol','quality'],
                         preference=['citric acid', 'volatile acidity'],
                         effect={'quality': {'chlorides': -1, 'total sulfur dioxide': 1, 'pH': -1, 'alcohol': 0},
                                 'total sulfur dioxide': {'free sulfur dioxide': 1, 'reacted sulfur dioxide': 1},
                                 'pH': {'volatile acidity': -1, 'fixed acidity': -1},
                                 'fixed acidity': {'citric acid': +1},
                                 'alcohol': {'initial sugar': +1},
                                 'residual sugar': {'initial sugar': +1}
                                 },
                         dominance={'citric acid': Dominance.MAX, 'volatile acidity': Dominance.MIN},
                         size=size,
                         seed=seed,
                         constant_controls=[frozenset({'pH'}),
                                            frozenset({'quality'}),
                                            frozenset({'chlorides', 'quality'}),
                                            frozenset({'chlorides', 'pH'})],
                         provided=False)



class WineQualityWhite2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='wine_quality_white',
                         control=['fixed acidity','volatile acidity','residual sugar','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol','quality'],
                         preference=['chlorides', 'citric acid'],
                         effect={'quality': {'chlorides': -1, 'total sulfur dioxide': 1, 'pH': -1, 'alcohol': 0},
                                 'total sulfur dioxide': {'free sulfur dioxide': 1, 'reacted sulfur dioxide': 1},
                                 'pH': {'volatile acidity': -1, 'fixed acidity': -1},
                                 'fixed acidity': {'citric acid': +1},
                                 'alcohol': {'initial sugar': +1},
                                 'residual sugar': {'initial sugar': +1}
                                 },
                         dominance={'chlorides': Dominance.MAX, 'citric acid': Dominance.MAX},
                         size=size,
                         seed=seed,
                         constant_controls=[frozenset({'quality'})],
                         provided=False)



class WineQualityWhite3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='wine_quality_white',
                         control=['fixed acidity','citric acid','residual sugar','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol','quality'],
                         preference=['chlorides', 'volatile acidity'],
                         effect={'quality': {'chlorides': -1, 'total sulfur dioxide': 1, 'pH': -1, 'alcohol': 0},
                                 'total sulfur dioxide': {'free sulfur dioxide': 1, 'reacted sulfur dioxide': 1},
                                 'pH': {'volatile acidity': -1, 'fixed acidity': -1},
                                 'fixed acidity': {'citric acid': +1},
                                 'alcohol': {'initial sugar': +1},
                                 'residual sugar': {'initial sugar': +1}
                                 },
                         dominance={'chlorides': Dominance.MAX, 'volatile acidity': Dominance.MAX},
                         size=size,
                         seed=seed,
                         constant_controls=[frozenset({'quality'})],
                         provided=False)



class WineQualityWhite4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='wine_quality_white',
                         control=['volatile acidity','citric acid','residual sugar','fixed acidity','total sulfur dioxide','density','pH','sulphates','alcohol','quality'],
                         preference=['chlorides', 'free sulfur dioxide'],
                         effect={'quality': {'chlorides': -1, 'total sulfur dioxide': 1, 'pH': -1, 'alcohol': 0},
                                 'total sulfur dioxide': {'free sulfur dioxide': 1, 'reacted sulfur dioxide': 1},
                                 'pH': {'volatile acidity': -1, 'fixed acidity': -1},
                                 'fixed acidity': {'citric acid': +1},
                                 'alcohol': {'initial sugar': +1},
                                 'residual sugar': {'initial sugar': +1}
                                 },
                         dominance={'chlorides': Dominance.MAX, 'free sulfur dioxide': Dominance.MAX},
                         size=size,
                         seed=seed,
                         constant_controls=[frozenset({'quality'})],
                         provided=False)



class WineQualityWhite5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='wine_quality_white',
                         control=['volatile acidity','residual sugar','fixed acidity','total sulfur dioxide','density','pH','sulphates','alcohol','quality'],
                         preference=['chlorides', 'free sulfur dioxide', 'citric acid'],
                         effect={'quality': {'chlorides': -1, 'total sulfur dioxide': 1, 'pH': -1, 'alcohol': 0},
                                 'total sulfur dioxide': {'free sulfur dioxide': 1, 'reacted sulfur dioxide': 1},
                                 'pH': {'volatile acidity': -1, 'fixed acidity': -1},
                                 'fixed acidity': {'citric acid': +1},
                                 'alcohol': {'initial sugar': +1},
                                 'residual sugar': {'initial sugar': +1}
                                 },
                         dominance=dominance,
                         infer_controls={
                             'chlorides': Dominance.MAX,
                             'citric acid': Dominance.MIN,
                             'free sulfur dioxide': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)
