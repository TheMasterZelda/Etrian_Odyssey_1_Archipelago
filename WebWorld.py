from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .Constant import GAME_NAME

class EtrianOdysseyWebWorld(WebWorld):
    game = GAME_NAME
    theme = "grassFlowers"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Etrian Odyssey for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheMasterZelda"],
    )
    tutorials = [setup_en]
