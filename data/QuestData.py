from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum

from .ClassData import EO1Class
from .EnemyData import EO1Enemies
from .InventoryItemData import EO1ItemID
from .MaterialData import EO1MaterialID
from .RegionData import EO1Regions
from .SkillData import EO1Skills


class QuestRequirement(IntEnum):
    NONE = 0
    QUEST = 1
    KEY_ITEM = 2
    BEAT_STORY = 3

class QuestCompletionRequirementType(IntEnum):
    CAN_REACH_REGION = 1
    CAN_OBTAIN_MATERIAL = 2
    HAS_QUEST_ITEM = 3
    HAS_CLASS_OF_LEVEL = 4
    HAS_CLASS_AND_SKILL = 5
    CAN_SOLO_ENEMY = 6
    CAN_FILL_X_MONSTER_CODEX_ENTRIES = 7
    CAN_FILL_X_ITEM_COMPENDIUM_ENTRIES = 8
    CAN_DEFEAT_ENCOUNTER = 9

class QuestCompletionRequirement(ABC):
    @property
    @abstractmethod
    def requirement_type(self) -> QuestCompletionRequirementType:
        pass

@dataclass
class CanReachRegion(QuestCompletionRequirement):
    region: str

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_REACH_REGION

@dataclass
class CanObtainMaterial(QuestCompletionRequirement):
    item_id: list[int]

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_OBTAIN_MATERIAL

@dataclass
class HasQuestItem(QuestCompletionRequirement):
    item_names: list[str]

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.HAS_QUEST_ITEM

@dataclass
class HasClassOfLevel(QuestCompletionRequirement):
    class_name: str
    required_level: int

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.HAS_CLASS_OF_LEVEL

@dataclass
class HasClassAndSkill(QuestCompletionRequirement):
    class_name: str
    skill_id: int

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.HAS_CLASS_AND_SKILL

@dataclass
class CanSoloEnemy(QuestCompletionRequirement):
    enemy_id: int

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_SOLO_ENEMY

@dataclass
class CanFillXMonsterCodexEntries(QuestCompletionRequirement):
    entries_count: int

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_FILL_X_MONSTER_CODEX_ENTRIES

@dataclass
class CanFillXItemCompendiumEntries(QuestCompletionRequirement):
    entries_count: int

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_FILL_X_ITEM_COMPENDIUM_ENTRIES

@dataclass
class CanDefeatEncounter(QuestCompletionRequirement):
    enemies: list[int]

    @property
    def requirement_type(self) -> QuestCompletionRequirementType:
        return QuestCompletionRequirementType.CAN_DEFEAT_ENCOUNTER

@dataclass(frozen=True)
class QuestData:
    quest_id: int
    location_id: int
    quest_name: str
    floor_requirement: int
    level_requirement: int
    required_stratum: int
    completion_flag: int
    quest_unlock_requirement: QuestRequirement = QuestRequirement.NONE
    quest_unlock_requirement_value: int = -1
    quest_completion_requirements: list[QuestCompletionRequirement] = field(default_factory=list)

    def get_full_location_name(self) -> str:
        return f"Quest Completion: {self.quest_name}"


class EO1QuestID:
    THE_LEATHERSMITHS_FAVOR = 0
    A_CERTAIN_SHOPS_REQUEST = 1
    TO_TASTE_IT_ONCE_MORE = 2
    A_FAVOR_TO_SHILLEKA_I = 3
    A_FAVOR_TO_SHILLEKA_II = 4
    A_FAVOR_TO_SHILLEKA_III = 5
    SUBDUING_THE_WOODFLIES = 6
    THE_LUCKY_COIN = 7
    EXPLORERS_GUILD_TRIAL = 9
    TO_MEET_A_SWORDSMAN = 12
    TO_MEET_A_BLADEMASTER = 13
    TO_MEET_A_HOLY_KNIGHT = 14
    IVORY_PRINCESS_DREAM_I = 15
    THE_FOSSIL_CHARM = 16
    CHEFS_REQUEST_I = 17
    APOTHECARYS_REQUEST_I = 18
    SHADOW_IN_THE_GROVE = 21
    FASHIONISTA_I = 22
    FASHIONISTA_II = 23
    REMEMBERING_THE_FALLEN = 24
    PRAYER_TO_THE_STARS = 25
    THE_IVORY_CHARM = 29
    FEAT_OF_STRENGTH_I = 30
    FEAT_OF_STRENGTH_II = 31
    FEAT_OF_STRENGTH_III = 32
    CHEFS_REQUEST_II = 33
    CHEFS_ODD_REQUEST_I = 34
    CHEFS_ODD_REQUEST_II = 35
    CHEFS_LATEST_REQUEST_I = 36
    CHEFS_LATEST_REQUEST_II = 37
    APOTHECARYS_REQUEST_II = 38
    UNDER_CONSTRUCTION = 39
    LOVE__CAST_IN_SILVER = 40
    APOTHECARYS_REQUEST_III = 41
    THE_FOREIGN_SEEKER = 42
    I_REFUSE_THEE__DEATH = 43
    A_SISTERS_PARTING_GIFT = 44
    LOVES_UNCERTAIN_PROMISE = 46
    FOND_MEMORIES_OF_YOU = 49
    CHEFS_DEMAND = 50
    HORTICULTURE = 51
    ORPHANS_OF_THE_FOREST = 52
    PEST_CONTROL = 53
    IDENTITY_UNKNOWN = 57
    MONSTER_AT_SUNRISE = 58
    WORK_STOPPAGE = 60
    THE_CRYSTAL_MAIDEN = 61
    EMBLEM_OF_LOVE = 62
    THE_GOLD_ENTHUSIAST = 63
    REMEMBRANCE_OF_A_FRIEND = 64
    SONG_FROM_THE_DEPTHS = 65
    SCAVENGING_FOR_IAN_I = 66
    IVORY_PRINCESS_DREAM_II = 68
    SCAVENGING_FOR_IAN_II = 69
    MONSTROUS_CODEX = 70
    THE_DIAMOND_CHARM = 71
    GOURMANDS_REQUEST = 72
    VERSUS_THE_UNKNOWN = 74
    THE_LEGENDARY_BIRD = 75
    OFFICIAL_BUSINESS_I = 77
    ITEM_COMPENDIUM = 78
    OFFICIAL_BUSINESS_II = 81
    REVERSAL_OF_THE_POLES = 82
    LOST_PET__REWARD_OFFERED = 83
    OFFICIAL_BUSINESS_III = 84
    PHANTOM_OF_THE_FOREST = 85
    THE_BANDITS_TREASURE = 86
    CALL_OF_THE_WYVERN = 87
    THE_DREAD_WYRM = 88
    PROOF_OF_HEROISM = 89
    THE_AZURE_COLOSSUS = 90
    REMNANTS_OF_AN_AGE_PAST = 91
    AWAKENING_THE_SERPENT = 92


ALL_QUEST_DATA: list[QuestData] = [
    QuestData(EO1QuestID.THE_LEATHERSMITHS_FAVOR, 4000, "The leathersmith's favor", -1, -1, 1, 0x404,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.SOFT_HIDE])]),
    QuestData(EO1QuestID.A_CERTAIN_SHOPS_REQUEST, 4001, "A certain shop's request", 1, -1, 1, 0x414, QuestRequirement.QUEST, EO1QuestID.THE_LEATHERSMITHS_FAVOR,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.PYROXENE])]),
    QuestData(EO1QuestID.TO_TASTE_IT_ONCE_MORE, 4002, "To taste it once more...", -1, -1, 1, 0x424,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B1F_MAIN)]), # TODO Quest Item Holy Water.
    QuestData(EO1QuestID.A_FAVOR_TO_SHILLEKA_I, 4003, "A favor to Shilleka I", -1, -1, 1, 0x434, QuestRequirement.KEY_ITEM, EO1ItemID.RADHA_NOTE,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.HARD_SHELL, EO1MaterialID.HARDWOOD])]),
    QuestData(EO1QuestID.A_FAVOR_TO_SHILLEKA_II, 4004, "A favor to Shilleka II", 3, -1, 1, 0x444, QuestRequirement.QUEST, EO1QuestID.A_FAVOR_TO_SHILLEKA_I,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.HORN, EO1MaterialID.GUM_HIDE])]),
    QuestData(EO1QuestID.A_FAVOR_TO_SHILLEKA_III, 4005, "A favor to Shilleka III", 7, -1, 2, 0x454, QuestRequirement.QUEST, EO1QuestID.A_FAVOR_TO_SHILLEKA_II,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.TAILBONE, EO1MaterialID.BIRD_TALON])]),
    QuestData(EO1QuestID.SUBDUING_THE_WOODFLIES, 4006, "Subduing the Woodflies", 3, -1, 1, 0x465,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B1F_MAIN)]), # This quest doesn't require to do anything. It has 2 endings: If you just turn it in immediately (bad), or if you entered the labyrinth since accepting it (good).
    QuestData(EO1QuestID.THE_LUCKY_COIN, 4007, "The lucky coin", 9, -1, 2, 0x475,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B8F_MAIN), CanDefeatEncounter([EO1Enemies.FIREATER])]), # TODO Maybe need Quest Item? Lucky Coin
    QuestData(EO1QuestID.EXPLORERS_GUILD_TRIAL, 4008, "Explorers Guild trial", 8, -1, 2, 0x492,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B8F_MAIN), CanDefeatEncounter([EO1Enemies.PONDCLAW])]), # Require in logic to be able to get the healing spring.
    QuestData(EO1QuestID.TO_MEET_A_SWORDSMAN, 4009, "To meet a swordsman...", 3, -1, 2, 0x4C4,
	              quest_completion_requirements=[HasClassOfLevel(EO1Class.LANDSKNECHT, 20)]),
    QuestData(EO1QuestID.TO_MEET_A_BLADEMASTER, 4010, "To meet a blademaster...", 5, -1, 3, 0x4D4, QuestRequirement.QUEST, EO1QuestID.TO_MEET_A_HOLY_KNIGHT,
	              quest_completion_requirements=[HasClassOfLevel(EO1Class.RONIN, 20)]),
    QuestData(EO1QuestID.TO_MEET_A_HOLY_KNIGHT, 4011, "To meet a holy knight...", 4, -1, 3, 0x4E4, QuestRequirement.QUEST, EO1QuestID.TO_MEET_A_SWORDSMAN,
	              quest_completion_requirements=[HasClassOfLevel(EO1Class.PROTECTOR, 30)]),
    QuestData(EO1QuestID.IVORY_PRINCESS_DREAM_I, 4012, "Ivory Princess' dream I", 24, -1, 5, 0x4F4,
	              quest_completion_requirements=[HasClassAndSkill(EO1Class.HEXER, EO1Skills.HEXER_TORPOR)]),
    QuestData(EO1QuestID.THE_FOSSIL_CHARM, 4013, "The fossil charm", 10, -1, 2, 0x504,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.FOSSIL])]),
    QuestData(EO1QuestID.CHEFS_REQUEST_I, 4014, "Chef's request I", 14, -1, 3, 0x514,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.BUG_NEST])]),
    QuestData(EO1QuestID.APOTHECARYS_REQUEST_I, 4015, "Apothecary's request I", 19, -1, 4, 0x524,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B18F_WEST)]), # Maybe can be encountered earlier?
    QuestData(EO1QuestID.SHADOW_IN_THE_GROVE, 4016, "Shadow in the grove", 6, -1, 2, 0x554,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B5F_MAIN), CanDefeatEncounter([EO1Enemies.SPIDER])]),
    QuestData(EO1QuestID.FASHIONISTA_I, 4017, "Fashionista I", 6, -1, 2, 0x564,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.INSECT_EYE])]),
    QuestData(EO1QuestID.FASHIONISTA_II, 4018, "Fashionista II", 7, -1, 2, 0x574, QuestRequirement.QUEST, EO1QuestID.FASHIONISTA_I,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.TOXIC_BARB])]),
    QuestData(EO1QuestID.REMEMBERING_THE_FALLEN, 4019, "Remembering the fallen", 11, -1, 3, 0x589,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B11F_MAIN)]), # TODO Rust Sword/Broken Axe/Old Wand
    QuestData(EO1QuestID.PRAYER_TO_THE_STARS, 4020, "Prayer to the stars", 6, -1, 2, 0x594,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.STARSEED])]),
    QuestData(EO1QuestID.THE_IVORY_CHARM, 4021, "The ivory charm", 15, -1, 3, 0x5D4, QuestRequirement.QUEST, EO1QuestID.THE_FOSSIL_CHARM,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.GREAT_TUSK])]),
    QuestData(EO1QuestID.FEAT_OF_STRENGTH_I, 4022, "Feat of strength I", 11, -1, 3, 0x5E6,
	              quest_completion_requirements=[CanSoloEnemy(EO1Enemies.CUTTER)]),
    QuestData(EO1QuestID.FEAT_OF_STRENGTH_II, 4023, "Feat of strength II", 14, -1, 4, 0x5F6, QuestRequirement.QUEST, EO1QuestID.FEAT_OF_STRENGTH_I,
	              quest_completion_requirements=[CanSoloEnemy(EO1Enemies.KILLCLAW)]),
    QuestData(EO1QuestID.FEAT_OF_STRENGTH_III, 4024, "Feat of strength III", 21, -1, 5, 0x606, QuestRequirement.QUEST, EO1QuestID.FEAT_OF_STRENGTH_II,
	              quest_completion_requirements=[CanSoloEnemy(EO1Enemies.SICKWOOD)]),
    QuestData(EO1QuestID.CHEFS_REQUEST_II, 4025, "Chef's request II", 17, -1, 4, 0x614,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.MUSK])]),
    QuestData(EO1QuestID.CHEFS_ODD_REQUEST_I, 4026, "Chef's odd request I", 4, -1, 1, 0x624,
	              quest_completion_requirements=[HasClassAndSkill(EO1Class.ALCHEMIST, EO1Skills.ALCHEMIST_FIRE)]),
    QuestData(EO1QuestID.CHEFS_ODD_REQUEST_II, 4027, "Chef's odd request II", 9, -1, 2, 0x634, QuestRequirement.QUEST, EO1QuestID.CHEFS_ODD_REQUEST_I,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.CARMINITE])]),
    QuestData(EO1QuestID.CHEFS_LATEST_REQUEST_I, 4028, "Chef's latest request I", 26, -1, 6, 0x644,
	              quest_completion_requirements=[HasClassAndSkill(EO1Class.ALCHEMIST, EO1Skills.ALCHEMIST_COCYTUS)]),
    QuestData(EO1QuestID.CHEFS_LATEST_REQUEST_II, 4029, "Chef's latest request II", 26, -1, 6, 0x654, QuestRequirement.QUEST, EO1QuestID.CHEFS_LATEST_REQUEST_I,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.COLD_SCALE])]),
    QuestData(EO1QuestID.APOTHECARYS_REQUEST_II, 4030, "Apothecary's request II", 19, -1, 4, 0x664, QuestRequirement.QUEST, EO1QuestID.APOTHECARYS_REQUEST_I,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.BIRD_LIMB])]),
    QuestData(EO1QuestID.UNDER_CONSTRUCTION, 4031, "Under construction", 18, -1, 4, 0x674,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.HARD_SHARD, EO1MaterialID.STEEL_CHIP])]),
    QuestData(EO1QuestID.LOVE__CAST_IN_SILVER, 4032, "Love, cast in silver", 12, -1, 3, 0x684,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.CORUNDUM])]),
    QuestData(EO1QuestID.APOTHECARYS_REQUEST_III, 4033, "Apothecary's request III", 18, -1, 4, 0x694, QuestRequirement.QUEST, EO1QuestID.APOTHECARYS_REQUEST_II,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.CORDYCEPS])]),
    QuestData(EO1QuestID.THE_FOREIGN_SEEKER, 4034, "The foreign seeker", 16, -1, 4, 0x6A4,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.N100_SHELL])]),
    QuestData(EO1QuestID.I_REFUSE_THEE__DEATH, 4035, "I refuse thee, Death", 24, -1, 5, 0x6B5,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.GUM_THREAD, EO1MaterialID.BLUE_BLOOD, EO1MaterialID.RED_BLOOD, EO1MaterialID.DRYWALL])]), # TODO Quest Item Panacea
    QuestData(EO1QuestID.A_SISTERS_PARTING_GIFT, 4036, "A sister's parting gift", 23, -1, 5, 0x6C4,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.ANGEL_WING])]),
    QuestData(EO1QuestID.LOVES_UNCERTAIN_PROMISE, 4037, "Love's uncertain promise", 16, -1, 4, 0x6E3,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B16F_MAIN)]), # TODO Bandanna
    QuestData(EO1QuestID.FOND_MEMORIES_OF_YOU, 4038, "Fond memories of you...", 13, -1, 5, 0x716,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B11F_PITFALL), CanDefeatEncounter([EO1Enemies.WARBULL]), CanDefeatEncounter([EO1Enemies.HELLBULL])]), # TODO Pearl
    QuestData(EO1QuestID.CHEFS_DEMAND, 4039, "Chef's demand", 17, -1, 4, 0x724,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.FISH_FIN, EO1MaterialID.DRY_PEACH, EO1MaterialID.RED_BEAK])]),
    QuestData(EO1QuestID.HORTICULTURE, 4040, "Horticulture", 6, -1, 2, 0x738,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B6F_MAIN), CanDefeatEncounter([EO1Enemies.WASPIOR, EO1Enemies.WASPIOR]), CanDefeatEncounter([EO1Enemies.WASPIOR, EO1Enemies.WASPIOR]), CanDefeatEncounter([EO1Enemies.WASPIOR, EO1Enemies.WASPIOR, EO1Enemies.SLEEPGEL]), CanDefeatEncounter([EO1Enemies.WASPIOR, EO1Enemies.WASPIOR, EO1Enemies.SLOTH])]), # TODO Quest Item Gold Seed/Rare Bloom
    QuestData(EO1QuestID.ORPHANS_OF_THE_FOREST, 4041, "Orphans of the forest", 13, -1, 3, 0x744,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B12F_ANT_MAZE)]),
    QuestData(EO1QuestID.PEST_CONTROL, 4042, "Pest control", 11, -1, 3, 0x758,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.AMBER_LUMP]), CanReachRegion(EO1Regions.B10F_MAIN), CanDefeatEncounter([EO1Enemies.TOXINFLY, EO1Enemies.TOXINFLY, EO1Enemies.TOXINFLY])]), # Encounters are: 2 Toxinfly, 2 Toxinfly, 3 Toxinfly, 3 Toxinfly.
    QuestData(EO1QuestID.IDENTITY_UNKNOWN, 4043, "Identity unknown", 7, -1, 2, 0x793, QuestRequirement.QUEST, EO1QuestID.SHADOW_IN_THE_GROVE,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B6F_MAIN), CanDefeatEncounter([EO1Enemies.PETALOID])]),
    QuestData(EO1QuestID.MONSTER_AT_SUNRISE, 4044, "Monster at sunrise", 29, -1, 6, 0x7A3,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B1F_MAIN), CanDefeatEncounter([EO1Enemies.CLOVER])]),
    QuestData(EO1QuestID.WORK_STOPPAGE, 4045, "Work stoppage", 18, -1, 4, 0x7C3,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B17F_MAIN), CanDefeatEncounter([EO1Enemies.SICKWOOD])]), # Technically its 3 individual Sickwood, but if the player can beat one of them, they can beat all of them.
    QuestData(EO1QuestID.THE_CRYSTAL_MAIDEN, 4046, "The Crystal Maiden", 21, -1, 5, 0x7D4,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.SHINY_VINE])]),
    QuestData(EO1QuestID.EMBLEM_OF_LOVE, 4047, "Emblem of love", 28, -1, 6, 0x7E4, QuestRequirement.QUEST, EO1QuestID.THE_CRYSTAL_MAIDEN,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.TRI_COLOR])]),
    QuestData(EO1QuestID.THE_GOLD_ENTHUSIAST, 4048, "The gold enthusiast", 22, -1, 5, 0x7F4,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.GOLD_FUR])]),
    QuestData(EO1QuestID.REMEMBRANCE_OF_A_FRIEND, 4049, "Remembrance of a friend", 21, -1, 5, 0x804, QuestRequirement.QUEST, EO1QuestID.REMEMBERING_THE_FALLEN,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.TINY_PETAL, EO1MaterialID.PURE_ROOT]), CanReachRegion(EO1Regions.B1F_MAIN)]),
    QuestData(EO1QuestID.SONG_FROM_THE_DEPTHS, 4050, "Song from the depths", 27, -1, 6, 0x813,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B24F_NORTH)]), # TODO Quest Item (Vox Stone)
    QuestData(EO1QuestID.SCAVENGING_FOR_IAN_I, 4051, "Scavenging for Ian I", 11, -1, 3, 0x824,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.SCRAP_IRON, EO1MaterialID.FOSSIL, EO1MaterialID.THIN_SHELL])]),
    QuestData(EO1QuestID.IVORY_PRINCESS_DREAM_II, 4052, "Ivory Princess' dream II", 24, -1, 5, 0x845, QuestRequirement.QUEST, EO1QuestID.IVORY_PRINCESS_DREAM_I,
	              quest_completion_requirements=[CanDefeatEncounter([EO1Enemies.DESOULER, EO1Enemies.DESOULER]), CanDefeatEncounter([EO1Enemies.SICKWOOD, EO1Enemies.SICKWOOD]), CanDefeatEncounter([EO1Enemies.KINGDILE, EO1Enemies.KINGDILE, EO1Enemies.KINGDILE])]), # TODO They are actually all one by one.
    QuestData(EO1QuestID.SCAVENGING_FOR_IAN_II, 4053, "Scavenging for Ian II", 14, -1, 3, 0x854,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.BUG_NEST, EO1MaterialID.STRAWBERRY, EO1MaterialID.SEA_BRANCH])]),
    QuestData(EO1QuestID.MONSTROUS_CODEX, 4054, "Monstrous Codex", 2, -1, 1, 0x863,
	              quest_completion_requirements=[CanFillXMonsterCodexEntries(10)]),
    QuestData(EO1QuestID.THE_DIAMOND_CHARM, 4055, "The diamond charm", 20, -1, 4, 0x874, QuestRequirement.QUEST, EO1QuestID.THE_IVORY_CHARM,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.CULLINAN])]),
    QuestData(EO1QuestID.GOURMANDS_REQUEST, 4056, "Gourmand's request", 30, -1, 6, 0x884,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.STIFF_HIDE, EO1MaterialID.STICKY_GOO, EO1MaterialID.GUM_THROAT, EO1MaterialID.TENDON, EO1MaterialID.DRYWALL])]),
    QuestData(EO1QuestID.VERSUS_THE_UNKNOWN, 4057, "Versus the unknown", 19, -1, 4, 0x8A3,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B18F_MAIN), CanDefeatEncounter([EO1Enemies.HEXTOAD]), CanDefeatEncounter([EO1Enemies.NIGHTOAD])]), # Has to defeat 3 Hextoad and 4 Nightoad.
    QuestData(EO1QuestID.THE_LEGENDARY_BIRD, 4058, "The legendary bird", 30, -1, 6, 0x8B4,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B30F_MAIN)]), # TODO Quest Item (Rare Meat) (Magic Down/Diamond/Black Gem/Shiny Gem)
    QuestData(EO1QuestID.OFFICIAL_BUSINESS_I, 4059, "Official business I", 12, -1, 3, 0x8D2,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B10F_EAST), CanReachRegion(EO1Regions.B10F_MAIN), CanReachRegion(EO1Regions.B11F_MAIN), CanDefeatEncounter([EO1Enemies.OMNIVORE])]), # TODO this quest is complex. Odd Powder
    QuestData(EO1QuestID.ITEM_COMPENDIUM, 4060, "Item Compendium", 28, -1, 6, 0x8E3,
	              quest_completion_requirements=[CanFillXItemCompendiumEntries(150)]),
    QuestData(EO1QuestID.OFFICIAL_BUSINESS_II, 4061, "Official business II", 30, -1, 6, 0x914,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B21F_EAST), CanDefeatEncounter([EO1Enemies.STEELWEB, EO1Enemies.STEELWEB, EO1Enemies.STEELWEB, EO1Enemies.STEELWEB, EO1Enemies.STEELWEB])]), # TODO validate elevator?
    QuestData(EO1QuestID.REVERSAL_OF_THE_POLES, 4062, "Reversal of the poles", 23, -1, 5, 0x924,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B18F_MAIN)]),
    QuestData(EO1QuestID.LOST_PET__REWARD_OFFERED, 4063, "Lost pet; reward offered", 29, -1, 6, 0x935,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B26F_MAIN), CanReachRegion(EO1Regions.B26F_SOUTH_WEST_SONGBIRD_ROOM), CanReachRegion(EO1Regions.B26F_SOUTH_EAST_SONGBIRD_ROOM), CanDefeatEncounter([EO1Enemies.GOUDARAT])]), # TODO Quest Item Gouda
    QuestData(EO1QuestID.OFFICIAL_BUSINESS_III, 4064, "Official business III", 30, -1, 6, 0x94D, QuestRequirement.QUEST, EO1QuestID.GOURMANDS_REQUEST,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B26F_NORTH), CanReachRegion(EO1Regions.B27F_MAIN), CanReachRegion(EO1Regions.B28F_DEATHPIT), CanReachRegion(EO1Regions.B29F_MAIN), CanReachRegion(EO1Regions.B30F_MAIN)]), # TODO Quest Item (Shiny Disc, Soft Glass, Copper Top, Token, Clam Tool), decide how to handle.
    QuestData(EO1QuestID.PHANTOM_OF_THE_FOREST, 4065, "Phantom of the forest", 21, 50, 5, 0x952,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B7F_SECRET_AREA), CanDefeatEncounter([EO1Enemies.ALRAUNE])]),
    QuestData(EO1QuestID.THE_BANDITS_TREASURE, 4066, "The bandit's treasure", 11, -1, 3, 0x963, QuestRequirement.KEY_ITEM, EO1ItemID.CLEAR_KEY,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B3F_SECRET_AREA), CanDefeatEncounter([EO1Enemies.GOLEM])]),
    QuestData(EO1QuestID.CALL_OF_THE_WYVERN, 4067, "Call of the Wyvern", -1, -1, 6, 0x972, QuestRequirement.BEAT_STORY,
	              quest_completion_requirements=[CanObtainMaterial([EO1MaterialID.TOUGH_FANG])]),
    QuestData(EO1QuestID.THE_DREAD_WYRM, 4068, "The dread Wyrm", -1, -1, 6, 0x983, QuestRequirement.QUEST, EO1QuestID.CALL_OF_THE_WYVERN,
	              quest_completion_requirements=[CanDefeatEncounter([EO1Enemies.WYRM])]),
    QuestData(EO1QuestID.PROOF_OF_HEROISM, 4069, "Proof of heroism", -1, -1, 6, 0x992, QuestRequirement.BEAT_STORY,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B15F_COTRANGL_ROOM)]), # TODO Quest Item Frozen Arm
    QuestData(EO1QuestID.THE_AZURE_COLOSSUS, 4070, "The azure colossus", -1, -1, 6, 0x9A3, QuestRequirement.QUEST, EO1QuestID.PROOF_OF_HEROISM,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B15F_DRAKE_ROOM), CanDefeatEncounter([EO1Enemies.DRAKE])]),
    QuestData(EO1QuestID.REMNANTS_OF_AN_AGE_PAST, 4071, "Remnants of an age past", -1, -1, 6, 0x9B7, QuestRequirement.BEAT_STORY,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B21F_SOUTH_WEST), CanReachRegion(EO1Regions.B22F_SOUTH_AREA_EAST), CanReachRegion(EO1Regions.B23F_MAIN), CanReachRegion(EO1Regions.B24F_NORTH), CanReachRegion(EO1Regions.B24F_MAIN)]), # TODO Quest Item Ankh A, B, C, D, E
    QuestData(EO1QuestID.AWAKENING_THE_SERPENT, 4072, "Awakening the serpent", -1, -1, 6, 0x9C3, QuestRequirement.QUEST, EO1QuestID.REMNANTS_OF_AN_AGE_PAST,
	              quest_completion_requirements=[CanReachRegion(EO1Regions.B21F_SOUTH_WEST), CanReachRegion(EO1Regions.B25F_ETREANT_ROOM), CanDefeatEncounter([EO1Enemies.DRAGON])]),
]

QUEST_DATA_BY_QUEST_ID: dict[int, QuestData] = {quest.quest_id: quest for quest in ALL_QUEST_DATA}
QUEST_DATA_BY_LOCATION_ID: dict[int, QuestData] = {quest.location_id: quest for quest in ALL_QUEST_DATA}