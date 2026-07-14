from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Location, ItemClassification
from .Items import EtrianOdysseyItem, EtrianOdysseyItemType
from .Rules import *
from .data.EnemyData import EO1Enemies
from .data.ItemCompoundData import EO1ItemCompound, SHOP_UNLOCK_BY_LOCATION_ID
from .data.QuestData import QuestData, ALL_QUEST_DATA
from .data.RegionData import EO1Regions, ALL_REGIONS
from .data.TreasureData import *
from .data.MissionData import *
from .data.CodexData import *
from .data.CompendiumData import *
from .data.Events import *
from .Constant import *
from enum import IntEnum, Enum

if TYPE_CHECKING:
    from . import EtrianOdysseyWorld

# Note regarding location ids:
# Missions use id 1 to 7.
# Treasure Chest use id 1000 to 1139.
# Codex use id 2000 to 2131.
# Compendium use id 3000 to 3195.
# Quests use id 4000 to 4999.
# Shop use id 5000 to 5999.

class EtrianOdysseyLocationType(Enum):
    TREASURE_BOX = 0
    MISSION_CLEAR = 1
    QUEST_COMPLETION = 2
    CODEX_ENTRY = 3
    COMPENDIUM_ENTRY = 4
    SHOP_ENTRY = 5
    #FOE
    #LABYRINTH_EVENT
    #TILE


class EtrianOdysseyLocation(Location):
    game = GAME_NAME
    location_type: EtrianOdysseyLocationType

def create_location_from_treasure_data(treasure_data: TreasureData) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, treasure_data.get_full_name())
    location.location_type = EtrianOdysseyLocationType.TREASURE_BOX
    return location

def create_location_from_mission_data(mission_data: MissionData) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, mission_data.get_full_name())
    location.location_type = EtrianOdysseyLocationType.MISSION_CLEAR
    return location

def create_location_from_codex_data(codex_data: CodexData) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, codex_data.get_full_name())
    location.location_type = EtrianOdysseyLocationType.CODEX_ENTRY
    return location

def create_location_from_compendium_data(compendium_data: CompendiumData) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, compendium_data.get_full_name())
    location.location_type = EtrianOdysseyLocationType.COMPENDIUM_ENTRY
    return location

def create_location_from_quest_data(quest_data: QuestData) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, quest_data.get_full_location_name())
    location.location_type = EtrianOdysseyLocationType.QUEST_COMPLETION
    return location

def create_location_from_shop_data(shop_data: EO1ItemCompound) -> EtrianOdysseyLocation:
    location = EtrianOdysseyLocation(None, shop_data.get_full_location_name())
    location.location_type = EtrianOdysseyLocationType.SHOP_ENTRY
    return location

def location_is_handled_in_game(location_id: int) -> bool:
    if location_id == -1:
        return False
    if location_id not in ALL_LOCATIONS_BY_ID:
        return False

    location = ALL_LOCATIONS_BY_ID[location_id]
    return location.location_type == EtrianOdysseyLocationType.TREASURE_BOX

ALL_LOCATIONS_BY_ID: dict[int, EtrianOdysseyLocation] = {
    **{treasure_data.location_id: create_location_from_treasure_data(treasure_data) for treasure_data in ALL_TREASURE_DATA},
    **{mission_data.location_id: create_location_from_mission_data(mission_data) for mission_data in ALL_MISSION_DATA},
    **{codex_data.location_id: create_location_from_codex_data(codex_data) for codex_data in ALL_CODEX_ENTRIES},
    **{compendium_data.location_id: create_location_from_compendium_data(compendium_data) for compendium_data in COMPENDIUM_TABLE},
    **{quest_data.location_id: create_location_from_quest_data(quest_data) for quest_data in ALL_QUEST_DATA},
    **{shop_data.ap_location_id: create_location_from_shop_data(shop_data) for shop_data in SHOP_UNLOCK_BY_LOCATION_ID.values()}
}
ALL_LOCATIONS_ID_BY_NAME: dict[str, int] = {ALL_LOCATIONS_BY_ID[location_id].name:location_id for location_id in ALL_LOCATIONS_BY_ID}

def create_all_locations(world: EtrianOdysseyWorld) -> None:
    create_treasure_locations(world)
    create_mission_clear_locations(world)

    if bool(world.options.codex_sanity.value):
        create_codex_locations(world)

    if bool(world.options.compendium_sanity.value):
        create_compendium_locations(world)

    if bool(world.options.quest_sanity.value):
        create_quest_completion_locations(world)

    if bool(world.options.shop_unlock_sanity.value):
        create_shop_locations(world)

def __any_enemy_in_goal(enemy_list: set[int], max_stratum: int) -> bool:
    for enemy_id in enemy_list:
        codex_data = CODEX_DATA_BY_ENEMY_ID[enemy_id]
        if codex_data.required_stratum > max_stratum:
            continue
        # TODO Filter on options for Quest Monsters here? Only affect optional boss drops.
        return True
    return False

def __any_gathering_spot_in_goal(gathering_spot_list: set[int], regions: set[str]) -> bool:
    for gathering_spot_unique_id in gathering_spot_list:
        gathering_spot_data = GATHERING_SPOT_BY_UNIQUE_ID[gathering_spot_unique_id]

        if gathering_spot_data.region in regions:
            return True
    return False

def __compendium_entry_is_in_goal(compendium_entry: CompendiumData, max_stratum: int, regions: set[str], options: EtrianOdysseyOptions) -> bool:
    if compendium_entry.conditional_drop:
        if not bool(options.compendium_sanity_include_conditional_drops):
            return False

    if compendium_entry.required_stratum is not None:
        if compendium_entry.required_stratum > max_stratum:
            return False

    if compendium_entry.source == CompendiumSource.MONSTER:
        return __any_enemy_in_goal(ENEMY_BY_DROP_ID[compendium_entry.item_id], max_stratum)
    elif compendium_entry.source == CompendiumSource.GATHERING:
        return __any_gathering_spot_in_goal(GATHERING_SPOT_BY_ITEM_ID[compendium_entry.item_id], regions)
    elif compendium_entry.source == CompendiumSource.BOTH:
        if __any_enemy_in_goal(ENEMY_BY_DROP_ID[compendium_entry.item_id], max_stratum):
            return True
        if __any_gathering_spot_in_goal(GATHERING_SPOT_BY_ITEM_ID[compendium_entry.item_id], regions):
            return True
        return False
    else:
        raise Exception(f"Unknown compendium source: {compendium_entry.source}")

def create_shop_locations(world: EtrianOdysseyWorld) -> None:
    shop_region = world.get_region(EO1Regions.SHILLEKA)
    max_stratum = get_max_stratum_for_goal(EO1Goal(world.options.goal.value))
    regions: set[str] = {region.name for region in world.get_regions()}

    def create_location(shop_entry: EO1ItemCompound):
        location = EtrianOdysseyLocation(world.player, shop_entry.get_full_location_name(), shop_entry.ap_location_id, shop_region)
        shop_region.locations.append(location)
        access_rule = CanUnlockShopItem(shop_entry.item_id)
        world.set_rule(location, access_rule)

    def material_is_in_goal(item_id: int) -> bool:
        if item_id == 0:
            return True

        if item_id not in COMPENDIUM_BY_ITEM_ID:
            raise Exception(f"Unknown material item id: {item_id}")

        compendium_entry = COMPENDIUM_BY_ITEM_ID[item_id]
        return __compendium_entry_is_in_goal(compendium_entry, max_stratum, regions, world.options)

    for shop_data in SHOP_UNLOCK_BY_LOCATION_ID.values():
        if not material_is_in_goal(shop_data.material_1_id):
            continue
        if not material_is_in_goal(shop_data.material_2_id):
            continue
        if not material_is_in_goal(shop_data.material_3_id):
            continue

        create_location(shop_data)


def create_quest_completion_locations(world: EtrianOdysseyWorld) -> None:
    pub_region = world.get_region(EO1Regions.PUB)
    max_stratum = get_max_stratum_for_goal(EO1Goal(world.options.goal.value))

    def create_location(quest: QuestData):
        location = EtrianOdysseyLocation(world.player, quest.get_full_location_name(), quest.location_id, pub_region)
        pub_region.locations.append(location)
        access_rule = CanCompleteQuest(quest.quest_id)
        world.set_rule(location, access_rule)

    for quest_data in ALL_QUEST_DATA:
        # Filter quests based on the max stratum.
        if quest_data.required_stratum > max_stratum:
            continue

        create_location(quest_data)

def create_codex_locations(world: EtrianOdysseyWorld) -> None:
    radha_hall_region = world.get_region(EO1Regions.RADHA_HALL)
    max_stratum = get_max_stratum_for_goal(EO1Goal(world.options.goal.value))
    quest_monsters_enabled = bool(world.options.codex_sanity_include_quest_monsters.value)

    def create_location(codex: CodexData):
        location = EtrianOdysseyLocation(world.player, codex.get_full_name(), codex.location_id, radha_hall_region)
        radha_hall_region.locations.append(location)
        access_rule = CanFillCodexEntry(codex.enemy_id)
        world.set_rule(location, access_rule)

    for codex_data in ALL_CODEX_ENTRIES:
        # Filter the codex entry based on the max stratum.
        if codex_data.required_stratum > max_stratum:
            continue

        if codex_data.encounter_type == CodexEncounterType.QUEST:
            if not quest_monsters_enabled:
                continue

        create_location(codex_data)

def create_compendium_locations(world: EtrianOdysseyWorld) -> None:
    radha_hall_region = world.get_region(EO1Regions.RADHA_HALL)
    max_stratum = get_max_stratum_for_goal(EO1Goal(world.options.goal.value))
    regions: set[str] = {region.name for region in world.get_regions()}

    def create_location(compendium: CompendiumData):
        location = EtrianOdysseyLocation(world.player, compendium.get_full_name(), compendium.location_id, radha_hall_region)
        radha_hall_region.locations.append(location)
        access_rule = CanFillCompendiumEntry(compendium.item_id)
        world.set_rule(location, access_rule)

    for compendium_data in COMPENDIUM_TABLE:
        if not __compendium_entry_is_in_goal(compendium_data, max_stratum, regions, world.options):
            continue

        create_location(compendium_data)

def create_treasure_locations(world: EtrianOdysseyWorld) -> None:
    goal = EO1Goal(world.options.goal.value)
    regions: set[str] = {region.name for region in world.get_regions()}

    def create_location(treasure_location: TreasureData, region: Region):
        location = EtrianOdysseyLocation(world.player,
                                         treasure_location.get_full_name(),
                                         treasure_location.location_id,
                                         region)
        region.locations.append(location)
        if not treasure_location.require_access_rule():
            return

        access_rules: list[Rule] = []

        if treasure_location.logic_requirement.require_escape:
            access_rules.append(CanEscape())
        if len(treasure_location.logic_requirement.mandatory_enemies) > 0:
            enemy_rules: list[CanDefeatEnemy] = []
            for enemy_id in treasure_location.logic_requirement.mandatory_enemies:
                enemy_rules.append(CanDefeatEnemy(enemy_id))
            access_rules.append(And(*enemy_rules))

        access_rule = Or(*access_rules)
        world.set_rule(location, access_rule)

    for treasure_data in ALL_TREASURE_DATA:
        if treasure_data.region not in regions:
            continue

        # Skip chests requiring beyond the goal stratum.
        if treasure_data.required_stratum is not None:
            if treasure_data.required_stratum > get_max_stratum_for_goal(goal):
                continue

        region = world.get_region(treasure_data.region)
        create_location(treasure_data, region)

def create_mission_clear_locations(world: EtrianOdysseyWorld) -> None:
    # Missions are a fair bit more complex, and are handled manually.
    goal = EO1Goal(world.options.goal.value)
    radha_hall_region = world.get_region(EO1Regions.RADHA_HALL)

    def create_location(mission_data: MissionData):
        location = EtrianOdysseyLocation(world.player, mission_data.get_full_name(), mission_data.location_id, radha_hall_region)
        radha_hall_region.locations.append(location)
        access_rule = get_mission_access_rule(world, mission_data.mission_id)
        world.set_rule(location, access_rule)

    # Note: We don't include missions that are the goal themselves.

    # Mission 1
    create_location(MISSION_1_DATA)

    if goal <= EO1Goal.defeat_fenrir.value:
        return

    # Mission 2
    create_location(MISSION_2_DATA)

    # Mission 3
    create_location(MISSION_3_DATA)

    if goal <= EO1Goal.defeat_cernunos.value:
        return

    # Mission 4
    create_location(MISSION_4_DATA)

    # Mission 5
    create_location(MISSION_5_DATA)

    if goal <= EO1Goal.defeat_cotrangl.value:
        return

    # Mission 6
    create_location(MISSION_6_DATA)

    if goal <= EO1Goal.annihilate_the_forest_folk.value:
        return

    # Mission 7
    create_location(MISSION_7_DATA)

def create_goal_event(world: EtrianOdysseyWorld) -> None:
    goal = EO1Goal(world.options.goal.value)

    def create_event(event_info: EventInfo, region_name: str, access_rule: Rule):
        region = world.get_region(region_name)
        event_location = EtrianOdysseyLocation(world.player, event_info.name, None, region)
        event_item = EtrianOdysseyItem(event_info.item_name, ItemClassification.progression, None, world.player)
        event_item.item_type = EtrianOdysseyItemType.EVENT
        event_location.place_locked_item(event_item)
        region.locations.append(event_location)
        world.set_completion_rule(Has(event_item.name))
        world.set_rule(event_location, access_rule)

    if goal == EO1Goal.defeat_fenrir:
        # Fenrir Defeated
        create_event(EVENT_FENRIR_DEFEATED, EO1Regions.B5F_FENRIR_LAIR, get_mission_access_rule(world, MISSION_2_DATA.mission_id))
    elif goal == EO1Goal.defeat_cernunos:
        # Cernunos Defeated
        create_event(EVENT_CERNUNOS_DEFEATED, EO1Regions.B10F_CERNUNOS_LAIR, get_mission_access_rule(world, MISSION_4_DATA.mission_id))
    elif goal == EO1Goal.defeat_cotrangl:
        # Cotrangl Defeated
        create_event(EVENT_COTRANGL_DEFEATED, EO1Regions.B15F_COTRANGL_ROOM, get_mission_access_rule(world, MISSION_6_DATA.mission_id))
    elif goal == EO1Goal.annihilate_the_forest_folk:
        # Annihilate the forest folk
        create_event(EVENT_ANNIHILATE_THE_FOREST_FOLK, EO1Regions.B20F_MAIN, get_mission_access_rule(world, MISSION_7_DATA.mission_id))
    elif goal == EO1Goal.defeat_etreant:
        # Etreant Defeated
        create_event(EVENT_ETREANT_DEFEATED, EO1Regions.B25F_ETREANT_ROOM, CanDefeatEnemy(EO1Enemies.ETREANT))
    elif goal == EO1Goal.defeat_primevil:
        # Primevil Defeated
        create_event(EVENT_PRIMEVIL_DEFEATED, EO1Regions.B30F_PRIMEVIL_ROOM, CanDefeatEnemy(EO1Enemies.PRIMEVIL))
    elif goal == EO1Goal.fully_complete_codex_and_compendium:
        create_event(EVENT_OBTAIN_THE_TOWN_CROWN, EO1Regions.B30F_PRIMEVIL_ROOM, CanFullyCompleteCodexAndCompendium())
    else:
        raise Exception(f"Goal {goal} not implemented")

def create_events(world: EtrianOdysseyWorld) -> None:
    regions: set[str] = {region.name for region in world.get_regions()}

    goal = EO1Goal(world.options.goal.value)
    goal_stratum = get_max_stratum_for_goal(goal)

    def create_event(event_info: EventInfo, region_name: str, access_rule: Rule):
        if event_info.required_stratum > goal_stratum:
            return

        if region_name not in regions:
            raise Exception(f"Region {region_name} not available for event {event_info.name}")

        region = world.get_region(region_name)
        event_location = EtrianOdysseyLocation(world.player, event_info.name, None, region)
        event_item = EtrianOdysseyItem(event_info.item_name, ItemClassification.progression, None, world.player)
        event_item.item_type = EtrianOdysseyItemType.EVENT
        event_location.place_locked_item(event_item)
        region.locations.append(event_location)
        world.set_rule(event_location, access_rule)

    # Goal events.
    create_goal_event(world)

    # Stratum 2 reached
    create_event(EVENT_STRATUM_2_REACHED, EO1Regions.B6F_MAIN, True_())

    # Dragon Egg Obtained
    create_event(EVENT_DRAGON_EGG_OBTAINED, EO1Regions.B8F_MAIN, True_()) # todo check for dragon egg once shuffled.

    # Mission 3 Completed
    create_event(EVENT_MISSION_3_COMPLETED, EO1Regions.B8F_MAIN, get_mission_access_rule(world, MISSION_3_DATA.mission_id))

    # Discover Claw Mark on B18F
    create_event(EVENT_DISCOVER_CLAW_MARK, EO1Regions.B18F_MAIN, True_())

    # Mission 7 Completed
    create_event(EVENT_MISSION_7_COMPLETED, EO1Regions.B20F_MAIN, get_mission_access_rule(world, MISSION_7_DATA.mission_id))

    # Elevator Activated
    create_event(EVENT_ELEVATOR_ACTIVATED, EO1Regions.B21F_SOUTH_WEST, True_())

    # Card Key
    create_event(EVENT_CARD_KEY_OBTAINED, EO1Regions.B21F_MAIN, CanDefeatEncounter((EO1Enemies.REN, EO1Enemies.TLACHTGA)))

    # Quest Items
    if not bool(world.options.shuffle_radha_note):
        create_event(EVENT_OBTAIN_RADHA_NOTE, EO1Regions.RADHA_HALL, CanReachLocation(MISSION_1_DATA.get_full_name(), EO1Regions.RADHA_HALL))
