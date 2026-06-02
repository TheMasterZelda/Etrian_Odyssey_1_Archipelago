from BaseClasses import CollectionState
from ..data.EnemyData import *
from .LogicData import *
from .SingleEnemyBattleProcessor import SingleEnemyBattleProcessor
from ..data.SkillData import SKILL_DATA_BY_ID, EO1SkillData
from .SkillHelper import *


class ConditionalDropProcessor:

    single_enemy_battle_processor: SingleEnemyBattleProcessor

    def __init__(self, single_enemy_battle_processor: SingleEnemyBattleProcessor):
        self.single_enemy_battle_processor = single_enemy_battle_processor

    def __is_conditional_ignorable_for_regular_drops(self, drop_condition: DropCondition) -> bool:
        if drop_condition in {
            DropCondition.NONE,
            DropCondition.KILL_1_TURNS,
            DropCondition.KILL_2_TURNS,
            DropCondition.KILL_3_TURNS,
            DropCondition.KILL_7_TURNS,
            DropCondition.FULL_BIND,
            DropCondition.INSTANT_DEATH # Instant death is never considered to proc in battle logic.
        }:
            return True
        if drop_condition in {
            DropCondition.STAB,
            DropCondition.FIRE,
            DropCondition.ICE,
            DropCondition.NOT_BASH,
            DropCondition.NOT_STAB,
            DropCondition.NOT_PHYSICAL,
            DropCondition.NOT_FIRE
        }:
            return False
        raise Exception(f"Unknown drop_condition: {drop_condition}")

    def __any_usable_skill_deal_damage_type(self, class_logic_data: list[SingleClassLogicData], damage_type: EO1Element) -> bool:
        for class_data in class_logic_data:
            for skill in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill.skill_id]
                if is_damage_type(skill_data, damage_type):
                    return True
        return False

    def __any_usable_skill_deal_not_damage_type(self, class_logic_data: list[SingleClassLogicData], damage_type: EO1Element) -> bool:
        for class_data in class_logic_data:
            for skill in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill.skill_id]
                if is_not_damage_type(skill_data, damage_type):
                    return True
        return False

    def __any_usable_skill_deal_not_physical(self, class_logic_data: list[SingleClassLogicData]) -> bool:
        for class_data in class_logic_data:
            for skill in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill.skill_id]
                if is_not_physical_damage_type(skill_data):
                    return True
        return False

    def __any_usable_skill_can_inflict_ailment(self, class_logic_data: list[SingleClassLogicData], ailment: EO1Ailment) -> bool:
        for class_data in class_logic_data:
            for skill in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill.skill_id]
                if can_inflict_ailment(skill_data, ailment):
                    return True
        return False

    def can_defeat_without_fulfilling_drop_condition(self, enemy_id: int, logic_data: AllLogicData) -> bool:
        enemy_data = ENEMY_BY_ID[enemy_id]

        # If the conditional drop isn't a guaranteed drop override, ignore everything else.
        if enemy_data.item_3_drop_chance < 100:
            return True

        if self.__is_conditional_ignorable_for_regular_drops(enemy_data.drop_condition):
            return True

        # TODO temporary.
        if enemy_id == EO1Enemies.FIREBIRD:
            #return self.single_enemy_battle_processor.can_defeat_with_condition(enemy_id, enemy_data.drop_condition, state, logic_data)
            return True

        raise Exception(f"enemy {enemy_id}")

    def can_fulfill_drop_condition(self, enemy_id: int, logic_data: AllLogicData, state: CollectionState) -> bool:
        enemy_data = ENEMY_BY_ID[enemy_id]

        def can_defeat_with_condition() -> bool:
            return self.single_enemy_battle_processor.can_defeat_with_condition(enemy_id, enemy_data.drop_condition, state, logic_data)

        if enemy_data.drop_condition == DropCondition.STAB:
            if not self.__any_usable_skill_deal_damage_type(logic_data.class_data.unlocked_classes, EO1Element.STAB):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.FIRE:
            if not self.__any_usable_skill_deal_damage_type(logic_data.class_data.unlocked_classes, EO1Element.FIRE):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.ICE:
            if not self.__any_usable_skill_deal_damage_type(logic_data.class_data.unlocked_classes, EO1Element.ICE):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.NOT_BASH:
            if not self.__any_usable_skill_deal_not_damage_type(logic_data.class_data.unlocked_classes, EO1Element.BASH):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.NOT_STAB:
            if not self.__any_usable_skill_deal_not_damage_type(logic_data.class_data.unlocked_classes, EO1Element.STAB):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.NOT_PHYSICAL:
            if not self.__any_usable_skill_deal_not_physical(logic_data.class_data.unlocked_classes):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.NOT_FIRE:
            if not self.__any_usable_skill_deal_not_damage_type(logic_data.class_data.unlocked_classes, EO1Element.FIRE):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.INSTANT_DEATH:
            if not self.__any_usable_skill_can_inflict_ailment(logic_data.class_data.unlocked_classes, EO1Ailment.INSTANT_DEATH):
                return False
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.FULL_BIND:
            if not self.__any_usable_skill_can_inflict_ailment(logic_data.class_data.unlocked_classes, EO1Ailment.HEAD_BIND):
                return False
            if not self.__any_usable_skill_can_inflict_ailment(logic_data.class_data.unlocked_classes, EO1Ailment.ARM_BIND):
                return False
            if not self.__any_usable_skill_can_inflict_ailment(logic_data.class_data.unlocked_classes, EO1Ailment.LEG_BIND):
                return False
            # Player can inflict all 3 binds individually. Leave the battle processor determine if it is realistic to do.
            return can_defeat_with_condition()
        # Kill within X turns is entirely up to the battle processor, nothing can be checked here.
        if (enemy_data.drop_condition == DropCondition.KILL_1_TURNS or
            enemy_data.drop_condition == DropCondition.KILL_2_TURNS or
            enemy_data.drop_condition == DropCondition.KILL_3_TURNS or
            enemy_data.drop_condition == DropCondition.KILL_7_TURNS):
            return can_defeat_with_condition()
        if enemy_data.drop_condition == DropCondition.NONE:
            return True
        raise Exception(f"Unknown drop condition {enemy_data.drop_condition}.")
