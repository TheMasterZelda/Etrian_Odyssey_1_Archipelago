from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .Constant import GAME_VERSION
from .Locations import *
from .Items import *
from .data.ClassData import EO1Class, ALL_CLASS_DATA
from .data.Events import EVENT_BY_NAME
from .data.QuestData import QUEST_DATA_BY_LOCATION_ID
from .data.SkillUnlockData import SkillItem

if TYPE_CHECKING:
    from . import EtrianOdysseyWorld

def __patch_treasure_box(location: Location, player: int) -> dict[str, int]:
    location_id = ALL_LOCATIONS_ID_BY_NAME[location.name]
    location_type = ALL_LOCATIONS_BY_ID[location_id].location_type
    if location_type != EtrianOdysseyLocationType.TREASURE_BOX:
        raise Exception(f"Location {location.name} is not a treasure box.")

    treasure_data = ALL_TREASURE_BY_LOCATION_ID[location_id]
    treasure_type = 0
    treasure_value = 0

    if location.item is None:
        raise Exception(f"Location {location.name} has no item assigned to it.")

    if location.item.player != player:
        treasure_type = 4
        treasure_value = 0
    else:
        item_id = ITEMS_ID_BY_NAME[location.item.name]
        item_type = ALL_ITEMS_BY_ID[item_id].item_type
        if item_type == EtrianOdysseyItemType.MONEY:
            treasure_type = 2
            treasure_value = ALL_MONEY_BY_ID[item_id].amount
        elif item_type == EtrianOdysseyItemType.INVENTORY:
            treasure_type = 3
            treasure_value = ITEM_PER_AP_ITEM_ID[item_id].item_id
        # elif item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
        #    treasure_type = 5
        #    treasure_value = ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item_id].floor_amount
        # elif item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
        #    treasure_type = 6
        #    treasure_value = ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item_id].level_amount
        # elif item_type == EtrianOdysseyItemType.CLASS:
        #    treasure_type = 7
        #    treasure_value = ALL_CLASS_BY_ITEM_ID[item_id].class_id
        else:
            treasure_type = 8
            treasure_value = 0

    def generate_treasure_box_patch_data(floor: int, chest_id: int, type: int, value: int) -> dict[str, int]:
        return {
            "floor": floor,
            "treasure_id": chest_id,
            "treasure_type": type,
            "treasure_value": value
        }

    return generate_treasure_box_patch_data(treasure_data.floor_number - 1, treasure_data.chest_id, treasure_type, treasure_value)

def __patch_quest_hint(location: Location, player: int, player_names: dict[int, str]) -> dict[str, Any]:
    location_id = ALL_LOCATIONS_ID_BY_NAME[location.name]
    location_type = ALL_LOCATIONS_BY_ID[location_id].location_type
    if location_type != EtrianOdysseyLocationType.QUEST_COMPLETION:
        raise Exception(f"Location {location.name} is not a quest completion.")

    quest_id = QUEST_DATA_BY_LOCATION_ID[location_id].quest_id
    item_player_id = location.item.player
    item_player_name = player_names[item_player_id]
    item_name = location.item.name

    return {
        "quest_id": quest_id,
        "item_player_id": item_player_id,
        "item_player_name": item_player_name,
        "item_name": item_name,
    }

def __patch_individual_location(location: Location, player: int, player_names: dict[int, str], hint_quest_rewards: bool, output_data):
    if location.name in EVENT_BY_NAME:
        return

    location_id = ALL_LOCATIONS_ID_BY_NAME[location.name]
    location_type = ALL_LOCATIONS_BY_ID[location_id].location_type
    if location_type == EtrianOdysseyLocationType.TREASURE_BOX:
        output_data["TreasureBoxes"].append(__patch_treasure_box(location, player))
    elif location_type == EtrianOdysseyLocationType.QUEST_COMPLETION:
        # No need to check for quest sanity since locations only exists if its enabled.
        if not hint_quest_rewards:
            return
        output_data["QuestHints"].append(__patch_quest_hint(location, player, player_names))


def generate_output(world: EtrianOdysseyWorld):
    multiworld = world.multiworld
    player = world.player
    hint_quest_rewards = bool(world.options.quest_completion_reward_hint)
    output_data = {
        "Version": GAME_VERSION,
        "Seed": multiworld.seed_name,
        "Slot": player,
        "Name": world.player_name,
        "InitialValues": {},
        "TreasureBoxes": [],
        "QuestHints": []
    }

    if world.options.level_cap_mode != 0:
        output_data["InitialValues"]["level_cap"] = world.initial_level_cap
    if world.options.floor_limit_mode != 0:
        output_data["InitialValues"]["floor_limit"] = world.initial_floor_limit

    output_data["RemoveSkillsRequirements"] = bool(world.options.remove_skills_requirements)
    output_data["MinimizeQuestMaterialGrind"] = bool(world.options.minimize_quest_material_grind)
    output_data["ShopUnlockMaterialCostDivider"] = int(world.options.shop_unlock_material_cost_divider.value)
    output_data["MaterialSellValueMultiplier"] = int(world.options.material_sell_value_multiplier.value)

    output_data["InitialValues"]["experience_modifier"] = int(world.options.experience_modifier)

    output_data["InitialValues"]["landsknecht_unlocked"] = EO1Class.LANDSKNECHT in world.starting_classes
    output_data["InitialValues"]["survivalist_unlocked"] = EO1Class.SURVIVALIST in world.starting_classes
    output_data["InitialValues"]["protector_unlocked"] = EO1Class.PROTECTOR in world.starting_classes
    output_data["InitialValues"]["dark_hunter_unlocked"] = EO1Class.DARK_HUNTER in world.starting_classes
    output_data["InitialValues"]["medic_unlocked"] = EO1Class.MEDIC in world.starting_classes
    output_data["InitialValues"]["alchemist_unlocked"] = EO1Class.ALCHEMIST in world.starting_classes
    output_data["InitialValues"]["troubadour_unlocked"] = EO1Class.TROUBADOUR in world.starting_classes
    output_data["InitialValues"]["ronin_unlocked"] = EO1Class.RONIN in world.starting_classes
    output_data["InitialValues"]["hexer_unlocked"] = EO1Class.HEXER in world.starting_classes

    # Handle Starting Skills.
    skill_values: list[int] = []
    for index in range(9):
        skill_values.append(0)

    cumulative_skill_items: list[SkillItem] = []
    for skill_item in world.starting_skills:
        skill_values = apply_skill_item_to_values(skill_item, skill_values, cumulative_skill_items)
        cumulative_skill_items.append(skill_item)

    for class_data in ALL_CLASS_DATA:
        output_data["InitialValues"][f"{class_data.name.lower().replace(' ', '_')}_skills"] = skill_values[class_data.class_id]

    # Handle location item patching.
    for location in multiworld.get_locations(player):
        __patch_individual_location(location, player, multiworld.player_name, hint_quest_rewards, output_data)

    return output_data

