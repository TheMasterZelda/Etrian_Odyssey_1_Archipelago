from typing import TYPE_CHECKING
from dataclasses import dataclass
from enum import IntEnum

from . import ALL_SKILLS_DATA
from .ClassData import *
from .SkillData import *

class SkillItemType(IntEnum):
    INDIVIDUAL = 0
    ALL = 1
    GROUP = 2
    PROGRESSIVE = 3
    MULTI_CLASS_GROUP = 4

@dataclass(frozen=True)
class SkillItem:
    ap_item_id: int
    ap_item_name: str
    skill_item_type: SkillItemType

@dataclass(frozen=True)
class GroupSkillItem:
    name: str
    ap_item_id: int
    class_name: str
    skills: list[int]

    def get_full_name(self) -> str:
        return f"{self.name} Skills ({self.class_name})"

    def to_skill_item(self) -> SkillItem:
        return SkillItem(self.ap_item_id, self.get_full_name(), SkillItemType.GROUP)

@dataclass(frozen=True)
class MultiClassGroupSkillItem:
    name: str
    ap_item_id: int
    skill_items: list[SkillItem]

    def to_skill_item(self) -> SkillItem:
        return SkillItem(self.ap_item_id, self.name, SkillItemType.MULTI_CLASS_GROUP)

@dataclass(frozen=True)
class SkillUnlockData:
    ap_item_id: int
    ap_item_name: str
    item_count_requirement: int = 1


ALL_STATS_GROUP_SKILLS: list[GroupSkillItem] = [
    GroupSkillItem("Stats Up", 701, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_HP_UP,
        EO1Skills.LANDSKNECHT_TP_UP,
        EO1Skills.LANDSKNECHT_ATK_UP,
        EO1Skills.LANDSKNECHT_DEF_UP
    ]),
    GroupSkillItem("Stats Up", 702, EO1Class.SURVIVALIST, [
        EO1Skills.SURVIVALIST_HP_UP,
        EO1Skills.SURVIVALIST_TP_UP,
        EO1Skills.SURVIVALIST_AGI_UP,
    ]),
    GroupSkillItem("Stats Up", 703, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_HP_UP,
        EO1Skills.PROTECTOR_TP_UP,
        EO1Skills.PROTECTOR_DEF_UP,
    ]),
    GroupSkillItem("Stats Up", 704, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_HP_UP,
        EO1Skills.DARK_HUNTER_TP_UP,
        EO1Skills.DARK_HUNTER_ATK_UP,
    ]),
    GroupSkillItem("Stats Up", 705, EO1Class.MEDIC, [
        EO1Skills.MEDIC_HP_UP,
        EO1Skills.MEDIC_TP_UP,
        EO1Skills.MEDIC_ATK_UP,
    ]),
    GroupSkillItem("Stats Up", 706, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_TP_UP,
    ]),
    GroupSkillItem("Stats Up", 707, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_HP_UP,
        EO1Skills.TROUBADOUR_TP_UP,
    ]),
    GroupSkillItem("Stats Up", 708, EO1Class.RONIN, [
        EO1Skills.RONIN_HP_UP,
        EO1Skills.RONIN_TP_UP,
        EO1Skills.RONIN_ATK_UP,
    ]),
    GroupSkillItem("Stats Up", 709, EO1Class.HEXER, [
        EO1Skills.HEXER_HP_UP,
        EO1Skills.HEXER_TP_UP,
    ]),
]

ALL_GATHERING_GROUP_SKILLS: list[GroupSkillItem] = [
    GroupSkillItem("Gathering", 710, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_MINE,
    ]),
    GroupSkillItem("Gathering", 711, EO1Class.SURVIVALIST, [
        EO1Skills.SURVIVALIST_CHOP,
        EO1Skills.SURVIVALIST_MINE,
        EO1Skills.SURVIVALIST_TAKE,
    ]),
    GroupSkillItem("Gathering", 712, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_MINE,
    ]),
    GroupSkillItem("Gathering", 713, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_TAKE,
    ]),
    GroupSkillItem("Gathering", 714, EO1Class.MEDIC, [
        EO1Skills.MEDIC_CHOP,
    ]),
    GroupSkillItem("Gathering", 715, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_CHOP,
    ]),
    GroupSkillItem("Gathering", 716, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_TAKE,
    ]),
    GroupSkillItem("Gathering", 717, EO1Class.RONIN, [
        EO1Skills.RONIN_MINE,
    ]),
    GroupSkillItem("Gathering", 718, EO1Class.HEXER, [
        EO1Skills.HEXER_MINE,
    ]),
]

ALL_OTHER_GROUP_SKILLS: list[GroupSkillItem] = [
    # Landsknecht
    GroupSkillItem("Sword", 610, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_SWORDS,
        EO1Skills.LANDSKNECHT_CLEAVER,
        EO1Skills.LANDSKNECHT_TORNADO,
        EO1Skills.LANDSKNECHT_ALLSLASH,
        EO1Skills.LANDSKNECHT_2_HIT
    ]),
    GroupSkillItem("Axe", 611, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_AXES,
        EO1Skills.LANDSKNECHT_CRUSH,
        EO1Skills.LANDSKNECHT_STUNNER,
        EO1Skills.LANDSKNECHT_SILENCER,
        EO1Skills.LANDSKNECHT_2_HIT
    ]),
    GroupSkillItem("Chase", 612, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_BLAZER,
        EO1Skills.LANDSKNECHT_FREEZER,
        EO1Skills.LANDSKNECHT_SHOCKER,
        EO1Skills.LANDSKNECHT_TP_UP
    ]),
    GroupSkillItem("ATK Up Tree", 613, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_ATK_UP,
        EO1Skills.LANDSKNECHT_WAR_CRY,
        EO1Skills.LANDSKNECHT_HELL_CRY
    ]),
    GroupSkillItem("DEF Up Tree", 614, EO1Class.LANDSKNECHT, [
        EO1Skills.LANDSKNECHT_DEF_UP,
        EO1Skills.LANDSKNECHT_ARM_HEAL,
        EO1Skills.LANDSKNECHT_FLEE
    ]),

    # Survivalist
    GroupSkillItem("Bow", 620, EO1Class.SURVIVALIST, [
        EO1Skills.SURVIVALIST_BOWS,
        EO1Skills.SURVIVALIST_TRUESHOT,
        EO1Skills.SURVIVALIST_MULTIHIT,
        EO1Skills.SURVIVALIST_DISABLE,
        EO1Skills.SURVIVALIST_APOLLON,
    ]),
    GroupSkillItem("Agility Battle", 621, EO1Class.SURVIVALIST, [
        EO1Skills.SURVIVALIST_AGI_UP,
        EO1Skills.SURVIVALIST_TRICKERY,
        EO1Skills.SURVIVALIST_QUICKEN,
        EO1Skills.SURVIVALIST_1ST_HIT,
        EO1Skills.SURVIVALIST_ESCAPE,
        EO1Skills.SURVIVALIST_CLOAK,
        EO1Skills.SURVIVALIST_1ST_TURN
    ]),
    GroupSkillItem("Agility Field", 622, EO1Class.SURVIVALIST, [
        EO1Skills.SURVIVALIST_AGI_UP,
        EO1Skills.SURVIVALIST_AMBUSH,
        EO1Skills.SURVIVALIST_AWARE,
        EO1Skills.SURVIVALIST_STALKER,
        EO1Skills.SURVIVALIST_OWL_EYE
    ]),

    # Protector
    GroupSkillItem("Shield", 630, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_SHIELDS,
        EO1Skills.PROTECTOR_F_GUARD,
        EO1Skills.PROTECTOR_B_GUARD,
        EO1Skills.PROTECTOR_DEFENDER,
    ]),
    GroupSkillItem("DEF Up tree", 631, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_DEF_UP,
        EO1Skills.PROTECTOR_PROVOKE,
        EO1Skills.PROTECTOR_PARRY,
        EO1Skills.PROTECTOR_AEGIS,
        EO1Skills.PROTECTOR_STALKER,
        EO1Skills.PROTECTOR_FLEE
    ]),
    GroupSkillItem("Hybrid tree", 632, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_EN_GARDE,
        EO1Skills.PROTECTOR_FORTIFY,
        EO1Skills.PROTECTOR_SMITE,
    ]),
    GroupSkillItem("Anti-element", 633, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_TP_UP,
        EO1Skills.PROTECTOR_SHIELDS,
        EO1Skills.PROTECTOR_ANTIFIRE,
        EO1Skills.PROTECTOR_ANTICOLD,
        EO1Skills.PROTECTOR_ANTIVOLT
    ]),
    GroupSkillItem("HP Up tree", 634, EO1Class.PROTECTOR, [
        EO1Skills.PROTECTOR_HP_UP,
        EO1Skills.PROTECTOR_CURE,
        EO1Skills.PROTECTOR_CURE_II
    ]),

    # Dark Hunter
    GroupSkillItem("Whip", 640, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_WHIPS,
        EO1Skills.DARK_HUNTER_VIPER,
        EO1Skills.DARK_HUNTER_GAG,
        EO1Skills.DARK_HUNTER_SHACKLES,
        EO1Skills.DARK_HUNTER_CUFFS,
        EO1Skills.DARK_HUNTER_CLIMAX,
        EO1Skills.DARK_HUNTER_ECSTASY
    ]),
    GroupSkillItem("Sword", 641, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_SWORDS,
        EO1Skills.DARK_HUNTER_HYPNOS,
        EO1Skills.DARK_HUNTER_NERVE,
        EO1Skills.DARK_HUNTER_MIRAGE,
        EO1Skills.DARK_HUNTER_DRAIN,
        EO1Skills.DARK_HUNTER_PETRIFY,
        EO1Skills.DARK_HUNTER_BAIT
    ]),
    GroupSkillItem("ATK Up tree", 642, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_ATK_UP,
        EO1Skills.DARK_HUNTER_FURY,
        EO1Skills.DARK_HUNTER_BOOST_UP,
        EO1Skills.DARK_HUNTER_ECSTASY,
        EO1Skills.DARK_HUNTER_BAIT
    ]),
    GroupSkillItem("TP Up tree", 643, EO1Class.DARK_HUNTER, [
        EO1Skills.DARK_HUNTER_TP_UP,
        EO1Skills.DARK_HUNTER_CLOAK
    ]),

    # Medic
    GroupSkillItem("Weak Heal", 650, EO1Class.MEDIC, [
        EO1Skills.MEDIC_HEALER,
        EO1Skills.MEDIC_CURE,
        EO1Skills.MEDIC_SALVE,
        EO1Skills.MEDIC_REGEN,
        EO1Skills.MEDIC_PATCH_UP,
    ]),
    GroupSkillItem("Medium Heal", 651, EO1Class.MEDIC, [
        EO1Skills.MEDIC_HEALER,
        EO1Skills.MEDIC_CURE_II,
        EO1Skills.MEDIC_SALVE_II,
        EO1Skills.MEDIC_H_TOUCH
    ]),
    GroupSkillItem("Strong Heal", 652, EO1Class.MEDIC, [
        EO1Skills.MEDIC_HEALER,
        EO1Skills.MEDIC_CURE_III,
        EO1Skills.MEDIC_REVIVE,
        EO1Skills.MEDIC_CPR,
        EO1Skills.MEDIC_IMMUNIZE
    ]),
    GroupSkillItem("Ailment Heal", 653, EO1Class.MEDIC, [
        EO1Skills.MEDIC_HEALER,
        EO1Skills.MEDIC_UNBIND,
        EO1Skills.MEDIC_REFRESH,
        EO1Skills.MEDIC_PATCH_UP,
    ]),
    GroupSkillItem("TP Up tree", 654, EO1Class.MEDIC, [
        EO1Skills.MEDIC_TP_UP,
        EO1Skills.MEDIC_SCAVENGE,
        EO1Skills.MEDIC_TP_REGEN
    ]),
    GroupSkillItem("ATK Up tree", 655, EO1Class.MEDIC, [
        EO1Skills.MEDIC_ATK_UP,
        EO1Skills.MEDIC_CADUCEUS
    ]),

    # Alchemist
    GroupSkillItem("Fire", 660, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_FIRE_UP,
        EO1Skills.ALCHEMIST_FIRE,
        EO1Skills.ALCHEMIST_FLAME,
        EO1Skills.ALCHEMIST_INFERNO
    ]),
    GroupSkillItem("Ice", 661, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_ICE_UP,
        EO1Skills.ALCHEMIST_ICE,
        EO1Skills.ALCHEMIST_FREEZE,
        EO1Skills.ALCHEMIST_COCYTUS
    ]),
    GroupSkillItem("Volt", 662, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_VOLT_UP,
        EO1Skills.ALCHEMIST_VOLT,
        EO1Skills.ALCHEMIST_THUNDER,
        EO1Skills.ALCHEMIST_THOR
    ]),
    GroupSkillItem("Poison", 663, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_TOXINS,
        EO1Skills.ALCHEMIST_POISON,
        EO1Skills.ALCHEMIST_VENOM
    ]),
    GroupSkillItem("TP Up tree", 664, EO1Class.ALCHEMIST, [
        EO1Skills.ALCHEMIST_TP_UP,
        EO1Skills.ALCHEMIST_SCAVENGE,
        EO1Skills.ALCHEMIST_SIGHT,
        EO1Skills.ALCHEMIST_WARP,
        EO1Skills.ALCHEMIST_TP_REGEN
    ]),

    # Troubadour
    GroupSkillItem("Stat Boost Song", 670, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_SONGS,
        EO1Skills.TROUBADOUR_BRAVERY,
        EO1Skills.TROUBADOUR_SHELTER,
        EO1Skills.TROUBADOUR_MERCURY
    ]),
    GroupSkillItem("Recovery Song", 671, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_SONGS,
        EO1Skills.TROUBADOUR_RECOVERY,
        EO1Skills.TROUBADOUR_DIVINITY,
        EO1Skills.TROUBADOUR_HEALING,
        EO1Skills.TROUBADOUR_RELAXING,
        EO1Skills.TROUBADOUR_STAMINA,
        EO1Skills.TROUBADOUR_ERASURE,
    ]),
    GroupSkillItem("Element", 672, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_SONGS,
        EO1Skills.TROUBADOUR_BLAZE,
        EO1Skills.TROUBADOUR_FROST,
        EO1Skills.TROUBADOUR_SHOCK,
        EO1Skills.TROUBADOUR_IFRIT,
        EO1Skills.TROUBADOUR_YMIR,
        EO1Skills.TROUBADOUR_TARANIS
    ]),
    GroupSkillItem("TP Up tree", 673, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_TP_UP,
        EO1Skills.TROUBADOUR_STALKER,
        EO1Skills.TROUBADOUR_RETURN,
        EO1Skills.TROUBADOUR_RELAXING
    ]),
    GroupSkillItem("HP Up tree", 674, EO1Class.TROUBADOUR, [
        EO1Skills.TROUBADOUR_HP_UP,
        EO1Skills.TROUBADOUR_HEALING,
        EO1Skills.TROUBADOUR_STAMINA
    ]),

    # Ronin
    GroupSkillItem("Overhead Stance", 680, EO1Class.RONIN, [
        EO1Skills.RONIN_KATANAS,
        EO1Skills.RONIN_KESAGIRI,
        EO1Skills.RONIN_OVERHEAD,
        EO1Skills.RONIN_ZAMBA,
        EO1Skills.RONIN_MIDAREBA,
        EO1Skills.RONIN_OROCHI
    ]),
    GroupSkillItem("Seigan Stance", 681, EO1Class.RONIN, [
        EO1Skills.RONIN_KATANAS,
        EO1Skills.RONIN_KESAGIRI,
        EO1Skills.RONIN_SEIGAN,
        EO1Skills.RONIN_MIKIRI,
        EO1Skills.RONIN_KOTEUCHI,
        EO1Skills.RONIN_RAIZUKI
    ]),
    GroupSkillItem("Iai Stance", 682, EO1Class.RONIN, [
        EO1Skills.RONIN_KATANAS,
        EO1Skills.RONIN_KESAGIRI,
        EO1Skills.RONIN_IAI,
        EO1Skills.RONIN_KUBIUCHI,
        EO1Skills.RONIN_GATOTSU,
        EO1Skills.RONIN_HYOSETSU
    ]),
    GroupSkillItem("ATK Up tree", 683, EO1Class.RONIN, [
        EO1Skills.RONIN_ATK_UP,
        EO1Skills.RONIN_SIGHT,
        EO1Skills.RONIN_CRIT_UP
    ]),
    GroupSkillItem("HP Up tree", 684, EO1Class.RONIN, [
        EO1Skills.RONIN_HP_UP,
        EO1Skills.RONIN_IBUKI
    ]),

    # Hexer
    GroupSkillItem("Status Curse", 690, EO1Class.HEXER, [
        EO1Skills.HEXER_CURSES,
        EO1Skills.HEXER_BLINDING,
        EO1Skills.HEXER_TORPOR,
        EO1Skills.HEXER_CORRUPT,
        EO1Skills.HEXER_EVIL_EYE,
        EO1Skills.HEXER_REVENGE,
        EO1Skills.HEXER_STAGGER,
        EO1Skills.HEXER_RELAPSE,
    ]),
    GroupSkillItem("Stat decrease", 691, EO1Class.HEXER, [
        EO1Skills.HEXER_CURSES,
        EO1Skills.HEXER_SAPPING,
        EO1Skills.HEXER_FRAILTY,
        EO1Skills.HEXER_LEADEN
    ]),
    GroupSkillItem("Bind Curse", 692, EO1Class.HEXER, [
        EO1Skills.HEXER_CURSES,
        EO1Skills.HEXER_CRANIAL,
        EO1Skills.HEXER_ABDOMEN,
        EO1Skills.HEXER_IMMOBILE,
        EO1Skills.HEXER_RELAPSE,
    ]),
    GroupSkillItem("Evil Eye tree", 693, EO1Class.HEXER, [
        EO1Skills.HEXER_CURSES,
        EO1Skills.HEXER_EVIL_EYE,
        EO1Skills.HEXER_LURE,
        EO1Skills.HEXER_PARALYZE,
        EO1Skills.HEXER_BETRAYAL,
        EO1Skills.HEXER_SUICIDE
    ])
]

ALL_GROUP_SKILLS: list[GroupSkillItem] = [
    *ALL_STATS_GROUP_SKILLS,
    *ALL_GATHERING_GROUP_SKILLS,
    *ALL_OTHER_GROUP_SKILLS
]


class EO1SkillPools:
    INDIVIDUAL_GENERIC_STATS_INCREASE_SKILLS: set[int] = {
            EO1Skills.LANDSKNECHT_HP_UP,
            EO1Skills.LANDSKNECHT_TP_UP,
            EO1Skills.LANDSKNECHT_ATK_UP,
            EO1Skills.LANDSKNECHT_DEF_UP,
            EO1Skills.SURVIVALIST_HP_UP,
            EO1Skills.SURVIVALIST_TP_UP,
            EO1Skills.SURVIVALIST_AGI_UP,
            EO1Skills.PROTECTOR_HP_UP,
            EO1Skills.PROTECTOR_TP_UP,
            EO1Skills.PROTECTOR_DEF_UP,
            EO1Skills.DARK_HUNTER_HP_UP,
            EO1Skills.DARK_HUNTER_TP_UP,
            EO1Skills.DARK_HUNTER_ATK_UP,
            EO1Skills.MEDIC_HP_UP,
            EO1Skills.MEDIC_TP_UP,
            EO1Skills.MEDIC_ATK_UP,
            EO1Skills.ALCHEMIST_TP_UP,
            EO1Skills.TROUBADOUR_HP_UP,
            EO1Skills.TROUBADOUR_TP_UP,
            EO1Skills.RONIN_HP_UP,
            EO1Skills.RONIN_TP_UP,
            EO1Skills.RONIN_ATK_UP,
            EO1Skills.HEXER_HP_UP,
            EO1Skills.HEXER_TP_UP,
    }
    INDIVIDUAL_MASTERY_SKILLS: set[int] = {
        EO1Skills.LANDSKNECHT_AXES,
        EO1Skills.LANDSKNECHT_SWORDS,
        EO1Skills.SURVIVALIST_BOWS,
        EO1Skills.PROTECTOR_SHIELDS,
        EO1Skills.DARK_HUNTER_WHIPS,
        EO1Skills.DARK_HUNTER_SWORDS,
        EO1Skills.RONIN_KATANAS,
        EO1Skills.MEDIC_HEALER,
        EO1Skills.ALCHEMIST_FIRE_UP,
        EO1Skills.ALCHEMIST_ICE_UP,
        EO1Skills.ALCHEMIST_VOLT_UP,
        EO1Skills.ALCHEMIST_TOXINS,
        EO1Skills.TROUBADOUR_SONGS,
        EO1Skills.HEXER_CURSES
    }
    INDIVIDUAL_GATHERING_SKILLS: set[int] = {
        EO1Skills.LANDSKNECHT_MINE,
        EO1Skills.SURVIVALIST_CHOP,
        EO1Skills.SURVIVALIST_MINE,
        EO1Skills.SURVIVALIST_TAKE,
        EO1Skills.PROTECTOR_MINE,
        EO1Skills.DARK_HUNTER_TAKE,
        EO1Skills.MEDIC_CHOP,
        EO1Skills.ALCHEMIST_CHOP,
        EO1Skills.TROUBADOUR_TAKE,
        EO1Skills.RONIN_MINE,
        EO1Skills.HEXER_MINE,
    }
    INDIVIDUAL_ALL_SKILLS: set[int] = {skill_id for skill_id in SKILL_DATA_BY_ID.keys()}
    INDIVIDUAL_ALL_OTHER_SKILLS: set[int] = (
            INDIVIDUAL_ALL_SKILLS
            - INDIVIDUAL_GENERIC_STATS_INCREASE_SKILLS
            - INDIVIDUAL_MASTERY_SKILLS
            - INDIVIDUAL_GATHERING_SKILLS
    )

def make_skill_item_from_skill_data(skill_data: EO1SkillData) -> SkillItem:
    return SkillItem(skill_data.ap_item_id, skill_data.get_full_name(), SkillItemType.INDIVIDUAL)
def make_skill_item_from_skill_id(skill_id: int) -> SkillItem:
    skill_data = SKILL_DATA_BY_ID[skill_id]
    return make_skill_item_from_skill_data(skill_data)
def make_skill_items_from_skill_list(skill_list: set[int]) -> list[SkillItem]:
    return [make_skill_item_from_skill_id(skill_id) for skill_id in skill_list]

class SkillUnlockItems:
    ALL_SKILLS = SkillItem(750, "All Skills", SkillItemType.ALL)
    ALL_STATS_SKILLS = MultiClassGroupSkillItem("All Stats Up Skills", 751, [
        group_skill.to_skill_item()
        for group_skill in ALL_STATS_GROUP_SKILLS
    ])
    ALL_MASTERY_SKILLS = MultiClassGroupSkillItem("All Mastery Skills", 752,
                                                  make_skill_items_from_skill_list(EO1SkillPools.INDIVIDUAL_MASTERY_SKILLS))
    ALL_GATHERING_SKILLS = MultiClassGroupSkillItem("All Gathering Skills", 753, [
        group_skill.to_skill_item()
        for group_skill in ALL_GATHERING_GROUP_SKILLS
    ])


ALL_MULTI_CLASS_GROUP_ITEMS: list[MultiClassGroupSkillItem] = [
    SkillUnlockItems.ALL_STATS_SKILLS,
    SkillUnlockItems.ALL_MASTERY_SKILLS,
    SkillUnlockItems.ALL_GATHERING_SKILLS,
]

ALL_SKILLS_ITEMS: list[SkillItem] = [
    *[make_skill_item_from_skill_data(skill_data) for skill_data in ALL_SKILLS_DATA],
    *[skill_group.to_skill_item() for skill_group in ALL_GROUP_SKILLS],
    *[multi_class_group.to_skill_item() for multi_class_group in ALL_MULTI_CLASS_GROUP_ITEMS],
    SkillUnlockItems.ALL_SKILLS,
]

GROUP_SKILL_ITEM_BY_ITEM_ID: dict[int, GroupSkillItem] = {skill_group.ap_item_id:skill_group for skill_group in ALL_GROUP_SKILLS}

MULTI_CLASS_GROUP_BY_ITEM_ID: dict[int, MultiClassGroupSkillItem] = {multi_class_group.ap_item_id:multi_class_group for multi_class_group in ALL_MULTI_CLASS_GROUP_ITEMS}

SKILL_ITEM_TYPE_BY_AP_ITEM_ID: dict[int, SkillItem] = {skill_item.ap_item_id:skill_item for skill_item in ALL_SKILLS_ITEMS}

def build_skill_unlock_dictionary() -> dict[int, list[SkillUnlockData]]:
    skill_unlock_dictionary: dict[int, list[SkillUnlockData]] = {}

    # Initialize the list of skills.
    for skill in ALL_SKILLS_DATA:
        skill_unlock_dictionary[skill.id] = []

    for skill_item in ALL_SKILLS_ITEMS:
        if skill_item.skill_item_type == SkillItemType.ALL:
            for skill_id in skill_unlock_dictionary.keys():
                skill_unlock_dictionary[skill_id].append(
                    SkillUnlockData(skill_item.ap_item_id, skill_item.ap_item_name, item_count_requirement=1)
                )
        elif skill_item.skill_item_type == SkillItemType.INDIVIDUAL:
            skill_data = SKILL_DATA_BY_ITEM_ID[skill_item.ap_item_id]
            skill_unlock_dictionary[skill_data.id].append(
                SkillUnlockData(skill_item.ap_item_id, skill_item.ap_item_name, item_count_requirement=1)
            )
        elif skill_item.skill_item_type == SkillItemType.GROUP:
            group_skill_item = GROUP_SKILL_ITEM_BY_ITEM_ID[skill_item.ap_item_id]
            for skill_id in group_skill_item.skills:
                skill_unlock_dictionary[skill_id].append(
                    SkillUnlockData(skill_item.ap_item_id, skill_item.ap_item_name, item_count_requirement=1)
                )
        elif skill_item.skill_item_type == SkillItemType.PROGRESSIVE:
            raise NotImplementedError()
        elif skill_item.skill_item_type == SkillItemType.MULTI_CLASS_GROUP:
            multi_class_group = MULTI_CLASS_GROUP_BY_ITEM_ID[skill_item.ap_item_id]
            for inner_skill_item in multi_class_group.skill_items:
                if inner_skill_item.skill_item_type == SkillItemType.INDIVIDUAL:
                    skill_data = SKILL_DATA_BY_ITEM_ID[inner_skill_item.ap_item_id]
                    skill_unlock_dictionary[skill_data.id].append(
                        SkillUnlockData(skill_item.ap_item_id, skill_item.ap_item_name, item_count_requirement=1)
                    )
                elif inner_skill_item.skill_item_type == SkillItemType.GROUP:
                    group_skill_item = GROUP_SKILL_ITEM_BY_ITEM_ID[inner_skill_item.ap_item_id]
                    for skill_id in group_skill_item.skills:
                        skill_unlock_dictionary[skill_id].append(
                            SkillUnlockData(skill_item.ap_item_id, skill_item.ap_item_name, item_count_requirement=1)
                        )
                else:
                    raise Exception(f"Skill Item Type {inner_skill_item.skill_item_type} is not a valid multi class group sub item.")
        else:
            raise Exception(f"Unknown skill item type {skill_item.skill_item_type}")

    return skill_unlock_dictionary

SKILL_UNLOCK_DATA_BY_SKILL_ID: dict[int, list[SkillUnlockData]] = build_skill_unlock_dictionary()

def get_class_name_for_skill_item(skill_item: SkillItem) -> str:
    if skill_item.skill_item_type == SkillItemType.ALL:
        raise Exception("SkillItemType of ALL is invalid for this function.")
    elif skill_item.skill_item_type == SkillItemType.MULTI_CLASS_GROUP:
        raise Exception("SkillItemType of MULTI_CLASS_GROUP is invalid for this function.")

    class_name: str = ""
    if skill_item.skill_item_type == SkillItemType.INDIVIDUAL:
        class_name = SKILL_DATA_BY_ITEM_ID[skill_item.ap_item_id].class_name
    elif skill_item.skill_item_type == SkillItemType.GROUP:
        class_name = GROUP_SKILL_ITEM_BY_ITEM_ID[skill_item.ap_item_id].class_name
    else:
        raise Exception(f"Unknown skill item type {skill_item.skill_item_type}")

    return class_name

def __get_class_index_for_skill_item(skill_item: SkillItem) -> int:
    class_name = get_class_name_for_skill_item(skill_item)
    return CLASS_DATA_BY_NAME[class_name].class_id

def __apply_skill_unlock_value(skill_data: EO1SkillData, skill_unlock_value: int) -> int:
    return skill_unlock_value | (1 << skill_data.skill_index)

def __get_new_skill_unlock_value(skill_item: SkillItem, skill_unlock_value: int, all_current_skill_items: list[SkillItem]) -> int:
    if skill_item.skill_item_type == SkillItemType.ALL:
        raise Exception("SkillItemType of ALL is invalid for this function.")
    elif skill_item.skill_item_type == SkillItemType.MULTI_CLASS_GROUP:
        raise Exception("SkillItemType of MULTI_CLASS_GROUP is invalid for this function.")

    if skill_item.skill_item_type == SkillItemType.INDIVIDUAL:
        skill_data = SKILL_DATA_BY_ITEM_ID[skill_item.ap_item_id]
        return __apply_skill_unlock_value(skill_data, skill_unlock_value)
    elif skill_item.skill_item_type == SkillItemType.GROUP:
        group_skill_item = GROUP_SKILL_ITEM_BY_ITEM_ID[skill_item.ap_item_id]

        for skill in group_skill_item.skills:
            skill_data = SKILL_DATA_BY_ID[skill]
            skill_unlock_value = __apply_skill_unlock_value(skill_data, skill_unlock_value)

        return skill_unlock_value
    else:
        raise Exception(f"Unknown skill item type {skill_item.skill_item_type}")

def __get_all_skill_unlock_value() -> int:
    result = 0
    for index in range(21):
        result |= 1 << index
    return result

# Used by the client.
def apply_skill_item_to_values(skill_item: SkillItem, skill_unlock_values: list[int], all_current_skill_items: list[SkillItem]) -> list[int]:
    for index in range(9):
        if skill_item.skill_item_type == SkillItemType.ALL:
            skill_unlock_values[index] = __get_all_skill_unlock_value()
            continue
        elif skill_item.skill_item_type == SkillItemType.MULTI_CLASS_GROUP:
            multi_class_group = MULTI_CLASS_GROUP_BY_ITEM_ID[skill_item.ap_item_id]
            for skill in multi_class_group.skill_items:
                class_index = __get_class_index_for_skill_item(skill)
                if class_index != index:
                    continue
                skill_unlock_value = skill_unlock_values[index]
                skill_unlock_values[index] = __get_new_skill_unlock_value(skill, skill_unlock_value, all_current_skill_items)
            continue

        class_index = __get_class_index_for_skill_item(skill_item)
        if class_index != index:
            continue
        skill_unlock_value = skill_unlock_values[index]
        skill_unlock_values[index] = __get_new_skill_unlock_value(skill_item, skill_unlock_value, all_current_skill_items)

    return skill_unlock_values







'''
LANDSKNECHT = "Landsknecht"
SURVIVALIST = "Survivalist"
PROTECTOR = "Protector"
DARK_HUNTER = "Dark Hunter"
RONIN = "Ronin"
MEDIC = "Medic"
ALCHEMIST = "Alchemist"
TROUBADOUR = "Troubadour"
HEXER = "Hexer"

class EO1SkillUnlock:
    LANDSKNECHT_SKILL_ALL = 2
    SURVIVALIST_SKILL_ALL = 2
    PROTECTOR_SKILL_ALL = "Protector"
    DARK_HUNTER_SKILL_ALL = "Dark Hunter"
    RONIN_SKILL_ALL = "Ronin"
    MEDIC_SKILL_ALL = "Medic"
    ALCHEMIST_SKILL_ALL = "Alchemist"
    TROUBADOUR_SKILL_ALL = "Troubadour"
    HEXER_SKILL_ALL = "Hexer"
LANDSKNECHT_STATS_BOOST_TREE = 1
LANDSKNECHT_GATHERING_TREE = 1
LANDSKNECHT_SWORD_TREE = 1
LANDSKNECHT_AXE_TREE = 1
LANDSKNECHT_CHASE_TREE = 1
LANDSKNECHT_MISC_TREE = 1

SURVIVALIST_STATS_BOOST_TREE = 1
SURVIVALIST_GATHERING_TREE = 1
SURVIVALIST_BOW_TREE = 1
SURVIVALIST_AGILITY_TREE = 1
SURVIVALIST_FIELD_TREE = 1

PROTECTOR_STATS_BOOST_TREE = 1
PROTECTOR_GATHERING_TREE = 1
PROTECTOR_SHIELD_TREE = 1
PROTECTOR_HEAL_TREE = 1
PROTECTOR_MISC_TREE = 1
PROTECTOR_ANTI_TREE = 1

DARK_HUNTER_STATS_BOOST_TREE = 1
DARK_HUNTER_GATHERING_TREE = 1
DARK_HUNTER_WHIP_TREE = 1
DARK_HUNTER_SWORD_TREE = 1
DARK_HUNTER_MISC_TREE = 1


MEDIC_STATS_BOOST_TREE = 1
MEDIC_GATHERING_TREE = 1
MEDIC_HEALER_TREE = 1
MEDIC_AILMENT_TREE = 1
MEDIC_MISC_TREE = 1

ALCHEMIST_STATS_BOOST_TREE = 1
ALCHEMIST_GATHERING_TREE = 1
ALCHEMIST_FIRE_TREE = 1
ALCHEMIST_ICE_TREE = 1
ALCHEMIST_VOLT_TREE = 1
ALCHEMIST_POISON_TREE = 1
ALCHEMIST_MISC_TREE = 1

TROUBADOUR_STATS_BOOST_TREE = 1
TROUBADOUR_GATHERING_TREE = 1
TROUBADOUR_SONG_TREE = 1
TROUBADOUR_ELEMENT_TREE = 1
TROUBADOUR_MISC_TREE = 1

RONIN_STATS_BOOST_TREE = 1
RONIN_GATHERING_TREE = 1
RONIN_OVERHEAD_TREE = 1
RONIN_IAI_TREE = 1
RONIN_SEIGAN_TREE = 1
RONIN_MISC_TREE = 1

HEXER_STATS_BOOST_TREE = 1
HEXER_GATHERING_TREE = 1
HEXER_CURSE_TREE = 1

HEXER_HP_UP = 0xA9
HEXER_TP_UP = 0xAA
HEXER_MINE = 0xAD

HEXER_CURSES = 0xAB
HEXER_BLINDING = 0xB5
HEXER_TORPOR = 0xB6
HEXER_CORRUPT = 0xB7
HEXER_EVIL_EYE = 0xB8

HEXER_LURE = 0xBD
HEXER_STAGGER = 0xAC
HEXER_RELAPSE = 0xB1
HEXER_REVENGE = 0xBC

HEXER_SAPPING = 0xAE
HEXER_FRAILTY = 0xAF
HEXER_LEADEN = 0xB0

HEXER_CRANIAL = 0xB2
HEXER_ABDOMEN = 0xB3
HEXER_IMMOBILE = 0xB4

HEXER_SUICIDE = 0xB9
HEXER_BETRAYAL = 0xBA
HEXER_PARALYZE = 0xBB
'''