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
    **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,

    OptionKeys.QUEST_SANITY: True,
    OptionKeys.QUEST_COMPLETION_REWARD_HINT: True,
}


class QuestSanityFenrirTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,
    }

class QuestSanityCernunosTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cernunos.value,
        **BASE_OPTIONS,
    }

class QuestSanityCotranglTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cotrangl.value,
        **BASE_OPTIONS,
    }

class QuestSanityForestFolkTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.annihilate_the_forest_folk.value,
        **BASE_OPTIONS,
    }

class QuestSanityEtreantTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
    }

#class QuestSanityPrimevilTest(EtrianOdysseyTestBase):
#    options = {
#        OptionKeys.GOAL: EO1Goal.defeat_primevil.value,
#        **BASE_OPTIONS,
#
#        OptionKeys.QUEST_SANITY: True,
#    }