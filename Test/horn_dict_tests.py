import unittest
from unittest.mock import patch
from pydantic import ValidationError

from Database.db import MHWildsDatabaseFactory
from Modeling.entities import HuntingHorn
from Modeling.enums import WeaponType


class TestHuntingHornDict(unittest.TestCase):

    def setUp(self):
        self.db = MHWildsDatabaseFactory.create_empty()
        self.db = MHWildsDatabaseFactory.populate_hunting_horns(self.db)

    def test_has_content(self):
        self.assertGreater(len(self.db.get_hunting_horn_dict()), 0, "The hunting horns dictionary should not be empty.")

    
if __name__ == "__main__":
    unittest.main()