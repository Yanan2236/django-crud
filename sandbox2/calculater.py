from snapshot import SnapShot
from skill import EffectSpec, ValueSpec
from enums import EffectKind


class DamageEngine:

    def finalize_amount(self, amount) -> int:
        return int(amount)
    
    def calculate(self, effect: EffectSpec, snapshot: SnapShot) -> int:
        value = effect.value
        amount = value.evaluate(snapshot)
        i = self.finalize_amount(amount)
        result = i if i >=0 else 0

        if effect.kind == EffectKind.HEAL: return -result
        else: return result