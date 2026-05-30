from BaseClasses import Item, ItemClassification, Location, Region
from enum import IntEnum, Enum

GAME_NAME = "Etrian Odyssey"
GAME_VERSION = "0.1.0"
MAX_LEVEL = 70
MAX_FLOOR = 30

#class BattleLogicModeType(IntEnum):
#    generous = 1
#    standard = 2
#    restrictive = 3
#    level_only = 4
#    no_logic = 5

class BattleLogicModeType(IntEnum):
    simplified = 3
    level_only = 4
    no_logic = 5

class BattleLogicDifficultyType(IntEnum):
    picnic = 1
    normal = 2
    expert = 3

class EO1Goal(IntEnum):
    defeat_fenrir = 1
    defeat_cernunos = 2
    defeat_cotrangl = 3
    annihilate_the_forest_folk = 4
    defeat_etreant = 5
    defeat_primevil = 6

class ClassSanityType(IntEnum):
    vanilla = 0
    start_with_all = 1
    shuffle_availability = 2

class SkillSanityType(IntEnum):
    none = 0
    shuffle_individually = 1
    shuffle_group = 2

class ItemGroupNames:
    MONEY = "Money"
    PROGRESSIVE_LEVEL_CAP = "Progression Level Cap"
    PROGRESSIVE_FLOOR_LIMIT = "Progression Floor Limit"
    CLASS = "Class"
    SKILL = "Skill"
    KEY_ITEM = "Key Item"
    CONSUMABLE = "Consumable"
    QUEST_ITEM = "Quest Item"
    # Consider splitting this into different groups.
    EQUIPMENT = "Equipment"
    EVENT = "Event"

def get_max_floor_for_goal(goal: EO1Goal) -> int:
    if goal == EO1Goal.defeat_fenrir:
        return 5
    elif goal == EO1Goal.defeat_cernunos:
        return 10
    elif goal == EO1Goal.defeat_cotrangl:
        return 15
    elif goal == EO1Goal.annihilate_the_forest_folk:
        return 20
    elif goal == EO1Goal.defeat_etreant:
        return 25
    elif goal == EO1Goal.defeat_primevil:
        return MAX_FLOOR
    else:
        raise Exception(f"Goal {goal} not implemented")

def get_max_level_for_goal(goal: EO1Goal) -> int:
    if goal == EO1Goal.defeat_fenrir:
        return 30
    elif goal == EO1Goal.defeat_cernunos:
        return 40
    elif goal == EO1Goal.defeat_cotrangl:
        return 50
    elif goal == EO1Goal.annihilate_the_forest_folk:
        return 60
    elif goal == EO1Goal.defeat_etreant:
        return MAX_LEVEL
    elif goal == EO1Goal.defeat_primevil:
        return MAX_LEVEL
    else:
        raise Exception(f"Goal {goal} not implemented")

def get_max_stratum_for_goal(goal: EO1Goal) -> int:
    if goal == EO1Goal.defeat_fenrir:
        return 1
    elif goal == EO1Goal.defeat_cernunos:
        return 2
    elif goal == EO1Goal.defeat_cotrangl:
        return 3
    elif goal == EO1Goal.annihilate_the_forest_folk:
        return 4
    elif goal == EO1Goal.defeat_etreant:
        return 5
    elif goal == EO1Goal.defeat_primevil:
        return 6
    else:
        raise Exception(f"Goal {goal} not implemented")

class SlotDataKeys:
    GOAL = "goal"
    QUEST_SANITY = "quest_sanity"
    QUEST_COMPLETION_REWARD_HINT = "quest_completion_reward_hint"
#    PROGRESSIVE_LEVEL_CAP_VALUE = "level_cap_increase_value"
#    PROGRESSIVE_FLOOR_LIMIT_VALUE = "floor_limit_increase_value"

