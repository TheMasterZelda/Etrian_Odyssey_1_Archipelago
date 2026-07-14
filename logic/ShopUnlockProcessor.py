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

        if context.logic_manager.can_fill_compendium_entry(material_item_id, context):
            return True

        # TODO doesn't make sense to do this here anymore.
        if not not context.logic_manager.can_fill_compendium_entry(material_item_id, context):
            raise Exception(f"Unknown material item id: {material_item_id}")

        return False

