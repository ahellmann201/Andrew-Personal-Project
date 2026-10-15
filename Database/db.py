from Modeling.entities import HuntingHorn
from Modeling.enums import WeaponType

import json
import requests




class MHWildsDatabase:
    def __init__(self):
        self.weapon_dicts = {weapon_type: {} for weapon_type in WeaponType}

    def get_hunting_horn_dict(self) -> dict[int, HuntingHorn]:
        return self.weapon_dicts[WeaponType.HUNTING_HORN]

    def add_to_hunting_horn_dict(self, hunting_horn: HuntingHorn):
        if hunting_horn.id is None:
            print("Error: Hunting Horn has no ID.")
            return

        if hunting_horn.id in self.get_hunting_horn_dict():
            print(f"Error: Hunting Horn with ID {hunting_horn.id} already exists.")
            return

        self.get_hunting_horn_dict()[hunting_horn.id] = hunting_horn

    def get_hunting_horn_by_id(self, horn_id: int) -> HuntingHorn | None:
        return self.get_hunting_horn_dict().get(horn_id)


    def get_hunting_horn_by_name(self, horn_name: str) -> HuntingHorn | None:
        return next(
            (horn for horn in self.get_hunting_horn_dict().values()
            if horn.name == horn_name),
            None
        )

    

class MHWildsDatabaseFactory:

    URL_WEAPONS = "https://wilds.mhdb.io/en/weapons"

    @staticmethod
    def create_empty() -> MHWildsDatabase:
        """Create and return database with empty dictionaries"""
        return MHWildsDatabase()


    @staticmethod
    def populate_hunting_horns(db: MHWildsDatabase) -> MHWildsDatabase:
        """Receives a database and populates it with Hunting Horns from the MHWilds API"""
        
        response = requests.get(
            MHWildsDatabaseFactory.URL_WEAPONS,
            headers={"User-Agent": "Mozilla/5.0"},
            params={
                "q": json.dumps({
                    "kind": WeaponType.HUNTING_HORN.value
                })
            },
            timeout=15
        )

        response.raise_for_status()

        for horn_data in response.json():
            horn = HuntingHorn.model_validate(horn_data)
            db.add_to_hunting_horn_dict(horn)
            
        return db

    
