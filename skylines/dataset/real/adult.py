from sympy.printing.numpy import const

from .real import RealDataset, Dominance


class Adult1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num', 'race', 'sex', 'cap-gain', 'hrs-wk'],
                         preference=['Income', 'educ-num'],
                         effect={'hrs-wk': {'age': 0.5, 'sex': 1},
                                 'educ-num': {'race': 1, 'sex': 1},
                                 'Income': {'age': 1, 'educ-num': 1, 'hrs-wk': 1},
                                 'cap-gain': {'Income': 1}},
                         dominance=dominance,
                         size=30_162,
                         seed=seed,
                         provided=False)

class Adult2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num', 'race', 'sex', 'cap-gain', 'hrs-wk'],
                         preference=['Income', 'age'],
                         effect={'hrs-wk': {'age': 0.5, 'sex': 1},
                                 'educ-num': {'race': 1, 'sex': 1},
                                 'Income': {'age': 1, 'educ-num': 1, 'hrs-wk': 1},
                                 'cap-gain': {'Income': 1}},
                         dominance=dominance,
                         size=30_162,
                         seed=seed,
                         provided=False)

class Adult3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num', 'race', 'sex', 'age', 'hrs-wk'],
                         preference=['Income', 'cap-gain'],
                         effect={'hrs-wk': {'age': 0.5, 'sex': 1},
                                 'educ-num': {'race': 1, 'sex': 1},
                                 'Income': {'age': 1, 'educ-num': 1, 'hrs-wk': 1},
                                 'cap-gain': {'Income': 1}},
                         dominance=dominance,
                         size=30_162,
                         seed=seed,
                         provided=False)

class Adult4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num', 'race', 'sex', 'age', 'cap-gain'],
                         preference=['Income', 'hrs-wk'],
                         effect={'hrs-wk': {'age': 0.5, 'sex': 1},
                                 'educ-num': {'race': 1, 'sex': 1},
                                 'Income': {'age': 1, 'educ-num': 1, 'hrs-wk': 1},
                                 'cap-gain': {'Income': 1}},
                         dominance=dominance,
                         size=30_162,
                         seed=seed,
                         provided=False)

class Adult5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num','sex','cap-loss','hrs-wk','cap-gain'],
                         preference=['age', 'Income'],
                         effect={'educ-num': {'age': 1, 'sex': 1},
                                 'hrs-wk': {'age': 1, 'educ-num': 1},
                                 'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                                 'captial-investments': {'family-inheritence': 0, 'age': 0},
                                 'cap-gain': {'captial-investments': 0},
                                 'cap-loss': {'captial-investments': 0},
                                 'family-inheritence': {'age': 0, 'sex': 0},
                                 },
                         dominance={'age': Dominance.MIN, 'Income': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[
                             frozenset({'educ-num', 'hrs-wk'})
                         ])

class Adult6(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['age','sex','cap-loss','cap-gain','hrs-wk'],
                         preference=['educ-num', 'Income'],
                         effect={'educ-num': {'age': 1, 'sex': 1},
                                 'hrs-wk': {'age': 1, 'educ-num': 1},
                                 'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                                 'captial-investments': {'family-inheritence': 0, 'age': 0},
                                 'cap-gain': {'captial-investments': 0},
                                 'cap-loss': {'captial-investments': 0},
                                 'family-inheritence': {'age': 0, 'sex': 0},
                                 },
                         dominance={'educ-num': Dominance.MIN, 'Income': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'age', 'hrs-wk', 'sex'})])

class Adult7(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['age','sex','cap-loss','Income','cap-gain'],
                         preference=['educ-num', 'hrs-wk'],
                         effect={'educ-num': {'age': 1, 'sex': 1},
                                 'hrs-wk': {'age': 1, 'educ-num': 1},
                                 'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                                 'captial-investments': {'family-inheritence': 0, 'age': 0},
                                 'cap-gain': {'captial-investments': 0},
                                 'cap-loss': {'captial-investments': 0},
                                 'family-inheritence': {'age': 0, 'sex': 0},
                                 },
                         dominance={'educ-num': Dominance.MIN, 'hrs-wk': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'Income', 'age', 'sex'})])

"""Not using this one"""
class Adult8(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['age','sex','cap-loss','educ-num','hrs-wk'],
                         preference=['cap-gain', 'Income'],
                         effect={'educ-num': {'age': 1, 'sex': 1},
                                 'hrs-wk': {'age': 1, 'educ-num': 1},
                                 'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                                 'captial-investments': {'family-inheritence': 0, 'age': 0},
                                 'cap-gain': {'captial-investments': 0},
                                 'cap-loss': {'captial-investments': 0},
                                 'family-inheritence': {'age': 0, 'sex': 0},
                                 },
                         dominance={'cap-gain': Dominance.MAX, 'Income': Dominance.MIN},
                         size=30_162,
                         seed=seed,
                         provided=False)

class Adult9(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num','sex','cap-loss','age','cap-gain'],
                         preference=['hrs-wk', 'Income'],
                         effect={'educ-num': {'age': 1, 'sex': 1},
                                 'hrs-wk': {'age': 1, 'educ-num': 1},
                                 'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                                 'captial-investments': {'family-inheritence': 0, 'age': 0},
                                 'cap-gain': {'captial-investments': 0},
                                 'cap-loss': {'captial-investments': 0},
                                 'family-inheritence': {'age': 0, 'sex': 0},
                                 },
                         dominance={'hrs-wk': Dominance.MIN, 'Income': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'educ-num'})])

class Adult10(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='adult',
                         control=['educ-num', 'sex', 'hrs-wk', 'Income'],
                         preference=['age', 'cap-gain', 'cap-loss'],
                         effect={
                             'educ-num': {'age': 1, 'sex': 1},
                             'hrs-wk': {'age': 1, 'educ-num': 1},
                             'Income': {'educ-num': 1, 'sex': 1, 'cap-gain': 1, 'cap-loss': -1, 'hrs-wk': 1},
                             'captial-investments': {'family-inheritence': 0, 'age': 0},
                             'cap-gain': {'captial-investments': 0},
                             'cap-loss': {'captial-investments': 0},
                             'family-inheritence': {'age': 0, 'sex': 0}
                         },
                         dominance=dominance,
                         infer_controls={
                             'age': Dominance.MIN,
                             'cap-gain': Dominance.MAX,
                             'cap-loss': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)
