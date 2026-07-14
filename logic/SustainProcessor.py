from __future__ import annotations

from .ILogicManager import ExecutionContext
from .LogicData import AllLogicData, ClassLogicData, SkillLogicData, SingleClassLogicData
from ..data.SustainData import *
from ..data.SkillData import *


from dataclasses import dataclass, field


@dataclass
class SustainValue:
    flat: int = 0
    percent: int = 0

    def get_effective_score_value(self, max_percent_value: int, percent_effectiveness: int, sustain_ratio: int) -> int:
        effective_percent = int(self.percent / 100 * max_percent_value)
        effective_percent = int(effective_percent / 100 * percent_effectiveness)
        if self.percent > 0:
            effective_percent = max(1, effective_percent)
        effective_value = max(self.flat, effective_percent)
        return int(effective_value / 100 * sustain_ratio)

    def set_value(self, value: int, value_type: SustainValueType) -> None:
        if value_type == SustainValueType.FLAT:
            if value > self.flat:
                self.flat = value
        elif value_type == SustainValueType.PERCENT:
            if value > self.percent:
                self.percent = value
        else:
            raise Exception(f"Unknown value type: {value_type}")

    def merge_values(self, sustain_value: SustainValue) -> None:
        self.set_value(sustain_value.flat, SustainValueType.FLAT)
        self.set_value(sustain_value.percent, SustainValueType.PERCENT)


@dataclass
class Sustain:
    single_hp: SustainValue = field(default_factory=SustainValue)
    single_tp: SustainValue = field(default_factory=SustainValue)
    multi_hp: SustainValue = field(default_factory=SustainValue)
    multi_tp: SustainValue = field(default_factory=SustainValue)
    revive: SustainValue = field(default_factory=SustainValue)

    def merge_values(self, sustain: Sustain) -> None:
        self.single_hp.merge_values(sustain.single_hp)
        self.single_tp.merge_values(sustain.single_tp)
        self.multi_hp.merge_values(sustain.multi_hp)
        self.multi_tp.merge_values(sustain.multi_tp)
        self.revive.merge_values(sustain.revive)


class SustainProcessor:
    def __get_sustain_items(self, context: ExecutionContext) -> Sustain:
        sustain_result = Sustain()
        for sustain_item in SUSTAIN_ITEMS:
            if not context.logic_manager.can_unlock_shop_item(sustain_item.related_id, context):
                continue

            if sustain_item.use_type != SustainUseType.ANYWHERE:
                raise Exception(f"Sustain items are expected to be of use type ANYWHERE. {sustain_item.related_id}")

            restore_hp: bool = False
            hp_value: int = 0
            restore_tp: bool = False
            tp_value: int = 0
            is_revive: bool = False
            revive_value: int = 0

            if sustain_item.sustain_type == SustainType.HP_RECOVERY:
                restore_hp = True
                hp_value = sustain_item.value
            elif sustain_item.sustain_type == SustainType.TP_RECOVERY:
                restore_tp = True
                tp_value = sustain_item.value
            elif sustain_item.sustain_type == SustainType.HP_TP_RECOVERY:
                restore_hp = True
                hp_value = sustain_item.value
                restore_tp = True
                tp_value = sustain_item.value_2
            elif sustain_item.sustain_type == SustainType.REVIVE:
                is_revive = True
                revive_value = sustain_item.value
            else:
                raise Exception(f"Unknown sustain type for item: {sustain_item.sustain_type}")

            if sustain_item.target == SustainTarget.SINGLE:
                if restore_hp:
                    sustain_result.single_hp.set_value(hp_value, sustain_item.value_type)
                if restore_tp:
                    sustain_result.single_tp.set_value(tp_value, sustain_item.value_type)
                if is_revive:
                    sustain_result.revive.set_value(revive_value, sustain_item.value_type)
            elif sustain_item.target == SustainTarget.ALL:
                if restore_hp:
                    sustain_result.multi_hp.set_value(hp_value, sustain_item.value_type)
                if restore_tp:
                    raise Exception(f"Item targeting ALL with TP restoring effect are unsupported")
                if is_revive:
                    raise Exception(f"Item targeting ALL with revive effect are unsupported")
            elif sustain_item.target == SustainTarget.SELF:
                raise Exception(f"Self Targeting sustain items are unsupported")
            else:
                raise Exception(f"Unknown sustain target: {sustain_item.target}")

        return sustain_result

    def __get_class_sustain_skills(self, logic_data: SingleClassLogicData, current_level_cap: int) -> Sustain:
        sustain_result = Sustain()

        for skill_data in logic_data.usable_skills:
            if skill_data.skill_id not in SUSTAIN_SKILL_BY_ID:
                continue
            sustain_skill = SUSTAIN_SKILL_BY_ID[skill_data.skill_id]

            effective_value: int = 0
            # Only consider lowest or highest level of skills.
            if skill_data.required_level + 10 > current_level_cap:
                effective_value = sustain_skill.value
            else:
                effective_value = sustain_skill.value_2

            if sustain_skill.sustain_type == SustainType.HP_TP_RECOVERY:
                raise Exception(f"Sustain skills restoring both HP and TP are unsupported")

            # For now, use the "Use_Type" as a multiplier of the value. It somewhat works for this game.
            if sustain_skill.use_type in {
                SustainUseType.BATTLE_ONLY,
                SustainUseType.FIELD_ONLY,
                SustainUseType.ANYWHERE
            }:
                effective_value = effective_value
            elif sustain_skill.use_type == SustainUseType.END_OF_BATTLE:
                effective_value = effective_value * 3
            elif sustain_skill.use_type == SustainUseType.BATTLE_ONLY_END_OF_TURN_BUFF:
                effective_value = effective_value * 3
            else:
                raise Exception(f"Unknown sustain use type: {sustain_skill.use_type}")

            sustain_target = sustain_skill.target

            # Self only isn't a true sustain skill, so reduce their effective value
            if sustain_target == SustainTarget.SELF:
                effective_value = int(effective_value / 2)
                effective_value = max(1, effective_value)
                sustain_target = SustainTarget.SINGLE

            if sustain_target == SustainTarget.SINGLE:
                if sustain_skill.sustain_type == SustainType.HP_RECOVERY:
                    sustain_result.single_hp.set_value(effective_value, sustain_skill.value_type)
                elif sustain_skill.sustain_type == SustainType.TP_RECOVERY:
                    sustain_result.single_tp.set_value(effective_value, sustain_skill.value_type)
                elif sustain_skill.sustain_type == SustainType.REVIVE:
                    sustain_result.revive.set_value(effective_value, sustain_skill.value_type)
                else:
                    raise Exception(f"Unknown sustain type: {sustain_skill.sustain_type}")
            elif sustain_target == SustainTarget.ALL:
                if sustain_skill.sustain_type == SustainType.HP_RECOVERY:
                    sustain_result.multi_hp.set_value(effective_value, sustain_skill.value_type)
                elif sustain_skill.sustain_type == SustainType.TP_RECOVERY:
                    sustain_result.multi_tp.set_value(effective_value, sustain_skill.value_type)
                elif sustain_skill.sustain_type == SustainType.REVIVE:
                    raise Exception(f"Skill targeting ALL with revive effect are unsupported")
                else:
                    raise Exception(f"Unknown sustain type: {sustain_skill.sustain_type}")
            else:
                raise Exception(f"Unknown sustain target: {sustain_target}")

        return sustain_result

    def __get_sustain_skills(self, logic_data: ClassLogicData, current_level_cap: int) -> Sustain:
        sustain_result = Sustain()

        for class_logic_data in logic_data.unlocked_classes:
            class_sustain_result = self.__get_class_sustain_skills(class_logic_data, current_level_cap)
            sustain_result.merge_values(class_sustain_result)

        return sustain_result

    def __get_percentage_effectiveness(self, current_level_cap) -> int:
        if current_level_cap >= 60:
            return 100
        if current_level_cap <= 10:
            return 10

        effectiveness = current_level_cap - 10
        return effectiveness * 1.8 + 10

    def get_current_sustain_score(self, context: ExecutionContext) -> int:
        current_level_cap = context.logic_data.get_effective_level_cap()
        item_sustains = self.__get_sustain_items(context)
        skill_sustains = self.__get_sustain_skills(context.logic_data.class_data, current_level_cap)

        percentage_effectiveness = self.__get_percentage_effectiveness(current_level_cap)

        #def print_sustain_value(sustain: SustainValue) -> str:
        #    return f"{sustain.flat} {sustain.percent}%"

        #def print_sustain(sustain: Sustain, prefix: str) -> None:
        #    print(f"{prefix}| HP:{print_sustain_value(sustain.single_hp)} - TP:{print_sustain_value(sustain.single_tp)} - "
        #          f"MHP:{print_sustain_value(sustain.multi_hp)} - MTP:{print_sustain_value(sustain.multi_tp)} - "
        #          f"Revive:{print_sustain_value(sustain.revive)}")

        def print_effective_sustain(sustain: Sustain, prefix: str) -> None:
            print(f"{prefix}| HP:{sustain.single_hp.get_effective_score_value(500, percentage_effectiveness, 100)} - "
                  f"TP:{sustain.single_tp.get_effective_score_value(100, percentage_effectiveness, 30)} - "
                  f"MHP:{sustain.multi_hp.get_effective_score_value(500, percentage_effectiveness, 100)} - "
                  f"MTP:{sustain.multi_tp.get_effective_score_value(100, percentage_effectiveness, 100)} - "
                  f"Revive:{sustain.revive.get_effective_score_value(100, 100, 50)}")


        #print_effective_sustain(item_sustains, "Item")
        #print_effective_sustain(skill_sustains, "Skill")

        sustain_score = 0

        # max_percent_value, percent_effectiveness, sustain_ratio
        item_single_hp_value = item_sustains.single_hp.get_effective_score_value(500, percentage_effectiveness, 100)
        item_single_tp_value = item_sustains.single_tp.get_effective_score_value(100, percentage_effectiveness, 100)
        item_multi_hp_value = item_sustains.multi_hp.get_effective_score_value(500, percentage_effectiveness, 100)
        item_multi_tp_value = item_sustains.multi_tp.get_effective_score_value(100, percentage_effectiveness, 50)

        if item_multi_hp_value > item_single_hp_value:
            item_single_hp_value = item_multi_hp_value

        sustain_score += item_single_hp_value
        sustain_score += item_multi_hp_value * 3
        sustain_score += item_single_tp_value
        sustain_score += item_multi_tp_value * 3

        skill_single_hp_value = skill_sustains.single_hp.get_effective_score_value(500, percentage_effectiveness, 100)
        skill_single_tp_value = skill_sustains.single_tp.get_effective_score_value(100, percentage_effectiveness, 100)
        skill_multi_hp_value = skill_sustains.multi_hp.get_effective_score_value(500, percentage_effectiveness, 100)
        skill_multi_tp_value = skill_sustains.multi_tp.get_effective_score_value(100, percentage_effectiveness, 100)

        if skill_multi_hp_value > skill_single_hp_value:
            skill_single_hp_value = skill_multi_hp_value

        sustain_score += skill_single_hp_value
        sustain_score += skill_multi_hp_value * 3
        sustain_score += skill_single_tp_value
        sustain_score += skill_multi_tp_value * 3

        # Revive is a flat boost to the sustain, if available.
        item_revive_value = item_sustains.revive.get_effective_score_value(100, 100, 100)
        skill_revive_value = skill_sustains.revive.get_effective_score_value(100, 100, 100)

        if item_revive_value > 0 or skill_revive_value > 0:
            sustain_score += 100

        return sustain_score

class NoSustainProcessor(SustainProcessor):
    def get_current_sustain_score(self, context: ExecutionContext) -> int:
        return 9999

