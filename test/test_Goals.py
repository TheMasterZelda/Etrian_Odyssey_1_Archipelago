from .Bases import EtrianOdysseyTestBase
from .Constant import *
from .Constant import OptionKeys
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

FULL_OPTIONS = {
    OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.simplified.value,
    OptionKeys.CLASS_SANITY_MODE: ClassSanityType.shuffle_availability.value,
    OptionKeys.STARTING_CLASS_COUNT: 4,
    OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
    OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
    OptionKeys.INITIAL_LEVEL_CAP: 10,
    OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
    OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
    OptionKeys.INITIAL_FLOOR_LIMIT: 1,
    OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
    **OptionSets.ENABLE_ALL_LOCATIONS
}

class DefeatFenrirTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,
    }

class DefeatFenrirFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **FULL_OPTIONS,
    }

class DefeatCernunosTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cernunos.value,
        **BASE_OPTIONS,
    }

class DefeatCernunosFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cernunos.value,
        **FULL_OPTIONS,
    }

class DefeatCotranglTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cotrangl.value,
        **BASE_OPTIONS,
    }

class DefeatCotranglFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cotrangl.value,
        **FULL_OPTIONS,
    }

class AnnihilateTheForestFolkTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.annihilate_the_forest_folk.value,
        **BASE_OPTIONS,
    }

class AnnihilateTheForestFolkFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.annihilate_the_forest_folk.value,
        **FULL_OPTIONS,
    }

class DefeatEtreantTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
    }

class DefeatEtreantFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **FULL_OPTIONS,
    }

class DefeatPrimevilTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_primevil.value,
        **BASE_OPTIONS,
    }

class DefeatPrimevilFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_primevil.value,
        **FULL_OPTIONS,
    }