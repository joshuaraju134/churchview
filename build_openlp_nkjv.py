import os
import json
import sqlite3
import urllib.request

DEST_DIR = r"C:\Users\Guest User\AppData\Roaming\openlp\data\bibles"
db_path = os.path.join(DEST_DIR, "New King James Version (NKJV).sqlite")

ENGLISH_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
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

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("CREATE TABLE metadata (key VARCHAR(255) PRIMARY KEY, value VARCHAR(255));")
cur.execute("CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, book_reference_id INTEGER, testament_reference_id INTEGER, name VARCHAR(50));")
cur.execute("CREATE INDEX ix_book_book_reference_id ON book (book_reference_id);")
cur.execute("CREATE INDEX ix_book_name ON book (name);")
cur.execute("CREATE TABLE verse (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER REFERENCES book(id), chapter INTEGER, verse INTEGER, text TEXT);")
cur.execute("CREATE INDEX ix_verse_id ON verse (id);")
cur.execute("CREATE INDEX ix_verse_book_id ON verse (book_id);")
cur.execute("CREATE INDEX ix_verse_chapter ON verse (chapter);")
cur.execute("CREATE INDEX ix_verse_verse ON verse (verse);")
cur.execute("CREATE INDEX ix_verse_text ON verse (text);")

cur.executemany("INSERT INTO metadata (key, value) VALUES (?, ?)", [
    ('version', '2'),
    ('name', 'New King James Version (NKJV)'),
    ('copyright', 'Thomas Nelson'),
    ('permissions', ''),
    ('book_name_language', '0')
])

req = urllib.request.urlopen("https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_nkjv.json")
books_data = json.loads(req.read().decode('utf-8'))

verse_rows = []
for b_idx in range(66):
    book_ref_id = b_idx + 1
    testament_ref_id = 1 if book_ref_id <= 39 else 2
    eng_name = ENGLISH_BOOKS[b_idx]

    cur.execute("INSERT INTO book (book_reference_id, testament_reference_id, name) VALUES (?, ?, ?)",
                (book_ref_id, testament_ref_id, eng_name))
    book_id = cur.lastrowid

    chapters = books_data[b_idx]['chapters']
    for ch_idx, verses in enumerate(chapters):
        ch_num = ch_idx + 1
        for v_idx, v_text in enumerate(verses):
            v_num = v_idx + 1
            verse_rows.append((book_id, ch_num, v_num, str(v_text)))

cur.executemany("INSERT INTO verse (book_id, chapter, verse, text) VALUES (?, ?, ?, ?)", verse_rows)
conn.commit()
conn.close()
print(f"OpenLP NKJV SQLite built successfully! Verses: {len(verse_rows)}")
