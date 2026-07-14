from random import Random
from typing import Any

from .Constant import SkillRequirementShuffleType, get_max_level_for_goal, EO1Goal, get_max_floor_for_goal
from .Options import EtrianOdysseyOptions
from .data.MaxLevelByFloor import MAX_LEVEL_BY_FLOOR
from .random.DataStructure import SingleSkillRequirementData


class RandomizedGameData:
    initialized: bool
    skill_requirements: list[SingleSkillRequirementData] | None

    def __init__(self):
        self.initialized = False
        self.skill_requirements = None

    def generate_randomized_game_data(self, random: Random, options: EtrianOdysseyOptions):
        # Only initialize once.
        if self.initialized:
            return

        self.__generate_skill_requirements(random, options)

        self.initialized = True

    def serialize(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.skill_requirements is not None:
            result["skill_requirements"] = []
            for single_skill_requirement_data in self.skill_requirements:
                result["skill_requirements"].append(single_skill_requirement_data.serialize())

        return result

    def deserialize(self, data: dict[str, Any]):
        if "skill_requirements" in data:
            self.skill_requirements = []
            for serialized_data in data["skill_requirements"]:
                single_skill_requirement_data = SingleSkillRequirementData()
                single_skill_requirement_data.deserialize(serialized_data)
                self.skill_requirements.append(single_skill_requirement_data)

        self.initialized = True

    def __generate_skill_requirements(self, random: Random, options: EtrianOdysseyOptions):
        max_level = get_max_level_for_goal(EO1Goal(options.goal.value))
        max_floor = get_max_floor_for_goal(EO1Goal(options.goal.value))
        max_level = min(max_level, MAX_LEVEL_BY_FLOOR[min(max_floor, 30)])
        skill_requirement_shuffle = SkillRequirementShuffleType(options.skill_requirement_shuffle.value)
        from .random.SkillRequirement import generate_skill_requirements
        self.skill_requirements = generate_skill_requirements(skill_requirement_shuffle, True, random, max_level)
