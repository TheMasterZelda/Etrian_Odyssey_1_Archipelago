from .StateInterface import StateInterface
from ..data.CompendiumData import *
from ..data.EnemyData import *
from ..data.GatheringSpotData import *
from ..data.SkillData import *

from .LogicData import *
from .ConditionalDropProcessor import *


TAKE_GATHERING_SKILLS: list[int] = [
    EO1Skills.SURVIVALIST_TAKE,
    EO1Skills.DARK_HUNTER_TAKE,
    EO1Skills.TROUBADOUR_TAKE
]
MINE_GATHERING_SKILLS: list[int] = [
    EO1Skills.LANDSKNECHT_MINE,
    EO1Skills.SURVIVALIST_MINE,
    EO1Skills.PROTECTOR_MINE,
    EO1Skills.RONIN_MINE,
    EO1Skills.HEXER_MINE
]
CHOP_GATHERING_SKILLS: list[int] = [
    EO1Skills.SURVIVALIST_CHOP,
    EO1Skills.MEDIC_CHOP,
    EO1Skills.ALCHEMIST_CHOP
]

class CompendiumProcessor:
    max_stratum: int
    conditional_drop_processor: ConditionalDropProcessor
    region_cache: set[str] | None

    def __init__(self, max_stratum: int, conditional_drop_processor: ConditionalDropProcessor):
        self.max_stratum = max_stratum
        self.conditional_drop_processor = conditional_drop_processor
        self.region_cache = None

    def can_fill_compendium_entry(self, item_id: int, state: StateInterface, logic_data: AllLogicData) -> bool:
        if self.region_cache is None:
            self.region_cache = set(state.get_regions())

        compendium_entry = COMPENDIUM_BY_ITEM_ID[item_id]

        if compendium_entry.source == CompendiumSource.MONSTER:
            return self.__can_fill_monster_entry(compendium_entry, state, logic_data)
        elif compendium_entry.source == CompendiumSource.GATHERING:
            return self.__can_fill_gathering_entry(compendium_entry, state, logic_data)
        elif compendium_entry.source == CompendiumSource.BOTH:
            return self.__can_fill_both_entry(compendium_entry, state, logic_data)
        else:
            raise Exception(f"Unknown compendium source: {compendium_entry.source}")

    def __can_fill_monster_entry(self, compendium_data: CompendiumData, state: StateInterface, logic_data: AllLogicData) -> bool:
        for enemy_id in ENEMY_BY_DROP_ID[compendium_data.item_id]:
            if enemy_id not in logic_data.codex_logic_data.fillable_codex_entries:
                continue
            enemy_data = ENEMY_BY_ID[enemy_id]
            has_conditional_drop = enemy_data.item_drop_3 != 0
            if has_conditional_drop:
                has_conditional_drop = enemy_data.drop_condition != DropCondition.NONE # Handles "Rare drop" conditionals.

            # If the monster has no conditional drop, then all its drops are fillable.
            if not has_conditional_drop:
                return True

            # Otherwise, conditional drops can nullify regular drops.
            if enemy_data.item_drop_1 == compendium_data.item_id:
                if self.conditional_drop_processor.can_defeat_without_fulfilling_drop_condition(enemy_id, logic_data):
                    return True
            elif enemy_data.item_drop_2 == compendium_data.item_id:
                if self.conditional_drop_processor.can_defeat_without_fulfilling_drop_condition(enemy_id, logic_data):
                    return True
            elif enemy_data.item_drop_3 == compendium_data.item_id:
                if self.conditional_drop_processor.can_fulfill_drop_condition(enemy_id, logic_data, state):
                    return True
            else:
                raise Exception(f"Enemy {enemy_id} cannot drop item {compendium_data.item_id}.")

        return False

    def __can_fill_gathering_entry(self, compendium_data: CompendiumData, state: StateInterface, logic_data: AllLogicData) -> bool:
        for gathering_spot_unique_id in GATHERING_SPOT_BY_ITEM_ID[compendium_data.item_id]:
            gathering_spot_data = GATHERING_SPOT_BY_UNIQUE_ID[gathering_spot_unique_id]

            # Skip regions not in the seed (depending on goal).
            if gathering_spot_data.region not in self.region_cache:
                continue

            # Cannot use the required gathering skill yet.
            if not self.__can_use_gathering_skill(gathering_spot_data.gather_type, state, logic_data):
                continue

            # If player can both use the gathering skill and reach the region.
            # Optimization: Doing a floor number check is much, much faster than doing a "can_reach_region" check.
            region_data = ALL_REGION_DATA_BY_NAME[gathering_spot_data.region]
            if region_data.floor_number > logic_data.current_floor_limit:
                continue
            if state.can_reach_region(gathering_spot_data.region):
                return True

        return False


    def __can_fill_both_entry(self, compendium_data: CompendiumData, state: StateInterface, logic_data: AllLogicData) -> bool:
        if self.__can_fill_monster_entry(compendium_data, state, logic_data):
            return True
        if self.__can_fill_gathering_entry(compendium_data, state, logic_data):
            return True
        return False

    def __can_use_gathering_skill(self, gather_type: EO1GatherType, state: StateInterface, logic_data: AllLogicData) -> bool:
        def can_use_any(gathering_skill_list: list[int], skills: dict[int, SkillLogicData]) -> bool:
            for gathering_skill in gathering_skill_list:
                if gathering_skill not in skills:
                    continue

                if skills[gathering_skill].skill_usable:
                    return True
            return False

        for class_data in logic_data.class_data.unlocked_classes:
            class_skills = class_data.class_skills

            if gather_type == EO1GatherType.CHOP:
                if can_use_any(CHOP_GATHERING_SKILLS, class_skills):
                    return True
            elif gather_type == EO1GatherType.MINE:
                if can_use_any(MINE_GATHERING_SKILLS, class_skills):
                    return True
            elif gather_type == EO1GatherType.TAKE:
                if can_use_any(TAKE_GATHERING_SKILLS, class_skills):
                    return True
            else:
                raise Exception(f"Unknown gather type: {gather_type}")

        return False