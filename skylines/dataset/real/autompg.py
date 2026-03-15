from .real import RealDataset, Dominance

# mpg,cylinders,displacement,horsepower,weight,acceleration

"""Not using"""
class AutoMPG1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['cylinders','displacement','horsepower','weight'],
                         preference=['mpg', 'acceleration'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance={'mpg': Dominance.MAX, 'acceleration': Dominance.MIN},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=None)

"""Not using"""
class AutoMPG2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','displacement','horsepower'],
                         preference=['weight', 'acceleration'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance={'weight': Dominance.MAX, 'acceleration': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=None)

class AutoMPG3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower','acceleration'],
                         preference=['weight', 'displacement'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance={'weight': Dominance.MAX, 'displacement': Dominance.MIN},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'mpg', 'cylinders'})])


class AutoMPG3_AUG(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower','acceleration'],
                         preference=['weight', 'displacement'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance={'weight': Dominance.MAX, 'displacement': Dominance.MIN},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'mpg', 'cylinders'})])

class AutoMPG4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','displacement','acceleration'],
                         preference=['weight', 'horsepower'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance={'weight': Dominance.MIN, 'horsepower': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'mpg', 'cylinders', 'displacement'})])

class AutoMPG5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower'],
                         preference=['weight', 'displacement', 'acceleration'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance=dominance,
                         infer_controls={
                             'acceleration': Dominance.MIN,
                             'displacement': Dominance.MIN,
                             'weight': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)

class AutoMPG6(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower'],
                         preference=['weight', 'displacement', 'acceleration'],
                         effect={'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                                 'horsepower': {'displacement': 1},
                                 'acceleration': {'horsepower': -1},
                                 'displacement': {'cylinders': 1},
                                 'weight': {'cylinders': 1}
                                 },
                         dominance=dominance,
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'cylinders', 'mpg'})])

class AutoMPG7(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower'],
                         preference=['weight', 'displacement', 'acceleration'],
                         effect={
                             'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                             'horsepower': {'displacement': 1},
                             'acceleration': {'horsepower': -1, 'weight': 1},
                             'displacement': {'cylinders': 1},
                             'weight': {'cylinders': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'acceleration': Dominance.MAX,
                             'displacement': Dominance.MAX,
                             'weight': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)

class AutoMPG8(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='autompg',
                         control=['mpg','cylinders','horsepower'],
                         preference=['weight', 'displacement', 'acceleration'],
                         effect={
                             'mpg': {'weight': -1, 'displacement': -1, 'horsepower': -1},
                             'horsepower': {'displacement': 1},
                             'acceleration': {'horsepower': -1, 'weight': 1},
                             'displacement': {'cylinders': 1},
                             'weight': {'cylinders': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'acceleration': Dominance.MIN,
                             'displacement': Dominance.MAX,
                             'weight': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)
