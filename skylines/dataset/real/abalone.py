from sympy.printing.numpy import const

from .real import RealDataset, Dominance


class Abalone1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex','Length','Diameter','Height','Shucked Weight','Viscera Weight','Shell Weight'],
                         preference=['Rings', 'Whole Weight'],
                         effect={'Rings': {'Age': 1},
                                 'Size/Volume': {'Age': 1, 'Sex': 0},
                                 'Length': {'Size/Volume': 1},
                                 'Diameter': {'Size/Volume': 1},
                                 'Height': {'Size/Volume': 1},
                                 'Shucked Weight': {'Size/Volume': 1},
                                 'Viscera Weight': {'Size/Volume': 1},
                                 'Shell Weight': {'Size/Volume': 1},
                                 'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1},
                                 },
                         dominance={'Rings': Dominance.MIN, 'Whole Weight': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'Shell Weight', 'Shucked Weight', 'Viscera Weight}'})])



class Abalone2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex','Length','Diameter','Height','Whole Weight','Viscera Weight','Shell Weight'],
                         preference=['Rings', 'Shucked Weight'],
                         effect={'Rings': {'Age': 1},
                                 'Size/Volume': {'Age': 1, 'Sex': 0},
                                 'Length': {'Size/Volume': 1},
                                 'Diameter': {'Size/Volume': 1},
                                 'Height': {'Size/Volume': 1},
                                 'Shucked Weight': {'Size/Volume': 1},
                                 'Viscera Weight': {'Size/Volume': 1},
                                 'Shell Weight': {'Size/Volume': 1},
                                 'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1},
                                 },
                         dominance={'Rings': Dominance.MIN, 'Shucked Weight': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'Whole Weight'})])



class Abalone3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex','Rings','Diameter','Height','Shucked Weight','Viscera Weight','Shell Weight'],
                         preference=['Length', 'Whole Weight'],
                         effect={'Rings': {'Age': 1},
                                 'Size/Volume': {'Age': 1, 'Sex': 0},
                                 'Length': {'Size/Volume': 1},
                                 'Diameter': {'Size/Volume': 1},
                                 'Height': {'Size/Volume': 1},
                                 'Shucked Weight': {'Size/Volume': 1},
                                 'Viscera Weight': {'Size/Volume': 1},
                                 'Shell Weight': {'Size/Volume': 1},
                                 'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1},
                                 },
                         dominance={'Length': Dominance.MIN, 'Whole Weight': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'Shucked Weight', 'Viscera Weight', 'Shell Weight'})])



class Abalone4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex', 'Rings', 'Height', 'Shucked Weight', 'Viscera Weight', 'Shell Weight'],
                         preference=['Length', 'Whole Weight', 'Diameter'],
                         effect={
                             'Rings': {'Age': 1},
                             'Size/Volume': {'Age': 1, 'Sex': 0},
                             'Length': {'Size/Volume': 1},
                             'Diameter': {'Size/Volume': 1},
                             'Height': {'Size/Volume': 1},
                             'Shucked Weight': {'Size/Volume': 1},
                             'Viscera Weight': {'Size/Volume': 1},
                             'Shell Weight': {'Size/Volume': 1},
                             'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Diameter': Dominance.MIN,
                             'Length': Dominance.MIN,
                             'Whole Weight': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)



class Abalone5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex', 'Rings', 'Diameter', 'Shucked Weight', 'Viscera Weight', 'Shell Weight'],
                         preference=['Length', 'Whole Weight', 'Height'],
                         effect={
                             'Rings': {'Age': 1},
                             'Size/Volume': {'Age': 1, 'Sex': 0},
                             'Length': {'Size/Volume': 1},
                             'Diameter': {'Size/Volume': 1},
                             'Height': {'Size/Volume': 1},
                             'Shucked Weight': {'Size/Volume': 1},
                             'Viscera Weight': {'Size/Volume': 1},
                             'Shell Weight': {'Size/Volume': 1},
                             'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Height': Dominance.MIN,
                             'Length': Dominance.MIN,
                             'Whole Weight': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)



class Abalone6(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='abalone',
                         control=['Sex','Length','Height','Whole Weight','Viscera Weight','Shell Weight'],
                         preference=['Rings', 'Shucked Weight', 'Diameter'],
                         effect={
                             'Rings': {'Age': 1},
                             'Size/Volume': {'Age': 1, 'Sex': 0},
                             'Length': {'Size/Volume': 1},
                             'Diameter': {'Size/Volume': 1},
                             'Height': {'Size/Volume': 1},
                             'Shucked Weight': {'Size/Volume': 1},
                             'Viscera Weight': {'Size/Volume': 1},
                             'Shell Weight': {'Size/Volume': 1},
                             'Whole Weight': {'Viscera Weight': 1, 'Shell Weight': 1, 'Shucked Weight': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Diameter': Dominance.MIN,
                             'Rings': Dominance.MIN,
                             'Shucked Weight': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)
