from __future__ import annotations

from .DataSource import SingleDataSource
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

def build_skill_requirements_source(randomized_game_data: RandomizedGameData) -> dict[int, EO1Class2SkillData]:
    skill_requirement_source: dict[int, EO1Class2SkillData] = {}

    for skill_requirement in randomized_game_data.skill_requirements:
        skill_requirement_source[skill_requirement.skill_id] = EO1Class2SkillData(
            skill_requirement.skill_id,
            skill_requirement.required_skill_1_id,
            skill_requirement.required_skill_1_level,
            skill_requirement.required_skill_2_id,
            skill_requirement.required_skill_2_level)
    return skill_requirement_source

class LogicProxy:
    logic_data: AllLogicData
    logic_cache_data: AllLogicCacheData
    options: EtrianOdysseyOptions
    logic_manager: LogicManager
    randomized_game_data: RandomizedGameData

    def __init__(self, options: EtrianOdysseyOptions, randomized_game_data: RandomizedGameData, initialize=True) -> None:
        if not randomized_game_data.initialized:
            raise Exception("RandomizedGameData was not initialized.")

        self.options = options
        self.randomized_game_data = randomized_game_data

        if not initialize:
            return

        self.logic_data = AllLogicData()
        self.logic_cache_data = AllLogicCacheData()

        data_source = EtrianOdysseyDataSource()

        if self.randomized_game_data.skill_requirements:
            data_source.skill_requirements_data_source = SingleDataSource(build_skill_requirements_source(self.randomized_game_data))
        #else:
        #    raise Exception("No rando?")

        self.logic_manager = LogicManager(self.options, data_source)
        self.logic_manager.initialize_data(self.logic_data, self.options)
        self.logic_manager.initialize_cache(self.logic_cache_data)

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

    def reached_region(self, state: StateInterface, region: Region):
        self.logic_manager.on_reached_region(region.name, self.__make_execution_context(state))

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
            #print(self.logic_cache_data.codex_entry.unaccessible)
            return False
        if self.logic_manager.get_fillable_compendium_entry_count(context) != 196:
            #print(self.logic_cache_data.compendium_entry.unaccessible)
            return False
        #print("Full Codex & Compendium")
        return True

    def can_start_quest(self, state: StateInterface, quest_id: int) -> bool:
        return self.logic_manager.can_start_quest(quest_id, self.__make_execution_context(state))

    def can_complete_quest(self, state: StateInterface, quest_id: int) -> bool:
        return self.logic_manager.can_complete_quest(quest_id, self.__make_execution_context(state))
