from pydantic import BaseModel, Field, ConfigDict

from enums import (
    HuntingHornBubbleKind,
    HuntingHornNote,
    HuntingHornWaveKind, BowCoating, ChargeBladePhial, GunlanceShell, AmmoKind, LightBowgunSpecialAmmo, SwitchAxePhial,
)

class WeaponDamage(BaseModel):
    raw: int | None = None
    display: int | None = None

class HuntingHorn(BaseModel):
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


class HuntingHornMelody(BaseModel):
    id: int | None = None
    notes: list[HuntingHornNote] = Field(
        default_factory=list
    )
    songs: list["HuntingHornSong"] = Field(
        default_factory=list
    )


class HuntingHornBubble(BaseModel):
    id: int | None = None
    kind: HuntingHornBubbleKind | None = None
    name: str | None = None


class HuntingHornWave(BaseModel):
    id: int | None = None
    kind: HuntingHornWaveKind | None = None
    name: str | None = None


class HuntingHornSong(BaseModel):
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

class Bow(BaseModel):
    coatings : list[BowCoating] = Field(
        default_factory=list
    )

class ChargeBlade(BaseModel):
    phial: ChargeBladePhial = Field(
        alias="phial",
    )

class Gunlance(BaseModel):
    shell: GunlanceShell = Field(
        alias="shell",
    )
    shell_level: int = Field()

class HeavyBowgun(BaseModel):
    ammo: list[HeavyBowgunAmmo] = Field()

class HeavyBowgunAmmo(BaseModel):
    kind: AmmoKind = Field(
        alias="kind",
    )
    level: int = Field()
    capaciy: int = Field()

class InsectGlaive(BaseModel):
    kinsect_level: int = Field()

class LightBowgun(BaseModel):
    ammo: list[LightBowgunAmmo] = Field()
    special_ammo: LightBowgunSpecialAmmo = Field(
        alias="specialAmmo",
    )

class LightBowgunAmmo(BaseModel):
    kind: AmmoKind = Field(
        alias="kind",
    )
    level: int = Field()
    capaciy: int = Field()
    rapid: bool = Field()

class SwitchAxe(BaseModel):
    pass

class Phial(BaseModel):
    kind: SwitchAxePhial = Field(
        alias="kind",
    )
    damage: WeaponDamage = Field()