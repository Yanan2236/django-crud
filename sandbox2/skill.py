from __future__ import annotations
from enums import TargetSide, Stat, EffectKind, Rank
from dataclasses import dataclass
from collections import defaultdict
from typestypes import StatRef
from condition import Condition

@dataclass(frozen=True, slots=True)
class PassiveSlot:
    cond: Condition
    book: SkillBook

    def pick_skill(self) -> SkillSpec:
        return self.book.pick(self.cond.rank)


@dataclass(frozen=True, slots=True)
class SkillBook:
    book: dict[Rank, SkillSpec]

    def pick(self, rk: Rank) -> SkillSpec:
        return self.book[rk]

@dataclass(frozen=True, slots=True)
class SkillSpec:
    name: str
    clause: tuple[EffectSpec,...]

    def __str__(self):
        return self.name

@dataclass(frozen=True, slots=True)
class EffectSpec:
    kind: EffectKind
    target: StatRef
    value: ValueSpec

@dataclass(frozen=True, slots=True)
class DamageEffect(EffectSpec): 
    pass

@dataclass(frozen=True, slots=True)
class StatusEffect(EffectSpec):
    remaining: int 
    
    def create_status_instance(self, volume) -> StatusInstance:
        return StatusInstance(status_kind=self.kind, remaining=self.remaining, volume=volume)

@dataclass(frozen=True, slots=True)
class ValueSpec:
    base: int
    terms: tuple[tuple[StatRef, float]] = ()

    def evaluate(self, snapshot: dict[StatRef, int]) -> float:
        total = self.base
        for ref, scale in self.terms:
            total += snapshot[ref] * scale
        return total

    @property
    def needs(self) -> dict[TargetSide, set[Stat]]:
        needs = defaultdict(set)
        for ref, _ in self.terms:
            needs[ref.side].add(ref.stat)
        return needs
   
@dataclass(slots=True)                  
class StatusInstance:
    status_kind: EffectKind
    remaining: int
    volume: int

    def turn_end(self) -> None:
        self.remaining -= 1

    @property
    def expired(self) -> bool:
        return self.remaining <= 0 

@dataclass(frozen=True, slots=True)
class Condition:
    stats: set[Stat]
    
    

