import requests
import json

from Database.db import MHWildsDatabase
from Modeling.entities import HuntingHorn
from Modeling.enums import WeaponType


URL_weapons = "https://wilds.mhdb.io/en/weapons"
URL_armors = "https://wilds.mhdb.io/en/armor"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

DUAL_BLADE_PARAMS = {
    "q": json.dumps({"kind": WeaponType.DUAL_BLADES.value})
}

HUNTING_HORN_PARAMS = {
    "q": json.dumps({"kind": WeaponType.HUNTING_HORN.value})
}

GREAT_SWORD_PARAMS = {
    "q": json.dumps({"kind": WeaponType.GREAT_SWORD.value})
}


MHWildsDB = MHWildsDatabase()


def load_hunting_horns():
    response = requests.get(
        URL_weapons,
        headers=HEADERS,
        params=HUNTING_HORN_PARAMS,
        timeout=15
    )
    response.raise_for_status()

    for horn_data in response.json():
        horn = HuntingHorn.model_validate(horn_data)
        MHWildsDB.add_to_hunting_horn_dict(horn)


def main():
    load_hunting_horns()

    horn = MHWildsDB.get_hunting_horn_by_id(1)
    print(horn)


if __name__ == "__main__":
    main()