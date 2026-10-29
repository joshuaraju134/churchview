import os
import json
import sqlite3
import urllib.request

BIBLE_DIR = r"C:\Users\Guest User\AppData\Roaming\openlp\data\bibles"
MAL_DB = os.path.join(BIBLE_DIR, "Malayalam BSI.sqlite")
OUT_JSON = r"c:\Users\Guest User\.gemini\antigravity-ide\scratch\bible_projector\bible_dual.json"

ENGLISH_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

MALAYALAM_BOOKS = [
    "ഉല്പത്തി", "പുറപ്പാടു", "ലേവ്യപുസ്തകം", "സംഖ്യാപുസ്തകം", "ആവർത്തനം",
    "യോശുവ", "ന്യായാധിപന്മാർ", "രൂത്ത്", "1 ശമൂവേൽ", "2 ശമൂവേൽ",
    "1 രാജാക്കന്മാർ", "2 രാജാക്കന്മാർ", "1 ദിനവൃത്താന്തം", "2 ദിനവൃത്താന്തം", "എസ്രാ",
    "നെഹെമ്യാവു", "എസ്ഥേർ", "ഇയ്യോബ്", "സങ്കീർത്തനങ്ങൾ", "സദൃശവാക്യങ്ങൾ",
    "സഭാപ്രസംഗി", "ഉത്തമഗീതം", "യെശയ്യാവു", "യിരെമ്യാവു", "വിലാപങ്ങൾ",
    "യെഹെസ്കേൽ", "ദാനീയേൽ", "ഹോശേയ", "യോവേൽ", "ആമോസ്",
    "ഓബദ്യാവു", "യോനാ", "മീഖാ", "നഹൂം", "ഹബക്കൂക്ക്",
    "സെഫന്യാവു", "ഹഗ്ഗായി", "സെഖര്യാവു", "മലാഖി",
    "മത്തായി", "മർക്കൊസ്", "ലൂക്കൊസ്", "യോഹന്നാൻ", "പ്രവൃത്തികൾ",
    "റോമർ", "1 കൊരിന്ത്യർ", "2 കൊരിന്ത്യർ", "ഗലാത്യർ", "എഫെസ്യർ",
    "ഫിലിപ്പിയർ", "കൊലൊസ്സ്യർ", "1 തെസ്സലോനീക്യർ", "2 തെസ്സലോനീക്യർ", "1 തിമൊഥെയൊസ്",
    "2 തിമൊഥെയൊസ്", "തീത്തൊസ്", "ഫിലേമോൻ", "എബ്രായർ", "യാക്കോബ്",
    "1 പത്രൊസ്", "2 പത്രൊസ്", "1 യോഹന്നാൻ", "2 യോഹന്നാൻ", "3 യോഹന്നാൻ",
    "യൂദാ", "വെളിപ്പാടു"
]

ENG_ABBREV = [
    "Gen", "Exo", "Lev", "Num", "Deu", "Jos", "Jdg", "Rut", "1Sa", "2Sa",
    "1Ki", "2Ki", "1Ch", "2Ch", "Ezr", "Neh", "Est", "Job", "Psa", "Pro",
    "Ecc", "Sng", "Isa", "Jer", "Lam", "Ezk", "Dan", "Hos", "Jol", "Amo",
    "Oba", "Jon", "Mic", "Nah", "Hab", "Zep", "Hag", "Zec", "Mal",
    "Mat", "Mrk", "Luk", "Jhn", "Act", "Rom", "1Co", "2Co", "Gal", "Eph",
    "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas",
    "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud", "Rev"
]

MAL_ABBREV = [
    "ഉല്പ", "പുറ", "ലേവ്യ", "സംഖ്യാ", "ആവർ", "യോശു", "ന്യായാ", "രൂത്ത്", "1ശമൂ", "2ശമൂ",
    "1രാജാ", "2രാജാ", "1ദിന", "2ദിന", "എസ്രാ", "നെഹെ", "എസ്ഥേ", "ഇയ്യോ", "സങ്കീ", "സദൃ",
    "സഭാ", "ഉത്ത", "യെശ", "യിരെ", "വിലാ", "യെഹെ", "ദാനീ", "ഹോശേ", "യോവേ", "ആമോ",
    "ഓബ", "യോനാ", "മീഖാ", "നഹൂം", "ഹബ", "സെഫ", "ഹഗ്ഗായി", "സെഖ", "മലാ",
    "മത്താ", "മർക്കൊ", "ലൂക്കൊ", "യോഹ", "പ്രവൃ", "റോമ", "1കൊരി", "2കൊരി", "ഗലാ", "എഫെ",
    "ഫിലി", "കൊലൊ", "1തെസ്സ", "2തെസ്സ", "1തിമൊ", "2തിമൊ", "തീത്തോ", "ഫിലേ", "എബ്രാ", "യാക്കോ",
    "1പത്രൊ", "2പത്രൊ", "1യോഹ", "2യോഹ", "3യോഹ", "യൂദാ", "വെളി"
]

def load_json_from_url(url):
    print("Fetching:", url)
    req = urllib.request.urlopen(url)
    return json.loads(req.read().decode('utf-8'))

def merge_all():
    print("Loading Malayalam BSI from SQLite...")
    mal_conn = sqlite3.connect(MAL_DB)
    mal_cur = mal_conn.cursor()

    print("Fetching NIV, NKJV, and KJV...")
    niv_data = load_json_from_url("https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_niv.json")
    nkjv_data = load_json_from_url("https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_nkjv.json")
    kjv_data = load_json_from_url("https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json")

    bible_data = []

    for idx in range(66):
        book_num = idx + 1
        name_en = ENGLISH_BOOKS[idx]
        name_ml = MALAYALAM_BOOKS[idx]
        abbrev_en = ENG_ABBREV[idx]
        abbrev_ml = MAL_ABBREV[idx]
        testament = "OT" if book_num <= 39 else "NT"

        # Get Malayalam verses
        mal_cur.execute("""
            SELECT v.chapter, v.verse, v.text
            FROM verse v
            JOIN book b ON v.book_id = b.id
            WHERE b.book_reference_id = ?
            ORDER BY v.chapter, v.verse
        """, (book_num,))
        mal_rows = mal_cur.fetchall()

        # Build lookup for English versions: (ch, verse) -> text
        niv_book = niv_data[idx]['chapters'] if idx < len(niv_data) else []
        nkjv_book = nkjv_data[idx]['chapters'] if idx < len(nkjv_data) else []
        kjv_book = kjv_data[idx]['chapters'] if idx < len(kjv_data) else []

        chapters = {}
        for ch, v, mal_text in mal_rows:
            if ch not in chapters:
                chapters[ch] = []

            # NIV verse
            ch_idx = ch - 1
            v_idx = v - 1
            niv_txt = ""
            if ch_idx < len(niv_book) and v_idx < len(niv_book[ch_idx]):
                niv_txt = str(niv_book[ch_idx][v_idx])

            # NKJV verse
            nkjv_txt = ""
            if ch_idx < len(nkjv_book) and v_idx < len(nkjv_book[ch_idx]):
                nkjv_txt = str(nkjv_book[ch_idx][v_idx])

            # KJV verse
            kjv_txt = ""
            if ch_idx < len(kjv_book) and v_idx < len(kjv_book[ch_idx]):
                kjv_txt = str(kjv_book[ch_idx][v_idx])

            chapters[ch].append({
                "v": v,
                "ml": mal_text,
                "niv": niv_txt,
                "nkjv": nkjv_txt,
                "kjv": kjv_txt
            })

        chapter_list = [chapters[k] for k in sorted(chapters.keys())]

        bible_data.append({
            "id": book_num,
            "name_en": name_en,
            "name_ml": name_ml,
            "abbrev_en": abbrev_en,
            "abbrev_ml": abbrev_ml,
            "testament": testament,
            "chapter_count": len(chapter_list),
            "chapters": chapter_list
        })

    mal_conn.close()

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(bible_data, f, ensure_ascii=False)

    size_mb = os.path.getsize(OUT_JSON) / (1024 * 1024)
    print(f"Updated multi-version Bible created! Size: {size_mb:.2f} MB")

if __name__ == '__main__':
    merge_all()
