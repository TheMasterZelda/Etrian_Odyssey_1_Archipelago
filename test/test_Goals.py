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
    **OptionSets.ENABLE_ALL_LOCATIONS
}


class DefeatFenrirTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,
    }

class DefeatCernunosTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cernunos.value,
        **BASE_OPTIONS,
    }

class DefeatCotranglTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cotrangl.value,
        **BASE_OPTIONS,
    }

#class AnnihilateTheForestFolkTest(EtrianOdysseyTestBase):
#    options = {
#        OptionKeys.GOAL: EO1Goal.annihilate_the_forest_folk.value,
#        **BASE_OPTIONS,
#    }

class DefeatEtreantTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
    }

#class DefeatPrimevilTest(EtrianOdysseyTestBase):
#    options = {
#        OptionKeys.GOAL: EO1Goal.defeat_primevil.value,
#        **BASE_OPTIONS,
#    }