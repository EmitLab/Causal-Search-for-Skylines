from .real import RealDataset, Dominance

class IndividualHouseholdPowerConsumption1(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 2_049_280,
                 seed: int = 42):
        super().__init__(file_name='individual_household_power_consumption',
                         control=['Date','Time','Global_active_power','Global_intensity','Voltage','Sub_metering_1','Sub_metering_3'],
                         preference=['Sub_metering_2', 'Global_reactive_power'],
                         effect={
                             'Global_intensity': {'Voltage': 1, 'Global_apparent_power': 1},
                             'Global_apparent_power': {'Global_reactive_power': 1, 'Global_active_power': 1},
                             'Global_reactive_power': {'Global_active_power': -1, 'Phase Angle': -1},
                             'Global_active_power': {'Sub_metering_1': 1, 'Sub_metering_2': 1, 'Sub_metering_3': 1},
                             'Sub_metering_1': {'Date': 0, 'Time': 0},
                             'Sub_metering_2': {'Date': 0, 'Time': 0},
                             'Sub_metering_3': {'Date': 0, 'Time': 0}
                         },
                         dominance={'Sub_metering_2': Dominance.MAX, 'Global_reactive_power': Dominance.MAX},
                         size=2_049_280,
                         seed=seed,
                         provided=True,
                         constant_controls=[frozenset({'Global_active_power'})])



"""Not using"""
class IndividualHouseholdPowerConsumption2(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 2_049_280,
                 seed: int = 42):
        super().__init__(file_name='individual_household_power_consumption',
                         control=['Date','Time','Global_active_power','Global_reactive_power','Voltage','Sub_metering_2','Sub_metering_1'],
                         preference=['Sub_metering_3', 'Global_intensity'],
                         effect={
                             'Global_intensity': {'Voltage': 1, 'Global_apparent_power': 1},
                             'Global_apparent_power': {'Global_reactive_power': 1, 'Global_active_power': 1},
                             'Global_reactive_power': {'Global_active_power': -1, 'Phase Angle': -1},
                             'Global_active_power': {'Sub_metering_1': 1, 'Sub_metering_2': 1, 'Sub_metering_3': 1},
                             'Sub_metering_1': {'Date': 0, 'Time': 0},
                             'Sub_metering_2': {'Date': 0, 'Time': 0},
                             'Sub_metering_3': {'Date': 0, 'Time': 0}
                         },
                         dominance={'Sub_metering_3': Dominance.MAX, 'Global_intensity': Dominance.MIN},
                         size=2_049_280,
                         seed=seed,
                         provided=True)



class IndividualHouseholdPowerConsumption3(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 2_049_280,
                 seed: int = 42):
        super().__init__(file_name='individual_household_power_consumption',
                         control=['Global_intensity','Global_active_power','Global_reactive_power','Sub_metering_1'],
                         preference=['Sub_metering_2', 'Sub_metering_3', 'Voltage'],
                         effect={
                             'Global_intensity': {'Voltage': 1, 'Global_apparent_power': 1},
                             'Global_apparent_power': {'Global_reactive_power': 1, 'Global_active_power': 1},
                             'Global_reactive_power': {'Global_active_power': -1, 'Phase Angle': -1},
                             'Global_active_power': {'Sub_metering_1': 1, 'Sub_metering_2': 1, 'Sub_metering_3': 1},
                             'Sub_metering_1': {'Date': 0, 'Time': 0},
                             'Sub_metering_2': {'Date': 0, 'Time': 0},
                             'Sub_metering_3': {'Date': 0, 'Time': 0}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Sub_metering_2': Dominance.MAX,
                             'Sub_metering_3': Dominance.MIN,
                             'Voltage': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)


class IndividualHouseholdPowerConsumption4(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance] = None,
                 size: int = 2_049_280,
                 seed: int = 42):
        super().__init__(file_name='individual_household_power_consumption',
                         control=['Global_active_power', 'Global_reactive_power', 'Sub_metering_1'],
                         preference=['Sub_metering_2', 'Sub_metering_3', 'Global_intensity', 'Voltage'],
                         effect={
                             'Global_intensity': {'Voltage': 1, 'Global_apparent_power': 1},
                             'Global_apparent_power': {'Global_reactive_power': 1, 'Global_active_power': 1},
                             'Global_reactive_power': {'Global_active_power': -1, 'Phase Angle': -1},
                             'Global_active_power': {'Sub_metering_1': 1, 'Sub_metering_2': 1, 'Sub_metering_3': 1},
                             'Sub_metering_1': {'Date': 0, 'Time': 0},
                             'Sub_metering_2': {'Date': 0, 'Time': 0},
                             'Sub_metering_3': {'Date': 0, 'Time': 0}
                         },
                         dominance=dominance,
                         infer_controls={
                             'Global_intensity': Dominance.MIN,
                             'Sub_metering_2': Dominance.MAX,
                             'Sub_metering_3': Dominance.MIN,
                             'Voltage': Dominance.MIN
                         },
                         size=size,
                         seed=seed,
                         provided=False)
