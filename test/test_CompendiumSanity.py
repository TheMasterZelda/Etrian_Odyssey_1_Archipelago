from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *


BASE_OPTIONS = {
    **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
    **OptionSets.NO_LEVEL_SHUFFLING,
    **OptionSets.NO_FLOOR_SHUFFLING,
    **OptionSets.NO_CLASS_SHUFFLING,
    **OptionSets.NO_SKILL_SHUFFLING,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}


class CompendiumSanityMinimalTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.CODEX_SANITY: False,
        OptionKeys.COMPENDIUM_SANITY: True,
        OptionKeys.COMPENDIUM_SANITY_INCLUDE_CONDITIONAL_DROPS: False,
    }

class CompendiumSanityFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.CODEX_SANITY: False,
        OptionKeys.COMPENDIUM_SANITY: True,
        OptionKeys.COMPENDIUM_SANITY_INCLUDE_CONDITIONAL_DROPS: True,
    }