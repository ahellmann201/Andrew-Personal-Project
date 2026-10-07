from typing import Any

from Modeling.entities import HuntingHorn
from Modeling.enums import WeaponType


class MHWildsDatabase:
    def __init__(self):
        self.weapon_dicts = {weapon_type: {} for weapon_type in WeaponType}


    def get_hunting_horn_dict(self) -> dict[int, HuntingHorn]:
        return self.weapon_dicts[WeaponType.HUNTING_HORN]

    def add_to_hunting_horn_dict(self, hunting_horn: HuntingHorn):
        horn_dict = self.get_hunting_horn_dict()
        horn_dict[hunting_horn.id] = hunting_horn

    def get_hunting_horn_by_id(self, horn_id: int) -> HuntingHorn | None:
        try:
            return self.get_hunting_horn_dict()[horn_id]
        except KeyError:
            return None