from dataclasses import dataclass
from collections import defaultdict

from typestypes import StatRef
from enums import Op, Rank



@dataclass(frozen=True, slots=True)
class Condition :  # Stat vs Stat
    rank: Rank
    lhs: StatRef | int
    rhs: StatRef | int
    op: Op
    lscale: float = 1.0
    rscale: float = 1.0
    bias: float = 0.0      # (lhs*lscale + bias) ? (rhs*rscale)

    @staticmethod
    def _cmp(op: Op, a: float, b: float) -> bool:
        match op:
            case Op.LT: return a <  b
            case Op.LE: return a <= b
            case Op.EQ: return a == b
            case Op.NE: return a != b
            case Op.GE: return a >= b
            case Op.GT: return a >  b
            case _: raise ValueError(op)

    @property
    def needs(self):
        needs = defaultdict(set)
        if isinstance(self.lhs, StatRef): needs[self.lhs.side].add(self.lhs.stat)
        if isinstance(self.rhs, StatRef): needs[self.rhs.side].add(self.rhs.stat)
        return needs


    def evaluate(self, snap) -> bool:
        def val(x): return snap[x] if isinstance(x, StatRef) else float(x)
        a = val(self.lhs) * self.lscale + self.bias
        b = val(self.rhs) * self.rscale
        return self._cmp(self.op, a, b)

