from dataclasses import dataclass
from .Constant import *
from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions
#, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
#    ItemDict, ItemsAccessibility, ItemSet, Visibility

class EtrianOdysseyGoal(Choice):
    """
    Controls what the goal of the game is for the randomizer.

    - **Defeat Fenrir:** Defeat the boss of the 1st Stratum, Fenrir (B5F) (Lvl 30).
    - **Defeat Cernunos:** Defeat the boss of the 2nd Stratum, Cernunos (B10F) (Lvl 40).
    - **Defeat Cotrangl:** Defeat the boss of the 3rd Stratum, Cotrangl (B15F) (Lvl 50).
    - **Annihilate the Forest Folk:** Defeat the boss of the 4th Stratum, Iwaopeln and all the FOEs on B20F (Lvl 60).
    - **Defeat Etreant:** Defeat the boss of the 5th Stratum (and the normal end of the game), Etreant (B25F) (Lvl 70).
    - **Defeat Primevil:** Defeat the boss of the 6th Stratum (postgame), Primevil (B30F) (Lvl 70). WARNING: NOT RECOMMENDED
      UNLESS YOU KNOW WHAT YOU ARE GETTING INTO
    """

    display_name = "Goal"
    option_defeat_fenrir = EO1Goal.defeat_fenrir.value
    option_defeat_cernunos = EO1Goal.defeat_cernunos.value
    option_defeat_cotrangl = EO1Goal.defeat_cotrangl.value
    #option_annihilate_the_forest_folk = EO1Goal.annihilate_the_forest_folk.value
    option_defeat_etreant  = EO1Goal.defeat_etreant.value
    #option_defeat_primevil = EO1Goal.defeat_primevil.value
    default = EO1Goal.defeat_etreant.value

class ExperienceModifier(Range):
    """
    Experience modifier (as percentage). Recommended at least 500(%).
    Note: Etrian Odyssey 1 uniquely has the level difference factored in damage calculation, making level extremely important.
    Note: This doesn't affect logic.
    """

    display_name = "Experience Modifier"
    range_start = 50
    range_end = 1000
    default = 500

class BattleLogicMode(Choice):
    """
    Controls how battle logic function.

    - **Simplified:** (Recommended) Criteria based logic for each individual enemies.
      Also does everything "Level Only" does.
    - **Level Only:** Battle Logic only consider the level cap of the player. Not recommended with Skill Shuffling.
    - **No Logic:** Absolutely no logic, everything is considered defeatable from the go.
      Recommended only if only level cap, class shuffling and skill shuffling are disabled.
    """

    display_name = "Battle Logic Mode"
    #option_generous = BattleLogicModeType.generous.value
    #option_standard = BattleLogicModeType.standard.value
    #option_restrictive = BattleLogicModeType.restrictive.value
    option_simplified = BattleLogicModeType.simplified.value
    option_level_only = BattleLogicModeType.level_only.value
    option_no_logic = BattleLogicModeType.no_logic.value
    default = BattleLogicModeType.level_only.value

class BattleLogicDifficulty(Choice):
    """
    Placeholder for future settings.
    """

    display_name = "Battle Logic Difficulty"
    #option_picnic = BattleLogicDifficultyType.picnic.value
    option_normal = BattleLogicDifficultyType.normal.value
    #option_expert = BattleLogicDifficultyType.expert.value
    default = BattleLogicDifficultyType.normal.value

class SustainLogicEnabled(DefaultOnToggle):
    """
    When enabled, ensure the player has strong enough renewable healing items or healing skills to reach each region.
    Note: This has a noticeable cost on generation time and should be turned off if Skills and Class are not shuffled.
    """

    display_name = "Sustain Logic Enabled"

class LevelCapMode(Choice):
    """
    Option that controls how level cap are handled. By default, in Etrian Odyssey 1, the player level cap at level 70
    and nothing increase it. This randomizer restrict this level cap and add Items that increase the starting cap for
    every player characters. This does not allow to go above level 70.

    Note: The starting level cap is defined by the Initial Level Cap option.
    Note: The item pool is balanced based on the goal in a way to have the final level cap to be within reason for it,
          instead of always having enough items to reach level 70. See the goals to know what are the targeted level cap.

    - **None:** Level cap is vanilla (70). Expect a lot of potential level grinding to be required.
    - **Fixed Increase:** (Recommended) Every level cap items will have the same level value, determined by the options.
    - **Complete Shuffle:** Add level cap items with random values.
    """

    display_name = "Level Cap Mode"
    option_none = 0
    option_fixed_increase = 1
    option_complete_shuffle = 2
    default = 1

class InitialLevelCap(Range):
    """
    Define the starting level cap of the player. Only used if "Level Cap Mode" is not "None".
    """

    display_name = "Initial Level Cap"
    range_start = 1
    range_end = MAX_LEVEL
    default = 10

class LevelCapIncreaseValue(Choice):
    """
    Define by how many level each Level Cap items increase the player level cap.
    Only used if "Level Cap Mode" is "Fixed Increase".
    """

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
    """
    Add extra Level Cap items to the item pool (instead of the minimum).
    Works with both "Fixed Increase" and "Complete Shuffle".

    The purpose of this option is to not require the player to need every single level cap items from the pool.
    """

    display_name = "Extra Progressive Level Cap Items"
    range_start = 0
    range_end = 30
    default = 0

class FloorLimitMode(Choice):
    """
    Option that controls how floor limit are handled. By default, in Etrian Odyssey 1, there are no concept of Floor
    Limit. The player can go to any floor available to their current progression (up to floor B30F). This randomizer
    restrict this by adding Items that increase the maximum floor the player go enter.

    Note: The starting floor limit is defined by the Initial Floor Limit option.
    Note: Pitfalls allow to bypass this limit, but are never considered in logic. This is intentional behavior.
    Note: The item pool is balanced based on the goal in a way to have the final floor limit stop at it,
          instead of always having enough items to reach Floor 30. See the goals to know what are the floor limit.

    - **None:** Floor Limit is vanilla (30).
    - **Fixed Increase:** (Recommended) Every floor limit items will have the same floor value, determined by the options.
    - **Complete Shuffle:** Add floor limit items with random values.
    """

    display_name = "Floor Limit Mode"
    option_none = 0
    option_fixed_increase = 1
    option_complete_shuffle = 2
    default = 1

class InitialFloorLimit(Range):
    """
    Define the starting floor limit. Only used if "Floor Limit Mode" is not "None".
    """

    display_name = "Initial Floor Limit"
    range_start = 1
    range_end = 30
    default = 5

class FloorLimitIncreaseValue(Choice):
    """
    Define by how many floor each Floor Limit items increase the floor limit.
    Only used if "Floor Limit Mode" is "Fixed Increase".
    """

    display_name = "Floor Limit Increase Value"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_10 = 10
    default = 1

class ExtraProgressiveFloorLimitItems(Range):
    """
    Add extra Floor Limit items to the item pool (instead of the minimum).
    Works with both "Fixed Increase" and "Complete Shuffle".

    The purpose of this option is to not require the player to need every single Floor Limit items from the pool.
    """

    display_name = "Extra Progressive Floor Limit Items"
    range_start = 0
    range_end = 10
    default = 0

class ClassSanityMode(Choice):
    """
    Controls how available character class are shuffled.

    - **Vanilla:** Start with all the vanilla starting class, shuffling only Ronin and Hexer.
                   Note that theses are shuffled in the item pool and are not unlocked by their normal method.
    - **Start With All:** No class are shuffled, the player starts with all of them available.
    - **Shuffle Availability:** Start with the amount of class defined by "Starting Class Count".
                                Every other class are shuffled in the item pool.
    """

    display_name = "Class Sanity Mode"
    option_vanilla = ClassSanityType.vanilla.value
    option_start_with_all = ClassSanityType.start_with_all.value
    option_shuffle_availability = ClassSanityType.shuffle_availability.value
    default = ClassSanityType.shuffle_availability.value

class StartingClassCount(Range):
    """
    Define how many class are available at the start. Only used if "Class Sanity Mode" is "Shuffle Availability".
    """

    display_name = "Starting Class Count"
    range_start = 1
    range_end = 9
    default = 4

# Skillsanity
class SkillSanityMode(Choice):
    """
    Controls how available class Skills are shuffled.

    Note: This shuffles the ability to learn skills. It doesn't change what skill a class have.

    - **None:** Vanilla behavior. All class skills are available as normal.
    - **Shuffle Individually:** Every Skill are their own individual item in the pool.
    - **Shuffle Group:** Skill are grouped in predetermined arbitrary categories, and each group are one item in the pool.
    """

    display_name = "Skill Sanity Mode"
    option_none = SkillSanityType.none.value
    option_shuffle_individually = SkillSanityType.shuffle_individually.value
    option_shuffle_group = SkillSanityType.shuffle_group.value
    #option_shuffle_progressive = 3
    default = SkillSanityType.none.value

class ShuffleGenericStatsIncreaseSkills(DefaultOnToggle):
    """
    Determine if the Generic Stats increase skills are shuffled.

    These are:
    - HP Up
    - TP Up
    - Atk Up
    - Def Up
    - Agi Up

    If enabled, these skills are shuffled according to the "Skill Sanity Mode" option.
    If disabled, the player start with all of them available.
    """

    display_name = "Shuffle Generic Stats Increase Skills"

class ShuffleMasterySkills(DefaultOnToggle):
    """
    Determine if the Mastery Skills are shuffled.

    These are:
    - Landsknecht Axes
    - Landsknecht Swords
    - Survivalist Bows
    - Protector Shields
    - Dark Hunter Whips
    - Dark Hunter Swords
    - Medic Healer
    - Alchemist Fire Up
    - Alchemist Ice Up
    - Alchemist Volt Up
    - Alchemist Toxins
    - Troubadour Songs
    - Ronin Katanas
    - Hexer Curses

    If enabled, these skills are shuffled according to the "Skill Sanity Mode" option.
    If disabled, the player start with all of them available.
    Note: This is not particularly useful for Skill Sanity Mode "Group".
    """

    display_name = "Shuffle Mastery Skills"

class ShuffleGatheringSkills(Toggle):
    """
    Determine if the Gathering skills are shuffled.

    These are:
    - Take
    - Mine
    - Chop

    If enabled, these skills are shuffled according to the "Skill Sanity Mode" option.
    If disabled, the player start with all of them available.
    """

    display_name = "Shuffle Gathering Skills"

class RemoveSkillsRequirements(Toggle):
    """
    This option removes the skills requirement from the game. This mean that every skill are learnable by themselves
    from level 1 (if unlocked). This affects Logic.

    This option is experimental and is recommended to make early game faster/smoother.

    Note: Most Ronin skills still need their respective Stance skills to be usable. Logic accounts for this.
    Note: Hexer Paralyze, Betrayal and Suicide skills still need Evil Eye to be usable. Logic accounts for this.
    """

    display_name = "Remove Skills Requirements"

class StartingSkillItemCount(Range):
    """
    Define how many skill items each character class start with unlocked.
    This doesn't count skills that are not shuffled because of the options.
    Skill Item in this context mean that with "Shuffle Group", each Skill Group count for one, instead of each skill
    counting individually.

    Note: Starting Skills are not guaranteed to be usable if required skills are not also unlocked.
    """

    display_name = "Starting Skill Item Count"
    range_start = 0
    range_end = 21
    default = 0

# Codexsanity
class CodexSanity(DefaultOnToggle):
    """
    Shuffles Monster Codex entries as Locations.

    Monster Codex entries are unlocked by defeating a monster for the first time.
    """

    display_name = "Codex Sanity"

# Compendiumsanity
class CompendiumSanity(Toggle):
    """
    Shuffles Item Compendium entries as Locations. Includes both Gathering items and Monster Drops.

    Item Compendium entries are unlocked by obtaining a material for the first time.
    """

    display_name = "Compendium Sanity"

class CompendiumSanityIncludeConditionalDrops(DefaultOnToggle):
    """
    Shuffles Item Compendium entries only available by Conditional Monster Drops as locations.
    """

    display_name = "Compendium Sanity Include Conditional Drops"

# QoL options
class ShopUnlockMaterialCostDivider(Choice):
    """
    Reduce the amount of material required to be sold to unlock new shop items.

    - **Vanilla:** Nothing is changed.
    - **Half:** The amount of material required is halved (rounded up).
    - **Quarter:** The amount of material required is divided by 4 (rounded up).
    - **One for All:** The amount of material required is set to 1 for every item. Minimal grind.

    Note: This doesn't affect logic.
    """

    display_name = "Shop Unlock Material Cost Divider"
    option_vanilla = 1
    option_half = 2
    option_quarter = 4
    option_one_for_all = 50
    default = 1

class MaterialSellValueMultiplier(Range):
    """
    Multiply the amount of money acquired by selling material. "1" means vanilla values.

    Note: This doesn't affect logic.
    """

    display_name = "Material Sell Value Multiplier"
    range_start = 1
    range_end = 100
    default = 1

# Quest sanity
# FOEsanity
# Shopsanity
# Tilesanity

# todo Rest option
# todo Shop balancing

@dataclass
class EtrianOdysseyOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for Etrian Odyssey.
    """

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
    shuffle_mastery_skills: ShuffleMasterySkills
    shuffle_gathering_skills: ShuffleGatheringSkills
    remove_skills_requirements: RemoveSkillsRequirements
    starting_skill_item_count: StartingSkillItemCount
    codex_sanity: CodexSanity
    compendium_sanity: CompendiumSanity
    compendium_sanity_include_conditional_drops: CompendiumSanityIncludeConditionalDrops
    shop_unlock_material_cost_divider: ShopUnlockMaterialCostDivider
    material_sell_value_multiplier: MaterialSellValueMultiplier

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