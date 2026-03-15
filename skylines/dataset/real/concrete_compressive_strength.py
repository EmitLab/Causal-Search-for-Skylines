from .real import RealDataset, Dominance

# cement,blast furnace,fly ash,water,superplasticizer,coarse aggregate,fine aggregate,age,concrete compressive strength

class ConcreteCompressiveStrength1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='concrete_compressive_strength',
                         control=['blast furnace slag','fly ash','superplasticizer','coarse aggregate','fine aggregate','age','concrete compressive strength'],
                         preference=['water', 'cement'],
                         effect={
                                'concrete compressive strength': {'cement': 1, 'blast furnace slag': 1,'fly ash': 1,
                                                                  'water': -1, 'superplasticizer': 1,
                                                                  'coarse aggregate': 1,'fine aggregate': 1,'age': 1},
                                 },
                         dominance={'water': Dominance.MIN, 'cement': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'concrete compressive strength'})])

class ConcreteCompressiveStrength2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='concrete_compressive_strength',
                         control=['blast furnace slag','fly ash','superplasticizer','coarse aggregate','fine aggregate','water','concrete compressive strength'],
                         preference=['age', 'cement'],
                         effect={
                                'concrete compressive strength': {'cement': 1, 'blast furnace slag': 1,'fly ash': 1,
                                                                  'water': -1, 'superplasticizer': 1,
                                                                  'coarse aggregate': 1,'fine aggregate': 1,'age': 1},
                                 },
                         dominance={'age': Dominance.MIN, 'cement': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'concrete compressive strength'})])

class ConcreteCompressiveStrength3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='concrete_compressive_strength',
                         control=['cement','blast furnace slag','fly ash','superplasticizer','coarse aggregate','age','concrete compressive strength'],
                         preference=['water', 'fine aggregate'],
                         effect={
                                'concrete compressive strength': {'cement': 1, 'blast furnace slag': 1,'fly ash': 1,
                                                                  'water': -1, 'superplasticizer': 1,
                                                                  'coarse aggregate': 1,'fine aggregate': 1,'age': 1},
                                 },
                         dominance={'water': Dominance.MAX, 'fine aggregate': Dominance.MAX},
                         size=size,
                         seed=seed,
                         provided=False)

class ConcreteCompressiveStrength4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='concrete_compressive_strength',
                         control=['cement', 'superplasticizer', 'coarse aggregate', 'fine aggregate', 'age', 'concrete compressive strength'],
                         preference=['blast furnace slag', 'fly ash', 'water'],
                         effect={
                             'concrete compressive strength': {
                                 'cement': 1,
                                 'blast furnace slag': 1,
                                 'fly ash': 1,
                                 'water': -1,
                                 'superplasticizer': 1,
                                 'coarse aggregate': 1,
                                 'fine aggregate': 1,
                                 'age': 1},
                         },
                         dominance=dominance,
                         infer_controls={
                             'blast furnace slag': Dominance.MIN,
                             'fly ash': Dominance.MAX,
                             'water': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)

class ConcreteCompressiveStrength5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='concrete_compressive_strength',
                         control=['cement', 'water', 'coarse aggregate', 'fine aggregate', 'age', 'concrete compressive strength'],
                         preference=['blast furnace slag', 'fly ash', 'superplasticizer'],
                         effect={
                             'concrete compressive strength': {
                                 'cement': 1,
                                 'blast furnace slag': 1,
                                 'fly ash': 1,
                                 'water': -1,
                                 'superplasticizer': 1,
                                 'coarse aggregate': 1,
                                 'fine aggregate': 1,
                                 'age': 1},
                         },
                         dominance=dominance,
                         infer_controls={
                             'blast furnace slag': Dominance.MIN,
                             'fly ash': Dominance.MAX,
                             'superplasticizer': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)
