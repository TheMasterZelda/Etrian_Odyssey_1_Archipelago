from abc import ABC, abstractmethod
from typing import Any

class IRandomizedGameDataEntry(ABC):
    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        pass
    @abstractmethod
    def deserialize(self, data: dict[str, Any]):
        pass

class SingleSkillRequirementData(IRandomizedGameDataEntry):
    skill_id: int
    required_skill_1_id: int
    required_skill_1_level: int
    required_skill_2_id: int
    required_skill_2_level: int

    def serialize(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "required_skill_1_id": self.required_skill_1_id,
            "required_skill_1_level": self.required_skill_1_level,
            "required_skill_2_id": self.required_skill_2_id,
            "required_skill_2_level": self.required_skill_2_level
        }

    def deserialize(self, data: dict[str, Any]):
        self.skill_id = data["skill_id"]
        self.required_skill_1_id = data["required_skill_1_id"]
        self.required_skill_1_level = data["required_skill_1_level"]
        self.required_skill_2_id = data["required_skill_2_id"]
        self.required_skill_2_level = data["required_skill_2_level"]

class RandomizedGameData:
    skill_requirements: list[SingleSkillRequirementData]
    #initial_floor_limit: int
    #initial_level_cap: int
    test: str

    def serialize(self) -> dict[str, Any]:
        pass

    def deserialize(self, data: dict[str, Any]):
        pass

#t = SingleSkillRequirementData()
#t.skill_id = 1
#t.required_skill_1_id = 2
#t.required_skill_1_level = 3
#t.required_skill_2_id = 4
#t.required_skill_2_level = 5
#print(vars(t))