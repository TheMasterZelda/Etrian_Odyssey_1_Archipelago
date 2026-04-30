from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from .LogicData import *

from BaseClasses import CollectionState

from ..data.EnemyData import *
from ..data.MaxLevelByFloor import MAX_LEVEL_BY_FLOOR

from enum import Enum
class DefeatCondition(Enum):
    STAB = "STAB"
    NOT_STAB = "NOT_STAB"
    FIRE = "FIRE"
    NOT_FIRE = "NOT_FIRE"
    ICE = "ICE"
    NOT_ICE = "NOT_ICE"
    BASH = "BASH"
    NOT_BASH = "NOT_BASH"
    PHYSICAL = "PHYSICAL"
    NOT_PHYSICAL = "NOT_PHYSICAL"

_MAX_FLOOR = 30


class SingleEnemyBattleProcessor(ABC):
    def get_enemy_data(self, enemy_id: int) -> EnemyData:
        return ENEMY_BY_ID[enemy_id]

    @abstractmethod
    def can_defeat_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        pass

    @abstractmethod
    def can_survive_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        pass

    #@abstractmethod
    #def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, state: CollectionState, logic_data: AllLogicData) -> bool:
    #    pass

    def max_level_for_defeat(self, logic_data: AllLogicData):
        return min(logic_data.current_level_cap, MAX_LEVEL_BY_FLOOR[min(logic_data.current_floor_limit, _MAX_FLOOR)])

class LevelOnlySingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def can_survive_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        #enemy_data.level * (95/100) - 5
        return logic_data.current_level_cap >= max(1, effective_enemy_level)

    def can_defeat_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        #enemy_data.level * (95/100) - 5
        return self.max_level_for_defeat(logic_data) >= max(1, effective_enemy_level)

class NoLogicSingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def can_survive_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        return True

    def can_defeat_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        return True

    #def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, state: CollectionState, logic_data: AllLogicData) -> bool:


