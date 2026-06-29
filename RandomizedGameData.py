from abc import ABC, abstractmethod
from typing import Any

class IRandomizedGameDataEntry(ABC):
    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        pass
    @abstractmethod
    def deserialize(self, data: dict[str, Any]):
        pass

class RandomizedGameData:




    def serialize(self) -> dict[str, Any]:
        pass

    def deserialize(self, data: dict[str, Any]):
        pass
