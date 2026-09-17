from typing import *

from pydantic import BaseModel, Field, ConfigDict

from Modeling.entities import HuntingHorn, WeaponDamage
from Modeling.enums import *


class Weapon(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    id: int | None = None
    name: str | None = None
    kind: WeaponType | None = None
    rarity: int | None = None
    damage: WeaponDamage | None = None
    description: str | None = None
    affinity: int | None = None
    defense_bonus: int | None = Field(
        default=None,
        alias="defenseBonus",
    )
    elderseal: Elderseal | None = None
    slots: list[int] = Field(
        default_factory=list
    )
    sharpness: "Sharpness | None" = None
    subtype: HuntingHorn | None = None

class Sharpness(BaseModel):
    red: int | None = None
    orange: int | None = None
    yellow: int | None = None
    green: int | None = None
    blue: int | None = None
    white: int | None = None
    purple: int | None = None


class Decoration(BaseModel):
    id: int | None = None
    name: str | None = None
    decoration: int | None = None
    slot: int | None = None
    rarity: int | None = None
    kind: DecorationKind = Field(
        alias="kind",
    )
    skills: list[SkillKind] = Field(
        alias="skills",
    )

class Skill(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    ranks: list[SkillRank] | None = None
    kind: SkillKind = Field(
        alias="kind",
    )

class SkillRank(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    level: int | None = None
    set_pieces_required: int | None = None


class WeaponSpecial(BaseModel):
    id: int | None = None
    damage: WeaponDamage | None = None
    hidden: bool | None = None
    kind: SpecialKind


class WeaponElement(WeaponSpecial):
    element: Element | None = None

class WeaponStatus(WeaponSpecial):
    status: Status | None = None


def get_weapon_special_kind(data: dict[str, Any]):
    kind = SpecialKind(data["kind"])
    if kind == SpecialKind.ELEMENT:
        return WeaponElement.model_validate(data)
    elif kind == SpecialKind.STATUS:
        return WeaponStatus.model_validate(data)

def get_weapon_subset(data: dict[str, Any]):
    kind = WeaponType(data["kind"])

    if kind == WeaponType.HUNTING_HORN:
        return HuntingHorn.model_validate(data)

