class Weapon:

    def __init__(self, data: dict[str, Any]):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.kind: str = data["kind"]
        self.rarity: int = data["rarity"]
        self.damage: int = extract_raw_damage(data["damage"])
        self.description: str = data["description"]
        self.affinity: int = data["affinity"]
        self.defense_bonus: int = data["defenseBonus"]
        self.elderseal: bool = data["elderseal"]
        # self.slots: List[Slot] = data["slots"]


    def __str__(self):
        return(
            f"id: {self.id}, "
            f"name: {self.name}, "
            f"kind: {self.kind}, "
            f"rarity: {self.rarity}, "
            f"damage: {self.damage}, "
            f"affinity: {self.affinity}, "
            f"defense_bonus: {self.defense_bonus}, "
            f"elderseal: {self.elderseal}, "
            f"description: {self.description} \n"
        )

def extract_raw_damage(o):
    return o["raw"]