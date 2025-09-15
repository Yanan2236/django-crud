from enums import SkillColor
from character import Character
from effectpresets import fireball, heal, atkbuff, fireball_ex, poison, cond, fireball_book, fireball_passive


Alice = Character(
    name="Alice",
    hp=120,
    attack=20,
    defense=3,
    basic_skills={SkillColor.RED: fireball_book, SkillColor.BLUE: fireball_book, SkillColor.GREEN: fireball_book},
    skills_weight={SkillColor.RED: 7, SkillColor.BLUE: 13, SkillColor.GREEN: 10},
    passives=[fireball_passive]
    )



Gin = Character(
    name="Gin",
    hp=150,
    attack=25,
    defense=5,
    basic_skills={SkillColor.RED: fireball_book, SkillColor.BLUE: fireball_book, SkillColor.GREEN: fireball_book},
    skills_weight={SkillColor.RED: 10, SkillColor.BLUE: 8, SkillColor.GREEN: 12},
    passives=[fireball_passive]
    )