from enum import Enum, IntEnum, auto

class Stat(Enum):
    ATTACK = auto()
    DEFENSE = auto()
    HP_MAX = auto()
    HP_CURR = auto()

class SkillColor(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"

class TargetSide(Enum):
    SELF= auto()
    OPPONENT = auto()
    ALL = auto()

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
    LT = auto()
    LE = auto()
    EQ = auto()
    NE = auto()
    GE = auto()
    GT = auto()

class Rank(Enum):
    R1 = auto()
    R2 = auto()
    R3 = auto()

    
