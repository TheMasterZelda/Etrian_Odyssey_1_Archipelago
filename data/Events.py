from dataclasses import dataclass

from .InventoryItemData import EO1ItemNames


class EventNames:
    FENRIR_DEFEATED = "Fenrir Defeated"
    STRATUM_2_REACHED = "Stratum 2 Reached"
    DRAGON_EGG_OBTAINED = "Dragon Egg Obtained"
    MISSION_3_COMPLETED = "Mission 3 Completed"
    CERNUNOS_DEFEATED = "Cernunos Defeated"
    COTRANGL_DEFEATED = "Cotrangl Defeated"
    DISCOVER_CLAW_MARK = "Discover Claw Mark"
    AZURE_COLOSSUS_QUEST_ACCEPTED = "Azure Colossus Quest Accepted"
    ANNIHILATE_THE_FOREST_FOLK = "Annihilate the forest folk"
    MISSION_7_COMPLETED = "Mission 7 Completed"
    ELEVATOR_ACTIVATED = "Elevator Activated"
    CARD_KEY_OBTAINED = "Card Key Obtained"
    ETREANT_DEFEATED = "Etreant Defeat"
    PRIMEVIL_DEFEATED = "Primevil Defeated"
    OBTAINED_THE_TOWN_CROWN = "Obtained the Town Crown"

@dataclass
class EventInfo:
    name: str
    item_name: str
    required_stratum: int

EVENT_FENRIR_DEFEATED = EventInfo(
    EventNames.FENRIR_DEFEATED,
    "Fenrir Defeated",
    required_stratum=1)

EVENT_STRATUM_2_REACHED = EventInfo(
    EventNames.STRATUM_2_REACHED,
    "Stratum 2 Reached",
    required_stratum=2)

EVENT_DRAGON_EGG_OBTAINED = EventInfo(
    EventNames.DRAGON_EGG_OBTAINED,
    "Dragon Egg Obtained",
    required_stratum=2)

EVENT_MISSION_3_COMPLETED = EventInfo(
    EventNames.MISSION_3_COMPLETED,
    "Mission 3 Completed",
    required_stratum=2)

EVENT_CERNUNOS_DEFEATED = EventInfo(
    EventNames.CERNUNOS_DEFEATED,
    "Cernunos defeated",
    required_stratum=2)

EVENT_COTRANGL_DEFEATED = EventInfo(
    EventNames.COTRANGL_DEFEATED,
    "Cotrangl defeated",
    required_stratum=3)

EVENT_DISCOVER_CLAW_MARK = EventInfo(
    EventNames.DISCOVER_CLAW_MARK,
    "Discover Claw Mark",
    required_stratum=4)

EVENT_AZURE_COLOSSUS_QUEST_ACCEPTED = EventInfo(
    EventNames.AZURE_COLOSSUS_QUEST_ACCEPTED,
    "Azure Colossus Quest Accepted",
    required_stratum=6)

EVENT_ANNIHILATE_THE_FOREST_FOLK = EventInfo(
    EventNames.ANNIHILATE_THE_FOREST_FOLK,
    "Forest Folk Annihilated",
    required_stratum=4)

EVENT_MISSION_7_COMPLETED = EventInfo(
    EventNames.MISSION_7_COMPLETED,
    "Mission 7 Completed",
    required_stratum=5)

EVENT_ELEVATOR_ACTIVATED = EventInfo(
    EventNames.ELEVATOR_ACTIVATED,
    "Elevator Activated",
    required_stratum=5)

EVENT_CARD_KEY_OBTAINED = EventInfo(
    EventNames.CARD_KEY_OBTAINED,
    "Card Key Obtained",
    required_stratum=5)

EVENT_ETREANT_DEFEATED = EventInfo(
    EventNames.ETREANT_DEFEATED,
    "Etreant Defeated",
    required_stratum=5)

EVENT_PRIMEVIL_DEFEATED = EventInfo(
    EventNames.PRIMEVIL_DEFEATED,
    "Primevil Defeated",
    required_stratum=6)

EVENT_OBTAIN_THE_TOWN_CROWN = EventInfo(
    EventNames.OBTAINED_THE_TOWN_CROWN,
    "Why would you do this",
    required_stratum=7)

EVENT_OBTAIN_RADHA_NOTE = EventInfo(
    "Obtain Radha Note",
    EO1ItemNames.RADHA_NOTE,
    required_stratum=1)

EVENT_BY_NAME: dict[str, EventInfo] = {
    EVENT_FENRIR_DEFEATED.name: EVENT_FENRIR_DEFEATED,
    EVENT_STRATUM_2_REACHED.name:EVENT_STRATUM_2_REACHED,
    EVENT_DRAGON_EGG_OBTAINED.name:EVENT_DRAGON_EGG_OBTAINED,
    EVENT_MISSION_3_COMPLETED.name:EVENT_MISSION_3_COMPLETED,
    EVENT_CERNUNOS_DEFEATED.name:EVENT_CERNUNOS_DEFEATED,
    EVENT_COTRANGL_DEFEATED.name:EVENT_COTRANGL_DEFEATED,
    EVENT_DISCOVER_CLAW_MARK.name:EVENT_DISCOVER_CLAW_MARK,
    EVENT_AZURE_COLOSSUS_QUEST_ACCEPTED.name:EVENT_AZURE_COLOSSUS_QUEST_ACCEPTED,
    EVENT_ANNIHILATE_THE_FOREST_FOLK.name:EVENT_ANNIHILATE_THE_FOREST_FOLK,
    EVENT_MISSION_7_COMPLETED.name:EVENT_MISSION_7_COMPLETED,
    EVENT_ELEVATOR_ACTIVATED.name:EVENT_ELEVATOR_ACTIVATED,
    EVENT_CARD_KEY_OBTAINED.name:EVENT_CARD_KEY_OBTAINED,
    EVENT_ETREANT_DEFEATED.name:EVENT_ETREANT_DEFEATED,
    EVENT_PRIMEVIL_DEFEATED.name:EVENT_PRIMEVIL_DEFEATED,
    EVENT_OBTAIN_THE_TOWN_CROWN.name:EVENT_OBTAIN_THE_TOWN_CROWN,
    EVENT_OBTAIN_RADHA_NOTE.name:EVENT_OBTAIN_RADHA_NOTE
}