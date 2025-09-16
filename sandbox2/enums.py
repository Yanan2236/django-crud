from enum import Enum, IntEnum, auto

class Stat(Enum):
    ATTACK = "ATTACK"
    DEFENSE = "DEFENSE"
    HP_MAX = "HP_MAX"
    HP_CURR = "HP_CURR"

class SkillColor(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"

class TargetSide(Enum):
    SELF= "SELF"
    OPPONENT = "OPPONENT"
    ALL = "ALL"

class EffectKind(Enum):
    DAMAGE = "DAMAGE"
    HEAL = "HEAL"
    POISON = "POISON"
    ATK_BUFF = "ATK_BUFF"
    DEF_BUFF = "DEF_BUFF"

class Outcome(Enum):
    ALLY = "ALLY"
    ENEMY = "ENEMY"
    DRAW = "DRAW"

class Op(Enum):
    LT = "LT"
    LE = "LE"
    EQ = "EQ"
    NE = "NE"
    GE = "GE"
    GT = "GT"

class Rank(Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"