from Modeling.weapon_model import Skill, SkillRank
from enums import *
from pydantic import BaseModel, Field, ConfigDict

class Charm(BaseModel):
    id: int = Field(alias="id")
    randomized: bool = Field(alias="randomized")
    ranks: list[CharmRank] = Field(alias="ranks")

class CharmRank(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    description: str = Field(alias="description")
    level: int = Field(alias="level")
    rarity: int = Field(alias="rarity")
    skills: list[SkillRank] = Field(alias="skills")
