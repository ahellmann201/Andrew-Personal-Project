from pydantic import Field

from Modeling.base_model import ApiModel
from Modeling.weapon_model import WeaponBase, WeaponDamage
from Modeling.enums import (
    HuntingHornBubbleKind,
    HuntingHornNote,
    HuntingHornWaveKind,
    BowCoating,
    ChargeBladePhial,
    GunlanceShell,
    AmmoKind,
    LightBowgunSpecialAmmo,
    SwitchAxePhial,
)


# ============================================================
# Hunting Horn
# ============================================================

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

    def __str__(self):
        return "\n".join(
            f"{name}: {value}"
            for name, value in self.model_dump().items()
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


# ============================================================
# Bow
# ============================================================

class Bow(WeaponBase):
    coatings: list[BowCoating] = Field(
        default_factory=list
    )


# ============================================================
# Charge Blade
# ============================================================

class ChargeBlade(WeaponBase):
    phial: ChargeBladePhial


# ============================================================
# Gunlance
# ============================================================

class Gunlance(WeaponBase):
    shell: GunlanceShell

    shell_level: int = Field(
        alias="shellLevel"
    )


# ============================================================
# Heavy Bowgun
# ============================================================

class HeavyBowgunAmmo(ApiModel):
    kind: AmmoKind
    level: int
    capacity: int


class HeavyBowgun(WeaponBase):
    ammo: list[HeavyBowgunAmmo] = Field(
        default_factory=list
    )


# ============================================================
# Insect Glaive
# ============================================================

class InsectGlaive(WeaponBase):
    kinsect_level: int = Field(
        alias="kinsectLevel"
    )


# ============================================================
# Light Bowgun
# ============================================================

class LightBowgunAmmo(ApiModel):
    kind: AmmoKind
    level: int
    capacity: int
    rapid: bool


class LightBowgun(WeaponBase):
    ammo: list[LightBowgunAmmo] = Field(
        default_factory=list
    )

    special_ammo: LightBowgunSpecialAmmo = Field(
        alias="specialAmmo"
    )


# ============================================================
# Switch Axe
# ============================================================

class Phial(ApiModel):
    kind: SwitchAxePhial
    damage: WeaponDamage | None = None


class SwitchAxe(WeaponBase):
    phial: Phial