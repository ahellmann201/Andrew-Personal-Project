import csv
import sqlite3
from pathlib import Path



conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
armorcolumns = ('set_name TEXT, piece_name TEXT, armor_type TEXT, set_variant TEXT, rank TEXT, rarity INTEGER, decoration_slot_size_1 INTEGER, decoration_slot_size_2 INTEGER, decoration_slot_size_3 INTEGER, defense INTEGER, fire_resistance INTEGER, water_resistance INTEGER, thunder_resistance INTEGER, ice_resistance INTEGER, dragon_resistance INTEGER, skill_name_1 TEXT, skill_level_1 INTEGER, skill_name_2 TEXT, skill_level_2 INTEGER, skill_name_3 TEXT, skill_level_3 INTEGER, group_skill_name TEXT, set_bonus_name TEXT')

cursor.execute(f'CREATE TABLE IF NOT EXISTS armor (id INTEGER PRIMARY KEY AUTOINCREMENT,{armorcolumns})')
insert_columns = ('set_name,piece_name,armor_type,set_variant,rank,rarity,decoration_slot_size_1,decoration_slot_size_2,decoration_slot_size_3,defense,fire_resistance,water_resistance,thunder_resistance,ice_resistance,dragon_resistance,skill_name_1,skill_level_1,skill_name_2,skill_level_2,skill_name_3,skill_level_3,group_skill_name,set_bonus_name')
placeholders = ', '.join(['?']*23)

insert_query = f'INSERT INTO armor ({insert_columns}) VALUES ({placeholders})'

#get folder for below
script_dir = Path(__file__).resolve().parent
file_path = script_dir.parent / "data" / "Armor_Data.csv"



with open (file_path, 'r', encoding = 'utf-8') as file:
    tsv_reader = csv.reader(file, delimiter=',')

    #skip header row
    next(tsv_reader,None)
    
    all_data = [row[1:]for row in tsv_reader]

    cursor.executemany(insert_query,all_data)

    conn.commit()
    conn.close()