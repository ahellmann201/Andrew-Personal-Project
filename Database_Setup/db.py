import csv
import sqlite3
from pathlib import Path

DB_NAME = 'my_database.db'

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    #skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL,
        skill_type TEXT,
        skill_description TEXT,
        skill_max_level INTEGER,
        level_1_effect TEXT, level_2_effect TEXT, level_3_effect TEXT, 
        level_4_effect TEXT, level_5_effect TEXT, level_6_effect TEXT, 
        level_7_effect TEXT
    )
    """)

    #armor table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS armor (
        armor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        set_name TEXT,
        piece_name TEXT,
        armor_type TEXT,
        set_variant TEXT,
        rank TEXT,
        rarity INTEGER,
        decoration_slot_size_1 INTEGER,
        decoration_slot_size_2 INTEGER,
        decoration_slot_size_3 INTEGER,
        defense INTEGER,
        fire_resistance INTEGER,
        water_resistance INTEGER,
        thunder_resistance INTEGER,
        ice_resistance INTEGER,
        dragon_resistance INTEGER
    )
    """)

    #armor/skills bridge table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS armor_skills (
        armor_id INTEGER,
        skill_id INTEGER,
        skill_level INTEGER,
        PRIMARY KEY (armor_id, skill_id),
        FOREIGN KEY (armor_id) REFERENCES armor (armor_id) ON DELETE CASCADE,
        FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE
    )
    """)

    #decorations main table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decoration (
    decoration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    decoration_name TEXT,
    slot_size INTEGER)
    """)

    #decoration/skill bridge
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decoration_skills (
    decoration_id INTEGER,
    skill_id INTEGER,
    skill_level INTEGER,
    PRIMARY KEY (decoration_id, skill_id),
    FOREIGN KEY (decoration_id) REFERENCES decoration (decoration_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE
)""")

    conn.commit()
    conn.close()




def get_folder_paths():
    script_dir = Path(__file__).resolve().parent
    armor_file_path = script_dir.parent / "data" / "Armor_Data.csv"
    decoration_file_path = script_dir.parent / "data" / "Decoration_Data.csv"
    skills_file_path = script_dir.parent / "data" / "Skills.csv"

    return skills_file_path,armor_file_path,decoration_file_path

def import_csv_data(skill_path,armor_path,deco_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    #------------------------------------------------------------------------------
    #                       SKILLS
    #------------------------------------------------------------------------------
    with open(skill_path,mode='r',encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:

            #dictionary for skills name,type,description,max_level,level_1_effect,level_2_effect,level_3_effect,level_4_effect,level_5_effect,level_6_effect,level_7_effect

            skill_name = row.get('name')
            skill_type = row.get('type')
            skill_description = row.get('description')
            skill_max_level = row.get('max_level')
            level_1_effect    = row.get('level_1_effect')
            level_2_effect    = row.get('level_2_effect')
            level_3_effect    = row.get('level_3_effect')
            level_4_effect    = row.get('level_4_effect')
            level_5_effect    = row.get('level_5_effect')
            level_6_effect    = row.get('level_6_effect')
            level_7_effect    = row.get('level_7_effect')

            cursor.execute("""
            INSERT OR IGNORE INTO skills (skill_name, skill_type, skill_description,skill_max_level,
                    level_1_effect, level_2_effect, level_3_effect, 
                    level_4_effect, level_5_effect, level_6_effect, 
                    level_7_effect )
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)
""",(skill_name,skill_type,skill_description,skill_max_level,
     level_1_effect,level_2_effect,level_3_effect,level_4_effect,level_5_effect,level_6_effect,level_7_effect))


    #------------------------------------------------------------------------------
    #                       ARMOR
    #------------------------------------------------------------------------------
    with open (armor_path, mode = 'r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:

            #dictionary for armor
            set_name = row.get('Set name')
            piece_name = row.get('Name')
            armor_type = row.get('Armor type')
            set_variant = row.get('set variant')
            rank = row.get('rank')
            rarity = row.get('rarity')
            decoration_slot_size_1 = row.get('slot 1')
            decoration_slot_size_2 = row.get('slot 2')
            decoration_slot_size_3 = row.get('slot 3')
            defense = row.get('defense')
            fire_resistance = row.get('fire res')
            water_resistance = row.get('water res')
            thunder_resistance = row.get('thunder res')
            ice_resistance = row.get('ice res')
            dragon_resistance = row.get("dragon res")

            #info for the bridge
            skill_1_name = row.get("skill 1")
            skill_1_level = row.get("skill 1 level")
            skill_2_name = row.get("skill 2")
            skill_2_level = row.get("skill 2 level")
            skill_3_name = row.get("skill 3")
            skill_3_level = row.get("skill 3 level")
            group_skill_name = row.get("group skill")
            set_bonus_name = row.get("set bonus skill")

            skill_1_id = None
            skill_2_id = None
            skill_3_id = None
            group_skill_id = None
            set_skill_id = None

            #get skill ids
            if skill_1_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills WHERE skill_name = ?",(skill_1_name,))
                result1 = cursor.fetchone()
                if result1:
                    skill_1_id = result1[0]

            if skill_2_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills WHERE skill_name = ?", (skill_2_name,))
                result2 = cursor.fetchone()
                if result2:
                    skill_2_id = result2[0]

            if skill_3_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills WHERE skill_name = ?", (skill_3_name,))
                result3 = cursor.fetchone()
                if result3:
                    skill_3_id = result3[0]

            if group_skill_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills where skill_name = ?", (group_skill_name,))
                resultg = cursor.fetchone()
                if resultg:
                    group_skill_id = resultg[0]

            if set_bonus_name !=  'NA':
                cursor.execute("SELECT skill_id FROM skills where skill_name = ?", (set_bonus_name,))
                resultsb = cursor.fetchone()
                if resultsb:
                    set_skill_id = resultsb[0]

           

            #insert info from armor csv into armor table
            cursor.execute("""
                INSERT OR IGNORE INTO armor (set_name,piece_name,armor_type,set_variant,rank,rarity,decoration_slot_size_1,decoration_slot_size_2,decoration_slot_size_3,
                 defense,fire_resistance,water_resistance,thunder_resistance,ice_resistance,dragon_resistance)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(set_name,piece_name,armor_type,set_variant,rank,rarity,decoration_slot_size_1,decoration_slot_size_2,decoration_slot_size_3,
                                                              defense,fire_resistance,water_resistance,thunder_resistance,ice_resistance,dragon_resistance))


            #grab armor id
            armor_id = cursor.lastrowid
            
            #insert info into armor/skill bridge
            if skill_1_id:
                cursor.execute("""INSERT OR IGNORE INTO armor_skills(armor_id,skill_id,skill_level) VALUES (?,?,?)
                """,(armor_id,skill_1_id,skill_1_level))

            if skill_2_id:
                cursor.execute("""INSERT OR IGNORE INTO armor_skills(armor_id,skill_id,skill_level) VALUES (?,?,?)
                """,(armor_id,skill_2_id,skill_2_level))

            if skill_3_id:
                cursor.execute("""INSERT OR IGNORE INTO armor_skills(armor_id,skill_id,skill_level) VALUES (?,?,?)""",(armor_id,skill_3_id,skill_3_level))

            if group_skill_id:
                cursor.execute("""INSERT OR IGNORE INTO armor_skills(armor_id,skill_id,skill_level) VALUES (?,?,?)""",(armor_id,group_skill_id,1))

            if set_skill_id:
                cursor.execute("""INSERT OR IGNORE INTO armor_skills(armor_id,skill_id,skill_level) VALUES (?,?,?)""",(armor_id,set_skill_id,1))

    #------------------------------------------------------------------------------
    #                       DECORATIONS
    #------------------------------------------------------------------------------
    with open(deco_path,mode='r',encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:

            decoration_name = row.get('name')
            skill_1_name = row.get('skill 1 name')
            skill_2_name = row.get('skill 2 name')
            skill_1_level = row.get('skill 1 level')
            skill_2_level = row.get('skill 2 level')
            slot_size = row.get('size')

            skill_1_id = None
            skill_2_id = None
            #get skill ids
            if skill_1_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills WHERE skill_name = ?",(skill_1_name,))
                result1 = cursor.fetchone()
                if result1:
                    skill_1_id = result1[0]

            if skill_2_name != 'NA':
                cursor.execute("SELECT skill_id FROM skills WHERE skill_name = ?", (skill_2_name,))
                result2 = cursor.fetchone()
                if result2:
                    skill_2_id = result2[0]

            cursor.execute("""INSERT OR IGNORE INTO decoration(decoration_name,slot_size) VALUES(?,?)""",(decoration_name,slot_size,))

            decoration_id = cursor.lastrowid

            if skill_1_id:
                cursor.execute("""INSERT OR IGNORE INTO decoration_skills(decoration_id,skill_id,skill_level) VALUES (?,?,?)
                """,(decoration_id,skill_1_id,skill_1_level,))

            if skill_2_id:
                cursor.execute("""INSERT OR IGNORE INTO decoration_skills(decoration_id,skill_id,skill_level) VALUES (?,?,?)
                """,(decoration_id,skill_2_id,skill_2_level,))


    #------------------------------------------------------------------------------
    #                       WEAPONS
    #------------------------------------------------------------------------------
    #
            




setup_database()
a,b,c = get_folder_paths()
import_csv_data(a,b,c)