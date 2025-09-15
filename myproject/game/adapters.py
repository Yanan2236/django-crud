from dataclasses import dataclass
from typing import Tuple, List
from .models import SkillBook, SkillVariant, SkillEffect, SkillEffectTerm, EffectKind

@dataclass(frozen=True, slots=True)
class StatRef:
    side: str
    stat: str

@dataclass(frozen=True, slots=True)
class ValueSpec:
    base: int
    terms: Tuple[Tuple[StatRef, float], ...] = ()

@dataclass(frozen=True, slots=True)
class EffectSpec:
    kind: str
    target: StatRef
    value: ValueSpec

@dataclass(frozen=True, slots=True)
class DamageEffect(EffectSpec): ...
@dataclass(frozen=True, slots=True)
class StatusEffect(EffectSpec):
    remaining: int

@dataclass(frozen=True, slots=True)
class SkillSpec:
    name: str
    clause: Tuple[EffectSpec, ...]

# === 組み立て ===
def _to_value_spec(e: SkillEffect) -> ValueSpec:
    terms: List[Tuple[StatRef, float]] = []
    for t in e.terms.all():
        terms.append((StatRef(t.ref_side, t.ref_stat), float(t.scale)))
    return ValueSpec(base=e.value_base, terms=tuple(terms))

def _to_effect_spec(e: SkillEffect) -> EffectSpec:
    target = StatRef(e.target_side, e.target_stat)
    v = _to_value_spec(e)
    if e.kind == EffectKind.STATUS:
        return StatusEffect(kind=e.kind, target=target, value=v, remaining=e.remaining or 0)
    else:
        # DAMAGE / HEAL / ATK_BUFF / POISON などは DamageEngine 側の分岐に合わせる
        return DamageEffect(kind=e.kind, target=target, value=v)

def book_rank_to_skillspec(book: SkillBook, rank: str) -> SkillSpec:
    variant = book.variants.get(rank=rank)
    effects = tuple(_to_effect_spec(e) for e in variant.effects.all())
    return SkillSpec(name=book.name, clause=effects)
