from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from .StateInterface import StateInterface

from ..data.ClassData import *
from ..data.SkillData import *
from ..data.SkillUnlockData import *

from ..Options import *
from .LogicData import *

class ClassProcessor:
    def __is_skill_unlocked(self, skill_id: int, state: StateInterface) -> bool:
        skill_unlocks = SKILL_UNLOCK_DATA_BY_SKILL_ID[skill_id]

        for skill_unlock in skill_unlocks:
            if state.has_item_count(skill_unlock.ap_item_name, skill_unlock.item_count_requirement):
                return True

        return False

    def __all_skills_unlocked(self, all_skill_id: set[int], state: StateInterface) -> bool:
        for skill_id in all_skill_id:
            if not self.__is_skill_unlocked(skill_id, state):
                return False
        return True

    def update_class_data(self, logic_data: AllLogicData, state: StateInterface) -> bool:
        changed = False

        for class_logic_data in logic_data.class_data.class_as_list:
            class_data = CLASS_DATA_BY_NAME[class_logic_data.class_name]
            if not class_logic_data.class_unlocked:
                if state.has_item(class_data.name):
                    class_logic_data.class_unlocked = True
                    changed = True
            for skill_logic_data in class_logic_data.class_skills.values():
                if not skill_logic_data.skill_unlocked:
                    if self.__is_skill_unlocked(skill_logic_data.skill_id, state):
                        skill_logic_data.skill_unlocked = True
                        changed = True

                if not skill_logic_data.skill_unlocked:
                    continue
                if skill_logic_data.skill_usable:
                    continue
                if skill_logic_data.required_level > logic_data.get_effective_level_cap(): # Don't count the +2 SP from level for now.
                    continue

                if self.__all_skills_unlocked(skill_logic_data.required_skills, state):
                    skill_logic_data.skill_usable = True
                    changed = True

        return changed

    def recalculate_class_data(self, logic_data: AllLogicData, state: StateInterface) -> bool:
        changed = False

        for class_logic_data in logic_data.class_data.class_as_list:
            class_data = CLASS_DATA_BY_NAME[class_logic_data.class_name]
            if class_logic_data.class_unlocked:
                if not state.has_item(class_data.name):
                    class_logic_data.class_unlocked = False
                    changed = True
            for skill_logic_data in class_logic_data.class_skills.values():
                if skill_logic_data.skill_unlocked:
                    if not self.__is_skill_unlocked(skill_logic_data.skill_id, state):
                        skill_logic_data.skill_unlocked = False
                        skill_logic_data.skill_usable = False
                        changed = True
                        continue

                if skill_logic_data.required_level < logic_data.get_effective_level_cap(): # Don't count the +2 SP from level for now.
                    skill_logic_data.skill_unlocked = False
                    changed = True

                if not self.__all_skills_unlocked(skill_logic_data.required_skills, state):
                    skill_logic_data.skill_usable = False
                    changed = True

        return changed

    def initialize_data(self, class_data: ClassLogicData, remove_skills_requirements: bool):
        class_data.landsknecht = self.__initialize_class_data(EO1Class.LANDSKNECHT, LANDSKNECHT_SKILLS, remove_skills_requirements)
        class_data.survivalist = self.__initialize_class_data(EO1Class.SURVIVALIST, SURVIVALIST_SKILLS, remove_skills_requirements)
        class_data.protector = self.__initialize_class_data(EO1Class.PROTECTOR, PROTECTOR_SKILLS, remove_skills_requirements)
        class_data.dark_hunter = self.__initialize_class_data(EO1Class.DARK_HUNTER, DARK_HUNTER_SKILLS, remove_skills_requirements)
        class_data.medic = self.__initialize_class_data(EO1Class.MEDIC, MEDIC_SKILLS, remove_skills_requirements)
        class_data.alchemist = self.__initialize_class_data(EO1Class.ALCHEMIST, ALCHEMIST_SKILLS, remove_skills_requirements)
        class_data.troubadour = self.__initialize_class_data(EO1Class.TROUBADOUR, TROUBADOUR_SKILLS, remove_skills_requirements)
        class_data.ronin = self.__initialize_class_data(EO1Class.RONIN, RONIN_SKILLS, remove_skills_requirements)
        class_data.hexer = self.__initialize_class_data(EO1Class.HEXER, HEXER_SKILLS, remove_skills_requirements)
        class_data.set_stale(True)

    def __initialize_class_data(self, class_name: str, class_skill_data: list[EO1SkillData], remove_skills_requirements: bool) -> SingleClassLogicData:
        new_class_data = SingleClassLogicData()
        new_class_data.class_name = class_name
        new_class_data.class_unlocked = False
        new_class_data.class_skills = {}

        class_data = CLASS_DATA_BY_NAME[class_name]

        def get_required_skills(skill_id: int) -> list[tuple[int, int]]:
            result = []
            class2skill = class_data.class2skills[skill_id]

            if class2skill.required_skill_1_id != 0:
                result.append((class2skill.required_skill_1_id, class2skill.required_skill_1_level))
                result.extend(get_required_skills(class2skill.required_skill_1_id))
            if class2skill.required_skill_2_id != 0:
                result.append((class2skill.required_skill_2_id, class2skill.required_skill_2_level))
                result.extend(get_required_skills(class2skill.required_skill_2_id))

            return result

        for skill in class_skill_data:
            skill_data = SkillLogicData()
            skill_data.skill_id = skill.id
            skill_data.skill_usable = False
            skill_data.skill_unlocked = False
            skill_data.required_skills = set()
            skill_data.required_level = 1

            if remove_skills_requirements:
                if skill.id in SKILL_HARD_DEPENDENCIES:
                    skill_data.required_level += 1
                    skill_data.required_skills.add(SKILL_HARD_DEPENDENCIES[skill.id])
                new_class_data.class_skills[skill.id] = skill_data
                continue

            requirements: dict[int, int] = {}
            for required_skill in get_required_skills(skill.id):
                required_skill_id = required_skill[0]
                required_level = required_skill[1]
                if required_skill_id in requirements:
                    if required_level > requirements[required_skill_id]:
                        requirements[required_skill_id] = required_level
                    else:
                        continue
                else:
                    requirements[required_skill_id] = required_level

            skill_data.required_level += sum(requirements.values())
            skill_data.required_skills = set(requirements)
            new_class_data.class_skills[skill.id] = skill_data

        return new_class_data