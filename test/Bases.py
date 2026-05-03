import unittest
from test.bases import WorldTestBase

from ..Constant import *

from ..World import EtrianOdysseyWorld

class EtrianOdysseyTestBase(WorldTestBase):
    game = GAME_NAME
    world: EtrianOdysseyWorld


    def generate_patch_raw_data(self):
        from ..Patch import generate_output

        # This is copied from WorldTestBase.test_fill
        from Fill import distribute_items_restrictive
        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            from worlds.AutoWorld import call_all
            call_all(self.multiworld, "post_fill")
            call_all(self.multiworld, "finalize_multiworld")
            placed_items = [loc.item for loc in self.multiworld.get_locations() if loc.item and loc.item.code]
            self.assertLessEqual(len(self.multiworld.itempool), len(placed_items),"Unplaced Items remaining in itempool")
        # ------

        return generate_output(self.world)

    def test_generate_patch(self):
        # For now, we can't test the patch output effectively, but when it becomes handled by the apworld, implement it.
        self.generate_patch_raw_data()

    #def setUp(self) -> None:
    #    if self.auto_construct:
    #        self.world_setup(seed=20586521702883398726)

    #options = {
        # General
    #    OptionKeys.GOAL: EO1Goal.defeat_etreant.value,
    #    OptionKeys.BATTLE_LOGIC_MODE: BattleLogicModeType.no_logic.value,
    #    OptionKeys.BATTLE_LOGIC_DIFFICULTY: BattleLogicDifficultyType.normal.value,

        # Level Caps
    #    OptionKeys.LEVEL_CAP_MODE: LevelCapMode.option_none,
    #    OptionKeys.INITIAL_LEVEL_CAP: 5,
    #    OptionKeys.LEVEL_CAP_INCREASE_VALUE: 4,
    #    OptionKeys.EXTRA_PROGRESSIVE_LEVEL_CAP_ITEMS: 0,

        # Floor Limits
    #    OptionKeys.FLOOR_LIMIT_MODE: LevelCapMode.option_none,
    #    OptionKeys.INITIAL_FLOOR_LIMIT: 1,
    #    OptionKeys.FLOOR_LIMIT_INCREASE_VALUE: 1,
    #    OptionKeys.EXTRA_PROGRESSIVE_FLOOR_LIMIT: 0,

        # Class
    #    OptionKeys.CLASS_SANITY_MODE: LevelCapMode.option_none,
    #    OptionKeys.STARTING_CLASS_COUNT: 1,

        # Skills
    #    OptionKeys.SKILL_SANITY_MODE: LevelCapMode.option_none,
    #    OptionKeys.SHUFFLE_GENERIC_STATS_INCREASE_SKILLS: False,
    #    OptionKeys.SHUFFLE_GATHERING_SKILLS: False,

        # Codex
    #    OptionKeys.CODEX_SANITY: False,

        # Compendium
    #    OptionKeys.COMPENDIUM_SANITY: False,
    #}


# The creation of multiworlds for use in tests is usually pretty quick, the test multiworlds typically only run the steps before fill. There are
# setup_solo_multiworld and setup_multiworld helpers for tests if you want to use them directly. You can control the steps that get run too, so
# you can run only up to generate_early or whatever is the latest run step that you need.

# They have docstrings. They're in test/general/__init__