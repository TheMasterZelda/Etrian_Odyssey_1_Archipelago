from __future__ import annotations
from abc import ABC, abstractmethod

from .LogicCacheData import AllLogicCacheData
from .LogicData import AllLogicData
from .StateInterface import StateInterface

class ExecutionContext:
    logic_manager: ILogicManager
    state: StateInterface
    logic_data: AllLogicData
    cache_data: AllLogicCacheData

class ILogicManager(ABC):
    @abstractmethod
    def on_item_collect(self, item_id: int, item_type: int, context: ExecutionContext) -> None:
        pass

    @abstractmethod
    def on_item_remove(self, item_id: int, item_type: int, context: ExecutionContext) -> None:
        pass

    @abstractmethod
    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_defeat_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_defeat_special_encounter(self, enemies: list[int], context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_survive_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_survive_encounter_group(self, encounter_group_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_unlock_shop_item(self, shop_item_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_fill_compendium_entry(self, item_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_fill_codex_entry(self, enemy_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def get_fillable_codex_entry_count(self, context: ExecutionContext) -> int:
        pass

    @abstractmethod
    def get_fillable_compendium_entry_count(self, context: ExecutionContext) -> int:
        pass