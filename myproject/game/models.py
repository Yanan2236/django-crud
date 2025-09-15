from django.db import models

class TargetSide(models.TextChoices):
    SELF = "SELF"
    OPP = "OPP"
    ALL = "ALL"

class Stat(models.TextChoices):
    ATTACK = "ATTACK"
    DEFENSE = "DEFENSE"
    HP_CURR = "HP_CURR"
    HP_MAX = "HP_MAX"

class EffectKind(models.TextChoices):
    DAMAGE = "DAMAGE"
    HEAL = "HEAL"
    POISON = "POISON"
    ATK_BUFF = "ATK_BUFF"
    DEF_BUFF = "DEF_BUFF"

class SkillColor(models.TextChoices):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"

class Op(models.TextChoices):
    LT = "LT"
    LE = "LE"
    EQ = "EQ"
    NE = "NE"
    GE = "GE"
    GT = "GT"

class Rank(models.TextChoices):
    R1 = "R1", "Rank 1"
    R2 = "R2", "Rank 2"
    R3 = "R3", "Rank 3"

class SkillBook(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class SkillVariant(models.Model):
    book= models.ForeignKey(SkillBook, on_delete=models.CASCADE, related_name="variants")
    rank = models.CharField(max_length=2, choices=Rank.choices)

    class Meta:
        unique_together = [("book", "rank")]
    def __str__(self): return f"{self.book.name}:{self.rank}"

class SkillEffect(models.Model):
    variant = models.ForeignKey(SkillVariant, on_delete=models.CASCADE, related_name="effects")
    order = models.PositiveIntegerField(default=0)

    kind = models.CharField(max_length=10, choices=EffectKind.choices)
    target_side = models.CharField(max_length=4, choices=TargetSide.choices)
    target_stat = models.CharField(max_length=16, choices=Stat.choices)

    value_base = models.IntegerField(default=0) # 後で係数付きに拡張するよ。

    remaining = models.PositiveIntegerField(null=True, blank=True) # 状態変化用

    class Meta:
        ordering = ["order"]

class SkillEffectTerm(models.Model):
    effect = models.ForeignKey(
        SkillEffect, on_delete=models.CASCADE, related_name="terms"
    )

    ref_side = models.CharField(max_length=4, choices=TargetSide.choices)
    ref_stat = models.CharField(max_length=16, choices=Stat.choices)
    scale = models.FloatField()

    def __str__(self):
        return f"{self.ref_side}.{self.ref_stat} x {self.scale:+g}"
    
    class Meta:
        verbose_name = "Value term"
        verbose_name_plural = "Value terms"