SAVE_ADDRESS_STATIC_POINTER_ADDRESS = 0x020F077C
GAME_STATE_STATIC_ADDRESS = 0X020F0CC0
PLAYER_SLOT_NAME_STATIC_ADDRESS = 0x020DC600
SAVE_CONTEXT_OFFSET = 0x14
MONEY_VALUE_OFFSET = 0x640 + SAVE_CONTEXT_OFFSET
INVENTORY_START_OFFSET = 0x66C + SAVE_CONTEXT_OFFSET
INVENTORY_ITEM_SIZE = 60
CUSTOM_SAVE_DATA_OFFSET = 0x213C + SAVE_CONTEXT_OFFSET
CUSTOM_SAVE_DATA_SIZE = 0x74

GENERIC_OBJECT_HEADER_SIZE = 0x30
OBJECT_0X15_STATIC_POINTER = 0x020DADA0
QUEST_WINDOW_OBJ_QUEST_ARRAY_OFFSET = 0x58
QUEST_WINDOW_OBJ_CURRENT_QUEST_INDEX_OFFSET = 0x134

COMPENDIUM_CODEX_TABLE_OFFSET = 0xAE0 + SAVE_CONTEXT_OFFSET
COMPENDIUM_CODEX_TABLE_SIZE = 0x5FF + 0xB1

SHOP_ITEM_FLAG_TABLE_OFFSET = 0x760 + 0x2C0 + SAVE_CONTEXT_OFFSET
SHOP_ITEM_FLAG_TABLE_SIZE = 0xC0

FLAG_TABLE_OFFSET = 0x26E8 + SAVE_CONTEXT_OFFSET
FLAG_TABLE_SIZE = 0x200

SC_LEVEL_CAP_OFFSET = 0x00
SC_FLOOR_LIMIT = 0x01
SC_LAST_RECEIVED_ITEM_INDEX = 0x04
SC_LAST_RECEIVED_INVENTORY_ITEM_INDEX = 0x08
SC_CLASS_UNLOCK = 0x10
SC_SKILL_UNLOCK = 0x20
SC_ITEM_RECEPTION = 0x4C
SC_ITEM_RECEPTION_ITEM_COUNT = 20

from dataclasses import dataclass

@dataclass
class EO1ItemLookupTableModifier:
    start: int
    end: int
    offset: int

# Used for Shop structures and item compendium.
ITEM_LOOKUP_TABLE_MODIFIER: list[EO1ItemLookupTableModifier] = [
    EO1ItemLookupTableModifier(1, 0x100, 0),
    EO1ItemLookupTableModifier(0x3E9, 0x4E8, 0x100),
    EO1ItemLookupTableModifier(0x7D1, 0x8D0, 0x200),
    EO1ItemLookupTableModifier(0xBB9, 0xCB8, 0x300),
    EO1ItemLookupTableModifier(0xFA1, 0x11A0, 0x400),
]

def get_modified_item_id_for_lookup(item_id: int) -> int:
    for modifier in ITEM_LOOKUP_TABLE_MODIFIER:
        if modifier.start <= item_id <= modifier.end:
            return item_id - modifier.start + modifier.offset
    raise Exception(f"Item ID {item_id} does not match any lookup table modifier ranges.")

class EO1CompendiumCodexValues:
    UNFILLED = 0
    UNREPORTED = 0xFF
    REPORTED_NEW_TAG = 0xFD
    REPORTED_NO_NEW_TAG = 0xF9