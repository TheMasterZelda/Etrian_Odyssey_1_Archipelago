from ..Constant import *
from ..Options import *

class OptionKeys:
    GOAL = "goal"
    #experience_modifier: ExperienceModifier irrelevant to the generation
    BATTLE_LOGIC_MODE = "battle_logic_mode"
    BATTLE_LOGIC_DIFFICULTY = "battle_logic_difficulty"
    SUSTAIN_LOGIC_ENABLED = "sustain_logic_enabled"
    LEVEL_CAP_MODE = "level_cap_mode"
    INITIAL_LEVEL_CAP = "initial_level_cap"
    LEVEL_CAP_INCREASE_VALUE = "level_cap_increase_value"
    EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS = "extra_progressive_level_cap_items"
    FLOOR_LIMIT_MODE = "floor_limit_mode"
    INITIAL_FLOOR_LIMIT = "initial_floor_limit"
    FLOOR_LIMIT_INCREASE_VALUE = "floor_limit_increase_value"
    EXTRA_PROGRESSIVE_FLOOR_LIMIT = "extra_progressive_floor_limit"
    CLASS_SANITY_MODE = "class_sanity_mode"
    STARTING_CLASS_COUNT = "starting_class_count"
    SKILL_SANITY_MODE = "skill_sanity_mode"
    SHUFFLE_GENERIC_STATS_INCREASE_SKILLS = "shuffle_generic_stats_increase_skills"
    SHUFFLE_MASTERY_SKILLS = "shuffle_mastery_skills"
    SHUFFLE_GATHERING_SKILLS = "shuffle_gathering_skills"
    REMOVE_SKILLS_REQUIREMENTS = "remove_skills_requirements"
    STARTING_SKILL_ITEM_COUNT = "starting_class_item_count"
    CODEX_SANITY = "codex_sanity"
    COMPENDIUM_SANITY = "compendium_sanity"
    COMPENDIUM_SANITY_INCLUDE_CONDITIONAL_DROPS = "compendium_sanity_include_conditional_drops"
    #shop_unlock_material_cost_divider: ShopUnlockMaterialCostDivider irrelevant to the generation

class OptionSets:
    DEFAULT_NO_BATTLE_LOGIC = {
        OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.no_logic.value,
        OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,
    }
    ENABLE_ALL_LOCATIONS = {
        OptionKeys.CODEX_SANITY: True,
        OptionKeys.COMPENDIUM_SANITY: True,
        OptionKeys.COMPENDIUM_SANITY_INCLUDE_CONDITIONAL_DROPS: True,
    }
    DISABLE_ALL_OPTIONAL_LOCATIONS = {
        OptionKeys.CODEX_SANITY: False,
        OptionKeys.COMPENDIUM_SANITY: False,
        OptionKeys.COMPENDIUM_SANITY_INCLUDE_CONDITIONAL_DROPS: False,
    }
    NO_LEVEL_SHUFFLING = {
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_none,
    }
    NO_FLOOR_SHUFFLING = {
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_none,
    }
    NO_SKILL_SHUFFLING = {
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.none.value,
    }
    NO_CLASS_SHUFFLING = {
        OptionKeys.CLASS_SANITY_MODE: ClassSanityType.start_with_all.value,
    }
    ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS = {
        OptionKeys.SUSTAIN_LOGIC_ENABLED: True
    }

class APGenSteps:
    GENERATE_EARLY = "generate_early"
    CREATE_REGIONS = "create_regions"
    CREATE_ITEMS = "create_items"
    SET_RULES = "set_rules"
    CONNECT_ENTRANCES = "connect_entrances"
    GENERATE_BASIC = "generate_basic"
    PRE_FILL = "pre_fill"
