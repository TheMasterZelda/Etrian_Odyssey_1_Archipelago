from __future__ import annotations
from rule_builder.rules import Rule

from typing import TYPE_CHECKING

#from .data import items as itm, entrances as ent
from worlds.generic.Rules import set_rule
from BaseClasses import CollectionState, MultiWorld, Item
from worlds.AutoWorld import LogicMixin
from .Constant import GAME_NAME
#from .Items import EtrianOdysseyItemType
#from .Locations import EtrianOdysseyLocation
from .data.InventoryItemData import EO1ItemNames
from .data.ItemData import *
from .Options import *
from .data.RegionData import EO1RegionData, ALL_REGION_DATA_BY_NAME
from .data.Entrances import *
from .data.ClassData import *
from .data.Events import *
from .data.EnemyData import EO1Enemies
from .data.RegionData import EO1Regions
import dataclasses
from typing import TYPE_CHECKING
from .logic.LogicManager import LogicManager

if TYPE_CHECKING:
    from . import EtrianOdysseyWorld

from rule_builder.rules import *

class EtrianOdysseyLogic(LogicMixin):
    etrianodyssey_logic_data: dict[int, LogicManager] # per player

    def init_mixin(self, multiworld: MultiWorld) -> None:
        self.etrianodyssey_logic_data = {
            player: LogicManager(multiworld.worlds[player].options, player) for player in multiworld.get_game_players(GAME_NAME)
        }

    def copy_mixin(self, new_state: CollectionState) -> CollectionState:
        new_state.etrianodyssey_logic_data = {
            player: logic_data.copy() for player, logic_data in self.etrianodyssey_logic_data.items()
        }
        return new_state

    def etrianodyssey_get_logic_manager(self, player: int) -> LogicManager:
        return self.etrianodyssey_logic_data[player]

# This is to remove individual warnings from calling this method.
def get_logic_manager(state: CollectionState, player: int) -> LogicManager:
    return state.etrianodyssey_get_logic_manager(player)

def get_battle_item_dependencies() -> list[str]:
    return [
        ItemGroupNames.PROGRESSIVE_LEVEL_CAP,
        ItemGroupNames.CLASS,
        ItemGroupNames.SKILL
    ]

def get_location_item_dependencies() -> list[str]:
    return [
        ItemGroupNames.PROGRESSIVE_FLOOR_LIMIT,
        ItemGroupNames.KEY_ITEM,
        # TODO add Quest items
        ItemGroupNames.EVENT # Events mostly lock regions.
    ]

@dataclasses.dataclass()
class FloorUnlocked(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    floor: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.floor, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        floor: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.floor <= get_logic_manager(state, self.player).get_current_floor_limit()

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {ItemGroupNames.PROGRESSIVE_FLOOR_LIMIT: {id(self)}}

@dataclasses.dataclass()
class CanSurviveRegion(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    region: str

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.region, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        region: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_survive_region(state, self.region)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanDefeatEnemy(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    enemy: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.enemy, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        enemy: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_defeat_enemy(state, self.enemy)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item_name: {id(self)} for item_name in get_battle_item_dependencies()}

@dataclasses.dataclass()
class CanDefeatEncounter(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    enemies: tuple[int, ...]

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.enemies, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        enemies: tuple[int, ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            enemies = list(self.enemies)
            return logic_manager.can_defeat_enemies(state, enemies)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item_name: {id(self)} for item_name in get_battle_item_dependencies()}

@dataclasses.dataclass()
class CanFillCodexEntry(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    enemy_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.enemy_id, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        enemy_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_fill_codex_entry(state, self.enemy_id)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanFillCompendiumEntry(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    item_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.item_id, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        item_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_fill_compendium_entry(state, self.item_id)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanUnlockShopItem(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    item_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.item_id, player=world.player)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        item_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_unlock_shop_item(state, self.item_id)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanUseSkill(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    skill_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.skill_id, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        skill_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_fill_codex_entry(state, self.skill_id)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                ItemGroupNames.PROGRESSIVE_FLOOR_LIMIT: {id(self)},
                # TODO add Key and Quest items
            }

@dataclasses.dataclass()
class CanEscape(Rule["EtrianOdysseyWorld"], game=GAME_NAME):

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # TODO support skills or Magnet too.
            return state.has(EO1ItemNames.RADHA_NOTE, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                EO1ItemNames.RADHA_NOTE: {id(self)},
            }

@dataclasses.dataclass()
class CanStartQuest(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    quest_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.quest_id, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        quest_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_start_quest(state, self.quest_id)
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanCompleteQuest(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    quest_id: int

    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(self.quest_id, player=world.player)  # , caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass
        quest_id: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_complete_quest(state, self.quest_id)
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }

@dataclasses.dataclass()
class CanFullyCompleteCodexAndCompendium(Rule["EtrianOdysseyWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: EtrianOdysseyWorld) -> Rule.Resolved:
        return self.Resolved(player=world.player)  # , caching_enabled=True)

    class Resolved(Rule.Resolved):
        # noinspection PyDataclass

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            logic_manager = get_logic_manager(state, self.player)
            return logic_manager.can_fully_complete_codex_and_compendium(state)
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item_name: {id(self)} for item_name in get_battle_item_dependencies()},
                **{item_name: {id(self)} for item_name in get_location_item_dependencies()},
            }


def resolve_entrance_rule(world: EtrianOdysseyWorld, source_region: EO1RegionData, exit_data: EO1Entrance) -> Rule:
    destination_data = ALL_REGION_DATA_BY_NAME[exit_data.destination]
    entrance_rule: Rule

    if exit_data.entrance_type == EntranceType.Entrance:
        return True_() # Always true, for now. This is to make floor 1 always in logic, no matter the settings.
    elif exit_data.entrance_type == EntranceType.StairsDown:
        entrance_rule = FloorUnlocked(destination_data.floor_number)
    elif exit_data.entrance_type == EntranceType.StairsUp:
        entrance_rule = True_() # Nothing restrict going up.
    elif exit_data.entrance_type == EntranceType.Elevator:
        entrance_rule = And(
            FloorUnlocked(destination_data.floor_number),
            Has(EVENT_ELEVATOR_ACTIVATED.item_name))
    elif exit_data.entrance_type == EntranceType.Pitfall:
        # For now, check floor restriction.
        entrance_rule = FloorUnlocked(destination_data.floor_number)
    elif exit_data.entrance_type == EntranceType.StratumTransition:
        # Functionally, its stairs, the type distinction exist to detect where goals finish.
        entrance_rule = FloorUnlocked(destination_data.floor_number)
    elif exit_data.entrance_type == EntranceType.VioletCrystalDoor:
        entrance_rule = Has(EO1ItemNames.VIOLET_KEY)
    elif exit_data.entrance_type == EntranceType.ClearCrystalDoor:
        entrance_rule = Has(EO1ItemNames.CLEAR_KEY)
    elif exit_data.entrance_type == EntranceType.CardKeyDoor:
        # Currently not randomized, but will be eventually.
        entrance_rule = Has(EVENT_CARD_KEY_OBTAINED.item_name)
    elif exit_data.entrance_type == EntranceType.EventLockedShortcut:
        event_info = EVENT_BY_NAME[exit_data.event_name]
        entrance_rule = Has(event_info.item_name)
    elif exit_data.entrance_type == EntranceType.MandatoryFight:
        entrance_rule = CanDefeatEncounter(tuple(exit_data.enemies))
    elif exit_data.entrance_type == EntranceType.OneWayFightOrEscape:
        entrance_rule = Or(
            CanDefeatEncounter(tuple(exit_data.enemies)),
            CanEscape()
        )
    elif exit_data.entrance_type == EntranceType.DragonDoor:
        entrance_rule = CanFillCodexEntry(exit_data.enemy_id)
    else:
        raise Exception(f"Unknown entrance type: {exit_data.entrance_type}")

    return And(CanSurviveRegion(exit_data.destination),
               FloorUnlocked(destination_data.floor_number),
        entrance_rule)

def get_mission_access_rule(world: EtrianOdysseyWorld, mission_id: int) -> Rule:
    if mission_id == 1:
        return True_()
    if mission_id == 2:
        return And(
            CanReachRegion(EO1Regions.B5F_FENRIR_LAIR),
            CanDefeatEnemy(EO1Enemies.FENRIR)
        )
    if mission_id == 3:
        return And(
            CanReachRegion(EO1Regions.B8F_MAIN),
            Has(EVENT_DRAGON_EGG_OBTAINED.item_name)  # todo replace this for the actual dragon egg item when shuffled.
        )
    if mission_id == 4:
        return And(
            CanReachRegion(EO1Regions.B10F_CERNUNOS_LAIR),
            CanDefeatEnemy(EO1Enemies.CERNUNOS)
        )
    if mission_id == 5:
        return And(
            FloorUnlocked(12),  # Minimum requirement no matter what.
            CanReachRegion(EO1Regions.B12F_ANT_NEST),
            CanDefeatEnemy(EO1Enemies.ROYALANT)  # Technically you don't have to, but you need to map behind the queen.
        )
    if mission_id == 6:
        return And(
            CanReachRegion(EO1Regions.B15F_COTRANGL_ROOM),
            CanDefeatEnemy(EO1Enemies.COTRANGL)
        )
    if mission_id == 7:
        return And(
            CanReachRegion(EO1Regions.B20F_MAIN),
            CanDefeatEnemy(EO1Enemies.IWAOPELN),
            CanDefeatEnemy(EO1Enemies.HUNTER),
            CanDefeatEnemy(EO1Enemies.OGRE),
            CanDefeatEnemy(EO1Enemies.CRUELLA),
            CanDefeatEnemy(EO1Enemies.DIABOLIX)
        )

    raise Exception(f"Unknown mission: {mission_id}")

def set_all_rules(world: EtrianOdysseyWorld) -> None:
    pass
