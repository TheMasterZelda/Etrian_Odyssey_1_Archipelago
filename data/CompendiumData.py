from dataclasses import dataclass
from enum import IntEnum

from .MaterialData import *
from .EnemyData import *
from .GatheringSpotData import *

class CompendiumSource(IntEnum):
    MONSTER = 0
    GATHERING = 1
    BOTH = 2

@dataclass
class CompendiumData:
    item_id: int
    material_name: str
    location_id: int
    source: CompendiumSource
    conditional_drop: bool = False

    def get_full_name(self) -> str:
        return f"Compendium entry #??: {self.material_name}"

COMPENDIUM_TABLE: list[CompendiumData] = [
    CompendiumData(EO1MaterialID.SMALL_FANG, "Small Fang", 3000, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SOFT_HIDE, "Soft Hide", 3001, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BEAST_BONE, "Beast Bone", 3002, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HARD_SHELL, "Hard Shell", 3003, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BUG_WING, "Bug Wing", 3004, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TINY_PETAL, "Tiny Petal", 3005, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.INSECT_EYE, "Insect Eye", 3006, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.HARE_TAIL, "Hare Tail", 3007, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HORN, "Horn", 3008, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HARDWOOD, "Hardwood", 3009, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.VINE, "Vine", 3010, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.CHARCOAL, "Charcoal", 3011, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.GUM_HIDE, "Gum Hide", 3012, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.THORN, "Thorn", 3013, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.METAL_HORN, "Metal Horn", 3014, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STIFF_HIDE, "Stiff Hide", 3015, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.AMBER_LUMP, "Amber Lump", 3016, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.CRABAPPLE, "Crabapple", 3017, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.MUGWORT, "Mugwort", 3018, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.RED_FRUIT, "Red Fruit", 3019, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.WHITESTONE, "Whitestone", 3020, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.PYROXENE, "Pyroxene", 3021, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.GOLEM_ROCK, "Golem Rock", 3022, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.LARGE_FANG, "Large Fang", 3023, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HUGE_FANG, "Huge Fang", 3024, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.WHITE_HIDE, "White Hide", 3025, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SCYTHE, "Scythe", 3026, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STICKY_GOO, "Sticky Goo", 3027, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STEEL_LUMP, "Steel Lump", 3028, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STINGER, "Stinger", 3029, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STICKY_WEB, "Sticky Web", 3030, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BENT_CLAW, "Bent Claw", 3031, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.LIGHT_WOOD, "Light Wood", 3032, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.DYE_PETAL, "Dye Petal", 3033, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STARSEED, "Starseed", 3034, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.SCENT_WOOD, "Scent Wood", 3035, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.GUM_VINE, "Gum Vine", 3036, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FEATHER, "Feather", 3037, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TAILBONE, "Tailbone", 3038, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.CARMINITE, "Carminite", 3039, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.IRON_SHELL, "Iron Shell", 3040, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.THICK_LEAF, "Thick Leaf", 3041, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BIRD_TALON, "Bird Talon", 3042, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TIGER_FANG, "Tiger Fang", 3043, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TIGER_FUR, "Tiger Fur", 3044, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.MINT_LEAF, "Mint Leaf", 3045, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SCRAP_IRON, "Scrap Iron", 3046, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.FOSSIL, "Fossil", 3047, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.BEAR_FUR, "Bear Fur", 3048, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BIRD_LIMB, "Bird Limb", 3049, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.THIN_SHELL, "Thin Shell", 3050, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.TOXIC_BARB, "Toxic Barb", 3051, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.SHARP_HORN, "Sharp Horn", 3052, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TOUGH_WING, "Tough Wing", 3053, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.TOUGH_FANG, "Tough Fang", 3054, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.GREAT_TUSK, "Great Tusk", 3055, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GUM_THROAT, "Gum Throat", 3056, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ROCK_CORAL, "Rock Coral", 3057, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.ELASTIC, "Elastic", 3058, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GLASS_EYE, "Glass Eye", 3059, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STEEL_BONE, "Steel Bone", 3060, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BONE_SHARD, "Bone Shard", 3061, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.CARAPACE, "Carapace", 3062, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BUG_NEST, "Bug Nest", 3063, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.BAT_WING, "Bat Wing", 3064, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SHINY_GOO, "Shiny Goo", 3065, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SHRED_NAIL, "Shred Nail", 3066, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_HIDE, "Red Hide", 3067, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BLOOD_FANG, "Blood Fang", 3068, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FISH_SCALE, "Fish Scale", 3069, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FISH_FIN, "Fish Fin", 3070, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.CRAB_LEG, "Crab Leg", 3071, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.ANT_HONEY, "Ant Honey", 3072, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STAB_SHELL, "Stab Shell", 3073, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.STRAWBERRY, "Strawberry", 3074, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SEA_BRANCH, "Sea Branch", 3075, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.CORUNDUM, "Corundum", 3076, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.RED_BLADE, "Red Blade", 3077, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DEATH_CLAW, "Death Claw", 3078, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HUGE_FIN, "Huge Fin", 3079, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.N100_SHELL, "100 Shell", 3080, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GATOR_SKIN, "Gator Skin", 3081, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HEATED_FUR, "Heated Fur", 3082, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FIRE_TAIL, "Fire Tail", 3083, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.WHITE_SKIN, "White Skin", 3084, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.WHITE_FANG, "White Fang", 3085, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SHINY_HORN, "Shiny Horn", 3086, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.MUSK, "Musk", 3087, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BROKEN_EYE, "Broken Eye", 3088, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.SILVER_EYE, "Silver Eye", 3089, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.NYX_SCYTHE, "Nyx Scythe", 3090, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TENDON, "Tendon", 3091, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DRIED_VINE, "Dried Vine", 3092, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.PURE_ROOT, "Pure Root", 3093, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HARD_SHARD, "Hard Shard", 3094, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.INK_STICK, "Ink Stick", 3095, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SAND_CLOTH, "Sand Cloth", 3096, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.SAND_TWIG, "Sand Twig", 3097, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.FAIRY_WING, "Fairy Wing", 3098, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FAIRY_SAP, "Fairy Sap", 3099, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_PLUME, "Red Plume", 3100, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_BEAK, "Red Beak", 3101, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DRY_PEACH, "Dry Peach", 3102, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.THROB_VINE, "Throb Vine", 3103, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_STRING, "Red String", 3104, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_THREAD, "Red Thread", 3105, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.OLEANDER, "Oleander", 3106, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STEEL_CLAW, "Steel Claw", 3107, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STEEL_CHIP, "Steel Chip", 3108, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.CULLINAN, "Cullinan", 3109, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.CORDYCEPS, "Cordyceps", 3110, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SAP_WINE, "Sap Wine", 3111, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SPACE_NAIL, "Space Nail", 3112, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.TINY_TOOTH, "Tiny Tooth", 3113, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DEMON_FUR, "Demon Fur", 3114, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.REX_THROAT, "Rex Throat", 3115, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GEM_CORE, "Gem Core", 3116, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GUM_THREAD, "Gum Thread", 3117, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_FUR, "Red Fur", 3118, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_BLOOD, "Red Blood", 3119, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GOLD_SHELL, "Gold Shell", 3120, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BLUE_BLOOD, "Blue Blood", 3121, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DEATH_STEM, "Death Stem", 3122, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.GOLD_FUR, "Gold Fur", 3123, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GOLD_TUSK, "Gold Tusk", 3124, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GOLD_HORN, "Gold Horn", 3125, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SPACE_HUSK, "Space Husk", 3126, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SPACE_CLAW, "Space Claw", 3127, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ANGEL_WING, "Angel Wing", 3128, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.LIFE_HONEY, "Life Honey", 3129, CompendiumSource.BOTH),
    CompendiumData(EO1MaterialID.STERNUM, "Sternum", 3130, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.CURSE_TUSK, "Curse Tusk", 3131, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ROYAL_HIDE, "Royal Hide", 3132, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SHROUD, "Shroud", 3133, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RED_ORE, "Red Ore", 3134, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.AMBROSIA, "Ambrosia", 3135, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.TRI_COLOR, "Tri-Color", 3136, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.HEADROOT, "Headroot", 3137, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.ARMROOT, "Armroot", 3138, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.LEGROOT, "Legroot", 3139, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.GUM_STRING, "Gum String", 3140, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SHINY_VINE, "Shiny Vine", 3141, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.SHINY_SEED, "Shiny Seed", 3142, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.DRYWALL, "Drywall", 3143, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.CRYSTWALL, "Crystwall", 3144, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.AZURE_ORE, "Azure Ore", 3145, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.EVIL_SHELL, "Evil Shell", 3146, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.EVIL_SCALE, "Evil Scale", 3147, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.EVIL_PLUME, "Evil Plume", 3148, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.EVIL_CREST, "Evil Crest", 3149, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.N1000_SHELL, "1000 Shell", 3150, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.OLD_SHELL, "Old Shell", 3151, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GEM_SCALE, "Gem Scale", 3152, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BLACK_ROOT, "Black Root", 3153, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.GEM_PLUME, "Gem Plume", 3154, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HEX_MARROW, "Hex Marrow", 3155, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.GOLD_PLUME, "Gold Plume", 3156, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HELL_WING, "Hell Wing", 3157, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.VELVET, "Velvet", 3158, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HOLED_LIMB, "Holed Limb", 3159, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RUBY_SKULL, "Ruby Skull", 3160, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.RUBY_BONE, "Ruby Bone", 3161, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.HEX_CHAIN, "Hex Chain", 3162, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.SWORD_RIB, "Sword Rib", 3163, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.FLAME_SKIN, "Flame Skin", 3164, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FROST_SKIN, "Frost Skin", 3165, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.VOLT_SKIN, "Volt Skin", 3166, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.VOLT_CORE, "Volt Core", 3167, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FIRE_SCALE, "Fire Scale", 3168, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FIRE_FANG, "Fire Fang", 3169, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.STATUE_ARM, "Statue Arm", 3170, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BEAST_EYE, "Beast Eye", 3171, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.FROST_BONE, "Frost Bone", 3172, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.DEMON_CORE, "Demon Core", 3173, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.EBON_PLUME, "Ebon Plume", 3174, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ICE_SPINE, "Ice Spine", 3175, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.BARBEL, "Barbel", 3176, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ROYAL_VINE, "Royal Vine", 3177, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.HARVESTER, "Harvester", 3178, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.ROYAL_MANE, "Royal Mane", 3179, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ANTS_JAW, "Ant's Jaw", 3180, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ICE_SCALE, "Ice Scale", 3181, CompendiumSource.MONSTER),
    #CompendiumData(EO1MaterialID.WINE_WHIP, "Wine Whip", 3182, CompendiumSource.MONSTER, conditional_drop=True),
    #CompendiumData(EO1MaterialID.ROSE_WHIP, "Rose Whip", 3183, CompendiumSource.MONSTER, conditional_drop=True),
    CompendiumData(EO1MaterialID.TOXIC_HAND, "Toxic Hand", 3184, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.VOLT_SCALE, "Volt Scale", 3185, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.YELLOW_ORE, "Yellow Ore", 3186, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.BUG_SCALE, "Bug Scale", 3187, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.COLD_SCALE, "Cold Scale", 3188, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.ODD_FRUIT, "Odd Fruit", 3189, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.CROSS_SEED, "Cross Seed", 3190, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.NARCISSUS, "Narcissus", 3191, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.MOSCHINO, "Moschino", 3192, CompendiumSource.GATHERING),
    CompendiumData(EO1MaterialID.S_LEAF, "S Leaf", 3193, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.M_LEAF, "M Leaf", 3194, CompendiumSource.MONSTER),
    CompendiumData(EO1MaterialID.L_LEAF, "L Leaf", 3195, CompendiumSource.MONSTER),
]

COMPENDIUM_BY_ITEM_ID: dict[int, CompendiumData] = {compendium_entry.item_id:compendium_entry for compendium_entry in COMPENDIUM_TABLE}
COMPENDIUM_BY_LOCATION_ID: dict[int, CompendiumData] = {compendium_entry.location_id:compendium_entry for compendium_entry in COMPENDIUM_TABLE}

def generate_enemy_by_drop_id_dictionary() -> dict[int, set[int]]:
    enemy_by_drop_id: dict[int, set[int]] = {}

    def add_entry(enemy_id: int, item_drop_id: int):
        if item_drop_id == 0:
            return

        if item_drop_id not in enemy_by_drop_id:
            enemy_by_drop_id[item_drop_id] = set()

        enemy_by_drop_id[item_drop_id].add(enemy_id)

    for enemy_data in ALL_ENEMIES:
        add_entry(enemy_data.enemy_id, enemy_data.item_drop_1)
        add_entry(enemy_data.enemy_id, enemy_data.item_drop_2)
        add_entry(enemy_data.enemy_id, enemy_data.item_drop_3)

    return enemy_by_drop_id

def generate_gathering_spot_by_item_id_dictionary() -> dict[int, set[int]]:
    gathering_spot_by_item_id: dict[int, set[int]] = {}

    def add_entry(gathering_spot: EO1GatheringSpotData, item_id: int):
        if item_id == 0:
            return

        if item_id not in gathering_spot_by_item_id:
            gathering_spot_by_item_id[item_id] = set()

        gathering_spot_by_item_id[item_id].add(gathering_spot.unique_id)

    for gathering_spot_data in GATHERING_SPOT_DATA:
        add_entry(gathering_spot_data, gathering_spot_data.material_1_id)
        add_entry(gathering_spot_data, gathering_spot_data.material_2_id)
        add_entry(gathering_spot_data, gathering_spot_data.material_3_id)

    return gathering_spot_by_item_id

ENEMY_BY_DROP_ID: dict[int, set[int]] = generate_enemy_by_drop_id_dictionary()
GATHERING_SPOT_BY_ITEM_ID: dict[int, set[int]] = generate_gathering_spot_by_item_id_dictionary()
