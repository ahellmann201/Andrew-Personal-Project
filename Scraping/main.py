from dis import disco
import requests
from bs4 import element
import json

from Database.db import MHWildsDatabase
from Modeling import *
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
    "q": json.dumps({
        "kind": WeaponType.DUAL_BLADES.value
    })
}
HUNTING_HORN_PARAMS = {
    "q": json.dumps({
        "kind": WeaponType.HUNTING_HORN.value
    })
}
GREAT_SWORD_PARAMS = {
    "q": json.dumps({
        "kind": WeaponType.GREAT_SWORD.value
    })
}
#curl -G "https://wilds.mhdb.io/en/weapons" --data-urlencode 'q={"kind": "dual-blades"}'


MHWildsDB =  MHWildsDatabase()

def test():
    dual_blade_response = requests.get(URL_weapons, headers=HEADERS, params=DUAL_BLADE_PARAMS)
    hunting_horn_response = requests.get(URL_weapons, headers=HEADERS, params=HUNTING_HORN_PARAMS)
    great_sword_response = requests.get(URL_weapons, headers=HEADERS, params=GREAT_SWORD_PARAMS)

    hunting_horn_json = hunting_horn_response.json()

    for horn in hunting_horn_json:
        huntinghorn = HuntingHorn.model_validate(horn)
        MHWildsDB.add_to_hunting_horn_dict(huntinghorn)

    t_horn = MHWildsDB.get_hunting_horn_by_id(1)
    print(t_horn)



def main():
    dual_blade_response = requests.get(URL_weapons, headers=HEADERS, params=DUAL_BLADE_PARAMS)
    hunting_horn_response = requests.get(URL_weapons, headers=HEADERS, params=HUNTING_HORN_PARAMS)
    great_sword_response = requests.get(URL_weapons, headers=HEADERS, params=GREAT_SWORD_PARAMS)


    test()


    # for n in range(len(hunting_horn_json)):
    #     Horn = Modeling.weapon_model.Weapon(hunting_horn_json[n])
    #     print(Hunting)





    return

if __name__ == "__main__":
    main()