from typing import Any

from pydantic import Field

from Modeling.base_model import ApiModel
from Modeling.enums import *


class WeaponDamage(ApiModel):
    raw: int | None = None
    display: int | None = None


class Sharpness(ApiModel):
    red: int | None = None
    orange: int | None = None
    yellow: int | None = None
    green: int | None = None
    blue: int | None = None
    white: int | None = None
    purple: int | None = None


class SkillRank(ApiModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    level: int | None = None

    set_pieces_required: int | None = Field(
        default=None,
        alias="setPiecesRequired",
    )


class Skill(ApiModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None

    ranks: list[SkillRank] = Field(
        default_factory=list
    )

    kind: SkillKind | None = None


class Decoration(ApiModel):
    id: int | None = None
    name: str | None = None
    decoration: int | None = None
    slot: int | None = None
    rarity: int | None = None

    kind: DecorationKind | None = None

    skills: list[SkillKind] = Field(
        default_factory=list
    )


class WeaponSpecial(ApiModel):
    id: int | None = None
    damage: WeaponDamage | None = None
    hidden: bool | None = None
    kind: SpecialKind


class WeaponElement(WeaponSpecial):
    element: Element | None = None


class WeaponStatus(WeaponSpecial):
    status: Status | None = None


def get_weapon_special_kind(data: dict[str, Any]) -> WeaponSpecial:
    kind = SpecialKind(data["kind"])

    if kind == SpecialKind.ELEMENT:
        return WeaponElement.model_validate(data)

    if kind == SpecialKind.STATUS:
        return WeaponStatus.model_validate(data)

    raise ValueError(f"Unsupported weapon special kind: {kind}")


class WeaponBase(ApiModel):
    id: int
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

    sharpness: Sharpness | None = None