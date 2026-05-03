from BaseClasses import CollectionState

from ..LogicData import *

from ...data.EnemyData import *
from ..SingleEnemyBattleProcessor import *
from .SimplifiedEnemyValues import *


class SimplifiedSingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def __survive_level_requirement_met(self, enemy_data: EnemyData, logic_data: AllLogicData) -> bool:
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        return logic_data.current_level_cap >= max(1, effective_enemy_level)

    def __defeat_level_requirement_met(self, enemy_data: EnemyData, logic_data: AllLogicData) -> bool:
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        return self.max_level_for_defeat(logic_data) >= max(1, effective_enemy_level)
    
    def can_survive_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__survive_level_requirement_met(enemy_data, logic_data):
            return False

        # TODO Temporary
        if enemy_id not in SIMPLIFIED_ENEMY_VALUES_BY_ID:
            return True

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        # If player has more than double the level, bypass other checks.
        if enemy_data.level * 2 < logic_data.current_level_cap:
            return True

        if sv_enemy.survive_criteria is None:
            return True

        return sv_enemy.survive_criteria.evaluate_criteria(sv_enemy.attributes, logic_data.class_data.unlocked_classes, logic_data)

    def can_defeat_enemy(self, enemy_id: int, state: CollectionState, logic_data: AllLogicData) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__defeat_level_requirement_met(enemy_data, logic_data):
            return False

        # TODO Temporary
        if enemy_id not in SIMPLIFIED_ENEMY_VALUES_BY_ID:
            return False

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        # If player has more than double the level, bypass other checks.
        # Don't. This has an extremely negative impact on the logic.
        #if enemy_data.level * 2 < logic_data.current_level_cap:
        #    return True

        if sv_enemy.defeat_criteria is None:
            return True

        return sv_enemy.defeat_criteria.evaluate_criteria(sv_enemy.attributes, logic_data.class_data.unlocked_classes, logic_data)

    def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, state: CollectionState, logic_data: AllLogicData) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__defeat_level_requirement_met(enemy_data, logic_data):
            return False
        # TODO Temporary
        if enemy_id not in SIMPLIFIED_ENEMY_VALUES_BY_ID:
            return False

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        if sv_enemy.defeat_criteria is None:
            return True

        enemy_attributes = sv_enemy.attributes.copy()
        sv_criteria = sv_enemy.defeat_criteria

        if condition == DropCondition.STAB:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.FIRE:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.ICE:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.NOT_BASH:
            # Handle this condition by treating it as a damage type immunity.
            enemy_attributes.damage_type_immunity.append(EO1Element.BASH)
        elif condition == DropCondition.NOT_STAB:
            # Handle this condition by treating it as a damage type immunity.
            enemy_attributes.damage_type_immunity.append(EO1Element.STAB)
        elif condition == DropCondition.NOT_PHYSICAL:
            # Handle this condition by treating it as a damage type immunity.
            enemy_attributes.damage_type_immunity.extend(EO1ElementGroup.PHYSICAL)
        elif condition == DropCondition.NOT_FIRE:
            # Handle this condition by treating it as a damage type immunity.
            enemy_attributes.damage_type_immunity.append(EO1Element.FIRE)
        elif condition == DropCondition.KILL_1_TURNS:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.KILL_2_TURNS:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.KILL_3_TURNS:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.KILL_7_TURNS:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.FULL_BIND:
            raise Exception(f"Not implemented DropCondition {condition}")
        elif condition == DropCondition.INSTANT_DEATH:
            raise Exception(f"Not implemented DropCondition {condition}")
        else:
            raise Exception(f"Unknown DropCondition {condition}")

        return sv_criteria.evaluate_criteria(enemy_attributes, logic_data.class_data.unlocked_classes, logic_data)
