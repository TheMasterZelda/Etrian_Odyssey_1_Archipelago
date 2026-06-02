from typing import TYPE_CHECKING, NamedTuple, Optional

class MissionData(NamedTuple):
    mission_id: int
    location_id: int
    name: str
    results_reported_flag_id: int

    def get_full_name(self) -> str:
        return f"Mission Completion: {self.name}"

MISSION_1_DATA = MissionData(1, 0x1, "Adventurer's initiation", 0x51)
MISSION_2_DATA = MissionData(2, 0x2, "The terror of Fenrir", 0x53)
MISSION_3_DATA = MissionData(3, 0x3, "Retrieve the dragon's egg", 0x55)
MISSION_4_DATA = MissionData(4, 0x4, "The hunt for Cernunos", 0x57)
MISSION_5_DATA = MissionData(5, 0x5, "Map the newfound Stratum", 0x59)
MISSION_6_DATA = MissionData(6, 0x6, "Lurker in the rainforest", 0x5B)
MISSION_7_DATA = MissionData(7, 0x7, "Annihilate the forest folk", 0x5D)

MISSION_7_CLEAR_FLAG = 0x1A6

ALL_MISSION_DATA = [
    MISSION_1_DATA,
    MISSION_2_DATA,
    MISSION_3_DATA,
    MISSION_4_DATA,
    MISSION_5_DATA,
    MISSION_6_DATA,
    MISSION_7_DATA
]

ALL_MISSION_DATA_BY_LOCATION_ID: dict[int, MissionData] = {mission_data.location_id:mission_data for mission_data in ALL_MISSION_DATA}