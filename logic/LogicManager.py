from .ILogicManager import ILogicManager, ExecutionContext
from .ClassProcessor import *
from .LogicCacheData import LogicCacheData, AllLogicCacheData
from .LogicCacheDataManager import DualIntSetLogicCacheDataManager
from .SustainProcessor import SustainProcessor, NoSustainProcessor
from .SingleEnemyBattleProcessor import *
from .EncounterBattleProcessor import *
from .EncounterGroupBattleProcessor import *
from .CodexProcessor import *
from .CompendiumProcessor import *
from .ConditionalDropProcessor import *
from .ShopUnlockProcessor import *
from .QuestProcessor import QuestProcessor
from .simplified_logic.SimplifiedSingleEnemyBattleProcessor import SimplifiedSingleEnemyBattleProcessor
from ..Items import EtrianOdysseyItemType
from ..data.ItemData import ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID, ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID


class EO1ExecutionContext(ExecutionContext):
    pass

class LogicManager(ILogicManager):
    # Processors.
    class_processor: ClassProcessor
    enemy_battle_processor: SingleEnemyBattleProcessor
    encounter_battle_processor: EncounterBattleProcessor
    encounter_group_battle_processor: EncounterGroupBattleProcessor
    codex_processor: CodexProcessor
    compendium_processor: CompendiumProcessor
    conditional_drop_processor: ConditionalDropProcessor
    shop_unlock_processor: ShopUnlockProcessor
    sustain_processor: SustainProcessor
    quest_processor: QuestProcessor

    def __init__(self, options: EtrianOdysseyOptions, data_source: EtrianOdysseyDataSource):
        max_stratum = get_max_stratum_for_goal(EO1Goal(options.goal.value))

        self.class_processor = ClassProcessor(data_source)
        self.enemy_battle_processor = self.__create_single_enemy_battle_processor_from_options(options)
        self.encounter_battle_processor = self.__create_encounter_battle_processor_from_options(options)
        self.encounter_group_battle_processor = self.__create_encounter_group_battle_processor_from_options(options)
        self.quest_processor = QuestProcessor()
        self.codex_processor = CodexProcessor(max_stratum)
        self.conditional_drop_processor = ConditionalDropProcessor(self.enemy_battle_processor)
        self.compendium_processor = CompendiumProcessor(max_stratum, self.conditional_drop_processor)
        self.shop_unlock_processor = ShopUnlockProcessor()
        self.sustain_processor = SustainProcessor()

    # todo move the processor creation to a dedicated file.
    @staticmethod
    def __create_single_enemy_battle_processor_from_options(options: EtrianOdysseyOptions) -> SingleEnemyBattleProcessor:
        battle_logic_mode_type = BattleLogicModeType(options.battle_logic_mode.value)
        if battle_logic_mode_type == BattleLogicModeType.no_logic:
            return NoLogicSingleEnemyBattleProcessor()
        elif battle_logic_mode_type == BattleLogicModeType.level_only:
            return LevelOnlySingleEnemyBattleProcessor()
        elif battle_logic_mode_type == BattleLogicModeType.simplified:
            return SimplifiedSingleEnemyBattleProcessor()

        raise Exception("Not implemented")

    @staticmethod
    def __create_encounter_battle_processor_from_options(options: EtrianOdysseyOptions) -> EncounterBattleProcessor:
        return SimpleEncounterBattleProcessor()

    @staticmethod
    def __create_encounter_group_battle_processor_from_options(options: EtrianOdysseyOptions) -> EncounterGroupBattleProcessor:
        return SimpleEncounterGroupBattleProcessor()

    def initialize_data(self, logic_data: AllLogicData, options: EtrianOdysseyOptions):
        logic_data.current_level_cap = options.get_effective_initial_level_cap()
        logic_data.current_floor_limit = options.get_effective_initial_floor_limit()
        self.class_processor.initialize_data(logic_data.class_data)

    def initialize_cache(self, cache_data: AllLogicCacheData):
        for enemy_data in ALL_ENEMIES:
            cache_data.defeatable_enemy.unaccessible.add(enemy_data.enemy_id)
            cache_data.survivable_enemy.unaccessible.add(enemy_data.enemy_id)

        for encounter_data in ALL_ENCOUNTERS:
            cache_data.defeatable_encounter.unaccessible.add(encounter_data.encounter_id)
            cache_data.survivable_encounter.unaccessible.add(encounter_data.encounter_id)

        for encounter_group_data in ALL_ENCOUNTER_GROUPS:
            cache_data.encounter_group.unaccessible.add(encounter_group_data.encounter_group_id)

        for codex_data in ALL_CODEX_ENTRIES:
            cache_data.codex_entry.unaccessible.add(codex_data.enemy_id)

        for compendium_data in COMPENDIUM_TABLE:
            cache_data.compendium_entry.unaccessible.add(compendium_data.item_id)

        for item_compound_data in ITEM_COMPOUND_TABLE:
            # Warp wires are a special kind of unlock item handled differently.
            if item_compound_data.item_id == EO1ItemID.WARP_WIRE:
                continue
            cache_data.shop_unlock_entry.unaccessible.add(item_compound_data.item_id)

    def on_item_collect(self, item_id: int, item_type: EtrianOdysseyItemType, context: EO1ExecutionContext) -> None:
        # Don't restrict to max value, so we support remove properly too.
        if item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            context.logic_data.current_level_cap += ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item_id].level_amount
            context.logic_data.set_skill_stale()
            context.cache_data.set_battle_stale()
        elif item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            context.logic_data.current_floor_limit += ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item_id].floor_amount
            context.logic_data.set_skill_stale() # Because of the soft level cap.
            context.cache_data.set_battle_stale()
            context.cache_data.set_location_stale()
        elif item_type == EtrianOdysseyItemType.CLASS:
            context.logic_data.set_skill_stale()
            context.cache_data.set_battle_stale()
        elif item_type == EtrianOdysseyItemType.INVENTORY:
            item_type = ITEM_PER_AP_ITEM_ID[item_id].type
            if item_type == EO1ItemType.Key or item_type == EO1ItemType.Quest:
                context.cache_data.set_location_stale()
        elif item_type == EtrianOdysseyItemType.SKILL:
            context.logic_data.set_skill_stale() # TODO ? Don't automatically set battle as stale, it will be done if there is a change.
            context.cache_data.set_battle_stale()
        elif item_type == EtrianOdysseyItemType.EVENT:
            context.cache_data.set_battle_stale()
            context.cache_data.set_location_stale()

        #floor_ = 1
        #for floor_limit in ALL_PROGRESSIVE_FLOOR_LIMIT:
        #    count = state.count(floor_limit.name, 1)
        #    floor_ += floor_limit.floor_amount * count

        #if floor_ != self.logic_data.current_floor_limit:
        #    raise Exception("not match")

    def on_item_remove(self, item_id: int, item_type: EtrianOdysseyItemType, context: EO1ExecutionContext) -> None:
        if item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            context.logic_data.current_level_cap -= ALL_PROGRESSIVE_LEVEL_CAP_BY_ITEM_ID[item_id].level_amount
        elif item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            context.logic_data.current_floor_limit -= ALL_PROGRESSIVE_FLOOR_BY_ITEM_ID[item_id].floor_amount

        def __recalculate_class_data() -> bool:
            changed = self.class_processor.recalculate_class_data(context.logic_data, context.state)
            context.logic_data.class_data.set_stale(True)
            return changed

        def __recalculate_sustain_score():
            context.cache_data.sustain_score.value = self.sustain_processor.get_current_sustain_score(context)
            context.cache_data.sustain_score.set_stale(True)

        def recalculate_battle():
            # Recalculate all battle related state data
            __recalculate_class_data()
            __recalculate_sustain_score()
            cache_manager = self.__get_defeatable_enemy_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_survivable_enemy_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_defeatable_encounter_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_survivable_encounter_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_encounter_group_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_codex_entry_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_compendium_entry_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_shop_unlock_entry_cache_manager(context)
            cache_manager.recalculate(context)

        def recalculate_location():
            __recalculate_sustain_score()
            cache_manager = self.__get_codex_entry_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_compendium_entry_cache_manager(context)
            cache_manager.recalculate(context)
            cache_manager = self.__get_shop_unlock_entry_cache_manager(context)
            cache_manager.recalculate(context)

        def recalculate_skill():
            __recalculate_class_data()
            __recalculate_sustain_score()

        context.cache_data.set_update_suspended(True)

        # Do the remove recalculations directly here.
        # If this become too costly, split the stale variable into positive and negative recalculation.
        if item_type == EtrianOdysseyItemType.PROGRESSIVE_LEVEL_CAP:
            recalculate_battle()
        elif item_type == EtrianOdysseyItemType.CLASS:
            recalculate_battle()
        elif item_type == EtrianOdysseyItemType.PROGRESSIVE_FLOOR_LIMIT:
            recalculate_battle()
            recalculate_location()
        elif item_type == EtrianOdysseyItemType.INVENTORY:
            item_type = ITEM_PER_AP_ITEM_ID[item_id].type
            if item_type == EO1ItemType.Key or item_type == EO1ItemType.Quest:
                recalculate_location()
        elif item_type == EtrianOdysseyItemType.SKILL:
            recalculate_skill()
            recalculate_battle()
            recalculate_location()
        elif item_type == EtrianOdysseyItemType.EVENT:
            recalculate_location()

        context.cache_data.set_update_suspended(False)

    def on_reached_region(self, region_name: str, context: EO1ExecutionContext):
        context.cache_data.sustain_score.set_stale(True)

    def on_ut_glitch_logic(self, context: EO1ExecutionContext):
        self.enemy_battle_processor = NoLogicSingleEnemyBattleProcessor()
        self.sustain_processor = NoSustainProcessor()

    def __get_defeatable_enemy_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.defeatable_enemy, self.enemy_battle_processor.can_defeat_enemy)
    def __get_survivable_enemy_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.survivable_enemy, self.enemy_battle_processor.can_survive_enemy)

    def __get_defeatable_encounter_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.defeatable_encounter, self.encounter_battle_processor.can_defeat_encounter)
    def __get_survivable_encounter_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.survivable_encounter, self.encounter_battle_processor.can_survive_encounter)

    def __get_encounter_group_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.encounter_group, self.encounter_group_battle_processor.can_survive_encounter_group)

    def __get_codex_entry_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.codex_entry, self.codex_processor.can_fill_codex_entry)
    def __get_compendium_entry_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.compendium_entry, self.compendium_processor.can_fill_compendium_entry)
    def __get_shop_unlock_entry_cache_manager(self, context: EO1ExecutionContext) -> DualIntSetLogicCacheDataManager:
        return DualIntSetLogicCacheDataManager(context.cache_data.shop_unlock_entry, self.shop_unlock_processor.can_unlock_item)

    def __update_class_data(self, context: EO1ExecutionContext) -> None:
        if context.logic_data.class_data.is_stale():
            if self.class_processor.update_class_data(context.logic_data, context.state):
                context.logic_data.set_battle_stale()
                context.cache_data.set_battle_stale()
            context.logic_data.class_data.set_stale(False)

    def __update_sustain_score(self, context: EO1ExecutionContext) -> None:
        if context.cache_data.sustain_score.is_stale():
            sustain_score = self.sustain_processor.get_current_sustain_score(context)
            context.cache_data.sustain_score.value = sustain_score
            context.cache_data.sustain_score.set_stale(False)

    def can_defeat_enemy(self, enemy_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_defeatable_enemy_cache_manager(context)
        return cache_manager.is_accessible(enemy_id, context)

    def can_defeat_encounter(self, encounter_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_defeatable_encounter_cache_manager(context)
        return cache_manager.is_accessible(encounter_id, context)

    def can_defeat_special_encounter(self, enemies: list[int], context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        return self.encounter_battle_processor.can_defeat_enemy_group(enemies, context)

    def can_survive_enemy(self, enemy_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_survivable_enemy_cache_manager(context)
        return cache_manager.is_accessible(enemy_id, context)

    def can_survive_encounter(self, encounter_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_survivable_encounter_cache_manager(context)
        return cache_manager.is_accessible(encounter_id, context)

    def can_survive_encounter_group(self, encounter_group_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_encounter_group_cache_manager(context)
        return cache_manager.is_accessible(encounter_group_id, context)

    def can_unlock_shop_item(self, shop_item_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_shop_unlock_entry_cache_manager(context)
        return cache_manager.is_accessible(shop_item_id, context)

    def can_fill_compendium_entry(self, item_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_compendium_entry_cache_manager(context)
        return cache_manager.is_accessible(item_id, context)

    def can_fill_codex_entry(self, enemy_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        cache_manager = self.__get_codex_entry_cache_manager(context)
        return cache_manager.is_accessible(enemy_id, context)

    def get_fillable_codex_entry_count(self, context: EO1ExecutionContext) -> int:
        self.__update_class_data(context)
        cache_manager = self.__get_codex_entry_cache_manager(context)
        cache_manager.update_all(context)
        return len(cache_manager.cache_data.accessible)

    def get_fillable_compendium_entry_count(self, context: EO1ExecutionContext) -> int:
        self.__update_class_data(context)
        cache_manager = self.__get_compendium_entry_cache_manager(context)
        cache_manager.update_all(context)
        return len(cache_manager.cache_data.accessible)

    def can_start_quest(self, quest_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        return self.quest_processor.can_start_quest(quest_id, context)

    def can_complete_quest(self, quest_id: int, context: EO1ExecutionContext) -> bool:
        self.__update_class_data(context)
        return self.quest_processor.can_complete_quest(quest_id, context)

    def can_sustain_region(self, region_sustain_score: int, context: EO1ExecutionContext) -> bool:
        # Optimization: Skip sustain check if the region requires none.
        if region_sustain_score == 0:
            return True

        self.__update_sustain_score(context)
        sustain_score = context.cache_data.sustain_score.value
        return sustain_score >= region_sustain_score