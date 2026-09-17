from pydantic import BaseModel, Field, ConfigDict

from base_model import ApiModel
from weapon_model import WeaponBase
from enums import (
    HuntingHornBubbleKind,
    HuntingHornNote,
    HuntingHornWaveKind, BowCoating, ChargeBladePhial, GunlanceShell, AmmoKind, LightBowgunSpecialAmmo, SwitchAxePhial,
)

class WeaponDamage(ApiModel):
    raw: int | None = None
    display: int | None = None

class HuntingHorn(WeaponBase):
    melody: "HuntingHornMelody | None" = None
    echo_bubble: "HuntingHornBubble | None" = Field(
        default=None,
        alias="echoBubble",
    )
    echo_wave: "HuntingHornWave | None" = Field(
        default=None,
        alias="echoWave",
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


class HuntingHornMelody(ApiModel):
    id: int | None = None
    notes: list[HuntingHornNote] = Field(
        default_factory=list
    )
    songs: list["HuntingHornSong"] = Field(
        default_factory=list
    )


class HuntingHornBubble(ApiModel):
    id: int | None = None
    kind: HuntingHornBubbleKind | None = None
    name: str | None = None


class HuntingHornWave(ApiModel):
    id: int | None = None
    kind: HuntingHornWaveKind | None = None
    name: str | None = None


class HuntingHornSong(ApiModel):
    id: int | None = None
    effect_id: int | None = Field(
        default=None,
        alias="effectId",
    )
    sequence: list[HuntingHornNote] = Field(
        default_factory=list
    )
    name: str | None = None

    model_config = ConfigDict(
        populate_by_name=True
    )

class Bow(WeaponBase):
    coatings : list[BowCoating] = Field(
        default_factory=list
    )

class ChargeBlade(WeaponBase):
    phial: ChargeBladePhial = Field(
        alias="phial",
    )

class Gunlance(WeaponBase):
    shell: GunlanceShell = Field(
        alias="shell",
    )
    shell_level: int = Field()

class HeavyBowgun(WeaponBase):
    ammo: list[HeavyBowgunAmmo] = Field()

class HeavyBowgunAmmo(BaseModel):
    kind: AmmoKind = Field(
        alias="kind",
    )
    level: int = Field()
    capaciy: int = Field()

class InsectGlaive(WeaponBase):
    kinsect_level: int = Field()

class LightBowgun(WeaponBase):
    ammo: list[LightBowgunAmmo] = Field()
    special_ammo: LightBowgunSpecialAmmo = Field(
        alias="specialAmmo",
    )

class LightBowgunAmmo(ApiModel):
    kind: AmmoKind = Field(
        alias="kind",
    )
    level: int = Field()
    capaciy: int = Field()
    rapid: bool = Field()

class SwitchAxe(WeaponBase):
    pass

class Phial(ApiModel):
    kind: SwitchAxePhial = Field(
        alias="kind",
    )
    damage: WeaponDamage = Field()