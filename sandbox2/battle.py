from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

from enums import Stat, TargetSide, SkillColor, Outcome, Rank
from character import Character, BattleActor
from skill import SkillSpec, ValueSpec, EffectSpec, StatRef, DamageEffect, StatusEffect, StatusInstance
from snapshot import SnapShot, EffectValueSnap
from calculater import DamageEngine
from typestypes import SelectedSkillColor, SelectedSkill, ClashRecord

from characterpresets import Alice, Gin

class Battle:
    def __init__(self, ally: Character, enemy: Character):
        self.ally = BattleActor(ally, "ally")
        self.enemy = BattleActor(enemy, "enemy")
        self.field = frozenset({self.ally, self.enemy})
        self.clash_history = []
        self.calculater = DamageEngine()

        print("ALLY passives:", [type(p) for p in self.ally.base.passives])
        print("ENEMY passives:", [type(p) for p in self.enemy.base.passives])

    _BEATS: dict[SkillColor, SkillColor] = {
        SkillColor.RED: SkillColor.GREEN,
        SkillColor.GREEN: SkillColor.BLUE,
        SkillColor.BLUE: SkillColor.RED,
    }

    def alive(self) -> list[BattleActor]:
        return [char for char in self.field if not char.is_defeated()]   

    def _collect_skill_color(self, actor: BattleActor) -> SelectedSkillColor:
        skill_color = actor.choose_skill()
        ssc = SelectedSkillColor(actor, skill_color)
        return ssc
    
    def _judge(self, ally: SkillColor, enemy: SkillColor):
        if ally == enemy: return Outcome.DRAW
        return Outcome.ALLY if self._BEATS[ally] == enemy else Outcome.ENEMY
    
    def _log(self, outcome: Outcome, ssc: SelectedSkillColor | None) -> None:
        if ssc is None:
            self.clash_history.append(ClashRecord(Outcome.DRAW, None, None))
        else:
            self.clash_history.append(ClashRecord(outcome, ssc.actor, ssc.color))

    def resolve_clash(self) -> SelectedSkillColor | None:
        draw_count = 0
        while True:
            ally_ssc = self._collect_skill_color(self.ally)
            enemy_ssc = self._collect_skill_color(self.enemy)
            result = self._judge(ally_ssc.color, enemy_ssc.color)

            match result:
                case Outcome.DRAW: 
                    draw_count += 1
                    if draw_count > 100:
                        self._log(Outcome.DRAW, None)
                        return None  
                    else: continue
                case Outcome.ALLY:
                    self._log(Outcome.ALLY, ally_ssc)
                    return ally_ssc
                case Outcome.ENEMY:
                    self._log(Outcome.ENEMY, enemy_ssc)
                    return enemy_ssc
    
    def trigger_skill(self, ssc: SelectedSkillColor) -> SelectedSkill:
        ss = SelectedSkill(ssc.actor, ssc.actor.use_skill(ssc.color))
        print(f"{ssc.actor} use {ssc.actor.use_skill(ssc.color)}") #bye
        return ss
    
    def target_is(self, actor: BattleActor, target_side: TargetSide) -> set[BattleActor]:
        match target_side:
            case TargetSide.SELF:
                return {actor}
            case TargetSide.OPPONENT:
                return self.field - {actor}
            case TargetSide.ALL:
                return self.field
            
    def _resolve_needs(self, effect: EffectSpec) -> dict[TargetSide, set[Stat]]:
        return effect.value.needs

    def query_stat(self, actor: BattleActor, need_stats: set[Stat]) -> dict[Stat, int | bool]:
        return actor.resolve_stat(need_stats)
    
    def _get_data(self, needs: dict[TargetSide, set[Stat]], actor: BattleActor) -> dict[StatRef, int]:
        data: dict[StatRef, int] = {}

        for target_side, need_stats in needs.items():
            (target, ) = self.target_is(actor, target_side)
            stats = self.query_stat(target, need_stats)
            for stat, i in stats.items():
                data[StatRef(target_side, stat)] = i

        return data

    def take_snapshot(self, actor: BattleActor, effect: EffectSpec) -> SnapShot:
        needs = self._resolve_needs(effect)
        data = self._get_data(needs, actor)
        return SnapShot.from_dict(data)
        
    def resolve_skill(self, ss: SelectedSkill):
        caster = ss.actor
        clause = ss.skill.clause
        for effect in clause:
            snapshot = self.take_snapshot(caster, effect)
            effect_value = self.calculater.calculate(effect, snapshot)
            target_side, stat = effect.target.side, effect.target.stat
            targets = self.target_is(caster, target_side)
            for target in targets:
                if isinstance(effect, DamageEffect):
                    target.apply_damage(stat, effect_value)
                elif isinstance(effect, StatusEffect):
                    si = effect.create_status_instance(volume=effect_value)
                    target.apply_status(si)

                effectsnap = EffectValueSnap(caster, target, effect.target, effect_value)
                print(effectsnap)

    def resolve_passives(self, char: BattleActor):
        for passive in char.base.passives:
            needs = passive.cond.needs
            skill = passive.pick_skill()
            snap = self._get_data(needs, char)
            if passive.cond.evaluate(snap):
                self.resolve_skill(SelectedSkill(char, skill))
            
    def resolve_turn(self):
        ssc = self.resolve_clash()
        ss = self.trigger_skill(ssc)
        self.resolve_skill(ss)

    def is_end(self):
        return any(char.is_defeated() for char in self.field)
    
    def tick_all_status(self):
        for char in self.field:
            char.tick_statuses()


    def battle(self):
        turn = 1
        while not self.is_end():
            print(); print(f"<turn:{turn}>")
            self.resolve_turn()
            if self.is_end():  # ← 追加：アクション直後に確定させるなら
                break

            for char in list(self.alive()):  # ← 追加：巡回集合を固定
                if char.is_defeated(): 
                    continue
                self.resolve_passives(char)
                if char.is_defeated():
                    continue
                char.apply_end_of_turn_effects()
                char.advance_statuses()
                print(f"<{char.base.name}>HP:{char.hp_curr},ATK:{char.resolve_attack()}")

            if self.is_end():  # ← 同ターン両者死亡を拾って即終了したいなら
                break

            turn += 1

                





battle = Battle(ally=Alice, enemy=Gin)
battle.battle()