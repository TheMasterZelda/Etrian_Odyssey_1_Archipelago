from typing import TYPE_CHECKING, NamedTuple, Optional
from dataclasses import dataclass, field
#from .EncounterGroupData import ENCOUNTER_GROUP_BY_ID
#from .EncounterData import ENCOUNTER_BY_ID
from .EnemyData import EO1Enemies
from .Entrances import *
from .Events import *

class EO1Regions:
    ETRIA = "Etria"
    SHILLEKA = "Shilleka's Goods"
    PUB = "Golden Deer Pub"
    RADHA_HALL = "Radha Hall"
    # todo add sub region to Radha Hall for clarity.
    B1F_MAIN = "B1F Main"
    B1F_CLEAR_CRYSTAL_ROOM = "B1F Clear Crystal Room"
    B1F_VIOLET_CRYSTAL_ROOM = "B1F Violet Crystal Room"
    B1F_SECRET_AREA = "B1F Secret Area"
    # B1F_NORTH - if we ever restrict the map?
    B2F_MAIN = "B2F Main"
    B2F_SOUTH = "B2F South"
    B2F_CLEAR_CRYSTAL_ROOM = "B2F Clear Crystal Room"
    B3F_MAIN = "B3F Main"
    # Split B3F in 2 if we restrict main missions?
    B3F_SECRET_AREA = "B3F Secret Area"
    B4F_MAIN = "B4F Main"
    B4F_SECRET_AREA = "B4F Secret Area"
    B5F_MAIN = "B5F Main"
    B5F_FENRIR_LAIR = "B5F Fenrir's Lair"
    B5F_SECRET_AREA = "B5F Secret Area"
    B6F_MAIN = "B6F Main"
    B6F_CLEAR_CRYSTAL_ROOM = "B6F Clear Crystal Room"
    B7F_MAIN = "B7F Main"
    B7F_SECRET_AREA = "B7F Secret Area"
    B8F_MAIN = "B8F Main"
    B8F_EAST_DRAGON_NEST_AREA = "B8F East Dragon Nest Area"
    B8F_WEST_DRAGON_NEST_AREA = "B8F West Dragon Nest Area"
    B8F_EAST = "B8F East"
    B8F_SOUTH = "B8F South"
    B8F_WEST = "B8F West"
    B8F_VIOLET_CRYSTAL_ROOM = "B8F Violet Crystal Room"
    B8F_SECRET_AREA = "B8F Secret Area"
    B9F_EAST = "B9F East"
    B9F_NORTH_WEST = "B9F North West"
    B9F_SOUTH = "B9F South"
    B9F_SOUTH_WEST = "B9F South West"
    B9F_SECRET_AREA = "B9F Secret Area"
    B9F_CLEAR_CRYSTAL_ROOM = "B9F Clear Crystal Room"
    B10F_MAIN = "B10F Main"
    B10F_EAST = "B10F East"
    B10F_CERNUNOS_LAIR = "B10F Cernunos Lair"
    B10F_VIOLET_CRYSTAL_ROOM = "B10F Violet Crystal Room"
    B10F_SECRET_AREA = "B10F Secret Area"
    B11F_MAIN = "B11F Main"
    B11F_PITFALL = "B11F Pitfall"
    B11F_SECRET_AREA = "B11F Secret Area"
    B12F_MAIN = "B12F Main"
    B12F_SOUTH = "B12F South"
    B12F_ANT_MAZE = "B12F Ant Maze" # Include all areas after the first respawning Ants.
    B12F_ANT_NEST = "B12F Ant Nest"
    B13F_MAIN = "B13F Main"
    B13F_NORTH = "B13F North"
    B14F_MAIN = "B14F Main"
    B15F_MAIN = "B15F Main"
    B15F_COTRANGL_ROOM = "B15F Cotrangl Room"
    B15F_SECRET_AREA = "B15F Secret Area"
    B16F_MAIN = "B16F Main"
    B16F_SECRET_AREA = "B16F Secret Area"
    B16F_EAST_SECRET_AREA = "B16F East Secret Area"
    B17F_MAIN = "B17F Main"
    #B17F_SECRET_AREA = "B17F Secret Area"
    B17F_SECRET_AREA_NORTH_EAST = "B17F Secret Area North East"
    B17F_SECRET_AREA_NORTH = "B17F Secret Area North"
    B17F_SECRET_AREA_SOUTH_EAST = "B17F Secret Area South East"
    B17F_SECRET_AREA_WEST = "B17F Secret Area West"
    B18F_MAIN = "B18F Main"
    B18F_WEST = "B18F West"
    B19F_MAIN = "B19F Main"
    B19F_STAIRS_ROOM = "B19F Stairs Room"
    B20F_MAIN = "B20F Main"
    B20F_NORTH_ROOM = "B20F North Room"
    B20F_VIOLET_CRYSTAL_ROOM = "B20F Violet Crystal Room"

    # This probably needs to be redone, especially to account for unavoidable fights.
    B21F_MAIN = "B21F Main" # West area.
    B21F_EAST = "B21F East"
    B21F_SOUTH_EAST = "B21F South East"
    B21F_SOUTH_WEST = "B21F South West"
    B22F_MAIN = "B22F Main" # North area
    B22F_NORTH_WEST_DEAD_END = "B22F North West Dead End"
    B22F_SOUTH_WEST_DEAD_END = "B22F South West Dead End"
    B22F_SOUTH_EAST_DEAD_END = "B22F South East Dead End"
    B22F_SOUTH_AREA_WEST = "B22F South Area West"
    B22F_SOUTH_AREA_EAST = "B22F South Area East"
    B22F_WEST_ELEVATOR = "B22F West Elevator"
    B23F_MAIN = "B23F Main"
    B23F_SOUTH_WEST = "B23F South West"
    B23F_SOUTH_EAST = "B23F South East"
    B23F_NORTH_EAST = "B23F North East"
    B23F_EAST_ELEVATOR = "B23F East Elevator"
    B24F_MAIN = "B24F Main"
    B24F_NORTH = "B24F North"
    B24F_SOUTH_WEST = "B24F South West"
    B25F_MAIN = "B25F Main"
    B25F_WEST_ELEVATOR = "B25F West Elevator"
    B25F_ETREANT_ROOM = "B25F Etreant Room"

    # Stratum 6 is a very rough implementation for now.
    B26F_MAIN = "B26F Main"
    B27F_MAIN = "B27F Main"
    B27F_NORTH = "B27F North"
    B28F_DEATHPIT = "B28F Death Pit"
    B28F_MAIN = "B28F Main"
    B29F_MAIN = "B29F Main"
    B30F_MAIN = "B30F Main"

TOWN: set[str] = {
    EO1Regions.ETRIA,
    EO1Regions.SHILLEKA,
    EO1Regions.PUB,
    EO1Regions.RADHA_HALL
}

STRATUM_1: set[str] = {
    EO1Regions.B1F_MAIN,
    EO1Regions.B1F_CLEAR_CRYSTAL_ROOM,
    EO1Regions.B1F_VIOLET_CRYSTAL_ROOM,
    EO1Regions.B1F_SECRET_AREA,
    EO1Regions.B2F_MAIN,
    EO1Regions.B2F_CLEAR_CRYSTAL_ROOM,
    EO1Regions.B3F_MAIN,
    EO1Regions.B3F_SECRET_AREA,
    EO1Regions.B4F_MAIN,
    EO1Regions.B4F_SECRET_AREA,
    EO1Regions.B5F_MAIN,
    EO1Regions.B5F_FENRIR_LAIR,
    EO1Regions.B5F_SECRET_AREA
}
STRATUM_2: set[str] = {
    EO1Regions.B6F_MAIN,
    EO1Regions.B6F_CLEAR_CRYSTAL_ROOM,
    EO1Regions.B7F_MAIN,
    EO1Regions.B7F_SECRET_AREA,
    EO1Regions.B8F_MAIN,
    EO1Regions.B8F_EAST_DRAGON_NEST_AREA,
    EO1Regions.B8F_WEST_DRAGON_NEST_AREA,
    EO1Regions.B8F_EAST,
    EO1Regions.B8F_SOUTH,
    EO1Regions.B8F_WEST,
    EO1Regions.B8F_VIOLET_CRYSTAL_ROOM,
    EO1Regions.B8F_SECRET_AREA,
    EO1Regions.B9F_EAST,
    EO1Regions.B9F_NORTH_WEST,
    EO1Regions.B9F_SOUTH,
    EO1Regions.B9F_SOUTH_WEST,
    EO1Regions.B9F_SECRET_AREA,
    EO1Regions.B9F_CLEAR_CRYSTAL_ROOM,
    EO1Regions.B10F_MAIN,
    EO1Regions.B10F_EAST,
    EO1Regions.B10F_CERNUNOS_LAIR,
    EO1Regions.B10F_VIOLET_CRYSTAL_ROOM,
    EO1Regions.B10F_SECRET_AREA
}

STRATUM_3: set[str] = {
    EO1Regions.B11F_MAIN,
    EO1Regions.B11F_PITFALL,
    EO1Regions.B11F_SECRET_AREA,
    EO1Regions.B12F_MAIN,
    EO1Regions.B12F_SOUTH,
    EO1Regions.B12F_ANT_MAZE,
    EO1Regions.B12F_ANT_NEST,
    EO1Regions.B13F_MAIN,
    EO1Regions.B13F_NORTH,
    EO1Regions.B14F_MAIN,
    EO1Regions.B15F_MAIN,
    EO1Regions.B15F_COTRANGL_ROOM,
    EO1Regions.B15F_SECRET_AREA
}

STRATUM_4: set[str] = {
    EO1Regions.B16F_MAIN,
    EO1Regions.B16F_SECRET_AREA,
    EO1Regions.B16F_EAST_SECRET_AREA,
    EO1Regions.B17F_MAIN,
    EO1Regions.B17F_SECRET_AREA_NORTH_EAST,
    EO1Regions.B17F_SECRET_AREA_NORTH,
    EO1Regions.B17F_SECRET_AREA_SOUTH_EAST,
    EO1Regions.B17F_SECRET_AREA_WEST,
    EO1Regions.B18F_MAIN,
    EO1Regions.B18F_WEST,
    EO1Regions.B19F_MAIN,
    EO1Regions.B19F_STAIRS_ROOM,
    EO1Regions.B20F_MAIN,
    EO1Regions.B20F_NORTH_ROOM,
    EO1Regions.B20F_VIOLET_CRYSTAL_ROOM
}

STRATUM_5: set[str] = {
    EO1Regions.B21F_MAIN,
    EO1Regions.B21F_EAST,
    EO1Regions.B21F_SOUTH_EAST,
    EO1Regions.B21F_SOUTH_WEST,
    EO1Regions.B22F_MAIN,
    EO1Regions.B22F_NORTH_WEST_DEAD_END,
    EO1Regions.B22F_SOUTH_WEST_DEAD_END,
    EO1Regions.B22F_SOUTH_EAST_DEAD_END,
    EO1Regions.B22F_SOUTH_AREA_WEST,
    EO1Regions.B22F_SOUTH_AREA_EAST,
    EO1Regions.B22F_WEST_ELEVATOR,
    EO1Regions.B23F_MAIN,
    EO1Regions.B23F_SOUTH_WEST,
    EO1Regions.B23F_SOUTH_EAST,
    EO1Regions.B23F_NORTH_EAST,
    EO1Regions.B23F_EAST_ELEVATOR,
    EO1Regions.B24F_MAIN,
    EO1Regions.B24F_NORTH,
    EO1Regions.B24F_SOUTH_WEST,
    EO1Regions.B25F_MAIN,
    EO1Regions.B25F_WEST_ELEVATOR,
    EO1Regions.B25F_ETREANT_ROOM,
}

STRATUM_6: set[str] = {
    EO1Regions.B26F_MAIN,
    EO1Regions.B27F_MAIN,
    EO1Regions.B27F_NORTH,
    EO1Regions.B28F_DEATHPIT,
    EO1Regions.B28F_MAIN,
    EO1Regions.B29F_MAIN,
    EO1Regions.B30F_MAIN
}

ALL_REGIONS: set[str] = {
    *TOWN,
    *STRATUM_1,
    *STRATUM_2,
    *STRATUM_3,
    *STRATUM_4,
    *STRATUM_5,
    *STRATUM_6
}


@dataclass(frozen=True)
class EO1RegionData:
    """
    This class represents the data for a region in Etrian Odyssey.
    :param name: The name of the region.
    :param floor_number: The floor number the region is in. 0 means outside the labyrinth.
    :param exits: All the exits of the region.

    """

    name: str
    floor_number: int
    sustain_score: int
    exits: list[EO1Entrance]
    encounters: list[int]
    foes: list[int] = field(default_factory=list)
    bosses: list[int] = field(default_factory=list)
    is_always_survivable: bool = False


ALL_REGION_DATA: list[EO1RegionData] = [
    # --------------------------------------------------
    # Town
    EO1RegionData(EO1Regions.ETRIA, 0, 0, [
        Entrance(EO1Regions.B1F_MAIN, "Labyrinth Entrance"),
        Entrance(EO1Regions.SHILLEKA, "Shilleka's Good"),
        Entrance(EO1Regions.PUB, "Golden Deer Pub"),
        Entrance(EO1Regions.RADHA_HALL, "Radha Hall"),
    ], []),
    EO1RegionData(EO1Regions.SHILLEKA, 0, 0, [], []),
    EO1RegionData(EO1Regions.PUB, 0, 0, [], []),
    EO1RegionData(EO1Regions.RADHA_HALL, 0, 0, [], []),


    # ---------------------------------------------------
    # Stratum 1
    EO1RegionData(EO1Regions.B1F_MAIN, 1, 0, [
        ClearCrystalDoor(EO1Regions.B1F_CLEAR_CRYSTAL_ROOM),
        VioletCrystalDoor(EO1Regions.B1F_VIOLET_CRYSTAL_ROOM),
        EventLockedShortcut(EO1Regions.B1F_SECRET_AREA, EventNames.STRATUM_2_REACHED, 2),
        StairsDown(EO1Regions.B2F_MAIN)
    ], [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]),
    EO1RegionData(EO1Regions.B1F_CLEAR_CRYSTAL_ROOM, 1, 0, [], [0x05]),
    EO1RegionData(EO1Regions.B1F_VIOLET_CRYSTAL_ROOM, 1, 0, [], [0x05]),
    EO1RegionData(EO1Regions.B1F_SECRET_AREA, 1, 50, [], [0x07, 0x08, 0x09], [EO1Enemies.RAGELOPE]),

    EO1RegionData(EO1Regions.B2F_MAIN, 2, 30, [
        MandatoryFight(EO1Regions.B2F_SOUTH, [EO1Enemies.RAGELOPE]),
        StairsDown(EO1Regions.B3F_MAIN)
    ], [0x0A, 0x0B, 0x0C, 0x0D], [EO1Enemies.RAGELOPE, EO1Enemies.KUYUTHA]),
    EO1RegionData(EO1Regions.B2F_SOUTH, 2, 30, [
        ClearCrystalDoor(EO1Regions.B2F_CLEAR_CRYSTAL_ROOM),
    ], [0x0B, 0x0C, 0x0D, 0x0E], [EO1Enemies.KUYUTHA]),
    EO1RegionData(EO1Regions.B2F_CLEAR_CRYSTAL_ROOM, 2, 30, [], [0x0D]),

    EO1RegionData(EO1Regions.B3F_MAIN, 3, 50, [
        StairsDown(EO1Regions.B4F_MAIN)
    ], [0x0F, 0x10, 0x11, 0x12, 0x13], [EO1Enemies.STALKER, EO1Enemies.KUYUTHA]),
    EO1RegionData(EO1Regions.B3F_SECRET_AREA, 3, 200, [], [0x14, 0x15, 0x16], [EO1Enemies.ARMOTH]),

    EO1RegionData(EO1Regions.B4F_MAIN, 4, 150, [
        StairsDown(EO1Regions.B5F_MAIN)
    ], [0x17, 0x18, 0x19, 0x1A], [EO1Enemies.WOLF]),
    EO1RegionData(EO1Regions.B4F_SECRET_AREA, 4, 200, [
        StairsUp(EO1Regions.B3F_SECRET_AREA)
    ], [0x1B, 0x1C, 0x1D], [EO1Enemies.CUTTER]),

    EO1RegionData(EO1Regions.B5F_MAIN, 5, 200, [
        MandatoryFight(EO1Regions.B5F_FENRIR_LAIR, [EO1Enemies.FENRIR]),
        ClearCrystalDoor(EO1Regions.B5F_SECRET_AREA)
    ], [0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23], [EO1Enemies.WOLF]),
    EO1RegionData(EO1Regions.B5F_FENRIR_LAIR, 5, 0, [
        StratumTransition(EO1Regions.B6F_MAIN),
    ], [0x23], [EO1Enemies.SKOLL], bosses=[EO1Enemies.FENRIR]),
    EO1RegionData(EO1Regions.B5F_SECRET_AREA, 5, 200, [
        StairsUp(EO1Regions.B4F_SECRET_AREA)
    ], [0x1F, 0x20, 0x21, 0x22, 0x24, 0x25, 0x26], [EO1Enemies.WOLF]),

    # -----------------------------------------------------
    # Stratum 2
    # B6F
	EO1RegionData(EO1Regions.B6F_MAIN, 6, 200, [
        StairsUp(EO1Regions.B7F_MAIN),
        ClearCrystalDoor(EO1Regions.B6F_CLEAR_CRYSTAL_ROOM)
    ], [0x27, 0x28, 0x29, 0x2A, 0x2B], [EO1Enemies.MOA, EO1Enemies.CUTTER]),
    EO1RegionData(EO1Regions.B6F_CLEAR_CRYSTAL_ROOM, 6, 0, [], [0x2B]),

    # B7F
    EO1RegionData(EO1Regions.B7F_MAIN, 7, 250, [
        StairsUp(EO1Regions.B8F_MAIN),
    ], [0x2C, 0x2D, 0x2E, 0x2F, 0x30], [EO1Enemies.ASSASSIN]),
    EO1RegionData(EO1Regions.B7F_SECRET_AREA, 7, 350, [], [0x31, 0x32, 0x33, 0x34, 0x35]),

    # B8F
    EO1RegionData(EO1Regions.B8F_MAIN, 8, 250, [
        VioletCrystalDoor(EO1Regions.B8F_VIOLET_CRYSTAL_ROOM),
        EventLockedShortcut(EO1Regions.B8F_EAST_DRAGON_NEST_AREA, EventNames.MISSION_3_COMPLETED, 2, "East"),
        EventLockedShortcut(EO1Regions.B8F_WEST_DRAGON_NEST_AREA, EventNames.MISSION_3_COMPLETED, 2, "West")
    ], [0x36, 0x37, 0x38, 0x3A], bosses=[EO1Enemies.WYVERN]),

    EO1RegionData(EO1Regions.B8F_EAST_DRAGON_NEST_AREA, 8, 0, [
        StairsDown(EO1Regions.B9F_EAST)
    ], [0x37]),

    EO1RegionData(EO1Regions.B8F_WEST_DRAGON_NEST_AREA, 8, 0, [
        StairsDown(EO1Regions.B9F_NORTH_WEST)
    ], [0x37]),

    EO1RegionData(EO1Regions.B8F_EAST, 8, 300, [], [0x39, 0x37], [EO1Enemies.ARMOTH]),
    EO1RegionData(EO1Regions.B8F_SOUTH, 8, 300, [
        StairsDown(EO1Regions.B9F_SOUTH)
    ], [0x38]),
    EO1RegionData(EO1Regions.B8F_WEST, 8, 300, [
        StairsDown(EO1Regions.B9F_SOUTH_WEST)
    ], [0x38, 0x39, 0x3A], [EO1Enemies.ASSASSIN]),
    EO1RegionData(EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 8, 0, [], [0x3A]),
    EO1RegionData(EO1Regions.B8F_SECRET_AREA, 8, 350, [
        StairsUp(EO1Regions.B7F_SECRET_AREA)
    ], [0x3B, 0x3C], [EO1Enemies.KILLCLAW]),

    # B9F
    EO1RegionData(EO1Regions.B9F_EAST, 9, 300, [
        StairsUp(EO1Regions.B8F_EAST, "North East"),
        StairsUp(EO1Regions.B8F_SOUTH, "South")
    ], [0x3D, 0x3E, 0x40, 0x41], [EO1Enemies.MOA, EO1Enemies.CUTTER]),
    EO1RegionData(EO1Regions.B9F_NORTH_WEST, 9, 300, [
        ClearCrystalDoor(EO1Regions.B9F_CLEAR_CRYSTAL_ROOM)
    ], [0x3A, 0x3D, 0x3E, 0x40, 0x41], [EO1Enemies.ASSASSIN]),
    EO1RegionData(EO1Regions.B9F_SOUTH, 9, 300, [
        StairsUp(EO1Regions.B8F_WEST)
    ], [0x3F, 0x40, 0x41]),
    EO1RegionData(EO1Regions.B9F_SOUTH_WEST, 9, 300, [
        StairsUp(EO1Regions.B10F_MAIN)
    ], [0x3F]),
    EO1RegionData(EO1Regions.B9F_SECRET_AREA, 9, 350, [
        StairsUp(EO1Regions.B8F_SECRET_AREA)
    ], [0x42, 0x43], [EO1Enemies.MOA]),
    EO1RegionData(EO1Regions.B9F_CLEAR_CRYSTAL_ROOM, 9, 0, [], [0x40, 0x41], [EO1Enemies.ARMOTH, EO1Enemies.MOA]),

    # B10F
    EO1RegionData(EO1Regions.B10F_MAIN, 10, 300, [
        MandatoryFight(EO1Regions.B10F_EAST, [EO1Enemies.MOA])
    ], [0x44, 0x45, 0x46, 0x47, 0x49, 0xDA], [EO1Enemies.ASSASSIN, EO1Enemies.MOA]),
    EO1RegionData(EO1Regions.B10F_EAST, 10, 300, [
        MandatoryFight(EO1Regions.B10F_CERNUNOS_LAIR, [EO1Enemies.CERNUNOS]),
        VioletCrystalDoor(EO1Regions.B10F_VIOLET_CRYSTAL_ROOM)
    ], [0x45, 0x46, 0x47, 0x48, 0x49, 0xDA], [EO1Enemies.ARMOTH, EO1Enemies.MOA]),
    EO1RegionData(EO1Regions.B10F_CERNUNOS_LAIR, 10, 0, [
        StratumTransition(EO1Regions.B11F_MAIN),
    ], [0x48], bosses=[EO1Enemies.CERNUNOS]),
    EO1RegionData(EO1Regions.B10F_VIOLET_CRYSTAL_ROOM, 10, 0, [], [0x49, 0x4A], is_always_survivable=True),
    EO1RegionData(EO1Regions.B10F_SECRET_AREA, 10, 350, [
        StairsUp(EO1Regions.B9F_SECRET_AREA)
    ], [0x4A]),

    # ---------------------------------------------------
    # Stratum 3
    # B11F
	EO1RegionData(EO1Regions.B11F_MAIN, 11, 350, [
        StairsDown(EO1Regions.B12F_MAIN),
        MandatoryFight(EO1Regions.B11F_PITFALL, [EO1Enemies.BLOODANT]),
        VioletCrystalDoor(EO1Regions.B11F_SECRET_AREA)
    ], [0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50], [EO1Enemies.SHELLTOR, EO1Enemies.BLOODANT]),
    EO1RegionData(EO1Regions.B11F_PITFALL, 11, 0, [
        Pitfall(EO1Regions.B12F_SOUTH),
    ], []),
    EO1RegionData(EO1Regions.B11F_SECRET_AREA, 11, 350, [
        StairsUp(EO1Regions.B10F_SECRET_AREA)
    ], [0x51, 0x52, 0x53, 0x54], [EO1Enemies.MUCKDILE]),

    # B12F
    EO1RegionData(EO1Regions.B12F_MAIN, 12, 350, [
        StairsUp(EO1Regions.B11F_MAIN)
    ], [0x55, 0x56, 0x59]),
    EO1RegionData(EO1Regions.B12F_SOUTH, 12, 350, [
        MandatoryFight(EO1Regions.B12F_ANT_MAZE, [EO1Enemies.SERVANT])
    ], [0x55, 0x56, 0x57, 0x59], [EO1Enemies.BLOODANT]),
    EO1RegionData(EO1Regions.B12F_ANT_MAZE, 12, 350, [
        MandatoryFight(EO1Regions.B12F_ANT_NEST, [EO1Enemies.ROYALANT])
    ], [0x56, 0x57, 0x58, 0x59], [EO1Enemies.BLOODANT, EO1Enemies.SERVANT]),
    EO1RegionData(EO1Regions.B12F_ANT_NEST, 12, 350, [
        StairsDown(EO1Regions.B13F_MAIN)
    ], [0x58], [EO1Enemies.BLOODANT], bosses=[EO1Enemies.ROYALANT]),

    # B13F
    EO1RegionData(EO1Regions.B13F_MAIN, 13, 350, [
        StairsDown(EO1Regions.B14F_MAIN)
    ], [0x5A, 0x5B, 0x5C, 0x5D, 0x5E], [EO1Enemies.KILLCLAW, EO1Enemies.MUCKDILE]),
    EO1RegionData(EO1Regions.B13F_NORTH, 13, 350, [], [0x5B, 0x5C, 0x5D, 0x5E], [EO1Enemies.KILLCLAW]),

    # B14F
    EO1RegionData(EO1Regions.B14F_MAIN, 14, 350, [
        StairsDown(EO1Regions.B15F_MAIN),
        StairsUp(EO1Regions.B13F_NORTH)
    ], [0x5F, 0x60, 0x61, 0x62, 0x63], [EO1Enemies.KILLCLAW, EO1Enemies.MUCKDILE]),

    # B15F
    EO1RegionData(EO1Regions.B15F_MAIN, 15, 400, [
        MandatoryFight(EO1Regions.B15F_COTRANGL_ROOM, [EO1Enemies.COTRANGL]),
    ], [0x65]),
    EO1RegionData(EO1Regions.B15F_COTRANGL_ROOM, 15, 0, [
        StratumTransition(EO1Regions.B16F_MAIN)
    ], [0x65], bosses=[EO1Enemies.COTRANGL]),
    EO1RegionData(EO1Regions.B15F_SECRET_AREA, 15, 1000, [], [0x68, 0x69, 0x6A, 0x6B, 0x6C], [EO1Enemies.TERALICH]),

    # -------------------------------------------------
    # Stratum 4
    # B16F
    EO1RegionData(EO1Regions.B16F_MAIN, 16, 400, [
        StairsDown(EO1Regions.B17F_MAIN),
        EventLockedShortcut(EO1Regions.B16F_SECRET_AREA, EventNames.AZURE_COLOSSUS_QUEST_ACCEPTED, 6, "West"),
        EventLockedShortcut(EO1Regions.B16F_EAST_SECRET_AREA, EventNames.DISCOVER_CLAW_MARK, 4, "East")
    ], [0x6D, 0x6E, 0x6F, 0x70, 0x71], [EO1Enemies.SICKWOOD]),
    EO1RegionData(EO1Regions.B16F_SECRET_AREA, 16, 800, [
        StairsUp(EO1Regions.B15F_SECRET_AREA),
    ], [0x75, 0x76, 0x77, 0x78, 0x79], [EO1Enemies.SICKWOOD]),
    EO1RegionData(EO1Regions.B16F_EAST_SECRET_AREA, 16, 600, [
        StairsDown(EO1Regions.B17F_SECRET_AREA_NORTH_EAST)
    ], [0x73]),

    # B17F
    EO1RegionData(EO1Regions.B17F_MAIN, 17, 400, [
        StairsDown(EO1Regions.B18F_MAIN)
    ], [0x7A, 0x7B, 0x7C, 0x7D, 0x7E], [EO1Enemies.SICKWOOD]),
    EO1RegionData(EO1Regions.B17F_SECRET_AREA_NORTH_EAST, 17, 600, [
        MandatoryFight(EO1Regions.B17F_SECRET_AREA_NORTH, [EO1Enemies.DINOLICH, EO1Enemies.DINOLICH, EO1Enemies.DINOLICH], "Dinolich"),
        MandatoryFight(EO1Regions.B17F_SECRET_AREA_SOUTH_EAST, [EO1Enemies.DESOULER], "Desouler"),
    ], [0x7F, 0x81], []),
    EO1RegionData(EO1Regions.B17F_SECRET_AREA_NORTH, 17, 600, [],
                  [0x7F], [EO1Enemies.KINGDILE, EO1Enemies.DINOLICH]),
    EO1RegionData(EO1Regions.B17F_SECRET_AREA_SOUTH_EAST, 17, 600, [
        MandatoryFight(EO1Regions.B17F_SECRET_AREA_WEST, [EO1Enemies.KINGDILE])
    ], [0x81], [EO1Enemies.KINGDILE, EO1Enemies.DESOULER]),
    EO1RegionData(EO1Regions.B17F_SECRET_AREA_WEST, 17, 600, [],
                  [0x83], [EO1Enemies.KINGDILE, EO1Enemies.DESOULER], bosses=[EO1Enemies.MANTICOR]),

    # B18F
    EO1RegionData(EO1Regions.B18F_MAIN, 18, 450, [
        MandatoryFight(EO1Regions.B18F_WEST, [EO1Enemies.DIABOLIX])
    ], [0x85, 0x86, 0x87, 0x88, 0x89], [EO1Enemies.BUD]),
    EO1RegionData(EO1Regions.B18F_WEST, 18, 450, [
        StairsDown(EO1Regions.B19F_MAIN)
    ], [0x88, 0x89, 0x8A], [EO1Enemies.CRUELLA, EO1Enemies.DIABOLIX]),

    # B19F
    EO1RegionData(EO1Regions.B19F_MAIN, 19, 700, [
        MandatoryFight(EO1Regions.B19F_STAIRS_ROOM, [EO1Enemies.CRUELLA, EO1Enemies.DIABOLIX]),
    ], [0x8B, 0x8C, 0x8D, 0x8E, 0x90], [EO1Enemies.SICKWOOD, EO1Enemies.CRUELLA, EO1Enemies.DIABOLIX]),
    EO1RegionData(EO1Regions.B19F_STAIRS_ROOM, 19, 0, [
        StairsDown(EO1Regions.B20F_MAIN)
    ], []),

    # B20F
    EO1RegionData(EO1Regions.B20F_MAIN, 20, 750, [
        EventLockedShortcut(EO1Regions.B20F_NORTH_ROOM, EventNames.MISSION_7_COMPLETED, 4),
        VioletCrystalDoor(EO1Regions.B20F_VIOLET_CRYSTAL_ROOM)
    ], [0x93], [EO1Enemies.CRUELLA, EO1Enemies.DIABOLIX, EO1Enemies.HUNTER, EO1Enemies.OGRE], bosses=[EO1Enemies.IWAOPELN]),
    EO1RegionData(EO1Regions.B20F_NORTH_ROOM, 20, 0, [
        StratumTransition(EO1Regions.B21F_MAIN)
    ], [0x93]),
    EO1RegionData(EO1Regions.B20F_VIOLET_CRYSTAL_ROOM, 20, 0, [], [0x93]),

    # -------------------------------------------------
    # Stratum 5
    EO1RegionData(EO1Regions.B21F_MAIN, 21, 750, [
        MandatoryFight(EO1Regions.B21F_EAST, [EO1Enemies.REN, EO1Enemies.TLACHTGA]),
        StairsDown(EO1Regions.B22F_NORTH_WEST_DEAD_END, "North West"),
        StairsDown(EO1Regions.B22F_SOUTH_WEST_DEAD_END, "South West"),
        Elevator(EO1Regions.B25F_WEST_ELEVATOR, "B25F"),
        Elevator(EO1Regions.B22F_WEST_ELEVATOR, "B22F"),
        Elevator(EO1Regions.B23F_MAIN, "B23F"),
        Elevator(EO1Regions.B24F_SOUTH_WEST, "B24F")
    ], [0x97, 0x98, 0x9A, 0x9B], [EO1Enemies.DINOLICH], bosses=[EO1Enemies.REN, EO1Enemies.TLACHTGA]),
    EO1RegionData(EO1Regions.B21F_EAST, 21, 750, [
        StairsDown(EO1Regions.B22F_MAIN),
        Elevator(EO1Regions.B25F_MAIN, "B25F"),
        Elevator(EO1Regions.B22F_SOUTH_AREA_EAST, "B22F"),
        Elevator(EO1Regions.B23F_EAST_ELEVATOR, "B23F"),
        Elevator(EO1Regions.B24F_NORTH, "B24F"),
    ], [0x98, 0x99, 0x9A, 0x9B], [EO1Enemies.DINOLICH]),
    EO1RegionData(EO1Regions.B21F_SOUTH_EAST, 21, 750, [
        MandatoryFight(EO1Regions.B21F_SOUTH_WEST, [EO1Enemies.KINGDILE])
    ], [0x99, 0x9B], [EO1Enemies.KINGDILE]),
    EO1RegionData(EO1Regions.B21F_SOUTH_WEST, 21, 750, [], [0x9B, 0x9C], [EO1Enemies.KINGDILE]),

    EO1RegionData(EO1Regions.B22F_MAIN, 22, 750, [
        StairsDown(EO1Regions.B23F_NORTH_EAST, "North East"),
        StairsDown(EO1Regions.B23F_MAIN, "North West"),
    ], [0x9D, 0x9E, 0x9F, 0xA0], [EO1Enemies.DINOLICH]),
    EO1RegionData(EO1Regions.B22F_NORTH_WEST_DEAD_END, 22, 0, [], []), # Cannot trigger encounters here (only one tile).
    EO1RegionData(EO1Regions.B22F_SOUTH_WEST_DEAD_END, 22, 0, [], [0x9D]),
    EO1RegionData(EO1Regions.B22F_SOUTH_EAST_DEAD_END, 22, 0, [], []), # Cannot trigger encounters here (only one tile).
    EO1RegionData(EO1Regions.B22F_SOUTH_AREA_WEST, 22, 750, [
        MandatoryFight(EO1Regions.B22F_SOUTH_AREA_EAST, [EO1Enemies.DESOULER, EO1Enemies.DESOULER])
    ], [0x9E, 0xA0, 0xA1], [EO1Enemies.DESOULER, EO1Enemies.KINGDILE]),
    EO1RegionData(EO1Regions.B22F_SOUTH_AREA_EAST, 22, 750, [
        MandatoryFight(EO1Regions.B22F_SOUTH_AREA_WEST, [EO1Enemies.DESOULER, EO1Enemies.DESOULER]),
        StairsUp(EO1Regions.B21F_SOUTH_EAST)
    ], [0xA2], [EO1Enemies.DESOULER]),

    EO1RegionData(EO1Regions.B22F_WEST_ELEVATOR, 22, 0, [], [0xA2]),

    EO1RegionData(EO1Regions.B23F_MAIN, 23, 750, [
        StairsDown(EO1Regions.B24F_NORTH, "North East"),
        StairsDown(EO1Regions.B24F_MAIN, "North West"),
        StairsUp(EO1Regions.B22F_SOUTH_AREA_WEST, "South West"),
        StairsUp(EO1Regions.B22F_MAIN, "North West")
    ], [0xA3, 0xA4, 0xA5, 0xA6, 0xA7], [EO1Enemies.KINGDILE, EO1Enemies.DESOULER]),
    EO1RegionData(EO1Regions.B23F_SOUTH_WEST, 23, 0, [], [0xA9, 0xAA], [EO1Enemies.KINGDILE]),
    EO1RegionData(EO1Regions.B23F_SOUTH_EAST, 23, 0, [
        StairsUp(EO1Regions.B22F_SOUTH_EAST_DEAD_END)
    ], [0xA9, 0xAA]),
    EO1RegionData(EO1Regions.B23F_NORTH_EAST, 23, 0, [], [0xA3]),
    EO1RegionData(EO1Regions.B23F_EAST_ELEVATOR, 23, 0, [], [0xA9, 0xAA]),

    EO1RegionData(EO1Regions.B24F_MAIN, 24, 750, [
        StairsUp(EO1Regions.B23F_SOUTH_EAST)
    ], [0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0], [EO1Enemies.DESOULER, EO1Enemies.DINOLICH]),
    EO1RegionData(EO1Regions.B24F_NORTH, 24, 800, [], [0xAB, 0xAC, 0xAD, 0xAE], [EO1Enemies.DESOULER, EO1Enemies.DINOLICH]),
    EO1RegionData(EO1Regions.B24F_SOUTH_WEST, 24, 800, [
        StairsUp(EO1Regions.B23F_SOUTH_WEST)
    ], [0xB0], [EO1Enemies.DESOULER]),

    EO1RegionData(EO1Regions.B25F_MAIN, 25, 800, [
        CardKeyDoor(EO1Regions.B25F_ETREANT_ROOM)
    ], [0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7], [EO1Enemies.TREETUSK, EO1Enemies.DESOULER, EO1Enemies.KINGDILE]),
    EO1RegionData(EO1Regions.B25F_ETREANT_ROOM, 25, 0, [
        StratumTransition(EO1Regions.B26F_MAIN),
    ], [0xB6], bosses=[EO1Enemies.ETREANT]),
    EO1RegionData(EO1Regions.B25F_WEST_ELEVATOR, 25, 0, [], [0xB2]),

    # ---------------------------------------------------------------
    # Stratum 6
    EO1RegionData(EO1Regions.B26F_MAIN, 26, 1000, [
        StairsDown(EO1Regions.B27F_MAIN)
    ], [0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE], [EO1Enemies.SHELLORD, EO1Enemies.TERALICH, EO1Enemies.SONGBIRD]),
    EO1RegionData(EO1Regions.B27F_MAIN, 27, 1000, [
        StairsDown(EO1Regions.B28F_MAIN),
        #EO1Entrances.B27F_STAIRS,
        Pitfall(EO1Regions.B28F_DEATHPIT)
    ], [0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4], [EO1Enemies.SHELLORD, EO1Enemies.SONGBIRD]),
    EO1RegionData(EO1Regions.B27F_NORTH, 27, 1000, [
        StairsDown(EO1Regions.B28F_MAIN)
    ], [0xC3, 0xC4, 0xC5]),
    EO1RegionData(EO1Regions.B28F_DEATHPIT, 28, 1000, [], [0xC6, 0xC7, 0xC8, 0xC9], [EO1Enemies.MACABRE]),
    EO1RegionData(EO1Regions.B28F_MAIN, 28, 1000, [
        StairsUp(EO1Regions.B27F_NORTH),
        StairsDown(EO1Regions.B29F_MAIN)
    ], [0xC9]),
    EO1RegionData(EO1Regions.B29F_MAIN, 29, 1000, [
        StairsDown(EO1Regions.B30F_MAIN)
    ], [0xCD, 0xCE, 0xCF, 0xDB], [EO1Enemies.SHELLORD]),
    EO1RegionData(EO1Regions.B30F_MAIN, 30, 1000, [], [0xD3, 0xD4, 0xD5, 0xD6, 0xDC], [EO1Enemies.SONGBIRD, EO1Enemies.TERALICH]),

]

ALL_REGION_DATA_BY_NAME: dict[str, EO1RegionData] = {region_data.name:region_data for region_data in ALL_REGION_DATA}

def generate_region_by_floor_dictionary()-> dict[int, list[str]]:
    region_by_floor: dict[int, list[str]] = {}

    def add_region(reg: str, floor_number: int):
        if floor_number not in region_by_floor:
            region_by_floor[floor_number] = []

        region_by_floor[floor_number].append(reg)

    for region_data in ALL_REGION_DATA:
        add_region(region_data.name, region_data.floor_number)

    return region_by_floor

ALL_REGIONS_BY_FLOOR: dict[int, list[str]] = generate_region_by_floor_dictionary()
