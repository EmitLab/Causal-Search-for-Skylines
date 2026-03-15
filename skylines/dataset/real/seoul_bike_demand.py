from skylines.dataset import RealDataset, Dominance


class SeoulBikeDemandDataset_1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         # control=['Temperature(C)','Humidity(%)','Wind speed (m/s)','Visibility(10m)','Dew point temperature(C)','Solar Radiation (MJ/m2)','Rainfall(mm)','Snowfall (cm)','Functioning Day'],
                         control=['Temperature(C)', 'Humidity(%)', 'Wind speed (m/s)', 'Visibility(10m)',
                                  'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 'Functioning Day'],
                         preference=['Rented Bike Count', 'Hour'],
                         effect={
                             'Temperature(C)': {'Snowfall (cm)': -1,
                                                'Rainfall(mm)': 1,
                                                'Solar Radiation (MJ/m2)': 1,
                                                'Wind speed (m/s)': -1},
                             'Rainfall(mm)': {'Humidity(%)': 1},
                             'Visibility(10m)': {'Rainfall(mm)': -1},
                             'Rented Bike Count': {'Hour': 1,
                                                   'Temperature': 1,
                                                   'Visibility(10m)': 1}
                         },
                         dominance=dominance,
                         size=8760,
                         seed=seed,
                         provided=False)



class SeoulBikeDemandDataset_2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         # control=['Temperature(C)','Humidity(%)','Wind speed (m/s)','Visibility(10m)','Dew point temperature(C)','Solar Radiation (MJ/m2)','Rainfall(mm)','Snowfall (cm)','Functioning Day'],
                         control=['Hour', 'Humidity(%)', 'Wind speed (m/s)', 'Visibility(10m)',
                                  'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 'Functioning Day'],
                         preference=['Rented Bike Count', 'Temperature(C)'],
                         effect={
                             'Temperature(C)': {'Snowfall (cm)': -1,
                                                'Rainfall(mm)': 1,
                                                'Solar Radiation (MJ/m2)': 1,
                                                'Wind speed (m/s)': -1},
                             'Rainfall(mm)': {'Humidity(%)': 1},
                             'Visibility(10m)': {'Rainfall(mm)': -1},
                             'Rented Bike Count': {'Hour': 1,
                                                   'Temperature': 1,
                                                   'Visibility(10m)': 1}
                         },
                         dominance=dominance,
                         size=8760,
                         seed=seed,
                         provided=False)



class SeoulBikeDemandDataset_3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
        #                  Date, Rented Bike Count, Hour, Temperature(C), Humidity( %), Wind speed(m / s), Visibility(10m), Dew point temperature(C), Solar Radiation(MJ / m2), Rainfall(mm), Snowfall (cm), Holiday, Functioning Day
                         control=['Date', 'Rented Bike Count', 'Hour', 'Humidity(%)', 'Wind speed (m/s)', 'Visibility(10m)', 'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 'Holiday', 'Functioning Day'],
                         preference=['Temperature(C)', 'Dew point temperature(C)'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1, 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)':0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance={'Temperature(C)': Dominance.MIN, 'Dew point temperature(C)': Dominance.MAX},
                         size=8760,
                         seed=seed,
                         provided=False,
                         constant_controls=[{{"Humidity(%)", 'Rainfall(mm)', 'Rented Bike Count'}}])



class SeoulBikeDemandDataset_4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         # control=['Temperature(C)','Humidity(%)','Wind speed (m/s)','Visibility(10m)','Dew point temperature(C)','Solar Radiation (MJ/m2)','Rainfall(mm)','Snowfall (cm)','Functioning Day'],
                         control=['Date', 'Rented Bike Count', 'Hour', 'Temperature(C)', 'Wind speed (m/s)',
                                  'Visibility(10m)', 'Dew point temperature(C)', 'Rainfall(mm)', 'Snowfall (cm)',
                                  'Holiday', 'Functioning Day'],
                         preference=['Humidity(%)', 'Solar Radiation (MJ/m2)'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1,
                                                 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)': 0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance={'Humidity(%)': Dominance.MAX, 'Solar Radiation (MJ/m2)': Dominance.MAX},
                         size=8760,
                         seed=seed,
                         provided=False,
                         constant_controls=[frozenset({'Rented Bike Count', 'Visibility(10m)', 'Wind speed (m/s)'})])



class SeoulBikeDemandDataset_5(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         # control=['Temperature(C)','Humidity(%)','Wind speed (m/s)','Visibility(10m)','Dew point temperature(C)','Solar Radiation (MJ/m2)','Rainfall(mm)','Snowfall (cm)','Functioning Day'],
                         control=['Date', 'Rented Bike Count', 'Hour', 'Temperature(C)', 'Wind speed (m/s)',
                                  'Solar Radiation (MJ/m2)', 'Dew point temperature(C)', 'Rainfall(mm)', 'Snowfall (cm)',
                                  'Holiday', 'Functioning Day'],
                         preference=['Humidity(%)', 'Visibility(10m)'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1,
                                                 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)': 0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance={'Humidity(%)': Dominance.MAX, 'Visibility(10m)': Dominance.MAX},
                         size=8760,
                         seed=seed,
                         provided=False,
                         constant_controls=[])



class SeoulBikeDemandDataset_6(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         control=['Date', 'Visibility(10m)', 'Hour','Humidity(%)',  'Wind speed (m/s)',
                                  'Solar Radiation (MJ/m2)', 'Dew point temperature(C)', 'Rainfall(mm)', 'Snowfall (cm)',
                                  'Holiday', 'Functioning Day'],
                         preference=['Temperature(C)','Rented Bike Count'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1,
                                                 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)': 0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance={'Temperature(C)': Dominance.MIN, 'Rented Bike Count': Dominance.MAX},
                         size=8760,
                         seed=seed,
                         provided=False)



class SeoulBikeDemandDataset_7(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         control=['Date', 'Rented Bike Count', 'Hour', 'Temperature(C)', 'Wind speed (m/s)',
                                  'Solar Radiation (MJ/m2)', 'Visibility(10m)', 'Rainfall(mm)', 'Snowfall (cm)',
                                  'Holiday', 'Functioning Day'],
                         preference=['Humidity(%)', 'Dew point temperature(C)'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1,
                                                 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)': 0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance={'Humidity(%)': Dominance.MAX, 'Dew point temperature(C)': Dominance.MIN},
                         size=8760,
                         seed=seed,
                         provided=False)


class SeoulBikeDemandDataset_8(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='seoul_bike_demand',
                         control=['Hour', 'Temperature(C)', 'Wind speed (m/s)',
                                  'Solar Radiation (MJ/m2)', 'Visibility(10m)', 'Holiday',
                                  'Functioning Day', 'Humidity(%)', 'Dew point temperature(C)'],
                         preference=['Rainfall(mm)', 'Snowfall (cm)', 'Rented Bike Count'],
                         effect={
                             'Season': {'Date': 0},
                             'Wind speed (m/s)': {'Season': 0},
                             'Solar Radiation (MJ/m2)': {'Season': 0, 'Hour': 0},
                             'Humidity(%)': {'Temperature(C)': 1, 'Wind speed (m/s)': 0},
                             'Temperature(C)': {'Wind speed (m/s)': 0, 'Solar Radiation (MJ/m2)': 1},
                             'Holiday': {'Date': 0, 'Season': 0},
                             'Visibility(10m)': {'Rainfall(mm)': -1, 'Snowfall (cm)': -1, 'Wind speed (m/s)': -1,
                                                 'Solar Radiation (MJ/m2)': 1},
                             'Dew point temperature(C)': {'Temperature(C)': 1, 'Humidity(%)': 1},
                             'Snowfall (cm)': {'Temperature(C)': -1, 'Humidity(%)': 1, 'Dew point temperature(C)': 1},
                             'Rainfall(mm)': {'Temperature': 1, 'Dew point temperature(C)': 1, 'Humidity(%)': 1},
                             'Functioning Day': {'Date': 0},
                             'Rented Bike Count': {'Hour': 0,
                                                   'Wind speed (m/s)': -1,
                                                   'Visibility(10m)': 1,
                                                   'Humidity(%)': -1,
                                                   'Temperature(C)': 0,
                                                   'Holiday': 1,
                                                   'Rainfall(mm)': -1,
                                                   'Snowfall (cm)': -1,
                                                   'Functioning Day': 1}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Rainfall(mm)': Dominance.MIN,
                             'Rented Bike Count': Dominance.MAX,
                             'Snowfall (cm)': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)
