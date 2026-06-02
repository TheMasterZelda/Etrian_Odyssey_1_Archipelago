from dataclasses import dataclass

from BaseClasses import ItemClassification

@dataclass(frozen=True)
class EO1ProgressiveFloorLimit:
    ap_item_id: int
    name: str
    floor_amount: int
    weight: int

PROGRESSIVE_FLOOR_LIMIT_1 = EO1ProgressiveFloorLimit(1, "Progressive Floor (1)", 1, weight=150)
PROGRESSIVE_FLOOR_LIMIT_2 = EO1ProgressiveFloorLimit(2, "Progressive Floor (2)", 2, weight=150)
PROGRESSIVE_FLOOR_LIMIT_3 = EO1ProgressiveFloorLimit(3, "Progressive Floor (3)", 3, weight=150)
PROGRESSIVE_FLOOR_LIMIT_4 = EO1ProgressiveFloorLimit(4, "Progressive Floor (4)", 4, weight=100)
PROGRESSIVE_FLOOR_LIMIT_5 = EO1ProgressiveFloorLimit(5, "Progressive Floor (5)", 5, weight=50)
PROGRESSIVE_FLOOR_LIMIT_10 = EO1ProgressiveFloorLimit(10, "Progressive Floor (10)", 10, weight=1)

ALL_PROGRESSIVE_FLOOR_LIMIT: list[EO1ProgressiveFloorLimit] = [
    PROGRESSIVE_FLOOR_LIMIT_1,
    PROGRESSIVE_FLOOR_LIMIT_2,
    PROGRESSIVE_FLOOR_LIMIT_3,
    PROGRESSIVE_FLOOR_LIMIT_4,
    PROGRESSIVE_FLOOR_LIMIT_5,
    PROGRESSIVE_FLOOR_LIMIT_10,
]

PROGRESSIVE_FLOOR_LIMIT_BY_VALUE: dict[int, EO1ProgressiveFloorLimit] = {progressive_floor.floor_amount:progressive_floor for progressive_floor in ALL_PROGRESSIVE_FLOOR_LIMIT}
ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID: dict[int, EO1ProgressiveFloorLimit] = {progressive_floor.ap_item_id:progressive_floor for progressive_floor in ALL_PROGRESSIVE_FLOOR_LIMIT}

@dataclass(frozen=True)
class EO1ProgressiveLevelCap:
    ap_item_id: int
    name: str
    level_amount: int
    weight: int

PROGRESSIVE_LEVEL_CAP_1 = EO1ProgressiveLevelCap(50, "Progressive Level Cap (1)", 1, weight=150)
PROGRESSIVE_LEVEL_CAP_2 = EO1ProgressiveLevelCap(51, "Progressive Level Cap (2)", 2, weight=150)
PROGRESSIVE_LEVEL_CAP_3 = EO1ProgressiveLevelCap(52, "Progressive Level Cap (3)", 3, weight=150)
PROGRESSIVE_LEVEL_CAP_4 = EO1ProgressiveLevelCap(53, "Progressive Level Cap (4)", 4, weight=100)
PROGRESSIVE_LEVEL_CAP_5 = EO1ProgressiveLevelCap(54, "Progressive Level Cap (5)", 5, weight=50)
PROGRESSIVE_LEVEL_CAP_10 = EO1ProgressiveLevelCap(55, "Progressive Level Cap (10)", 10, weight=10)
PROGRESSIVE_LEVEL_CAP_15 = EO1ProgressiveLevelCap(56, "Progressive Level Cap (15)", 15, weight=1)

ALL_PROGRESSIVE_LEVEL_CAP: list[EO1ProgressiveLevelCap] = [
    PROGRESSIVE_LEVEL_CAP_1,
    PROGRESSIVE_LEVEL_CAP_2,
    PROGRESSIVE_LEVEL_CAP_3,
    PROGRESSIVE_LEVEL_CAP_4,
    PROGRESSIVE_LEVEL_CAP_5,
    PROGRESSIVE_LEVEL_CAP_10,
    PROGRESSIVE_LEVEL_CAP_15
]

PROGRESSIVE_LEVEL_CAP_BY_VALUE: dict[int, EO1ProgressiveLevelCap] = {progressive_level.level_amount:progressive_level for progressive_level in ALL_PROGRESSIVE_LEVEL_CAP}
ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID: dict[int, EO1ProgressiveLevelCap] = {progressive_level.ap_item_id:progressive_level for progressive_level in ALL_PROGRESSIVE_LEVEL_CAP}

@dataclass(frozen=True)
class EO1Money:
    ap_item_id: int
    name: str
    amount: int
    classification: ItemClassification
    weight: int

EN200 = EO1Money(900, "200en", 200, ItemClassification.filler, weight=10)
EN400 = EO1Money(901, "400en", 400, ItemClassification.filler, weight=10)
EN500 = EO1Money(902, "500en", 500, ItemClassification.filler | ItemClassification.useful, weight=20)
EN700 = EO1Money(903, "700en", 700, ItemClassification.filler | ItemClassification.useful, weight=20)
EN800 = EO1Money(904, "800en", 800, ItemClassification.filler | ItemClassification.useful, weight=20)
EN900 = EO1Money(905, "900en", 900, ItemClassification.filler | ItemClassification.useful, weight=20)
EN1000 = EO1Money(906, "1000en", 1000, ItemClassification.filler | ItemClassification.useful, weight=20)
EN1400 = EO1Money(907, "1400en", 1400, ItemClassification.filler | ItemClassification.useful, weight=15)
EN1500 = EO1Money(908, "1500en", 1500, ItemClassification.filler | ItemClassification.useful, weight=15)
EN1800 = EO1Money(909, "1800en", 1800, ItemClassification.filler | ItemClassification.useful, weight=15)
EN2000 = EO1Money(910, "2000en", 2000, ItemClassification.filler | ItemClassification.useful, weight=15)
EN3000 = EO1Money(911, "3000en", 3000, ItemClassification.filler | ItemClassification.useful, weight=10)
EN3500 = EO1Money(912, "3500en", 3500, ItemClassification.filler | ItemClassification.useful, weight=10)
EN5000 = EO1Money(913, "5000en", 5000, ItemClassification.filler | ItemClassification.useful, weight=5)
EN7000 = EO1Money(914, "7000en", 7000, ItemClassification.filler | ItemClassification.useful, weight=3)
EN8500 = EO1Money(915, "8500en", 8500, ItemClassification.filler | ItemClassification.useful, weight=2)
EN10000 = EO1Money(916, "10000en", 10000, ItemClassification.filler | ItemClassification.useful, weight=1)

ALL_MONEY_ITEMS: list[EO1Money] = [
    EN200,
    EN400,
    EN500,
    EN700,
    EN800,
    EN900,
    EN1000,
    EN1400,
    EN1500,
    EN1800,
    EN2000,
    EN3000,
    EN3500,
    EN5000,
    EN7000,
    EN8500,
    EN10000
]

ALL_MONEY_BY_ID: dict[int, EO1Money] = {money_data.ap_item_id:money_data for money_data in ALL_MONEY_ITEMS}

