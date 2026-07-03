from __future__ import annotations

from .LogicCacheData import AllLogicCacheData
from .LogicManager import LogicManager, EO1ExecutionContext
from .StateInterface import StateInterface
from . import QuestProcessor
from .SustainProcessor import SustainProcessor
from ..Items import EtrianOdysseyItemType, EtrianOdysseyItem
from ..RandomizedGameData import RandomizedGameData
from ..data.ItemData import *
from ..data.InventoryItemData import *
from ..Options import *

#from ..data import EnemyData, EncounterGroupData, EncounterData, RegionData
from ..data.RegionData import *
from ..Constant import *
from typing import TYPE_CHECKING

from collections.abc import Callable

from .LogicData import *
from .ClassProcessor import *
from .SingleEnemyBattleProcessor import *
from .EncounterBattleProcessor import *
from .EncounterGroupBattleProcessor import *
from .CodexProcessor import *
from .CompendiumProcessor import *
from .ConditionalDropProcessor import *
from .ShopUnlockProcessor import *
from .QuestProcessor import *
from .simplified_logic.SimplifiedSingleEnemyBattleProcessor import SimplifiedSingleEnemyBattleProcessor

class LogicProxy:
    logic_data: AllLogicData
    logic_cache_data: AllLogicCacheData
    options: EtrianOdysseyOptions
    logic_manager: LogicManager
    randomized_game_data: RandomizedGameData

    def __init__(self, options: EtrianOdysseyOptions, randomized_game_data: RandomizedGameData, initialize=True) -> None:
        self.options = options
        self.randomized_game_data = randomized_game_data

        if not initialize:
            return

        self.logic_data = AllLogicData()
        self.logic_cache_data = AllLogicCacheData()
        self.logic_data.current_level_cap = options.get_effective_initial_level_cap()
        self.logic_data.current_floor_limit = options.get_effective_initial_floor_limit()

        max_stratum = get_max_stratum_for_goal(EO1Goal(options.goal.value))

        self.logic_manager = LogicManager()
        data_source = EtrianOdysseyDataSource()
        self.logic_manager.class_processor = ClassProcessor(data_source)
        self.logic_manager.enemy_battle_processor = self.__create_single_enemy_battle_processor_from_options(options)
        self.logic_manager.encounter_battle_processor = self.__create_encounter_battle_processor_from_options(options)
        self.logic_manager.encounter_group_battle_processor = self.__create_encounter_group_battle_processor_from_options(options)
        self.logic_manager.quest_processor = QuestProcessor()
        self.logic_manager.codex_processor = CodexProcessor(max_stratum)
        self.logic_manager.conditional_drop_processor = ConditionalDropProcessor(self.logic_manager.enemy_battle_processor)
        self.logic_manager.compendium_processor = CompendiumProcessor(max_stratum, self.logic_manager.conditional_drop_processor)
        self.logic_manager.shop_unlock_processor = ShopUnlockProcessor()
        self.logic_manager.sustain_processor = SustainProcessor()

        # Initialize class data
        self.logic_manager.class_processor.initialize_data(self.logic_data.class_data, bool(options.remove_skills_requirements))
        self.logic_manager.initialize_cache(self.logic_cache_data)

        #if self.randomized_game_data.test != "123":
        #    raise Exception("no")

    def __make_execution_context(self, state: StateInterface) -> EO1ExecutionContext:
        context = EO1ExecutionContext()
        context.logic_data = self.logic_data
        context.cache_data = self.logic_cache_data
        context.logic_manager = self.logic_manager
        context.state = state
        return context

    def copy(self) -> LogicProxy:
        new_copy = LogicProxy(self.options, self.randomized_game_data, initialize=False)
        new_copy.logic_data = self.logic_data.copy()
        new_copy.logic_cache_data = self.logic_cache_data.copy()
        new_copy.logic_manager = self.logic_manager # Copy reference only
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

    def collect(self, state: StateInterface, item: EtrianOdysseyItem) -> None:
        if item.name == UT_GLITCH_LOGIC_ITEM_NAME:
            self.logic_manager.on_ut_glitch_logic(self.__make_execution_context(state))
            return

        if not hasattr(item, "item_type"):
            raise Exception(f"Expected an item_type to be defined for {item.name}")

        self.logic_manager.on_item_collect(item.code, item.item_type, self.__make_execution_context(state))

    def remove(self, state: StateInterface, item: EtrianOdysseyItem) -> None:
        if not hasattr(item, "item_type"):
            raise Exception(f"Expected an item_type to be defined for {item.name}")

        self.logic_manager.on_item_remove(item.code, item.item_type, self.__make_execution_context(state))

    def get_current_floor_limit(self) -> int:
        return self.logic_data.current_floor_limit

    def can_survive_region(self, state: StateInterface, region_name: str) -> bool:
        context = self.__make_execution_context(state)
        region_data = ALL_REGION_DATA_BY_NAME[region_name]

        if region_data.is_always_survivable:
            return True

        for encounter_group_id in region_data.encounters:
            if not self.logic_manager.can_survive_encounter_group(encounter_group_id, context):
                return False

        # TODO handle for glitched logic.
        if not bool(self.options.sustain_logic_enabled):
            return True

        return self.logic_manager.can_sustain_region(region_data.sustain_score, context)

    def can_defeat_enemies(self, state: StateInterface, enemies: list[int]) -> bool:
        return self.logic_manager.can_defeat_special_encounter(enemies, self.__make_execution_context(state))

    def can_defeat_enemy(self, state: StateInterface, enemy: int) -> bool:
        return self.logic_manager.can_defeat_enemy(enemy, self.__make_execution_context(state))

    def can_fill_codex_entry(self, state: StateInterface, enemy_id: int) -> bool:
        return self.logic_manager.can_fill_codex_entry(enemy_id, self.__make_execution_context(state))

    def can_fill_compendium_entry(self, state: StateInterface, item_id: int) -> bool:
        return self.logic_manager.can_fill_compendium_entry(item_id, self.__make_execution_context(state))

    def can_unlock_shop_item(self, state: StateInterface, shop_item_id: int) -> bool:
        return self.logic_manager.can_unlock_shop_item(shop_item_id, self.__make_execution_context(state))

    def can_fully_complete_codex_and_compendium(self, state: StateInterface) -> bool:
        context = self.__make_execution_context(state)
        if self.logic_manager.get_fillable_codex_entry_count(context) != 131:
            return False
        if self.logic_manager.get_fillable_compendium_entry_count(context) != 196:
            return False
        return True

    def can_start_quest(self, state: StateInterface, quest_id: int) -> bool:
        return self.logic_manager.can_start_quest(quest_id, self.__make_execution_context(state))

    def can_complete_quest(self, state: StateInterface, quest_id: int) -> bool:
        return self.logic_manager.can_complete_quest(quest_id, self.__make_execution_context(state))
