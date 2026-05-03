from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *

# Test the various level cap settings.

BASE_OPTIONS = {
    **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
    **OptionSets.NO_FLOOR_SHUFFLING,
    **OptionSets.NO_CLASS_SHUFFLING,
    **OptionSets.NO_SKILL_SHUFFLING,
    **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}

class LevelCapFixedIncreaseTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,
    }

class LevelCapExtraItemsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 5,
    }

class LevelCapCompleteShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_complete_shuffle,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 5,
    }

class LevelCapStratum1GoalTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,
    }

class LevelCapAllLocationsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
        **OptionSets.NO_FLOOR_SHUFFLING,
        **OptionSets.NO_CLASS_SHUFFLING,
        **OptionSets.NO_SKILL_SHUFFLING,
        **OptionSets.ENABLE_ALL_LOCATIONS,

        # Level Caps
        OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
        OptionKeys.INITIAL_LEVEL_CAP: 5,
        OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
        OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,
    }