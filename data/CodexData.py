from enum import IntEnum
from .EnemyData import *

class CodexEncounterType(IntEnum):
    REGULAR = 1
    FOE = 2
    BOSS = 3
    QUEST = 4
    MINION = 5

class CodexData:
    enemy_id: int
    codex_id: int
    location_id: int
    required_stratum: int
    encounter_type: CodexEncounterType

    def __init__(self, enemy_id: int, codex_id: int, location_id: int, required_stratum: int, encounter_type: CodexEncounterType) -> None:
        self.enemy_id = enemy_id
        self.codex_id = codex_id
        self.location_id = location_id
        self.required_stratum = required_stratum
        self.encounter_type = encounter_type

    def get_full_name(self) -> str:
        return f"Codex entry #{self.codex_id}: {ENEMY_BY_ID[self.enemy_id].name}"

ALL_CODEX_ENTRIES: list[CodexData] = [
    CodexData(EO1Enemies.GOUDARAT, 0x0, 2000, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.TREERAT, 0x1, 2001, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.WOODFLY, 0x2, 2002, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MOLE, 0x3, 2003, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.CLAWBUG, 0x4, 2004, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.VENOMFLY, 0x5, 2005, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HARE, 0x6, 2006, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FENDER, 0x7, 2007, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MANDRAKE, 0x8, 2008, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.ROLLER, 0x9, 2009, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.CLAWFLY, 0xA, 2010, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.WARBULL, 0xB, 2011, 1, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SLEEPGEL, 0xC, 2012, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.VENOMGEL, 0xD, 2013, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.WASPIOR, 0xE, 2014, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SPIDER, 0xF, 2015, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FANGLEAF, 0x10, 2016, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SLOTH, 0x11, 2017, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.PETALOID, 0x12, 2018, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.EVILOID, 0x13, 2019, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FIREBIRD, 0x14, 2020, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MANEATER, 0x15, 2021, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SCORPION, 0x16, 2022, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.STINGMAW, 0x17, 2023, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.GLOWBIRD, 0x18, 2024, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MADWORM, 0x19, 2025, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.GUARDANT, 0x1A, 2026, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.TREEFROG, 0x1B, 2027, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.DEATHANT, 0x1C, 2028, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HEXFROG, 0x1D, 2029, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.WOODBAT, 0x1E, 2030, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MELTWORM, 0x1F, 2031, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MORIYANA, 0x20, 2032, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.VAMPBAT, 0x21, 2033, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.CUTCRAB, 0x22, 2034, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SWORDER, 0x23, 2035, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.REDCLAW, 0x24, 2036, 3, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FLAMERAT, 0x25, 2037, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.GOLDEER, 0x26, 2038, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SOLDIER, 0x27, 2039, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MYSTIC, 0x28, 2040, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MANTIS, 0x29, 2041, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SABREMAW, 0x2A, 2042, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.PIXIE, 0x2B, 2043, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HEXROOT, 0x2C, 2044, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.WARRIOR, 0x2D, 2045, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.DRUID, 0x2E, 2046, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FAERIE, 0x2F, 2047, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.REDBEAK, 0x30, 2048, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.IMMOA, 0x31, 2049, 4, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.DARKHARE, 0x32, 2050, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MAUL, 0x33, 2051, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.BURSTGEL, 0x34, 2052, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.DIREWOLF, 0x35, 2053, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MUSKOID, 0x36, 2054, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.KINGFROG, 0x37, 2055, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.KINGAPIS, 0x38, 2056, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.CLAWLORD, 0x39, 2057, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.SILKER, 0x3A, 2058, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.VARAHA, 0x3B, 2059, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.ARMOROLL, 0x3C, 2060, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HELLBULL, 0x3D, 2061, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.KINGYANA, 0x3E, 2062, 5, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FLAMEGEL, 0x3F, 2063, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HAZEFLY, 0x40, 2064, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.HELLFLY, 0x41, 2065, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.BLADER, 0x42, 2066, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.MONOCYTE, 0x43, 2067, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.LARGEANT, 0x44, 2068, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.RED_CELL, 0x45, 2069, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.EVILROOT, 0x46, 2070, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.ROCKWOOD, 0x47, 2071, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.METALION, 0x48, 2072, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.LUCIFIRD, 0x49, 2073, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.IRONCRAB, 0x4A, 2074, 6, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.FIREATER, 0x4B, 2075, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.PONDCLAW, 0x4C, 2076, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.TOXINFLY, 0x4D, 2077, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.OMNIVORE, 0x4E, 2078, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.NIGHTOAD, 0x4F, 2079, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.HEXTOAD, 0x50, 2080, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.STEELWEB, 0x51, 2081, 7, CodexEncounterType.QUEST), # Quest enemies not considered for now.
    CodexData(EO1Enemies.RAGELOPE, 0x52, 2082, 1, CodexEncounterType.FOE),
    CodexData(EO1Enemies.KUYUTHA, 0x53, 2083, 1, CodexEncounterType.FOE),
    CodexData(EO1Enemies.WOLF, 0x54, 2084, 1, CodexEncounterType.FOE),
    CodexData(EO1Enemies.MOA, 0x55, 2085, 2, CodexEncounterType.FOE),
    CodexData(EO1Enemies.ASSASSIN, 0x56, 2086, 2, CodexEncounterType.FOE),
    CodexData(EO1Enemies.CUTTER, 0x57, 2087, 2, CodexEncounterType.FOE),
    CodexData(EO1Enemies.BLOODANT, 0x58, 2088, 3, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SERVANT, 0x59, 2089, 3, CodexEncounterType.FOE),
    CodexData(EO1Enemies.KILLCLAW, 0x5A, 2090, 3, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SICKWOOD, 0x5B, 2091, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.CRUELLA, 0x5C, 2092, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.DIABOLIX, 0x5D, 2093, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.DESOULER, 0x5E, 2094, 5, CodexEncounterType.FOE),
    CodexData(EO1Enemies.KINGDILE, 0x5F, 2095, 5, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SONGBIRD, 0x60, 2096, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SHELLORD, 0x61, 2097, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.MACABRE, 0x62, 2098, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.WYRMOID, 0x63, 2099, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.DRAKOID, 0x64, 2100, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.DRAGOID, 0x65, 2101, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.STALKER, 0x66, 2102, 1, CodexEncounterType.FOE),
    CodexData(EO1Enemies.ARMOTH, 0x67, 2103, 2, CodexEncounterType.FOE),
    CodexData(EO1Enemies.MUCKDILE, 0x68, 2104, 3, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SHELLTOR, 0x69, 2105, 3, CodexEncounterType.FOE),
    CodexData(EO1Enemies.OGRE, 0x6A, 2106, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.HUNTER, 0x6B, 2107, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.TREETUSK, 0x6C, 2108, 5, CodexEncounterType.FOE),
    CodexData(EO1Enemies.DINOLICH, 0x6D, 2109, 5, CodexEncounterType.FOE),
    CodexData(EO1Enemies.TERALICH, 0x6E, 2110, 6, CodexEncounterType.FOE),
    CodexData(EO1Enemies.SKOLL, 0x6F, 2111, 2, CodexEncounterType.FOE), # Not a check for stratum 1 goals.
    CodexData(EO1Enemies.FENRIR, 0x70, 2112, 2, CodexEncounterType.BOSS), # Not a check for stratum 1 goals.
    CodexData(EO1Enemies.CUROLLER, 0x71, 2113, 3, CodexEncounterType.MINION), # Not a check for stratum 2 goals.
    CodexData(EO1Enemies.CERNUNOS, 0x72, 2114, 3, CodexEncounterType.BOSS), # Not a check for stratum 2 goals.
    CodexData(EO1Enemies.ROYALANT, 0x73, 2115, 3, CodexEncounterType.BOSS),
    CodexData(EO1Enemies.COTRANGL, 0x74, 2116, 4, CodexEncounterType.BOSS), # Not a check for stratum 3 goals.
    CodexData(EO1Enemies.IWAOPELN, 0x75, 2117, 5, CodexEncounterType.BOSS), # Not a check for stratum 4 goals.
    CodexData(EO1Enemies.REN, 0x76, 2118, 5, CodexEncounterType.BOSS),
    CodexData(EO1Enemies.TLACHTGA, 0x77, 2119, 5, CodexEncounterType.BOSS),
    CodexData(EO1Enemies.ETREANT, 0x78, 2120, 6, CodexEncounterType.BOSS), # Not a check for stratum 5 goals.
    CodexData(EO1Enemies.GOLEM, 0x79, 2121, 7, CodexEncounterType.BOSS), # Is in stratum 1 but require stratum 3.
    CodexData(EO1Enemies.WYVERN, 0x7A, 2122, 4, CodexEncounterType.BOSS), # Is in stratum 2, but is stronger than the stratum 3 boss.
    CodexData(EO1Enemies.MANTICOR, 0x7B, 2123, 7, CodexEncounterType.BOSS),
    CodexData(EO1Enemies.ALRAUNE, 0x7C, 2124, 7, CodexEncounterType.BOSS), # Is in stratum 2 but require stratum 5.
    CodexData(EO1Enemies.WYRM, 0x7D, 2125, 7, CodexEncounterType.BOSS),# Quest enemies not considered for now.
    CodexData(EO1Enemies.DRAKE, 0x7E, 2126, 7, CodexEncounterType.BOSS),# Quest enemies not considered for now.
    CodexData(EO1Enemies.DRAGON, 0x7F, 2127, 7, CodexEncounterType.BOSS),# Quest enemies not considered for now.
    CodexData(EO1Enemies.PRIMEVIL, 0x80, 2128, 7, CodexEncounterType.BOSS), # Not a check for stratum 6 goals.
    CodexData(EO1Enemies.SPROUT, 0x81, 2129, 2, CodexEncounterType.REGULAR),
    CodexData(EO1Enemies.BUD, 0x82, 2130, 4, CodexEncounterType.FOE),
    CodexData(EO1Enemies.CLOVER, 0x83, 2131, 6, CodexEncounterType.REGULAR),
]

CODEX_DATA_BY_LOCATION_ID: dict[int, CodexData] = {codex_data.location_id:codex_data for codex_data in ALL_CODEX_ENTRIES}
CODEX_DATA_BY_ENEMY_ID: dict[int, CodexData] = {codex_data.enemy_id:codex_data for codex_data in ALL_CODEX_ENTRIES}
