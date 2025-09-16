from __future__ import annotations 
import random
from collections import defaultdict
from enums import SkillColor, Stat, EffectKind, Rank
from skill import SkillSpec, StatusInstance, SkillBook, PassiveSlot
from condition import Condition


class Character:
    def __init__(self, name: str, hp: int, attack: int, defense: int, basic_skills: dict[SkillColor, SkillBook], skills_weight: dict[SkillColor, int], passives: list[PassiveSlot]):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.basic_skills = basic_skills
        self.skills_weight = skills_weight
        self.passives = passives

class BattleActor:
    def __init__(self, base: Character, id_: str):
        self.base = base
        self.attack = base.attack
        self.defense = base.defense
        self.hp_curr = self.base.hp
        self.status_effects: dict[EffectKind, list[StatusInstance]] = defaultdict(list)
        self.id = id_

    _STATS_MAP = {
        Stat.ATTACK: "attack",
        Stat.HP_CURR: "hp_curr",
    }

    def __repr__(self):
        return f"<{self.base.name}>HP:{self.hp_curr}"

    def __str__(self):
        return self.base.name

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, BattleActor) and self.id == other.id

    def resolve_attack(self) -> int:
        buffs = self.status_effects[EffectKind.ATK_BUFF]
        total_buff = sum(s.volume for s in buffs)
        total_attack = self.attack + total_buff
        return total_attack if total_attack >= 0 else 0
    
    def resolve_defense(self) -> int:
        buffs = self.status_effects[EffectKind.DEF_BUFF]
        total_buff = sum(s.volume for s in buffs)
        total_defence = self.defense + total_buff
        return total_defence if total_defence >= 0 else 0
    
    def resolve_hp_curr(self) -> int:
        return self.hp_curr
    
    def resolve_hp_max(self) -> int:
        return self.base.hp
    
    def resolve_hp_miss(self) -> int:
        return self.base.hp - self.hp_curr
    
    def resolve_poison(self) -> int:
        poisons = self.status_effects[EffectKind.POISON]
        total_poison = sum(s.volume for s in poisons)
        return total_poison
    
    _RESOLVE_STAT = {
        Stat.ATTACK: resolve_attack,
        Stat.DEFENSE: resolve_defense,
        Stat.HP_CURR: resolve_hp_curr,
        Stat.HP_MAX: resolve_hp_max,
        Stat.HP_MISS: resolve_hp_miss,
    }

    def is_defeated(self) -> bool:
        return self.hp_curr <= 0

    def resolve_stat(self, stats: set[Stat]) -> dict[Stat, int | bool]:
        return {stat: self._RESOLVE_STAT[stat](self) for stat in stats}
    
    def choose_skill(self) -> SkillColor:
        skill_color = random.choices(
            population=list(self.base.skills_weight.keys()),
            weights=list(self.base.skills_weight.values()),
            k=1
        )[0]
        return skill_color
    
    def use_skill(self, skill_color: SkillColor) -> SkillSpec:
        return self.base.basic_skills[skill_color].pick(Rank.R2)
    

    def apply_damage(self, stat: Stat, effect_value: int) -> None:
        field = self._STATS_MAP[stat]
        current = getattr(self, field)
        setattr(self, field, current - effect_value)

    def apply_status(self, status_instance: StatusInstance) -> None:
        self.status_effects[status_instance.status_kind].append(status_instance)

    def _apply_poison(self) -> None:
        v = self.resolve_poison()
        self.apply_damage(Stat.HP_CURR, v)

    def apply_end_of_turn_effects(self):
        self._apply_poison()


    def resolve_passive(self): # OOOOOOOOOOOOOOO
        pass
        

    def tick_statuses(self):
        for _, statuses in self.status_effects.items():
            for s in statuses:
                s.turn_end()

    def purne_expired_status(self):
        for kind, statuses in self.status_effects.items():
            kept = [s for s in statuses if not s.expired]
            self.status_effects[kind] = kept
            
    def advance_statuses(self) -> None:
        self.tick_statuses()
        self.purne_expired_status()
        

    


      
