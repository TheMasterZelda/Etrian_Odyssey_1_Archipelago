from .Bases import EtrianOdysseyTestBase
from .Constant import *
from .Constant import OptionKeys
from ..Constant import *
from ..Options import *


BASE_OPTIONS = {
    OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.simplified.value,
    OptionKeys.CLASS_SANITY_MODE: ClassSanityType.shuffle_availability.value,
    OptionKeys.STARTING_CLASS_COUNT: 4,
    OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_fixed_increase,
    OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
    OptionKeys.INITIAL_LEVEL_CAP: 10,
    OptionKeys.FLOOR_LIMIT_MODE: FloorLimitMode.option_fixed_increase,
    OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
    OptionKeys.INITIAL_FLOOR_LIMIT: 1,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
    **OptionSets.ENABLE_ALL_LOCATIONS
}

class SkillRequirementShuffleRemoveTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.remove.value,
    }

class SkillRequirementShuffleNonRootMasteryTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.non_root_shuffle_with_mastery_retention.value,
    }

class SkillRequirementShuffleNonRootTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.non_root_shuffle.value,
    }

class SkillRequirementShuffleFullMasteryTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.full_shuffle_with_mastery_retention.value,
    }

class SkillRequirementShuffleFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.full_shuffle.value,
    }

class SkillRequirementShuffleChaosTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class SkillRequirementShuffleDefeatFenrirTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_fenrir.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class DefeatCernunosTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cernunos.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class SkillRequirementShuffleDefeatCotranglTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_cotrangl.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class SkillRequirementShuffleAnnihilateTheForestFolkTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.annihilate_the_forest_folk.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class SkillRequirementShuffleDefeatEtreantTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class SkillRequirementShuffleDefeatPrimevilTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_primevil.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }

class FullyCompleteCodexAndCompendiumFullTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.fully_complete_codex_and_compendium.value,
        **BASE_OPTIONS,

        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.chaos.value,
    }