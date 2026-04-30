from __future__ import annotations

from BaseClasses import CollectionState
from .SustainProcessor import SustainProcessor
from ..Items import EtrianOdysseyItemType, EtrianOdysseyItem
from ..data.ItemData import *
from ..data.InventoryItemData import *
from ..Options import *

#from ..data import EnemyData, EncounterGroupData, EncounterData, RegionData
from ..data.RegionData import *
from ..Constant import *
from typing import TYPE_CHECKING

from collections.abc import Iterator, Callable

from .LogicData import *
from .ClassProcessor import *
from .SingleEnemyBattleProcessor import *
from .EncounterBattleProcessor import *
from .EncounterGroupBattleProcessor import *
from .CodexProcessor import *
from .CompendiumProcessor import *
from .ConditionalDropProcessor import *
from .ShopUnlockProcessor import *
from .simplified_logic.SimplifiedSingleEnemyBattleProcessor import SimplifiedSingleEnemyBattleProcessor

if TYPE_CHECKING:
    from .. import EtrianOdysseyWorld

class LogicManager:
    logic_data: AllLogicData
    options: EtrianOdysseyOptions
    player_id: int

    # Processors.
    class_processor: ClassProcessor
    enemy_battle_processor: SingleEnemyBattleProcessor
    encounter_battle_processor: EncounterBattleProcessor
    encounter_group_battle_processor: EncounterGroupBattleProcessor
    codex_processor: CodexProcessor
    compendium_processor: CompendiumProcessor
    conditional_drop_processor: ConditionalDropProcessor
    #shop_unlock_processor: ShopUnlockProcessor
    sustain_processor: SustainProcessor

    def __init__(self, options: EtrianOdysseyOptions, player_id: int, fill_default=True) -> None:
        self.logic_data = AllLogicData(fill_default)
        self.logic_data.current_level_cap = options.get_effective_initial_level_cap()
        self.logic_data.current_floor_limit = options.get_effective_initial_floor_limit()
        self.options = options
        self.player_id = player_id

        self.class_processor = ClassProcessor(player_id)
        self.sustain_processor = SustainProcessor()
        self.enemy_battle_processor = self.__create_single_enemy_battle_processor_from_options(options)
        self.encounter_battle_processor = self.__create_encounter_battle_processor_from_options(options)
        self.encounter_group_battle_processor = self.__create_encounter_group_battle_processor_from_options(options)
        max_stratum = get_max_stratum_for_goal(EO1Goal(options.goal.value))

        self.conditional_drop_processor = ConditionalDropProcessor()
        self.codex_processor = CodexProcessor(max_stratum, player_id)
        self.compendium_processor = CompendiumProcessor(max_stratum, player_id, self.conditional_drop_processor)
        #self.shop_unlock_processor = ShopUnlockProcessor()

        if fill_default:
            # Initialize class data
            self.class_processor.initialize_data(self.logic_data.class_data, bool(options.remove_skills_requirements))
            pass

    def copy(self) -> LogicManager:
        new_copy = LogicManager(self.options, player_id=self.player_id, fill_default=False)
        new_copy.logic_data = self.logic_data.copy()
        # Don't copy the processors, they will be generated anew, and they are stateless by design.
        return new_copy

# todo move the processor creation to a dedicated file.
    @staticmethod
    def __create_single_enemy_battle_processor_from_options(options: EtrianOdysseyOptions) -> SingleEnemyBattleProcessor:
        battle_logic_mode_type = BattleLogicModeType(options.battle_logic_mode.value)
        if battle_logic_mode_type == BattleLogicModeType.no_logic:
            return NoLogicSingleEnemyBattleProcessor()
        elif battle_logic_mode_type == BattleLogicModeType.level_only:
            return LevelOnlySingleEnemyBattleProcessor()
        elif battle_logic_mode_type == BattleLogicModeType.simplified:
            return SimplifiedSingleEnemyBattleProcessor()

        raise Exception("Not implemented")

    @staticmethod
    def __create_encounter_battle_processor_from_options(options: EtrianOdysseyOptions) -> EncounterBattleProcessor:
        return SimpleEncounterBattleProcessor()

    @staticmethod
    def __create_encounter_group_battle_processor_from_options(options: EtrianOdysseyOptions) -> EncounterGroupBattleProcessor:
        return SimpleEncounterGroupBattleProcessor()

    def collect(self, state: CollectionState, item: EtrianOdysseyItem) -> None:
        if not hasattr(item, "item_type"):
            raise Exception(f"Expected an item_type to be defined for {item.name}")

        # Don't restrict to max value, so we support remove properly too.
        if item.item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            self.logic_data.current_level_cap += ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item.code].level_amount
            self.logic_data.set_battle_stale()
        elif item.item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            self.logic_data.current_floor_limit += ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item.code].floor_amount
            self.logic_data.set_battle_stale()
            self.logic_data.set_location_stale()
        elif item.item_type == EtrianOdysseyItemType.CLASS:
            self.logic_data.set_battle_stale()
        elif item.item_type == EtrianOdysseyItemType.INVENTORY:
            item_type = ITEM_PER_AP_ITEM_ID[item.code].type
            if item_type == EO1ItemType.Key or item_type == EO1ItemType.Quest:
                self.logic_data.set_location_stale()
        elif item.item_type == EtrianOdysseyItemType.SKILL:
            self.logic_data.set_skill_stale() # Don't automatically set battle as stale, it will be done if there is a change.
            self.logic_data.set_battle_stale()
        elif item.item_type == EtrianOdysseyItemType.EVENT:
            self.logic_data.set_location_stale()

        #floor_ = 1
        #for floor_limit in ALL_PROGRESSIVE_FLOOR_LIMIT:
        #    count = state.count(floor_limit.name, 1)
        #    floor_ += floor_limit.floor_amount * count

        #if floor_ != self.logic_data.current_floor_limit:
        #    raise Exception("not match")

    def remove(self, state: CollectionState, item: EtrianOdysseyItem) -> None:
        if not hasattr(item, "item_type"):
            raise Exception(f"Expected an item_type to be defined for {item.name}")

        if item.item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            self.logic_data.current_level_cap -= ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item.code].level_amount
        elif item.item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            self.logic_data.current_floor_limit -= ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item.code].floor_amount

        def recalculate_battle():
            # Recalculate all battle related state data
            self.__recalculate_class_data(state)
            self.__recalculate_set_logic_data(self.logic_data.defeatable_enemy,
                                              self.enemy_battle_processor.can_defeat_enemy, state)
            self.__recalculate_set_logic_data(self.logic_data.survivable_enemy,
                                              self.enemy_battle_processor.can_survive_enemy, state)
            self.__recalculate_set_logic_data(self.logic_data.defeatable_encounter,
                                              self.encounter_battle_processor.can_defeat_encounter, state)
            self.__recalculate_set_logic_data(self.logic_data.survivable_encounter,
                                              self.encounter_battle_processor.can_survive_encounter, state)
            self.__recalculate_set_logic_data(self.logic_data.encounter_group,
                                              self.encounter_group_battle_processor.can_survive_encounter_group, state)
            self.__recalculate_set_logic_data(self.logic_data.codex_logic_data,
                                              self.codex_processor.can_fill_codex_entry, state)
            self.__recalculate_set_logic_data(self.logic_data.compendium_logic_data,
                                              self.compendium_processor.can_fill_compendium_entry, state)

        def recalculate_location():
            self.__recalculate_set_logic_data(self.logic_data.codex_logic_data,
                                              self.codex_processor.can_fill_codex_entry, state)
            self.__recalculate_set_logic_data(self.logic_data.compendium_logic_data,
                                              self.compendium_processor.can_fill_compendium_entry, state)

        def recalculate_skill():
            self.__recalculate_class_data(state)

        # Do the remove recalculations directly here.
        # If this become too costly, split the stale variable into positive and negative recalculation.
        if item.item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            recalculate_battle()
        elif item.item_type == EtrianOdysseyItemType.CLASS:
            recalculate_battle()
        elif item.item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            recalculate_battle()
            recalculate_location()
        elif item.item_type == EtrianOdysseyItemType.INVENTORY:
            item_type = ITEM_PER_AP_ITEM_ID[item.code].type
            if item_type == EO1ItemType.Key or item_type == EO1ItemType.Quest:
                recalculate_location()
        elif item.item_type == EtrianOdysseyItemType.SKILL:
            recalculate_skill()
            recalculate_battle()
            recalculate_location()
        elif item.item_type == EtrianOdysseyItemType.EVENT:
            recalculate_location()

    def get_current_floor_limit(self) -> int:
        return self.logic_data.current_floor_limit

    def can_survive_region(self, state: CollectionState, region_name: str) -> bool:
        region_data = ALL_REGION_DATA_BY_NAME[region_name]
        self.__update_encounter_group(state)

        for encounter_group_id in region_data.encounters:
            if encounter_group_id not in self.logic_data.encounter_group.survivable_encounter_groups:
                return False

        # todo sustain.

        return True

    # todo this is technically distinct from the encounter list. This needs improvement.
    def can_defeat_enemies(self, state: CollectionState, enemies: list[int]) -> bool:
        return all(self.can_defeat_enemy(state, enemy) for enemy in enemies)

    def can_defeat_enemy(self, state: CollectionState, enemy: int) -> bool:
        self.__update_defeatable_enemies(state)
        return enemy in self.logic_data.defeatable_enemy.defeatable_enemies

    def can_fill_codex_entry(self, state: CollectionState, enemy_id: int) -> bool:
        self.__update_fillable_codex_entries(state)
        return enemy_id in self.logic_data.codex_logic_data.fillable_codex_entries

    def can_fill_compendium_entry(self, state: CollectionState, item_id: int) -> bool:
        self.__update_fillable_compendium_entries(state)
        return item_id in self.logic_data.compendium_logic_data.fillable_compendium_entries

    def __update_defeatable_enemies(self, state: CollectionState) -> None:
        self.__update_class_data(state)

        # Note: This may seems like a circular reference (and it logically is), but it is handled by delaying
        #self.__update_shop_consumable_entries(state)

        if self.logic_data.defeatable_enemy.is_stale():
            self.__update_set_logic_data(self.logic_data.defeatable_enemy, self.enemy_battle_processor.can_defeat_enemy, state)

    def __update_survivable_enemies(self, state: CollectionState) -> None:
        self.__update_class_data(state)

        if self.logic_data.survivable_enemy.is_stale():
            self.__update_set_logic_data(self.logic_data.survivable_enemy, self.enemy_battle_processor.can_survive_enemy, state)

    def __update_defeatable_encounters(self, state: CollectionState) -> None:
        self.__update_class_data(state)
        self.__update_defeatable_enemies(state)

        if self.logic_data.defeatable_encounter.is_stale():
            self.__update_set_logic_data(self.logic_data.defeatable_encounter, self.encounter_battle_processor.can_defeat_encounter, state)

    def __update_survivable_encounters(self, state: CollectionState) -> None:
        self.__update_class_data(state)
        self.__update_survivable_enemies(state)

        if self.logic_data.survivable_encounter.is_stale():
            self.__update_set_logic_data(self.logic_data.survivable_encounter, self.encounter_battle_processor.can_survive_encounter, state)

    def __update_encounter_group(self, state: CollectionState) -> None:
        self.__update_class_data(state)
        self.__update_survivable_enemies(state)
        self.__update_survivable_encounters(state)

        if self.logic_data.encounter_group.is_stale():
            self.__update_set_logic_data(self.logic_data.encounter_group, self.encounter_group_battle_processor.can_survive_encounter_group, state)

    def __update_fillable_codex_entries(self, state: CollectionState) -> None:
        self.__update_class_data(state)
        self.__update_defeatable_encounters(state)

        if self.logic_data.codex_logic_data.is_stale():
            self.__update_set_logic_data(self.logic_data.codex_logic_data, self.codex_processor.can_fill_codex_entry, state)

    def __update_fillable_compendium_entries(self, state: CollectionState) -> None:
        self.__update_class_data(state)
        self.__update_defeatable_encounters(state)
        self.__update_fillable_codex_entries(state)

        if self.logic_data.compendium_logic_data.is_stale():
            changed = self.__update_set_logic_data(self.logic_data.compendium_logic_data, self.compendium_processor.can_fill_compendium_entry, state)
            #if changed:
                #self.logic_data.set_shop_consumable_stale()

    #def __update_shop_consumable_entries(self, state: CollectionState) -> None:
    #    # This have dependencies on compendium entries, but this makes a circular reference.
    #    # To avoid infinite looping, do a direct update of the compendium entries here, instead of a delayed one.
    #    # This will have the impact of logic being delayed by one step, but it also
    #    # somewhat represent the need to go back to town anyway.
    #    is_stale = self.logic_data.shop_consumable_unlock_logic_data.is_stale()
    #
    #    self.__update_class_data(state)
    #
    #    # Update Codex and Compendium, in order, if they are stale.
    #    if self.logic_data.codex_logic_data.is_stale():
    #        self.__update_set_logic_data(self.logic_data.codex_logic_data, self.codex_processor.can_fill_codex_entry, state)
    #        # But keep it stale.
    #        self.logic_data.codex_logic_data.set_stale(True)
    #    if self.logic_data.compendium_logic_data.is_stale():
    #        is_stale |= self.__update_set_logic_data(self.logic_data.compendium_logic_data, self.compendium_processor.can_fill_compendium_entry, state)
    #        # But keep it stale.
    #        self.logic_data.compendium_logic_data.set_stale(True)

    #    # Now compendium is as up to date as can be without being unsafe.
    #    if is_stale:
    #        changed = self.__update_set_logic_data(self.logic_data.shop_consumable_unlock_logic_data, self.shop_unlock_processor.can_unlock_item, state)
    #        if changed:
    #            self.logic_data.set_battle_stale()

    def __update_class_data(self, state: CollectionState) -> None:
        if self.logic_data.class_data.is_stale():
            if self.class_processor.update_class_data(self.logic_data, state):
                self.logic_data.set_battle_stale()
            self.logic_data.class_data.set_stale(False)

    def __update_set_logic_data(self, logic_data: DualIntSetLogicData, can_access: Callable[int, CollectionState, AllLogicData], state: CollectionState) -> bool:
        new_accessible = set()
        for identifier in logic_data.unaccessible:
            if can_access(identifier, state, self.logic_data):
                new_accessible.add(identifier)

        for identifier in new_accessible:
            logic_data.unaccessible.remove(identifier)
            logic_data.accessible.add(identifier)

        logic_data.set_stale(False)
        changed = len(new_accessible) > 0
        return changed

    def __recalculate_class_data(self, state: CollectionState) -> bool:
        changed = self.class_processor.recalculate_class_data(self.logic_data, state)
        # TODO decide if this is omitted. Do not set to False, since the data could already be stale.
        self.logic_data.class_data.set_stale(True)
        return changed

    def __recalculate_set_logic_data(self, logic_data: DualIntSetLogicData, can_access: Callable[int, CollectionState, AllLogicData], state: CollectionState) -> bool:
        new_unaccessible = set()
        for identifier in logic_data.accessible:
            if not can_access(identifier, state, self.logic_data):
                new_unaccessible.add(identifier)

        for identifier in new_unaccessible:
            logic_data.accessible.remove(identifier)
            logic_data.unaccessible.add(identifier)

        # TODO decide if this is omitted. Do not set to False, since the data could already be stale.
        logic_data.set_stale(True) # For safety.

        changed = len(new_unaccessible) > 0
        return changed
