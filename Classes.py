"""
Classes for Monster Hunter Wilds Skill Builder
This file contains all data classes for skills, armor, and decorations
"""
import csv
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Set, Tuple
from pathlib import Path

# ========== HELPER FUNCTIONS ==========

def parse_int(value: str, default: int = 0) -> int:
    """Parse integer, handling NA and empty strings"""
    if not value or value.strip().upper() in ['NA', 'N/A', '', 'NULL', 'NONE']:
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default

def parse_str(value: str, default: str = '') -> str:
    """Parse string, handling NA"""
    if not value or value.strip().upper() in ['NA', 'N/A', '', 'NULL', 'NONE']:
        return default
    return value.strip()

def parse_float(value: str, default: float = 0.0) -> float:
    """Parse float, handling NA"""
    if not value or value.strip().upper() in ['NA', 'N/A', '', 'NULL', 'NONE']:
        return default
    try:
        return float(value.strip())
    except ValueError:
        return default

def parse_bool(value: str) -> bool:
    """Parse boolean, handling various formats"""
    if not value:
        return False
    value = value.strip().upper()
    return value in ['TRUE', 'YES', 'Y', '1', 'T']

# ========== BASE SKILL CLASSES ==========

@dataclass
class Skill:
    """
    Represents any skill - regular, group, or set bonus.
    """
    id: str
    name: str
    skill_type: str  # Attack, Defense, Utility, Group, SetBonus
    description: str
    max_level: int
    level_effects: Dict[int, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate and clean up data"""
        # Ensure max_level is integer
        self.max_level = int(self.max_level)
        
        # Remove any level effects beyond max_level
        levels_to_remove = [lvl for lvl in self.level_effects if lvl > self.max_level]
        for level in levels_to_remove:
            del self.level_effects[level]
    
    def get_effect(self, level: int) -> str:
        """Get the effect description for a specific level"""
        if 1 <= level <= self.max_level:
            return self.level_effects.get(level, f"Level {level} effect")
        return f"Invalid level. Max is {self.max_level}"
    
    def __str__(self) -> str:
        return f"{self.name} (Max Lv{self.max_level})"
    
    def __repr__(self) -> str:
        return f"Skill(id={self.id}, name={self.name}, type={self.skill_type})"


@dataclass
class GroupSkill(Skill):
    """Special type of skill for armor set group skills"""
    def __post_init__(self):
        super().__post_init__()
        self.skill_type = "Group"


@dataclass
class SetBonusSkill(Skill):
    """Special type of skill for armor set bonuses"""
    def __post_init__(self):
        super().__post_init__()
        self.skill_type = "SetBonus"


# ========== ARMOR CLASSES ==========

@dataclass
class ArmorPiece:
    """
    Represents a single armor piece from Armor_Info.tsv
    """
    id: str
    set_name: str
    name: str
    armor_type: str  # head, chest, arms, waist, legs
    set_variant: str
    rank: str
    rarity: int
    slots: List[int]  # [slot_1, slot_2, slot_3] (0 means no slot)
    defense: int
    resistances: Dict[str, int]  # fire_res, water_res, etc.
    skills: Dict[str, int]  # skill_name -> level provided
    group_skill: Optional[str] = None
    set_bonus_skill: Optional[str] = None
    
    def __post_init__(self):
        """Convert numeric fields - already handled by parse_int"""
        pass
    
    def get_available_slots(self) -> List[int]:
        """Get list of decoration slots (excluding 0 slots)"""
        return [slot for slot in self.slots if slot > 0]
    
    def total_slot_space(self) -> int:
        """Get total decoration slot capacity"""
        return sum(self.slots)
    
    def can_fit_decoration(self, decoration_size: int) -> bool:
        """Check if a decoration of given size can fit"""
        available_slots = self.get_available_slots()
        return any(slot >= decoration_size for slot in available_slots)


@dataclass
class Decoration:
    """
    Represents a decoration from Decoration_Info.tsv
    """
    id: str
    name: str
    skills: Dict[str, int]  # skill_name -> level provided
    size: int  # 1, 2, 3, 4 (must fit in armor slot)
    
    def __post_init__(self):
        pass  # Already handled by parse_int
    
    def fits_in_slot(self, slot_size: int) -> bool:
        """Check if decoration fits in a given slot size"""
        return self.size <= slot_size


@dataclass
class Weapon:
    """Represents a weapon (simplified for now)"""
    name: str
    weapon_type: str
    attack: int
    skills: Dict[str, int] = field(default_factory=dict)
    slots: List[int] = field(default_factory=list)
    
    def __post_init__(self):
        pass  # Already handled by parse_int


@dataclass
class Charm:
    """Represents a charm/talisman"""
    name: str
    skills: Dict[str, int] = field(default_factory=dict)
    slots: List[int] = field(default_factory=list)


# ========== BUILD CLASSES ==========

@dataclass
class Build:
    """
    Represents a complete build with all equipped items.
    """
    head: Optional[ArmorPiece] = None
    chest: Optional[ArmorPiece] = None
    arms: Optional[ArmorPiece] = None
    waist: Optional[ArmorPiece] = None
    legs: Optional[ArmorPiece] = None
    weapon1: Optional[Weapon] = None
    weapon2: Optional[Weapon] = None
    charm: Optional[Charm] = None
    decorations: List[Decoration] = field(default_factory=list)
    
    def total_defense(self) -> int:
        """Calculate total defense from all armor pieces"""
        total = 0
        for piece in [self.head, self.chest, self.arms, self.waist, self.legs]:
            if piece:
                total += piece.defense
        return total
    
    def get_resistances(self) -> Dict[str, int]:
        """Get total elemental resistances"""
        resistances = {
            'fire': 0, 'water': 0, 'thunder': 0,
            'ice': 0, 'dragon': 0
        }
        
        for piece in [self.head, self.chest, self.arms, self.waist, self.legs]:
            if piece:
                for element, value in piece.resistances.items():
                    resistances[element] += value
        
        return resistances
    
    def get_all_skills(self, data_manager: 'DataManager') -> Dict[str, int]:
        """
        Get all active skills with their total levels.
        Includes armor skills, weapon skills, charm skills, and decoration skills.
        """
        skill_levels = {}
        
        # Check all equipment pieces
        all_pieces = [
            self.head, self.chest, self.arms, self.waist, self.legs,
            self.weapon1, self.weapon2, self.charm
        ]
        
        for piece in all_pieces:
            if piece and hasattr(piece, 'skills') and piece.skills:
                for skill_name, level in piece.skills.items():
                    if skill_name in skill_levels:
                        skill_levels[skill_name] += level
                    else:
                        skill_levels[skill_name] = level
        
        # Add decoration skills
        for decoration in self.decorations:
            for skill_name, level in decoration.skills.items():
                if skill_name in skill_levels:
                    skill_levels[skill_name] += level
                else:
                    skill_levels[skill_name] = level
        
        return skill_levels
    
    def get_group_skills(self) -> Set[str]:
        """Get all unique group skills from the armor set"""
        group_skills = set()
        for piece in [self.head, self.chest, self.arms, self.waist, self.legs]:
            if piece and piece.group_skill:
                group_skills.add(piece.group_skill)
        return group_skills
    
    def get_set_bonus_skills(self) -> Set[str]:
        """Get all unique set bonus skills from the armor set"""
        set_bonus_skills = set()
        for piece in [self.head, self.chest, self.arms, self.waist, self.legs]:
            if piece and piece.set_bonus_skill:
                set_bonus_skills.add(piece.set_bonus_skill)
        return set_bonus_skills
    
    def total_slot_space(self) -> int:
        """Get total available decoration slot space"""
        total = 0
        for piece in [self.head, self.chest, self.arms, self.waist, self.legs,
                     self.weapon1, self.weapon2, self.charm]:
            if piece and hasattr(piece, 'slots'):
                total += sum(piece.slots)
        return total
    
    def used_slot_space(self) -> int:
        """Get total decoration slot space used"""
        return sum(decoration.size for decoration in self.decorations)
    
    def can_add_decoration(self, decoration: Decoration) -> bool:
        """Check if a decoration can be added (has available slot space)"""
        available_space = self.total_slot_space() - self.used_slot_space()
        return decoration.size <= available_space
    
    def meets_requirements(self, data_manager: 'DataManager', required_skills: Dict[str, int]) -> bool:
        """Check if this build meets all required skill levels"""
        active_skills = self.get_all_skills(data_manager)
        
        for skill_name, required_level in required_skills.items():
            current_level = active_skills.get(skill_name, 0)
            if current_level < required_level:
                return False
        
        return True


# ========== DATA MANAGER CLASS ==========

class DataManager:
    """
    Manages loading all data from TSV files with NA handling.
    """
    
    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        
        # Skill storage
        self.skills: Dict[str, Skill] = {}  # skill_name -> Skill object
        self.skills_by_id: Dict[str, Skill] = {}  # skill_id -> Skill object
        
        # Equipment storage
        self.armor: List[ArmorPiece] = []
        self.decorations: List[Decoration] = []
        self.weapons: List[Weapon] = []
        self.charms: List[Charm] = []
        
        # Indexes for faster lookup
        self.armor_by_type: Dict[str, List[ArmorPiece]] = {
            'head': [], 'chest': [], 'arms': [], 'waist': [], 'legs': []
        }
        self.armor_by_set: Dict[str, List[ArmorPiece]] = {}
    
    def load_all_data(self):
        """Load all TSV files"""
        print("📦 Loading all game data...")
        
        # Load skills first (other files reference skills)
        if not self.load_skills("Skill_Info.tsv"):
            print("⚠️ Could not load skills, creating sample data")
            self.create_sample_skills()
        
        # Load armor
        if not self.load_armor("Armor_Info.tsv"):
            print("⚠️ Could not load armor, creating sample data")
            self.create_sample_armor()
        
        # Load decorations
        if not self.load_decorations("Decoration_Info.tsv"):
            print("⚠️ Could not load decorations, creating sample data")
            self.create_sample_decorations()
        
        # Load weapons and charms would go here
        self.create_sample_weapons()
        self.create_sample_charms()
        
        print(f"✅ Loaded: {len(self.skills)} skills, {len(self.armor)} armor pieces, "
              f"{len(self.decorations)} decorations")
    
    def load_skills(self, filename: str) -> bool:
        """Load skills from TSV file with NA handling"""
        file_path = self.data_folder / filename
        
        if not file_path.exists():
            print(f"❌ Skills file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                
                skills_loaded = 0
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Extract level effects with NA handling
                        level_effects = {}
                        for i in range(1, 8):
                            effect_key = f"level_{i}_effect"
                            if effect_key in row and row[effect_key].strip():
                                effect_value = parse_str(row[effect_key])
                                if effect_value:  # Only add if not empty after NA handling
                                    level_effects[i] = effect_value
                        
                        # Determine skill type
                        skill_type = parse_str(row.get('type', ''), 'Unknown')
                        
                        # Create skill based on type
                        if 'group' in skill_type.lower():
                            skill = GroupSkill(
                                id=parse_str(row['id']),
                                name=parse_str(row['name']),
                                skill_type='Group',
                                description=parse_str(row.get('description', '')),
                                max_level=parse_int(row['max_level']),
                                level_effects=level_effects
                            )
                        elif 'set' in skill_type.lower() or 'bonus' in skill_type.lower():
                            skill = SetBonusSkill(
                                id=parse_str(row['id']),
                                name=parse_str(row['name']),
                                skill_type='SetBonus',
                                description=parse_str(row.get('description', '')),
                                max_level=parse_int(row['max_level']),
                                level_effects=level_effects
                            )
                        else:
                            skill = Skill(
                                id=parse_str(row['id']),
                                name=parse_str(row['name']),
                                skill_type=skill_type,
                                description=parse_str(row.get('description', '')),
                                max_level=parse_int(row['max_level']),
                                level_effects=level_effects
                            )
                        
                        self.skills[skill.name] = skill
                        self.skills_by_id[skill.id] = skill
                        skills_loaded += 1
                        
                    except Exception as e:
                        print(f"⚠️ Error loading skill on row {row_num}: {e}")
                        print(f"   Row data preview: {dict(list(row.items())[:5])}")
                        continue
                
                print(f"✅ Loaded {skills_loaded} skills from {filename}")
                return True
                
        except Exception as e:
            print(f"❌ Error reading skills file: {e}")
            return False
    
    def load_armor(self, filename: str) -> bool:
        """Load armor from TSV file with NA handling"""
        file_path = self.data_folder / filename
        
        if not file_path.exists():
            print(f"❌ Armor file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                
                armor_loaded = 0
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Parse skills (skill_1, skill_1_level, etc.) with NA handling
                        skills = {}
                        for i in range(1, 4):
                            skill_key = f"skill_{i}"
                            level_key = f"skill_{i}_level"
                            
                            skill_name = parse_str(row.get(skill_key, ''))
                            if skill_name:  # Only process if skill name is not empty/NA
                                level = parse_int(row.get(level_key, '1'), 1)
                                
                                # Check if skill exists
                                if skill_name in self.skills:
                                    skills[skill_name] = level
                                else:
                                    # Create placeholder skill if it doesn't exist
                                    placeholder = Skill(
                                        id=f"PLACEHOLDER_{skill_name}",
                                        name=skill_name,
                                        skill_type='Unknown',
                                        description='[Skill not found in skill database]',
                                        max_level=level,
                                        level_effects={i: f"Level {i}" for i in range(1, level+1)}
                                    )
                                    self.skills[skill_name] = placeholder
                                    self.skills_by_id[placeholder.id] = placeholder
                                    skills[skill_name] = level
                        
                        # Parse slots with NA handling
                        slots = [
                            parse_int(row.get('slot_1', '0'), 0),
                            parse_int(row.get('slot_2', '0'), 0),
                            parse_int(row.get('slot_3', '0'), 0)
                        ]
                        
                        # Parse resistances with NA handling
                        resistances = {
                            'fire': parse_int(row.get('fire_res', '0'), 0),
                            'water': parse_int(row.get('water_res', '0'), 0),
                            'thunder': parse_int(row.get('thunder_res', '0'), 0),
                            'ice': parse_int(row.get('ice_res', '0'), 0),
                            'dragon': parse_int(row.get('dragon_res', '0'), 0)
                        }
                        
                        # Parse other fields with NA handling
                        armor_type = parse_str(row.get('Armor_type', ''), 'unknown').lower()
                        if armor_type not in ['head', 'chest', 'arms', 'waist', 'legs']:
                            print(f"⚠️ Row {row_num}: Unknown armor type '{armor_type}', defaulting to 'head'")
                            armor_type = 'head'
                        
                        armor = ArmorPiece(
                            id=parse_str(row.get('ID', f"ARMOR_{row_num}")),
                            set_name=parse_str(row.get('Set_name', 'Unknown Set')),
                            name=parse_str(row.get('Name', f"Armor Piece {row_num}")),
                            armor_type=armor_type,
                            set_variant=parse_str(row.get('set_variant', '')),
                            rank=parse_str(row.get('rank', '')),
                            rarity=parse_int(row.get('rarity', '1'), 1),
                            slots=slots,
                            defense=parse_int(row.get('defense', '0'), 0),
                            resistances=resistances,
                            skills=skills,
                            group_skill=parse_str(row.get('group_skill', '')) or None,
                            set_bonus_skill=parse_str(row.get('set_bonus_skill', '')) or None
                        )
                        
                        self.armor.append(armor)
                        
                        # Add to indexes
                        if armor.armor_type in self.armor_by_type:
                            self.armor_by_type[armor.armor_type].append(armor)
                        
                        if armor.set_name not in self.armor_by_set:
                            self.armor_by_set[armor.set_name] = []
                        self.armor_by_set[armor.set_name].append(armor)
                        
                        armor_loaded += 1
                        
                    except Exception as e:
                        print(f"⚠️ Error loading armor on row {row_num}: {e}")
                        # Print first few items to see what's causing the error
                        if row_num <= 3:  # Only print first 3 rows for debugging
                            print(f"   Row data preview: {dict(list(row.items())[:10])}")
                        continue
                
                print(f"✅ Loaded {armor_loaded} armor pieces from {filename}")
                return True
                
        except Exception as e:
            print(f"❌ Error reading armor file: {e}")
            return False
    
    def load_decorations(self, filename: str) -> bool:
        """Load decorations from TSV file with NA handling"""
        file_path = self.data_folder / filename
        
        if not file_path.exists():
            print(f"❌ Decorations file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                
                decorations_loaded = 0
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Parse skills with NA handling
                        skills = {}
                        for i in range(1, 3):  # skill_1 and skill_2
                            skill_key = f"skill_{i}_name"
                            level_key = f"skill_{i}_level"
                            
                            skill_name = parse_str(row.get(skill_key, ''))
                            if skill_name:  # Only process if skill name is not empty/NA
                                level = parse_int(row.get(level_key, '1'), 1)
                                
                                # Check if skill exists
                                if skill_name in self.skills:
                                    skills[skill_name] = level
                                else:
                                    # Create placeholder skill
                                    placeholder = Skill(
                                        id=f"DECO_PLACEHOLDER_{skill_name}",
                                        name=skill_name,
                                        skill_type='Unknown',
                                        description='[Skill from decoration]',
                                        max_level=level,
                                        level_effects={1: f"Provides {skill_name} Lv{level}"}
                                    )
                                    self.skills[skill_name] = placeholder
                                    self.skills_by_id[placeholder.id] = placeholder
                                    skills[skill_name] = level
                        
                        decoration = Decoration(
                            id=parse_str(row.get('id', f"DECO_{row_num}")),
                            name=parse_str(row.get('name', f"Decoration {row_num}")),
                            skills=skills,
                            size=parse_int(row.get('size', '1'), 1)
                        )
                        
                        self.decorations.append(decoration)
                        decorations_loaded += 1
                        
                    except Exception as e:
                        print(f"⚠️ Error loading decoration on row {row_num}: {e}")
                        continue
                
                print(f"✅ Loaded {decorations_loaded} decorations from {filename}")
                return True
                
        except Exception as e:
            print(f"❌ Error reading decorations file: {e}")
            return False
    
    # ========== SAMPLE DATA CREATION ==========
    
    def create_sample_skills(self):
        """Create sample skills for testing"""
        print("📝 Creating sample skills data...")
        
        sample_skills = [
            {
                'id': 'ATK001',
                'name': 'Attack Boost',
                'type': 'Attack',
                'description': 'Increases attack power',
                'max_level': 7,
                'level_1_effect': 'Attack +3',
                'level_4_effect': 'Attack +5%',
                'level_7_effect': 'Attack +10%'
            },
            {
                'id': 'CRT001',
                'name': 'Critical Eye',
                'type': 'Attack',
                'description': 'Increases affinity',
                'max_level': 7,
                'level_1_effect': 'Affinity +5%',
                'level_7_effect': 'Affinity +40%'
            },
            {
                'id': 'HLT001',
                'name': 'Health Boost',
                'type': 'Defense',
                'description': 'Increases maximum health',
                'max_level': 3,
                'level_1_effect': 'Health +15',
                'level_3_effect': 'Health +50'
            },
            {
                'id': 'GRP001',
                'name': 'Rathalos Essence',
                'type': 'Group',
                'description': 'Rathalos set group skill',
                'max_level': 1,
                'level_1_effect': 'Fire Attack +10%'
            },
            {
                'id': 'SET001',
                'name': 'Rathalos Mastery',
                'type': 'SetBonus',
                'description': 'Rathalos set bonus',
                'max_level': 4,
                'level_1_effect': 'True Razor Sharp',
                'level_4_effect': 'Heaven-sent'
            },
        ]
        
        for data in sample_skills:
            if 'group' in data['type'].lower():
                skill = GroupSkill(
                    id=data['id'],
                    name=data['name'],
                    skill_type='Group',
                    description=data['description'],
                    max_level=data['max_level'],
                    level_effects={int(k.split('_')[1]): v for k, v in data.items() 
                                  if k.startswith('level_') and v}
                )
            elif 'set' in data['type'].lower():
                skill = SetBonusSkill(
                    id=data['id'],
                    name=data['name'],
                    skill_type='SetBonus',
                    description=data['description'],
                    max_level=data['max_level'],
                    level_effects={int(k.split('_')[1]): v for k, v in data.items() 
                                  if k.startswith('level_') and v}
                )
            else:
                skill = Skill(
                    id=data['id'],
                    name=data['name'],
                    skill_type=data['type'],
                    description=data['description'],
                    max_level=data['max_level'],
                    level_effects={int(k.split('_')[1]): v for k, v in data.items() 
                                  if k.startswith('level_') and v}
                )
            
            self.skills[skill.name] = skill
            self.skills_by_id[skill.id] = skill
    
    def create_sample_armor(self):
        """Create sample armor for testing"""
        print("📝 Creating sample armor data...")
        
        sample_armor = [
            ArmorPiece(
                id='ARM001',
                set_name='Rathalos',
                name='Rathalos Helm',
                armor_type='head',
                set_variant='Alpha',
                rank='Master',
                rarity=8,
                slots=[3, 1, 0],
                defense=70,
                resistances={'fire': 3, 'water': 0, 'thunder': -2, 'ice': 0, 'dragon': 0},
                skills={'Attack Boost': 2},
                group_skill='Rathalos Essence',
                set_bonus_skill='Rathalos Mastery'
            ),
            ArmorPiece(
                id='ARM002',
                set_name='Rathalos',
                name='Rathalos Mail',
                armor_type='chest',
                set_variant='Alpha',
                rank='Master',
                rarity=8,
                slots=[2, 0, 0],
                defense=72,
                resistances={'fire': 3, 'water': 0, 'thunder': -2, 'ice': 0, 'dragon': 0},
                skills={'Weakness Exploit': 1},
                group_skill='Rathalos Essence',
                set_bonus_skill='Rathalos Mastery'
            ),
        ]
        
        for armor in sample_armor:
            self.armor.append(armor)
            if armor.armor_type in self.armor_by_type:
                self.armor_by_type[armor.armor_type].append(armor)
            if armor.set_name not in self.armor_by_set:
                self.armor_by_set[armor.set_name] = []
            self.armor_by_set[armor.set_name].append(armor)
    
    def create_sample_decorations(self):
        """Create sample decorations for testing"""
        print("📝 Creating sample decorations data...")
        
        sample_decorations = [
            Decoration(
                id='DEC001',
                name='Attack Jewel 4',
                skills={'Attack Boost': 1},
                size=4
            ),
            Decoration(
                id='DEC002',
                name='Critical Jewel 2',
                skills={'Critical Eye': 1},
                size=2
            ),
            Decoration(
                id='DEC003',
                name='Tenderizer Jewel 2',
                skills={'Weakness Exploit': 1},
                size=2
            ),
        ]
        
        self.decorations.extend(sample_decorations)
    
    def create_sample_weapons(self):
        """Create sample weapons for testing"""
        self.weapons = [
            Weapon(
                name='Rathalos Longsword',
                weapon_type='longsword',
                attack=210,
                skills={'Attack Boost': 1},
                slots=[3, 1]
            ),
            Weapon(
                name='Rathalos Greatsword',
                weapon_type='greatsword',
                attack=250,
                skills={},
                slots=[2, 2]
            ),
        ]
    
    def create_sample_charms(self):
        """Create sample charms for testing"""
        self.charms = [
            Charm(
                name='Attack Charm III',
                skills={'Attack Boost': 3},
                slots=[2, 1]
            ),
            Charm(
                name='Critical Eye Charm II',
                skills={'Critical Eye': 2},
                slots=[3, 0]
            ),
        ]
    
    # ========== QUERY METHODS ==========
    
    def get_skill(self, identifier: str) -> Optional[Skill]:
        """Get a skill by name or ID"""
        if identifier in self.skills:
            return self.skills[identifier]
        if identifier in self.skills_by_id:
            return self.skills_by_id[identifier]
        return None
    
    def search_skills(self, search_term: str) -> List[Skill]:
        """Search for skills by name (case-insensitive)"""
        search_term = search_term.lower()
        results = []
        
        for skill in self.skills.values():
            if search_term in skill.name.lower():
                results.append(skill)
        
        return results
    
    def get_skills_by_type(self) -> Dict[str, List[Skill]]:
        """Organize skills by type"""
        skills_by_type = {}
        for skill in self.skills.values():
            if skill.skill_type not in skills_by_type:
                skills_by_type[skill.skill_type] = []
            skills_by_type[skill.skill_type].append(skill)
        
        # Sort each type's skills alphabetically
        for skill_type in skills_by_type:
            skills_by_type[skill_type].sort(key=lambda x: x.name)
        
        return skills_by_type
    
    def get_armor_by_slot(self, slot_type: str) -> List[ArmorPiece]:
        """Get armor pieces by slot type (head, chest, etc.)"""
        return self.armor_by_type.get(slot_type.lower(), [])
    
    def get_decorations_by_size(self, max_size: Optional[int] = None) -> List[Decoration]:
        """Get decorations, optionally filtered by maximum size"""
        if max_size:
            return [d for d in self.decorations if d.size <= max_size]
        return self.decorations
    
    def get_decorations_by_skill(self, skill_name: str) -> List[Decoration]:
        """Get decorations that provide a specific skill"""
        return [d for d in self.decorations if skill_name in d.skills]
    
    def get_armor_by_skill(self, skill_name: str, min_level: int = 1) -> List[ArmorPiece]:
        """Get armor pieces that provide a specific skill at or above min_level"""
        results = []
        for armor in self.armor:
            if skill_name in armor.skills and armor.skills[skill_name] >= min_level:
                results.append(armor)
        return results
    
    def get_compatible_decorations(self, slot_sizes: List[int]) -> List[Decoration]:
        """Get decorations that can fit in at least one of the given slot sizes"""
        compatible = []
        for decoration in self.decorations:
            for slot_size in slot_sizes:
                if slot_size >= decoration.size:
                    compatible.append(decoration)
                    break
        return compatible


# ========== TEST FUNCTION ==========

def test_data_manager():
    """Test the data manager"""
    print("Testing Data Manager...")
    
    manager = DataManager("data")
    manager.load_all_data()
    
    print(f"\nTotal skills: {len(manager.skills)}")
    print(f"Total armor: {len(manager.armor)}")
    print(f"Total decorations: {len(manager.decorations)}")
    
    # Test getting a skill
    attack_boost = manager.get_skill("Attack Boost")
    if attack_boost:
        print(f"\nFound skill: {attack_boost}")
        print(f"Type: {attack_boost.skill_type}")
        print(f"Max Level: {attack_boost.max_level}")
    
    # Test armor by type
    head_armor = manager.get_armor_by_slot("head")
    print(f"\nHead armor pieces: {len(head_armor)}")
    
    # Test skill search
    print("\nSearching for 'critical':")
    for skill in manager.search_skills("critical"):
        print(f"  - {skill.name} ({skill.skill_type})")

if __name__ == "__main__":
    test_data_manager()