from Modeling.weapon_model import Skill
from enums import *
from pydantic import BaseModel, Field, ConfigDict

class Armor(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    kind: ArmorKind = Field(
        alias="ArmorKind",
    )
    rank: Rank = Field(
        alias="Rank",
    )
    defense: ArmorDefense = Field()
    resistances: ArmorResistances = Field()
    slots: list[int]= Field(
        alias="slots",
    )
    armor_set: ArmorSet = Field(
        alias="armorSet",
    )

class ArmorDefense(BaseModel):
    base: int | None = None
    max: int | None = None

class ArmorResistances(BaseModel):
    fire: int | None = None
    water: int | None = None
    ice: int | None = None
    thunder: int | None = None
    dragon: int | None = None

class ArmorSet(BaseModel):
    id: int | None = None
    name: str | None = None
    pieces: list[Armor] | None = None
    set_bonus_skill: Skill = Field(
        alias="setBonusSkill",
    )
    group_bonus_skill: Skill = Field(
        alias="groupBonusSkill",
    )