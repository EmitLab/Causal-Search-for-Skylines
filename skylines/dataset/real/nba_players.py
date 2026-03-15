from .real import RealDataset, Dominance


class NBA_Players_1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(file_name='NBA_Players',
                         control=['player_height', 'player_weight'],
                         preference=['reb', 'ast'],
                         effect={'reb': {'player_height': 1.0, 'player_weight': 1.0},
                                 'ast': {'player_height': -1.0, 'player_weight': -1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class NBA_Players_2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(file_name='NBA_Players',
                         control=['player_height'],
                         preference=['player_weight', 'ast'],
                         effect={'player_weight': {'player_height': 1.0},
                                 'ast': {'player_height': 1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class NBA_Players_3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(file_name='NBA_Players',
                         control=['draft_round', 'draft_number'],
                         preference=['player_height', 'ast'],
                         effect={'player_height': {'draft_round': -1.0, 'draft_number': -1.0},
                                 'ast': {'draft_round': -1.0, 'draft_number': -1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)


class NBA_Players_4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10000,
                 seed: int = 42):
        super().__init__(file_name='NBA_Players',
                         control=['DR&DN'],
                         preference=['player_height', 'ast'],
                         effect={'player_height': {'DR&DN': -1.0},
                                 'ast': {'DR&DN': -1.0}},
                         dominance=dominance,
                         size=size,
                         seed=seed)
