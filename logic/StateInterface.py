from __future__ import annotations
from abc import ABC, abstractmethod


class StateInterface(ABC):
    @abstractmethod
    def can_reach_region(self, region: str) -> bool:
        pass

    @abstractmethod
    def has_item(self, item_name: str) -> bool:
        pass

    @abstractmethod
    def has_item_count(self, item_name: str, item_count: int) -> bool:
        pass

    @abstractmethod
    def get_regions(self) -> list[str]:
        pass

