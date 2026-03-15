from .data.pire._effect_json import pire_effects
from .real import RealDataset, Dominance

class Pire(RealDataset):

    def __init__(self,
                 dominance: dict[str, Dominance],
                 size: int = None,
                 seed: int = 42):
        super().__init__(file_name='pire',
                         control=['plant.port_a.m_flow', 'plant.T_a.T',
                                  'plant.port_a.p',	'plant.T_b.T', 'plant.port_b.p', 'plant.mFloEnt.m_flow',
                                  'plant.senTemEnt.T', 'plant.senTemLvg.T', 'plant.byp.m_flow',
                                  'plant.heaPumHea.port_a1.m_flow', 'plant.heaPumHea.P', 'plant.heaPumCoo.port_a2.m_flow',
                                  'plant.heaPumCoo.P', 'plant.tow.port_a.m_flow', 'plant.tow.P', 'substation1.loaCoo',
                                  'substation1.port_a.m_flow', 'substation1.Ta', 'substation1.Tb',
                                  'substation1.spaceHeating.port_a.m_flow', 'substation1.spaceHeating.TSouEnt.T',
                                  'substation1.spaceHeating.TSouLvg.T', 'substation1.spaceHeating.pumSou.PPum',
                                  'substation1.PHea', 'substation1.spaceCooling.port_a.m_flow',
                                  'substation1.spaceCooling.mWseSou.m_flow',	'substation1.spaceCooling.mHPSou.m_flow',
                                  'substation1.spaceCooling.TSouEnt.T', 'substation1.spaceCooling.TSouLvg.T',
                                  'substation1.spaceCooling.pumWSESou.P', 'substation1.spaceCooling.pumHPSou.P',
                                  'substation1.PCoo', 'pipWar1.port_a.p', 'pipWar1.port_b.p', 'pipCol1.port_a.p',
                                  'pipCol1.port_b.p'],
                         preference=['time', 'plant.TDryBulb.y', 'plant.yMod'],
                         effect=pire_effects,
                         dominance=dominance,
                         size=52_851,
                         seed=seed,
                         provided=True)
