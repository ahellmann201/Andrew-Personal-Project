from typing import Any

from enums import *

class HuntingHorn:
    def __init__(self,
                 melody: HuntingHornMelody | None = None,
                 echo_bubble: HuntingHornBubble | None = None,
                 echo_wave: HuntingHornWave | None = None,):
        self.melody: HuntingHornMelody | None = melody
        self.echo_bubble: HuntingHornBubble | None = echo_bubble
        self.echo_wave: HuntingHornWave | None = echo_wave

    @classmethod
    def from_dict(cls,data: dict[str,Any]) -> "HuntingHorn" :
        return cls(
            melody=HuntingHornMelody.from_dict(data['melody']),
            echo_bubble=HuntingHornBubble.from_dict(data['echoBubble']),
            echo_wave = HuntingHornWave.from_dict(data['echoWave'])
        )


class HuntingHornMelody:
    def __init__(self,
        id: int | None = None,
        notes: list[HuntingHornNote] | None = None,
        songs: list[HuntingHornSong] | None = None,
    ):
        self.id: int | None = id
        self.notes: list[HuntingHornNote] = notes or []
        self.songs: list[HuntingHornSong] = songs or []


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HuntingHornMelody":
        return cls(
            id = data["id"],
            notes = [
                HuntingHornNote(note)
                for note in data["notes"]
            ],
            songs = [
                HuntingHornSong.from_dict(song)
                for song in data["songs"]
            ]


        )



class HuntingHornBubble:
    def __init__(
        self,
        id: int | None = None,
        kind: HuntingHornBubbleKind | None = None,
        name: str | None = None,
    ):
        self.id: int | None = id
        self.kind: HuntingHornBubbleKind | None = kind
        self.name: str | None = name

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HuntingHornBubble" :
        return cls(
            id = data['id'],
            kind = HuntingHornBubbleKind(data['kind']),
            name = data['name'],
        )


class HuntingHornWave:
    def __init__(
        self,
        id: int | None = None,
        kind: HuntingHornWaveKind | None = None,
        name: str | None = None,
    ):
        self.id: int | None = id
        self.kind: HuntingHornWaveKind | None = kind
        self.name: str | None = name

    @classmethod
    def from_dict(cls,data: dict[str,Any])->"HuntingHornWave":
        return cls(
            id = data['id'],
            kind = HuntingHornWaveKind(data['kind']),
            name = data['name'],
        )


class HuntingHornSong:
    def __init__(self,
                 id : int | None = None,
                 effect_id : int | None = None,
                 sequence: list[HuntingHornNote] | None = None,
                 name: str | None = None):
        self.id: int | None = id
        self.effect_id: int | None = effect_id
        self.sequence: list[HuntingHornNote] = sequence or []
        self.name: str | None = name

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HuntingHornSong":
        if(data["id"] is None):
            return cls(
                id = None,
                effect_id = None,
                sequence = [],
                name = ""
            )
        return cls(
            id = data['id'],
            effect_id = data['effectId'],
            sequence = [
                HuntingHornNote(note)
                for note in data['sequence']
            ],
            name = data['name']

        )
