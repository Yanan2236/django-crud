from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from enums import SkillColor, Outcome, TargetSide, Stat

if TYPE_CHECKING:
    from character import BattleActor
    from skill import SkillSpec


@dataclass(frozen=True, slots=True)
class SelectedSkillColor:
    actor: BattleActor
    color: SkillColor

@dataclass(frozen=True, slots=True)
class SelectedSkill:
    actor: BattleActor
    skill: SkillSpec

@dataclass(frozen=True, slots=True)
class ClashRecord:
    result: Outcome
    actor: BattleActor | None
    skill_color: SkillColor | None

@dataclass(frozen=True, slots=True)
class StatRef:
    side: TargetSide
    stat: Stat