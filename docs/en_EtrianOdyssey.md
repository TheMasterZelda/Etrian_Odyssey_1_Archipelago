# Etrian Odyssey

## Warning

At the moment, this randomizer is still in active development, and so is susceptible to generation problems and logic bugs. Please make sure other players and the host are aware of the risks.

## What does randomization do to this game?

Randomization of Etrian Odyssey randomizes available character class and skills, along introducing a level cap 
and a floor limit that progressively increase. It shuffles treasure box content, Mission and Quest rewards 
along other locations.

## What is the goal of Etrian Odyssey when randomized?

The goal is to complete up to one stratum decided by the player. Completing a stratum is
defined by defeating its final floor boss. Note that any location on floors past the goal will not get shuffled.

At the moment, goal past stratum 3 are not recommended for sync sessions considering the length of the game.

## What items and locations get shuffled?

Items and Locations are not a one to one match in this game. The list of items and locations changes
based on the player yaml options. When generating, all necessary items will be first created, and every
remaining slot will be filled with random inventory consumables or money.

Here is the full list of possible Items:

- Consumables
- Money
- Key Items (Clear Key, Violet Key)
- Progressive Level Cap
- Progressive Floor Limit
- Class
- Skill (Either Individually or Grouped)

Here is the full list of possible Locations:

- Treasure Boxes
- Mission Clear
- Monster Codex entries
- Item Compendium entries


## Which items can be in another player's world?

Any items added to the item pool can be in another player world.

## What does another world's item look like in Etrian Odyssey?

Items in Etrian Odyssey does not have any visual indicator. As such, the player will only see
a vague message about what they got (if at all). This .apworld is intended to be used along
a client or tracker to be fully aware of everything they get or find.

## What happens when I receive and item?

When the player receive an item, if it isn't an inventory item, the player will receive it
directly. There are no in-game indicator when this happens. The player can see at any time
what their current floor limit or level cap is on the top right screen of the main party menu.

For the reception of inventory items, the player must enter Shilleka's Good in Etria and use the
`Receive Item` option. This will add the items to the player inventory (so long they have space for it),
up to a queue of 20. If more than 20 items are to be received, the player must interact again with
the option. If your inventory is full, you will need to sell or discard some items.

Do note that items obtained from treasure box are added directly to the player inventory.

## I found a bug!

Nice! First, make sure its a bug specific to the randomizer, then go to the dedicated etrian odyssey discord channel in the Archipelago discord and let us know about it. Alternatively, you can open an issue on this github repository, but please let me (TheMasterZelda) know in the discord channel as I am not monitoring the issues actively.

