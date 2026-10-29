# -*- coding: utf-8 -*-
"""
Converter to parse all OpenLyrics Malayalam Christian songs from the repository archive,
apply accurate Malayalam-to-Latin transliteration, merge with beloved English Hymns,
and generate the full production VerseView songs database (songs_database.json).
"""

import os
import re
import json
import zipfile
import xml.etree.ElementTree as ET

ML_VOWELS = {
    'അ': 'a', 'ആ': 'aa', 'ഇ': 'i', 'ഈ': 'ee', 'ഉ': 'u', 'ഊ': 'oo',
    'ഋ': 'ri', 'എ': 'e', 'ഏ': 'ae', 'ഐ': 'ai', 'ഒ': 'o', 'ഓ': 'o', 'ഔ': 'au'
}
ML_MATRAS = {
    'ാ': 'aa', 'ി': 'i', 'ീ': 'ee', 'ു': 'u', 'ൂ': 'oo', 'ൃ': 'ri',
    'െ': 'e', 'േ': 'ae', 'ൈ': 'ai', 'ൊ': 'o', 'ോ': 'o', 'ൗ': 'au'
}
ML_CONSONANTS = {
    'ക': 'k', 'ഖ': 'kh', 'ഗ': 'g', 'ഘ': 'gh', 'ങ': 'ng',
    'ച': 'ch', 'ഛ': 'chh', 'ജ': 'j', 'ഝ': 'jh', 'ഞ': 'nj',
    'ട': 't', 'ഠ': 'th', 'ഡ': 'd', 'ഢ': 'dh', 'ണ': 'n',
    'ത': 'th', 'ഥ': 'th', 'ദ': 'd', 'ധ': 'dh', 'ന': 'n',
    'പ': 'p', 'ഫ': 'ph', 'ബ': 'b', 'ഭ': 'bh', 'മ': 'm',
    'യ': 'y', 'ര': 'r', 'ല': 'l', 'വ': 'v', 'ശ': 'sh',
    'ഷ': 'sh', 'സ': 's', 'ഹ': 'h', 'ള': 'l', 'ഴ': 'zh', 'റ': 'r'
}
ML_CHILLU = {
    'ൽ': 'l', 'ർ': 'r', 'ൻ': 'n', 'ൺ': 'n', 'ൿ': 'k', 'ൾ': 'l'
}

def transliterate(text):
    if not text:
        return ""
    lines = text.split('\n')
    trans_lines = []
    for line in lines:
        out = []
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            if ch in ML_CHILLU:
                out.append(ML_CHILLU[ch])
                i += 1
                continue
            if ch in ML_VOWELS:
                out.append(ML_VOWELS[ch])
                i += 1
                continue
            if ch in ML_CONSONANTS:
                cons = ML_CONSONANTS[ch]
                if i + 1 < n:
                    nxt = line[i + 1]
                    if nxt == '്':
                        # Check conjunct
                        if i + 2 < n and line[i + 2] in ML_CONSONANTS:
                            out.append(cons)
                            i += 2
                            continue
                        else:
                            out.append(cons)
                            i += 2
                            continue
                    elif nxt in ML_MATRAS:
                        out.append(cons + ML_MATRAS[nxt])
                        i += 2
                        continue
                    elif nxt == 'ം':
                        out.append(cons + 'am')
                        i += 2
                        continue
                out.append(cons + 'a')
                i += 1
                continue
            if ch == 'ം':
                out.append('m')
                i += 1
                continue
            out.append(ch)
            i += 1
        trans_line = ''.join(out)
        # Capitalize first letter of line
        if trans_line:
            trans_line = trans_line[0].upper() + trans_line[1:]
        trans_lines.append(trans_line)
    return '\n'.join(trans_lines)

def parse_xml_song(xml_text):
    # Remove XML namespaces for effortless parsing
    cleaned_xml = re.sub(r'\s+xmlns(:\w+)?="[^"]+"', '', xml_text, count=1)
    root = ET.fromstring(cleaned_xml)
    
    # 1. Title
    title_el = root.find('.//titles/title')
    title_ml = title_el.text.strip() if title_el is not None and title_el.text else "ഗാനം"
    
    # 2. Author / Book
    author_el = root.find('.//authors/author')
    author = author_el.text.strip() if author_el is not None and author_el.text else "Kristheeya Keerthanangal"
    if author == "Author Unknown":
        author = "Kristheeya Keerthanangal"
        
    # 3. Transliterated Title
    translit_title_el = root.find('.//titles/title[@translit="en"]')
    if translit_title_el is not None and translit_title_el.text:
        title_en = translit_title_el.text.strip().title()
    else:
        title_en = transliterate(title_ml).strip().title()
        
    # 4. Verses / Stanzas
    stanzas = []
    verse_nodes = root.findall('.//lyrics/verse')
    
    stanza_idx = 1
    for v_node in verse_nodes:
        name_attr = v_node.attrib.get('name', '').lower()
        
        # Extract lines text, treating <br/> as newline
        # ElementTree itertext() doesn't preserve <br/> as newline automatically unless serialized
        xml_str = ET.tostring(v_node, encoding='unicode')
        xml_str = re.sub(r'<br\s*/?>', '\n', xml_str)
        # remove tags
        text_lines = re.sub(r'<[^>]+>', '', xml_str).strip()
        if not text_lines:
            continue
            
        # Clean lines
        clean_lines = '\n'.join([l.strip() for l in text_lines.split('\n') if l.strip()])
        if not clean_lines:
            continue
            
        # Determine label
        if 'c' in name_attr or 'chorus' in clean_lines.lower() or clean_lines.startswith('പല്ലവി'):
            label = "Chorus / പല്ലവി"
            tag = "C"
        else:
            label = f"Stanza {stanza_idx} / {stanza_idx}-ാം ചരണം"
            tag = f"S{stanza_idx}"
            stanza_idx += 1
            
        # Transliterate lines
        en_lines = transliterate(clean_lines)
        
        stanzas.append({
            "label": label,
            "tag": tag,
            "ml": clean_lines,
            "en": en_lines
        })
        
    return {
        "title_ml": title_ml,
        "title_en": title_en,
        "book": author,
        "category": "Malayalam Christian Hymns",
        "stanzas": stanzas
    }

def main():
    zip_path = 'malayalam_songs_repo.zip'
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found.")
        return
        
    all_songs = []
    seen_titles = set()
    
    print("Parsing 1000+ Malayalam Christian Hymns from archive...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        xml_names = [f for f in zf.namelist() if f.endswith('.xml')]
        xml_names.sort()
        
        song_num = 1
        for name in xml_names:
            try:
                content = zf.read(name).decode('utf-8')
                song_obj = parse_xml_song(content)
                
                # Check for duplicates
                norm_title = re.sub(r'\s+', '', song_obj["title_ml"])
                if norm_title in seen_titles or len(song_obj["stanzas"]) == 0:
                    continue
                seen_titles.add(norm_title)
                
                song_obj["id"] = song_num
                song_obj["number"] = song_num
                all_songs.append(song_obj)
                song_num += 1
            except Exception as e:
                # ignore malformed individual XML
                continue

    print(f"Successfully processed {len(all_songs)} unique Malayalam Christian songs!")
    
    # Add top English Hymns
    english_hymns = [
        {
            "id": 2001,
            "number": 2001,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "അത്ഭുത കൃപ (Amazing Grace)",
            "title_en": "Amazing Grace",
            "stanzas": [
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "അത്ഭുത കൃപ! എത്ര മധുര ശബ്ദം\nഎന്നെപ്പോൽ ഒരു പാപിയെ രക്ഷിച്ചു!\nഞാൻ ഒരിക്കൽ നഷ്ടപ്പെട്ടു, എന്നാൽ ഇപ്പോൾ കണ്ടെത്തി;\nഅന്ധനായിരുന്നു ഞാൻ, ഇപ്പോൾ കാണുന്നു.",
                    "en": "Amazing grace! How sweet the sound\nThat saved a wretch like me!\nI once was lost, but now am found;\nWas blind, but now I see."
                },
                {
                    "label": "Stanza 2 / ചരണം 2",
                    "tag": "S2",
                    "ml": "കൃപയാണ് എന്റെ ഹൃദയത്തെ ഭയപ്പെടുത്താൻ പഠിപ്പിച്ചത്,\nകൃപയാണ് എന്റെ ഭയങ്ങളെ ശമിപ്പിച്ചത്;\nഞാൻ ആദ്യം വിശ്വസിച്ച ആ നാഴികയിൽ\nആ കൃപ എത്ര വിലപ്പെട്ടതായി തോന്നി!",
                    "en": "'Twas grace that taught my heart to fear,\nAnd grace my fears relieved;\nHow precious did that grace appear\nThe hour I first believed."
                },
                {
                    "label": "Stanza 3 / ചരണം 3",
                    "tag": "S3",
                    "ml": "അനേകം ആപത്തുകളിലൂടെയും പ്രയാസങ്ങളിലൂടെയും\nഞാൻ ഇതിനകം കടന്നുവന്നു;\nകൃപയാണ് എന്നെ ഇതുവരെ സുരക്ഷിതമായി കൊണ്ടുവന്നത്,\nകൃപ എന്നെ വീട്ടിലേക്ക് നയിക്കും.",
                    "en": "Through many dangers, toils, and snares,\nI have already come;\n'Tis grace hath brought me safe thus far,\nAnd grace will lead me home."
                },
                {
                    "label": "Stanza 4 / ചരണം 4",
                    "tag": "S4",
                    "ml": "നാം പതിനായിരം വർഷങ്ങൾ അവിടെ ആയിരുന്നാലും,\nസൂര്യനെപ്പോലെ ശോഭിച്ചുകൊണ്ട്,\nദൈവത്തിന്റെ സ്തുതി പാടുവാൻ ഉള്ള ദിനങ്ങൾ\nതുടങ്ങിയ നാളിനേക്കാൾ ഒട്ടും കുറവല്ല.",
                    "en": "When we've been there ten thousand years,\nBright shining as the sun,\nWe've no less days to sing God's praise\nThan when we'd first begun."
                }
            ]
        },
        {
            "id": 2002,
            "number": 2002,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "എന്റെ കർത്താവേ ദൈവമേ (How Great Thou Art)",
            "title_en": "How Great Thou Art",
            "stanzas": [
                {
                    "label": "Chorus / പല്ലവി",
                    "tag": "C",
                    "ml": "അപ്പോൾ എൻ ആത്മാവു പാടുന്നു രക്ഷകാ,\nനീ എത്ര വലിയവൻ! നീ എത്ര വലിയവൻ!\nഅപ്പോൾ എൻ ആത്മാവു പാടുന്നു രക്ഷകാ,\nനീ എത്ര വലിയവൻ! നീ എത്ര വലിയവൻ!",
                    "en": "Then sings my soul, my Saviour God, to Thee:\nHow great Thou art, how great Thou art!\nThen sings my soul, my Saviour God, to Thee:\nHow great Thou art, how great Thou art!"
                },
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "ഓ കർത്താവേ ദൈവമേ! വിസ്മയത്തോടെ ഞാൻ\nനിൻ കരങ്ങൾ തീർത്ത പ്രപഞ്ചം കാണുമ്പോൾ,\nനക്ഷത്രങ്ങളെ കാണുന്നു, ഗർജ്ജിക്കുന്ന ഇടിമുഴക്കം കേൾക്കുന്നു,\nപ്രപഞ്ചത്തിലെങ്ങും നിൻ ശക്തി വെളിപ്പെടുന്നു.",
                    "en": "O Lord my God! When I in awesome wonder\nConsider all the works Thy hand hath made,\nI see the stars, I hear the rolling thunder,\nThy pow'r throughout the universe displayed:"
                },
                {
                    "label": "Stanza 2 / ചരണം 2",
                    "tag": "S2",
                    "ml": "ദൈവം തൻ പുത്രനെ ഒഴിവാക്കാതെ,\nമരിക്കുവാൻ അയച്ചു എന്ന് ഞാൻ ചിന്തിക്കുമ്പോൾ,\nക്രൂശിൽ അവൻ സന്തോഷത്തോടെ എന്റെ ഭാരം വഹിച്ചു,\nഎന്റെ പാപം നീക്കുവാൻ രക്തം ചിന്തി മരിച്ചു.",
                    "en": "And when I think that God, His Son not sparing,\nSent Him to die, I scarce can take it in;\nThat on the cross, my burden gladly bearing,\nHe bled and died to take away my sin:"
                },
                {
                    "label": "Stanza 3 / ചരണം 3",
                    "tag": "S3",
                    "ml": "ക്രിസ്തു ആർപ്പോടെ വീണ്ടും വരുമ്പോൾ,\nഎന്നെ വീട്ടിലേക്ക് കൊണ്ടുപോകുമ്പോൾ, എൻ ഹൃദയത്തിൽ എന്ത് സന്തോഷം!\nഅപ്പോൾ ഞാൻ താണു വണങ്ങി ആരാധിക്കും,\nഎന്റെ ദൈവമേ, നീ എത്ര വലിയവൻ എന്ന് ഘോഷിക്കും!",
                    "en": "When Christ shall come with shout of acclamation\nAnd take me home, what joy shall fill my heart!\nThen I shall bow in humble adoration,\nAnd there proclaim, my God, how great Thou art!"
                }
            ]
        },
        {
            "id": 2003,
            "number": 2003,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "യേശുവിലുണ്ടൊരു നല്ല സ്നേഹിതൻ (What a Friend We Have in Jesus)",
            "title_en": "What a Friend We Have in Jesus",
            "stanzas": [
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "യേശുവിൽ എത്രയോ നല്ല സ്നേഹിതനുണ്ട്,\nനമ്മുടെ പാപങ്ങളും ദുഃഖങ്ങളും വഹിക്കുവാൻ!\nഎല്ലാം പ്രാർത്ഥനയിൽ ദൈവത്തിന്റെ അടുക്കൽ\nകൊണ്ടുവരുവാൻ എത്ര വലിയ ഭാഗ്യം!",
                    "en": "What a friend we have in Jesus,\nAll our sins and griefs to bear!\nWhat a privilege to carry\nEverything to God in prayer!"
                },
                {
                    "label": "Stanza 2 / ചരണം 2",
                    "tag": "S2",
                    "ml": "നമുക്ക് എത്രയോ പ്രാവശ്യം സമാധാനം നഷ്ടപ്പെടുന്നു,\nഎത്രയോ വേദനകൾ നാം വെറുതെ സഹിക്കുന്നു,\nകാരണം എല്ലാം നാം പ്രാർത്ഥനയിൽ\nദൈവത്തിന്റെ അടുക്കൽ സമർപ്പിക്കുന്നില്ല!",
                    "en": "Oh, what peace we often forfeit,\nOh, what needless pain we bear,\nAll because we do not carry\nEverything to God in prayer!"
                },
                {
                    "label": "Stanza 3 / ചരണം 3",
                    "tag": "S3",
                    "ml": "നമുക്ക് പരീക്ഷണങ്ങളും പ്രലോഭനങ്ങളുമുണ്ടോ?\nഎവിടെയെങ്കിലും കഷ്ടതകളുണ്ടോ?\nനാം ഒരിക്കലും നിരാശപ്പെടരുത്;\nപ്രാർത്ഥനയിൽ കർത്താവിങ്കൽ കൊണ്ടുപോവുക!",
                    "en": "Have we trials and temptations?\nIs there trouble anywhere?\nWe should never be discouraged;\nTake it to the Lord in prayer!"
                }
            ]
        },
        {
            "id": 2004,
            "number": 2004,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "യേശു എന്റേതല്ലോ (Blessed Assurance)",
            "title_en": "Blessed Assurance, Jesus is Mine",
            "stanzas": [
                {
                    "label": "Chorus / പല്ലവി",
                    "tag": "C",
                    "ml": "ഇതാണ് എൻ ചരിത്രം, ഇതാണ് എൻ ഗാനം,\nഎൻ രക്ഷകനെ റോജും വാഴ്ത്തുന്നു ഞാൻ;\nഇതാണ് എൻ ചരിത്രം, ഇതാണ് എൻ ഗാനം,\nഎൻ രക്ഷകനെ റോജും വാഴ്ത്തുന്നു ഞാൻ!",
                    "en": "This is my story, this is my song,\nPraising my Saviour all the day long;\nThis is my story, this is my song,\nPraising my Saviour all the day long!"
                },
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "ധന്യമാം ഉറപ്പ്, യേശു എന്റേതാണ്!\nദിവ്യ മഹത്വത്തിന്റെ ഒരു മുന്നാസ്വാദനം!\nരക്ഷയുടെ അവകാശി, ദൈവത്താൽ വിലയ്ക്കെടുക്കപ്പെട്ടവൻ,\nആത്മാവിനാൽ ജനിച്ചവൻ, രക്തത്താൽ കഴുകപ്പെട്ടവൻ.",
                    "en": "Blessed assurance, Jesus is mine!\nOh, what a foretaste of glory divine!\nHeir of salvation, purchase of God,\nBorn of His Spirit, washed in His blood."
                }
            ]
        },
        {
            "id": 2005,
            "number": 2005,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത് (Great is Thy Faithfulness)",
            "title_en": "Great is Thy Faithfulness",
            "stanzas": [
                {
                    "label": "Chorus / പല്ലവി",
                    "tag": "C",
                    "ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത്!\nപ്രഭാതം തോറും പുതിയ കൃപകൾ ഞാൻ കാണുന്നു;\nഎനിക്ക് ആവശ്യമുള്ളതെല്ലാം നിൻ കരം നൽകിയിരിക്കുന്നു;\nനിൻ വിശ്വസ്തത എത്രയോ വലിയത്, കർത്താവേ എനിക്ക്!",
                    "en": "Great is Thy faithfulness! Great is Thy faithfulness!\nMorning by morning new mercies I see;\nAll I have needed Thy hand hath provided;\nGreat is Thy faithfulness, Lord, unto me!"
                },
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത്, പിതാവാം ദൈവമേ,\nനിന്നിൽ തിരിയുന്നതിന്റെ യാതൊരു നിഴലുമില്ല;\nനീ ഒരിക്കലും മാറുന്നില്ല, നിൻ അനുകമ്പ പരാജയപ്പെടുന്നില്ല;\nനീ എന്നേക്കും നിലകൊള്ളുന്നതുപോലെ തന്നെ തുടരും.",
                    "en": "Great is Thy faithfulness, O God my Father,\nThere is no shadow of turning with Thee;\nThou changest not, Thy compassions, they fail not;\nAs Thou hast been Thou forever wilt be."
                }
            ]
        },
        {
            "id": 2006,
            "number": 2006,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "ക്രിസ്തുവിൽ മാത്രം (In Christ Alone)",
            "title_en": "In Christ Alone",
            "stanzas": [
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "ക്രിസ്തുവിൽ മാത്രം എന്റെ പ്രത്യാശ അധിഷ്ഠിതമാണ്;\nഅവനാണ് എന്റെ വെളിച്ചം, എന്റെ ശക്തി, എന്റെ ഗാനം;\nഈ മൂലക്കല്ല്, ഈ ഉറപ്പുള്ള പാറക്കല്ല്,\nകഠിനമായ വരൾച്ചയിലും കൊടുങ്കാറ്റിലും ഉറച്ചുനിൽക്കുന്നു.",
                    "en": "In Christ alone my hope is found,\nHe is my light, my strength, my song;\nThis Cornerstone, this solid Ground,\nFirm through the fiercest drought and storm."
                },
                {
                    "label": "Stanza 2 / ചരണം 2",
                    "tag": "S2",
                    "ml": "ക്രൂശിൽ യേശു മരിച്ചപ്പോൾ,\nദൈവത്തിന്റെ നീതി പൂർണ്ണമായി തൃപ്തിപ്പെട്ടു;\nഎല്ലാ പാപങ്ങളും അവന്റെ മേൽ ചുമത്തപ്പെട്ടു;\nക്രിസ്തുവിന്റെ മരണത്തിൽ ഞാൻ ജീവിക്കുന്നു.",
                    "en": "There on the cross as Jesus died,\nThe wrath of God was satisfied;\nFor every sin on Him was laid;\nHere in the death of Christ I live."
                }
            ]
        },
        {
            "id": 2007,
            "number": 2007,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "പരിശുദ്ധൻ! പരിശുദ്ധൻ! പരിശുദ്ധൻ! (Holy, Holy, Holy)",
            "title_en": "Holy, Holy, Holy! Lord God Almighty",
            "stanzas": [
                {
                    "label": "Stanza 1 / ചരണം 1",
                    "tag": "S1",
                    "ml": "പരിശുദ്ധൻ, പരിശുദ്ധൻ, പരിശുദ്ധൻ! സർവ്വശക്തനായ ദൈവമേ!\nഉഷസ്സിൽ ഞങ്ങളുടെ ഗാനം നിന്നിലേക്ക് ഉയരും;\nപരിശുദ്ധൻ, പരിശുദ്ധൻ, പരിശുദ്ധൻ! കരുണാമയനും സർവ്വശക്തനുമായവനേ!\nത്രിയേക ദൈവമേ, വാഴ്ത്തപ്പെട്ട ത്രിത്വമേ!",
                    "en": "Holy, Holy, Holy! Lord God Almighty!\nEarly in the morning our song shall rise to Thee;\nHoly, Holy, Holy! Merciful and Mighty!\nGod in three Persons, blessed Trinity!"
                }
            ]
        },
        {
            "id": 2008,
            "number": 2008,
            "category": "English Hymns",
            "book": "Hymns of Faith",
            "title_ml": "ദൈവത്തിന്നു മഹത്വം (To God Be the Glory)",
            "title_en": "To God Be the Glory",
            "stanzas": [
                {
                    "label": "Chorus / പല്ലവി",
                    "tag": "C",
                    "ml": "കർത്താവിനെ സ്തുതിപ്പിൻ, ഭൂമി അവൻ ശബ്ദം കേൾക്കട്ടെ!\nകർത്താവിനെ സ്തുതിപ്പിൻ, ജനങ്ങൾ സന്തോഷിക്കട്ടെ!\nപിതാവിന്റെ അടുക്കൽ യേശുപുത്രനിലൂടെ വരിക,\nഅവൻ ചെയ്ത വലിയ കാര്യങ്ങൾക്കായി അവനു മഹത്വം നൽകുക!",
                    "en": "Praise the Lord, praise the Lord, let the earth hear His voice!\nPraise the Lord, praise the Lord, let the people rejoice!\nO come to the Father, through Jesus the Son,\nAnd give Him the glory, great things He hath done!"
                }
            ]
        }
    ]
    
    all_songs.extend(english_hymns)
    
    out_file = 'songs_database.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(all_songs, f, ensure_ascii=False, indent=2)
        
    print(f"\n========================================================")
    print(f"  SUCCESS! Total songs in VerseView database: {len(all_songs)}")
    print(f"  Saved to: {os.path.abspath(out_file)}")
    print(f"  Size: {os.path.getsize(out_file) / 1024:.1f} KB")
    print(f"========================================================")

if __name__ == '__main__':
    main()
