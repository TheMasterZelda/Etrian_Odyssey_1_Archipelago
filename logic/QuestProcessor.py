from __future__ import annotations
from BaseClasses import CollectionState
from typing import Callable

from .EncounterBattleProcessor import EncounterBattleProcessor
from ..data.InventoryItemData import EO1KeyItem, KEY_ITEM_DATA_BY_ITEM_ID
from ..data.QuestData import *
from ..data.RegionData import *

from .LogicData import *

class QuestProcessor:
    player_id: int
    encounter_battle_processor: EncounterBattleProcessor


    def __can_reach_region_requirement(self, param: CanReachRegion, logic_data: AllLogicData, state: CollectionState) -> bool:
        return state.can_reach_region(param.region, self.player_id)

    def __can_obtain_material_requirement(self, param: CanObtainMaterial, logic_data: AllLogicData, state: CollectionState) -> bool:
        for material_id in param.item_id:
            if material_id not in logic_data.compendium_logic_data.fillable_compendium_entries:
                return False

        # Passed all items.
        return True

    def __has_quest_item_requirement(self, param: HasQuestItem, logic_data: AllLogicData, state: CollectionState) -> bool:
        raise Exception("__has_quest_item_requirement")

    def __has_class_of_level_requirement(self, param: HasClassOfLevel, logic_data: AllLogicData, state: CollectionState) -> bool:
        class_data = logic_data.class_data.class_as_dict[param.class_name]
        if not class_data.class_unlocked:
            return False

        return logic_data.get_effective_level_cap() >= param.required_level

    def __has_class_and_skill_requirement(self, param: HasClassAndSkill, logic_data: AllLogicData, state: CollectionState) -> bool:
        class_data = logic_data.class_data.class_as_dict[param.class_name]
        if not class_data.class_unlocked:
            return False

        skill_data = class_data.class_skills[param.skill_id]
        return skill_data.skill_usable

    def __can_solo_enemy_requirement(self, param: CanSoloEnemy, logic_data: AllLogicData, state: CollectionState) -> bool:
        def has_any(class_skills: dict[int, SkillLogicData], skills: list[int]) -> bool:
            for skill in skills:
                if class_skills[skill].skill_usable:
                    return True
            return False

        def has_class_and_skill(class_name: str, skill_requirements: list[list[int]]) -> bool:
            if not logic_data.class_data.class_as_dict[class_name].class_unlocked:
                return False

            for skill_requirement in skill_requirements:
                if not has_any(logic_data.class_data.class_as_dict[class_name].class_skills, skill_requirement):
                    return False
            return True

        enemy_data = ENEMY_BY_ID[param.enemy_id]
        if param.enemy_id == EO1Enemies.CUTTER:
            if logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if EO1ItemID.MEDICA_III not in logic_data.shop_unlock_logic_data.unlockable_shop_items:
                if EO1ItemID.MEDICA_IV not in logic_data.shop_unlock_logic_data.unlockable_shop_items:
                    return False
        elif param.enemy_id == EO1Enemies.KILLCLAW:
            if logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if EO1ItemID.MEDICA_IV not in logic_data.shop_unlock_logic_data.unlockable_shop_items:
                return False
        elif param.enemy_id == EO1Enemies.SICKWOOD:
            if logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if EO1ItemID.MEDICA_IV not in logic_data.shop_unlock_logic_data.unlockable_shop_items:
                return False
        else:
            raise Exception(f"Can Solo Enemy quest requirement not implemented for enemy {param.enemy_id}")

        if has_class_and_skill(EO1Class.PROTECTOR, [
            [EO1Skills.PROTECTOR_SMITE],
            [EO1Skills.PROTECTOR_DEF_UP, EO1Skills.PROTECTOR_HP_UP]
        ]):
            return True

        if has_class_and_skill(EO1Class.LANDSKNECHT, [
            [EO1Skills.LANDSKNECHT_CLEAVER, EO1Skills.LANDSKNECHT_TORNADO, EO1Skills.LANDSKNECHT_CRUSH,
             EO1Skills.LANDSKNECHT_STUNNER],
            [EO1Skills.LANDSKNECHT_DEF_UP, EO1Skills.LANDSKNECHT_HP_UP],
            [EO1Skills.LANDSKNECHT_ATK_UP, EO1Skills.LANDSKNECHT_WAR_CRY, EO1Skills.LANDSKNECHT_HELL_CRY]
        ]):
            return True

        if has_class_and_skill(EO1Class.SURVIVALIST, [
            [EO1Skills.SURVIVALIST_TRUESHOT, EO1Skills.SURVIVALIST_MULTIHIT],
            [EO1Skills.SURVIVALIST_HP_UP, EO1Skills.SURVIVALIST_TRICKERY]
        ]):
            return True

        if has_class_and_skill(EO1Class.DARK_HUNTER, [
            [EO1Skills.DARK_HUNTER_VIPER, EO1Skills.DARK_HUNTER_GAG, EO1Skills.DARK_HUNTER_CUFFS, EO1Skills.DARK_HUNTER_SHACKLES, EO1Skills.DARK_HUNTER_HYPNOS, EO1Skills.DARK_HUNTER_NERVE, EO1Skills.DARK_HUNTER_PETRIFY, EO1Skills.DARK_HUNTER_DRAIN, EO1Skills.DARK_HUNTER_MIRAGE],
            [EO1Skills.DARK_HUNTER_HP_UP, EO1Skills.DARK_HUNTER_DRAIN],
        ]):
            return True

        if has_class_and_skill(EO1Class.RONIN, [
            [EO1Skills.RONIN_KESAGIRI, EO1Skills.RONIN_ZAMBA, EO1Skills.RONIN_MIDAREBA, EO1Skills.RONIN_OROCHI, EO1Skills.RONIN_RAIZUKI, EO1Skills.RONIN_GATOTSU, EO1Skills.RONIN_HYOSETSU],
            [EO1Skills.RONIN_HP_UP, EO1Skills.RONIN_ATK_UP]
        ]):
            return True

        if has_class_and_skill(EO1Class.ALCHEMIST, [
            [EO1Skills.ALCHEMIST_FLAME, EO1Skills.ALCHEMIST_FREEZE, EO1Skills.ALCHEMIST_THUNDER],
        ]):
            # Alchemist have a higher level requirement due to being squishy.
            if logic_data.get_effective_level_cap() >= enemy_data.level + 15:
                return True

        return False

    def __can_fill_x_monster_codex_entries_requirement(self, param: CanFillXMonsterCodexEntries, logic_data: AllLogicData, state: CollectionState) -> bool:
        currently_fillable_count = len(logic_data.codex_logic_data.fillable_codex_entries)
        return currently_fillable_count >= param.entries_count

    def __can_fill_x_item_compendium_entries_requirement(self, param: CanFillXItemCompendiumEntries, logic_data: AllLogicData, state: CollectionState) -> bool:
        currently_fillable_count = len(logic_data.compendium_logic_data.fillable_compendium_entries)
        return currently_fillable_count >= param.entries_count

    def __can_defeat_encounter_requirement(self, param: CanDefeatEncounter, logic_data: AllLogicData, state: CollectionState) -> bool:
        return self.encounter_battle_processor.can_defeat_enemy_group(param.enemies, state, logic_data)

    quest_completion_requirement_lookup: dict[QuestCompletionRequirementType, Callable[[QuestProcessor, QuestCompletionRequirement, AllLogicData, CollectionState], bool]] = {
        QuestCompletionRequirementType.CAN_REACH_REGION: __can_reach_region_requirement,
        QuestCompletionRequirementType.CAN_OBTAIN_MATERIAL: __can_obtain_material_requirement,
        QuestCompletionRequirementType.HAS_QUEST_ITEM: __has_quest_item_requirement,
        QuestCompletionRequirementType.HAS_CLASS_OF_LEVEL: __has_class_of_level_requirement,
        QuestCompletionRequirementType.HAS_CLASS_AND_SKILL: __has_class_and_skill_requirement,
        QuestCompletionRequirementType.CAN_SOLO_ENEMY: __can_solo_enemy_requirement,
        QuestCompletionRequirementType.CAN_FILL_X_MONSTER_CODEX_ENTRIES: __can_fill_x_monster_codex_entries_requirement,
        QuestCompletionRequirementType.CAN_FILL_X_ITEM_COMPENDIUM_ENTRIES: __can_fill_x_item_compendium_entries_requirement,
        QuestCompletionRequirementType.CAN_DEFEAT_ENCOUNTER: __can_defeat_encounter_requirement,
    }

    def __init__(self, player_id: int, encounter_battle_processor: EncounterBattleProcessor) -> None:
        self.player_id = player_id
        self.encounter_battle_processor = encounter_battle_processor

    def __requirement_met(self, requirement: QuestCompletionRequirement, logic_data: AllLogicData, state: CollectionState) -> bool:
        requirement_type = requirement.requirement_type

        if requirement_type not in QuestProcessor.quest_completion_requirement_lookup:
            raise Exception(f"QuestRequirementType {requirement_type} is not implemented.")

        return QuestProcessor.quest_completion_requirement_lookup[requirement_type](self, requirement, logic_data, state)

    def __can_reach_floor(self, floor_number: int, logic_data: AllLogicData,  state: CollectionState) -> bool:
        if floor_number > logic_data.current_floor_limit:
            return False
        all_floor_regions = ALL_REGIONS_BY_FLOOR[floor_number]
        for region in all_floor_regions:
            # TODO: This is to handle unaccessible regions from the goal. This could have a better implementation.
            if region not in state.multiworld.regions.region_cache[self.player_id]:
                continue
            if state.can_reach_region(region, self.player_id):
                return True
        return False

    def can_start_quest(self, quest_id: int, logic_data: AllLogicData, state: CollectionState) -> bool:
        quest_data = QUEST_DATA_BY_QUEST_ID[quest_id]

        # Note: Every quest has a requirement of having Mission 1 completed. However, Mission 1 is always completable
        # and this won't be changed (map cannot be shuffled).

        if quest_data.floor_requirement != -1:
            if not self.__can_reach_floor(quest_data.floor_requirement, logic_data, state):
                return False

        if quest_data.level_requirement != -1:
            if quest_data.level_requirement > logic_data.get_effective_level_cap():
                return False

        if quest_data.quest_unlock_requirement == QuestRequirement.NONE:
            return True
        elif quest_data.quest_unlock_requirement == QuestRequirement.KEY_ITEM:
            key_item_data = KEY_ITEM_DATA_BY_ITEM_ID[quest_data.quest_unlock_requirement_value]
            return state.has(key_item_data.name, self.player_id)
        elif quest_data.quest_unlock_requirement == QuestRequirement.QUEST:
            return self.can_complete_quest(quest_data.quest_unlock_requirement_value, logic_data, state)
        elif quest_data.quest_unlock_requirement == QuestRequirement.BEAT_STORY:
            if not state.can_reach_region(EO1Regions.B25F_ETREANT_ROOM, self.player_id):
                return False
            return EO1Enemies.ETREANT in logic_data.defeatable_enemy.defeatable_enemies
        else:
            raise Exception(f"Unknown QuestRequirement: {quest_data.quest_unlock_requirement}")

    def can_complete_quest(self, quest_id: int, logic_data: AllLogicData, state: CollectionState) -> bool:
        if not self.can_start_quest(quest_id, logic_data, state):
            return False

        quest_data = QUEST_DATA_BY_QUEST_ID[quest_id]
        quest_completion_requirements = quest_data.quest_completion_requirements

        if quest_completion_requirements is None:
            raise Exception(f"Quest {quest_id} is lacking a completion requirement")
        if not quest_completion_requirements:
            raise Exception(f"Quest {quest_id} is lacking a completion requirement")

        for completion_requirement in quest_completion_requirements:
            if not self.__requirement_met(completion_requirement, logic_data, state):
                return False

        # Every requirement met.
        return True
