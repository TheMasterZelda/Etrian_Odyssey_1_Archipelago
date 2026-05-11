import unittest

from ...logic.SkillHelper import *
from ...data.SkillData import *

class SkillHelper(unittest.TestCase):

    def test_is_not_physical_damage_type(self):

        def assert_false(skill_id: int):
            skill_data = SKILL_DATA_BY_ID[skill_id]
            self.assertFalse(is_not_physical_damage_type(skill_data), f"Skill {skill_data.get_full_name()} should not be Not Physical")

        def assert_true(skill_id: int):
            skill_data = SKILL_DATA_BY_ID[skill_id]
            self.assertTrue(is_not_physical_damage_type(skill_data), f"Skill {skill_data.get_full_name()} should be Not Physical")

        assert_false(EO1Skills.LANDSKNECHT_HP_UP)
        assert_false(EO1Skills.LANDSKNECHT_AXES)
        assert_false(EO1Skills.LANDSKNECHT_2_HIT)
        assert_false(EO1Skills.HEXER_MINE)
        assert_false(EO1Skills.LANDSKNECHT_WAR_CRY)
        assert_false(EO1Skills.LANDSKNECHT_ARM_HEAL)
        assert_false(EO1Skills.LANDSKNECHT_CRUSH)
        assert_false(EO1Skills.LANDSKNECHT_BLAZER)
        assert_false(EO1Skills.SURVIVALIST_TRICKERY)
        assert_false(EO1Skills.SURVIVALIST_QUICKEN)
        assert_false(EO1Skills.HEXER_BLINDING)
        assert_false(EO1Skills.HEXER_SAPPING)
        assert_true(EO1Skills.ALCHEMIST_FIRE)
        assert_true(EO1Skills.ALCHEMIST_FLAME)
        assert_true(EO1Skills.ALCHEMIST_INFERNO)
        assert_true(EO1Skills.ALCHEMIST_ICE)
        assert_true(EO1Skills.ALCHEMIST_FREEZE)
        assert_true(EO1Skills.ALCHEMIST_COCYTUS)
        assert_true(EO1Skills.ALCHEMIST_VOLT)
        assert_true(EO1Skills.ALCHEMIST_THUNDER)
        assert_true(EO1Skills.ALCHEMIST_THOR)

