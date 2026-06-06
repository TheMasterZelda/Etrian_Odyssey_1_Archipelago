from __future__ import annotations
from dataclasses import dataclass

from ...data.EnemyData import EO1Enemies
from ...data.Generic import EO1Element, EO1Ailment
from .EnemyAttributes import EnemyAttributes

from .Constant import *
from .SimplifiedValuesCriteria import *

# For some reason the IDE scream about missing import, despite not being true.
from .SimplifiedValuesCriteria import SVCriteria, CanUseActiveSkill, OrSVCriteria, AndSVCriteria


@dataclass
class SimplifiedEnemyValues:
    enemy_id: int
    defeat_criteria: SVCriteria
    survive_criteria: SVCriteria = field(default_factory=TrueSVCriteria)
    attributes: EnemyAttributes = field(default_factory=EnemyAttributes)

SIMPLIFIED_ENEMY_VALUES_TABLE: list[SimplifiedEnemyValues] = [
    # Stratum 1
    SimplifiedEnemyValues(EO1Enemies.TREERAT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.FIRE]
                          )),
    SimplifiedEnemyValues(EO1Enemies.WOODFLY, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.ARM],
                              can_inflict_bind=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.MOLE, ClassSVCriteria(front_class_count=1),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.ICE]
                          )),
    SimplifiedEnemyValues(EO1Enemies.CLAWBUG,
                          OrSVCriteria([
                              CanUseDamageSkill(skill_power=SkillPower.WEAK),
                              CanUseDamageSkill(damage_type=EO1Element.FIRE),
                              CanUseDamageSkill(damage_type=EO1Element.ICE),
                              CanUseDamageSkill(damage_type=EO1Element.THUNDER),
                          ]),
                          attributes=EnemyAttributes(
                              damage_type_resistance=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH],
                              damage_type_weakness=[EO1Element.FIRE, EO1Element.ICE, EO1Element.THUNDER]
                          )),

    SimplifiedEnemyValues(EO1Enemies.VENOMFLY,
                          OrSVCriteria([
                              CanUseDamageSkill(skill_power=SkillPower.MEDIUM),
                              CanUseDamageSkill(damage_type=EO1Element.THUNDER),
                              HasAntiStatusSVCriteria()
                          ]),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.THUNDER],
                              can_inflict_status_effect=True,
                              skills_body_use=[EO1BodyPart.LEG]
                          )),

    SimplifiedEnemyValues(EO1Enemies.HARE, TrueSVCriteria(),
                          survive_criteria=ClassSVCriteria(front_class_count=1),
                          attributes=EnemyAttributes(
                          )),
    SimplifiedEnemyValues(EO1Enemies.FENDER, ClassSVCriteria(front_class_count=1, back_class_count=1),
                          survive_criteria=ClassSVCriteria(front_class_count=1),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.LEG]
                          )),

    SimplifiedEnemyValues(EO1Enemies.MANDRAKE,
                          ClassSVCriteria(front_class_count=1, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )), # At least one front and back row class with something decent.
                          survive_criteria=ClassSVCriteria(front_class_count=1,
                                                           criteria=OrSVCriteria([
                                                               CanUseActiveSkill(
                                                                   skill_viability_level=SkillViabilityLevel.NORMAL
                                                               ),
                                                               HasDefensivePassive(),
                                                               HasOffensivePassive()
                                                           ])),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.FIRE],
                              damage_type_resistance=[EO1Element.ICE, EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Corrode

    SimplifiedEnemyValues(EO1Enemies.ROLLER,
                          ClassSVCriteria(front_class_count=1, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )), # At least one front and back row class with something decent.
                          survive_criteria=ClassSVCriteria(front_class_count=1,
                                                           criteria=OrSVCriteria([
                                                               CanUseActiveSkill(
                                                                   skill_viability_level=SkillViabilityLevel.NORMAL
                                                               ),
                                                               HasDefensivePassive(),
                                                               HasOffensivePassive()
                                                           ])),
                          attributes=EnemyAttributes(
                              damage_type_resistance=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH],
                              damage_type_weakness=[EO1Element.ICE, EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Defend (self buff)
    SimplifiedEnemyValues(EO1Enemies.CLAWFLY,
                          ClassSVCriteria(front_class_count=1, back_class_count=1,
                                          criteria=OrSVCriteria([
                                              CanUseDamageSkill(
                                                  damage_type=EO1Element.THUNDER,
                                              ),
                                              CanUseDamageSkill(
                                                  damage_type=EO1Element.ICE,
                                              ),
                                              CanUseActiveSkill(
                                                  skill_count=2,
                                                  skill_viability_level=SkillViabilityLevel.NORMAL
                                              )
                                          ])),
                          survive_criteria=ClassSVCriteria(front_class_count=2,
                                                           criteria=OrSVCriteria([
                                                               CanUseActiveSkill(
                                                                   skill_count=2,
                                                                   skill_viability_level=SkillViabilityLevel.NORMAL
                                                               ),
                                                               HasDefensivePassive()
                                                           ])),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.ARM],
                              can_inflict_bind=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.WARBULL,
                          ClassSVCriteria(front_class_count=2, back_class_count=1,
                                          criteria=OrSVCriteria([
                                              CanUseDamageSkill(
                                                  skill_power=SkillPower.MEDIUM
                                              ),
                                              # TODO damage mitigation skill.
                                          ])),
                          survive_criteria=ClassSVCriteria(front_class_count=1),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )),

    # FOE
    SimplifiedEnemyValues(EO1Enemies.RAGELOPE,
                          ClassSVCriteria(front_class_count=2, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )),

    SimplifiedEnemyValues(EO1Enemies.KUYUTHA,
                          ClassSVCriteria(front_class_count=2, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )),
    SimplifiedEnemyValues(EO1Enemies.STALKER,
                          ClassSVCriteria(front_class_count=2, back_class_count=2,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )),
    SimplifiedEnemyValues(EO1Enemies.WOLF,
                          ClassSVCriteria(front_class_count=2, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_apply_buff=True,
                          )), # Evil Cry

    # Boss
    SimplifiedEnemyValues(EO1Enemies.SKOLL,
                          ClassSVCriteria(front_class_count=2, back_class_count=1,
                                          criteria=CanUseActiveSkill(
                                              skill_viability_level=SkillViabilityLevel.NORMAL
                                          )),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_apply_buff=True,
                          )), # Evil Cry
    SimplifiedEnemyValues(EO1Enemies.FENRIR,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          HasAntiStatusSVCriteria(),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseDamageSkill(damage_type=EO1Element.FIRE)
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM),
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )),

    # Every enemy onwards makes the assumption the player is strong enough to defeat Fenrir.
    # This is to both reduce the code bloat but also improve performances.
    # TODO validate "early appearance" enemies. Those need to be handled.

    # Stratum 2
    # TODO Can be encountered in stratum 1 B4F
    # TODO Can be encountered in stratum 1 B5F
    SimplifiedEnemyValues(EO1Enemies.SLEEPGEL, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )), # Use Head
    # TODO Can be encountered in stratum 1 B4F
    # TODO Can be encountered in stratum 1 B5F
    SimplifiedEnemyValues(EO1Enemies.VENOMGEL,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          HasAntiStatusSVCriteria(),
                                          CanUseDamageSkill(damage_type=EO1Element.ICE),
                                          CanUseDamageSkill(damage_type=EO1Element.THUNDER),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )), # Use Head
    # TODO Can be encountered in stratum 1 B5F
    SimplifiedEnemyValues(EO1Enemies.WASPIOR, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG],
                              can_inflict_status_effect=True
                          )), # Use Leg
    # TODO Can be encountered in stratum 1 B3F
    SimplifiedEnemyValues(EO1Enemies.SPIDER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True,
                              can_inflict_bind=True
                          )), # Use Head
    # TODO Can be encountered in stratum 1 B4F
    SimplifiedEnemyValues(EO1Enemies.FANGLEAF,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM],
                              can_inflict_status_effect=True,
                              can_inflict_bind=True

                          )), # Use Arm
    # TODO Can be encountered in stratum 1 B4F
    # TODO Can be encountered in stratum 1 B5F
    SimplifiedEnemyValues(EO1Enemies.SLOTH,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]

                          )), # Use Arm
    # TODO Can be encountered in stratum 1 B3F
    SimplifiedEnemyValues(EO1Enemies.PETALOID,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          HasAntiStatusSVCriteria(),
                                          CanUseDamageSkill(damage_type=EO1Element.FIRE)
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True

                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.EVILOID,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          HasAntiBindSVCriteria(),
                                          CanUseDamageSkill(damage_type=EO1Element.FIRE),
                                          #CanUseAOEDamageMitigationSkill()
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD,EO1BodyPart.ARM],
                              can_inflict_bind=True

                          )), # Use Head Arm
    # TODO Can be encountered in stratum 1 B3F
    SimplifiedEnemyValues(EO1Enemies.FIREBIRD,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(damage_type=EO1Element.STAB),
                                          CanUseDamageSkill(damage_type=EO1Element.ICE),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]

                          )), # Use Head # Corrode (debuff)
    # TODO Can be encountered in stratum 1 B4F
    SimplifiedEnemyValues(EO1Enemies.MANEATER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_inflict_bind=True

                          )), # Use Head Arm
    # TODO Can be encountered in stratum 1 B3F
    SimplifiedEnemyValues(EO1Enemies.SCORPION,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG],
                              can_inflict_status_effect=True

                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.STINGMAW, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                          )),
    SimplifiedEnemyValues(EO1Enemies.GLOWBIRD, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]

                          )), # Use Head # Corrode (Debuff)
    SimplifiedEnemyValues(EO1Enemies.SPROUT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                          )),

    # FOE
    # Note: No idea if this is the right damage type (for the mitigation).
    SimplifiedEnemyValues(EO1Enemies.MOA,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB),
                                          CanUseAOEHealSkill(),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]

                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.CUTTER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          HasAntiStatusSVCriteria(),
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_inflict_status_effect=True

                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.ASSASSIN,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG],
                              can_inflict_status_effect=True

                          )), # Use Leg
    # Note: No idea if this is the right damage type (for the mitigation).
    SimplifiedEnemyValues(EO1Enemies.ARMOTH,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB),
                                          CanUseAOEHealSkill(),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]
                          )),
    SimplifiedEnemyValues(EO1Enemies.PONDCLAW, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]

                          )), # Use Head # Defend (self-buff)

    # Boss
    SimplifiedEnemyValues(EO1Enemies.CUROLLER, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True,
                          )), # Use Head Arm # Defend (AOE buff)
    # TODO more conditions favorable to the player.
    # Note: No idea if this is the right damage type (for the mitigation).
    SimplifiedEnemyValues(EO1Enemies.CERNUNOS,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True
                          )), # Use Head Arm # Has Counter # NOTE: Cernunos doesn't apply buff itself, but his summons do.

    # Stratum 3
    SimplifiedEnemyValues(EO1Enemies.MADWORM, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Can Debuff (Resist All)
    SimplifiedEnemyValues(EO1Enemies.GUARDANT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )),
    SimplifiedEnemyValues(EO1Enemies.TREEFROG, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_bind=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.DEATHANT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Can Debuff (Speed)
    SimplifiedEnemyValues(EO1Enemies.HEXFROG, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.WOODBAT, TrueSVCriteria()),
    SimplifiedEnemyValues(EO1Enemies.MELTWORM, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Can Debuff (Resist All)
    SimplifiedEnemyValues(EO1Enemies.MORIYANA, TrueSVCriteria()),
    SimplifiedEnemyValues(EO1Enemies.VAMPBAT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )),
    SimplifiedEnemyValues(EO1Enemies.CUTCRAB, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_apply_buff=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.SWORDER, TrueSVCriteria()),
    SimplifiedEnemyValues(EO1Enemies.REDCLAW, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_inflict_status_effect=True
                          )),

    # FOE
    SimplifiedEnemyValues(EO1Enemies.BLOODANT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Debuff (Speed)
    SimplifiedEnemyValues(EO1Enemies.SERVANT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )),
    SimplifiedEnemyValues(EO1Enemies.KILLCLAW, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )),
    # AOE physical damage.
    SimplifiedEnemyValues(EO1Enemies.MUCKDILE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )),
    # AOE Ice damage.
    SimplifiedEnemyValues(EO1Enemies.SHELLTOR, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )),
    # Boss
    SimplifiedEnemyValues(EO1Enemies.ROYALANT,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.BASH),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_inflict_status_effect=True
                          )), # Use Head ARM LEG
    SimplifiedEnemyValues(EO1Enemies.COTRANGL,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.ICE),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.LEG],
                              can_inflict_bind=True,
                              can_inflict_status_effect=True,
                              can_apply_buff=True
                          )), # Can Debuff (ATK)

    # Stratum 4
    SimplifiedEnemyValues(EO1Enemies.FLAMERAT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Fire Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.GOLDEER, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.LEG],
                          )), # Use Head Leg
    SimplifiedEnemyValues(EO1Enemies.SOLDIER, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.MYSTIC, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.MANTIS, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )), # Use Arm
    SimplifiedEnemyValues(EO1Enemies.SABREMAW, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Ice Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.PIXIE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE, EO1Element.ICE, EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Fire Ice Thunder Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.HEXROOT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.WARRIOR, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM]
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.DRUID, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.FAERIE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE, EO1Element.ICE, EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Fire Ice Thunder Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.REDBEAK, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE]
                          )), # Fire Immunity
    SimplifiedEnemyValues(EO1Enemies.IMMOA, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]
                          )), # Use Leg

    SimplifiedEnemyValues(EO1Enemies.SICKWOOD, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.CRUELLA,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.FIRE),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.ICE),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.THUNDER), CanInflictAilment(EO1Ailment.HEAD_BIND),
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=HasAntiStatusSVCriteria()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.DIABOLIX,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=HasAntiStatusSVCriteria()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.OGRE,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=3,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.FIRE),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.ICE),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.THUNDER),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD], # Bugged, cannot actually use EO1BodyPart.ARM,
                              can_apply_buff=True,

                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.HUNTER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=3,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=4,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.SLASH),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.STAB),
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.BASH),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],

                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.BUD, TrueSVCriteria()),

    SimplifiedEnemyValues(EO1Enemies.IWAOPELN,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=4,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=4,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.ICE),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.SLASH),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.STAB),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.BASH),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.THUNDER),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.SLASH),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_inflict_status_effect=True,
                              can_inflict_bind=True,
                          )), # Use Head Arm Leg

    # Stratum 5
    SimplifiedEnemyValues(EO1Enemies.DARKHARE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.MAUL, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )), # Use Arm
    SimplifiedEnemyValues(EO1Enemies.BURSTGEL, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.ARM]
                          )), # Fire Immunity # Use Arm
    SimplifiedEnemyValues(EO1Enemies.DIREWOLF, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Fire Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.MUSKOID, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.KINGFROG, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.KINGAPIS, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]
                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.CLAWLORD, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.SILKER, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.VARAHA, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]
                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.ARMOROLL, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                          )),
    SimplifiedEnemyValues(EO1Enemies.HELLBULL, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG]
                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.KINGYANA, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM]
                          )), # Use Arm

    SimplifiedEnemyValues(EO1Enemies.DESOULER, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.KINGDILE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.TREETUSK, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.LEG]
                          )), # Use Head Leg
    SimplifiedEnemyValues(EO1Enemies.DINOLICH, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD]
                          )), # Use Head

    SimplifiedEnemyValues(EO1Enemies.REN,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=4,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=4,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.FIRE),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.THUNDER),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.SLASH),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG]
                          )), # Ice Immunity # Use Head Arm Leg # AOE physical, Buff
    SimplifiedEnemyValues(EO1Enemies.TLACHTGA,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=4,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.SLASH),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.STAB),
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG, damage_type=EO1Element.BASH),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True,
                              can_inflict_bind=True
                          )), # Use Head # TODO HasAntiBindSVCriteria(), HasAntiStatusSVCriteria(),
    SimplifiedEnemyValues(EO1Enemies.ETREANT,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=4,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=5,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(skill_power=SkillPower.STRONG),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.BASH),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_apply_buff=True
                          )), # Use Head Arm Leg # AOE Stab and Bash

    # Stratum 6
    SimplifiedEnemyValues(EO1Enemies.FLAMEGEL,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH, EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD],
                          )), # Slash Stab Bash Fire Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.HAZEFLY,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG],
                              can_inflict_status_effect=True,
                          )), # Use Leg
    SimplifiedEnemyValues(EO1Enemies.HELLFLY,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True,
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.BLADER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.LEG],
                              can_apply_buff=True
                          )), # Use Head Leg
    SimplifiedEnemyValues(EO1Enemies.MONOCYTE,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM],
                              can_inflict_status_effect=True,
                          )), # Use Arm
    SimplifiedEnemyValues(EO1Enemies.LARGEANT,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.RED_CELL,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=3,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Use Arm
    SimplifiedEnemyValues(EO1Enemies.EVILROOT,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              )
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Use Arm
    SimplifiedEnemyValues(EO1Enemies.ROCKWOOD,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=HasAntiBindSVCriteria()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.METALION,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH, EO1Element.FIRE, EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Slash Stab Bash Fire Ice Immunity # Use Arm
    SimplifiedEnemyValues(EO1Enemies.LUCIFIRD,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM, damage_type=EO1Element.STAB)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.IRONCRAB,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.SLASH, EO1Element.STAB, EO1Element.BASH, EO1Element.FIRE, EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Slash Stab Bash Fire Ice Immunity # Use Arm
    SimplifiedEnemyValues(EO1Enemies.CLOVER, TrueSVCriteria()),

    SimplifiedEnemyValues(EO1Enemies.SONGBIRD,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.SHELLORD,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(damage_type=EO1Element.ICE)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD],
                          )), # Fire Immunity # Use Head
    SimplifiedEnemyValues(EO1Enemies.MACABRE,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB)
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True
                          )), # Use Head Arm
    SimplifiedEnemyValues(EO1Enemies.TERALICH,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(damage_type=EO1Element.FIRE),
                                          CanUseDamageSkill(damage_type=EO1Element.ICE),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                          )), # Use Head

    SimplifiedEnemyValues(EO1Enemies.WYRMOID,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.SLASH)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(damage_type=EO1Element.ICE)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.ARM, EO1BodyPart.LEG],
                          )), # Fire Immunity # Use Arm Leg
    SimplifiedEnemyValues(EO1Enemies.DRAKOID,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.ICE)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(damage_type=EO1Element.FIRE)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Ice Immunity # Use Arm
    SimplifiedEnemyValues(EO1Enemies.DRAGOID,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseDamageSkill(damage_type=EO1Element.STAB)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.ARM],
                          )), # Volt Immunity # Use Arm
    SimplifiedEnemyValues(EO1Enemies.PRIMEVIL,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=5,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB)
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=AndSVCriteria([
                                          CanUseAOEDamageNegationSkill(damage_type=EO1Element.FIRE),
                                          CanUseAOEDamageNegationSkill(damage_type=EO1Element.ICE),
                                          CanUseAOEDamageNegationSkill(damage_type=EO1Element.THUNDER),
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill()
                                  ),
                                  AdventurerMatch(
                                      match_count=3,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              can_inflict_bind=True,
                              can_inflict_status_effect=True,
                          )), # Immune to binds

    # Superbosses
    # TODO wrong damage type on AOE skill.
    SimplifiedEnemyValues(EO1Enemies.WYVERN,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=3,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=3,
                                      criteria=OrSVCriteria([
                                          CanInflictAilment(EO1Ailment.LEG_BIND),
                                          CanInflictAilment(EO1Ailment.ARM_BIND),
                                          CanInflictAilment(EO1Ailment.HEAD_BIND),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.SLASH),
                                          CanUseAOEHealSkill(),
                                      ])
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_inflict_bind=True
                          )),
    SimplifiedEnemyValues(EO1Enemies.GOLEM,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=2,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.BASH),
                                          CanUseAOEHealSkill()
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=3,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_inflict_status_effect=True,
                              can_apply_buff=True
                          )), # Block, Ward, Regen buffs
    SimplifiedEnemyValues(EO1Enemies.ALRAUNE,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=3,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.THUNDER),
                                          CanUseAOEHealSkill()
                                      ])
                                  ),
                                  AdventurerMatch(
                                      match_count=3,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.THUNDER, EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_inflict_status_effect=True
                          )), # Ice Thunder Immunity # Use Head Arm Leg
    SimplifiedEnemyValues(EO1Enemies.MANTICOR,
                          AndSVCriteria([
                              HasAntiStatusSVCriteria(),
                              PartySVCriteria(
                                  valid_class_criteria=CanUseActiveSkill(
                                      skill_count=3,
                                      skill_viability_level=SkillViabilityLevel.NORMAL
                                  ),
                                  extra_criteria=[
                                      AdventurerMatch(
                                          match_count=1,
                                          criteria=OrSVCriteria([
                                              # TODO validate damage type
                                              CanUseAOEDamageMitigationSkill(damage_type=EO1Element.STAB),
                                              CanUseAOEHealSkill()
                                          ])
                                      ),
                                      AdventurerMatch(
                                          match_count=3,
                                          criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                      )
                                  ]
                              )
                          ]),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.LEG],
                              can_inflict_status_effect=True,
                          )), # Use Head Leg
    SimplifiedEnemyValues(EO1Enemies.WYRM,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=5,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageNegationSkill(damage_type=EO1Element.FIRE),
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageMitigationSkill(damage_type=EO1Element.SLASH),
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill(),
                                  ),
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM),
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.FIRE],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_inflict_status_effect=True,
                              can_apply_buff=True,
                              can_inflict_bind=True
                          )),  # Fire Immunity # Use Head Arm Leg
    SimplifiedEnemyValues(EO1Enemies.DRAKE,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=5,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageNegationSkill(damage_type=EO1Element.ICE),
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanRemoveIceblock(),
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill(),
                                  ),
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.ICE],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM, EO1BodyPart.LEG],
                              can_apply_buff=True,
                          )),  # Ice Immunity  # Use Head Arm Leg
    SimplifiedEnemyValues(EO1Enemies.DRAGON,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_count=5,
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEDamageNegationSkill(damage_type=EO1Element.THUNDER),
                                  ),
                                  AdventurerMatch(
                                      match_count=1,
                                      criteria=CanUseAOEHealSkill(),
                                  ),
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=CanUseDamageSkill(skill_power=SkillPower.MEDIUM)
                                  ),
                              ]
                          ),
                          attributes=EnemyAttributes(
                              damage_type_immunity=[EO1Element.THUNDER],
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_apply_buff=True,
                          )), # Thunder Immunity # Use Head Arm

    # Quest enemies
    SimplifiedEnemyValues(EO1Enemies.FIREATER,
                          PartySVCriteria(
                              valid_class_criteria=CanUseActiveSkill(
                                  skill_viability_level=SkillViabilityLevel.NORMAL
                              ),
                              extra_criteria=[
                                  AdventurerMatch(
                                      match_count=2,
                                      criteria=OrSVCriteria([
                                          CanUseDamageSkill(damage_type=EO1Element.STAB),
                                          CanUseDamageSkill(damage_type=EO1Element.ICE),
                                          CanUseAOEDamageMitigationSkill(damage_type=EO1Element.FIRE),
                                      ])
                                  )
                              ]
                          ),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                          )),  # Use Head # Corrode (debuff)
    SimplifiedEnemyValues(EO1Enemies.TOXINFLY, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.LEG],
                              can_inflict_status_effect=True
                          )), # Use Leg # Inflict Poison
    SimplifiedEnemyValues(EO1Enemies.OMNIVORE, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD, EO1BodyPart.ARM],
                              can_inflict_bind=True
                          )), # Use Head Arm # Inflict binds
    SimplifiedEnemyValues(EO1Enemies.STEELWEB, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                          )), # Use Head
    SimplifiedEnemyValues(EO1Enemies.GOUDARAT, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              damage_type_weakness=[EO1Element.FIRE]
                          )),
    SimplifiedEnemyValues(EO1Enemies.NIGHTOAD, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )), # Use Head # Inflict Poison
    SimplifiedEnemyValues(EO1Enemies.HEXTOAD, TrueSVCriteria(),
                          attributes=EnemyAttributes(
                              skills_body_use=[EO1BodyPart.HEAD],
                              can_inflict_status_effect=True
                          )), # Use Head # Inflict Curse
]

SIMPLIFIED_ENEMY_VALUES_BY_ID: dict[int, SimplifiedEnemyValues] = {enemy_data.enemy_id:enemy_data for enemy_data in SIMPLIFIED_ENEMY_VALUES_TABLE}