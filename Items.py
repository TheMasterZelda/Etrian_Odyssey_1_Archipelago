from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item
import math
from .data.ClassData import *
from .data.SkillData import *
from .data.SkillUnlockData import *
from .data.InventoryItemData import *
from .data.ItemData import *
from .Constant import GAME_NAME
from enum import IntEnum, Enum
from .Options import *

if TYPE_CHECKING:
    from . import EtrianOdysseyWorld

# Note regarding item ids:
# Progressive Floor use id 1 to 10
# Progressive Level use id 50 to 56
# Class use id 100 to 108
# Skill use id 200 to 388
# Special Skill items use id 600 to 699
# Special Skill items use id 700 to 750
# Money use id 900 to 916
# Items use id 1001 to 2243

class EtrianOdysseyItemType(Enum):
    EVENT = -1
    INVENTORY = 0
    MONEY = 1
    PROGRESSIVE_FLOOR_LIMIT = 2
    PROGRESSIVE_LEVEL_CAP = 3
    CLASS = 4
    SKILL = 5

class EtrianOdysseyItem(Item):
    game = GAME_NAME
    item_type: EtrianOdysseyItemType

def create_item_from_item_data(item_data: EO1ItemData, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(item_data.name, item_data.classification, item_data.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.INVENTORY
    return item

def create_item_from_money_data(money_data: EO1Money, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(money_data.name, money_data.classification, money_data.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.MONEY
    return item

def create_item_from_progressive_floor(progressive_floor: EO1ProgressiveFloorLimit, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(progressive_floor.name, ItemClassification.progression, progressive_floor.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT
    return item

def create_item_from_progressive_level(progressive_level: EO1ProgressiveLevelCap, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(progressive_level.name, ItemClassification.progression, progressive_level.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP
    return item

def create_item_from_class_data(class_data: EO1ClassData, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(class_data.name, ItemClassification.progression, class_data.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.CLASS
    return item

def create_item_from_skill_item(skill_data: SkillItem, player: int | None) -> EtrianOdysseyItem:
    item = EtrianOdysseyItem(skill_data.ap_item_name, ItemClassification.progression, skill_data.ap_item_id, player)
    item.item_type = EtrianOdysseyItemType.SKILL
    return item

ALL_ITEMS_BY_ID: dict[int, EtrianOdysseyItem] = {
    **{item_data.ap_item_id:create_item_from_item_data(item_data, None) for item_data in ALL_ITEM_DATA},
    **{money_data.ap_item_id:create_item_from_money_data(money_data, None) for money_data in ALL_MONEY_ITEMS},
    **{progressive_floor.ap_item_id:create_item_from_progressive_floor(progressive_floor, None) for progressive_floor in ALL_PROGRESSIVE_FLOOR_LIMIT},
    **{progressive_level.ap_item_id:create_item_from_progressive_level(progressive_level, None) for progressive_level in ALL_PROGRESSIVE_LEVEL_CAP},
    **{class_data.ap_item_id:create_item_from_class_data(class_data, None) for class_data in ALL_CLASS_DATA},
    **{skill_item.ap_item_id:create_item_from_skill_item(skill_item, None) for skill_item in ALL_SKILLS_ITEMS}
}
ITEMS_ID_BY_NAME: dict[str, int] = {ALL_ITEMS_BY_ID[item_id].name:item_id for item_id in ALL_ITEMS_BY_ID}

def get_random_filler_consumable(world: EtrianOdysseyWorld) -> str:
    all_consumable_name = [consumable_data.name for consumable_data in CONSUMABLE_DATA]
    all_consumable_weight = [consumable_data.weight for consumable_data in CONSUMABLE_DATA]
    result = world.random.choices(all_consumable_name, weights=all_consumable_weight, k=1)
    return result[0]

def get_random_filler_money(world: EtrianOdysseyWorld) -> str:
    all_money_name = [money_data.name for money_data in ALL_MONEY_ITEMS]
    all_money_weight = [money_data.weight for money_data in ALL_MONEY_ITEMS]
    result = world.random.choices(all_money_name, weights=all_money_weight, k=1)
    return result[0]

def get_random_filler_item_name(world: EtrianOdysseyWorld) -> str:
    # todo handle equipments?
    item_roll_value = world.random.randint(0, 100)
    if item_roll_value <= 20: # 20% of items are money.
        return get_random_filler_money(world)
    # Consumable it is.
    return get_random_filler_consumable(world)

def create_item_from_name(world: EtrianOdysseyWorld, name: str) -> EtrianOdysseyItem:
    item_id = ITEMS_ID_BY_NAME[name]
    item_base = ALL_ITEMS_BY_ID[item_id]
    item = EtrianOdysseyItem(item_base.name, item_base.classification, item_base.code, world.player)
    item.item_type = item_base.item_type
    return item

def randomly_pick_progressive_items(world: EtrianOdysseyWorld, total_value: int, extra_count: int, values: list[tuple[int, int]]) -> list[int]:
    def filter_list(max_value: int, values_to_filter: list[tuple[int, int]]) -> list[tuple[int, int]]:
        #filtered_values: list[tuple[int, int]] = []
        #for value in values_to_filter:
        #    if value[0] <= max_value:
        #        filtered_values.append(value)
        #return filtered_values
        return [value for value in values_to_filter if value[0] <= max_value]

    def pick_one(options: list[tuple[int, int]], ) -> int:
        valid_option_values = [option[0] for option in options]
        valid_option_weights = [option[1] for option in options]
        option = world.random.choices(valid_option_values, weights=valid_option_weights, k=1)
        return option[0]

    result_items: list[int] = []
    remaining_value = total_value

    while remaining_value > 0:
        valid_options = filter_list(remaining_value, values)
        selected_option = pick_one(valid_options)
        result_items.append(selected_option)
        remaining_value -= selected_option

    # If there are no valid options, skip the extra items. This mean the player shuffled something but set the default value to the max.
    valid_options = filter_list(total_value, values)
    if len(valid_options) == 0:
        return result_items

    for _ in range(extra_count):
        selected_option = pick_one(valid_options)
        result_items.append(selected_option)

    return result_items

def get_progressive_level_cap_items(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:
    extra_count = world.options.extra_progressive_level_cap_items.value
    initial_level = world.options.initial_level_cap.value
    max_level = get_max_level_for_goal(EO1Goal(world.options.goal.value))
    missing_level_to_max = max_level - initial_level
    if world.options.level_cap_mode == LevelCapMode.option_none:
        return []
    elif world.options.level_cap_mode == LevelCapMode.option_fixed_increase:
        level_cap_item_data = PROGRESSIVE_LEVEL_CAP_BY_VALUE[world.options.level_cap_increase_value.value]
        item_amount = math.ceil(missing_level_to_max / level_cap_item_data.level_amount)
        return [create_item_from_progressive_level(level_cap_item_data, world.player) for _ in range(item_amount + extra_count)]
    elif world.options.level_cap_mode == LevelCapMode.option_complete_shuffle:
        level_options: list[tuple[int, int]] = [(level_cap_data.level_amount, level_cap_data.weight)
                                                for level_cap_data in ALL_PROGRESSIVE_LEVEL_CAP]

        randomly_selected_level_caps = randomly_pick_progressive_items(world, missing_level_to_max, extra_count, level_options)

        return [create_item_from_progressive_level(PROGRESSIVE_LEVEL_CAP_BY_VALUE[level_cap], world.player)
                for level_cap in randomly_selected_level_caps]

    raise Exception("Not implemented")

def get_progressive_floor_limit_items(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:
    extra_count = world.options.extra_progressive_floor_limit.value
    initial_floor = world.options.initial_floor_limit.value
    max_floor = get_max_floor_for_goal(EO1Goal(world.options.goal.value))
    missing_floor_to_max = max_floor - initial_floor
    if world.options.floor_limit_mode == FloorLimitMode.option_none:
        return []
    elif world.options.floor_limit_mode == FloorLimitMode.option_fixed_increase:
        floor_limit_item_data = PROGRESSIVE_FLOOR_LIMIT_BY_VALUE[world.options.floor_limit_increase_value.value]
        item_amount = math.ceil(missing_floor_to_max / floor_limit_item_data.floor_amount)
        return [create_item_from_progressive_floor(floor_limit_item_data, world.player) for _ in range(item_amount + extra_count)]
    elif world.options.floor_limit_mode == FloorLimitMode.option_complete_shuffle:
        floor_options: list[tuple[int, int]] = [(floor_data.floor_amount, floor_data.weight)
                                                for floor_data in ALL_PROGRESSIVE_FLOOR_LIMIT]

        randomly_selected_floor_limit = randomly_pick_progressive_items(world, missing_floor_to_max, extra_count, floor_options)

        return [create_item_from_progressive_floor(PROGRESSIVE_FLOOR_LIMIT_BY_VALUE[floor_data], world.player)
                for floor_data in randomly_selected_floor_limit]

    raise Exception("Not implemented")

def __build_individual_skill_sanity_pool(shuffle_generic_stats_increase_skill: bool, shuffle_mastery_skills: bool, shuffle_gathering_skills: bool) -> list[SkillItem]:
    skill_pool: list[SkillItem] = []

    if shuffle_generic_stats_increase_skill:
        skill_pool.extend(make_skill_items_from_skill_list(EO1SkillPools.INDIVIDUAL_GENERIC_STATS_INCREASE_SKILLS))

    if shuffle_mastery_skills:
        skill_pool.extend(make_skill_items_from_skill_list(EO1SkillPools.INDIVIDUAL_MASTERY_SKILLS))

    if shuffle_gathering_skills:
        skill_pool.extend(make_skill_items_from_skill_list(EO1SkillPools.INDIVIDUAL_GATHERING_SKILLS))

    skill_pool.extend(make_skill_items_from_skill_list(EO1SkillPools.INDIVIDUAL_ALL_OTHER_SKILLS))

    return skill_pool

def __build_group_skill_sanity_pool(shuffle_generic_stats_increase_skill: bool, shuffle_gathering_skills: bool) -> list[SkillItem]:
    skill_pool: list[SkillItem] = []

    if shuffle_generic_stats_increase_skill:
        skill_pool.extend([skill_group.to_skill_item() for skill_group in ALL_STATS_GROUP_SKILLS])

    if shuffle_gathering_skills:
        skill_pool.extend([skill_group.to_skill_item() for skill_group in ALL_GATHERING_GROUP_SKILLS])

    skill_pool.extend([skill_group.to_skill_item() for skill_group in ALL_OTHER_GROUP_SKILLS])

    return skill_pool

def __get_skill_item_pool(world: EtrianOdysseyWorld) -> list[SkillItem]:
    skill_sanity_mode = SkillSanityType(world.options.skill_sanity_mode.value)
    if skill_sanity_mode == SkillSanityType.none:
        return [] # No skill items in the pool when skill sanity is off.

    shuffle_generic_stats_increase_skills = bool(world.options.shuffle_generic_stats_increase_skills.value)
    shuffle_mastery_skills = bool(world.options.shuffle_mastery_skills.value)
    shuffle_gathering_skills = bool(world.options.shuffle_gathering_skills.value)
    if skill_sanity_mode == SkillSanityType.shuffle_individually:
        return __build_individual_skill_sanity_pool(shuffle_generic_stats_increase_skills, shuffle_mastery_skills, shuffle_gathering_skills)
    elif skill_sanity_mode == SkillSanityType.shuffle_group:
        return __build_group_skill_sanity_pool(shuffle_generic_stats_increase_skills, shuffle_gathering_skills)

    raise Exception(f"Skill Sanity Mode {skill_sanity_mode} not implemented.")

def __get_random_skill_item_for_class(world: EtrianOdysseyWorld, class_name: str, skill_item_pool: list[SkillItem], skill_item_count: int) -> list[SkillItem]:
    effective_skill_item_pool: list[SkillItem] = []

    for skill_item in skill_item_pool:
        if skill_item.skill_item_type == SkillItemType.INDIVIDUAL:
            if class_name == get_class_name_for_skill_item(skill_item):
                effective_skill_item_pool.append(skill_item)
        elif skill_item.skill_item_type == SkillItemType.GROUP:
            if class_name == get_class_name_for_skill_item(skill_item):
                effective_skill_item_pool.append(skill_item)
        else:
            raise Exception(f"Unsupported Skill Item Type {skill_item.skill_item_type} for class based selection.")

    effective_skill_item_count = min(skill_item_count, len(effective_skill_item_pool))
    return world.random.sample(effective_skill_item_pool, k=effective_skill_item_count)

def get_starting_skill_items(world: EtrianOdysseyWorld) -> list[SkillItem]:
    skill_sanity_mode = SkillSanityType(world.options.skill_sanity_mode.value)
    if skill_sanity_mode == SkillSanityType.none:
        return [SkillUnlockItems.ALL_SKILLS]

    starting_skills: list[SkillItem] = []

    if not world.options.shuffle_generic_stats_increase_skills:
        starting_skills.append(SkillUnlockItems.ALL_STATS_SKILLS.to_skill_item())

    if not world.options.shuffle_mastery_skills:
        starting_skills.append(SkillUnlockItems.ALL_MASTERY_SKILLS.to_skill_item())

    if not world.options.shuffle_gathering_skills:
        starting_skills.append(SkillUnlockItems.ALL_GATHERING_SKILLS.to_skill_item())

    starting_skill_item_count = world.options.starting_skill_item_count.value

    if skill_sanity_mode == SkillSanityType.shuffle_individually:
        skill_item_pool = __get_skill_item_pool(world)
        if starting_skill_item_count == 0:
            return starting_skills
        for class_data in ALL_CLASS_DATA:
            starting_class_skills = __get_random_skill_item_for_class(world, class_data.name, skill_item_pool, starting_skill_item_count)
            starting_skills.extend(starting_class_skills)
        return starting_skills
    elif skill_sanity_mode == SkillSanityType.shuffle_group:
        skill_item_pool = __get_skill_item_pool(world)
        if starting_skill_item_count == 0:
            return starting_skills
        for class_data in ALL_CLASS_DATA:
            starting_class_skills = __get_random_skill_item_for_class(world, class_data.name, skill_item_pool, starting_skill_item_count)
            starting_skills.extend(starting_class_skills)
        return starting_skills

    raise Exception(f"Skill Sanity Mode {skill_sanity_mode} not implemented.")

def get_shuffled_skill_items(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:
    skill_sanity_mode = SkillSanityType(world.options.skill_sanity_mode.value)
    if skill_sanity_mode == SkillSanityType.none:
        return []

    starting_skill_ap_item_ids = {skill_item.ap_item_id for skill_item in world.starting_skills}

    skill_item_pool = __get_skill_item_pool(world)

    shuffled_skill_items = [
        skill_item
        for skill_item in skill_item_pool
        if skill_item.ap_item_id not in starting_skill_ap_item_ids
    ]

    return [create_item_from_skill_item(skill_item, world.player) for skill_item in shuffled_skill_items]

def get_starting_classes(world: EtrianOdysseyWorld) -> list[EO1ClassData]:
    class_sanity_mode = ClassSanityType(world.options.class_sanity_mode.value)
    if class_sanity_mode == ClassSanityType.vanilla:
        return [
            CLASS_DATA_BY_NAME[EO1Class.LANDSKNECHT],
            CLASS_DATA_BY_NAME[EO1Class.SURVIVALIST],
            CLASS_DATA_BY_NAME[EO1Class.PROTECTOR],
            CLASS_DATA_BY_NAME[EO1Class.DARK_HUNTER],
            CLASS_DATA_BY_NAME[EO1Class.MEDIC],
            CLASS_DATA_BY_NAME[EO1Class.ALCHEMIST],
            CLASS_DATA_BY_NAME[EO1Class.TROUBADOUR]
        ]
    elif class_sanity_mode == ClassSanityType.start_with_all:
        return ALL_CLASS_DATA
    elif class_sanity_mode == ClassSanityType.shuffle_availability:
        count = world.options.starting_class_count.value
        return world.random.sample(ALL_CLASS_DATA, k=count)
    raise Exception(f"Unknown Class Sanity Mode {class_sanity_mode}")

def get_shuffled_classes(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:
    missing_classes = [class_data for class_data in ALL_CLASS_DATA if class_data.name not in world.starting_classes]
    return [create_item_from_class_data(class_data, world.player) for class_data in missing_classes]

def get_shuffled_key_items(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:
    key_items: list[EtrianOdysseyItem] = [
        create_item_from_item_data(KEY_ITEM_DATA_BY_ITEM_ID[EO1ItemID.CLEAR_KEY], world.player),
        create_item_from_item_data(KEY_ITEM_DATA_BY_ITEM_ID[EO1ItemID.VIOLET_KEY], world.player)
    ]

    if bool(world.options.shuffle_radha_note):
        key_items.append(create_item_from_item_data(KEY_ITEM_DATA_BY_ITEM_ID[EO1ItemID.RADHA_NOTE], world.player))

    return key_items

def create_all_items(world: EtrianOdysseyWorld) -> list[EtrianOdysseyItem]:

    pool = []
    pool += get_progressive_level_cap_items(world)
    pool += get_progressive_floor_limit_items(world)
    pool += get_shuffled_classes(world)
    pool += get_shuffled_key_items(world)
    pool += get_shuffled_skill_items(world)

    number_of_items = len(pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items < 0:
        raise Exception(f"There are not enough locations to fit all progression items. There are "
                        f"{abs(needed_number_of_filler_items)} too many progression items. "
                        "Please add more locations or reduce the amount of progression items "
                        "(level cap, floor limit, class, skills)")

    pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    return pool