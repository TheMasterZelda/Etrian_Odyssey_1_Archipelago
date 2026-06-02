from __future__ import annotations
from dataclasses import dataclass, field

from ...data.Generic import EO1Element, EO1Ailment, EO1BodyPart


@dataclass
class EnemyAttributes:
    damage_type_resistance: list[EO1Element] = field(default_factory=list)
    damage_type_immunity: list[EO1Element] = field(default_factory=list)
    damage_type_weakness: list[EO1Element] = field(default_factory=list)
    ailment_resistance: list[EO1Element] = field(default_factory=list)
    skills_body_use: list[EO1BodyPart] = field(default_factory=list)
    can_inflict_status_effect: bool = False
    can_inflict_bind: bool = False
    can_apply_buff: bool = False # TODO change for a list of buff effects to handle counter?
    # TODO list of debuff that can be applied to the party.

    def copy(self) -> EnemyAttributes:
        new_copy = EnemyAttributes()
        new_copy.damage_type_resistance = self.damage_type_resistance.copy()
        new_copy.damage_type_immunity = self.damage_type_immunity.copy()
        new_copy.damage_type_weakness = self.damage_type_weakness.copy()
        new_copy.ailment_resistance = self.ailment_resistance.copy()
        new_copy.skills_body_use = self.skills_body_use.copy()
        new_copy.can_inflict_status_effect = self.can_inflict_status_effect
        new_copy.can_inflict_bind = self.can_inflict_bind
        new_copy.can_apply_buff = self.can_apply_buff
        return new_copy