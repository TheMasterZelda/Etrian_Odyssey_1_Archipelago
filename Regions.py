from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region
from .data.RegionData import *
from .data.Entrances import EntranceType
#from .data import Regions, Entrances
from .Rules import *

if TYPE_CHECKING:
    from . import EtrianOdysseyWorld

def _is_entrance_valid_for_goal(world: EtrianOdysseyWorld, exit_data: EO1Entrance, destination_data: EO1RegionData) -> bool:
    if exit_data.entrance_type == EntranceType.StratumTransition:
        max_floor = get_max_floor_for_goal(EO1Goal(world.options.goal.value))
        # If destination floor is above the max, skip it.
        if destination_data.floor_number > max_floor:
            return False

    if exit_data.entrance_type in [EntranceType.EventLockedShortcut, EntranceType.QuestLockedShortcut]:
        max_stratum = get_max_stratum_for_goal(EO1Goal(world.options.goal.value))
        event_shortcut_data = exit_data
        # If required stratum is above the max, skip it.
        if exit_data.stratum_required > max_stratum:
            return False

    return True

def create_and_connect_regions(world: EtrianOdysseyWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: EtrianOdysseyWorld) -> None:

    regions: list[str] = [EO1Regions.ETRIA]

    index = 0
    while True:
        if len(regions) < index + 1:
            break
        region_name = regions[index]
        region_data = ALL_REGION_DATA_BY_NAME[region_name]
        for exit_data in region_data.exits:
            destination_data = ALL_REGION_DATA_BY_NAME[exit_data.destination]
            if not _is_entrance_valid_for_goal(world, exit_data, destination_data):
                continue

            if exit_data.destination in regions:
                continue

            regions.append(exit_data.destination)
        index += 1
        continue

    world.multiworld.regions += [
        Region(region_name, world.player, world.multiworld)
        for region_name in regions]


def connect_regions(world: EtrianOdysseyWorld) -> None:
    for region in world.get_regions():
        region_name = region.name
        region_data = ALL_REGION_DATA_BY_NAME[region_name]
        for exit_data in region_data.exits:
            destination_data = ALL_REGION_DATA_BY_NAME[exit_data.destination]
            if not _is_entrance_valid_for_goal(world, exit_data, destination_data):
                continue

            destination = world.get_region(exit_data.destination)
            access_rule = resolve_entrance_rule(world, region_data, exit_data)
            region.connect(destination, f"{region_name} {exit_data.full_name}", access_rule)
