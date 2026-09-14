import csv
import requests
from bs4 import BeautifulSoup

URL = "https://game8.co/games/Monster-Hunter-Wilds/archives/500352"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def inspect_note_markup(soup: BeautifulSoup, limit: int = 20):
    """
    Run this first. It prints the raw markup around the first N note
    icons so you can see whether note types (Primary/Secondary/Flourish)
    live in an <img alt="">, a <span class="">, a title attribute, etc.
    game8 typically renders each note as a small icon image inside the
    table cell, e.g. <img alt="Primary Note" src="...">
    """
    # Common containers for this kind of guide table on game8
    candidates = soup.select("table img, td img, li img, div.a-table img")
    print(f"Found {len(candidates)} candidate note images.\n")
    for img in candidates[:limit]:
        print("---")
        print("alt:", img.get("alt"))
        print("title:", img.get("title"))
        print("class:", img.get("class"))
        print("src:", img.get("src"))
        print("parent tag:", img.parent.name, "| parent class:", img.parent.get("class"))


def extract_song_rows(soup: BeautifulSoup):
    """
    Extract song rows from the 'List of Hunting Horn Songs' section.
    Each row = song name + ordered list of note types (Primary/Secondary/Flourish).

    NOTE: The exact selectors below (table/tr/td, or ul/li) may need
    adjusting once you've run inspect_note_markup() and seen the real
    tag names/classes/alt text on this page.
    """
    rows = []

    # Try table-based structure first
    tables = soup.find_all("table")
    for table in tables:
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue

            song_name = cells[0].get_text(strip=True)
            if not song_name:
                continue

            note_types = []
            for cell in cells[1:]:
                imgs = cell.find_all("img")
                if imgs:
                    for img in imgs:
                        # Prefer alt text, fall back to title, fall back to class
                        label = img.get("alt") or img.get("title") or ""
                        note_types.append(label.strip())
                else:
                    text = cell.get_text(strip=True)
                    if text:
                        note_types.append(text)

            if note_types:
                rows.append((song_name, note_types))

    return rows


def print_structured(rows):
    print(f"{'Song':30s} | Notes")
    print("-" * 60)
    for song_name, note_types in rows:
        padded = note_types + [""] * (4 - len(note_types))  # pad to 4 columns
        print(f"{song_name:30s} | " + "\t".join(padded[:4]))


def save_csv(rows, path="hunting_horn_songs.csv"):
    max_notes = max((len(n) for _, n in rows), default=0)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Song"] + [f"Note {i+1}" for i in range(max_notes)])
        for song_name, note_types in rows:
            padded = note_types + [""] * (max_notes - len(note_types))
            writer.writerow([song_name] + padded)
    print(f"\nSaved {len(rows)} rows to {path}")


def main():
    soup = fetch_soup(URL)

    print("=== STEP 1: Inspect raw note markup ===")
    inspect_note_markup(soup)

    print("\n=== STEP 2: Extracted structured rows ===")
    rows = extract_song_rows(soup)
    print_structured(rows)

    if rows:
        save_csv(rows)


if __name__ == "__main__":
    main()