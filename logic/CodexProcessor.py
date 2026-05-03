from BaseClasses import CollectionState

from ..data.CodexData import *
from ..data.EncounterData import *
from ..data.EncounterGroupData import *
from ..data.RegionData import *

from .LogicData import *

def get_static_region_list() -> list[str]:
    regions: list[str] = [EO1Regions.ETRIA]

    index = 0
    while True:
        if len(regions) < index + 1:
            break
        region_name = regions[index]
        region_data = ALL_REGION_DATA_BY_NAME[region_name]
        for exit_data in region_data.exits:
            if exit_data.destination in regions:
                continue

            regions.append(exit_data.destination)
        index += 1
        continue

    return regions

def generate_region_by_encounter_dictionary() -> dict[int, list[str]]:
    regions = get_static_region_list()
    region_by_encounter: dict[int, list[str]] = {}

    def add_encounter(reg: str, encounter_id: int):
        if encounter_id not in region_by_encounter:
            region_by_encounter[encounter_id] = []

        region_by_encounter[encounter_id].append(reg)

    for region in regions:
        region_data = ALL_REGION_DATA_BY_NAME[region]

        for encounter_group_id in region_data.encounters:
            encounter_group_data = ENCOUNTER_GROUP_BY_ID[encounter_group_id]

            add_encounter(region, encounter_group_data.encounter_id_1)
            add_encounter(region, encounter_group_data.encounter_id_2)
            add_encounter(region, encounter_group_data.encounter_id_3)

    return region_by_encounter

def generate_encounter_by_monster_dictionary() -> dict[int, list[int]]:
    encounter_by_monster: dict[int, list[int]] = {}

    def add_if_valid_enemy(enemy_id: int, encounter_id: int):
        if enemy_id == 0x00:
            return

        if enemy_id not in encounter_by_monster:
            encounter_by_monster[enemy_id] = []

        if encounter_id in encounter_by_monster[enemy_id]:
            return

        encounter_by_monster[enemy_id].append(encounter_id)

    for encounter_data in ALL_ENCOUNTERS:
        add_if_valid_enemy(encounter_data.enemy_1_id, encounter_data.encounter_id)
        add_if_valid_enemy(encounter_data.enemy_2_id, encounter_data.encounter_id)
        add_if_valid_enemy(encounter_data.enemy_3_id, encounter_data.encounter_id)
        add_if_valid_enemy(encounter_data.enemy_4_id, encounter_data.encounter_id)
        add_if_valid_enemy(encounter_data.enemy_5_id, encounter_data.encounter_id)

    return encounter_by_monster

def generate_region_by_foe_dictionary()-> dict[int, list[str]]:
    regions = get_static_region_list()
    region_by_foe: dict[int, list[str]] = {}

    def add_foe(reg: str, foe_id: int):
        if foe_id not in region_by_foe:
            region_by_foe[foe_id] = []

        region_by_foe[foe_id].append(reg)

    for region in regions:
        region_data = ALL_REGION_DATA_BY_NAME[region]

        for foe in region_data.foes:
            add_foe(region, foe)

    return region_by_foe

def generate_region_by_boss_dictionary()-> dict[int, list[str]]:
    regions = get_static_region_list()
    region_by_boss: dict[int, list[str]] = {}

    def add_boss(reg: str, boss_id: int):
        if boss_id not in region_by_boss:
            region_by_boss[boss_id] = []

        region_by_boss[boss_id].append(reg)

    for region in regions:
        region_data = ALL_REGION_DATA_BY_NAME[region]

        for boss in region_data.bosses:
            add_boss(region, boss)

    return region_by_boss


REGION_BY_ENCOUNTER: dict[int, list[str]] = generate_region_by_encounter_dictionary()
ENCOUNTER_BY_MONSTER: dict[int, list[int]] = generate_encounter_by_monster_dictionary()
REGION_BY_FOE: dict[int, list[str]] = generate_region_by_foe_dictionary()
REGION_BY_BOSS: dict[int, list[str]] = generate_region_by_boss_dictionary()

class CodexProcessor:
    max_stratum: int
    player_id: int
    region_cache: set[str] | None

    def __init__(self, max_stratum: int, player_id: int):
        self.player_id = player_id
        self.max_stratum = max_stratum
        self.region_cache = None

    def can_fill_codex_entry(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        if self.region_cache is None:
            self.region_cache = set([region_data.name for region_data
                                     in state.multiworld.worlds[self.player_id].get_regions()])

        if enemy_id not in logic_data.defeatable_enemy.defeatable_enemies:
            return False

        codex_data = CODEX_DATA_BY_ENEMY_ID[enemy_id]

        if codex_data.required_stratum > self.max_stratum:
            return False

        if codex_data.encounter_type == CodexEncounterType.REGULAR:
            return self.__can_fill_regular_entry(codex_data, state, logic_data)
        elif codex_data.encounter_type == CodexEncounterType.FOE:
            return self.__can_fill_foe_entry(codex_data, state, logic_data)
        elif codex_data.encounter_type == CodexEncounterType.BOSS:
            return self.__can_fill_boss_entry(codex_data, state, logic_data)
        elif codex_data.encounter_type == CodexEncounterType.MINION:
            return self.__can_fill_minion_entry(codex_data, state, logic_data)
        elif codex_data.encounter_type == CodexEncounterType.QUEST:
            return False

        raise Exception("Not implemented")

    def __can_reach_any_regions(self, regions: list[str], state: CollectionState, logic_data: AllLogicData) -> bool:
        for region in regions:
            # Skip regions not in the seed (depending on goal).
            if region not in self.region_cache:
                continue

            # Optimization: Doing a floor number check is much, much faster than doing a "can_reach_region" check.
            region_data = ALL_REGION_DATA_BY_NAME[region]
            if region_data.floor_number > logic_data.current_floor_limit:
                continue
            if state.can_reach_region(region, self.player_id):
                return True
        return False

    def __can_fill_regular_entry(self, codex_data: CodexData, state: CollectionState, logic_data: AllLogicData) -> bool:
        # Temporary, since we only support regular encounter monsters.
        #if codex_data.enemy_id not in ENCOUNTER_BY_MONSTER:
        #    return False

        encounters = ENCOUNTER_BY_MONSTER[codex_data.enemy_id]

        for encounter_id in encounters:
            if encounter_id not in logic_data.defeatable_encounter.defeatable_encounters:
                continue

            regions = REGION_BY_ENCOUNTER[encounter_id]
            if self.__can_reach_any_regions(regions, state, logic_data):
                return True

        # If we got here, this mean none of the encounters are both defeatable and reachable.
        return False

    def __can_fill_foe_entry(self, codex_data, state, logic_data) -> bool:
        regions = REGION_BY_FOE[codex_data.enemy_id]
        return self.__can_reach_any_regions(regions, state, logic_data)

    def __can_fill_boss_entry(self, codex_data, state, logic_data) -> bool:
        # Bosses are more complex, since they can be locked behind questlines.
        # However, for now quest related bosses are unsupported.
        regions = REGION_BY_BOSS[codex_data.enemy_id]
        return self.__can_reach_any_regions(regions, state, logic_data)

    def __can_fill_minion_entry(self, codex_data, state, logic_data) -> bool:
        # For this game, there is only one minion type enemy, so this function is hard coded for them.
        if EO1Enemies.CERNUNOS not in logic_data.defeatable_encounter.defeatable_encounters:
            return False

        # This is recursive, but it's controlled.
        # If other minion types get added, add a validation the enemy type here isn't also minion (to avoid stackoverflow mistakes).
        return self.can_fill_codex_entry(EO1Enemies.CERNUNOS, state, logic_data)


