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
from ..data.EncounterGroupData import *

class EncounterGroupBattleProcessor(ABC):
    def get_encounter_group_data(self, encounter_group_id: int) -> EncounterGroupData:
        return ENCOUNTER_GROUP_BY_ID[encounter_group_id]

    def get_all_encounters(self, encounter_group_data: EncounterGroupData) -> list[int]:
        encounter_list: list[int] = []

        def add_if_not_zero(encounter_id: int):
            if encounter_id != 0x00:
                encounter_list.append(encounter_id)

        add_if_not_zero(encounter_group_data.encounter_id_1)
        add_if_not_zero(encounter_group_data.encounter_id_2)
        add_if_not_zero(encounter_group_data.encounter_id_3)

        return encounter_list

    @abstractmethod
    def can_survive_encounter_group(self, encounter_group_id: int, context: ExecutionContext) -> bool:
        pass

class SimpleEncounterGroupBattleProcessor(EncounterGroupBattleProcessor):
    def can_survive_encounter_group(self, encounter_group_id: int, context: ExecutionContext) -> bool:
        encounter_group_data = self.get_encounter_group_data(encounter_group_id)

        encounter_list = self.get_all_encounters(encounter_group_data)

        for encounter_id in encounter_list:
            if not context.logic_manager.can_survive_encounter(encounter_id, context):
                return False

        return True