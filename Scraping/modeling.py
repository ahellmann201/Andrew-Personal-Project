class Special:

    def __init__(
        self,
        element: str = "NA",
        kind: str = "NA",
        damage: int | str = "NA",
        hidden: bool | str = "NA"
    ) -> None:

        self.element = element
        self.kind = kind
        self.damage = damage
        self.hidden = hidden

    @classmethod
    def from_dict(cls, data: dict) -> "Special":
        if(len(data) == 0):
            return cls(
                element = "NA",
                kind = "NA",
                damage = "NA",
                hidden = "NA"
            )

        return cls(
            element=data[0]['element'],
            kind=data[0]['kind'],
            damage=extract_raw_damage(data[0]['damage']),
            hidden=data[0]['hidden']
        )

    def __str__(self) -> str:
        return (
            f"Element: {self.element}, "
            f"Kind: {self.kind}, "
            f"Damage: {self.damage}, "
            f"Hidden: {self.hidden}"
        )

class Slot:
    def __init__(
        self,
        slot_1: str = "NA",
        slot_2: str = "NA",
        slot_3: str = "NA",
    )-> None:
        self.slot_1 = slot_1
        self.slot_2 = slot_2
        self.slot_3 = slot_3

    @classmethod
    def from_dict(cls, data: dict) -> "Slot":
        if(len(data) == 0):
            return cls(
                slot_1 = "NA",
                slot_2 = "NA",
                slot_3 = "NA"
            )

        return cls(
            slot_1=data[0]["slot_1"],
            slot_2=data[0]["slot_2"],
            slot_3=data[0]["slot_3"]
        )


class SkillRank:
    def __init__(
            self,
            name: str = "NA",
            description: str = "NA",
            level: int = "NA",
            set_pieces_required: int = "NA",
    )-> None:
        self.name = name
        self.description = description
        self.level = level
        self.set_pieces_required = set_pieces_required

    @classmethod
    def from_dict(cls, data: dict) -> "SkillRank":
        if(len(data) == 0):
            return cls(
                name = "NA",
                description = "NA",
                level = "NA",
                set_pieces_required = "NA"
            )
        return cls(
            name = data[0]["name"],
            description = data[0]["description"],
            level = data[0]["level"],
            set_pieces_required = data[0]["set_pieces_required"],
        )
#
# class Skill:
#     def __init__(
#             self,
#             name: str = "NA",
#             description: str = "NA",
#             ranks: list[SkillRank] = SkillRank.from_dict(list[str]),
#             kind = SkillKind.BLANK,
#     )-> None:
#         self.name = name
#         self.description = description
#         self.ranks = ranks
#         self.kind = SkillKind(kind)
#
#     @classmethod
#     def from_dict(cls, data: dict) -> "Skill":
#         if(len(data) == 0):
#             return cls(
#                 name = "NA",
#                 description = "NA",
#                 ranks = ["NA"],
#                 kind = "NA"
#             )
#         return cls(
#             name = data[0]["name"],
#             description = data[0]["description"],
#             ranks = data[0]["ranks"],
#             kind = data[0]["kind"]
#         )
#
#
#


