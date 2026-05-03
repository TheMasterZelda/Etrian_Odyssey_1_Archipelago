from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *


BASE_OPTIONS = {
    **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
    **OptionSets.NO_LEVEL_SHUFFLING,
    **OptionSets.NO_FLOOR_SHUFFLING,
    **OptionSets.NO_SKILL_SHUFFLING,
    **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}


class ClassSanityVanillaTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Class
        OptionKeys.CLASS_SANITY_MODE: ClassSanityType.vanilla.value,
        OptionKeys.STARTING_CLASS_COUNT: 1,
    }

class ClassSanityFullShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        # Class
        OptionKeys.CLASS_SANITY_MODE: ClassSanityType.shuffle_availability.value,
        OptionKeys.STARTING_CLASS_COUNT: 1,
    }
