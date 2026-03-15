from .real import RealDataset, Dominance
from .. import SyntheticDataset


class Hong_Kong_Weather_1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='hong_kong_weather',
                         control=['mean_temp', 'max_temp', 'min_grass_temp', 'mean_wet_bulb_temp', 'mean_dew_point_temp', 'rel_humidity', 'cloud', 'rainfall'],
                         preference=['min_temp', 'pressure'],
                         effect={
                             'min_temp': {'cloud': 1},
                             'max_temp': {'cloud': -1},
                             'mean_temp': {'min_temp': 1, 'max_temp': 1},
                             'pressure': {'mean_temp': -1},
                             'rel_humidity': {'mean_temp': -1, 'mean_dew_point_temp': 1},
                             'cloud': {'rel_humidity': 1},
                             'rainfall': {'cloud': 1, 'rel_humidity': 1, 'pressure': -1},
                             'mean_wet_bulb_temp': {'mean_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1},
                             'min_grass_temp': {'min_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1, 'cloud': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'min_temp': Dominance.MAX,
                             'pressure': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)



class Hong_Kong_Weather_2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='hong_kong_weather',
                         control=['mean_temp', 'max_temp', 'min_grass_temp', 'mean_wet_bulb_temp', 'rel_humidity', 'cloud', 'rainfall'],
                         preference=['min_temp', 'pressure', 'mean_dew_point_temp'],
                         effect={
                             'min_temp': {'cloud': 1},
                             'max_temp': {'cloud': -1},
                             'mean_temp': {'min_temp': 1, 'max_temp': 1},
                             'pressure': {'mean_temp': -1},
                             'rel_humidity': {'mean_temp': -1, 'mean_dew_point_temp': 1},
                             'cloud': {'rel_humidity': 1},
                             'rainfall': {'cloud': 1, 'rel_humidity': 1, 'pressure': -1},
                             'mean_wet_bulb_temp': {'mean_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1},
                             'min_grass_temp': {'min_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1, 'cloud': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'mean_dew_point_temp': Dominance.MIN,
                             'min_temp': Dominance.MAX,
                             'pressure': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)


class Hong_Kong_Weather_3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='hong_kong_weather',
                         control=['mean_temp', 'max_temp', 'min_grass_temp', 'min_temp', 'mean_dew_point_temp', 'pressure'],
                         preference=['rel_humidity', 'mean_wet_bulb_temp', 'rainfall', 'cloud'],
                         effect={
                             'min_temp': {'cloud': 1},
                             'max_temp': {'cloud': -1},
                             'mean_temp': {'min_temp': 1, 'max_temp': 1},
                             'pressure': {'mean_temp': -1},
                             'rel_humidity': {'mean_temp': -1, 'mean_dew_point_temp': 1},
                             'cloud': {'rel_humidity': 1},
                             'rainfall': {'cloud': 1, 'rel_humidity': 1, 'pressure': -1},
                             'mean_wet_bulb_temp': {'mean_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1},
                             'min_grass_temp': {'min_temp': 1, 'rel_humidity': 1, 'mean_dew_point_temp': 1, 'cloud': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'cloud': Dominance.MAX,
                             'mean_wet_bulb_temp': Dominance.MAX,
                             'rainfall': Dominance.MAX,
                             'rel_humidity': Dominance.MAX
                         },
                         size=size,
                         seed=seed,
                         provided=False)
