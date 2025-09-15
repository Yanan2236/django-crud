
from __future__ import annotations
from dataclasses import dataclass

from skill import StatRef, EffectSpec, ValueSpec, SkillSpec, DamageEffect, StatusEffect, SkillBook, PassiveSlot
from enums import TargetSide, Stat, EffectKind, Op, Rank
from condition import Condition

SELF_ATK = StatRef(TargetSide.SELF, Stat.ATTACK)
SELF_DEF = StatRef(TargetSide.SELF, Stat.DEFENSE)
SELF_HP_CURR = StatRef(TargetSide.SELF, Stat.HP_CURR)
SELF_HP_MAX = StatRef(TargetSide.SELF, Stat.HP_MAX)
OPP_ATK = StatRef(TargetSide.OPPONENT, Stat.ATTACK)
OPP_DEF = StatRef(TargetSide.OPPONENT, Stat.DEFENSE)
OPP_HP_CURR = StatRef(TargetSide.OPPONENT, Stat.HP_CURR)

cond = Condition(
    rank=Rank.R1,
    lhs=SELF_HP_CURR,
    rhs=SELF_HP_MAX,
    op=Op.LE,
    lscale=100, rscale=30
)

fireball = SkillSpec(
    name="fireball",
    clause=(
        DamageEffect(EffectKind.DAMAGE, OPP_HP_CURR, ValueSpec(base=10, terms=((SELF_ATK, 0.2), (OPP_DEF, -1.0),))),
    )
)

heal = SkillSpec(
    name="heal",
    clause=(
        DamageEffect(EffectKind.HEAL, SELF_HP_CURR, ValueSpec(base=0, terms=((SELF_ATK, 0.5),))),
        )
)

atkbuff = SkillSpec(
    name="atkbuff",
    clause=(
        StatusEffect(EffectKind.ATK_BUFF, SELF_ATK, ValueSpec(base=0, terms=((SELF_ATK, 0.3),)), remaining=3),
    )
)

fireball_ex = SkillSpec(
    name="fireball_ex",
    clause=(
        DamageEffect(EffectKind.DAMAGE, OPP_HP_CURR, ValueSpec(base=10, terms=((SELF_ATK, 0.2), (OPP_DEF, -1.0),))),
        DamageEffect(EffectKind.DAMAGE, OPP_HP_CURR, ValueSpec(base=0, terms=((SELF_ATK, 0.5),))),
    )
)

poison = SkillSpec(
    name="poison",
    clause=(
        StatusEffect(EffectKind.POISON, OPP_HP_CURR, ValueSpec(base=0, terms=((SELF_ATK, 0.25),)), remaining=2),
    )
)

fireball_book = SkillBook({
    Rank.R1: fireball_ex,
    Rank.R2: fireball,
    Rank.R3: fireball_ex,
})

fireball_passive = PassiveSlot(
    cond=cond,
    book=fireball_book,
)

