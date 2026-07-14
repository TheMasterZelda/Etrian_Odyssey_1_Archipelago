# TODO find a better place for these.
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

    def __init__(self):
        self.skill_id = 0
        self.required_skill_1_id = 0
        self.required_skill_1_level = 0
        self.required_skill_2_id = 0
        self.required_skill_2_level = 0

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