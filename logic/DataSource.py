from abc import ABC

from .LogicData import SingleClassLogicData
from ..data.SkillUnlockData import *


class DataSource(ABC):
    pass


class EtrianOdysseyDataSource(DataSource):
    def get_skill_unlock_data_by_skill_id(self, skill_id: int) -> list[SkillUnlockData]:
        return SKILL_UNLOCK_DATA_BY_SKILL_ID[skill_id]

    def get_skill_requirements_by_skill_id(self, skill_id: int) -> EO1Class2SkillData:
        return SKILL_REQUIREMENTS_BY_ID[skill_id]