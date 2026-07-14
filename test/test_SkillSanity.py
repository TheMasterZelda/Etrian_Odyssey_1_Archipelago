from .Bases import EtrianOdysseyTestBase
from .Constant import *
from ..Constant import *
from ..Options import *


BASE_OPTIONS = {
    **OptionSets.DEFAULT_NO_BATTLE_LOGIC,
    **OptionSets.NO_LEVEL_SHUFFLING,
    **OptionSets.NO_FLOOR_SHUFFLING,
    **OptionSets.NO_CLASS_SHUFFLING,
    **OptionSets.ENABLE_ALL_OPTIONAL_LOGIC_OPTIONS,
}


class SkillSanityIndividualShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.ENABLE_ALL_LOCATIONS, # Individual Shuffling need more locations.

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: False,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: False,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: False,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 0,
    }

class SkillSanityIndividualShuffleWithStartingItemTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.ENABLE_ALL_LOCATIONS, # Individual Shuffling need more locations.

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: False,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: False,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: False,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 10,
    }

class SkillSanityAllIndividualShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.ENABLE_ALL_LOCATIONS,  # Individual Shuffling need more locations.

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 0,
    }

class SkillSanityAllIndividualShuffleWithStartingItemTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.ENABLE_ALL_LOCATIONS,  # Individual Shuffling need more locations.

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 15,
    }

class SkillSanityGroupShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: False,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: False,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: False,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 0,
    }

class SkillSanityGroupShuffleWithStartingItemTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: False,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: False,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: False,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 10,
    }

class SkillSanityAllGroupShuffleTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.DISABLE_ALL_OPTIONAL_LOCATIONS,

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_group.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,
        OptionKeys.STARTING_SKILL_ITEM_COUNT: 0,
    }

class SkillSanityNoSkillsRequirementsTest(EtrianOdysseyTestBase):
    options = {
        OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
        **BASE_OPTIONS,
        **OptionSets.ENABLE_ALL_LOCATIONS,  # Individual Shuffling need more locations.

        # Skills
        OptionKeys.SKILL_SANITY_MODE: SkillSanityType.shuffle_individually.value,
        OptionKeys.SKILL_REQUIREMENT_SHUFFLE: SkillRequirementShuffleType.remove.value,
        OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: True,
        OptionKeys.SHUFFLE_MASTERY_SKILLS: True,
        OptionKeys.SHUFFLE_GATHERING_SKILLS: True,
    }