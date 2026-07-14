from ..LogicData import *

from ...data.EnemyData import *
from ..SingleEnemyBattleProcessor import *
from .SimplifiedEnemyValues import *
from .SimplifiedValuesCriteria import SVCriteria, AdventurerMatch
from ...data.Generic import EO1Ailment


class SimplifiedSingleEnemyBattleProcessor(SingleEnemyBattleProcessor):
    def __survive_level_requirement_met(self, enemy_data: EnemyData, logic_data: AllLogicData) -> bool:
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        # TODO use effective level cap instead?
        return logic_data.current_level_cap >= max(1, effective_enemy_level)

    def __defeat_level_requirement_met(self, enemy_data: EnemyData, logic_data: AllLogicData) -> bool:
        # For now, just use the raw level.
        effective_enemy_level = enemy_data.level
        return logic_data.get_effective_level_cap() >= max(1, effective_enemy_level)

    def __copy_and_inject_criteria(self, original_criteria: SVCriteria, criteria_to_inject: SVCriteria) -> SVCriteria:
        if isinstance(original_criteria, PartySVCriteria):
            new_criteria = cast(PartySVCriteria, original_criteria.copy())
            new_criteria.extra_criteria.append(AdventurerMatch(1, criteria_to_inject))
            return new_criteria
        elif isinstance(original_criteria, TrueSVCriteria):
            return criteria_to_inject
        elif isinstance(original_criteria, ClassSVCriteria):
            return AndSVCriteria([original_criteria.copy(), criteria_to_inject])
        else:
            raise Exception()
        return original_criteria

    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__survive_level_requirement_met(enemy_data, context.logic_data):
            return False

        # TODO Temporary
        if enemy_id not in SIMPLIFIED_ENEMY_VALUES_BY_ID:
            return True

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        # If player has more than double the level, bypass other checks.
        if enemy_data.level * 2 < context.logic_data.get_effective_level_cap():
            return True

        if sv_enemy.survive_criteria is None:
            return True

        return sv_enemy.survive_criteria.evaluate_criteria(sv_enemy.attributes, context.logic_data.class_data.unlocked_classes, context.logic_data)

    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__defeat_level_requirement_met(enemy_data, context.logic_data):
            return False

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        # If player has more than double the level, bypass other checks.
        # Don't. This has an extremely negative impact on the logic.
        #if enemy_data.level * 2 < logic_data.current_level_cap:
        #    return True

        if sv_enemy.defeat_criteria is None:
            return True

        return sv_enemy.defeat_criteria.evaluate_criteria(sv_enemy.attributes, context.logic_data.class_data.unlocked_classes, context.logic_data)

    def can_defeat_with_condition(self, enemy_id: int, condition: DropCondition, context: ExecutionContext) -> bool:
        enemy_data = self.get_enemy_data(enemy_id)
        if not self.__defeat_level_requirement_met(enemy_data, context.logic_data):
            return False

        sv_enemy = SIMPLIFIED_ENEMY_VALUES_BY_ID[enemy_id]

        if sv_enemy.defeat_criteria is None:
            return True

        enemy_attributes = sv_enemy.attributes.copy()
        sv_criteria = sv_enemy.defeat_criteria

        if condition == DropCondition.STAB:
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanUseDamageSkill(damage_type=EO1Element.STAB, ignore_immunities=True))
        elif condition == DropCondition.FIRE:
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanUseDamageSkill(damage_type=EO1Element.FIRE, ignore_immunities=True))
        elif condition == DropCondition.ICE:
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanUseDamageSkill(damage_type=EO1Element.ICE, ignore_immunities=True))
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
            # Stalker
            if enemy_id == EO1Enemies.STALKER:
                if context.logic_data.get_effective_level_cap() < 50:
                    return False
            # Mantis
            elif enemy_id == EO1Enemies.MANTIS:
                if context.logic_data.get_effective_level_cap() < 45:
                    return False
            else:
                raise Exception(f"Unknown Enemy {enemy_id} for DropCondition Kill in 1 turn")
        elif condition == DropCondition.KILL_2_TURNS:
            # Ogre
            # Hunter
            # Similarly hard to kill enemies.
            if context.logic_data.get_effective_level_cap() < 65:
                return False
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanUseSpecificActiveSkill(skill_id=[EO1Skills.TROUBADOUR_BRAVERY, EO1Skills.HEXER_FRAILTY]))
        elif condition == DropCondition.KILL_3_TURNS:
            # Wyvern
            if context.logic_data.get_effective_level_cap() < 70:
                return False
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanUseSpecificActiveSkill(skill_id=[EO1Skills.TROUBADOUR_BRAVERY, EO1Skills.HEXER_FRAILTY]))
        elif condition == DropCondition.KILL_7_TURNS:
            # Manticor
            if context.logic_data.get_effective_level_cap() < 55:
                return False
        elif condition == DropCondition.FULL_BIND:
            # Cruella
            # Diabolix
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanInflictAilment(ailment=EO1Ailment.HEAD_BIND))
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanInflictAilment(ailment=EO1Ailment.ARM_BIND))
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanInflictAilment(ailment=EO1Ailment.LEG_BIND))
        elif condition == DropCondition.INSTANT_DEATH:
            sv_criteria = self.__copy_and_inject_criteria(sv_criteria, CanInflictAilment(EO1Ailment.INSTANT_DEATH))
        else:
            raise Exception(f"Unknown DropCondition {condition}")

        return sv_criteria.evaluate_criteria(enemy_attributes, context.logic_data.class_data.unlocked_classes, context.logic_data)
