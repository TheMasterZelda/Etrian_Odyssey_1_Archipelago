from abc import ABC, abstractmethod
from enum import IntEnum

class EO1Ailment(IntEnum):
    NONE = 0
    HEAD_BIND = 1
    ARM_BIND = 2
    LEG_BIND = 3
    INSTANT_DEATH = 4
    PETRIFY = 5
    SLEEP = 6
    PARALYSIS = 7
    CONFUSION = 8
    FEAR = 9
    POISON = 10
    BLIND = 11
    CURSE = 12
    STUN = 13

class EO1Element(IntEnum):
    NONE = 0
    SLASH = 1
    BASH = 2
    STAB = 3
    FIRE = 4
    ICE = 5
    THUNDER = 6
    #PHYSICAL = 7
    #ELEMENTAL = 8 # TODO Remove. This isn't an element, this is a category.
    #ALL = 9

class EO1ElementGroup:
    PHYSICAL = [EO1Element.SLASH, EO1Element.BASH, EO1Element.STAB]
    ELEMENTAL = [EO1Element.FIRE, EO1Element.ICE, EO1Element.THUNDER]

class EO1BodyPart(IntEnum):
    NONE = 0
    HEAD = 1
    ARM = 2
    LEG = 3
    #ALL = 4

class IEtrianOdysseyLocationData(ABC):
    @abstractmethod
    def get_full_name(self) -> str:
        pass

    @abstractmethod
    def get_location_id(self) -> int:
        pass

    @abstractmethod
    def get_required_stratum(self) -> int | None:
        pass