from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from enums import Stat
from character import BattleActor
from skill import StatRef

@dataclass(frozen=True, slots=True)
class SnapShot:
    _values: Mapping[StatRef, int]

    @classmethod
    def from_dict(cls, data: dict[StatRef, int]) -> SnapShot:
        return cls(MappingProxyType(data.copy()))
    
    def __getitem__(self, key: StatRef) -> int: return self._values[key] 
    def __iter__(self): return iter(self._values)
    def __len__(self): return len(self._values)
    def items(self): return self._values.items()
    def keys(self): return self._values.keys()
    def values(self): return self._values.values()

@dataclass(frozen=True, slots=True)
class EffectValueSnap:
    caster: BattleActor
    target: BattleActor
    target_stat: Stat
    effect_value: int
    
    def __str__(self) -> str:
        return f"{self.caster} -> {self.target}: {self.effect_value} damage"

