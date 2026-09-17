import json
import unittest
from pathlib import Path

from Database.db import build_weapon_db
from Modeling.enums import BowCoating
from Modeling.weapons import Bow, HuntingHorn

FIXTURES = Path(__file__).resolve().parent.parent / "Scraping"


class TestWeaponModeling(unittest.TestCase):
    def test_hunting_horn_parses_trunk_and_tail(self):
        data = json.loads((FIXTURES / "huntinghorn.json").read_text(encoding="utf-8"))
        horns = [w for w in data if w["kind"] == "hunting-horn"]

        db = build_weapon_db(horns)
        horn = db[531]

        self.assertIsInstance(horn, HuntingHorn)
        self.assertEqual(horn.name, "Hope Horn I")
        self.assertEqual(horn.damage_raw, 90)
        self.assertEqual(
            [song.name for song in horn.melody.songs],
            [
                "Self-Improvement",
                "Attack Up (S)",
                "Fire Res (S)",
                "Sonic Waves",
                "Melody of Life",
            ],
        )
        self.assertEqual(horn.echo_bubble.name, "Evasion & Movement Speed Up")

    def test_bow_parses_trunk_and_tail(self):
        data = json.loads((FIXTURES / "output.json").read_text(encoding="utf-8"))

        db = build_weapon_db(data)
        bow = db[11]

        self.assertIsInstance(bow, Bow)
        self.assertEqual(bow.name, "Rey Perkonis III")
        self.assertEqual(bow.coatings, [BowCoating.PIERCE, BowCoating.BLAST])
        self.assertEqual(bow.slots, [3, 2])

    def test_discriminated_union_picks_the_right_class(self):
        horn_data = json.loads((FIXTURES / "huntinghorn.json").read_text(encoding="utf-8"))
        bow_data = json.loads((FIXTURES / "output.json").read_text(encoding="utf-8"))
        horns_only = [w for w in horn_data if w["kind"] == "hunting-horn"]

        db = build_weapon_db(bow_data + horns_only)

        self.assertIsInstance(db[11], Bow)
        self.assertIsInstance(db[531], HuntingHorn)


if __name__ == "__main__":
    unittest.main()
