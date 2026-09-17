from enum import Enum

class WeaponType(Enum):
    BOW = 'bow'
    CHARGE_BLADE = 'charge-blade'
    DUAL_BLADES = 'dual-blades'
    GREAT_SWORD = 'great-sword'
    GUNLANCE = 'gunlance'
    HAMMER = 'hammer'
    HEAVY_BOWGUN = 'heavy-bowgun'
    HUNTING_HORN='hunting-horn'
    INSECT_GLAIVE='insect-glaive'
    LANCE='lance'
    LIGHT_BOWGUN = 'light-bowgun'
    LONG_SWORD = 'long-sword'
    SWITCH_AXE = 'switch-axe'
    SWORD_SHIELD = 'sword-shield'

class SkillKind(Enum):
    ARMOR = 'armor'
    WEAPON = 'weapon'
    SET = 'set'
    GROUP = 'group'

class BowCoating(Enum):
    CLOSE_RANGE = 'close-range'
    POWER = 'power'
    PIERCE = 'pierce'
    PARALYSIS = 'paralysis'
    POISON = 'poison'
    SLEEP = 'sleep'
    BLAST = 'blast'
    EXHAUST = 'exhaust'

class ChargeBladePhial(Enum):
    ELEMENT='element'
    IMPACT='impact'

class GunlanceShell(Enum):
    NORMAL='normal'
    WIDE='wide'
    LONG='long'

class AmmoKind(Enum):
    NORMAL='normal'
    PIERCE='pierce'
    SPREAD='spread'
    SLICING='slicing'
    STICKY='sticky'
    CLUSTER='cluster'
    WYVERN='wyvern'
    POISON='poison'
    PARALYSIS='paralysis'
    SLEEP='sleep'
    FLAMING='flaming'
    WATER='water'
    FREEZE='freeze'
    THUNDER='thunder'
    DRAGON='dragon'
    RECOVER='recover'
    DEMON='demon'
    ARMOR='armor'
    EXHAUST='exhaust'
    TRANQ='tranq'

class HuntingHornNote(Enum):
    PURPLE='purple'
    RED='red'
    ORANGE='orange'
    YELLOW='yellow'
    GREEN='green'
    BLUE='blue'
    AQUA='aqua'
    WHITE='white'

class HuntingHornBubbleKind(Enum):
    EVASION='evasion'
    REGEN='regen'
    STAMINA='stamina'
    DAMAGE='damage'
    DEFENSE='defense'
    IMMUNITY='immunity'

class HuntingHornWaveKind(Enum):
    BLUNT='blunt'
    SLASH='slash'
    FIRE='fire'
    WATER='water'
    THUNDER='thunder'
    ICE='ice'
    DRAGON='dragon'
    POISON='poison'
    PARALYZE='paralyze'
    SLEEP='sleep'
    BLAST='blast'

class SwitchAxePhial(Enum):
    POWER='power'
    ELEMENT='element'
    DRAGON='dragon'
    EXHAUST='exhaust'
    PARALYZE='paralyze'
    POISON='poison'

class LightBowgunSpecialAmmo(Enum):
    WYVERN_BLAST='wyvernblast'
    ADHESIVE='adhesive'

class Elderseal(Enum):
    LOW='low'
    AVERAGE='average'
    HIGH='high'

class Element(Enum):
    FIRE='fire'
    WATER='water'
    ICE='ice'
    THUNDER='thunder'
    DRAGON='dragon'

class Status(Enum):
    POISON='poison'
    SLEEP='sleep'
    PARALYSIS='paralysis'
    STUN='stun'
    BLASTBLIGHT='blastblight'

class SpecialKind(Enum):
    ELEMENT='element'
    STATUS='status'

class DecorationKind(Enum):
    WEAPON='weapon'
    ARMOR='armor'

class ArmorKind(Enum):
    HEAD='head'
    CHEST='chest'
    ARMS='arms'
    WAIST='waist'
    LEGS='legs'

class Rank(Enum):
    LOW='low'
    HIGH='high'
    MASTER='master'