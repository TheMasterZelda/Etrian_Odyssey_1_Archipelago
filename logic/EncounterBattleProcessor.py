from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from .ILogicManager import ExecutionContext
from .StateInterface import StateInterface
from ..Options import *
from ..Constant import *
from .LogicData import *
from ..data.EnemyData import *
from ..data.EncounterData import *

class EncounterBattleProcessor(ABC):
    def get_enemy_data(self, enemy_id: int) -> EnemyData:
        return ENEMY_BY_ID[enemy_id]

    def get_encounter_data(self, encounter_id: int) -> EncounterData:
        return ENCOUNTER_BY_ID[encounter_id]

    def get_all_encounter_enemies(self, encounter_data: EncounterData) -> list[int]:
        enemy_list: list[int] = []

        def add_if_not_zero(enemy_id: int):
            if enemy_id != 0x00:
                enemy_list.append(enemy_id)

        add_if_not_zero(encounter_data.enemy_1_id)
        add_if_not_zero(encounter_data.enemy_2_id)
        add_if_not_zero(encounter_data.enemy_3_id)
        add_if_not_zero(encounter_data.enemy_4_id)
        add_if_not_zero(encounter_data.enemy_5_id)

        return enemy_list

    @abstractmethod
    def can_defeat_enemy_group(self, enemies: list[int], context: ExecutionContext) -> bool:
        pass

    def can_defeat_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        encounter_data = self.get_encounter_data(encounter_id)
        enemy_list = self.get_all_encounter_enemies(encounter_data)

        return self.can_defeat_enemy_group(enemy_list, context)

    @abstractmethod
    def can_survive_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        pass

class SimpleEncounterBattleProcessor(EncounterBattleProcessor):
    def can_defeat_enemy_group(self, enemies: list[int], context: ExecutionContext) -> bool:
        for enemy_id in enemies:
            if enemy_id in context.logic_data.defeatable_enemy.undefeatable_enemies:
                return False

        return True

    def can_survive_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        encounter_data = self.get_encounter_data(encounter_id)
        enemy_list = self.get_all_encounter_enemies(encounter_data)

        for enemy_id in enemy_list:
            if enemy_id in context.logic_data.survivable_enemy.unsurvivable_enemies:
                return False

        return True