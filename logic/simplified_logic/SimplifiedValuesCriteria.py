from __future__ import annotations
from typing import TYPE_CHECKING, Callable, cast
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, ABCMeta

from BaseClasses import CollectionState
from .EnemyAttributes import EnemyAttributes
from ..LogicData import SingleClassLogicData, AllLogicData, SkillLogicData
from ...data.Generic import *

from ..SkillHelper import *
import itertools

from .SimplifiedClassValues import *
from .SimplifiedSkillValues import *

from .Constant import *


def get_effective_skill_viability_level(active_skill_values: ActiveSkillValues, enemy_attributes: EnemyAttributes) -> SkillViabilityLevel:
    if active_skill_values.viability_level == SkillViabilityLevel.TERRIBLE:
        return SkillViabilityLevel.TERRIBLE
    if active_skill_values.viability_level != SkillViabilityLevel.SITUATIONAL:
        return active_skill_values.viability_level

    # Handle Situational Skills.
    cause = active_skill_values.situational_cause
    if cause is None:
        return SkillViabilityLevel.SITUATIONAL

    skill_data = SKILL_DATA_BY_ID[active_skill_values.skill_id]

    # Chase skills not handled for now.
    if cause == SituationalSkillCause.CHASE:
        return SkillViabilityLevel.SITUATIONAL
    # In terms of combat, escape skills are terrible.
    if cause == SituationalSkillCause.ESCAPE:
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.ELEMENTAL_GUARD:
        # TODO
        return SkillViabilityLevel.SITUATIONAL
    if cause == SituationalSkillCause.ELEMENTAL_IMBUE:
        if skill_data.primary_element in enemy_attributes.damage_type_weakness:
            return SkillViabilityLevel.NORMAL
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.ELEMENTAL_DEFENSE:
        # TODO
        return SkillViabilityLevel.SITUATIONAL
    if cause == SituationalSkillCause.BIND_HEAL:
        if enemy_attributes.can_inflict_bind:
            return SkillViabilityLevel.NORMAL
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.STATUS_HEAL:
        if enemy_attributes.can_inflict_status_effect:
            return SkillViabilityLevel.NORMAL
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.AILMENT_RECOVERY:
        if enemy_attributes.can_inflict_status_effect or enemy_attributes.can_inflict_bind:
            return SkillViabilityLevel.NORMAL # Maybe Bad, honestly.
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.BUFF_REMOVAL:
        if enemy_attributes.can_apply_buff:
            return SkillViabilityLevel.NORMAL
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.BIND_ATTACK:
        if skill_data.ailment in enemy_attributes.skills_body_use:
            return SkillViabilityLevel.NORMAL
        return SkillViabilityLevel.TERRIBLE
    if cause == SituationalSkillCause.STATUS_ATTACK:
        #if skill_data.ailment in enemy_attributes.sta
        return SkillViabilityLevel.SITUATIONAL # TODO
    if cause == SituationalSkillCause.RELAPSE:
        return SkillViabilityLevel.SITUATIONAL # TODO
    if cause == SituationalSkillCause.ECSTASY:
        return SkillViabilityLevel.SITUATIONAL # TODO
    if cause == SituationalSkillCause.CLIMAX:
        return SkillViabilityLevel.SITUATIONAL # TODO

    raise Exception(f"Unknown Situational Cause: {cause}")

@dataclass(frozen=True)
class SVCriteria(ABC):
    @abstractmethod
    def copy(self) -> SVCriteria:
        pass

    @abstractmethod
    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        pass

@dataclass(frozen=True)
class GroupSVCriteria(SVCriteria, metaclass=ABCMeta):
    criteria: list[SVCriteria]

@dataclass(frozen=True)
class OrSVCriteria(GroupSVCriteria):
    def copy(self) -> SVCriteria:
        new_copy = OrSVCriteria([])

        for inner_criteria in self.criteria:
            new_copy.criteria.append(inner_criteria.copy())

        return new_copy

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        for inner_criteria in self.criteria:
            if inner_criteria.evaluate_criteria(enemy_attributes, class_logic_data, all_logic_data):
                return True
        return False

@dataclass(frozen=True)
class AndSVCriteria(GroupSVCriteria):
    def copy(self) -> SVCriteria:
        new_copy = AndSVCriteria([])

        for inner_criteria in self.criteria:
            new_copy.criteria.append(inner_criteria.copy())

        return new_copy

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        for inner_criteria in self.criteria:
            if not inner_criteria.evaluate_criteria(enemy_attributes, class_logic_data, all_logic_data):
                return False
        return True

@dataclass(frozen=True)
class TrueSVCriteria(SVCriteria):
    def copy(self) -> SVCriteria:
        return TrueSVCriteria()

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        return True

@dataclass(frozen=True)
class FalseSVCriteria(SVCriteria):
    def copy(self) -> SVCriteria:
        return FalseSVCriteria()

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        return False

@dataclass(frozen=True)
class ClassSVCriteria(SVCriteria):
    front_class_count: int | None = None
    back_class_count: int | None = None
    total_class_count: int | None = None
    criteria: SVCriteria = field(default_factory=TrueSVCriteria)

    def copy(self) -> SVCriteria:
        return ClassSVCriteria(self.front_class_count, self.back_class_count, self.total_class_count, self.criteria.copy())

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        front_row_count = 0
        back_row_count = 0
        total_count = 0

        for class_data in class_logic_data:
            if not class_data.class_unlocked:
                continue

            simplified_class_data = SIMPLIFIED_CLASS_VALUES_BY_NAME[class_data.class_name]

            if not self.criteria.evaluate_criteria(enemy_attributes, [class_data], all_logic_data):
                continue

            if simplified_class_data.is_front_row_viable:
                front_row_count += 1
            if simplified_class_data.is_back_row_viable:
                back_row_count += 1
            total_count += 1

        if self.front_class_count is not None:
            if front_row_count < self.front_class_count:
                return False

        if self.back_class_count is not None:
            if back_row_count < self.back_class_count:
                return False

        if self.total_class_count is not None:
            if total_count < self.total_class_count:
                return False

        return True


@dataclass
class PlayerParty:
    members: list[str]

    def is_valid_party(self, front_row_class: set[str], back_row_class: set[str]) -> bool:
        front_count = 0
        back_count = 0
        total_count = 0

        for member in self.members:
            if member in front_row_class:
                front_count += 1
            elif member in back_row_class:
                back_count += 1
            total_count += 1

        if front_count > 3:
            return False
        if back_count > 3:
            return False
        if total_count > 5:
            return False
        return True

    def clone(self) -> PlayerParty:
        return PlayerParty(self.members.copy())

    def members_as_set(self) -> set[str]:
        return set(self.members)


@dataclass(frozen=True)
class AdventurerMatch:
    match_count: int
    criteria: SVCriteria = field(default_factory=TrueSVCriteria)

    def copy(self) -> AdventurerMatch:
        return AdventurerMatch(self.match_count, self.criteria.copy())


@dataclass(frozen=True)
class PartySVCriteria(SVCriteria):
    valid_class_criteria: SVCriteria = field(default_factory=TrueSVCriteria)
    extra_criteria: list[AdventurerMatch] = field(default_factory=list)

    def copy(self) -> SVCriteria:
        new_copy = PartySVCriteria(self.valid_class_criteria.copy(), [])
        for extra_criteria in self.extra_criteria:
            new_copy.extra_criteria.append(extra_criteria.copy())
        return new_copy

    @staticmethod
    def build_possible_party(eligible_class: list[str], front_row_class: set[str], back_row_class: set[str], allow_repeats: bool):
        if allow_repeats:
            iter_generator = itertools.combinations_with_replacement(eligible_class, 5)
        else:
            iter_generator = itertools.combinations(eligible_class, 5)

        for party_members in iter_generator:
            party = PlayerParty([])
            for member in party_members:
                party.members.append(member)

            if party.is_valid_party(front_row_class, back_row_class):
                yield party

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        valid_front_line_class: set[str] = set()
        valid_back_line_class: set[str] = set()
        valid_class_by_name: dict[str, SingleClassLogicData] = {}

        for class_data in class_logic_data:
            if not class_data.class_unlocked:
                continue
            simplified_class_data = SIMPLIFIED_CLASS_VALUES_BY_NAME[class_data.class_name]

            # Only consider classes that match the general criteria.
            if not self.valid_class_criteria.evaluate_criteria(enemy_attributes, [class_data], all_logic_data):
                continue

            valid_class_by_name[class_data.class_name] = class_data
            if simplified_class_data.is_front_row_viable:
                valid_front_line_class.add(class_data.class_name)
            if simplified_class_data.is_back_row_viable:
                valid_back_line_class.add(class_data.class_name)

        if len(valid_front_line_class) < 2:
            return False
        if len(valid_back_line_class) < 2:
            return False
        if len(valid_class_by_name) < 5:
            return False

        # We have at least 2 front, 2 back and 5 total classes that match the general criteria.
        # Now we have to find out if a party composition match the other criteria.
        if len(self.extra_criteria) == 0:
            return True

        # Build the requirements list from the criteria list.
        party_requirements: list[tuple[set[str], int]] = []
        for sub_criteria in self.extra_criteria:
            matching_classes = {class_data.class_name for class_data in valid_class_by_name.values() if sub_criteria.criteria.evaluate_criteria(enemy_attributes, [class_data], all_logic_data)}
            if len(matching_classes) < sub_criteria.match_count:
                return False # This criteria cannot be matched.

            party_requirements.append((matching_classes, sub_criteria.match_count))

        def match_requirement(requirement: tuple[set[str], int], party: set[str]) -> bool:
            return len(party.intersection(requirement[0])) >= requirement[1]

        def match_all(possible_party: PlayerParty) -> bool:
            members = possible_party.members_as_set()
            for party_requirement in party_requirements:
                if not match_requirement(party_requirement, members):
                    return False
            return True

        for current_party in self.build_possible_party(list(valid_class_by_name.keys()), valid_front_line_class, valid_back_line_class, allow_repeats=False):
            if match_all(current_party):
                return True

        return False

@dataclass(frozen=True)
class HasAntiStatusSVCriteria(SVCriteria):
    def copy(self) -> SVCriteria:
        return HasAntiStatusSVCriteria()

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        # First, check for a status heal skill.
        for class_data in class_logic_data:
            for skill_logic_data in class_data.usable_skills:
                skill_data = SIMPLIFIED_SKILL_BY_SKILL_ID[skill_logic_data.skill_id]
                if skill_data.get_skill_type() == SkillType.STATUS_HEAL:
                    return True

        # If we didn't find a status heal skill, check for any unlocked class if they can use the required skills to make Theriaca B.
        take_skill_usable = False
        chop_skill_usable = False

        for class_data in all_logic_data.class_data.class_as_list:
            if not class_data.class_unlocked:
                continue
            for skill_logic_data in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill_logic_data.skill_id]
                if skill_data.skill_type == EO1SkillType.CHOP:
                    chop_skill_usable = True
                if skill_data.skill_type == EO1SkillType.TAKE:
                    take_skill_usable = True

        # Theriaca B requires Chop and Take (or Waspior, but let's ignore this one for now).
        if take_skill_usable and chop_skill_usable:
            return True
        return False


@dataclass(frozen=True)
class HasAntiBindSVCriteria(SVCriteria):
    def copy(self) -> SVCriteria:
        return HasAntiBindSVCriteria()

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        return True # Theriaca A is always obtainable, since the only material required are Bug Wing.

@dataclass(frozen=True)
class CanInflictAilment(SVCriteria):
    ailment: EO1Ailment

    def copy(self) -> SVCriteria:
        return CanInflictAilment(self.ailment)

    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        for class_data in class_logic_data:
            for skill_logic_data in class_data.usable_skills:
                skill_data = SKILL_DATA_BY_ID[skill_logic_data.skill_id]
                if not is_battle_skill(skill_data):
                    continue
                if not is_battle_active_skill(skill_data):
                    continue
                if not is_enemy_targeting_skill(skill_data):
                    continue
                if skill_data.ailment == EO1Ailment.NONE:
                    continue
                if skill_data.ailment == self.ailment:
                    return True
        return False

class IndividualClassCriteriaBase(SVCriteria):
    def evaluate_criteria(self, enemy_attributes: EnemyAttributes, class_logic_data: list[SingleClassLogicData], all_logic_data: AllLogicData) -> bool:
        for class_data in class_logic_data:
            if self.evaluate_single_class(enemy_attributes, class_data, all_logic_data):
                return True
        return False

    @abstractmethod
    def evaluate_single_class(self, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        pass

@dataclass(frozen=True)
class SkillCountCriteriaBase(IndividualClassCriteriaBase):
    skill_count: int = 1

    @staticmethod
    def get_skill_data(skill: SkillLogicData) -> EO1SkillData:
        return SKILL_DATA_BY_ID[skill.skill_id]

    @staticmethod
    def get_simplified_values(skill: SkillLogicData) -> SimplifiedSkillValues:
        return SIMPLIFIED_SKILL_BY_SKILL_ID[skill.skill_id]

    def evaluate_single_class(self, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not class_data.class_unlocked:
            return False

        simplified_class_data = SIMPLIFIED_CLASS_VALUES_BY_NAME[class_data.class_name]
        matching_skills: set[int] = set()
        for skill_logic_data in class_data.usable_skills:
            if self.evaluate_single_skill(skill_logic_data, enemy_attributes, class_data, all_logic_data):
                if skill_logic_data.skill_id in simplified_class_data.non_cumulative_logic_skills:
                    if len(matching_skills.intersection(simplified_class_data.non_cumulative_logic_skills)) > 0:
                        continue
                matching_skills.add(skill_logic_data.skill_id)

        return len(matching_skills) >= self.skill_count

    @abstractmethod
    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        pass

@dataclass(frozen=True)
class CanUseActiveSkill(SkillCountCriteriaBase):
    damage_type_resistances: list[EO1Element] = field(default_factory=list)
    ailment_resistances: list[EO1Ailment] = field(default_factory=list)
    skill_viability_level: SkillViabilityLevel | None = None
    ignore_immunities: bool = False

    def copy(self) -> SVCriteria:
        return CanUseActiveSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities)

    @staticmethod
    def get_as_active_skill_values(skill_values: SimplifiedSkillValues) -> ActiveSkillValues:
        return cast(ActiveSkillValues, skill_values)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not skill.skill_usable:
            return False

        simplified_values = self.get_simplified_values(skill)
        if simplified_values.get_skill_use_type() != SkillUseType.ACTIVE:
            return False

        active_skill_values = self.get_as_active_skill_values(simplified_values)
        if self.skill_viability_level is not None:
            effective_skill_viability_level = get_effective_skill_viability_level(active_skill_values, enemy_attributes)
            if effective_skill_viability_level.value < self.skill_viability_level.value:
                return False

        skill_data = self.get_skill_data(skill)

        if active_skill_values.is_damage_skill():
            if not self.ignore_immunities:
                for element in enemy_attributes.damage_type_immunity:
                    if skill_data.primary_element == element:
                        return False
                    elif skill_data.secondary_element is not None:
                        if skill_data.secondary_element == element:
                            return False

            # TODO review
            for element in self.damage_type_resistances:
                if skill_data.primary_element == element:
                    return False
                elif skill_data.secondary_element is not None:
                    if skill_data.secondary_element == element:
                        return False

        for ailment in self.ailment_resistances:
            raise Exception("Ailment not supported")

        return True

@dataclass(frozen=True)
class CanUseDamageSkill(CanUseActiveSkill):
    skill_power: SkillPower | None = None
    damage_type: EO1Element | None = None

    def copy(self) -> SVCriteria:
        return CanUseDamageSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities,
            self.skill_power,
            self.damage_type)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanUseDamageSkill, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        simplified_values = self.get_simplified_values(skill)
        active_skill_values = self.get_as_active_skill_values(simplified_values)
        skill_data = self.get_skill_data(skill)

        # If not a damage skill, ignore it (return false).
        if not active_skill_values.is_damage_skill():
            return False
        damage_skill_values = cast(DamageSkillValues, simplified_values)
        if damage_skill_values is None:
            raise Exception(f"Skill {skill.skill_id} is a damage skill with no defined power.")
        # If skill power filter, apply it.
        if self.skill_power is not None:
            if damage_skill_values.skill_power.value < self.skill_power.value:
                return False
        # If damage type filter, apply it.
        if self.damage_type is not None:
            if skill_data.primary_element != self.damage_type:
                if skill_data.secondary_element is None:
                    return False
                elif skill_data.secondary_element != self.damage_type:
                    return False

        # Passed all filters.
        return True

@dataclass(frozen=True)
class CanUseAOEDamageMitigationSkill(CanUseActiveSkill):
    damage_type: EO1Element | None = None


    def copy(self) -> SVCriteria:
        return CanUseAOEDamageMitigationSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities,
            self.damage_type)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanUseAOEDamageMitigationSkill, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        if self.damage_type is None:
            raise Exception("Missing damage type in CanUseAOEDamageMitigationSkill criteria.")

        simplified_values = self.get_simplified_values(skill)
        skill_data = self.get_skill_data(skill)

        if simplified_values.get_skill_type() == SkillType.GUARD:
            guard_skill = cast(GuardSkillValues, simplified_values)
            if guard_skill.target_type == SkillTargetType.SINGLE:
                return False
            # TODO what to do with BACK and FRONT only?
            if guard_skill.target_type != SkillTargetType.ALL:
                return False

            # Can mitigate the necessary damage type?
            if self.damage_type in guard_skill.damage_types:
                return True
            return False
        elif simplified_values.get_skill_type() == SkillType.BUFF:
            buff_skill = cast(BuffSkillValues, simplified_values)
            # Single Target buff aren't enough.
            if buff_skill.target_type == SkillTargetType.SINGLE:
                return False

            # TODO what to do with BACK and FRONT only? Note: there is none in EO1.
            if buff_skill.target_type != SkillTargetType.ALL:
                return False

            # TODO technically this isn't fully accurate. If the skill boost DEF, its true, but some are direct physical damage mitigation only.
            if buff_skill.effect_type == SkillEffectType.DEFENSE:
                return True

            if buff_skill.effect_type == SkillEffectType.ELEMENTAL_DEFENSE:
                # TODO for other EO games this won't work since it can be multiple elements.
                element = skill_data.primary_element
                if element is None:
                    raise Exception(f"Skill {skill.skill_id} should define an element.")
                if element == self.damage_type:
                    return True
                return False

            # Max HP doesn't mitigate damage, so let's ignore it for simplified logic.
            # Don't consider Evasion boost, too unreliable.
            return False
        elif simplified_values.get_skill_type() == SkillType.DEBUFF:
            debuff_skill = cast(DebuffSkillValues, simplified_values)
            # Single Target buff aren't enough.
            if debuff_skill.target_type == SkillTargetType.SINGLE:
                return False

            # TODO what to do with BACK and FRONT only? Note: there is none in EO1.
            if debuff_skill.target_type != SkillTargetType.ALL:
                return False

            if debuff_skill.effect_type == SkillEffectType.ATTACK:
                return self.damage_type in EO1ElementGroup.PHYSICAL

            return False

        # Not any of the damage mitigation skill types.
        return False

@dataclass(frozen=True)
class CanUseAOEDamageNegationSkill(CanUseActiveSkill):
    damage_type: EO1Element | None = None

    def copy(self) -> SVCriteria:
        return CanUseAOEDamageNegationSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities,
            self.damage_type)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanUseAOEDamageNegationSkill, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        if self.damage_type is None:
            raise Exception("Missing damage type in CanUseAOEDamageNegationSkill criteria.")

        simplified_values = self.get_simplified_values(skill)
        skill_data = self.get_skill_data(skill)

        if simplified_values.get_skill_type() == SkillType.GUARD:
            guard_skill = cast(GuardSkillValues, simplified_values)
            if guard_skill.target_type == SkillTargetType.SINGLE:
                return False
            if guard_skill.target_type != SkillTargetType.ALL:
                return False

            # Can mitigate the necessary damage type?
            if self.damage_type in guard_skill.damage_types:
                return True

            if self.damage_type in EO1ElementGroup.PHYSICAL:
                return False

            if self.damage_type == EO1Element.FIRE:
                return skill.skill_id == EO1Skills.PROTECTOR_ANTIFIRE
            if self.damage_type == EO1Element.ICE:
                return skill.skill_id == EO1Skills.PROTECTOR_ANTICOLD
            if self.damage_type == EO1Element.THUNDER:
                return skill.skill_id == EO1Skills.PROTECTOR_ANTIVOLT

            return False

        # Not any of the damage mitigation skill types.
        return False

@dataclass(frozen=True)
class CanRemoveIceblock(CanUseActiveSkill):
    def copy(self) -> SVCriteria:
        return CanRemoveIceblock(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanRemoveIceblock, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        if skill.skill_id == EO1Skills.TROUBADOUR_ERASURE:
            return True
        if skill.skill_id == EO1Skills.HEXER_FRAILTY:
            return True

        return False

@dataclass(frozen=True)
class CanUseSpecificActiveSkill(CanUseActiveSkill):
    skill_id: list[int] = field(default_factory=list)

    def copy(self) -> SVCriteria:
        return CanUseSpecificActiveSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level,
            self.ignore_immunities,
            self.skill_id.copy())

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanUseSpecificActiveSkill, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        return skill.skill_id in self.skill_id

class CanUseAOEHealSkill(CanUseActiveSkill):
    def copy(self) -> SVCriteria:
        return CanUseAOEHealSkill(
            self.skill_count,
            self.damage_type_resistances.copy(),
            self.ailment_resistances.copy(),
            self.skill_viability_level)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes, class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not super(CanUseAOEHealSkill, self).evaluate_single_skill(skill, enemy_attributes, class_data, all_logic_data):
            return False

        simplified_values = self.get_simplified_values(skill)
        if simplified_values.get_skill_type() == SkillType.HEAL:
            heal_skill = cast(HealSkillValues, simplified_values)
            # TODO handle line specific heals (not in EO1).
            if heal_skill.target_type == SkillTargetType.ALL:
                return True
            return False
        elif simplified_values.get_skill_type() == SkillType.BUFF:
            buff_skill = cast(BuffSkillValues, simplified_values)
            # TODO handle line specific buff (not in EO1).
            if buff_skill.target_type != SkillTargetType.ALL:
                return True

            if buff_skill.effect_type == SkillEffectType.HP_RECOVERY:
                return True
            return False
        return False

class HasDefensivePassive(SkillCountCriteriaBase):
    def copy(self) -> SVCriteria:
        return HasDefensivePassive(self.skill_count)

    @staticmethod
    def get_as_passive_stat_skill_values(skill_values: SimplifiedSkillValues) -> PassiveStatSkillValues:
        return cast(PassiveStatSkillValues, skill_values)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes,
                              class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not skill.skill_usable:
            return False

        simplified_values = self.get_simplified_values(skill)
        if simplified_values.get_skill_type() != SkillType.PASSIVE_STAT:
            return False

        passive_skill_values = self.get_as_passive_stat_skill_values(simplified_values)

        if passive_skill_values.parameter == SkillPassiveParamType.HP:
            return True
        elif passive_skill_values.parameter == SkillPassiveParamType.DEF:
            return True
        return False

class HasOffensivePassive(SkillCountCriteriaBase):
    def copy(self) -> SVCriteria:
        return HasOffensivePassive(self.skill_count)

    @staticmethod
    def get_as_passive_stat_skill_values(skill_values: SimplifiedSkillValues) -> PassiveStatSkillValues:
        return cast(PassiveStatSkillValues, skill_values)

    def evaluate_single_skill(self, skill: SkillLogicData, enemy_attributes: EnemyAttributes,
                              class_data: SingleClassLogicData, all_logic_data: AllLogicData) -> bool:
        if not skill.skill_usable:
            return False

        simplified_values = self.get_simplified_values(skill)
        if simplified_values.get_skill_type() != SkillType.PASSIVE_STAT:
            if simplified_values.get_skill_type() != SkillType.MASTERY:
                return False

            mastery_skill_values = cast(MasterySkillValues, simplified_values)

            if mastery_skill_values.effect_type == MasteryEffectType.WEAPON:
                return True
            return False

        passive_skill_values = self.get_as_passive_stat_skill_values(simplified_values)

        if passive_skill_values.parameter == SkillPassiveParamType.ATK:
            return True
        elif passive_skill_values.parameter == SkillPassiveParamType.DEF:
            return True
        return False