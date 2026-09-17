import json

import requests

from Database.db import build_weapon_db
from Modeling import WeaponType

URL_weapons = "https://wilds.mhdb.io/en/weapons"
URL_armors = "https://wilds.mhdb.io/en/armor"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
HUNTING_HORN_PARAMS = {
    "q": json.dumps({
        "kind": WeaponType.HUNTING_HORN.value
    })
}
#curl -G "https://wilds.mhdb.io/en/weapons" --data-urlencode 'q={"kind": "hunting-horn"}'


def main():
    hunting_horn_response = requests.get(URL_weapons, headers=HEADERS, params=HUNTING_HORN_PARAMS)

    hunting_horns = build_weapon_db(hunting_horn_response.json())
    for horn in hunting_horns.values():
        print(horn)


    return

if __name__ == "__main__":
    main()