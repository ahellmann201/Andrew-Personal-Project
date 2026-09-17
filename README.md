# Andrew-Personal-Project

A weapon/armor database built from the [wilds.mhdb.io](https://wilds.mhdb.io) API, structured well enough to build queries and reusable methods on top of it.

## Note to Andrew: how the Pydantic modeling works (`pydantic-migration` branch)

This branch replaces the hand-written parsing you had (`from_dict` classmethods, parsing inside `__init__`, `"NA"` sentinel strings — three different styles across the codebase) with [Pydantic](https://docs.pydantic.dev/) models. This note explains the mechanism and the exact flow from the raw API JSON to the typed objects you query against, with pointers to the old code and the new code so you can compare them side by side.

The full reasoning behind *why* is in [`WEAPON_MODELING_REVIEW.md`](../WEAPON_MODELING_REVIEW.md) (one level up, outside the repo). This README is the "how it actually works" follow-up.

### The core mechanism: `BaseModel`

`pydantic.BaseModel` is a class that reads your type annotations and builds a validator for you — you stop writing the code that walks a dict and converts each field, and instead *describe* the shape you want:

```python
class Damage(ApiModel):
    raw: int
    display: int
```

Calling `Damage(**{"raw": 90, "display": 378})` (or, more precisely, `Damage.model_validate(...)`, which is what happens under the hood for nested fields) converts and checks every field according to its annotation, and raises `ValidationError` — naming the exact field — the moment something doesn't fit.

### `ApiModel`: shared config, written once

See [`Modeling/base.py`](Modeling/base.py):

```python
class ApiModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )
```

Every model in the project inherits from this instead of `BaseModel` directly, so this configuration exists in one place:

| Option | What it solves |
|---|---|
| `populate_by_name=True` | Lets a field declared with `Field(alias="effectId")` accept **either** `effectId` (as the API sends it) **or** `effect_id` (if you build the object by hand in Python). |
| `extra="ignore"` | If the API adds a field tomorrow that isn't modeled, parsing doesn't crash — it's dropped. |
| `frozen=True` | Objects can't be mutated after construction (`horn.name = "x"` raises). Once something is validated, it stays valid — nothing downstream can silently un-validate it. |

### The flow, step by step

Entry point: [`Database/db.py`](Database/db.py)

```python
WeaponListAdapter.validate_python(raw)   # raw = list[dict], straight from response.json()
```

1. **A raw `dict` comes in** — still `camelCase`, still no types: `{"id": 531, "kind": "hunting-horn", "damage": {"raw": 90, ...}, "melody": {...}, ...}`.

2. **Discriminator check.** `Weapon` (in [`Modeling/weapons.py`](Modeling/weapons.py)) is defined as:
   ```python
   Weapon = Annotated[HuntingHorn | Bow, Field(discriminator="kind")]
   ```
   Before validating any field, Pydantic looks *only* at `dict["kind"]` (`"hunting-horn"`) and picks exactly one class to validate the whole dict against. This is what avoids "one `Weapon` class where 90% of the fields are `None`" — each object is validated against one complete, specific class.

3. **Recursive field validation, inside out.** To build a `HuntingHorn`, Pydantic first has to build its nested fields:
   - `damage: Damage` → the sub-dict `{"raw": 90, "display": 378}` becomes a real `Damage` object (same process, one level deeper).
   - `melody: HuntingHornMelody` → its own sub-dict is validated, and inside it `songs: list[HuntingHornSong]` builds one `HuntingHornSong` per list element.
   - `notes: list[HuntingHornNote]` → each string (`"white"`, `"red"`, ...) is matched against the `HuntingHornNote` enum and converted to the matching member. An unknown value fails right here, at the exact field path — not three layers away.

4. **Alias resolution.** A field declared as `effect_id: int = Field(alias="effectId")` tells Pydantic to read `effectId` from the input dict and expose it as `.effect_id` on the object. This one line replaces the `effect_id = data["effectId"]` you used to write by hand in every `from_dict`.

5. **All-or-nothing.** If anything fails anywhere in that recursion, nothing is built — Pydantic collects every error found (with full field paths) and raises one `ValidationError`. If it succeeds, the object is already valid *and* frozen.

### Before / after

**Before** — three different parsing styles. To see them as they were, run:
```bash
git show 294f989:Modeling/entities.py
git show 294f989:Modeling/weapon_model.py
git show 294f989:Scraping/modeling.py
```

`Modeling/weapon_model.py` at `294f989`, for example, parsed inside `__init__` and referenced `Any` without importing it (it couldn't even run):

```python
class Weapon:
    def __init__(self, data: dict[str, Any]):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.damage: int = extract_raw_damage(data["damage"])
        ...
```

`Modeling/entities.py` at `294f989` had the right idea (`from_dict` factory methods) but every one of the five Hunting Horn classes repeated the same boilerplate by hand:

```python
class HuntingHornSong:
    def __init__(self, id=None, effect_id=None, sequence=None, name=None):
        self.id = id
        self.effect_id = effect_id
        self.sequence = sequence or []
        self.name = name

    @classmethod
    def from_dict(cls, data):
        if data["id"] is None:
            return cls(id=None, effect_id=None, sequence=[], name="")
        return cls(
            id=data["id"],
            effect_id=data["effectId"],
            sequence=[HuntingHornNote(n) for n in data["sequence"]],
            name=data["name"],
        )
```

**After** — one convention, declared once:

- [`Modeling/base.py`](Modeling/base.py) — the trunk every weapon shares (`WeaponBase`: `id`, `name`, `damage`, `specials`, `skills`, `series`, ...).
- [`Modeling/weapons.py`](Modeling/weapons.py) — each weapon's tail (`HuntingHorn`, `Bow` so far) plus the discriminated union.
- [`Database/db.py`](Database/db.py) — the one call (`TypeAdapter(list[Weapon]).validate_python(raw)`) that replaces every `from_dict` loop.
- [`tests/test_weapons.py`](tests/test_weapons.py) — proves the flow above end to end against the real fixture payloads in [`Scraping/huntinghorn.json`](Scraping/huntinghorn.json) and [`Scraping/output.json`](Scraping/output.json).

Same `HuntingHornSong`, now:

```python
class HuntingHornSong(ApiModel):
    id: int
    effect_id: int = Field(alias="effectId")
    sequence: list[HuntingHornNote]
    name: str
```

No `__init__`, no `from_dict` — `from_dict` doesn't exist anymore because Pydantic *is* the parsing.

### Extending it — adding weapon #3

Only `HuntingHorn` and `Bow` are modeled right now (the two the review used to prove the pattern out). To add another weapon kind:

1. In [`Modeling/weapons.py`](Modeling/weapons.py), write a `WeaponBase` subclass with `kind: Literal[WeaponType.<KIND>]` plus that weapon's extra fields (its "tail").
2. Add it to the `Weapon` union: `HuntingHorn | Bow | YourNewClass`.
3. Add a fixture-backed test in [`tests/test_weapons.py`](tests/test_weapons.py) the same way the existing two do it — get real API data for that weapon kind first, don't guess at field names.

Twelve more to go, each one should be a handful of lines.
