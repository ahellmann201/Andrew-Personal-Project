from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    """Common configuration for everything parsed from the wilds.mhdb.io API."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )


class Damage(ApiModel):
    raw: int
    display: int


class WeaponRef(ApiModel):
    id: int


class Special(ApiModel):
    id: int
    element: str | None = None
    kind: str | None = None
    weapon: WeaponRef | None = None
    damage: Damage | None = None
    hidden: bool = False


class SkillRef(ApiModel):
    id: int
    name: str
    description: str


class WeaponSkill(ApiModel):
    id: int
    skill: SkillRef
    level: int
    name: str | None = None
    description: str
    set_pieces_required: int | None = Field(default=None, alias="setPiecesRequired")


class Series(ApiModel):
    id: int
    game_id: int = Field(alias="gameId")
    name: str


class WeaponBase(ApiModel):
    """The trunk every weapon shares. Never instantiated directly."""

    id: int
    game_id: int = Field(alias="gameId")
    name: str
    rarity: int
    description: str = ""
    damage: Damage
    affinity: int = 0
    defense_bonus: int = Field(default=0, alias="defenseBonus")
    elderseal: str | None = None
    specials: list[Special] = []
    slots: list[int] = []
    skills: list[WeaponSkill] = []
    series: Series | None = None
    # Deeply nested (materials, items, icons...) and not needed for querying yet.
    crafting: dict[str, Any] | None = None

    @property
    def damage_raw(self) -> int:
        """Convenience for queries — see WEAPON_MODELING_REVIEW.md section 2."""
        return self.damage.raw
