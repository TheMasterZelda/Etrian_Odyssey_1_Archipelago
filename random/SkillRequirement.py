from random import Random
from typing import Callable

from .DataStructure import SingleSkillRequirementData
from ..Constant import SkillRequirementShuffleType
from ..data.ClassData import CLASS_2_SKILLS
from ..data.SkillData import *

def generate_skill_requirements(skill_requirement_shuffle: SkillRequirementShuffleType, split_gathering: bool, random: Random, max_level: int) -> list[SingleSkillRequirementData]:
    if skill_requirement_shuffle == SkillRequirementShuffleType.vanilla:
        return []

    if skill_requirement_shuffle == SkillRequirementShuffleType.remove:
        skill_requirements = []
        for class2skill in CLASS_2_SKILLS:
            single_skill_requirement_data = SingleSkillRequirementData()
            single_skill_requirement_data.skill_id = class2skill.skill_id
            single_skill_requirement_data.required_skill_1_id = 0
            single_skill_requirement_data.required_skill_2_id = 0
            single_skill_requirement_data.required_skill_1_level = 0
            single_skill_requirement_data.required_skill_2_level = 0
            skill_requirements.append(single_skill_requirement_data)
        return skill_requirements
    if skill_requirement_shuffle == SkillRequirementShuffleType.level_shuffle:
        skill_requirements = []
        for class2skill in CLASS_2_SKILLS:
            single_skill_requirement_data = SingleSkillRequirementData()
            single_skill_requirement_data.skill_id = class2skill.skill_id
            single_skill_requirement_data.required_skill_1_id = class2skill.required_skill_1_id
            single_skill_requirement_data.required_skill_1_level = class2skill.required_skill_1_level
            single_skill_requirement_data.required_skill_2_id = class2skill.required_skill_2_id
            single_skill_requirement_data.required_skill_2_level = class2skill.required_skill_2_level

            if single_skill_requirement_data.required_skill_1_id != 0:
                single_skill_requirement_data.required_skill_1_level = __get_random_skill_level(random)
            if single_skill_requirement_data.required_skill_2_id != 0:
                single_skill_requirement_data.required_skill_2_level = __get_random_skill_level(random)

            skill_requirements.append(single_skill_requirement_data)
        return skill_requirements
    if skill_requirement_shuffle == SkillRequirementShuffleType.non_root_shuffle_with_mastery_retention:
        return __generate_all_class_skill_requirements(False, True, False, split_gathering, max_level, random)
    if skill_requirement_shuffle == SkillRequirementShuffleType.non_root_shuffle:
        return __generate_all_class_skill_requirements(False, False, False, split_gathering, max_level, random)
    if skill_requirement_shuffle == SkillRequirementShuffleType.full_shuffle_with_mastery_retention:
        return __generate_all_class_skill_requirements(True, True, False, split_gathering, max_level, random)
    if skill_requirement_shuffle == SkillRequirementShuffleType.full_shuffle:
        return __generate_all_class_skill_requirements(True, False, False, split_gathering, max_level, random)
    if skill_requirement_shuffle == SkillRequirementShuffleType.chaos:
        return __generate_all_class_skill_requirements(True, False, True, split_gathering, max_level, random)
    raise Exception(f"Unknown skill_requirement_shuffle type {skill_requirement_shuffle}")

def __generate_all_class_skill_requirements(full_shuffle: bool, mastery_retention: bool, chaos: bool, split_gathering: bool,
                                            max_level: int, random: Random) -> list[SingleSkillRequirementData]:
    def generate(skills: list[int], function: Callable[[list[int]], list[SingleSkillRequirementData]]):
        if not split_gathering:
            return function(skills)

        gathering_skills: set[int] = {skill_id for skill_id in skills if SKILL_SHUFFLE_INFO_BY_SKILL_ID[skill_id].is_gathering}
        skills = [skill_id for skill_id in skills if skill_id not in gathering_skills]

        result = function(skills)

        for skill_id in gathering_skills:
            requirement = SingleSkillRequirementData()
            requirement.skill_id = skill_id
            requirement.required_skill_1_id = 0
            requirement.required_skill_2_id = 0
            requirement.required_skill_1_level = 0
            requirement.required_skill_2_level = 0
            result.append(requirement)

        return result

    def generate_non_root(skills: list[EO1SkillData]) -> list[SingleSkillRequirementData]:
        return generate(__get_skill_ids(skills), lambda x: __generate_non_root_shuffle(x, mastery_retention, max_level, random))

    def generate_full(skills: list[EO1SkillData]) -> list[SingleSkillRequirementData]:
        return generate(__get_skill_ids(skills), lambda x: __generate_full_shuffle(x, mastery_retention, chaos, max_level, random))

    skill_requirements: list[SingleSkillRequirementData] = []
    if full_shuffle:
        skill_requirements.extend(generate_full(LANDSKNECHT_SKILLS))
        skill_requirements.extend(generate_full(SURVIVALIST_SKILLS))
        skill_requirements.extend(generate_full(PROTECTOR_SKILLS))
        skill_requirements.extend(generate_full(DARK_HUNTER_SKILLS))
        skill_requirements.extend(generate_full(MEDIC_SKILLS))
        skill_requirements.extend(generate_full(ALCHEMIST_SKILLS))
        skill_requirements.extend(generate_full(TROUBADOUR_SKILLS))
        skill_requirements.extend(generate_full(RONIN_SKILLS))
        skill_requirements.extend(generate_full(HEXER_SKILLS))
    else:
        skill_requirements.extend(generate_non_root(LANDSKNECHT_SKILLS))
        skill_requirements.extend(generate_non_root(SURVIVALIST_SKILLS))
        skill_requirements.extend(generate_non_root(PROTECTOR_SKILLS))
        skill_requirements.extend(generate_non_root(DARK_HUNTER_SKILLS))
        skill_requirements.extend(generate_non_root(MEDIC_SKILLS))
        skill_requirements.extend(generate_non_root(ALCHEMIST_SKILLS))
        skill_requirements.extend(generate_non_root(TROUBADOUR_SKILLS))
        skill_requirements.extend(generate_non_root(RONIN_SKILLS))
        skill_requirements.extend(generate_non_root(HEXER_SKILLS))
    return skill_requirements


def __get_skill_ids(skills: list[EO1SkillData]) -> list[int]:
    return [skill.id for skill in skills]

def __get_random_skill_level(random: Random) -> int:
    random_roll = random.randint(0, 100)
    if random_roll <= 10:  # 10% of skills have a high requirement (8, 9 or 10).
        return random.randint(8, 10)

    # Random between 1 and 7.
    return random.choices([1, 2, 3, 4, 5, 6, 7],
                          [20, 20, 30, 30, 40, 5, 15], k=1)[0]


def __get_random_skill_count_with_secondary_requirement(random: Random) -> int:
    return random.choices([2, 3, 4, 5, 6, 7, 8, 9],
                          [15, 15, 5, 5, 5, 10, 5, 5], k=1)[0]


def __get_random_root_skill_count(random: Random) -> int:
    return random.choice([3, 3, 4, 4, 4, 5, 6, 6])


def __ensure_no_circular_dependency(skill_requirements: dict[int, SingleSkillRequirementData]) -> bool:
    def get_required_skills(skill_id: int, parsed_skills: set[int]) -> bool:
        if skill_id in parsed_skills:
            return False

        parsed_skills.add(skill_id)

        # Skill is not generated yet.
        if skill_id not in skill_requirements:
            return True

        single_skill_requirement = skill_requirements[skill_id]

        if single_skill_requirement.required_skill_1_id != 0:
            if not get_required_skills(single_skill_requirement.required_skill_1_id, parsed_skills.copy()):
                return False
        if single_skill_requirement.required_skill_2_id != 0:
            if not get_required_skills(single_skill_requirement.required_skill_2_id, parsed_skills.copy()):
                return False

        return True

    for skill in skill_requirements.values():
        if not get_required_skills(skill.skill_id, set()):
            return False
    return True


def __ensure_dependency_count_respected(source_skill_id: int, max_requirement: int, skill_requirements: dict[int, SingleSkillRequirementData]) -> bool:
    if source_skill_id not in skill_requirements:
        raise Exception(
            f"Cannot validate the skill dependency depth since the skill id isn't defined in the skill requirements.")

    def get_required_skills(skill_id: int) -> set[int]:
        result = set[int]()

        # Skill is not generated yet.
        if skill_id not in skill_requirements:
            return result

        single_skill_requirement = skill_requirements[skill_id]

        if single_skill_requirement.required_skill_1_id != 0:
            result.add(single_skill_requirement.required_skill_1_id)
            result.update(get_required_skills(single_skill_requirement.required_skill_1_id))
        if single_skill_requirement.required_skill_2_id != 0:
            result.add(single_skill_requirement.required_skill_2_id)
            result.update(get_required_skills(single_skill_requirement.required_skill_2_id))

        return result

    for skill in skill_requirements.values():
        requirement_count = len(get_required_skills(skill.skill_id))
        if requirement_count > max_requirement:
            return False
    return True


def __get_minimum_required_level(skill: int, skill_requirements: dict[int, SingleSkillRequirementData]):
    def get_required_skills(skill_id: int) -> list[tuple[int, int]]:
        result = []

        # Unknown for now.
        if skill_id not in skill_requirements:
            return result

        requirement = skill_requirements[skill_id]

        if requirement.required_skill_1_id != 0:
            result.append((requirement.required_skill_1_id, requirement.required_skill_1_level))
            result.extend(get_required_skills(requirement.required_skill_1_id))
        if requirement.required_skill_2_id != 0:
            result.append((requirement.required_skill_2_id, requirement.required_skill_2_level))
            result.extend(get_required_skills(requirement.required_skill_2_id))

        return result

    def add_all_required_skills(result_requirements: dict[int, int], skill_id: int) -> None:
        for required_skill in get_required_skills(skill_id):
            required_skill_id = required_skill[0]
            required_level = required_skill[1]
            if required_skill_id in result_requirements:
                if required_level > result_requirements[required_skill_id]:
                    result_requirements[required_skill_id] = required_level
                else:
                    continue
            else:
                result_requirements[required_skill_id] = required_level

    requirements: dict[int, int] = {}

    add_all_required_skills(requirements, skill)

    return sum(requirements.values()) + 1


def __ensure_minimum_skill_level_respected(max_level_requirement: int, skill_requirements: dict[int, SingleSkillRequirementData]) -> bool:
    for skill in skill_requirements.values():
        level_requirement = __get_minimum_required_level(skill.skill_id, skill_requirements)
        if level_requirement > max_level_requirement:
            return False
    return True


def __generate_class_skill_requirements(skills: list[int], root_skills: list[int], non_root_skills: list[int], mastery_retention: bool, chaos: bool, max_level: int, random: Random) -> list[
    SingleSkillRequirementData]:
    skill_requirements: dict[int, SingleSkillRequirementData] = {}
    max_requirement: int = 4
    max_level_requirement: int = min(30, max_level - 10)
    if chaos:
        max_requirement = 20
        max_level_requirement = min(50, max_level - 10)

    for skill_id in root_skills:
        new_requirement = SingleSkillRequirementData()
        new_requirement.skill_id = skill_id
        skill_requirements[skill_id] = new_requirement

    skills_with_secondary_requirement: set[int]
    if chaos:
        skills_with_secondary_requirement = set(random.choices(non_root_skills, k=random.randint(2, 15)))
    else:
        skills_with_secondary_requirement = set(
            random.choices(non_root_skills, k=__get_random_skill_count_with_secondary_requirement(random)))

    eligible_skill_for_secondary_requirement = skills.copy()

    for skill_id in non_root_skills:
        new_requirement = SingleSkillRequirementData()
        new_requirement.skill_id = skill_id
        skill_requirements[skill_id] = new_requirement
        skill_info = SKILL_SHUFFLE_INFO_BY_SKILL_ID[skill_id]
        if not mastery_retention or skill_info.mastery_tree_id is None:
            skill_pool: list[int]
            if chaos:
                skill_pool = skills.copy()
            else:
                skill_pool = root_skills.copy()
            while skill_pool:
                new_requirement_id = random.choice(skill_pool)
                new_requirement.required_skill_1_id = new_requirement_id
                if not __ensure_no_circular_dependency(skill_requirements):
                    skill_pool.remove(new_requirement_id)
                    continue
                if not __ensure_dependency_count_respected(skill_id, max_requirement, skill_requirements):
                    skill_pool.remove(new_requirement_id)
                    continue
                new_requirement.required_skill_1_level = __get_random_skill_level(random)
                if not __ensure_minimum_skill_level_respected(max_level_requirement, skill_requirements):
                    # Technically the skill may not be the problem, but instead the level.
                    skill_pool.remove(new_requirement_id)
                    continue
                break

            if len(skill_pool) == 0:
                # If no valid skills are available
                new_requirement.required_skill_1_id = 0
                new_requirement.required_skill_1_level = 0
                continue
        else:
            new_requirement.required_skill_1_id = skill_info.mastery_tree_id
            new_requirement.required_skill_1_level = __get_random_skill_level(random)
            # Make ABSOLUTELY sure we have no breaking dependencies.
            if not __ensure_no_circular_dependency(skill_requirements):
                raise Exception("Failure Circular")
                # Fallback remove the dependency.
                new_requirement.required_skill_1_id = 0
                new_requirement.required_skill_1_level = 0
                continue
            # We tolerate +1 dependency here.
            if not __ensure_dependency_count_respected(skill_id, max_requirement + 1, skill_requirements):
                # Despite the +1 we broke. Fallback by removing dependency.
                new_requirement.required_skill_1_id = 0
                new_requirement.required_skill_1_level = 0
                continue
            if not __ensure_minimum_skill_level_respected(max_level_requirement, skill_requirements):
                # Set to level 1. This should guarantee nothing to break.
                new_requirement.required_skill_1_level = 1

        if skill_id in skills_with_secondary_requirement:
            # Secondary pull from any skills.
            skill_pool = eligible_skill_for_secondary_requirement.copy()
            skill_pool.remove(new_requirement.required_skill_1_id)  # Don't require the same skill twice...
            while skill_pool:
                new_requirement_id = random.choice(skill_pool)
                new_requirement.required_skill_2_id = new_requirement_id
                if not __ensure_no_circular_dependency(skill_requirements):
                    skill_pool.remove(new_requirement_id)
                    continue
                if not __ensure_dependency_count_respected(skill_id, max_requirement, skill_requirements):
                    skill_pool.remove(new_requirement_id)
                    continue
                new_requirement.required_skill_2_level = __get_random_skill_level(random)
                if not __ensure_minimum_skill_level_respected(max_level_requirement, skill_requirements):
                    # Technically the skill may not be the problem, but instead the level.
                    skill_pool.remove(new_requirement_id)
                    continue
                break

            if len(skill_pool) == 0:
                # None of the skills match the criteria. Cancel the second skill requirement.
                new_requirement.required_skill_2_id = 0
                new_requirement.required_skill_2_level = 0
                continue

    return list(skill_requirements.values())


def __generate_non_root_shuffle(skills: list[int], mastery_retention: bool, max_level: int, random: Random) -> list[SingleSkillRequirementData]:
    # Shuffle order so dependencies are more random.
    random.shuffle(skills)

    root_skills: list[int] = []
    non_root_skills: list[int] = []

    for skill_id in skills:
        skill_info = SKILL_SHUFFLE_INFO_BY_SKILL_ID[skill_id]
        if skill_info.is_root_skill:
            root_skills.append(skill_id)
        else:
            non_root_skills.append(skill_id)
    return __generate_class_skill_requirements(skills, root_skills, non_root_skills, mastery_retention, False,
                                                    max_level, random)

def __generate_full_shuffle(skills: list[int], mastery_retention: bool, chaos: bool, max_level: int, random: Random) -> list[SingleSkillRequirementData]:
    # Shuffle order so dependencies are more random.
    random.shuffle(skills)

    potential_root_skills = skills.copy()
    mastery_skills: set[int] = set()
    if mastery_retention:
        for skill_id in skills:
            skill_info = SKILL_SHUFFLE_INFO_BY_SKILL_ID[skill_id]
            if skill_info.mastery_tree_id is not None:
                potential_root_skills.remove(skill_info.skill_id)
                mastery_skills.add(skill_info.mastery_tree_id)

    root_skills: list[int]
    if chaos:
        root_skills = random.choices(potential_root_skills, k=random.randint(3, 5))
    else:
        root_skills = random.choices(potential_root_skills, k=__get_random_root_skill_count(random))
    non_root_skills: list[int] = []
    for skill_id in skills:
        if skill_id not in root_skills:
            non_root_skills.append(skill_id)

    # With Mastery Retention, the mastery skills must be at the very end to prevent infinite dependencies.
    if mastery_retention:
        to_add: list[int] = []
        for skill_id in mastery_skills:
            if skill_id in non_root_skills:
                non_root_skills.remove(skill_id)
                to_add.append(skill_id)
        non_root_skills.extend(to_add)

    return __generate_class_skill_requirements(skills, root_skills, non_root_skills, mastery_retention, chaos, max_level, random)
