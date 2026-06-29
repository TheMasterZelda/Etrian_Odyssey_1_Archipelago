from typing import TYPE_CHECKING, Dict, Set, Tuple, Any

import Utils
import math
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from NetUtils import NetworkItem, ClientStatus
from dataclasses import dataclass
from .data.Memory import *
from .Items import *
from .Locations import *
from .data.InventoryItemData import *
from .data.ItemData import *
from .data.QuestData import QUEST_DATA_BY_LOCATION_ID, QUEST_DATA_BY_QUEST_ID
from .data.ItemCompoundData import SHOP_UNLOCK_BY_LOCATION_ID
from .data.TreasureData import *
from .Constant import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

EXPECTED_ROM_NAME = "EO1AP V1"

BIZHAWK_ARM9_DOMAIN = "ARM9 System Bus"


def get_client_as_command_processor(self: "BizHawkClientCommandProcessor"):
    ctx = self.ctx
    from worlds._bizhawk.context import BizHawkClientContext
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, EtrianOdysseyClient)
    return client

class EtrianOdysseyClientCustomCommands(IntEnum):
    NONE = 0
    DEBUG_EO_SET_FLAG_OFF = 1
    DEBUG_EO_SET_FLAG_ON = 2
    DEBUG_EO_WRITE_RAW = 3

def cmd_debug_eo_set_flag_off(self: "BizHawkClientCommandProcessor", flag_id: str):
    client = get_client_as_command_processor(self)
    client.custom_command_to_run = EtrianOdysseyClientCustomCommands.DEBUG_EO_SET_FLAG_OFF
    client.custom_command_parameter = int(flag_id)

def cmd_debug_eo_set_flag_on(self: "BizHawkClientCommandProcessor", flag_id: str):
    client = get_client_as_command_processor(self)
    client.custom_command_to_run = EtrianOdysseyClientCustomCommands.DEBUG_EO_SET_FLAG_ON
    client.custom_command_parameter = int(flag_id)

def cmd_debug_eo_write_raw(self: "BizHawkClientCommandProcessor", address: str, size: str, value: str):
    client = get_client_as_command_processor(self)
    client.custom_command_to_run = EtrianOdysseyClientCustomCommands.DEBUG_EO_WRITE_RAW
    client.custom_command_parameter = [int(address), int(size), int(value)]

class EtrianOdysseyClient(BizHawkClient):
    game = GAME_NAME
    system = "NDS"
    #patch_suffix = ".apeo1"
    goal: EO1Goal | None
    scouted_locations: set[int]
    quest_completion_reward_hint: bool | None
    key_items_to_process: set[int]
    custom_command_to_run: EtrianOdysseyClientCustomCommands
    custom_command_parameter: Any

    def initialize_client(self):
        self.goal = None
        self.scouted_locations = set()
        self.quest_completion_reward_hint = None
        self.key_items_to_process = {key_item.item_id for key_item in KEY_ITEMS_WITH_FLAG}

    def register_custom_commands(self, ctx: "BizHawkClientContext"):
        ctx.command_processor.commands["debug_eo_set_flag_off"] = cmd_debug_eo_set_flag_off
        ctx.command_processor.commands["debug_eo_set_flag_on"] = cmd_debug_eo_set_flag_on
        ctx.command_processor.commands["debug_eo_write_raw"] = cmd_debug_eo_write_raw

        self.custom_command_to_run = EtrianOdysseyClientCustomCommands.NONE
        self.custom_command_parameter = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        def __rom_name_match(rom_name_bytes: bytes) -> bool:
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name == "ETRIAN1":
                logger.info("ERROR: You appear to be running an unpatched version of Etrian Odyssey. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != EXPECTED_ROM_NAME:
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
            return True

        try:
            try:
                # Attempt to do this using Bizhawk 2.10+ compatible code.
                rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0, 12, "ROM")]))[0]
                if not __rom_name_match(rom_name_bytes):
                    return False
            except UnicodeDecodeError:
                # If this failed, this may be due to running on Bizhawk 2.9.
                # Attempt to read the rom name from main memory instead.
                rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x02BFFA80, 12, BIZHAWK_ARM9_DOMAIN)]))[0]
                if not __rom_name_match(rom_name_bytes):
                    return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        self.initialize_client()
        self.register_custom_commands(ctx)

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        player_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(PLAYER_SLOT_NAME_STATIC_ADDRESS, 0x40, BIZHAWK_ARM9_DOMAIN)]))[0]
        player_name = player_name_bytes.decode("utf-8").rstrip("\x00")
        ctx.auth = player_name

    @staticmethod
    def check_flag(flag_table: bytes, flag_id_to_check: int) -> bool:
        byte_offset = math.floor(flag_id_to_check / 8)
        bit = 1 << (flag_id_to_check % 8)
        return flag_table[byte_offset] & bit != 0

    @staticmethod
    def check_codex_entry(enemy_id: int, codex_table: bytes, reported_only: bool) -> bool:
        entry_value = codex_table[0x600 + enemy_id]

        if entry_value == EO1CompendiumCodexValues.UNFILLED:
            return False

        if reported_only and entry_value == EO1CompendiumCodexValues.UNREPORTED:
            return False

        return True

    @staticmethod
    def check_compendium_entry(item_id: int, compendium_table: bytes, reported_only: bool) -> bool:
        entry_value = compendium_table[0x400 + (item_id - 0xFA1)]

        if entry_value == EO1CompendiumCodexValues.UNFILLED:
            return False

        if reported_only and entry_value == EO1CompendiumCodexValues.UNREPORTED:
            return False

        return True

    def check_shop_entry(self, item_id: int, shop_table: bytes) -> bool:
        effective_item_id = get_modified_item_id_for_lookup(item_id)
        return self.check_flag(shop_table, effective_item_id)

    @staticmethod
    def load_reception_inventory_item_from_index(sc_data: bytes, index: int) -> int:
        return int.from_bytes(sc_data[SC_ITEM_RECEPTION + index * 2:SC_ITEM_RECEPTION + index * 2 + 2], "little")

    @staticmethod
    def handle_non_inventory_item_receptions(player_id: int, items_received: list[NetworkItem], all_previous_items_received: list[NetworkItem], save_pointer: int, raw_money: bytes, sc_data: bytes) -> dict[int, tuple[int, int, int]]:
        @dataclass
        class MemoryValues:
            current_value: int
            new_value: int
            value_size: int

        custom_savedata_address = save_pointer + CUSTOM_SAVE_DATA_OFFSET
        money_address = save_pointer + MONEY_VALUE_OFFSET
        money = int.from_bytes(raw_money, "little")
        level_cap_address = custom_savedata_address + SC_LEVEL_CAP_OFFSET
        level_cap = int.from_bytes(sc_data[SC_LEVEL_CAP_OFFSET:SC_LEVEL_CAP_OFFSET+1], "little")
        floor_limit_address = custom_savedata_address + SC_FLOOR_LIMIT
        floor_limit = int.from_bytes(sc_data[SC_FLOOR_LIMIT:SC_FLOOR_LIMIT+1], "little")
        class_unlock_address = custom_savedata_address + SC_CLASS_UNLOCK
        class_unlocks = sc_data[SC_CLASS_UNLOCK:SC_CLASS_UNLOCK+9]
        skill_unlock_address: list[int] = []
        skill_unlocks: list[int] = []

        for index in range(9):
            skill_offset = SC_SKILL_UNLOCK + (4 * index)
            skill_unlock_address.append(custom_savedata_address + skill_offset)
            skill_unlocks.append(int.from_bytes(sc_data[skill_offset:skill_offset+4], "little"))

        memory_values: dict[int, MemoryValues] = {
            money_address: MemoryValues(money, money, 4),
            level_cap_address: MemoryValues(level_cap, level_cap, 1),
            floor_limit_address: MemoryValues(floor_limit, floor_limit, 1),
            **{class_unlock_address+index:MemoryValues(class_unlocks[index], class_unlocks[index], 1) for index in range(9)},
            **{skill_unlock_address[index]:MemoryValues(skill_unlocks[index], skill_unlocks[index], 4) for index in range(9)}
        }

        # This is to handle progressive skills.
        all_current_skill_items: list[SkillItem] = []
        for item in all_previous_items_received:
            item_id = item.item
            item_type = ALL_ITEMS_BY_ID[item_id].item_type
            if item_type != EtrianOdysseyItemType.SKILL:
                continue
            all_current_skill_items.append(SKILL_ITEM_TYPE_BY_AP_ITEM_ID[item_id])

        for current_item in items_received:
            item_id = current_item.item
            item_type = ALL_ITEMS_BY_ID[item_id].item_type
            if item_type == EtrianOdysseyItemType.INVENTORY:
                continue
            elif item_type == EtrianOdysseyItemType.MONEY:
                if current_item.player == player_id and location_is_handled_in_game(current_item.location):
                    continue
                memory_values[money_address].new_value += ALL_MONEY_BY_ID[item_id].amount
            elif item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
                prog_level_data = ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item_id]
                new_value = memory_values[level_cap_address].new_value + prog_level_data.level_amount
                new_value = min(new_value, MAX_LEVEL)
                memory_values[level_cap_address].new_value = new_value
            elif item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
                prog_floor_data = ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item_id]
                new_value = memory_values[floor_limit_address].new_value + prog_floor_data.floor_amount
                new_value = min(new_value, MAX_FLOOR)
                memory_values[floor_limit_address].new_value = new_value
            elif item_type == EtrianOdysseyItemType.CLASS:
                class_data = ALL_CLASS_BY_ITEM_ID[item_id]
                memory_values[class_unlock_address+class_data.class_order_id].new_value = 1
            elif item_type == EtrianOdysseyItemType.SKILL:
                skill_item = SKILL_ITEM_TYPE_BY_AP_ITEM_ID[item_id]
                skill_unlock_values: list[int] = []
                for index in range(9):
                    skill_unlock_values.append(memory_values[skill_unlock_address[index]].new_value)

                skill_unlock_values = apply_skill_item_to_values(skill_item, skill_unlock_values, all_current_skill_items)

                for index in range(9):
                    memory_values[skill_unlock_address[index]].new_value = skill_unlock_values[index]

                all_current_skill_items.append(skill_item)
            else:
                raise NotImplementedError(f"Unknown item type: {item_type}")


        writes_to_perform: dict[int, tuple[int, int, int]] = {}

        for address, values in memory_values.items():
            if values.current_value != values.new_value:
                writes_to_perform[address] = (values.current_value, values.new_value, values.value_size)

        return writes_to_perform

    async def handle_received_items(self, ctx: "BizHawkClientContext", save_pointer: int, raw_money: bytes, sc_data: bytes, global_guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        last_received_item_index = int.from_bytes(sc_data[SC_LAST_RECEIVED_ITEM_INDEX:SC_LAST_RECEIVED_ITEM_INDEX+4], "little")
        last_received_inventory_item_index = int.from_bytes(sc_data[SC_LAST_RECEIVED_INVENTORY_ITEM_INDEX:SC_LAST_RECEIVED_INVENTORY_ITEM_INDEX+4], "little")

        items_reception_array = [self.load_reception_inventory_item_from_index(sc_data, i) for i in range(SC_ITEM_RECEPTION_ITEM_COUNT)]

        writes_to_perform: dict[int, tuple[int, int, int]] = {}

        save_last_received_item_index = last_received_item_index
        save_last_received_inventory_item_index = last_received_inventory_item_index

        if len(ctx.items_received) > last_received_item_index:
            result = self.handle_non_inventory_item_receptions(ctx.slot, ctx.items_received[last_received_item_index:], ctx.items_received[:last_received_item_index], save_pointer, raw_money, sc_data)
            last_received_item_index = len(ctx.items_received)
            if result:
                writes_to_perform.update(result)

        if 0x00 in items_reception_array:
            current_item_reception_index = items_reception_array.index(0x00)
            for current_item in ctx.items_received[last_received_inventory_item_index:]:
                item_id = current_item.item
                item_type = ALL_ITEMS_BY_ID[item_id].item_type
                if item_type != EtrianOdysseyItemType.INVENTORY:
                    last_received_inventory_item_index += 1
                    continue

                if current_item.player == ctx.slot and location_is_handled_in_game(current_item.location):
                    last_received_inventory_item_index += 1
                    continue

                for item_index in range(current_item_reception_index, SC_ITEM_RECEPTION_ITEM_COUNT):
                    eo_item_id = items_reception_array[item_index]
                    if eo_item_id != 0x00:
                        current_item_reception_index += 1
                        continue

                    current_item_reception_index = item_index + 1
                    last_received_inventory_item_index += 1
                    address = save_pointer + CUSTOM_SAVE_DATA_OFFSET + SC_ITEM_RECEPTION + item_index * 2
                    writes_to_perform[address] = (0x00, ITEM_PER_AP_ITEM_ID[item_id].item_id, 2)
                    break

                if 0x00 not in items_reception_array[current_item_reception_index:]:
                    break

        if save_last_received_item_index != last_received_item_index:
            address = save_pointer + CUSTOM_SAVE_DATA_OFFSET + SC_LAST_RECEIVED_ITEM_INDEX
            writes_to_perform[address] = (save_last_received_item_index, last_received_item_index, 4)

        if save_last_received_inventory_item_index != last_received_inventory_item_index:
            address = save_pointer + CUSTOM_SAVE_DATA_OFFSET + SC_LAST_RECEIVED_INVENTORY_ITEM_INDEX
            writes_to_perform[address] = (save_last_received_inventory_item_index, last_received_inventory_item_index, 4)

        if not writes_to_perform:
            return

        writes: list[tuple[int, bytes, str]] = []
        writes_guards: list[tuple[int, bytes, str]] = list(global_guards.values())

        for address, values in writes_to_perform.items():
            writes_guards.append((address, values[0].to_bytes(values[2], "little"), BIZHAWK_ARM9_DOMAIN))
            writes.append((address, values[1].to_bytes(values[2], "little"), BIZHAWK_ARM9_DOMAIN))

        await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, writes_guards)

    async def handle_location_checking(self, ctx: "BizHawkClientContext", save_pointer: int, flag_table: bytes, coco_table: bytes, shop_table: bytes):
        new_checks: list[int] = []

        def check_flag(flag_id_to_check: int) -> bool:
            return self.check_flag(flag_table, flag_id_to_check)

        for location_id in ctx.missing_locations:
            location_type = ALL_LOCATIONS_BY_ID[location_id].location_type
            if location_type == EtrianOdysseyLocationType.TREASURE_BOX:
                treasure_data = ALL_TREASURE_BY_LOCATION_ID[location_id]
                floor_number = treasure_data.floor_number - 1
                flag_id = floor_number * 0x10 + treasure_data.chest_id + 0xE00
                if check_flag(flag_id):
                    new_checks.append(location_id)
            elif location_type == EtrianOdysseyLocationType.MISSION_CLEAR:
                mission_data = ALL_MISSION_DATA_BY_LOCATION_ID[location_id]
                if check_flag(mission_data.results_reported_flag_id):
                    new_checks.append(location_id)
            elif location_type == EtrianOdysseyLocationType.CODEX_ENTRY:
                codex_data = CODEX_DATA_BY_LOCATION_ID[location_id]
                if self.check_codex_entry(codex_data.enemy_id, coco_table, reported_only=False):
                    new_checks.append(location_id)
            elif location_type == EtrianOdysseyLocationType.COMPENDIUM_ENTRY:
                compendium_data = COMPENDIUM_BY_LOCATION_ID[location_id]
                if self.check_compendium_entry(compendium_data.item_id, coco_table, reported_only=False):
                    new_checks.append(location_id)
            elif location_type == EtrianOdysseyLocationType.QUEST_COMPLETION:
                quest_data = QUEST_DATA_BY_LOCATION_ID[location_id]
                if check_flag(quest_data.completion_flag):
                    new_checks.append(location_id)
            elif location_type == EtrianOdysseyLocationType.SHOP_ENTRY:
                shop_data = SHOP_UNLOCK_BY_LOCATION_ID[location_id]
                if self.check_shop_entry(shop_data.item_id, shop_table):
                    new_checks.append(location_id)
            else:
                raise NotImplementedError(f"Unknown location type: {location_type}")

        if new_checks:
            await ctx.check_locations(new_checks)

    async def handle_goal(self, ctx: "BizHawkClientContext", codex_table: bytes, flag_table: bytes):
        if ctx.finished_game:
            return

        def check_flag(flag_id_to_check: int) -> bool:
            return self.check_flag(flag_table, flag_id_to_check)

        goal_filled = False
        if self.goal == EO1Goal.defeat_fenrir:
            goal_filled = self.check_codex_entry(EO1Enemies.FENRIR, codex_table, reported_only=False)
        elif self.goal == EO1Goal.defeat_cernunos:
            goal_filled = self.check_codex_entry(EO1Enemies.CERNUNOS, codex_table, reported_only=False)
        elif self.goal == EO1Goal.defeat_cotrangl:
            goal_filled = self.check_codex_entry(EO1Enemies.COTRANGL, codex_table, reported_only=False)
        elif self.goal == EO1Goal.annihilate_the_forest_folk:
            goal_filled = check_flag(MISSION_7_CLEAR_FLAG)
        elif self.goal == EO1Goal.defeat_etreant:
            goal_filled = self.check_codex_entry(EO1Enemies.ETREANT, codex_table, reported_only=False)
        elif self.goal == EO1Goal.defeat_primevil:
            goal_filled = self.check_codex_entry(EO1Enemies.PRIMEVIL, codex_table, reported_only=False)
        elif self.goal == EO1Goal.fully_complete_codex_and_compendium:
            goal_filled = check_flag(TOWN_CROWN_FLAG)
        else:
            raise Exception(f"Goal {self.goal} not implemented")

        if goal_filled:
            ctx.finished_game = True
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def handle_key_item_flags(self, ctx: "BizHawkClientContext", flag_table_save_pointer: int, flag_table: bytes, inventory_table: bytes, global_guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        # This function is to handle flags that get set by events when obtaining key items.
        # This could also be handled within the game itself via assembly, but for now this is how it was chosen to be handled.
        if len(self.key_items_to_process) == 0:
            return

        @dataclass
        class MemoryValues:
            current_value: int
            new_value: int
            value_size: int

        def load_inventory_item(index: int) -> int:
            return int.from_bytes(inventory_table[index * 2:index * 2 + 2], "little")

        def get_flag_byte_offset(flag_id_to_check: int) -> int:
            return math.floor(flag_id_to_check / 8)

        def get_flag_to_set(flag_id_to_check: int) -> int:
            return 1 << (flag_id_to_check % 8)

        inventory_items = [load_inventory_item(i) for i in range(INVENTORY_ITEM_SIZE)]

        memory_values: dict[int, MemoryValues] = {}

        for item_id in inventory_items:
            if item_id not in self.key_items_to_process:
                continue

            key_item_data = KEY_ITEM_DATA_BY_ITEM_ID[item_id]
            if self.check_flag(flag_table, key_item_data.associated_flag):
                self.key_items_to_process.remove(item_id)
                continue

            flag_offset = get_flag_byte_offset(key_item_data.associated_flag)
            flag_value_address = flag_table_save_pointer + flag_offset
            flag_value = flag_table[flag_offset]

            if flag_value_address not in memory_values:
                memory_values[flag_value_address] = MemoryValues(flag_value, flag_value, 1)

            new_flag_value = flag_value | get_flag_to_set(key_item_data.associated_flag)
            memory_values[flag_value_address].new_value = new_flag_value

        writes_to_perform: dict[int, tuple[int, int, int]] = {}

        for address, values in memory_values.items():
            if values.current_value != values.new_value:
                writes_to_perform[address] = (values.current_value, values.new_value, values.value_size)

        if not writes_to_perform:
            return

        writes: list[tuple[int, bytes, str]] = []
        writes_guards: list[tuple[int, bytes, str]] = list(global_guards.values())

        for address, values in writes_to_perform.items():
            writes_guards.append((address, values[0].to_bytes(values[2], "little"), BIZHAWK_ARM9_DOMAIN))
            writes.append((address, values[1].to_bytes(values[2], "little"), BIZHAWK_ARM9_DOMAIN))

        await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, writes_guards)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        if self.goal is None:
            self.goal = EO1Goal(ctx.slot_data[SlotDataKeys.GOAL])

            if bool(ctx.slot_data[SlotDataKeys.QUEST_SANITY]):
                self.quest_completion_reward_hint = bool(ctx.slot_data[SlotDataKeys.QUEST_COMPLETION_REWARD_HINT])
            else:
                self.quest_completion_reward_hint = False

        try:
            read_results = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (SAVE_ADDRESS_STATIC_POINTER_ADDRESS, 4, BIZHAWK_ARM9_DOMAIN),
                    (GAME_STATE_STATIC_ADDRESS, 4, BIZHAWK_ARM9_DOMAIN)
                ])

            save_pointer = int.from_bytes(read_results[0], byteorder='little')
            game_state = int.from_bytes(read_results[1], byteorder='little')

            # No save pointer, can't do anything.
            if save_pointer == 0:
                return

            # Bad game states, we are not in a loaded save.
            if game_state == 0x0 or game_state == 0x1 or game_state == 0x2 or game_state == 0x3 or game_state == 0xF:
                return

            guards: Dict[str, Tuple[int, bytes, str]] = {}
            guards["SAVEDATA_PTR"] = (SAVE_ADDRESS_STATIC_POINTER_ADDRESS, save_pointer.to_bytes(4, "little"), BIZHAWK_ARM9_DOMAIN)
            guards["GAMESTATE"] = (GAME_STATE_STATIC_ADDRESS, game_state.to_bytes(4, "little"), BIZHAWK_ARM9_DOMAIN)
            # todo other validations

            read_results = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (save_pointer + MONEY_VALUE_OFFSET, 4, BIZHAWK_ARM9_DOMAIN),
                    (save_pointer + CUSTOM_SAVE_DATA_OFFSET, CUSTOM_SAVE_DATA_SIZE, BIZHAWK_ARM9_DOMAIN),
                    (save_pointer + FLAG_TABLE_OFFSET, FLAG_TABLE_SIZE, BIZHAWK_ARM9_DOMAIN),
                    (save_pointer + COMPENDIUM_CODEX_TABLE_OFFSET, COMPENDIUM_CODEX_TABLE_SIZE, BIZHAWK_ARM9_DOMAIN),
                    (save_pointer + INVENTORY_START_OFFSET, INVENTORY_ITEM_SIZE * 2, BIZHAWK_ARM9_DOMAIN),
                    (save_pointer + SHOP_ITEM_FLAG_TABLE_OFFSET, SHOP_ITEM_FLAG_TABLE_SIZE, BIZHAWK_ARM9_DOMAIN),
                ],
                list(guards.values())
            )

            if read_results is None:
                return

            await self.handle_received_items(ctx, save_pointer, read_results[0], read_results[1], guards)
            await self.handle_location_checking(ctx, save_pointer, read_results[2], read_results[3], read_results[5])
            await self.handle_goal(ctx, read_results[3], read_results[2])

            await self.handle_key_item_flags(ctx, save_pointer + FLAG_TABLE_OFFSET, read_results[2], read_results[4], guards)

            await self.handle_scout(ctx, save_pointer, game_state, guards)

            await self.process_custom_commands(ctx, save_pointer + FLAG_TABLE_OFFSET, read_results[2], guards)
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def get_quest_scout(self, ctx: "BizHawkClientContext", save_pointer: int, game_state: int, global_guards: Dict[str, Tuple[int, bytes, str]]) -> list[int]:
        if game_state != 0x09:
            return []

        guards: Dict[str, Tuple[int, bytes, str]] = {}
        guards.update(global_guards)

        read_results = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (OBJECT_0X15_STATIC_POINTER, 4, BIZHAWK_ARM9_DOMAIN)
            ], list(guards.values()))

        if read_results is None:
            return []

        # Read the static object pointer.
        obj0x15_pointer = int.from_bytes(read_results[0], byteorder='little')

        if obj0x15_pointer == 0:
            return []

        guards["OBJ0x15_POINTER"] = (OBJECT_0X15_STATIC_POINTER, obj0x15_pointer.to_bytes(4, "little"), BIZHAWK_ARM9_DOMAIN)

        quest_window_obj_addr = obj0x15_pointer + GENERIC_OBJECT_HEADER_SIZE
        # Read the instance pointer.
        read_results = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (quest_window_obj_addr + QUEST_WINDOW_OBJ_QUEST_ARRAY_OFFSET, 2 * 5, BIZHAWK_ARM9_DOMAIN),
                (quest_window_obj_addr + QUEST_WINDOW_OBJ_CURRENT_QUEST_INDEX_OFFSET, 4, BIZHAWK_ARM9_DOMAIN),
            ], list(guards.values()))

        if read_results is None:
            return []

        quest_index = int.from_bytes(read_results[1], byteorder='little')

        read_results = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (quest_window_obj_addr + QUEST_WINDOW_OBJ_QUEST_ARRAY_OFFSET, 2 * (quest_index + 1), BIZHAWK_ARM9_DOMAIN),
                (quest_window_obj_addr + QUEST_WINDOW_OBJ_CURRENT_QUEST_INDEX_OFFSET, 4, BIZHAWK_ARM9_DOMAIN),
            ], list(guards.values()))

        if read_results is None:
            return []

        quest_index = int.from_bytes(read_results[1], byteorder='little')
        quest_id = int.from_bytes(read_results[0][quest_index * 2:quest_index * 2 + 2], "little")

        if quest_id not in QUEST_DATA_BY_QUEST_ID:
            return []

        location_id = QUEST_DATA_BY_QUEST_ID[quest_id].location_id

        if location_id not in ctx.missing_locations:
            return []

        return [location_id]

    async def handle_scout(self, ctx: "BizHawkClientContext", save_pointer: int, game_state: int, guards: Dict[str, Tuple[int, bytes, str]]):
        locations_to_scout: set[int] = set()
        if self.quest_completion_reward_hint:
            locations_to_scout.update(await self.get_quest_scout(ctx, save_pointer, game_state, guards))

        if len(locations_to_scout) > 0:
            locations_to_scout.difference_update(self.scouted_locations)
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": locations_to_scout, "create_as_hint": 2}])
            self.scouted_locations.update(locations_to_scout)

    async def process_custom_commands(self,
                                      ctx: "BizHawkClientContext",
                                      flag_table_save_pointer: int,
                                      flag_table: bytes,
                                      global_guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        def get_flag_byte_offset(flag_id_to_check: int) -> int:
            return math.floor(flag_id_to_check / 8)

        def get_flag_to_set(flag_id_to_check: int) -> int:
            return 1 << (flag_id_to_check % 8)

        if self.custom_command_to_run == EtrianOdysseyClientCustomCommands.NONE:
            return

        if self.custom_command_to_run == EtrianOdysseyClientCustomCommands.DEBUG_EO_SET_FLAG_OFF:
            writes: list[tuple[int, bytes, str]] = []
            writes_guards: list[tuple[int, bytes, str]] = list(global_guards.values())

            flag_offset = get_flag_byte_offset(self.custom_command_parameter)
            flag_value_address = flag_table_save_pointer + flag_offset
            flag_value = flag_table[flag_offset]

            new_flag_value = flag_value & (0xFF ^ get_flag_to_set(self.custom_command_parameter))

            writes_guards.append((flag_value_address, flag_value.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN))
            writes.append((flag_value_address, new_flag_value.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN))

            await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, writes_guards)
        elif self.custom_command_to_run == EtrianOdysseyClientCustomCommands.DEBUG_EO_SET_FLAG_ON:
            writes: list[tuple[int, bytes, str]] = []
            writes_guards: list[tuple[int, bytes, str]] = list(global_guards.values())

            flag_offset = get_flag_byte_offset(self.custom_command_parameter)
            flag_value_address = flag_table_save_pointer + flag_offset
            flag_value = flag_table[flag_offset]

            new_flag_value = flag_value | get_flag_to_set(self.custom_command_parameter)

            writes_guards.append((flag_value_address, flag_value.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN))
            writes.append((flag_value_address, new_flag_value.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN))

            await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, writes_guards)
        elif self.custom_command_to_run == EtrianOdysseyClientCustomCommands.DEBUG_EO_WRITE_RAW:
            await bizhawk.write(ctx.bizhawk_ctx, [(self.custom_command_parameter[0], int(self.custom_command_parameter[2]).to_bytes(self.custom_command_parameter[1], "little"), BIZHAWK_ARM9_DOMAIN)])
        else:
            raise Exception(f"Unknown custom_command_to_run: {self.custom_command_to_run}")

        self.custom_command_to_run = EtrianOdysseyClientCustomCommands.NONE
        self.custom_command_parameter = None
