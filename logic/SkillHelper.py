from ..data.SkillData import *


_BATTLE_SKILL: dict[EO1SkillType, bool] = {
    EO1SkillType.PASSIVE: True, # Not always. Need to be split.
    EO1SkillType.MASTERY: True,
    EO1SkillType.PHYSICAL_ATTACK: True,
    EO1SkillType.MAGICAL_ATTACK: True,
    EO1SkillType.AILMENT_ATTACK: True,
    EO1SkillType.DEBUFF: True,
    EO1SkillType.BUFF: True,
    EO1SkillType.COUNTER: True,
    EO1SkillType.CHASE: True,
    EO1SkillType.DEFENSE: True,
    EO1SkillType.HEAL: True,
    EO1SkillType.AILMENT_HEAL: True,
    EO1SkillType.BUFF_REMOVAL: True,
    EO1SkillType.ESCAPE: True,
    EO1SkillType.SPECIAL_PHYSICAL_ATTACK: True,
    EO1SkillType.TURN_MANIPULATION: True,
    EO1SkillType.FIELD_HEAL: False,
    EO1SkillType.FIELD_PASSIVE: False,
    EO1SkillType.FIELD_UTILITY: False,
    EO1SkillType.CURSE: True,
    EO1SkillType.CHOP: False,
    EO1SkillType.MINE: False,
    EO1SkillType.TAKE: False,
}

_ACTIVE_BATTLE_SKILL: dict[EO1SkillType, bool] = {
    EO1SkillType.PASSIVE: False,
    EO1SkillType.MASTERY: False,
    EO1SkillType.PHYSICAL_ATTACK: True,
    EO1SkillType.MAGICAL_ATTACK: True,
    EO1SkillType.AILMENT_ATTACK: True,
    EO1SkillType.DEBUFF: True,
    EO1SkillType.BUFF: True,
    EO1SkillType.COUNTER: True,
    EO1SkillType.CHASE: True,
    EO1SkillType.DEFENSE: True,
    EO1SkillType.HEAL: True,
    EO1SkillType.AILMENT_HEAL: True,
    EO1SkillType.BUFF_REMOVAL: True,
    EO1SkillType.ESCAPE: True,
    EO1SkillType.SPECIAL_PHYSICAL_ATTACK: True,
    EO1SkillType.TURN_MANIPULATION: True,
    EO1SkillType.CURSE: True,
}

_ENEMY_TARGETING_SKILL: dict[EO1SkillType, bool] = {
    EO1SkillType.PHYSICAL_ATTACK: True,
    EO1SkillType.MAGICAL_ATTACK: True,
    EO1SkillType.AILMENT_ATTACK: True,
    EO1SkillType.DEBUFF: True,
    EO1SkillType.BUFF: False,
    EO1SkillType.COUNTER: True,
    EO1SkillType.CHASE: True,
    EO1SkillType.DEFENSE: False,
    EO1SkillType.HEAL: False,
    EO1SkillType.AILMENT_HEAL: False,
    EO1SkillType.BUFF_REMOVAL: True,
    EO1SkillType.ESCAPE: False,
    EO1SkillType.SPECIAL_PHYSICAL_ATTACK: True,
    EO1SkillType.TURN_MANIPULATION: False,
    EO1SkillType.CURSE: True,
}

def is_battle_skill(skill_data: EO1SkillData) -> bool:
    return _BATTLE_SKILL[skill_data.skill_type]

def is_battle_active_skill(skill_data: EO1SkillData) -> bool:
    return _ACTIVE_BATTLE_SKILL[skill_data.skill_type]

def is_enemy_targeting_skill(skill_data: EO1SkillData) -> bool:
    return _ENEMY_TARGETING_SKILL[skill_data.skill_type]

def can_inflict_ailment(skill_data: EO1SkillData, ailment: EO1Ailment) -> bool:
    if not is_battle_skill(skill_data):
        return False
    if not is_battle_active_skill(skill_data):
        return False
    if not is_enemy_targeting_skill(skill_data):
        return False

    return skill_data.ailment == ailment

def is_damage_type(skill_data: EO1SkillData, damage_type: EO1Element) -> bool:
    if not is_battle_skill(skill_data):
        return False
    if not is_battle_active_skill(skill_data):
        return False
    if not is_enemy_targeting_skill(skill_data):
        return False

    if skill_data.primary_element == damage_type:
        return True
    if skill_data.secondary_element == damage_type:
        return True
    return False

def is_not_damage_type(skill_data: EO1SkillData, damage_type: EO1Element) -> bool:
    return not is_damage_type(skill_data, damage_type)

def is_any_damage_type(skill_data: EO1SkillData, damage_types: list[EO1Element]) -> bool:
    if not is_battle_skill(skill_data):
        return False
    if not is_battle_active_skill(skill_data):
        return False
    if not is_enemy_targeting_skill(skill_data):
        return False

    for damage_type in damage_types:
        if skill_data.primary_element == damage_type:
            return True
        if skill_data.secondary_element == damage_type:
            return True
    return False

def is_not_physical_damage_type(skill_data: EO1SkillData) -> bool:
    if not is_battle_skill(skill_data):
        return False
    if not is_battle_active_skill(skill_data):
        return False
    if not is_enemy_targeting_skill(skill_data):
        return False

    if skill_data.primary_element in EO1ElementGroup.PHYSICAL:
        return False
    if skill_data.secondary_element in EO1ElementGroup.PHYSICAL:
        return False

    return True


