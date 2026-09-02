import csv
import sqlite3
from pathlib import Path


script_dir = Path(__file__).resolve().parent
file_path = script_dir.parent / "data" / "Skills.csv"

with open (file_path, 'r', encoding = 'utf-8') as file:
    tsv_reader = csv.reader(file, delimiter=',')

    for row_num, row in enumerate(tsv_reader, start = 1):

        if len(row[0:])!=11:
            print(f" Line {row_num} has {len(row[0:])} items instead of 23")