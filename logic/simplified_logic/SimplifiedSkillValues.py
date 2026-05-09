from __future__ import annotations
from enum import StrEnum, IntEnum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from ...data.Generic import *
from ...data.SkillData import *
from .Constant import *

class SkillType(IntEnum):
    NON_BATTLE = 0
    ATTACK = 1
    NORMAL_ATTACK_PASSIVE = 4
    #MAGICAL_ATTACK = 2
    CHASE = 8
    COUNTER = 18
    AILMENT_ATTACK = 16
    PASSIVE_STAT = 2
    BATTLE_START_PASSIVE = 12
    PASSIVE_BOOST = 15
    MASTERY = 3
    GUARD = 17
    AGGRO = 10
    BUFF = 5
    DEBUFF = 9
    HEAL = 6
    BIND_HEAL = 13
    STATUS_HEAL = 14
    REVIVE = 19
    ESCAPE = 7
    TURN_MANIPULATION = 11
    BUFF_REMOVAL = 20
    CURSE = 21

class SituationalSkillCause(IntEnum):
    CHASE = 1
    ESCAPE = 2
    ELEMENTAL_GUARD = 3
    ELEMENTAL_IMBUE = 4
    ELEMENTAL_DEFENSE = 5
    BIND_HEAL = 6
    STATUS_HEAL = 7
    AILMENT_RECOVERY = 8
    BUFF_REMOVAL = 9
    BIND_ATTACK = 10
    STATUS_ATTACK = 11
    RELAPSE = 12
    ECSTASY = 13
    CLIMAX = 14

class SkillUseType(IntEnum):
    NON_BATTLE = 0
    PASSIVE = 1
    ACTIVE = 2

@dataclass
class SimplifiedSkillValues(ABC):
    skill_id: int

    #def __init__(self, skill_id: int, viability_level: SkillViabilityLevel):
    #    self.skill_id = skill_id

    @abstractmethod
    def get_skill_use_type(self) -> SkillUseType:
        pass

    @abstractmethod
    def get_skill_type(self) -> SkillType:
        pass

@dataclass
class NonBattleSkillValues(SimplifiedSkillValues):
    def get_skill_use_type(self) -> SkillUseType:
        return SkillUseType.NON_BATTLE
    def get_skill_type(self) -> SkillType:
        return SkillType.NON_BATTLE

@dataclass
class PassiveSkillValues(SimplifiedSkillValues):
    def get_skill_use_type(self) -> SkillUseType:
        return SkillUseType.PASSIVE
    @abstractmethod
    def get_skill_type(self) -> SkillType:
        pass

@dataclass
class ActiveSkillValues(SimplifiedSkillValues):
    viability_level: SkillViabilityLevel
    situational_cause: SituationalSkillCause | None = None

    def get_skill_use_type(self) -> SkillUseType:
        return SkillUseType.ACTIVE
    @abstractmethod
    def get_skill_type(self) -> SkillType:
        pass
    @abstractmethod
    def is_damage_skill(self) -> bool:
        pass

@dataclass
class DamageSkillValues(ActiveSkillValues):
    skill_power: SkillPower | None = None
    @abstractmethod
    def get_skill_type(self) -> SkillType:
        pass
    def is_damage_skill(self) -> bool:
        return True

@dataclass
class PassiveStatSkillValues(PassiveSkillValues):
    parameter: SkillPassiveParamType

    def get_skill_type(self) -> SkillType:
        return SkillType.PASSIVE_STAT

@dataclass
class AttackSkillValues(DamageSkillValues):
    skill_power: SkillPower | None = None
    #primary_element: EO1Element
    #secondary_element: EO1Element
    #is_magical: bool
    def get_skill_type(self) -> SkillType:
        return SkillType.ATTACK

@dataclass
class MasterySkillValues(PassiveSkillValues):
    effect_type: MasteryEffectType

    def get_skill_type(self) -> SkillType:
        return SkillType.MASTERY

class NormalAttackPassiveSkillValues(PassiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.NORMAL_ATTACK_PASSIVE

@dataclass
class SkillEffectBase(ActiveSkillValues):
    effect_type: SkillEffectType | None = None
    target_type: SkillTargetType | None = None

    @abstractmethod
    def get_skill_type(self) -> SkillType:
        pass
    def is_damage_skill(self) -> bool:
        return False

class BuffSkillValues(SkillEffectBase):
    def get_skill_type(self) -> SkillType:
        return SkillType.BUFF
    def is_damage_skill(self) -> bool:
        return False

class DebuffSkillValues(SkillEffectBase):
    def get_skill_type(self) -> SkillType:
        return SkillType.DEBUFF
    def is_damage_skill(self) -> bool:
        return False

@dataclass
class HealSkillValues(ActiveSkillValues):
    target_type: SkillTargetType | None = None

    def get_skill_type(self) -> SkillType:
        return SkillType.HEAL
    def is_damage_skill(self) -> bool:
        return False

class EscapeSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.ESCAPE
    def is_damage_skill(self) -> bool:
        return False

class ChaseSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.CHASE
    def is_damage_skill(self) -> bool:
        return False # TODO this is false, but Chase skills are unsupported at the moment.

class AggroSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.AGGRO
    def is_damage_skill(self) -> bool:
        return False

class TurnManipulationSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.TURN_MANIPULATION
    def is_damage_skill(self) -> bool:
        return False

class TurnManipulationPassiveSkillValues(PassiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.TURN_MANIPULATION

class BattleStartPassiveSkillValues(PassiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.BATTLE_START_PASSIVE

class BindHealValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.BIND_HEAL
    def is_damage_skill(self) -> bool:
        return False

class StatusHealValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.STATUS_HEAL
    def is_damage_skill(self) -> bool:
        return False

class PassiveBoostValues(PassiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.PASSIVE_BOOST

class AilmentAttackValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.AILMENT_ATTACK
    def is_damage_skill(self) -> bool:
        return False#??

@dataclass
class GuardSkillValues(ActiveSkillValues):
    target_type: SkillTargetType | None = None
    damage_types: list[EO1Element] = field(default_factory=list)

    def get_skill_type(self) -> SkillType:
        return SkillType.GUARD
    def is_damage_skill(self) -> bool:
        return False

class CounterSkillValues(DamageSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.COUNTER

class ReviveSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.REVIVE
    def is_damage_skill(self) -> bool:
        return False

class BuffRemovalSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.BUFF_REMOVAL
    def is_damage_skill(self) -> bool:
        return False

class CurseSkillValues(ActiveSkillValues):
    def get_skill_type(self) -> SkillType:
        return SkillType.CURSE
    def is_damage_skill(self) -> bool:
        return False# TODO ??


SIMPLIFIED_SKILL_VALUES: list[SimplifiedSkillValues] = [
    # Landsknecht
    PassiveStatSkillValues(EO1Skills.LANDSKNECHT_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.LANDSKNECHT_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.LANDSKNECHT_ATK_UP, SkillPassiveParamType.ATK),
    PassiveStatSkillValues(EO1Skills.LANDSKNECHT_DEF_UP, SkillPassiveParamType.DEF),
    MasterySkillValues(EO1Skills.LANDSKNECHT_AXES, MasteryEffectType.WEAPON),
    MasterySkillValues(EO1Skills.LANDSKNECHT_SWORDS, MasteryEffectType.WEAPON),
    NormalAttackPassiveSkillValues(EO1Skills.LANDSKNECHT_2_HIT),
    NonBattleSkillValues(EO1Skills.LANDSKNECHT_MINE),
    BuffSkillValues(EO1Skills.LANDSKNECHT_WAR_CRY, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.ATTACK, target_type=SkillTargetType.SELF),
    BuffSkillValues(EO1Skills.LANDSKNECHT_HELL_CRY, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.ATTACK, target_type=SkillTargetType.SELF),
    BindHealValues(EO1Skills.LANDSKNECHT_ARM_HEAL, SkillViabilityLevel.BAD),
    AttackSkillValues(EO1Skills.LANDSKNECHT_CRUSH, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.LANDSKNECHT_STUNNER, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.LANDSKNECHT_SILENCER, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.LANDSKNECHT_CLEAVER, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.LANDSKNECHT_TORNADO, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.LANDSKNECHT_ALLSLASH, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM),
    ChaseSkillValues(EO1Skills.LANDSKNECHT_BLAZER, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.CHASE),
    ChaseSkillValues(EO1Skills.LANDSKNECHT_SHOCKER, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.CHASE),
    ChaseSkillValues(EO1Skills.LANDSKNECHT_FREEZER, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.CHASE),
    EscapeSkillValues(EO1Skills.LANDSKNECHT_FLEE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ESCAPE),

    # Survivalist
    PassiveStatSkillValues(EO1Skills.SURVIVALIST_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.SURVIVALIST_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.SURVIVALIST_AGI_UP, SkillPassiveParamType.AGI),
    MasterySkillValues(EO1Skills.SURVIVALIST_BOWS, MasteryEffectType.WEAPON),
    TurnManipulationPassiveSkillValues(EO1Skills.SURVIVALIST_1ST_HIT),
    BattleStartPassiveSkillValues(EO1Skills.SURVIVALIST_AMBUSH),
    NonBattleSkillValues(EO1Skills.SURVIVALIST_CHOP),
    NonBattleSkillValues(EO1Skills.SURVIVALIST_MINE),
    NonBattleSkillValues(EO1Skills.SURVIVALIST_TAKE),
    TurnManipulationSkillValues(EO1Skills.SURVIVALIST_1ST_TURN, SkillViabilityLevel.GOOD),
    DebuffSkillValues(EO1Skills.SURVIVALIST_TRICKERY, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.ACCURACY, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.SURVIVALIST_QUICKEN, SkillViabilityLevel.BAD, effect_type=SkillEffectType.SPEED, target_type=SkillTargetType.ALL),
    AttackSkillValues(EO1Skills.SURVIVALIST_TRUESHOT, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.SURVIVALIST_MULTIHIT, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM), # Because of random targeting
    AttackSkillValues(EO1Skills.SURVIVALIST_DISABLE, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.SURVIVALIST_APOLLON, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AggroSkillValues(EO1Skills.SURVIVALIST_CLOAK, SkillViabilityLevel.TERRIBLE),
    # Isn't this a passive?
    EscapeSkillValues(EO1Skills.SURVIVALIST_ESCAPE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ESCAPE),
    BattleStartPassiveSkillValues(EO1Skills.SURVIVALIST_AWARE),
    NonBattleSkillValues(EO1Skills.SURVIVALIST_STALKER),
    NonBattleSkillValues(EO1Skills.SURVIVALIST_OWL_EYE),

    # Protector
    PassiveStatSkillValues(EO1Skills.PROTECTOR_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.PROTECTOR_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.PROTECTOR_DEF_UP, SkillPassiveParamType.DEF),
    MasterySkillValues(EO1Skills.PROTECTOR_SHIELDS, MasteryEffectType.OTHER),
    PassiveBoostValues(EO1Skills.PROTECTOR_AEGIS),
    PassiveBoostValues(EO1Skills.PROTECTOR_EN_GARDE),
    NonBattleSkillValues(EO1Skills.PROTECTOR_MINE),
    AggroSkillValues(EO1Skills.PROTECTOR_PROVOKE, SkillViabilityLevel.TERRIBLE),
    GuardSkillValues(EO1Skills.PROTECTOR_F_GUARD, SkillViabilityLevel.GOOD, target_type=SkillTargetType.FRONT_ALL, damage_types=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH]),
    GuardSkillValues(EO1Skills.PROTECTOR_B_GUARD, SkillViabilityLevel.BAD, target_type=SkillTargetType.BACK_ALL, damage_types=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH]),
    GuardSkillValues(EO1Skills.PROTECTOR_PARRY, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SELF, damage_types=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH]),
    BuffSkillValues(EO1Skills.PROTECTOR_FORTIFY, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.SELF),
    BuffSkillValues(EO1Skills.PROTECTOR_DEFENDER, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.ALL),
    AttackSkillValues(EO1Skills.PROTECTOR_SMITE, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    GuardSkillValues(EO1Skills.PROTECTOR_ANTIFIRE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_GUARD, target_type=SkillTargetType.ALL, damage_types=[EO1Element.FIRE]),
    GuardSkillValues(EO1Skills.PROTECTOR_ANTIVOLT, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_GUARD, target_type=SkillTargetType.ALL, damage_types=[EO1Element.THUNDER]),
    GuardSkillValues(EO1Skills.PROTECTOR_ANTICOLD, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_GUARD, target_type=SkillTargetType.ALL, damage_types=[EO1Element.ICE]),
    HealSkillValues(EO1Skills.PROTECTOR_CURE, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SINGLE),
    HealSkillValues(EO1Skills.PROTECTOR_CURE_II, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SINGLE),
    EscapeSkillValues(EO1Skills.PROTECTOR_FLEE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ESCAPE),
    NonBattleSkillValues(EO1Skills.PROTECTOR_STALKER),

    # Dark Hunter
    PassiveStatSkillValues(EO1Skills.DARK_HUNTER_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.DARK_HUNTER_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.DARK_HUNTER_ATK_UP, SkillPassiveParamType.ATK),
    MasterySkillValues(EO1Skills.DARK_HUNTER_WHIPS, MasteryEffectType.WEAPON),
    MasterySkillValues(EO1Skills.DARK_HUNTER_SWORDS, MasteryEffectType.WEAPON),
    PassiveBoostValues(EO1Skills.DARK_HUNTER_BOOST_UP),#, SkillPassiveParamType.BOOST),
    PassiveBoostValues(EO1Skills.DARK_HUNTER_FURY),
    NonBattleSkillValues(EO1Skills.DARK_HUNTER_TAKE),
    AggroSkillValues(EO1Skills.DARK_HUNTER_CLOAK, SkillViabilityLevel.TERRIBLE),
    AttackSkillValues(EO1Skills.DARK_HUNTER_VIPER, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_GAG, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_CUFFS, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_SHACKLES, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_ECSTASY, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ECSTASY, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.DARK_HUNTER_CLIMAX, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.CLIMAX, skill_power=SkillPower.WEAK), # Skill Power set to Weak because unless it executes, it does only 100% damage.
    AttackSkillValues(EO1Skills.DARK_HUNTER_HYPNOS, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_NERVE, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_PETRIFY, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    CounterSkillValues(EO1Skills.DARK_HUNTER_BAIT, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.DARK_HUNTER_DRAIN, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.DARK_HUNTER_MIRAGE, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),

    # Medic
    PassiveStatSkillValues(EO1Skills.MEDIC_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.MEDIC_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.MEDIC_ATK_UP, SkillPassiveParamType.ATK),
    MasterySkillValues(EO1Skills.MEDIC_HEALER, MasteryEffectType.OTHER),
    NonBattleSkillValues(EO1Skills.MEDIC_PATCH_UP),
    NonBattleSkillValues(EO1Skills.MEDIC_SCAVENGE),
    PassiveBoostValues(EO1Skills.MEDIC_TP_REGEN),
    NonBattleSkillValues(EO1Skills.MEDIC_CHOP),
    HealSkillValues(EO1Skills.MEDIC_CURE, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SINGLE),
    HealSkillValues(EO1Skills.MEDIC_CURE_II, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SINGLE),
    HealSkillValues(EO1Skills.MEDIC_CURE_III, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SINGLE),
    HealSkillValues(EO1Skills.MEDIC_SALVE, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.ALL),
    HealSkillValues(EO1Skills.MEDIC_SALVE_II, SkillViabilityLevel.GOOD, target_type=SkillTargetType.ALL),
    ReviveSkillValues(EO1Skills.MEDIC_REVIVE, SkillViabilityLevel.GOOD),
    BindHealValues(EO1Skills.MEDIC_UNBIND, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.BIND_HEAL),
    StatusHealValues(EO1Skills.MEDIC_REFRESH, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.STATUS_HEAL),
    BuffSkillValues(EO1Skills.MEDIC_IMMUNIZE, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.ALL),
    AttackSkillValues(EO1Skills.MEDIC_CADUCEUS, SkillViabilityLevel.NORMAL, skill_power=SkillPower.STRONG),
    BuffSkillValues(EO1Skills.MEDIC_CPR, SkillViabilityLevel.BAD, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.MEDIC_REGEN, SkillViabilityLevel.BAD, effect_type=SkillEffectType.HP_RECOVERY, target_type=SkillTargetType.ALL),
    NonBattleSkillValues(EO1Skills.MEDIC_H_TOUCH),

    # Alchemist
    PassiveStatSkillValues(EO1Skills.ALCHEMIST_TP_UP, SkillPassiveParamType.TP),
    MasterySkillValues(EO1Skills.ALCHEMIST_FIRE_UP, MasteryEffectType.OTHER),
    MasterySkillValues(EO1Skills.ALCHEMIST_ICE_UP, MasteryEffectType.OTHER),
    MasterySkillValues(EO1Skills.ALCHEMIST_VOLT_UP, MasteryEffectType.OTHER),
    MasterySkillValues(EO1Skills.ALCHEMIST_TOXINS, MasteryEffectType.OTHER),
    NonBattleSkillValues(EO1Skills.ALCHEMIST_SCAVENGE),
    PassiveBoostValues(EO1Skills.ALCHEMIST_TP_REGEN),
    NonBattleSkillValues(EO1Skills.ALCHEMIST_CHOP),
    AttackSkillValues(EO1Skills.ALCHEMIST_FIRE, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.ALCHEMIST_FLAME, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.ALCHEMIST_INFERNO, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.ALCHEMIST_ICE, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.ALCHEMIST_FREEZE, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.ALCHEMIST_COCYTUS, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.ALCHEMIST_VOLT, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.ALCHEMIST_THUNDER, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.ALCHEMIST_THOR, SkillViabilityLevel.GOOD, skill_power=SkillPower.MEDIUM),
    AilmentAttackValues(EO1Skills.ALCHEMIST_POISON, SkillViabilityLevel.NORMAL),
    AilmentAttackValues(EO1Skills.ALCHEMIST_VENOM, SkillViabilityLevel.NORMAL),
    NonBattleSkillValues(EO1Skills.ALCHEMIST_SIGHT),
    NonBattleSkillValues(EO1Skills.ALCHEMIST_WARP),

    # Troubadour
    PassiveStatSkillValues(EO1Skills.TROUBADOUR_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.TROUBADOUR_TP_UP, SkillPassiveParamType.TP),
    MasterySkillValues(EO1Skills.TROUBADOUR_SONGS, MasteryEffectType.OTHER),
    NonBattleSkillValues(EO1Skills.TROUBADOUR_DIVINITY),
    BuffSkillValues(EO1Skills.TROUBADOUR_BRAVERY, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.ATTACK, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_SHELTER, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_MERCURY, SkillViabilityLevel.BAD, effect_type=SkillEffectType.SPEED, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_BLAZE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_IMBUE, effect_type=SkillEffectType.AFFINITY, target_type=SkillTargetType.SINGLE),
    BuffSkillValues(EO1Skills.TROUBADOUR_FROST, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_IMBUE, effect_type=SkillEffectType.AFFINITY, target_type=SkillTargetType.SINGLE),
    BuffSkillValues(EO1Skills.TROUBADOUR_SHOCK, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_IMBUE, effect_type=SkillEffectType.AFFINITY, target_type=SkillTargetType.SINGLE),
    BuffRemovalSkillValues(EO1Skills.TROUBADOUR_ERASURE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.BUFF_REMOVAL),
    BuffSkillValues(EO1Skills.TROUBADOUR_STAMINA, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.MAXHP, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_IFRIT, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_DEFENSE, effect_type=SkillEffectType.ELEMENTAL_DEFENSE, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_YMIR, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_DEFENSE, effect_type=SkillEffectType.ELEMENTAL_DEFENSE, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_TARANIS, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.ELEMENTAL_DEFENSE, effect_type=SkillEffectType.ELEMENTAL_DEFENSE, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_HEALING, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.HP_RECOVERY, target_type=SkillTargetType.ALL), # Bad?
    BuffSkillValues(EO1Skills.TROUBADOUR_RELAXING, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.SP_RECOVERY, target_type=SkillTargetType.ALL),
    BuffSkillValues(EO1Skills.TROUBADOUR_RECOVERY, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.AILMENT_RECOVERY, effect_type=SkillEffectType.AILMENT_RECOVERY, target_type=SkillTargetType.ALL),
    NonBattleSkillValues(EO1Skills.TROUBADOUR_STALKER),
    NonBattleSkillValues(EO1Skills.TROUBADOUR_RETURN),
    NonBattleSkillValues(EO1Skills.TROUBADOUR_TAKE),

    # Ronin
    PassiveStatSkillValues(EO1Skills.RONIN_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.RONIN_TP_UP, SkillPassiveParamType.TP),
    PassiveStatSkillValues(EO1Skills.RONIN_ATK_UP, SkillPassiveParamType.ATK),
    MasterySkillValues(EO1Skills.RONIN_KATANAS, MasteryEffectType.WEAPON),
    NormalAttackPassiveSkillValues(EO1Skills.RONIN_CRIT_UP),
    PassiveBoostValues(EO1Skills.RONIN_SIGHT),
    NonBattleSkillValues(EO1Skills.RONIN_MINE),
    HealSkillValues(EO1Skills.RONIN_IBUKI, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SELF),
    AttackSkillValues(EO1Skills.RONIN_KESAGIRI, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    BuffSkillValues(EO1Skills.RONIN_OVERHEAD, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.STANCE, target_type=SkillTargetType.SELF),
    AttackSkillValues(EO1Skills.RONIN_ZAMBA, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    AttackSkillValues(EO1Skills.RONIN_MIDAREBA, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.RONIN_OROCHI, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    BuffSkillValues(EO1Skills.RONIN_SEIGAN, SkillViabilityLevel.NORMAL, effect_type=SkillEffectType.STANCE, target_type=SkillTargetType.SELF),
    GuardSkillValues(EO1Skills.RONIN_MIKIRI, SkillViabilityLevel.NORMAL, target_type=SkillTargetType.SELF, damage_types=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH, EO1Element.FIRE, EO1Element.ICE, EO1Element.THUNDER]),
    AttackSkillValues(EO1Skills.RONIN_KOTEUCHI, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.RONIN_RAIZUKI, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),
    BuffSkillValues(EO1Skills.RONIN_IAI, SkillViabilityLevel.BAD, effect_type=SkillEffectType.STANCE, target_type=SkillTargetType.SELF),
    AttackSkillValues(EO1Skills.RONIN_KUBIUCHI, SkillViabilityLevel.NORMAL, skill_power=SkillPower.WEAK),
    AttackSkillValues(EO1Skills.RONIN_GATOTSU, SkillViabilityLevel.GOOD, skill_power=SkillPower.STRONG),
    AttackSkillValues(EO1Skills.RONIN_HYOSETSU, SkillViabilityLevel.NORMAL, skill_power=SkillPower.MEDIUM),

    # Hexer
    PassiveStatSkillValues(EO1Skills.HEXER_HP_UP, SkillPassiveParamType.HP),
    PassiveStatSkillValues(EO1Skills.HEXER_TP_UP, SkillPassiveParamType.TP),
    MasterySkillValues(EO1Skills.HEXER_CURSES, MasteryEffectType.OTHER),
    BattleStartPassiveSkillValues(EO1Skills.HEXER_STAGGER),
    NonBattleSkillValues(EO1Skills.HEXER_MINE),
    DebuffSkillValues(EO1Skills.HEXER_SAPPING, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.ATTACK, target_type=SkillTargetType.ALL),
    DebuffSkillValues(EO1Skills.HEXER_FRAILTY, SkillViabilityLevel.GOOD, effect_type=SkillEffectType.DEFENSE, target_type=SkillTargetType.ALL),
    DebuffSkillValues(EO1Skills.HEXER_LEADEN, SkillViabilityLevel.BAD, effect_type=SkillEffectType.SPEED, target_type=SkillTargetType.ALL),
    CurseSkillValues(EO1Skills.HEXER_RELAPSE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.RELAPSE),
    AilmentAttackValues(EO1Skills.HEXER_CRANIAL, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.BIND_ATTACK),
    AilmentAttackValues(EO1Skills.HEXER_ABDOMEN, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.BIND_ATTACK),
    AilmentAttackValues(EO1Skills.HEXER_IMMOBILE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.BIND_ATTACK),
    AilmentAttackValues(EO1Skills.HEXER_BLINDING, SkillViabilityLevel.NORMAL),
    AilmentAttackValues(EO1Skills.HEXER_TORPOR, SkillViabilityLevel.NORMAL),
    AilmentAttackValues(EO1Skills.HEXER_CORRUPT, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.STATUS_ATTACK),
    AilmentAttackValues(EO1Skills.HEXER_EVIL_EYE, SkillViabilityLevel.SITUATIONAL, situational_cause=SituationalSkillCause.STATUS_ATTACK),
    CurseSkillValues(EO1Skills.HEXER_SUICIDE, SkillViabilityLevel.NORMAL),
    CurseSkillValues(EO1Skills.HEXER_BETRAYAL, SkillViabilityLevel.NORMAL),
    CurseSkillValues(EO1Skills.HEXER_PARALYZE, SkillViabilityLevel.BAD),
    AttackSkillValues(EO1Skills.HEXER_REVENGE, SkillViabilityLevel.BAD, skill_power=SkillPower.WEAK), # Never enforce the use of low HP Hexer strategy.
    NonBattleSkillValues(EO1Skills.HEXER_LURE),
]

SIMPLIFIED_SKILL_BY_SKILL_ID: dict[int, SimplifiedSkillValues] = {skill_value.skill_id: skill_value for skill_value in SIMPLIFIED_SKILL_VALUES}


