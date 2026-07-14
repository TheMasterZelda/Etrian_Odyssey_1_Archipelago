from abc import ABC
from typing import Generic, TypeVar

from .LogicData import SingleClassLogicData
from ..data.SkillUnlockData import *


class DataSource(ABC):
    pass

T = TypeVar('T')

class SingleDataSource(Generic[T]):
    data_collection: T

    def __init__(self, data_collection: T):
        self.data_collection = data_collection

class EtrianOdysseyDataSource(DataSource):
    skill_requirements_data_source: SingleDataSource[dict[int, EO1Class2SkillData]]

    def __init__(self):
        self.skill_requirements_data_source = SingleDataSource(SKILL_REQUIREMENTS_BY_ID)

    def get_skill_unlock_data_by_skill_id(self, skill_id: int) -> list[SkillUnlockData]:
        return SKILL_UNLOCK_DATA_BY_SKILL_ID[skill_id]

    def get_skill_requirements_by_skill_id(self, skill_id: int) -> EO1Class2SkillData:
        return self.skill_requirements_data_source.data_collection[skill_id]

    # ClassData
    # LogicalSkillDependency

    # ENEMY_BY_ID
    # ENCOUNTER_BY_ID
    # ENCOUNTER_GROUP_BY_ID
    # ITEM_COMPOUND_BY_ITEM_ID