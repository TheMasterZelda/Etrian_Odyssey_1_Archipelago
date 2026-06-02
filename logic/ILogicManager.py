from __future__ import annotations
from abc import ABC, abstractmethod

from .LogicData import AllLogicData
from .StateInterface import StateInterface

class ExecutionContext:
    logic_manager: ILogicManager
    state: StateInterface
    logic_data: AllLogicData

class ILogicManager(ABC):
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