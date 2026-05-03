from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *


BASE_OPTIONS = {
    **OptionSets.NO_FLOOR_SHUFFLING,
    **OptionSets.NO_CLASS_SHUFFLING,
    **OptionSets.NO_SKILL_SHUFFLING,
    **OptionSets.ENABLE_ALL_LOCATIONS,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}

LEVEL_CAP_OPTIONS = {
    OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
    OptionKeys.INITIAL_LEVEL_CAP: 5,
    OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
    OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,
}


class BattleLogicModeLevelOnlyTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.NO_CLASS_SHUFFLING,
        **OptionSets.NO_SKILL_SHUFFLING,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.LEVEL_CAP_INCREASE_VALUE: 1,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,

        # Battle Logic
        OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.level_only.value,
        OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,
    }


class BattleLogicModeSimplifiedClassShufflingTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **LEVEL_CAP_OPTIONS,
        **OptionSets.NO_SKILL_SHUFFLING,

        # Class
        OptionKeys.CLASS_SANITY_MODE: ClassSanityType.shuffle_availability.value,
        OptionKeys.STARTING_CLASS_COUNT: 1,

        # Battle Logic
        OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.simplified.value,
        OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,
    }


class BattleLogicModeSimplifiedSkillShufflingTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **LEVEL_CAP_OPTIONS,
        **OptionSets.NO_CLASS_SHUFFLING,

        # Skill
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,

        # Battle Logic
        OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.simplified.value,
        OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,
    }


class BattleLogicModeSimplifiedSkillShufflingNoSkillsRequirementsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **LEVEL_CAP_OPTIONS,
        **OptionSets.NO_CLASS_SHUFFLING,

        # Skill
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.REMOVE_SKILLS_REQUIREMENTS: True,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,

        # Battle Logic
        OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.simplified.value,
        OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,
    }