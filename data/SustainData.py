from dataclasses import dataclass
from .InventoryItemData import *
from .SkillData import *
from enum import IntEnum

class SustainType(IntEnum):
    HP_RECOVERY = 0
    TP_RECOVERY = 1
    HP_TP_RECOVERY = 2
    REVIVE = 3
    #ENCOUNTER_REDUCTION = 4
    # Could have "petrify" cure, but only a very small handful of enemy can inflict it.

class SustainSource(IntEnum):
    ITEM = 0
    SKILL = 1

class SustainUseType(IntEnum):
    BATTLE_ONLY = 0
    FIELD_ONLY = 1
    ANYWHERE = 2
    END_OF_BATTLE = 3
    BATTLE_ONLY_END_OF_TURN_BUFF = 4

class SustainTarget(IntEnum):
    SINGLE = 0
    SELF = 1
    ALL = 2

class SustainValueType(IntEnum):
    FLAT = 0
    PERCENT = 1
    H_TOUCH = 2 # H.Touch is weird.


@dataclass
class SustainData:
    related_id: int
    sustain_type: SustainType
    sustain_source: SustainSource
    use_type: SustainUseType
    target: SustainTarget
    value_type: SustainValueType
    value: int
    value_2: int = 0


SUSTAIN_ITEMS: list[SustainData] = [
    # Items
    SustainData(EO1ItemID.MEDICA, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 30),
    SustainData(EO1ItemID.MEDICA_II, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 100),
    SustainData(EO1ItemID.MEDICA_III, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 200),
    SustainData(EO1ItemID.MEDICA_IV, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 350),
    SustainData(EO1ItemID.MEDICA_V, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.PERCENT, 100),
    SustainData(EO1ItemID.AMRITA, SustainType.TP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 15),
    SustainData(EO1ItemID.AMRITA_II, SustainType.TP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 50),
    SustainData(EO1ItemID.HAMAO, SustainType.HP_TP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 300, 50),
    SustainData(EO1ItemID.HAMAOPRIME, SustainType.HP_TP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.PERCENT, 100, 100),
    SustainData(EO1ItemID.SOMA, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.ALL, SustainValueType.FLAT, 144),
    SustainData(EO1ItemID.SOMAPRIME, SustainType.HP_RECOVERY, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.ALL, SustainValueType.PERCENT, 100),
    SustainData(EO1ItemID.NECTAR, SustainType.REVIVE, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 18),
    SustainData(EO1ItemID.NECTAR_II, SustainType.REVIVE, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 300),
    SustainData(EO1ItemID.NECTAR_III, SustainType.REVIVE, SustainSource.ITEM, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.PERCENT, 100),
]

SUSTAIN_SKILLS: list[SustainData] = [
    # Skills
    #SustainData(EO1Skills.SURVIVALIST_AMBUSH, ),
    #SustainData(EO1Skills.SURVIVALIST_AWARE, ),
    #SustainData(EO1Skills.SURVIVALIST_STALKER, SustainType.ENCOUNTER_REDUCTION, SustainSource.SKILL, SustainUseType.FIELD_ONLY, SustainTarget.ALL),
    SustainData(EO1Skills.PROTECTOR_CURE, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 17, 77),
    SustainData(EO1Skills.PROTECTOR_CURE_II, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 63, 133),
    #SustainData(EO1Skills.PROTECTOR_STALKER, SustainType.ENCOUNTER_REDUCTION, SustainSource.SKILL, SustainUseType.FIELD_ONLY, SustainTarget.ALL),
    #SustainData(EO1Skills.DARK_HUNTER_DRAIN, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY, SustainTarget.SELF),
    SustainData(EO1Skills.RONIN_IBUKI, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY, SustainTarget.SELF, SustainValueType.FLAT, 17, 77),
    #SustainData(EO1Skills.RONIN_MIKIRI, ),
    SustainData(EO1Skills.MEDIC_CURE, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 15, 75),
    SustainData(EO1Skills.MEDIC_CURE_II, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 60, 130),
    SustainData(EO1Skills.MEDIC_CURE_III, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 500, 500),
    SustainData(EO1Skills.MEDIC_SALVE, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.ALL, SustainValueType.FLAT, 20, 80),
    SustainData(EO1Skills.MEDIC_SALVE_II, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.ALL, SustainValueType.FLAT, 75, 180),
    SustainData(EO1Skills.MEDIC_REVIVE, SustainType.REVIVE, SustainSource.SKILL, SustainUseType.ANYWHERE, SustainTarget.SINGLE, SustainValueType.FLAT, 15, 75),
    SustainData(EO1Skills.MEDIC_REGEN, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF, SustainTarget.ALL, SustainValueType.PERCENT, 5, 16),
    #SustainData(EO1Skills.MEDIC_H_TOUCH, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.FIELD_ONLY, SustainTarget.ALL, SustainValueType.H_TOUCH, 25, 40),
    SustainData(EO1Skills.MEDIC_PATCH_UP, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.END_OF_BATTLE, SustainTarget.ALL, SustainValueType.PERCENT, 1, 12),
    SustainData(EO1Skills.MEDIC_TP_REGEN, SustainType.TP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF, SustainTarget.SELF, SustainValueType.FLAT, 1, 5),
    SustainData(EO1Skills.ALCHEMIST_TP_REGEN, SustainType.TP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF, SustainTarget.SELF, SustainValueType.FLAT, 1, 5),
    SustainData(EO1Skills.TROUBADOUR_HEALING, SustainType.HP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF, SustainTarget.ALL, SustainValueType.PERCENT, 2, 13),
    SustainData(EO1Skills.TROUBADOUR_RELAXING, SustainType.TP_RECOVERY, SustainSource.SKILL, SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF, SustainTarget.ALL, SustainValueType.PERCENT, 1, 5),
    #SustainData(EO1Skills.TROUBADOUR_STALKER, SustainType.ENCOUNTER_REDUCTION, SustainSource.SKILL, SustainUseType.FIELD_ONLY, SustainTarget.ALL),
    #SustainData(EO1Skills.FLEE, ),
]

SUSTAIN_ITEM_BY_ID: dict[int, SustainData] = {data.related_id:data for data in SUSTAIN_ITEMS}
SUSTAIN_SKILL_BY_ID: dict[int, SustainData] = {data.related_id:data for data in SUSTAIN_SKILLS}
