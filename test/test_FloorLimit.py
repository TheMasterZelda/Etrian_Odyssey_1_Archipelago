from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *

# Test the various floor limit settings.

BASE_OPTIONS = {
    **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
    **OptionSets.NO_LEVEL_SHUFFLING,
    **OptionSets.NO_CLASS_SHUFFLING,
    **OptionSets.NO_SKILL_SHUFFLING,
    **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}

class FloorLimitFixedIncreaseTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Floor Limits
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
        OptionKeys.INITIAL_FLOOR_LIMIT: 1,
        OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
        OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 0,
    }

class FloorLimitExtraItemsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Floor Limits
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
        OptionKeys.INITIAL_FLOOR_LIMIT: 1,
        OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
        OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 5,
    }

class FloorLimitCompleteShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Floor Limits
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_complete_shuffle,
        OptionKeys.INITIAL_FLOOR_LIMIT: 1,
        OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 5,
    }

class FloorLimitStratum1GoalTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,

        # Floor Limits
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
        OptionKeys.INITIAL_FLOOR_LIMIT: 1,
        OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
        OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 0,
    }

class FloorLimitAllLocationsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
        **OptionSets.NO_LEVEL_SHUFFLING,
        **OptionSets.NO_CLASS_SHUFFLING,
        **OptionSets.NO_SKILL_SHUFFLING,
        **OptionSets.ENABLE_ALL_LOCATIONS,

        # Floor Limits
        OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
        OptionKeys.INITIAL_FLOOR_LIMIT: 1,
        OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
        OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 0,
    }