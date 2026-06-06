from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple, Optional

from .EnemyData import EO1Enemies
from .RegionData import EO1Regions
from enum import IntEnum

class TreasureContentType(IntEnum):
    Item = 0
    Money = 1

@dataclass(frozen=True)
class TreasureLogicRequirement:
    mandatory_enemies: list[int]
    require_escape: bool = False

class TreasureData(NamedTuple):
    floor_number: int
    chest_id: int
    name: str
    default_content_type: TreasureContentType
    default_content_value: int
    region: str
    location_id: int
    logic_requirement: TreasureLogicRequirement = TreasureLogicRequirement([], False)
    required_stratum: int | None = None

    def get_full_name(self) -> str:
        return f"{self.region} - {self.name}{' ' if self.name != '' else ''}Chest"

    def require_access_rule(self) -> bool:
        return self.logic_requirement.require_escape \
            or len(self.logic_requirement.mandatory_enemies) > 0

ALL_TREASURE_DATA: list[TreasureData] = [
    TreasureData(1, 0, "A6", TreasureContentType.Item, 2003, EO1Regions.B1F_SECRET_AREA, 1000),  # B1F At [25,1], 0x07D3 - Plumed Hat
    TreasureData(1, 1, "A3 North", TreasureContentType.Item, 2, EO1Regions.B1F_MAIN, 1001),  # B1F At [12,2], 0x0002 - Scramasax
    TreasureData(1, 2, "", TreasureContentType.Item, 4290, EO1Regions.B1F_CLEAR_CRYSTAL_ROOM, 1002),  # B1F At [2,3], 0x10C2 - Nectar
    TreasureData(1, 3, "A3 Middle", TreasureContentType.Item, 4280, EO1Regions.B1F_MAIN, 1003),  # B1F At [12,3], 0x10B8 - Medica II
    TreasureData(1, 4, "A3 South", TreasureContentType.Money, 200, EO1Regions.B1F_MAIN, 1004),  # B1F At [12,4], 200en
    TreasureData(1, 5, "B6", TreasureContentType.Item, 4280, EO1Regions.B1F_SECRET_AREA, 1005),  # B1F At [28,6], 0x10B8 - Medica II
    TreasureData(1, 6, "C6 North", TreasureContentType.Item, 7, EO1Regions.B1F_SECRET_AREA, 1006),  # B1F At [28,10], 0x0007 - Rapier
    TreasureData(1, 7, "North", TreasureContentType.Item, 4291, EO1Regions.B1F_VIOLET_CRYSTAL_ROOM, 1007),  # B1F At [11,12], 0x10C3 - Nectar II
    TreasureData(1, 8, "South", TreasureContentType.Item, 59, EO1Regions.B1F_VIOLET_CRYSTAL_ROOM, 1008),  # B1F At [11,13], 0x003B - Gem Staff
    TreasureData(1, 9, "C6 South", TreasureContentType.Money, 500, EO1Regions.B1F_SECRET_AREA, 1009),  # B1F At [28,14], 500en
    TreasureData(2, 0, "A3", TreasureContentType.Item, 4374, EO1Regions.B2F_MAIN, 1010),  # B2F At [9,1], 0x1116 - Warp Wire
    TreasureData(2, 1, "A6", TreasureContentType.Item, 1008, EO1Regions.B2F_MAIN, 1011, TreasureLogicRequirement([EO1Enemies.KUYUTHA])),  # B2F At [25,3], 0x03F0 - Buffcoat
    TreasureData(2, 2, "North", TreasureContentType.Item, 4282, EO1Regions.B2F_CLEAR_CRYSTAL_ROOM, 1012),  # B2F At [33,10], 0x10BA - Medica IV
    TreasureData(2, 3, "C1", TreasureContentType.Item, 4290, EO1Regions.B2F_SOUTH, 1013),  # B2F At [1,11], 0x10C2 - Nectar
    TreasureData(2, 4, "South", TreasureContentType.Item, 4288, EO1Regions.B2F_CLEAR_CRYSTAL_ROOM, 1014),  # B2F At [33,13], 0x10C0 - Soma
    TreasureData(3, 0, "A1 North", TreasureContentType.Money, 400, EO1Regions.B3F_MAIN, 1015),  # B3F At [1,1], 400en
    TreasureData(3, 1, "A1 Middle", TreasureContentType.Item, 4281, EO1Regions.B3F_MAIN, 1016),  # B3F At [1,2], 0x10B9 - Medica III
    TreasureData(3, 2, "A1 South", TreasureContentType.Item, 2057, EO1Regions.B3F_MAIN, 1017),  # B3F At [1,3], 0x0809 - Hide Boot
    TreasureData(3, 3, "F1", TreasureContentType.Item, 4295, EO1Regions.B3F_MAIN, 1018),  # B3F At [4,25], 0x10C7 - Theriaca A
    TreasureData(3, 4, "F4", TreasureContentType.Money, 500, EO1Regions.B3F_MAIN, 1019, TreasureLogicRequirement([EO1Enemies.RAGELOPE], require_escape=True)),  # B3F At [16,25], 500en
    TreasureData(4, 0, "A1", TreasureContentType.Item, 4284, EO1Regions.B4F_MAIN, 1020),  # B4F At [1,4], 0x10BC - Amrita
    TreasureData(4, 1, "B4", TreasureContentType.Money, 2000, EO1Regions.B4F_SECRET_AREA, 1021, TreasureLogicRequirement([EO1Enemies.CUTTER]), required_stratum=2),  # B4F At [19,5], 2000en
    TreasureData(4, 2, "B3 East", TreasureContentType.Item, 4280, EO1Regions.B4F_MAIN, 1022),  # B4F At [13,8], 0x10B8 - Medica II
    TreasureData(4, 3, "B3 West", TreasureContentType.Item, 1006, EO1Regions.B4F_MAIN, 1023),  # B4F At [11,9], 0x03EE - Plate
    TreasureData(4, 4, "E4", TreasureContentType.Item, 4308, EO1Regions.B4F_SECRET_AREA, 1024),  # B4F At [19,20], 0x10D4 - Stonard II
    TreasureData(4, 5, "F2", TreasureContentType.Item, 4305, EO1Regions.B4F_MAIN, 1025, TreasureLogicRequirement([EO1Enemies.WOLF], require_escape=True)),  # B4F At [7,28], 0x10D1 - Bravant
    TreasureData(5, 0, "B7", TreasureContentType.Item, 4284, EO1Regions.B5F_SECRET_AREA, 1026),  # B5F At [32,9], 0x10BC - Amrita
    TreasureData(5, 1, "C7", TreasureContentType.Item, 5, EO1Regions.B5F_MAIN, 1027),  # B5F At [30,10], 0x0005 - Boar Spear
    TreasureData(5, 2, "E1 West", TreasureContentType.Item, 4291, EO1Regions.B5F_SECRET_AREA, 1028),  # B5F At [3,21], 0x10C3 - Nectar II
    TreasureData(5, 3, "E1 East", TreasureContentType.Item, 4306, EO1Regions.B5F_SECRET_AREA, 1029),  # B5F At [4,21], 0x10D2 - Bravant II
    TreasureData(5, 4, "E6", TreasureContentType.Item, 4315, EO1Regions.B5F_MAIN, 1030),  # B5F At [27,24], 0x10DB - Blaze Oil
    TreasureData(6, 0, "A6", TreasureContentType.Item, 4281, EO1Regions.B6F_MAIN, 1031),  # B6F At [26,3], 0x10B9 - Medica III
    TreasureData(6, 1, "", TreasureContentType.Money, 1000, EO1Regions.B6F_CLEAR_CRYSTAL_ROOM, 1032),  # B6F At [23,11], 1000en
    TreasureData(6, 2, "C3", TreasureContentType.Item, 57, EO1Regions.B6F_MAIN, 1033),  # B6F At [14,13], 0x0039 - Down Staff
    TreasureData(6, 3, "C4", TreasureContentType.Item, 4307, EO1Regions.B6F_MAIN, 1034),  # B6F At [18,13], 0x10D3 - Stonard
    TreasureData(7, 0, "A1", TreasureContentType.Item, 4354, EO1Regions.B7F_MAIN, 1035, TreasureLogicRequirement([EO1Enemies.ASSASSIN], require_escape=True)),  # B7F At [2,1], 0x1102 - Clear Key
    TreasureData(7, 1, "A4", TreasureContentType.Item, 1025, EO1Regions.B7F_SECRET_AREA, 1036),  # B7F At [18,1], 0x0401 - Surcoat
    TreasureData(7, 2, "A7", TreasureContentType.Item, 4288, EO1Regions.B7F_SECRET_AREA, 1037),  # B7F At [33,1], 0x10C0 - Soma
    TreasureData(7, 3, "C2", TreasureContentType.Item, 2004, EO1Regions.B7F_MAIN, 1038),  # B7F At [5,14], 0x07D4 - Chain Helm
    TreasureData(7, 4, "D4", TreasureContentType.Item, 4282, EO1Regions.B7F_SECRET_AREA, 1039),  # B7F At [18,18], 0x10BA - Medica IV
    TreasureData(7, 5, "D7", TreasureContentType.Item, 4306, EO1Regions.B7F_SECRET_AREA, 1040),  # B7F At [33,18], 0x10D2 - Bravant II
    TreasureData(8, 0, "North West", TreasureContentType.Money, 500, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1041),  # B8F At [12,1], 500en
    TreasureData(8, 1, "North", TreasureContentType.Money, 1500, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1042),  # B8F At [13,1], 1500en
    TreasureData(8, 2, "North East", TreasureContentType.Money, 1000, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1043),  # B8F At [14,1], 1000en
    TreasureData(8, 3, "West", TreasureContentType.Item, 4283, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1044),  # B8F At [12,3], 0x10BB - Medica V
    TreasureData(8, 4, "East", TreasureContentType.Item, 4291, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1045),  # B8F At [14,3], 0x10C3 - Nectar II
    TreasureData(8, 5, "South West", TreasureContentType.Item, 2060, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1046),  # B8F At [12,5], 0x080C - Moccasins
    TreasureData(8, 6, "South East", TreasureContentType.Item, 4286, EO1Regions.B8F_VIOLET_CRYSTAL_ROOM, 1047),  # B8F At [14,5], 0x10BE - Hamao
    TreasureData(8, 7, "West", TreasureContentType.Item, 1013, EO1Regions.B8F_EAST, 1048),  # B8F At [28,14], 0x03F5 - Iron Plate
    TreasureData(8, 8, "Middle", TreasureContentType.Money, 500, EO1Regions.B8F_EAST, 1049),  # B8F At [29,14], 500en
    TreasureData(8, 9, "East", TreasureContentType.Item, 4307, EO1Regions.B8F_EAST, 1050),  # B8F At [30,14], 0x10D3 - Stonard
    TreasureData(9, 0, "A5", TreasureContentType.Item, 4281, EO1Regions.B9F_EAST, 1051),  # B9F At [23,3], 0x10B9 - Medica III
    TreasureData(9, 1, "B2", TreasureContentType.Item, 4332, EO1Regions.B9F_NORTH_WEST, 1052),  # B9F At [9,7], 0x10EC - Magnet
    TreasureData(9, 2, "West", TreasureContentType.Item, 33, EO1Regions.B9F_CLEAR_CRYSTAL_ROOM, 1053),  # B9F At [5,12], 0x0021 - Broadaxe
    TreasureData(9, 3, "Middle", TreasureContentType.Money, 900, EO1Regions.B9F_CLEAR_CRYSTAL_ROOM, 1054),  # B9F At [6,12], 900en
    TreasureData(9, 4, "East", TreasureContentType.Item, 4296, EO1Regions.B9F_CLEAR_CRYSTAL_ROOM, 1055),  # B9F At [7,12], 0x10C8 - Theriaca B
    TreasureData(9, 5, "C5", TreasureContentType.Item, 1015, EO1Regions.B9F_EAST, 1056),  # B9F At [21,12], 0x03F7 - Oak Jacket
    TreasureData(9, 6, "D3", TreasureContentType.Item, 4290, EO1Regions.B9F_SOUTH, 1057),  # B9F At [12,16], 0x10C2 - Nectar
    TreasureData(10, 0, "West", TreasureContentType.Item, 59, EO1Regions.B10F_VIOLET_CRYSTAL_ROOM, 1058),  # B10F At [29,3], 0x003B - Gem Staff
    TreasureData(10, 1, "Middle", TreasureContentType.Item, 4291, EO1Regions.B10F_VIOLET_CRYSTAL_ROOM, 1059),  # B10F At [30,3], 0x10C3 - Nectar II
    TreasureData(10, 2, "East", TreasureContentType.Money, 1400, EO1Regions.B10F_VIOLET_CRYSTAL_ROOM, 1060),  # B10F At [31,3], 1400en
    TreasureData(10, 3, "A1", TreasureContentType.Item, 6, EO1Regions.B10F_MAIN, 1061),  # B10F At [2,4], 0x0006 - Broadsword
    TreasureData(10, 4, "D5", TreasureContentType.Item, 4285, EO1Regions.B10F_EAST, 1062),  # B10F At [24,16], 0x10BD - Amrita II
    TreasureData(11, 0, "A1", TreasureContentType.Money, 700, EO1Regions.B11F_MAIN, 1063),  # B11F At [1,2], 700en
    TreasureData(11, 1, "B4", TreasureContentType.Item, 4282, EO1Regions.B11F_MAIN, 1064),  # B11F At [18,9], 0x10BA - Medica IV
    TreasureData(11, 2, "C2", TreasureContentType.Item, 4285, EO1Regions.B11F_MAIN, 1065),  # B11F At [5,11], 0x10BD - Amrita II
    TreasureData(11, 3, "", TreasureContentType.Item, 1024, EO1Regions.B11F_SECRET_AREA, 1066),  # B11F At [22,22], 0x0400 - 7 Doublet
    TreasureData(12, 0, "A5", TreasureContentType.Item, 4281, EO1Regions.B12F_MAIN, 1067),  # B12F At [22,1], 0x10B9 - Medica III
    TreasureData(12, 1, "B3", TreasureContentType.Item, 4285, EO1Regions.B12F_ANT_MAZE, 1068),  # B12F At [12,9], 0x10BD - Amrita II
    TreasureData(12, 2, "D4", TreasureContentType.Item, 4305, EO1Regions.B12F_SOUTH, 1069),  # B12F At [18,17], 0x10D1 - Bravant
    TreasureData(12, 3, "E5", TreasureContentType.Item, 2005, EO1Regions.B12F_SOUTH, 1070),  # B12F At [20,20], 0x07D5 - Gum Helm
    TreasureData(13, 0, "A1", TreasureContentType.Item, 2024, EO1Regions.B13F_NORTH, 1071),  # B13F At [2,1], 0x07E8 - Fang Glove
    TreasureData(13, 1, "A2", TreasureContentType.Item, 4285, EO1Regions.B13F_NORTH, 1072),  # B13F At [9,1], 0x10BD - Amrita II
    TreasureData(13, 2, "B4", TreasureContentType.Item, 4355, EO1Regions.B13F_NORTH, 1073),  # B13F At [16,5], 0x1103 - Violet Key
    TreasureData(13, 3, "B7", TreasureContentType.Item, 4281, EO1Regions.B13F_MAIN, 1074),  # B13F At [31,9], 0x10B9 - Medica III
    TreasureData(13, 4, "D3", TreasureContentType.Item, 120, EO1Regions.B13F_MAIN, 1075),  # B13F At [10,15], 0x0078 - Wind Whip
    TreasureData(13, 5, "D5", TreasureContentType.Item, 4306, EO1Regions.B13F_MAIN, 1076),  # B13F At [21,15], 0x10D2 - Bravant II
    TreasureData(14, 0, "C7 West", TreasureContentType.Item, 4286, EO1Regions.B14F_MAIN, 1077),  # B14F At [30,11], 0x10BE - Hamao
    TreasureData(14, 1, "C7 East", TreasureContentType.Money, 800, EO1Regions.B14F_MAIN, 1078),  # B14F At [31,11], 800en
    TreasureData(14, 2, "D4", TreasureContentType.Item, 4281, EO1Regions.B14F_MAIN, 1079),  # B14F At [16,15], 0x10B9 - Medica III
    TreasureData(14, 3, "F2", TreasureContentType.Item, 4312, EO1Regions.B14F_MAIN, 1080),  # B14F At [6,28], 0x10D8 - Ice Mist
    TreasureData(15, 0, "A3", TreasureContentType.Item, 4308, EO1Regions.B15F_SECRET_AREA, 1081),  # B15F At [10,2], 0x10D4 - Stonard II
    TreasureData(15, 1, "B2", TreasureContentType.Item, 4303, EO1Regions.B15F_SECRET_AREA_WEST, 1082),  # B15F At [8,6], 0x10CF - Axcela III
    TreasureData(15, 2, "C5", TreasureContentType.Item, 4306, EO1Regions.B15F_SECRET_AREA, 1083),  # B15F At [23,13], 0x10D2 - Bravant II
    TreasureData(15, 3, "D5", TreasureContentType.Item, 1025, EO1Regions.B15F_SECRET_AREA, 1084),  # B15F At [23,16], 0x0401 - Surcoat
    TreasureData(15, 4, "D7", TreasureContentType.Money, 1500, EO1Regions.B15F_SECRET_AREA, 1085),  # B15F At [30,16], 1500en
    TreasureData(15, 5, "E1 West", TreasureContentType.Item, 2061, EO1Regions.B15F_MAIN, 1086),  # B15F At [1,22], 0x080D - Scale Boot
    TreasureData(15, 6, "E1 East", TreasureContentType.Item, 4315, EO1Regions.B15F_MAIN, 1087),  # B15F At [2,22], 0x10DB - Blaze Oil
    TreasureData(16, 0, "A3", TreasureContentType.Item, 4296, EO1Regions.B16F_MAIN, 1088),  # B16F At [12,4], 0x10C8 - Theriaca B
    TreasureData(16, 1, "A5", TreasureContentType.Money, 1000, EO1Regions.B16F_MAIN, 1089),  # B16F At [24,4], 1000en
    TreasureData(16, 2, "D1 West", TreasureContentType.Item, 4282, EO1Regions.B16F_SECRET_AREA, 1090),  # B16F At [1,15], 0x10BA - Medica IV
    TreasureData(16, 3, "D1 East", TreasureContentType.Item, 2062, EO1Regions.B16F_SECRET_AREA, 1091),  # B16F At [2,15], 0x080E - Fairy Boot
    TreasureData(16, 4, "D5", TreasureContentType.Item, 1030, EO1Regions.B16F_MAIN, 1092),  # B16F At [20,18], 0x0406 - Brigandine
    TreasureData(16, 5, "E2", TreasureContentType.Item, 4288, EO1Regions.B16F_SECRET_AREA, 1093),  # B16F At [6,23], 0x10C0 - Soma
    TreasureData(17, 0, "", TreasureContentType.Item, 4289, EO1Regions.B17F_SECRET_AREA_NORTH, 1094, TreasureLogicRequirement([EO1Enemies.KINGDILE]), required_stratum=5),  # B17F At [5,2], 0x10C1 - Somaprime
    TreasureData(17, 1, "C2", TreasureContentType.Item, 4285, EO1Regions.B17F_MAIN, 1095),  # B17F At [7,10], 0x10BD - Amrita II
    TreasureData(17, 2, "D5", TreasureContentType.Item, 2008, EO1Regions.B17F_MAIN, 1096),  # B17F At [24,18], 0x07D8 - Sandy Pin
    TreasureData(18, 0, "", TreasureContentType.Item, 4302, EO1Regions.B18F_WEST, 1097),  # B18F At [1,21], 0x10CE - Axcela II
    TreasureData(19, 0, "E2", TreasureContentType.Money, 1800, EO1Regions.B19F_MAIN, 1098),  # B19F At [9,23], 1800en
    TreasureData(19, 1, "E6", TreasureContentType.Item, 2026, EO1Regions.B19F_MAIN, 1099),  # B19F At [25,23], 0x07EA - Tiger Hand
    TreasureData(20, 0, "North", TreasureContentType.Item, 4291, EO1Regions.B20F_VIOLET_CRYSTAL_ROOM, 1100),  # B20F At [1,11], 0x10C3 - Nectar II
    TreasureData(20, 1, "Middle", TreasureContentType.Item, 4282, EO1Regions.B20F_VIOLET_CRYSTAL_ROOM, 1101),  # B20F At [1,12], 0x10BA - Medica IV
    TreasureData(20, 2, "South", TreasureContentType.Item, 98, EO1Regions.B20F_VIOLET_CRYSTAL_ROOM, 1102),  # B20F At [1,13], 0x0062 - Vine Bow
    TreasureData(20, 3, "C6", TreasureContentType.Item, 4285, EO1Regions.B20F_MAIN, 1103),  # B20F At [29,13], 0x10BD - Amrita II
    TreasureData(21, 0, "A5", TreasureContentType.Item, 2065, EO1Regions.B21F_EAST, 1104),  # B21F At [24,4], 0x0811 - Fur Boot
    TreasureData(21, 1, "F5", TreasureContentType.Item, 4332, EO1Regions.B21F_SOUTH_EAST, 1105),  # B21F At [24,25], 0x10EC - Magnet
    TreasureData(22, 0, "A6", TreasureContentType.Item, 16, EO1Regions.B22F_MAIN, 1106),  # B22F At [27,3], 0x0010 - Pattisa
    TreasureData(22, 1, "North", TreasureContentType.Item, 4291, EO1Regions.B22F_WEST_ELEVATOR, 1107),  # B22F At [5,8], 0x10C3 - Nectar II
    TreasureData(22, 2, "South", TreasureContentType.Money, 3000, EO1Regions.B22F_WEST_ELEVATOR, 1108),  # B22F At [3,17], 3000en
    TreasureData(22, 3, "E5", TreasureContentType.Item, 4285, EO1Regions.B22F_SOUTH_AREA_EAST, 1109),  # B22F At [22,20], 0x10BD - Amrita II
    TreasureData(23, 0, "A4", TreasureContentType.Item, 4291, EO1Regions.B23F_MAIN, 1110),  # B23F At [17,4], 0x10C3 - Nectar II
    TreasureData(23, 1, "D2 North", TreasureContentType.Item, 1039, EO1Regions.B23F_SOUTH_WEST, 1111),  # B23F At [8,17], 0x040F - Composite
    TreasureData(23, 2, "D2 South", TreasureContentType.Item, 4282, EO1Regions.B23F_SOUTH_WEST, 1112),  # B23F At [8,18], 0x10BA - Medica IV
    TreasureData(23, 3, "E6", TreasureContentType.Item, 4289, EO1Regions.B23F_SOUTH_EAST, 1113),  # B23F At [27,20], 0x10C1 - Somaprime
    TreasureData(23, 4, "F3", TreasureContentType.Item, 4374, EO1Regions.B23F_MAIN, 1114),  # B23F At [13,26], 0x1116 - Warp Wire
    TreasureData(24, 0, "A3", TreasureContentType.Item, 2028, EO1Regions.B24F_NORTH, 1115),  # B24F At [11,3], 0x07EC - Blood Gage
    TreasureData(24, 1, "C4 North", TreasureContentType.Item, 4292, EO1Regions.B24F_NORTH, 1116),  # B24F At [17,11], 0x10C4 - Nectar III
    TreasureData(24, 2, "C4 South", TreasureContentType.Item, 4283, EO1Regions.B24F_NORTH, 1117),  # B24F At [18,13], 0x10BB - Medica V
    TreasureData(24, 3, "D4", TreasureContentType.Item, 2010, EO1Regions.B24F_MAIN, 1118),  # B24F At [18,17], 0x07DA - Circlet
    TreasureData(24, 4, "E7", TreasureContentType.Money, 3500, EO1Regions.B24F_MAIN, 1119),  # B24F At [33,20], 3500en
    TreasureData(25, 0, "A1", TreasureContentType.Item, 4291, EO1Regions.B25F_MAIN, 1120),  # B25F At [1,3], 0x10C3 - Nectar II
    TreasureData(25, 1, "A7", TreasureContentType.Item, 1035, EO1Regions.B25F_MAIN, 1121),  # B25F At [33,3], 0x040B - Demon Coat
    TreasureData(25, 2, "F1", TreasureContentType.Item, 4288, EO1Regions.B25F_MAIN, 1122),  # B25F At [1,26], 0x10C0 - Soma
    TreasureData(25, 3, "F7", TreasureContentType.Item, 4287, EO1Regions.B25F_MAIN, 1123),  # B25F At [33,26], 0x10BF - Hamaoprime
    TreasureData(26, 0, "D2", TreasureContentType.Money, 5000, EO1Regions.B26F_MAIN, 1124),  # B26F At [9,15], 5000en
    TreasureData(26, 1, "D6", TreasureContentType.Item, 4292, EO1Regions.B26F_MAIN, 1125),  # B26F At [25,15], 0x10C4 - Nectar III
    TreasureData(26, 2, "E1", TreasureContentType.Item, 4288, EO1Regions.B26F_MAIN, 1126),  # B26F At [3,23], 0x10C0 - Soma
    TreasureData(26, 3, "E7", TreasureContentType.Item, 4303, EO1Regions.B26F_MAIN, 1127),  # B26F At [31,23], 0x10CF - Axcela III
    TreasureData(27, 0, "A1", TreasureContentType.Item, 64, EO1Regions.B27F_NORTH, 1128),  # B27F At [1,1], 0x0040 - Warhammer
    TreasureData(27, 1, "A7", TreasureContentType.Money, 7000, EO1Regions.B27F_NORTH, 1129),  # B27F At [31,1], 7000en
    TreasureData(27, 2, "B2 North", TreasureContentType.Item, 125, EO1Regions.B27F_MAIN, 1130),  # B27F At [9,7], 0x007D - Knout
    TreasureData(27, 3, "B2 South", TreasureContentType.Item, 1041, EO1Regions.B27F_MAIN, 1131),  # B27F At [9,8], 0x0411 - Blood Coat
    TreasureData(27, 4, "E5", TreasureContentType.Item, 4287, EO1Regions.B27F_MAIN, 1132),  # B27F At [23,22], 0x10BF - Hamaoprime
    TreasureData(27, 5, "F3", TreasureContentType.Item, 4289, EO1Regions.B27F_MAIN, 1133),  # B27F At [10,28], 0x10C1 - Somaprime
    TreasureData(28, 0, "", TreasureContentType.Money, 8500, EO1Regions.B28F_DEATHPIT, 1134),  # B28F At [31,15], 8500en
    TreasureData(29, 0, "A2", TreasureContentType.Item, 4292, EO1Regions.B29F_MAIN, 1135),  # B29F At [6,2], 0x10C4 - Nectar III
    TreasureData(29, 1, "A6", TreasureContentType.Item, 4283, EO1Regions.B29F_MAIN, 1136),  # B29F At [26,2], 0x10BB - Medica V
    TreasureData(29, 2, "D3", TreasureContentType.Money, 10000, EO1Regions.B29F_MAIN, 1137),  # B29F At [11,17], 10000en
    TreasureData(29, 3, "F2", TreasureContentType.Item, 4288, EO1Regions.B29F_MAIN, 1138),  # B29F At [6,28], 0x10C0 - Soma
    TreasureData(29, 4, "F6", TreasureContentType.Item, 4292, EO1Regions.B29F_MAIN, 1139),  # B29F At [26,28], 0x10C4 - Nectar III
]

ALL_TREASURE_BY_FLOOR_AND_ID: dict[tuple[int, int], TreasureData] = {(treasure_data.floor_number, treasure_data.chest_id):treasure_data for treasure_data in ALL_TREASURE_DATA}

ALL_TREASURE_BY_LOCATION_ID: dict[int, TreasureData] = {treasure_data.location_id:treasure_data for treasure_data in ALL_TREASURE_DATA}

