from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from ..data.EnemyData import *
from ..data.EncounterData import *
from ..data.EncounterGroupData import *
from ..data.CodexData import *
from ..data.CompendiumData import *
from ..data.InventoryItemData import EO1ItemNames, EO1ItemID, CONSUMABLE_DATA
from ..data.MaxLevelByFloor import MAX_LEVEL_BY_FLOOR

if TYPE_CHECKING:
    from .. import EtrianOdysseyWorld

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

class DualIntSetLogicData(LogicData):
    unaccessible: set[int]
    accessible: set[int]

    def __init__(self, fill_default: bool):
        super().__init__()
        self.unaccessible = set()
        self.accessible = set()

        if fill_default:
            self.fill_default()

    def copy_data(self, new_copy: DualIntSetLogicData) -> None:
        new_copy.unaccessible = self.unaccessible.copy()
        new_copy.accessible = self.accessible.copy()
        new_copy.stale = self.stale

    @abstractmethod
    def fill_default(self) -> None:
        pass

class DefeatableEnemyLogicData(DualIntSetLogicData):
    def copy(self) -> DefeatableEnemyLogicData:
        new_copy = DefeatableEnemyLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for enemy_data in ALL_ENEMIES:
            self.undefeatable_enemies.add(enemy_data.enemy_id)

    @property
    def undefeatable_enemies(self) -> set[int]:
        return self.unaccessible
    @property
    def defeatable_enemies(self) -> set[int]:
        return self.accessible

class SurvivableEnemyLogicData(DualIntSetLogicData):
    def copy(self) -> SurvivableEnemyLogicData:
        new_copy = SurvivableEnemyLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for enemy_data in ALL_ENEMIES:
            self.unsurvivable_enemies.add(enemy_data.enemy_id)

    @property
    def unsurvivable_enemies(self) -> set[int]:
        return self.unaccessible
    @property
    def survivable_enemies(self) -> set[int]:
        return self.accessible

class DefeatableEncounterLogicData(DualIntSetLogicData):
    def copy(self) -> DefeatableEncounterLogicData:
        new_copy = DefeatableEncounterLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for enemy_data in ALL_ENCOUNTERS:
            self.undefeatable_encounters.add(enemy_data.encounter_id)

    @property
    def undefeatable_encounters(self) -> set[int]:
        return self.unaccessible
    @property
    def defeatable_encounters(self) -> set[int]:
        return self.accessible

class SurvivableEncounterLogicData(DualIntSetLogicData):
    def copy(self) -> SurvivableEncounterLogicData:
        new_copy = SurvivableEncounterLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for enemy_data in ALL_ENCOUNTERS:
            self.unsurvivable_encounters.add(enemy_data.encounter_id)

    @property
    def unsurvivable_encounters(self) -> set[int]:
        return self.unaccessible
    @property
    def survivable_encounters(self) -> set[int]:
        return self.accessible

class EncounterGroupLogicData(DualIntSetLogicData):
    def copy(self) -> EncounterGroupLogicData:
        new_copy = EncounterGroupLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for encounter_group_data in ALL_ENCOUNTER_GROUPS:
            self.unsurvivable_encounter_groups.add(encounter_group_data.encounter_group_id)

    @property
    def unsurvivable_encounter_groups(self) -> set[int]:
        return self.unaccessible
    @property
    def survivable_encounter_groups(self) -> set[int]:
        return self.accessible

class CodexLogicData(DualIntSetLogicData):
    def copy(self) -> CodexLogicData:
        new_copy = CodexLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for codex_data in ALL_CODEX_ENTRIES:
            self.unfillable_codex_entries.add(codex_data.enemy_id)

    @property
    def unfillable_codex_entries(self) -> set[int]:
        return self.unaccessible
    @property
    def fillable_codex_entries(self) -> set[int]:
        return self.accessible

class CompendiumLogicData(DualIntSetLogicData):
    def copy(self) -> CompendiumLogicData:
        new_copy = CompendiumLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for compendium_data in COMPENDIUM_TABLE:
            self.unfillable_compendium_entries.add(compendium_data.item_id)

    @property
    def unfillable_compendium_entries(self) -> set[int]:
        return self.unaccessible
    @property
    def fillable_compendium_entries(self) -> set[int]:
        return self.accessible

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

#class SustainLogicData(LogicData):
#    current_max_sustain_score: int

class ShopUnlockLogicData(DualIntSetLogicData):
    def copy(self) -> ShopUnlockLogicData:
        new_copy = ShopUnlockLogicData(fill_default=False)
        self.copy_data(new_copy)
        return new_copy

    def fill_default(self) -> None:
        for consumable_data in CONSUMABLE_DATA:
            # Warp wires are a special kind of unlock item handled differently.
            if consumable_data.item_id == EO1ItemID.WARP_WIRE:
                continue
            self.non_unlockable_shop_items.add(consumable_data.item_id)

    @property
    def non_unlockable_shop_items(self) -> set[int]:
        return self.unaccessible
    @property
    def unlockable_shop_items(self) -> set[int]:
        return self.accessible

class AllLogicData:
    current_level_cap: int
    current_floor_limit: int

    class_data: ClassLogicData
    defeatable_enemy: DefeatableEnemyLogicData
    survivable_enemy: SurvivableEnemyLogicData
    defeatable_encounter: DefeatableEncounterLogicData
    survivable_encounter: SurvivableEncounterLogicData
    encounter_group: EncounterGroupLogicData
    codex_logic_data: CodexLogicData
    compendium_logic_data: CompendiumLogicData
    shop_unlock_logic_data: ShopUnlockLogicData
    #SustainLogicData

    def __init__(self, fill_default: bool):
        # The management of the default values is left to the LogicManager.
        self.current_level_cap = 0
        self.current_floor_limit = 0

        self.class_data = ClassLogicData()
        self.defeatable_enemy = DefeatableEnemyLogicData(fill_default)
        self.survivable_enemy = SurvivableEnemyLogicData(fill_default)
        self.defeatable_encounter = DefeatableEncounterLogicData(fill_default)
        self.survivable_encounter = SurvivableEncounterLogicData(fill_default)
        self.encounter_group = EncounterGroupLogicData(fill_default)
        self.codex_logic_data = CodexLogicData(fill_default)
        self.compendium_logic_data = CompendiumLogicData(fill_default)
        self.shop_unlock_logic_data = ShopUnlockLogicData(fill_default)
        # Sustain

    def get_effective_level_cap(self):
        return min(self.current_level_cap, MAX_LEVEL_BY_FLOOR[min(self.current_floor_limit, 30)])

    def copy(self) -> AllLogicData:
        new_copy = AllLogicData(fill_default=False)

        new_copy.current_level_cap = self.current_level_cap
        new_copy.current_floor_limit = self.current_floor_limit

        new_copy.class_data = self.class_data.copy()
        new_copy.defeatable_enemy = self.defeatable_enemy.copy()
        new_copy.survivable_enemy = self.survivable_enemy.copy()
        new_copy.defeatable_encounter = self.defeatable_encounter.copy()
        new_copy.survivable_encounter = self.survivable_encounter.copy()
        new_copy.encounter_group = self.encounter_group.copy()
        new_copy.codex_logic_data = self.codex_logic_data.copy()
        new_copy.compendium_logic_data = self.compendium_logic_data.copy()
        new_copy.shop_unlock_logic_data = self.shop_unlock_logic_data.copy()
        #SustainLogicData
        return new_copy

    def set_skill_stale(self):
        self.class_data.set_stale(True)

    def set_battle_stale(self):
        self.class_data.set_stale(True)
        self.defeatable_enemy.set_stale(True)
        self.survivable_enemy.set_stale(True)
        self.defeatable_encounter.set_stale(True)
        self.survivable_encounter.set_stale(True)
        self.encounter_group.set_stale(True)
        self.codex_logic_data.set_stale(True)
        self.compendium_logic_data.set_stale(True)
        self.shop_unlock_logic_data.set_stale(True)

    def set_location_stale(self):
        self.codex_logic_data.set_stale(True)
        self.compendium_logic_data.set_stale(True)
        self.shop_unlock_logic_data.set_stale(True)
