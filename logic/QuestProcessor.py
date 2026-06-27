from __future__ import annotations
from typing import Callable

from .EncounterBattleProcessor import EncounterBattleProcessor
from .ILogicManager import ExecutionContext
from .StateInterface import StateInterface
from ..data.InventoryItemData import EO1KeyItem, KEY_ITEM_DATA_BY_ITEM_ID
from ..data.QuestData import *
from ..data.RegionData import *

from .LogicData import *

class QuestProcessor:
    region_cache: set[str] | None

    def __can_reach_region_requirement(self, param: CanReachRegion, context: ExecutionContext) -> bool:
        return context.state.can_reach_region(param.region)

    def __can_obtain_material_requirement(self, param: CanObtainMaterial, context: ExecutionContext) -> bool:
        for material_id in param.item_id:
            if not context.logic_manager.can_fill_compendium_entry(material_id, context):
                return False

        # Passed all items.
        return True

    def __has_quest_item_requirement(self, param: HasQuestItem, context: ExecutionContext) -> bool:
        raise Exception("__has_quest_item_requirement")

    def __has_class_of_level_requirement(self, param: HasClassOfLevel, context: ExecutionContext) -> bool:
        class_data = context.logic_data.class_data.class_as_dict[param.class_name]
        if not class_data.class_unlocked:
            return False

        return context.logic_data.get_effective_level_cap() >= param.required_level

    def __has_class_and_skill_requirement(self, param: HasClassAndSkill, context: ExecutionContext) -> bool:
        class_data = context.logic_data.class_data.class_as_dict[param.class_name]
        if not class_data.class_unlocked:
            return False

        skill_data = class_data.class_skills[param.skill_id]
        return skill_data.skill_usable

    def __can_solo_enemy_requirement(self, param: CanSoloEnemy, context: ExecutionContext) -> bool:
        def has_any(class_skills: dict[int, SkillLogicData], skills: list[int]) -> bool:
            for skill in skills:
                if class_skills[skill].skill_usable:
                    return True
            return False

        def has_class_and_skill(class_name: str, skill_requirements: list[list[int]]) -> bool:
            if not context.logic_data.class_data.class_as_dict[class_name].class_unlocked:
                return False

            for skill_requirement in skill_requirements:
                if not has_any(context.logic_data.class_data.class_as_dict[class_name].class_skills, skill_requirement):
                    return False
            return True

        enemy_data = ENEMY_BY_ID[param.enemy_id]
        if param.enemy_id == EO1Enemies.CUTTER:
            if context.logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if not context.logic_manager.can_unlock_shop_item(EO1ItemID.MEDICA_III, context):
                if not context.logic_manager.can_unlock_shop_item(EO1ItemID.MEDICA_IV, context):
                    return False
        elif param.enemy_id == EO1Enemies.KILLCLAW:
            if context.logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if not context.logic_manager.can_unlock_shop_item(EO1ItemID.MEDICA_IV, context):
                return False
        elif param.enemy_id == EO1Enemies.SICKWOOD:
            if context.logic_data.get_effective_level_cap() < enemy_data.level + 10:
                return False
            if not context.logic_manager.can_unlock_shop_item(EO1ItemID.MEDICA_IV, context):
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
            if context.logic_data.get_effective_level_cap() >= enemy_data.level + 15:
                return True

        return False

    def __can_fill_x_monster_codex_entries_requirement(self, param: CanFillXMonsterCodexEntries, context: ExecutionContext) -> bool:
        currently_fillable_count = context.logic_manager.get_fillable_codex_entry_count(context)
        return currently_fillable_count >= param.entries_count

    def __can_fill_x_item_compendium_entries_requirement(self, param: CanFillXItemCompendiumEntries, context: ExecutionContext) -> bool:
        currently_fillable_count = context.logic_manager.get_fillable_compendium_entry_count(context)
        return currently_fillable_count >= param.entries_count

    def __can_defeat_encounter_requirement(self, param: CanDefeatEncounter, context: ExecutionContext) -> bool:
        return context.logic_manager.can_defeat_special_encounter(param.enemies, context)

    quest_completion_requirement_lookup: dict[QuestCompletionRequirementType, Callable[[QuestProcessor, QuestCompletionRequirement, ExecutionContext], bool]] = {
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

    def __init__(self) -> None:
        self.region_cache = None

    def __requirement_met(self, requirement: QuestCompletionRequirement, context: ExecutionContext) -> bool:
        requirement_type = requirement.requirement_type

        if requirement_type not in QuestProcessor.quest_completion_requirement_lookup:
            raise Exception(f"QuestRequirementType {requirement_type} is not implemented.")

        return QuestProcessor.quest_completion_requirement_lookup[requirement_type](self, requirement, context)

    def __can_reach_floor(self, floor_number: int, context: ExecutionContext) -> bool:
        if floor_number > context.logic_data.current_floor_limit:
            return False
        all_floor_regions = ALL_REGIONS_BY_FLOOR[floor_number]
        for region in all_floor_regions:
            # TODO: This is to handle unaccessible regions from the goal. This could have a better implementation.
            if region not in self.region_cache:
                continue
            if context.state.can_reach_region(region):
                return True
        return False

    def can_start_quest(self, quest_id: int, context: ExecutionContext) -> bool:
        if self.region_cache is None:
            self.region_cache = set(context.state.get_regions())

        quest_data = QUEST_DATA_BY_QUEST_ID[quest_id]

        # Note: Every quest has a requirement of having Mission 1 completed. However, Mission 1 is always completable
        # and this won't be changed (map cannot be shuffled).

        if quest_data.floor_requirement != -1:
            if not self.__can_reach_floor(quest_data.floor_requirement, context):
                return False

        if quest_data.level_requirement != -1:
            if quest_data.level_requirement > context.logic_data.get_effective_level_cap():
                return False

        if quest_data.quest_unlock_requirement == QuestRequirement.NONE:
            return True
        elif quest_data.quest_unlock_requirement == QuestRequirement.KEY_ITEM:
            key_item_data = KEY_ITEM_DATA_BY_ITEM_ID[quest_data.quest_unlock_requirement_value]
            return context.state.has_item(key_item_data.name)
        elif quest_data.quest_unlock_requirement == QuestRequirement.QUEST:
            return self.can_complete_quest(quest_data.quest_unlock_requirement_value, context)
        elif quest_data.quest_unlock_requirement == QuestRequirement.BEAT_STORY:
            if not context.state.can_reach_region(EO1Regions.B25F_ETREANT_ROOM):
                return False
            return context.logic_manager.can_defeat_enemy(EO1Enemies.ETREANT, context)
        else:
            raise Exception(f"Unknown QuestRequirement: {quest_data.quest_unlock_requirement}")

    def can_complete_quest(self, quest_id: int, context: ExecutionContext) -> bool:
        if self.region_cache is None:
            self.region_cache = set(context.state.get_regions())

        if not self.can_start_quest(quest_id, context):
            return False

        quest_data = QUEST_DATA_BY_QUEST_ID[quest_id]
        quest_completion_requirements = quest_data.quest_completion_requirements

        if quest_completion_requirements is None:
            raise Exception(f"Quest {quest_id} is lacking a completion requirement")
        if not quest_completion_requirements:
            raise Exception(f"Quest {quest_id} is lacking a completion requirement")

        for completion_requirement in quest_completion_requirements:
            if not self.__requirement_met(completion_requirement, context):
                return False

        # Every requirement met.
        return True
