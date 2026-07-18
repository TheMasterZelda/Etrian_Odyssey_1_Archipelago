from __future__ import annotations
from abc import ABC, abstractmethod

# TODO Rename

class LogicCacheData(ABC):
    stale: bool

    def __init__(self):
        self.stale = True

    def set_stale(self, stale: bool) -> None:
        self.stale = stale

    def is_stale(self) -> bool:
        return self.stale

    @abstractmethod
    def copy(self) -> LogicCacheData:
        pass

class DualIntSetLogicCacheData(LogicCacheData):
    unaccessible: set[int]
    accessible: set[int]
    update_suspended: bool

    def __init__(self):
        super().__init__()
        self.unaccessible = set()
        self.accessible = set()
        self.update_suspended = False

    def copy(self) -> DualIntSetLogicCacheData:
        new_copy = DualIntSetLogicCacheData()
        self.copy_data(new_copy)
        return new_copy

    def copy_data(self, new_copy: DualIntSetLogicCacheData) -> None:
        new_copy.unaccessible = self.unaccessible.copy()
        new_copy.accessible = self.accessible.copy()
        new_copy.stale = self.stale
        new_copy.update_suspended = self.update_suspended

class IntLogicCacheValue(LogicCacheData):
    value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def copy(self) -> IntLogicCacheValue:
        new_copy = IntLogicCacheValue(self.value)
        return new_copy

class AllLogicCacheData:
    defeatable_enemy: DualIntSetLogicCacheData
    survivable_enemy: DualIntSetLogicCacheData
    defeatable_encounter: DualIntSetLogicCacheData
    survivable_encounter: DualIntSetLogicCacheData
    encounter_group: DualIntSetLogicCacheData
    codex_entry: DualIntSetLogicCacheData
    compendium_entry: DualIntSetLogicCacheData
    shop_unlock_entry: DualIntSetLogicCacheData
    sustain_score: IntLogicCacheValue

    def __init__(self):
        self.defeatable_enemy = DualIntSetLogicCacheData()
        self.survivable_enemy = DualIntSetLogicCacheData()
        self.defeatable_encounter = DualIntSetLogicCacheData()
        self.survivable_encounter = DualIntSetLogicCacheData()
        self.encounter_group = DualIntSetLogicCacheData()
        self.codex_entry = DualIntSetLogicCacheData()
        self.compendium_entry = DualIntSetLogicCacheData()
        self.shop_unlock_entry = DualIntSetLogicCacheData()
        self.sustain_score = IntLogicCacheValue(0)

    def copy(self) -> AllLogicCacheData:
        new_copy = AllLogicCacheData()

        new_copy.defeatable_enemy = self.defeatable_enemy.copy()
        new_copy.survivable_enemy = self.survivable_enemy.copy()
        new_copy.defeatable_encounter = self.defeatable_encounter.copy()
        new_copy.survivable_encounter = self.survivable_encounter.copy()
        new_copy.encounter_group = self.encounter_group.copy()
        new_copy.codex_entry = self.codex_entry.copy()
        new_copy.compendium_entry = self.compendium_entry.copy()
        new_copy.shop_unlock_entry = self.shop_unlock_entry.copy()
        new_copy.sustain_score = self.sustain_score.copy()
        return new_copy

    def set_update_suspended(self, update_suspended: bool) -> None:
        self.defeatable_enemy.update_suspended = update_suspended
        self.survivable_enemy.update_suspended = update_suspended
        self.defeatable_encounter.update_suspended = update_suspended
        self.survivable_encounter.update_suspended = update_suspended
        self.encounter_group.update_suspended = update_suspended
        self.codex_entry.update_suspended = update_suspended
        self.compendium_entry.update_suspended = update_suspended
        self.shop_unlock_entry.update_suspended = update_suspended
        #self.sustain_score.update_suspended = update_suspended

    #def set_skill_stale(self):
        #self.class_data.set_stale(True)

    def set_battle_stale(self):
        #self.class_data.set_stale(True)
        self.defeatable_enemy.set_stale(True)
        self.survivable_enemy.set_stale(True)
        self.defeatable_encounter.set_stale(True)
        self.survivable_encounter.set_stale(True)
        self.encounter_group.set_stale(True)
        self.codex_entry.set_stale(True)
        self.compendium_entry.set_stale(True)
        self.shop_unlock_entry.set_stale(True)
        self.sustain_score.set_stale(True)

    def set_location_stale(self):
        self.codex_entry.set_stale(True)
        self.compendium_entry.set_stale(True)
        self.shop_unlock_entry.set_stale(True)
        self.sustain_score.set_stale(True)

    def set_shop_unlock_stale(self):
        self.shop_unlock_entry.set_stale(True)
        self.sustain_score.set_stale(True)