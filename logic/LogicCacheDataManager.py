from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable

from .ILogicManager import ExecutionContext
from .LogicCacheData import DualIntSetLogicCacheData
from .StateInterface import StateInterface

# TODO Rename

class ILogicCacheDataManager(ABC):
    @abstractmethod
    def update_all(self, context: ExecutionContext) -> bool:
        pass

    @abstractmethod
    def recalculate(self, context: ExecutionContext) -> bool:
        pass

class DualIntSetLogicCacheDataManager(ILogicCacheDataManager):
    cache_data: DualIntSetLogicCacheData
    can_access_function: Callable[[int, ExecutionContext], bool]

    def __init__(self, logic_data: DualIntSetLogicCacheData, can_access: Callable[int, ExecutionContext]):
        self.cache_data = logic_data
        self.can_access_function = can_access

    def is_accessible(self, identifier: int, context: ExecutionContext) -> bool:
        if identifier in self.cache_data.accessible:
            return True

        if self.can_access_function(identifier, context):
            if not self.cache_data.update_suspended:
                self.cache_data.unaccessible.remove(identifier)
                self.cache_data.accessible.add(identifier)
            return True

        return False

    def update_all(self, context: ExecutionContext) -> bool:
        if not self.cache_data.is_stale():
            return False

        self.cache_data.update_suspended = True

        new_accessible = set()
        for identifier in self.cache_data.unaccessible:
            if self.can_access_function(identifier, context):
                new_accessible.add(identifier)

        for identifier in new_accessible:
            self.cache_data.unaccessible.remove(identifier)
            self.cache_data.accessible.add(identifier)

        self.cache_data.update_suspended = False

        self.cache_data.set_stale(False)
        changed = len(new_accessible) > 0
        return changed

    def recalculate(self, context: ExecutionContext) -> bool:
        new_unaccessible = set()
        for identifier in self.cache_data.accessible:
            if not self.can_access_function(identifier, context):
                new_unaccessible.add(identifier)

        for identifier in new_unaccessible:
            self.cache_data.accessible.remove(identifier)
            self.cache_data.unaccessible.add(identifier)

        # TODO decide if this is omitted. Do not set to False, since the data could already be stale.
        self.cache_data.set_stale(True) # For safety.

        changed = len(new_unaccessible) > 0
        return changed
