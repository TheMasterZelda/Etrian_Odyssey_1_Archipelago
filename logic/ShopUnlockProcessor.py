from .ILogicManager import ExecutionContext
from .StateInterface import StateInterface
from ..logic.LogicData import AllLogicData
from ..data.ItemCompoundData import *


class ShopUnlockProcessor:
    def can_unlock_item(self, item_id: int, context: ExecutionContext) -> bool:
        item_compound = ITEM_COMPOUND_BY_ITEM_ID[item_id]

        if not self.__is_material_available(item_compound.material_1_id, context):
            return False
        if not self.__is_material_available(item_compound.material_2_id, context):
            return False
        if not self.__is_material_available(item_compound.material_3_id, context):
            return False

        return True

    def __is_material_available(self, material_item_id: int, context: ExecutionContext) -> bool:
        if material_item_id == 0:
            return True

        if material_item_id in context.logic_data.compendium_logic_data.fillable_compendium_entries:
            return True

        if material_item_id not in context.logic_data.compendium_logic_data.unfillable_compendium_entries:
            raise Exception(f"Unknown material item id: {material_item_id}")

        return False

