from dataclasses import dataclass
from enum import IntEnum

from .MaterialData import *
from .RegionData import *
#from .Generic import *

class EO1GatherType(IntEnum):
    CHOP = 0
    MINE = 1
    TAKE = 2

@dataclass(frozen=True)
class EO1GatheringSpotData:
    unique_id: int
    gather_type: EO1GatherType
    gathering_spot_id: int
    floor_number: int
    material_1_id: int
    material_2_id: int
    material_3_id: int
    material_1_probability: int
    material_2_probability: int
    material_3_probability: int
    region: str

GATHERING_SPOT_DATA: list[EO1GatheringSpotData] = [
    EO1GatheringSpotData(0, EO1GatherType.CHOP, 1, 0, EO1MaterialID.MUGWORT, EO1MaterialID.HARDWOOD, EO1MaterialID.RED_FRUIT, 50, 30, 10, EO1Regions.B1F_MAIN), # X Coord:10, Y Coord:16
    EO1GatheringSpotData(1, EO1GatherType.CHOP, 2, 4, EO1MaterialID.MUGWORT, EO1MaterialID.HARDWOOD, EO1MaterialID.RED_FRUIT, 50, 25, 15, EO1Regions.B5F_MAIN), # X Coord:24, Y Coord:13
    EO1GatheringSpotData(2, EO1GatherType.CHOP, 3, 5, EO1MaterialID.LIGHT_WOOD, EO1MaterialID.MUGWORT, EO1MaterialID.STARSEED, 50, 25, 15, EO1Regions.B6F_MAIN), # X Coord:9, Y Coord:11
    EO1GatheringSpotData(3, EO1GatherType.CHOP, 4, 9, EO1MaterialID.SCENT_WOOD, EO1MaterialID.STARSEED, EO1MaterialID.CROSS_SEED, 50, 25, 20, EO1Regions.B10F_EAST), # X Coord:22, Y Coord:4
    EO1GatheringSpotData(4, EO1GatherType.CHOP, 5, 12, EO1MaterialID.BUG_NEST, EO1MaterialID.STRAWBERRY, EO1MaterialID.SEA_BRANCH, 50, 25, 15, EO1Regions.B13F_NORTH), # X Coord:33, Y Coord:3
    EO1GatheringSpotData(5, EO1GatherType.CHOP, 6, 13, EO1MaterialID.STRAWBERRY, EO1MaterialID.BUG_NEST, EO1MaterialID.NARCISSUS, 50, 25, 20, EO1Regions.B14F_MAIN), # X Coord:2, Y Coord:18
    EO1GatheringSpotData(6, EO1GatherType.CHOP, 7, 17, EO1MaterialID.DRY_PEACH, EO1MaterialID.SAND_TWIG, EO1MaterialID.SAP_WINE, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:12, Y Coord:6
    EO1GatheringSpotData(7, EO1GatherType.CHOP, 8, 18, EO1MaterialID.DRY_PEACH, EO1MaterialID.SAND_TWIG, EO1MaterialID.SAP_WINE, 50, 25, 15, EO1Regions.B19F_MAIN), # X Coord:9, Y Coord:27
    EO1GatheringSpotData(8, EO1GatherType.CHOP, 9, 20, EO1MaterialID.DEATH_STEM, EO1MaterialID.NARCISSUS, EO1MaterialID.SHINY_SEED, 50, 30, 10, EO1Regions.B21F_EAST), # X Coord:28, Y Coord:4
    EO1GatheringSpotData(9, EO1GatherType.CHOP, 10, 23, EO1MaterialID.SHINY_VINE, EO1MaterialID.NARCISSUS, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B24F_MAIN), # X Coord:26, Y Coord:26
    EO1GatheringSpotData(10, EO1GatherType.CHOP, 11, 25, EO1MaterialID.SAP_WINE, EO1MaterialID.LIFE_HONEY, EO1MaterialID.MOSCHINO, 50, 25, 15, EO1Regions.B26F_MAIN), # X Coord:33, Y Coord:3
    EO1GatheringSpotData(11, EO1GatherType.CHOP, 12, 27, EO1MaterialID.NARCISSUS, EO1MaterialID.LIFE_HONEY, EO1MaterialID.MOSCHINO, 50, 25, 20, EO1Regions.B28F_DEATHPIT), # X Coord:8, Y Coord:19
    EO1GatheringSpotData(12, EO1GatherType.CHOP, 13, 0, EO1MaterialID.MUGWORT, EO1MaterialID.HARDWOOD, EO1MaterialID.RED_FRUIT, 50, 25, 15, EO1Regions.B1F_MAIN), # X Coord:2, Y Coord:16
    EO1GatheringSpotData(13, EO1GatherType.CHOP, 14, 4, EO1MaterialID.HARDWOOD, EO1MaterialID.MUGWORT, EO1MaterialID.RED_FRUIT, 50, 25, 15, EO1Regions.B5F_MAIN), # X Coord:8, Y Coord:24
    EO1GatheringSpotData(14, EO1GatherType.CHOP, 15, 5, EO1MaterialID.SCENT_WOOD, EO1MaterialID.MUGWORT, EO1MaterialID.STARSEED, 50, 25, 15, EO1Regions.B6F_MAIN), # X Coord:30, Y Coord:14
    EO1GatheringSpotData(15, EO1GatherType.CHOP, 16, 9, EO1MaterialID.LIGHT_WOOD, EO1MaterialID.SCENT_WOOD, EO1MaterialID.STARSEED, 50, 25, 15, EO1Regions.B10F_EAST), # X Coord:24, Y Coord:12
    EO1GatheringSpotData(16, EO1GatherType.CHOP, 17, 12, EO1MaterialID.STRAWBERRY, EO1MaterialID.BUG_NEST, EO1MaterialID.SEA_BRANCH, 50, 25, 15, EO1Regions.B13F_NORTH), # X Coord:25, Y Coord:1
    EO1GatheringSpotData(17, EO1GatherType.CHOP, 18, 13, EO1MaterialID.BUG_NEST, EO1MaterialID.STRAWBERRY, EO1MaterialID.NARCISSUS, 50, 25, 15, EO1Regions.B14F_MAIN), # X Coord:33, Y Coord:9
    EO1GatheringSpotData(18, EO1GatherType.CHOP, 19, 17, EO1MaterialID.DRY_PEACH, EO1MaterialID.CROSS_SEED, EO1MaterialID.SAP_WINE, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:28, Y Coord:12
    EO1GatheringSpotData(19, EO1GatherType.CHOP, 20, 18, EO1MaterialID.SAND_TWIG, EO1MaterialID.CROSS_SEED, EO1MaterialID.SAP_WINE, 50, 25, 15, EO1Regions.B19F_MAIN), # X Coord:24, Y Coord:1
    EO1GatheringSpotData(20, EO1GatherType.CHOP, 21, 21, EO1MaterialID.DEATH_STEM, EO1MaterialID.SHINY_VINE, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B22F_MAIN), # X Coord:24, Y Coord:12
    EO1GatheringSpotData(21, EO1GatherType.CHOP, 22, 22, EO1MaterialID.SHINY_VINE, EO1MaterialID.DEATH_STEM, EO1MaterialID.SHINY_SEED, 50, 25, 20, EO1Regions.B23F_EAST_ELEVATOR), # X Coord:25, Y Coord:15
    EO1GatheringSpotData(22, EO1GatherType.CHOP, 23, 25, EO1MaterialID.LIFE_HONEY, EO1MaterialID.SAP_WINE, EO1MaterialID.MOSCHINO, 50, 25, 20, EO1Regions.B26F_MAIN), # X Coord:14, Y Coord:26
    EO1GatheringSpotData(23, EO1GatherType.CHOP, 24, 27, EO1MaterialID.NARCISSUS, EO1MaterialID.SAP_WINE, EO1MaterialID.ARMROOT, 50, 25, 10, EO1Regions.B28F_DEATHPIT), # X Coord:31, Y Coord:27
    EO1GatheringSpotData(24, EO1GatherType.MINE, 1, 3, EO1MaterialID.PYROXENE, EO1MaterialID.METAL_HORN, EO1MaterialID.WHITESTONE, 50, 25, 15, EO1Regions.B4F_MAIN), # X Coord:2, Y Coord:7
    EO1GatheringSpotData(25, EO1GatherType.MINE, 2, 4, EO1MaterialID.PYROXENE, EO1MaterialID.METAL_HORN, EO1MaterialID.WHITESTONE, 50, 25, 15, EO1Regions.B5F_MAIN), # X Coord:24, Y Coord:17
    EO1GatheringSpotData(26, EO1GatherType.MINE, 3, 5, EO1MaterialID.SCRAP_IRON, EO1MaterialID.WHITESTONE, EO1MaterialID.THIN_SHELL, 50, 25, 20, EO1Regions.B6F_MAIN), # X Coord:10, Y Coord:18
    EO1GatheringSpotData(27, EO1GatherType.MINE, 4, 8, EO1MaterialID.SCRAP_IRON, EO1MaterialID.FOSSIL, EO1MaterialID.THIN_SHELL, 50, 25, 15, EO1Regions.B9F_NORTH_WEST), # X Coord:10, Y Coord:11
    EO1GatheringSpotData(28, EO1GatherType.MINE, 5, 9, EO1MaterialID.SCRAP_IRON, EO1MaterialID.FOSSIL, EO1MaterialID.THIN_SHELL, 50, 25, 15, EO1Regions.B10F_MAIN), #TODO ASSASSIN? # X Coord:8, Y Coord:21
    EO1GatheringSpotData(29, EO1GatherType.MINE, 6, 10, EO1MaterialID.ROCK_CORAL, EO1MaterialID.CRAB_LEG, EO1MaterialID.CORUNDUM, 50, 25, 15, EO1Regions.B11F_MAIN), # X Coord:28, Y Coord:1
    EO1GatheringSpotData(30, EO1GatherType.MINE, 7, 15, EO1MaterialID.STEEL_CHIP, EO1MaterialID.HARD_SHARD, EO1MaterialID.CULLINAN, 50, 25, 15, EO1Regions.B16F_MAIN), # X Coord:16, Y Coord:3
    EO1GatheringSpotData(31, EO1GatherType.MINE, 8, 17, EO1MaterialID.HARD_SHARD, EO1MaterialID.STEEL_CHIP, EO1MaterialID.CULLINAN, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:28, Y Coord:22
    EO1GatheringSpotData(32, EO1GatherType.MINE, 9, 20, EO1MaterialID.CRYSTWALL, EO1MaterialID.DRYWALL, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B21F_MAIN), # X Coord:6, Y Coord:4
    EO1GatheringSpotData(33, EO1GatherType.MINE, 10, 22, EO1MaterialID.CRYSTWALL, EO1MaterialID.DRYWALL, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B23F_MAIN), # X Coord:4, Y Coord:7
    EO1GatheringSpotData(34, EO1GatherType.MINE, 11, 23, EO1MaterialID.CRYSTWALL, EO1MaterialID.DRYWALL, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B24F_NORTH), # X Coord:25, Y Coord:4
    EO1GatheringSpotData(35, EO1GatherType.MINE, 12, 25, EO1MaterialID.NARCISSUS, EO1MaterialID.SHINY_SEED, EO1MaterialID.TRI_COLOR, 50, 25, 15, EO1Regions.B26F_MAIN), # X Coord:33, Y Coord:4
    EO1GatheringSpotData(36, EO1GatherType.MINE, 13, 27, EO1MaterialID.CROSS_SEED, EO1MaterialID.NARCISSUS, EO1MaterialID.LEGROOT, 50, 25, 10, EO1Regions.B28F_DEATHPIT), # X Coord:8, Y Coord:20
    EO1GatheringSpotData(37, EO1GatherType.MINE, 14, 3, EO1MaterialID.METAL_HORN, EO1MaterialID.PYROXENE, EO1MaterialID.WHITESTONE, 50, 25, 15, EO1Regions.B4F_MAIN), # X Coord:1, Y Coord:22
    EO1GatheringSpotData(38, EO1GatherType.MINE, 15, 4, EO1MaterialID.METAL_HORN, EO1MaterialID.PYROXENE, EO1MaterialID.WHITESTONE, 50, 25, 15, EO1Regions.B5F_MAIN), # X Coord:17, Y Coord:1
    EO1GatheringSpotData(39, EO1GatherType.MINE, 16, 5, EO1MaterialID.FOSSIL, EO1MaterialID.SCRAP_IRON, EO1MaterialID.THIN_SHELL, 50, 25, 15, EO1Regions.B6F_MAIN), # X Coord:30, Y Coord:1
    EO1GatheringSpotData(40, EO1GatherType.MINE, 17, 8, EO1MaterialID.FOSSIL, EO1MaterialID.WHITESTONE, EO1MaterialID.THIN_SHELL, 50, 25, 15, EO1Regions.B9F_NORTH_WEST), # X Coord:16, Y Coord:12
    EO1GatheringSpotData(41, EO1GatherType.MINE, 18, 9, EO1MaterialID.FOSSIL, EO1MaterialID.SCRAP_IRON, EO1MaterialID.THIN_SHELL, 50, 25, 15, EO1Regions.B10F_MAIN), # X Coord:8, Y Coord:10
    EO1GatheringSpotData(42, EO1GatherType.MINE, 19, 10, EO1MaterialID.CRAB_LEG, EO1MaterialID.ROCK_CORAL, EO1MaterialID.CORUNDUM, 50, 25, 15, EO1Regions.B11F_MAIN), # X Coord:1, Y Coord:14
    EO1GatheringSpotData(43, EO1GatherType.MINE, 20, 15, EO1MaterialID.HARD_SHARD, EO1MaterialID.STEEL_CHIP, EO1MaterialID.CULLINAN, 50, 25, 20, EO1Regions.B16F_SECRET_AREA), # X Coord:4, Y Coord:11
    EO1GatheringSpotData(44, EO1GatherType.MINE, 21, 17, EO1MaterialID.STEEL_CHIP, EO1MaterialID.HARD_SHARD, EO1MaterialID.CULLINAN, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:12, Y Coord:16
    EO1GatheringSpotData(45, EO1GatherType.MINE, 22, 21, EO1MaterialID.DRYWALL, EO1MaterialID.CRYSTWALL, EO1MaterialID.SHINY_SEED, 50, 25, 20, EO1Regions.B22F_SOUTH_AREA_WEST), # TODO maybe need to defeat Desouler? # X Coord:12, Y Coord:14
    EO1GatheringSpotData(46, EO1GatherType.MINE, 23, 22, EO1MaterialID.DRYWALL, EO1MaterialID.CRYSTWALL, EO1MaterialID.SHINY_SEED, 50, 25, 15, EO1Regions.B23F_MAIN), #TODO Maybe need to escape # X Coord:27, Y Coord:17
    EO1GatheringSpotData(47, EO1GatherType.MINE, 24, 23, EO1MaterialID.DRYWALL, EO1MaterialID.CRYSTWALL, EO1MaterialID.SHINY_SEED, 50, 25, 20, EO1Regions.B24F_MAIN), #TODO Probably need defeating Dinolich # X Coord:12, Y Coord:25
    EO1GatheringSpotData(48, EO1GatherType.MINE, 25, 25, EO1MaterialID.SHINY_SEED, EO1MaterialID.NARCISSUS, EO1MaterialID.TRI_COLOR, 50, 25, 25, EO1Regions.B26F_MAIN), # X Coord:31, Y Coord:19
    EO1GatheringSpotData(49, EO1GatherType.MINE, 26, 27, EO1MaterialID.SHINY_SEED, EO1MaterialID.CROSS_SEED, EO1MaterialID.TRI_COLOR, 50, 25, 15, EO1Regions.B28F_DEATHPIT), # X Coord:30, Y Coord:28
    EO1GatheringSpotData(50, EO1GatherType.TAKE, 1, 2, EO1MaterialID.TINY_PETAL, EO1MaterialID.AMBER_LUMP, EO1MaterialID.CRABAPPLE, 50, 25, 15, EO1Regions.B3F_MAIN), # X Coord:12, Y Coord:25
    EO1GatheringSpotData(51, EO1GatherType.TAKE, 2, 5, EO1MaterialID.MINT_LEAF, EO1MaterialID.CRABAPPLE, EO1MaterialID.CROSS_SEED, 50, 25, 15, EO1Regions.B6F_MAIN), # X Coord:3, Y Coord:4
    EO1GatheringSpotData(52, EO1GatherType.TAKE, 3, 7, EO1MaterialID.MINT_LEAF, EO1MaterialID.DYE_PETAL, EO1MaterialID.CROSS_SEED, 50, 25, 15, EO1Regions.B8F_MAIN), # X Coord:12, Y Coord:13
    EO1GatheringSpotData(53, EO1GatherType.TAKE, 4, 9, EO1MaterialID.MINT_LEAF, EO1MaterialID.CROSS_SEED, EO1MaterialID.TOXIC_BARB, 50, 25, 15, EO1Regions.B10F_EAST), #TODO BLOCKED BY MOA  # X Coord:19, Y Coord:4
    EO1GatheringSpotData(54, EO1GatherType.TAKE, 5, 12, EO1MaterialID.GLASS_EYE, EO1MaterialID.ANT_HONEY, EO1MaterialID.STAB_SHELL, 50, 25, 15, EO1Regions.B13F_NORTH), # X Coord:33, Y Coord:5
    EO1GatheringSpotData(55, EO1GatherType.TAKE, 6, 17, EO1MaterialID.CROSS_SEED, EO1MaterialID.SAND_CLOTH, EO1MaterialID.CORDYCEPS, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:31, Y Coord:3
    EO1GatheringSpotData(56, EO1GatherType.TAKE, 7, 19, EO1MaterialID.SAND_CLOTH, EO1MaterialID.CROSS_SEED, EO1MaterialID.CORDYCEPS, 50, 25, 15, EO1Regions.B20F_MAIN), # X Coord:29, Y Coord:11
    EO1GatheringSpotData(57, EO1GatherType.TAKE, 8, 20, EO1MaterialID.ANGEL_WING, EO1MaterialID.LIFE_HONEY, EO1MaterialID.GUM_STRING, 50, 25, 15, EO1Regions.B21F_SOUTH_EAST), # X Coord:28, Y Coord:25
    EO1GatheringSpotData(58, EO1GatherType.TAKE, 9, 23, EO1MaterialID.ANGEL_WING, EO1MaterialID.LIFE_HONEY, EO1MaterialID.GUM_STRING, 50, 25, 20, EO1Regions.B24F_NORTH), # X Coord:23, Y Coord:4
    EO1GatheringSpotData(59, EO1GatherType.TAKE, 10, 25, EO1MaterialID.CROSS_SEED, EO1MaterialID.CORDYCEPS, EO1MaterialID.AMBROSIA, 50, 25, 15, EO1Regions.B26F_MAIN), # X Coord:33, Y Coord:5
    EO1GatheringSpotData(60, EO1GatherType.TAKE, 11, 27, EO1MaterialID.CROSS_SEED, EO1MaterialID.AMBROSIA, EO1MaterialID.HEADROOT, 50, 25, 10, EO1Regions.B28F_DEATHPIT), # X Coord:9, Y Coord:20
    EO1GatheringSpotData(61, EO1GatherType.TAKE, 12, 2, EO1MaterialID.AMBER_LUMP, EO1MaterialID.TINY_PETAL, EO1MaterialID.CRABAPPLE, 50, 25, 15, EO1Regions.B3F_MAIN), # X Coord:16, Y Coord:19
    EO1GatheringSpotData(62, EO1GatherType.TAKE, 13, 5, EO1MaterialID.MINT_LEAF, EO1MaterialID.DYE_PETAL, EO1MaterialID.CROSS_SEED, 50, 25, 15, EO1Regions.B6F_MAIN), # X Coord:5, Y Coord:17
    EO1GatheringSpotData(63, EO1GatherType.TAKE, 14, 7, EO1MaterialID.CRABAPPLE, EO1MaterialID.MINT_LEAF, EO1MaterialID.CROSS_SEED, 50, 25, 15, EO1Regions.B8F_MAIN), # X Coord:18, Y Coord:5
    EO1GatheringSpotData(64, EO1GatherType.TAKE, 15, 9, EO1MaterialID.DYE_PETAL, EO1MaterialID.MINT_LEAF, EO1MaterialID.CROSS_SEED, 50, 25, 15, EO1Regions.B10F_EAST), # X Coord:12, Y Coord:14
    EO1GatheringSpotData(65, EO1GatherType.TAKE, 16, 12, EO1MaterialID.ANT_HONEY, EO1MaterialID.GLASS_EYE, EO1MaterialID.STAB_SHELL, 50, 25, 15, EO1Regions.B13F_NORTH), # X Coord:25, Y Coord:3
    EO1GatheringSpotData(66, EO1GatherType.TAKE, 17, 17, EO1MaterialID.SAND_CLOTH, EO1MaterialID.CROSS_SEED, EO1MaterialID.CORDYCEPS, 50, 25, 15, EO1Regions.B18F_MAIN), # X Coord:18, Y Coord:4
    EO1GatheringSpotData(67, EO1GatherType.TAKE, 18, 19, EO1MaterialID.SAND_CLOTH, EO1MaterialID.CROSS_SEED, EO1MaterialID.OLEANDER, 50, 25, 15, EO1Regions.B20F_NORTH_ROOM), # X Coord:14, Y Coord:4
    EO1GatheringSpotData(68, EO1GatherType.TAKE, 19, 20, EO1MaterialID.LIFE_HONEY, EO1MaterialID.ANGEL_WING, EO1MaterialID.GUM_STRING, 50, 25, 15, EO1Regions.B21F_SOUTH_WEST), #TODO Maybe mandatory Kingdile # X Coord:10, Y Coord:25
    EO1GatheringSpotData(69, EO1GatherType.TAKE, 20, 22, EO1MaterialID.LIFE_HONEY, EO1MaterialID.ANGEL_WING, EO1MaterialID.GUM_STRING, 50, 25, 15, EO1Regions.B23F_MAIN), #TODO maybe need to escape # X Coord:22, Y Coord:1
    EO1GatheringSpotData(70, EO1GatherType.TAKE, 21, 25, EO1MaterialID.CORDYCEPS, EO1MaterialID.CROSS_SEED, EO1MaterialID.AMBROSIA, 50, 25, 15, EO1Regions.B26F_MAIN), # X Coord:20, Y Coord:26
    EO1GatheringSpotData(71, EO1GatherType.TAKE, 22, 27, EO1MaterialID.CROSS_SEED, EO1MaterialID.CORDYCEPS, EO1MaterialID.AMBROSIA, 50, 25, 15, EO1Regions.B28F_DEATHPIT), # X Coord:31, Y Coord:28
]

GATHERING_SPOT_BY_UNIQUE_ID: dict[int, EO1GatheringSpotData] = {
    gathering_spot_data.unique_id:gathering_spot_data
    for gathering_spot_data in GATHERING_SPOT_DATA
}

#def validate_all():
#    for gathering_spot in GATHERING_SPOT_DATA:
#        region_data = ALL_REGION_DATA_BY_NAME[gathering_spot.region]
#        if gathering_spot.floor_number + 1 != region_data.floor_number:
#            raise Exception(f"Mismatching floor numbers for gathering spot {gathering_spot.unique_id}")
#validate_all()