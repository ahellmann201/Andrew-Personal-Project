from typing import Annotated, Literal

from pydantic import Field, TypeAdapter

from Modeling.base import ApiModel, WeaponBase
from Modeling.enums import (
    BowCoating,
    HuntingHornBubbleKind,
    HuntingHornNote,
    HuntingHornWaveKind,
    WeaponType,
)

# --- hunting horn ------------------------------------------------------------


class HuntingHornSong(ApiModel):
    id: int
    effect_id: int = Field(alias="effectId")
    sequence: list[HuntingHornNote]
    name: str


class HuntingHornMelody(ApiModel):
    id: int
    notes: list[HuntingHornNote]
    songs: list[HuntingHornSong] = []


class HuntingHornBubble(ApiModel):
    id: int
    kind: HuntingHornBubbleKind
    name: str


class HuntingHornWave(ApiModel):
    id: int
    kind: HuntingHornWaveKind
    name: str


class HuntingHorn(WeaponBase):
    kind: Literal[WeaponType.HUNTING_HORN]
    melody: HuntingHornMelody
    echo_bubble: HuntingHornBubble = Field(alias="echoBubble")
    echo_wave: HuntingHornWave = Field(alias="echoWave")


# --- bow ----------------------------------------------------------------------


class Bow(WeaponBase):
    kind: Literal[WeaponType.BOW]
    coatings: list[BowCoating] = []


# --- the union ------------------------------------------------------------
# Add the remaining twelve weapon kinds here as their tails get modeled,
# following the same pattern: WeaponBase subclass + Literal[WeaponType....].

Weapon = Annotated[
    HuntingHorn | Bow,
    Field(discriminator="kind"),
]

WeaponListAdapter: TypeAdapter = TypeAdapter(list[Weapon])
