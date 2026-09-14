from dis import disco
import requests
from bs4 import element

from modeling import *

URL_weapons = "https://wilds.mhdb.io/en/weapons"
URL_armors = "https://wilds.mhdb.io/en/armor"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}







def main():
    response = requests.get(URL_weapons, headers=HEADERS)
    data = response.json()

    for n in range(0,10):
        dictionary1 = data[n]
        temp_coating = dictionary1["coatings"]
        temp_game_id = dictionary1["gameId"]
        temp_rarity = dictionary1["rarity"]
        temp_kind = dictionary1["kind"]
        temp_damage = dictionary1["damage"]["raw"]
        special = Special.from_dict(dictionary1["specials"])
        temp_name = dictionary1['name']
        temp_description = dictionary1['description']
        temp_defense_bonus = dictionary1['defenseBonus']
        temp_elderseal = dictionary1['elderSeal']
        temp_slot = Slot.from_dict(dictionary1["slot"])
        temp_affinity = dictionary1["affinity"]


        print(special)




    return

if __name__ == "__main__":
    main()