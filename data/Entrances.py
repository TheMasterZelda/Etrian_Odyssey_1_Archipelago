from enum import IntEnum
from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

class EntranceType(IntEnum):
    Entrance = 0
    StairsDown = 1
    StairsUp = 2
    Elevator = 3
    Pitfall = 4
    StratumTransition = 5
    VioletCrystalDoor = 6
    ClearCrystalDoor = 7
    CardKeyDoor = 8
    EventLockedShortcut = 9
    MandatoryFight = 10
    OneWayFightOrEscape = 11
    DragonDoor = 12
    QuestLockedShortcut = 13


class EO1Entrance(ABC):
    destination: str
    name_prefix: Optional[str]
    name_suffix: Optional[str]

    def __init__(self, destination: str, name_prefix: Optional[str] = "", name_suffix: Optional[str] = ""):
        self.destination = destination
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix

    #@property
    #def is_stratum_transition(self) -> bool:
    #    return False

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def full_name(self) -> str:
        name = self.name
        if self.name_prefix:
            name = f"{self.name_prefix} {name}"
        if self.name_suffix:
            name = f"{name} {self.name_suffix}"
        return name

    @property
    @abstractmethod
    def entrance_type(self) -> EntranceType:
        pass

class Entrance(EO1Entrance):
    name = "To"
    entrance_type = EntranceType.Entrance

class StairsUp(EO1Entrance):
    name = "Stairs Up"
    entrance_type = EntranceType.StairsUp

class StairsDown(EO1Entrance):
    name = "Stairs Down"
    entrance_type = EntranceType.StairsDown

class Elevator(EO1Entrance):
    name = "Elevator"
    entrance_type = EntranceType.Elevator

class Pitfall(EO1Entrance):
    name = "Pitfall"
    entrance_type = EntranceType.Pitfall

class StratumTransition(StairsDown):
    entrance_type = EntranceType.StratumTransition
    #@override
    #def is_stratum_transition(self) -> bool:
    #    return True
    #pass

class VioletCrystalDoor(EO1Entrance):
    name = "Violet Crystal Door"
    entrance_type = EntranceType.VioletCrystalDoor

class ClearCrystalDoor(EO1Entrance):
    name = "Clear Crystal Door"
    entrance_type = EntranceType.ClearCrystalDoor

class CardKeyDoor(EO1Entrance):
    name = "Card Key Door"
    entrance_type = EntranceType.CardKeyDoor

class EventLockedShortcut(EO1Entrance):
    name = "Event Locked Shortcut"
    entrance_type = EntranceType.EventLockedShortcut
    event_name: str
    stratum_required: int

    def __init__(self, destination: str, event_name: str, stratum_required: int, name_prefix: Optional[str] = ""):
        super().__init__(destination, name_prefix)
        self.event_name = event_name
        self.stratum_required = stratum_required

class MandatoryFight(EO1Entrance):
    name = "Fight"
    entrance_type = EntranceType.MandatoryFight
    enemies: list[int]

    def __init__(self, destination: str, enemies: list[int], name_prefix: Optional[str] = ""):
        super().__init__(destination, name_prefix)
        self.enemies = enemies

class OneWayFightOrEscape(EO1Entrance):
    name = "One Way"
    entrance_type = EntranceType.OneWayFightOrEscape
    enemies: list[int]

    def __init__(self, destination: str, enemies: list[int], name_prefix: Optional[str] = "", name_suffix: Optional[str] = ""):
        super().__init__(destination, name_prefix, name_suffix)
        self.enemies = enemies

class DragonDoor(EO1Entrance):
    name = "Dragon Door"
    entrance_type = EntranceType.DragonDoor
    enemy_id: int

    def __init__(self, destination: str, enemy_id: int, name_prefix: Optional[str] = "", name_suffix: Optional[str] = ""):
        super().__init__(destination, name_prefix, name_suffix)
        self.enemy_id = enemy_id


class QuestLockedShortcut(EO1Entrance):
    name = "Quest Locked Shortcut"
    entrance_type = EntranceType.QuestLockedShortcut
    quest_id: int
    stratum_required: int

    def __init__(self, destination: str, quest_id: int, stratum_required: int, name_prefix: Optional[str] = ""):
        super().__init__(destination, name_prefix)
        self.quest_id = quest_id
        self.stratum_required = stratum_required
