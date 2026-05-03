# TODO this is a "work in progress" and is mostly used as an interactive test for Sustain.

from worlds.etrian_odyssey.logic.ClassProcessor import ClassProcessor
from worlds.etrian_odyssey.logic.SustainProcessor import *
from worlds.etrian_odyssey.logic.LogicData import *
from worlds.etrian_odyssey.data.InventoryItemData import *


def get_score(logic_data: AllLogicData, items: list[int], level = None) -> int:
    data = logic_data.copy()

    if level is not None:
        data.current_level_cap = level

    for item in items:
        data.shop_unlock_logic_data.non_unlockable_shop_items.remove(item)
        data.shop_unlock_logic_data.unlockable_shop_items.add(item)

    processor = SustainProcessor()
    return processor.get_current_sustain_score(data)

def get_skill_score(logic_data: AllLogicData, skills: list[int], level = None) -> int:
    data = logic_data.copy()
    class_processor = ClassProcessor(1)
    for class_data in data.class_data.class_as_list:
        class_data.class_unlocked = True

    class_dict = data.class_data.class_as_dict

    for skill in skills:
        skill_data = SKILL_DATA_BY_ID[skill]
        class_dict[skill_data.class_name].class_skills[skill].skill_usable = True

    if level is not None:
        data.current_level_cap = level

    processor = SustainProcessor()
    return processor.get_current_sustain_score(data)

def get_skill_score_plus(logic_data: AllLogicData, skills: list[int]) -> str:
    return (f"{get_skill_score(logic_data, skills, 5)},"
            f"{get_skill_score(logic_data, skills, 11)},"
            f"{get_skill_score(logic_data, skills, 20)},"
            f"{get_skill_score(logic_data, skills, 30)},"
            f"{get_skill_score(logic_data, skills, 50)},"
            f"{get_skill_score(logic_data, skills, 70)}")




def test():
    logic_data = AllLogicData(fill_default=True)
    class_processor = ClassProcessor(1)
    class_processor.initialize_data(logic_data.class_data, remove_skills_requirements=True)

    print(get_score(logic_data, [EO1ItemID.MEDICA, EO1ItemID.AMRITA]))
    print(get_score(logic_data, [EO1ItemID.MEDICA, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_III, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_IV, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_V, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA], 10))
    print(get_score(logic_data, [EO1ItemID.MEDICA_V, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA], 30))
    print(get_score(logic_data, [EO1ItemID.MEDICA_V, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA], 50))
    print(get_score(logic_data, [EO1ItemID.MEDICA_V, EO1ItemID.MEDICA_II, EO1ItemID.AMRITA], 70))
    print(get_score(logic_data, [EO1ItemID.MEDICA, EO1ItemID.AMRITA_II]))
    print(f"Medica:{get_score(logic_data, [EO1ItemID.MEDICA])}")
    print(f"Medica2:{get_score(logic_data, [EO1ItemID.MEDICA_II])}")
    print(f"Medica3:{get_score(logic_data, [EO1ItemID.MEDICA_III])}")
    print(f"Medica4:{get_score(logic_data, [EO1ItemID.MEDICA_IV])}")
    print(f"Hamao:{get_score(logic_data, [EO1ItemID.HAMAO])}")
    print(f"HamaoPrime:{get_score(logic_data, [EO1ItemID.HAMAOPRIME])}")
    print(f"Soma:{get_score(logic_data, [EO1ItemID.SOMA])}")
    print(f"SomaPrime:{get_score(logic_data, [EO1ItemID.SOMAPRIME])}")
    print(get_score(logic_data, [EO1ItemID.NECTAR]))
    print(get_score(logic_data, [EO1ItemID.NECTAR_II]))
    print(get_score(logic_data, [EO1ItemID.NECTAR_III]))


    print(f"Soma+Medica1:{get_score(logic_data, [EO1ItemID.SOMA, EO1ItemID.MEDICA])}")
    print(f"Soma+Medica2:{get_score(logic_data, [EO1ItemID.SOMA, EO1ItemID.MEDICA_II])}")
    print(f"Soma+Medica3:{get_score(logic_data, [EO1ItemID.SOMA, EO1ItemID.MEDICA_III])}")
    print(f"Soma+Medica4:{get_score(logic_data, [EO1ItemID.SOMA, EO1ItemID.MEDICA_IV])}")

    print(get_score(logic_data, [EO1ItemID.AMRITA_II, EO1ItemID.HAMAO]))
    print(get_score(logic_data, [EO1ItemID.HAMAO]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_III, EO1ItemID.AMRITA_II, EO1ItemID.SOMA, EO1ItemID.HAMAO]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_IV, EO1ItemID.AMRITA_II, EO1ItemID.SOMA, EO1ItemID.HAMAO]))
    print(get_score(logic_data, [EO1ItemID.MEDICA_IV, EO1ItemID.AMRITA_II, EO1ItemID.SOMA, EO1ItemID.HAMAO, EO1ItemID.NECTAR]))

    print(f"S2?:{get_score(logic_data, [EO1ItemID.MEDICA_III, EO1ItemID.AMRITA, EO1ItemID.NECTAR])}")
    print(f"S4:{get_score(logic_data, [EO1ItemID.MEDICA_III, EO1ItemID.AMRITA_II, EO1ItemID.NECTAR, EO1ItemID.SOMA])}")


    print ("Skills:")
    print("PCure: " + get_skill_score_plus(logic_data, [EO1Skills.PROTECTOR_CURE]))
    print("PCure2: " + get_skill_score_plus(logic_data, [EO1Skills.PROTECTOR_CURE_II]))
    print("RIbuki: " + get_skill_score_plus(logic_data, [EO1Skills.RONIN_IBUKI]))
    print("ATPRegen: " + get_skill_score_plus(logic_data, [EO1Skills.ALCHEMIST_TP_REGEN]))
    print("THealing: " + get_skill_score_plus(logic_data, [EO1Skills.TROUBADOUR_HEALING]))
    print("TRelaxing: " + get_skill_score_plus(logic_data, [EO1Skills.TROUBADOUR_RELAXING]))

    print("MCure: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_CURE]))
    print("MCure2: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_CURE_II]))
    print("MCure3: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_CURE_III]))
    print("MSalve: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_SALVE]))
    print("MSalve2: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_SALVE_II]))
    print("MRevive: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_REVIVE]))
    print("MRegen: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_REGEN]))
    print("MPatchUp: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_PATCH_UP]))
    print("MTPRegen: " + get_skill_score_plus(logic_data, [EO1Skills.MEDIC_TP_REGEN]))



    pass


def validate_regions():
    for region in ALL_REGION_DATA:
        if region.floor_number > 30:
            raise Exception(f"Region {region.name} is greater than 30")


#validate_regions()
#test()