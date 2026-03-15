from skylines.dataset import RealDataset, Dominance

# Elevation	Aspect	Slope	Horizontal_Distance_To_Hydrology	Vertical_Distance_To_Hydrology	Horizontal_Distance_To_Roadways	Hillshade_9am	Hillshade_Noon	Hillshade_3pm	Horizontal_Distance_To_Fire_Points	Cover_Type	Wilderness_Area	Soil_Type
class CovertypeDataset1(RealDataset):
    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='covertype',
                         control=['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways', 'Hillshade_Noon', 'Horizontal_Distance_To_Fire_Points', 'Cover_Type', 'Wilderness_Area',	'Soil_Type'],
                         preference=['Hillshade_9am', 'Hillshade_3pm'],
                         effect={
                             'Cover_Type': {'Wilderness_Area': 0, 'Soil_Type': 0, 'Hillshade_9am': 0, 'Hillshade_Noon': 0, 'Hillshade_3pm': 0, 'Elevation': 0, 'Horizontal_Distance_To_Hydrology': 0, 'Vertical_Distance_To_Hydrology': 0},
                             'Hillshade_9am': {'Aspect': -1, 'Slope': -1},
                             'Hillshade_Noon': {'Aspect': 1, 'Slope': -1},
                             'Hillshade_3pm': {'Aspect': 1, 'Slope': -1},
                             'Soil_Type': {'Slope': 0, 'Horizontal_Distance_To_Hydrology': 0},
                             'Slope': {'Elevation': 1},
                             'Horizontal_Distance_To_Hydrology': {'Elevation': 1},
                             'Vertical_Distance_To_Hydrology': {'Elevation': 1, 'Soil_Type': 0},
                             'Horizontal_Distance_To_Fire_Points': {'Horizontal_Distance_To_Hydrology': -1, 'Vertical_Distance_To_Hydrology': -1, 'Wilderness_Area': 0},
                            'Horizontal_Distance_To_Roadways': {'Wilderness_Area': 0},
                         },
                         dominance={'Hillshade_9am': Dominance.MAX, 'Hillshade_3pm': Dominance.MAX},
                         size=581_012,
                         provided=True,
                         seed=seed,
                         constant_controls=[frozenset({'Aspect'})])

class CovertypeDataset2(RealDataset):
    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='covertype',
                         control=['Hillshade_9am', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Hillshade_3pm', 'Cover_Type', 'Wilderness_Area',	'Soil_Type'],
                         preference=['Elevation', 'Horizontal_Distance_To_Fire_Points'],
                         effect={
                             'Cover_Type': {'Wilderness_Area': 0, 'Soil_Type': 0, 'Hillshade_9am': 0, 'Hillshade_Noon': 0, 'Hillshade_3pm': 0, 'Elevation': 0, 'Horizontal_Distance_To_Hydrology': 0, 'Vertical_Distance_To_Hydrology': 0},
                             'Hillshade_9am': {'Aspect': -1, 'Slope': -1},
                             'Hillshade_Noon': {'Aspect': 1, 'Slope': -1},
                             'Hillshade_3pm': {'Aspect': 1, 'Slope': -1},
                             'Soil_Type': {'Slope': 0, 'Horizontal_Distance_To_Hydrology': 0},
                             'Slope': {'Elevation': 1},
                             'Horizontal_Distance_To_Hydrology': {'Elevation': 1},
                             'Vertical_Distance_To_Hydrology': {'Elevation': 1, 'Soil_Type': 0},
                             'Horizontal_Distance_To_Fire_Points': {'Horizontal_Distance_To_Hydrology': -1, 'Vertical_Distance_To_Hydrology': -1, 'Wilderness_Area': 0},
                            'Horizontal_Distance_To_Roadways': {'Wilderness_Area': 0},
                         },
                         dominance={'Elevation': Dominance.MAX, 'Horizontal_Distance_To_Fire_Points': Dominance.MAX},
                         size=581_012,
                         provided=True,
                         seed=seed,
                         constant_controls=[frozenset({'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology'})])

class CovertypeDataset3(RealDataset):
    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 10_000,
                 seed: int = 42):
        super().__init__(file_name='covertype',
                         control=['Hillshade_9am', 'Aspect', 'Horizontal_Distance_To_Fire_Points', 'Horizontal_Distance_To_Hydrology', 'Elevation', 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Hillshade_3pm', 'Cover_Type', 'Wilderness_Area',	'Soil_Type'],
                         preference=['Vertical_Distance_To_Hydrology', 'Slope'],
                         effect={
                             'Cover_Type': {'Wilderness_Area': 0, 'Soil_Type': 0, 'Hillshade_9am': 0, 'Hillshade_Noon': 0, 'Hillshade_3pm': 0, 'Elevation': 0, 'Horizontal_Distance_To_Hydrology': 0, 'Vertical_Distance_To_Hydrology': 0},
                             'Hillshade_9am': {'Aspect': -1, 'Slope': -1},
                             'Hillshade_Noon': {'Aspect': 1, 'Slope': -1},
                             'Hillshade_3pm': {'Aspect': 1, 'Slope': -1},
                             'Soil_Type': {'Slope': 0, 'Horizontal_Distance_To_Hydrology': 0},
                             'Slope': {'Elevation': 1},
                             'Horizontal_Distance_To_Hydrology': {'Elevation': 1},
                             'Vertical_Distance_To_Hydrology': {'Elevation': 1, 'Soil_Type': 0},
                             'Horizontal_Distance_To_Fire_Points': {'Horizontal_Distance_To_Hydrology': -1, 'Vertical_Distance_To_Hydrology': -1, 'Wilderness_Area': 0},
                            'Horizontal_Distance_To_Roadways': {'Wilderness_Area': 0},
                         },
                         dominance={'Vertical_Distance_To_Hydrology': Dominance.MIN, 'Slope': Dominance.MAX},
                         size=581_012,
                         provided=True,
                         seed=seed,
                         constant_controls=[frozenset({'Elevation'})])
