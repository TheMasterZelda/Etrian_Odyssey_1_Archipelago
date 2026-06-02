from .ILogicManager import ILogicManager, ExecutionContext
from .ClassProcessor import *
from .SustainProcessor import SustainProcessor
from .SingleEnemyBattleProcessor import *
from .EncounterBattleProcessor import *
from .EncounterGroupBattleProcessor import *
from .CodexProcessor import *
from .CompendiumProcessor import *
from .ConditionalDropProcessor import *
from .ShopUnlockProcessor import *
from .QuestProcessor import QuestProcessor

class LogicManager(ILogicManager):
    # Processors.
    class_processor: ClassProcessor
    enemy_battle_processor: SingleEnemyBattleProcessor
    encounter_battle_processor: EncounterBattleProcessor
    encounter_group_battle_processor: EncounterGroupBattleProcessor
    codex_processor: CodexProcessor
    compendium_processor: CompendiumProcessor
    conditional_drop_processor: ConditionalDropProcessor
    shop_unlock_processor: ShopUnlockProcessor
    sustain_processor: SustainProcessor
    quest_processor: QuestProcessor

    def can_defeat_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        return self.enemy_battle_processor.can_defeat_enemy(enemy_id, context)

    def can_defeat_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        return self.encounter_battle_processor.can_defeat_encounter(encounter_id, context)

    def can_defeat_special_encounter(self, enemies: list[int], context: ExecutionContext) -> bool:
        return self.encounter_battle_processor.can_defeat_enemy_group(enemies, context)

    def can_survive_enemy(self, enemy_id: int, context: ExecutionContext) -> bool:
        return self.enemy_battle_processor.can_survive_enemy(enemy_id, context)

    def can_survive_encounter(self, encounter_id: int, context: ExecutionContext) -> bool:
        return self.encounter_battle_processor.can_survive_encounter(encounter_id, context)

    def can_survive_encounter_group(self, encounter_group_id: int, context: ExecutionContext) -> bool:
        return self.encounter_group_battle_processor.can_survive_encounter_group(encounter_group_id, context)

    def can_unlock_shop_item(self, shop_item_id: int, context: ExecutionContext) -> bool:
        return self.shop_unlock_processor.can_unlock_item(shop_item_id, context)

    def can_fill_compendium_entry(self, item_id: int, context: ExecutionContext) -> bool:
        return self.compendium_processor.can_fill_compendium_entry(item_id, context)

    def can_fill_codex_entry(self, enemy_id: int, context: ExecutionContext) -> bool:
        return self.codex_processor.can_fill_codex_entry(enemy_id, context)        # TODO decide if this is omitted. Do not set to False, since the data could already be stale.
        logic_data.set_stale(True) # For safety.

        changed = len(new_unaccessible) > 0
        return changed
