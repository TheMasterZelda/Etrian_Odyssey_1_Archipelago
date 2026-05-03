from dataclasses import dataclass
from .Constant import *
from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions
#, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
#    ItemDict, ItemsAccessibility, ItemSet, Visibility

class EtrianOdysseyGoal(Choice):
    display_name = "Goal"
    option_defeat_fenrir = EO1Goal.defeat_fenrir.value
    option_defeat_cernunos = EO1Goal.defeat_cernunos.value
    option_defeat_cotrangl = EO1Goal.defeat_cotrangl.value
    #option_annihilate_the_forest_folk = EO1Goal.annihilate_the_forest_folk.value
    option_defeat_etreant  = EO1Goal.defeat_etreant.value
    #option_defeat_primevil = EO1Goal.defeat_primevil.value
    default = EO1Goal.defeat_etreant.value

class ExperienceModifier(Range):
    display_name = "Experience Modifier"
    range_start = 50
    range_end = 1000
    default = 500

class BattleLogicMode(Choice):
    display_name = "Battle Logic Mode"
    #option_generous = BattleLogicModeType.generous.value
    #option_standard = BattleLogicModeType.standard.value
    #option_restrictive = BattleLogicModeType.restrictive.value
    option_simplified = BattleLogicModeType.simplified.value
    option_level_only = BattleLogicModeType.level_only.value
    option_no_logic = BattleLogicModeType.no_logic.value
    default = BattleLogicModeType.level_only.value

class BattleLogicDifficulty(Choice):
    display_name = "Battle Logic Difficulty"
    #option_picnic = BattleLogicDifficultyType.picnic.value
    option_normal = BattleLogicDifficultyType.normal.value
    #option_expert = BattleLogicDifficultyType.expert.value
    default = BattleLogicDifficultyType.normal.value

class SustainLogicEnabled(DefaultOnToggle):
    display_name = "Sustain Logic Enabled"

class LevelCapMode(Choice):
    display_name = "Level Cap Mode"
    option_none = 0
    option_fixed_increase = 1
    option_complete_shuffle = 2
    default = 1

class InitialLevelCap(Range):
    display_name = "Initial Level Cap"
    range_start = 1
    range_end = MAX_LEVEL
    default = 10

class LevelCapIncreaseValue(Choice):
    display_name = "Level Cap Increase Value"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_10 = 10
    option_15 = 15
    default = 4

class ExtraProgressiveLevelCapItems(Range):
    display_name = "Extra Progressive Level Cap Items"
    range_start = 0
    range_end = 30
    default = 0

class FloorLimitMode(Choice):
    display_name = "Floor Limit Mode"
    option_none = 0
    option_fixed_increase = 1
    option_complete_shuffle = 2
    default = 1

class InitialFloorLimit(Range):
    display_name = "Initial Floor Limit"
    range_start = 1
    range_end = 30
    default = 1

class FloorLimitIncreaseValue(Choice):
    display_name = "Floor Limit Increase Value"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_10 = 10
    default = 1

class ExtraProgressiveFloorLimitItems(Range):
    display_name = "Extra Progressive Floor Limit Items"
    range_start = 0
    range_end = 10
    default = 0

class ClassSanityMode(Choice):
    display_name = "Class Sanity Mode"
    option_vanilla = ClassSanityType.vanilla.value
    option_start_with_all = ClassSanityType.start_with_all.value
    option_shuffle_availability = ClassSanityType.shuffle_availability.value
    default = ClassSanityType.shuffle_availability.value

class StartingClassCount(Range):
    display_name = "Starting Class Count"
    range_start = 1
    range_end = 9
    default = 4

# Skillsanity
class SkillSanityMode(Choice):
    display_name = "Skill Sanity Mode"
    option_none = SkillSanityType.none.value
    option_shuffle_individually = SkillSanityType.shuffle_individually.value
    option_shuffle_group = SkillSanityType.shuffle_group.value
    #option_shuffle_progressive = 3
    default = SkillSanityType.none.value

class ShuffleGenericStatsIncreaseSkills(DefaultOnToggle):
    display_name = "Shuffle Generic Stats Increase Skills"

class ShuffleGatheringSkills(Toggle):
    display_name = "Shuffle Gathering Skills"

class RemoveSkillsRequirements(Toggle):
    display_name = "Remove Skills Requirements"

class StartingSkillItemCount(Range):
    display_name = "Starting Skill Item Count"
    range_start = 0
    range_end = 21
    default = 0

# Codexsanity
class CodexSanity(DefaultOnToggle):
    display_name = "Codex Sanity"

# Compendiumsanity
class CompendiumSanity(Toggle):
    display_name = "Compendium Sanity"

class CompendiumSanityIncludeConditionalDrops(DefaultOnToggle):
    display_name = "Compendium Sanity Include Conditional Drops"

# QoL options
class ShopUnlockMaterialCostDivider(Choice):
    display_name = "Shop Unlock Material Cost Divider"
    option_vanilla = 1
    option_half = 2
    option_quarter = 4
    option_one_for_all = 50
    default = 1

# Quest sanity
# FOEsanity
# Shopsanity
# Tilesanity

# todo Rest option
# todo Shop balancing

@dataclass
class EtrianOdysseyOptions(PerGameCommonOptions):
    goal: EtrianOdysseyGoal
    experience_modifier: ExperienceModifier
    battle_logic_mode: BattleLogicMode
    battle_logic_difficulty: BattleLogicDifficulty
    sustain_logic_enabled: SustainLogicEnabled
    level_cap_mode: LevelCapMode
    initial_level_cap: InitialLevelCap
    level_cap_increase_value: LevelCapIncreaseValue
    extra_progressive_level_cap_items: ExtraProgressiveLevelCapItems
    floor_limit_mode: FloorLimitMode
    initial_floor_limit: InitialFloorLimit
    floor_limit_increase_value: FloorLimitIncreaseValue
    extra_progressive_floor_limit: ExtraProgressiveFloorLimitItems
    class_sanity_mode: ClassSanityMode
    starting_class_count: StartingClassCount
    skill_sanity_mode: SkillSanityMode
    shuffle_generic_stats_increase_skills: ShuffleGenericStatsIncreaseSkills
    shuffle_gathering_skills: ShuffleGatheringSkills
    remove_skills_requirements: RemoveSkillsRequirements
    starting_skill_item_count: StartingSkillItemCount
    codex_sanity: CodexSanity
    compendium_sanity: CompendiumSanity
    compendium_sanity_include_conditional_drops: CompendiumSanityIncludeConditionalDrops
    shop_unlock_material_cost_divider: ShopUnlockMaterialCostDivider

    def get_effective_initial_level_cap(self) -> int:
        if self.level_cap_mode.value != LevelCapMode.option_none:
            return self.initial_level_cap.value
        else:
            return MAX_LEVEL

    def get_effective_initial_floor_limit(self) -> int:
        if self.floor_limit_mode.value != FloorLimitMode.option_none:
            return self.initial_floor_limit.value
        else:
            return MAX_FLOOR