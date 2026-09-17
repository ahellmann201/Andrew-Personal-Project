from Modeling.weapons import Weapon, WeaponListAdapter


def build_weapon_db(raw: list[dict]) -> dict[int, Weapon]:
    """Parse the API payload into the in-memory database, keyed by id."""
    weapons = WeaponListAdapter.validate_python(raw)
    return {w.id: w for w in weapons}
