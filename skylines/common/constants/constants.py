from skylines import n_samples
from skylines.dataset import *


def recursive_dominance_combinations(preference: list[str], index: int) -> list[dict[str, Dominance]]:
    if index == len(preference) - 1:
        return [{preference[index]: Dominance.MAX}, {preference[index]: Dominance.MIN}]

    next_combinations = recursive_dominance_combinations(preference, index + 1)

    combinations = []
    for combination in next_combinations:
        combinations.append({preference[index]: Dominance.MAX} | combination)
    for combination in next_combinations:
        combinations.append({preference[index]: Dominance.MIN} | combination)

    return combinations


def get_all_dominance_combinations(dataset_class: Dataset.__class__) -> list[
    tuple[Dataset.__class__, dict[str, Dominance]]]:
    dataset: Dataset = dataset_class(size=n_samples)
    return [(dataset_class, combination) for combination in recursive_dominance_combinations(sorted(dataset.preference), 0)]


__experiments = None


def get_experiments():
    global __experiments

    if __experiments is None:
        __experiments = {
            1: get_all_dominance_combinations(XY_C_1),  # XX, NN
            2: get_all_dominance_combinations(XY_CD_1),  # XX, NN
            3: get_all_dominance_combinations(XYZ_C_1),  # XXX, NNN
            4: [(XYZ_CD_1, None),
                (XYZ_CD_1, {'X': Dominance.MIN, 'Y': Dominance.MAX, 'Z': Dominance.MAX})],
            5: [(XYZ_CD_2, None)],
            6: [(XYZ_CDE, None)],
            7: [(XYZW_ABCDEF_1, None)],
            8: [(XYZW_ABCDEF_2, None)],
            9: [(XYZW_ABCDEFG_1, None)],
            10: [(XYZW_ABCDEFG_2, None)],
            11: [(XYZW_ABCDEFG_3, None)],
            12: [(XYZW_ABCDEFG_4, None)], # This experiment is identical to experiment 9 (mistake, don't run)
            13: [(NBA_Players_1, None)],
            14: [(NBA_Players_2, None)],
            15: [(NBA_Players_3, None)],
            16: [(NBA_Players_4, None)],
            17: [(XY_ABC_1, None)],
            18: [(XY_ABCD, None)],
            19: [(Collider_XYZ_CDE_1, None)],
            20: get_all_dominance_combinations(Collider_XYZ_CDE_2),
            21: [(Collider_XYZW_ABCD_1, None)],
            22: [(Collider_XYZW_ABCD_2, None)],
            23: [(XY_C_2, None)],
            24: [(XY_CD_2, None)],
            25: [(XYZ_C_2, None)],
            26: [(XYZ_C_3, None)],
            27: [(XYZWPQRSTU_ABCDEF, None)],
            28: [(Adult1, {'Income': Dominance.MAX, 'educ-num': Dominance.MIN})],
            29: [(Adult2, {'Income': Dominance.MAX, 'age': Dominance.MIN})],
            30: [(Adult3, {'Income': Dominance.MIN, 'cap-gain': Dominance.MAX})],
            31: [(Adult4, {'Income': Dominance.MAX, 'hrs-wk': Dominance.MIN})],
            32: [(XY_CD_3, None)],
            33: [(XY_CD_4, None)],
            34: [(XY_CD_5, None)],
            35: [(XY_CD_6, None)],
            36: [(XY_CD_7, None)],
            37: [(XY_CD_8, None)],
            38: [(XY_CDE_1, None)],
            39: [(XY_CDE_2, None)],
            40: [(XY_ABCD_1_LN, None)],
            41: [(XY_ABCD_1_HN, None)],
            42: [(XY_ABCD_2_LN, None)],
            43: [(XY_ABCD_2_HN, None)],
            44: [(XY_ABCD_3_LN, None)],
            45: [(XY_ABCD_3_HN, None)],
            46: [(XY_ABCD_4_LN, None)],
            47: [(XY_ABCD_4_HN, None)],
            48: [(SeoulBikeDemandDataset_1, {'Rented Bike Count': Dominance.MAX, 'Hour': Dominance.MIN})],
            49: [(SeoulBikeDemandDataset_2, {'Rented Bike Count': Dominance.MAX, 'Temperature(C)': Dominance.MIN})],
            53: [(IndividualHouseholdPowerConsumption1, None)],
            54: [(WineQualityWhite1, None)],
            55: [(WineQualityWhite2, None)],
            56: [(WineQualityWhite3, None)],
            57: [(WineQualityWhite4, None)],
            58: [(Adult5, None)],
            59: [(Adult6, None)],
            60: [(Adult7, None)],
            61: [(Adult8, None)],
            62: [(Adult9, None)],
            63: [(Abalone1, None)],
            64: [(Abalone2, None)],
            65: [(Abalone3, None)],
            66: [(AutoMPG3, None)],
            67: [(AutoMPG4, None)],
            68: [(ConcreteCompressiveStrength1, None)],
            69: [(ConcreteCompressiveStrength2, None)],
            70: [(ConcreteCompressiveStrength3, None)],
            71: [(IndividualHouseholdPowerConsumption1, None)],
            72: [(CovertypeDataset1, None)],
            73: [(CovertypeDataset2, None)],
            74: [(CovertypeDataset3, None)],
            75: get_all_dominance_combinations(AutoMPG5),  # NNX, XXN
            76: [(XY_C_4, None)],
            77: [(XY_C_5, None)],
            78: get_all_dominance_combinations(Abalone4),  # NNX, XXN
            79: get_all_dominance_combinations(Abalone5),  # NNX, XXN
            80: get_all_dominance_combinations(Abalone6),  # NNX, XXN
            81: get_all_dominance_combinations(Adult10),  # NXX, XNN
            82: get_all_dominance_combinations(ConcreteCompressiveStrength4),  # NXX, XNN
            83: get_all_dominance_combinations(ConcreteCompressiveStrength5),  # NXN, XNX
            84: get_all_dominance_combinations(SeoulBikeDemandDataset_8),  # NXN, XNX
            85: get_all_dominance_combinations(WineQualityWhite5),  # XNX, NXN
            86: get_all_dominance_combinations(IndividualHouseholdPowerConsumption3),  # XNN, NXX
            87: get_all_dominance_combinations(Hong_Kong_Weather_1),  # XX, NN
            88: get_all_dominance_combinations(Hong_Kong_Weather_2),  # NXX, XNN
            89: get_all_dominance_combinations(DryBean_1),  # XX, NN
            90: get_all_dominance_combinations(DryBean_2),  # NXX, XNN
            91: get_all_dominance_combinations(XY_C_1_b),  # XN, NX
            92: get_all_dominance_combinations(XY_CD_1_b),  # XN, NX
            93: get_all_dominance_combinations(XYZ_C_1_b),  # XX, NN
            94: [(XYZW_ABCDEFG_2_b, None)],
            95: [(XYZW_ABCDEFG_2_c, None)],
            96: [(XYZW_ABCDEFG_2_d, None)],
            97: [(XY_ABCD_b, None)],
            98: [(XY_ABCD_c, None)],
            99: [(Collider_XYZ_CDE_2_b, None)],
            100: [(Collider_XYZ_CDE_2_c, None)],
            101: [(Collider_XYZ_CDE_2_d, None)],
            102: get_all_dominance_combinations(XY_C_1_b),  # XN, NX
            103: get_all_dominance_combinations(XY_C_1),  # XX, NN
            104: get_all_dominance_combinations(XY_CD_1_b),  # XN, NX
            105: get_all_dominance_combinations(XY_CD_1),  # XX, NN
            106: get_all_dominance_combinations(XYZ_C_1_c),  # XXN, NNX
            107: get_all_dominance_combinations(XYZ_C_1_d),  # XNX, NXN
            108: get_all_dominance_combinations(XYZ_C_1_e),  # NXX, XNN
            109: get_all_dominance_combinations(XYZ_C_1_e),
            110: get_all_dominance_combinations(XYZ_C_1_c),
            111: [(XYZ_C_1_d, {'X': Dominance.MAX, 'Y': Dominance.MAX, 'Z': Dominance.MIN})],
            112: get_all_dominance_combinations(XYZ_C_1),
            113: get_all_dominance_combinations(XYZ_C_1_f),  # XN, NX
            114: [(XYZ_C_1_f, {'X': Dominance.MIN, 'Y': Dominance.MAX})],
            115: [(XYZ_C_1_b, {'X': Dominance.MIN, 'Y': Dominance.MIN})],
            116: get_all_dominance_combinations(XYZ_C_1_g),  # XX, NN
            117: get_all_dominance_combinations(XYZ_C_1_h),  # XN, NX
            118: [(XYZ_C_1_h, {'Y': Dominance.MIN, 'Z': Dominance.MAX})],
            119: [(XYZ_C_1_g, {'Y': Dominance.MIN, 'Z': Dominance.MIN})],
            120: get_all_dominance_combinations(XYZ_C_1_i),  # XX, NN
            121: get_all_dominance_combinations(XYZ_C_1_j),  # XN, NX
            122: [(XYZ_C_1_j, {'X': Dominance.MIN, 'Z': Dominance.MAX})],
            123: [(XYZ_C_1_i, {'X': Dominance.MIN, 'Z': Dominance.MIN})],
            124: get_all_dominance_combinations(XY_CD_9),  # XX, NN
            125: get_all_dominance_combinations(XY_CD_10),  # XN, NX
            126: get_all_dominance_combinations(XYZ_CD_3),  # XXX, NNN
            127: get_all_dominance_combinations(XYZ_CD_4),  # XNX, NXN
            128: get_all_dominance_combinations(XYZ_CD_5),  # XXN, NXX, NNX, XNN
            129: get_all_dominance_combinations(XYZ_CD_6),  # XX, NN
            130: get_all_dominance_combinations(XYZ_CD_7),  # XN, NX
            131: get_all_dominance_combinations(XYZ_CD_8),  # XX, NN
            132: get_all_dominance_combinations(XYZ_CD_9),  # XN, NX
            133: get_all_dominance_combinations(XYZ_CD_10),  # XX, NN
            134: get_all_dominance_combinations(XYZ_CD_11),  # XN, NX
            135: [(AutoMPG6, {'weight': Dominance.MAX, 'displacement': Dominance.MIN, 'acceleration': Dominance.MAX})],
            136: get_all_dominance_combinations(XYZ_CD_12_a),  # XXX, NNN
            137: get_all_dominance_combinations(XYZ_CD_12_b),  # XXN, NNX
            138: get_all_dominance_combinations(XYZ_CD_14),  # XNX, NXN
            139: get_all_dominance_combinations(XYZ_CD_13),  # XNN, NXX
            140: get_all_dominance_combinations(XYZW_CDE_1),  # XXXX, NNNN
            141: get_all_dominance_combinations(XYZW_CDE_10),  # XNNX, NXXN
            142: get_all_dominance_combinations(XYZW_CDE_2),  # XNXX, NXNN
            143: get_all_dominance_combinations(XYZW_CDE_11),  # XXNX, NNXN
            144: get_all_dominance_combinations(XYZW_CDE_3_a),  # XXXN, NNNX
            145: get_all_dominance_combinations(XYZW_CDE_3_b),  # XNNN, NXXX
            146: get_all_dominance_combinations(XYZW_CDE_4),  # XNXN, NXNX
            147: get_all_dominance_combinations(XYZW_CDE_12),  # XXNN, NNXX
            148: get_all_dominance_combinations(XYZW_CDE_5_a),  # XXXX, NNNN
            149: get_all_dominance_combinations(XYZW_CDE_5_b),  # XNNX, NXXN
            150: get_all_dominance_combinations(XYZW_CDE_6),  # XNXX, NXNN
            151: get_all_dominance_combinations(XYZW_CDE_7),  # XXNX, NNXN
            152: get_all_dominance_combinations(XYZW_CDE_8_a),  # XXXN, NNNX
            153: get_all_dominance_combinations(XYZW_CDE_8_b),  # XNNN, NXXX
            154: get_all_dominance_combinations(XYZW_CDE_9_a),  # XNXN, NXNX
            155: get_all_dominance_combinations(XYZW_CDE_9_b),  # XXNN, NNXX
            156: get_all_dominance_combinations(Hong_Kong_Weather_3),  # XXXX, NNNN
            157: get_all_dominance_combinations(DryBean_3),  # XXN, NNX
            158: get_all_dominance_combinations(IndividualHouseholdPowerConsumption4),  # NXNN, XNXX
            159: get_all_dominance_combinations(AutoMPG7),  # XXX, NNN
            160: get_all_dominance_combinations(AutoMPG8),  # NXN, XNX
        }

    return __experiments
