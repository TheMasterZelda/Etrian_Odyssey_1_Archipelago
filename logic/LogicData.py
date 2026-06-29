from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from ..data.EnemyData import *
from ..data.EncounterData import *
from ..data.EncounterGroupData import *
from ..data.CodexData import *
from ..data.CompendiumData import *
from ..data.InventoryItemData import EO1ItemNames, EO1ItemID, CONSUMABLE_DATA
from ..data.ItemCompoundData import ITEM_COMPOUND_TABLE
from ..data.MaxLevelByFloor import MAX_LEVEL_BY_FLOOR


class LogicData(ABC):
    stale: bool

    def __init__(self):
        self.stale = True

    def set_stale(self, stale: bool) -> None:
        self.stale = stale

    def is_stale(self) -> bool:
        return self.stale

    @abstractmethod
    def copy(self) -> LogicData:
        pass

class SkillLogicData(LogicData):
    skill_id: int
    skill_unlocked: bool
    skill_usable: bool
    required_skills: set[int]
    required_level: int

    def copy(self) -> SkillLogicData:
        new_copy = SkillLogicData()
        new_copy.skill_id = self.skill_id
        new_copy.skill_unlocked = self.skill_unlocked
        new_copy.skill_usable = self.skill_usable
        new_copy.required_skills = self.required_skills.copy()
        new_copy.required_level = self.required_level
        new_copy.stale = self.stale

        return new_copy

class SingleClassLogicData(LogicData):
    class_name: str
    class_unlocked: bool
    class_skills: dict[int, SkillLogicData]

    def copy(self) -> SingleClassLogicData:
        new_copy = SingleClassLogicData()
        new_copy.class_name = self.class_name
        new_copy.class_unlocked = self.class_unlocked
        new_copy.class_skills = {}
        for skill_entry in self.class_skills.values():
            new_entry = skill_entry.copy()
            new_copy.class_skills[new_entry.skill_id] = new_entry
        new_copy.stale = self.stale
        return new_copy

    @property
    def usable_skills(self) -> list[SkillLogicData]:
        return [skill_data for skill_data in self.class_skills.values() if skill_data.skill_usable]


class ClassLogicData(LogicData):
    landsknecht: SingleClassLogicData
    survivalist: SingleClassLogicData
    protector: SingleClassLogicData
    dark_hunter: SingleClassLogicData
    medic: SingleClassLogicData
    alchemist: SingleClassLogicData
    troubadour: SingleClassLogicData
    ronin: SingleClassLogicData
    hexer: SingleClassLogicData

    def copy(self) -> ClassLogicData:
        new_copy = ClassLogicData()
        new_copy.landsknecht = self.landsknecht.copy()
        new_copy.survivalist = self.survivalist.copy()
        new_copy.protector = self.protector.copy()
        new_copy.dark_hunter = self.dark_hunter.copy()
        new_copy.medic = self.medic.copy()
        new_copy.alchemist = self.alchemist.copy()
        new_copy.troubadour = self.troubadour.copy()
        new_copy.ronin = self.ronin.copy()
        new_copy.hexer = self.hexer.copy()
        new_copy.stale = self.stale
        return new_copy

    @property
    def class_as_list(self) -> list[SingleClassLogicData]:
        return [self.landsknecht, self.survivalist, self.protector, self.dark_hunter, self.medic,
                self.alchemist, self.troubadour, self.ronin, self.hexer]

    @property
    def class_as_dict(self) -> dict[str, SingleClassLogicData]:
        return {class_data.class_name:class_data for class_data in self.class_as_list}

    @property
    def unlocked_classes(self) -> list[SingleClassLogicData]:
        return [class_data for class_data in self.class_as_list if class_data.class_unlocked]

class AllLogicData:
    current_level_cap: int
    current_floor_limit: int

    class_data: ClassLogicData

    def __init__(self):
        # The management of the default values is left to the LogicManager.
        self.current_level_cap = 0
        self.current_floor_limit = 0

        self.class_data = ClassLogicData()

    def get_effective_level_cap(self):
        return min(self.current_level_cap, MAX_LEVEL_BY_FLOOR[min(self.current_floor_limit, 30)])

    def copy(self) -> AllLogicData:
        new_copy = AllLogicData()

        new_copy.current_level_cap = self.current_level_cap
        new_copy.current_floor_limit = self.current_floor_limit

        new_copy.class_data = self.class_data.copy()
        return new_copy

    def set_skill_stale(self):
        self.class_data.set_stale(True)

    def set_battle_stale(self):
        self.class_data.set_stale(True)
