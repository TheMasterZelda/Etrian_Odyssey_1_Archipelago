from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from .ILogicManager import ExecutionContext
from .LogicData import *
from .StateInterface import StateInterface

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


class SingleEnemyBattleProcessor(ABC):
    def get_enemy_data(self, enemy_id: int) -> EnemyData:
        return ENEMY_BY_ID[enemy_id]

    @abstractmethod
    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, context: ExecutionContext) -> bool:
        pass

class LevelOnlySingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        #enemy_data.level * (95/100) - 5
        # TODO use effective level cap instead?
        return context.logic_data.current_level_cap >= max(1, effective_enemy_level)

    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        #enemy_data.level * (95/100) - 5
        return context.logic_data.get_effective_level_cap() >= max(1, effective_enemy_level)

    def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, context: ExecutionContext) -> bool:
        return self.can_defeat_enemy(enemy_id, context)

class NoLogicSingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        return True

    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        return True

    def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, context: ExecutionContext) -> bool:
        # TODO Check for actual things for the "Kill in X Turns" drop conditions.
        return True


