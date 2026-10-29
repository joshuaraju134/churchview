// BroadcastChannel for cross-window real-time sync with 0ms latency
// Church of God (Full Gospel) in India, Alappuzha Town
const channel = new BroadcastChannel('church_bible_projector');

let currentMainMode = 'BIBLE'; // 'BIBLE' | 'SONGS'

let bibleData = [];
let songsData = [];

// Bible Navigation State
let liveBookIndex = 42; // Default to John (index 42 in 0-based list)
let liveChapter = 3;   // Default to Chapter 3
let liveVerse = 16;    // Default to Verse 16

let viewingBookIndex = 42;
let viewingChapter = 3;
let bookSearchQuery = '';
let bookFilterTestament = 'ALL'; // 'ALL' | 'NT' | 'OT'

// Songs Navigation State (VerseView style)
let viewingSongIndex = 0;   // Index in songsData
let viewingStanzaIndex = 0; // Index in song.stanzas
let liveSongIndex = -1;     // -1 when verse is live
let liveStanzaIndex = -1;
let songSearchQuery = '';
let songFilterCategory = 'ALL'; // 'ALL' | 'MALAYALAM' | 'ENGLISH'

// Display & Presentation State
let currentEnglishVersion = 'nkjv'; // 'nkjv' | 'niv' | 'kjv'
let scriptureLayout = 'dual';        // 'dual' | 'malayalam' | 'english'
let verseHistory = [];               // History of projected verses
let showWatermark = true;
let displayMode = 'VERSE';          // 'VERSE' | 'DEFAULT' | 'BLACK'
let currentTheme = 'dark-midnight';
let malFontSize = 46;
let engFontSize = 30;

// Common Bible book abbreviations mapping
const BOOK_LOOKUP = {
    // English
    'gen': 0, 'genesis': 0, 'exo': 1, 'exodus': 1, 'ex': 1, 'lev': 2, 'leviticus': 2,
    'num': 3, 'numbers': 3, 'deu': 4, 'deut': 4, 'deuteronomy': 4, 'dt': 4,
    'jos': 5, 'joshua': 5, 'jdg': 6, 'judges': 6, 'rut': 7, 'ruth': 7,
    '1sa': 8, '1samuel': 8, '1sam': 8, '1 samuel': 8, '1 sam': 8,
    '2sa': 9, '2samuel': 9, '2sam': 9, '2 samuel': 9, '2 sam': 9,
    '1ki': 10, '1kings': 10, '1 kings': 10,
    '2ki': 11, '2kings': 11, '2 kings': 11,
    '1ch': 12, '1chronicles': 12, '1 chron': 12, '1 chronicles': 12,
    '2ch': 13, '2chronicles': 13, '2 chron': 13, '2 chronicles': 13,
    'ezr': 14, 'ezra': 14, 'neh': 15, 'nehemiah': 15, 'est': 16, 'esther': 16,
    'job': 17, 'psa': 18, 'psalms': 18, 'ps': 18, 'psalm': 18,
    'pro': 19, 'proverbs': 19, 'pr': 19, 'ecc': 20, 'ecclesiastes': 20,
    'sng': 21, 'song': 21, 'song of songs': 21, 'song of solomon': 21,
    'isa': 22, 'isaiah': 22, 'jer': 23, 'jeremiah': 23, 'lam': 24, 'lamentations': 24,
    'ezk': 25, 'ezekiel': 25, 'dan': 26, 'daniel': 26, 'hos': 27, 'hosea': 27,
    'jol': 28, 'joel': 28, 'amo': 29, 'amos': 29, 'oba': 30, 'obadiah': 30,
    'jon': 31, 'jonah': 31, 'mic': 32, 'micah': 32, 'nah': 33, 'nahum': 33,
    'hab': 34, 'habakkuk': 34, 'zep': 35, 'zephaniah': 35,
    'hag': 36, 'haggai': 36, 'zec': 37, 'zechariah': 37, 'mal': 38, 'malachi': 38,
    'mat': 39, 'matt': 39, 'matthew': 39, 'mt': 39,
    'mrk': 40, 'mark': 40, 'mk': 40,
    'luk': 41, 'luke': 41, 'lk': 41,
    'jhn': 42, 'john': 42, 'jn': 42,
    'act': 43, 'acts': 43,
    'rom': 44, 'romans': 44, 'ro': 44,
    '1co': 45, '1cor': 45, '1corinthians': 45, '1 cor': 45, '1 corinthians': 45,
    '2co': 46, '2cor': 46, '2corinthians': 46, '2 cor': 46, '2 corinthians': 46,
    'gal': 47, 'galatians': 47, 'eph': 48, 'ephesians': 48,
    'php': 49, 'phil': 49, 'philippians': 49, 'col': 50, 'colossians': 50,
    '1th': 51, '1thess': 51, '1thessalonians': 51, '1 thess': 51,
    '2th': 52, '2thess': 52, '2thessalonians': 52, '2 thess': 52,
    '1ti': 53, '1tim': 53, '1timothy': 53, '1 tim': 53,
    '2ti': 54, '2tim': 54, '2timothy': 54, '2 tim': 54,
    'tit': 55, 'titus': 55, 'phm': 56, 'philemon': 56, 'heb': 57, 'hebrews': 57,
    'jas': 58, 'james': 58,
    '1pe': 59, '1pet': 59, '1peter': 59, '1 pet': 59,
    '2pe': 60, '2pet': 60, '2peter': 60, '2 pet': 60,
    '1jn': 61, '1john': 61, '1 john': 61,
    '2jn': 62, '2john': 62, '2 john': 62,
    '3jn': 63, '3john': 63, '3 john': 63,
    'jud': 64, 'jude': 64,
    'rev': 65, 'revelation': 65,

    // Malayalam common abbreviations
    'ഉല്പ': 0, 'ഉല്പത്തി': 0, 'പുറ': 1, 'പുറപ്പാടു': 1, 'പുറപ്പാട്': 1,
    'ലേവ്യ': 2, 'സംഖ്യാ': 3, 'ആവർ': 4, 'ആവർത്തനം': 4,
    'യോശു': 5, 'യോശുവ': 5, 'ന്യായാ': 6, 'ന്യായാധിപന്മാർ': 6, 'രൂത്ത്': 7,
    '1ശമൂ': 8, '1 ശമൂവേൽ': 8, '2ശമൂ': 9, '2 ശമൂവേൽ': 9,
    '1രാജാ': 10, '1 രാജാക്കന്മാർ': 10, '2രാജാ': 11, '2 രാജാക്കന്മാർ': 11,
    '1ദിന': 12, '2ദിന': 13, 'എസ്രാ': 14, 'നെഹെ': 15, 'നെഹെമ്യാവു': 15,
    'എസ്ഥേ': 16, 'എസ്ഥേർ': 16, 'ഇയ്യോ': 17, 'ഇയ്യോബ്': 17,
    'സങ്കീ': 18, 'സങ്കീർത്തനങ്ങൾ': 18, 'സങ്കീർത്തനം': 18,
    'സദൃ': 19, 'സദൃശവാക്യങ്ങൾ': 19, 'സഭാ': 20, 'സഭാപ്രസംഗി': 20,
    'ഉത്ത': 21, 'ഉത്തമഗീതം': 21, 'യെശ': 22, 'യെശയ്യാവു': 22,
    'യിരെ': 23, 'യിരെമ്യാവു': 23, 'വിലാ': 24, 'വിലാപങ്ങൾ': 24,
    'യെഹെ': 25, 'യെഹെസ്കേൽ': 25, 'ദാനീ': 26, 'ദാനീയേൽ': 26,
    'ഹോശേ': 27, 'യോവേ': 28, 'ആമോ': 29, 'ആമോസ്': 29,
    'മത്താ': 39, 'മത്തായി': 39, 'മർക്കൊ': 40, 'മർക്കൊസ്': 40,
    'ലൂക്കൊ': 41, 'ലൂക്കൊസ്': 41, 'യോഹ': 42, 'യോഹന്നാൻ': 42,
    'പ്രവൃ': 43, 'പ്രവൃത്തികൾ': 43, 'റോമ': 44, 'റോമർ': 44,
    '1കൊരി': 45, '1 കൊരിന്ത്യർ': 45, '2കൊരി': 46, '2 കൊരിന്ത്യർ': 46,
    'ഗലാ': 47, 'ഗലാത്യർ': 47, 'എഫെ': 48, 'എഫെസ്യർ': 48,
    'ഫിലി': 49, 'ഫിലിപ്പിയർ': 49, 'കൊലൊ': 50, 'കൊലൊസ്സ്യർ': 50,
    '1തെസ്സ': 51, '2തെസ്സ': 52, '1തിമൊ': 53, '2തിമൊ': 54,
    'തീത്തോ': 55, 'തീത്തൊസ്': 55, 'ഫിലേ': 56, 'ഫിലേമോൻ': 56,
    'എബ്രാ': 57, 'എബ്രായർ': 57, 'യാക്കോ': 58, 'യാക്കോബ്': 58,
    '1പത്രൊ': 59, '2പത്രൊ': 60, '1യോഹ': 61, '2യോഹ': 62, '3യോഹ': 63,
    'യൂദാ': 64, 'വെളി': 65, 'വെളിപ്പാടു': 65, 'വെളിപ്പാട്': 65
};

function getVerseEnglish(v) {
    if (!v) return '';
    if (currentEnglishVersion === 'nkjv' && v.nkjv) return v.nkjv;
    if (currentEnglishVersion === 'niv' && v.niv) return v.niv;
    if (currentEnglishVersion === 'kjv' && v.kjv) return v.kjv;
    return v.nkjv || v.niv || v.kjv || v.en || '';
}

async function init() {
    try {
        // 1. Fetch Scriptures
        const bibleRes = await fetch('bible_dual.json');
        bibleData = await bibleRes.json();

        // 2. Fetch VerseView Songs Database
        try {
            const songsRes = await fetch('songs_database.json');
            songsData = await songsRes.json();
        } catch (e) {
            console.warn('Could not load songs_database.json, initializing empty songs list', e);
            songsData = [];
        }

        // 3. Merge custom user songs from localStorage
        loadCustomSongs();

        // Hide loading overlay
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';

        // Render Bible books & Chapter 1
        renderBookGrid();
        renderChapterBar(bibleData[viewingBookIndex]);
        loadChapter(viewingBookIndex, viewingChapter);

        // Render VerseView Songs list & initial song
        renderSongList();
        if (songsData.length > 0) {
            selectSong(0);
        }

        loadScriptureLayout();
        loadHoldingConfig();
        loadHistory();
        setupEventListeners();

        // Initial launch verse (John 3:16)
        setTimeout(() => {
            projectVerse(liveBookIndex, liveChapter, liveVerse);
        }, 300);

    } catch (err) {
        console.error('Failed to initialize ChurchView:', err);
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.innerHTML = `
                <div style="color: #ff6b6b; padding: 20px; text-align: center;">
                    <h2>Error Loading ChurchView Data</h2>
                    <p>${err.message}</p>
                </div>
            `;
        }
    }
}

/* ========================================================= */
/* MAIN MODE SWITCHER (SCRIPTURES vs SONGS)                  */
/* ========================================================= */
function switchMainMode(mode) {
    currentMainMode = mode;
    const isBible = (mode === 'BIBLE');

    // Update Header Tab Buttons
    const btnBible = document.getElementById('nav-btn-bible');
    const btnSongs = document.getElementById('nav-btn-songs');
    if (btnBible) btnBible.classList.toggle('active', isBible);
    if (btnSongs) btnSongs.classList.toggle('active', !isBible);

    // Toggle Left Sidebars
    const sidebarBible = document.getElementById('sidebar-bible');
    const sidebarSongs = document.getElementById('sidebar-songs');
    if (sidebarBible) sidebarBible.style.display = isBible ? 'flex' : 'none';
    if (sidebarSongs) sidebarSongs.style.display = isBible ? 'none' : 'flex';

    // Toggle Center Panels
    const centerBible = document.getElementById('center-bible-panel');
    const centerSongs = document.getElementById('center-songs-panel');
    if (centerBible) centerBible.style.display = isBible ? 'flex' : 'none';
    if (centerSongs) centerSongs.style.display = isBible ? 'none' : 'flex';

    // Toggle Bible English Version Dropdown
    const versionWrap = document.getElementById('bible-version-selector-wrap');
    if (versionWrap) versionWrap.style.display = isBible ? 'flex' : 'none';

    // Update Search Bar Placeholder
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.value = '';
        if (isBible) {
            searchInput.placeholder = "Quick Jump: Type 'John 3:16', 'റോമ 8:28', 'Gen 1:1'...";
        } else {
            searchInput.placeholder = "Quick Song Jump: Type #12, 'Krooshin', 'Amazing Grace'...";
        }
    }
}

/* ========================================================= */
/* 1. BOOKS SIDEBAR SEARCH & SELECTION                      */
/* ========================================================= */
function renderBookGrid() {
    const otContainer = document.getElementById('ot-books-list');
    const ntContainer = document.getElementById('nt-books-list');
    const otSection = document.getElementById('ot-section');
    const ntSection = document.getElementById('nt-section');
    const emptyMsg = document.getElementById('books-empty-msg');
    const countBadge = document.getElementById('books-count-badge');

    if (!otContainer || !ntContainer) return;
    otContainer.innerHTML = '';
    ntContainer.innerHTML = '';

    const cleanQuery = bookSearchQuery.trim().toLowerCase();
    let visibleCount = 0;
    let otCount = 0;
    let ntCount = 0;

    bibleData.forEach((b, idx) => {
        // Testament filtering
        if (bookFilterTestament === 'OT' && b.testament !== 'OT') return;
        if (bookFilterTestament === 'NT' && b.testament !== 'NT') return;

        // Search query filtering
        if (cleanQuery) {
            const matchEn = b.name_en.toLowerCase().includes(cleanQuery);
            const matchMl = b.name_ml.includes(cleanQuery);
            const matchAbbrevEn = b.abbrev_en ? b.abbrev_en.toLowerCase().includes(cleanQuery) : false;
            const matchAbbrevMl = b.abbrev_ml ? b.abbrev_ml.includes(cleanQuery) : false;
            const matchNumber = String(idx + 1) === cleanQuery;

            if (!matchEn && !matchMl && !matchAbbrevEn && !matchAbbrevMl && !matchNumber) {
                return;
            }
        }

        visibleCount++;
        if (b.testament === 'OT') otCount++;
        else ntCount++;

        const btn = document.createElement('button');
        btn.className = `book-btn ${idx === viewingBookIndex ? 'active' : ''}`;
        btn.id = `book-btn-${idx}`;

        const bookNum = (idx + 1 < 10) ? `0${idx + 1}` : `${idx + 1}`;
        btn.innerHTML = `
            <div class="book-btn-left">
                <span class="book-order-pill">${bookNum}</span>
                <div class="book-names-col">
                    <span class="book-name-ml">${b.name_ml}</span>
                    <span class="book-name-en">${b.name_en}</span>
                </div>
            </div>
            <span class="book-ch-pill">${b.chapter_count}ch</span>
        `;
        btn.onclick = () => selectBook(idx);

        if (b.testament === 'OT') {
            otContainer.appendChild(btn);
        } else {
            ntContainer.appendChild(btn);
        }
    });

    if (countBadge) {
        countBadge.innerText = `${visibleCount} Books`;
    }

    if (otSection) otSection.style.display = (otCount > 0) ? 'block' : 'none';
    if (ntSection) ntSection.style.display = (ntCount > 0) ? 'block' : 'none';
    if (emptyMsg) emptyMsg.style.display = (visibleCount === 0) ? 'flex' : 'none';
}

function filterBooks(query) {
    bookSearchQuery = query || '';
    const clearBtn = document.getElementById('book-search-clear-btn');
    if (clearBtn) {
        clearBtn.style.display = bookSearchQuery ? 'block' : 'none';
    }
    renderBookGrid();
}

function clearBookSearch() {
    const input = document.getElementById('book-search-input');
    if (input) input.value = '';
    filterBooks('');
}

function setBookFilter(testament) {
    bookFilterTestament = testament || 'ALL';
    document.querySelectorAll('.book-search-container .pill-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (testament === 'ALL') document.getElementById('book-tab-all')?.classList.add('active');
    if (testament === 'NT') document.getElementById('book-tab-nt')?.classList.add('active');
    if (testament === 'OT') document.getElementById('book-tab-ot')?.classList.add('active');
    renderBookGrid();
}

function selectBook(bookIdx) {
    viewingBookIndex = bookIdx;
    viewingChapter = 1;

    document.querySelectorAll('.book-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`book-btn-${bookIdx}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    const book = bibleData[bookIdx];
    renderChapterBar(book);
    loadChapter(bookIdx, 1);
}

function selectBookView(bookIdx, chapterNum) {
    viewingBookIndex = bookIdx;
    viewingChapter = chapterNum;

    document.querySelectorAll('.book-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`book-btn-${bookIdx}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    const book = bibleData[bookIdx];
    renderChapterBar(book);
    loadChapter(bookIdx, chapterNum);
}

/* ========================================================= */
/* 2. SCRIPTURES CHAPTER & VERSE NAVIGATOR                   */
/* ========================================================= */
function renderChapterBar(book) {
    const chDropdown = document.getElementById('chapter-select-dropdown');
    if (chDropdown) {
        chDropdown.innerHTML = '';
        for (let ch = 1; ch <= book.chapter_count; ch++) {
            const opt = document.createElement('option');
            opt.value = ch;
            opt.innerText = `Chapter ${ch}`;
            if (ch === viewingChapter) opt.selected = true;
            chDropdown.appendChild(opt);
        }
        chDropdown.onchange = (e) => {
            const selectedCh = parseInt(e.target.value);
            viewingChapter = selectedCh;
            loadChapter(viewingBookIndex, selectedCh);
            chDropdown.blur();
        };
    }

    const bar = document.getElementById('chapter-pills-bar');
    if (!bar) return;
    bar.innerHTML = '';

    for (let ch = 1; ch <= book.chapter_count; ch++) {
        const pill = document.createElement('button');
        pill.className = `chapter-pill ${ch === viewingChapter ? 'active' : ''}`;
        pill.id = `ch-pill-${ch}`;
        pill.innerText = ch;
        const targetCh = ch;
        pill.onclick = () => {
            viewingChapter = targetCh;
            loadChapter(viewingBookIndex, targetCh);
            pill.blur();
        };
        bar.appendChild(pill);
    }
}

function loadChapter(bookIdx, chapterNum) {
    viewingBookIndex = bookIdx;
    viewingChapter = chapterNum;

    const book = bibleData[bookIdx];

    const chDropdown = document.getElementById('chapter-select-dropdown');
    if (chDropdown) chDropdown.value = chapterNum;

    document.querySelectorAll('.chapter-pill').forEach(p => p.classList.remove('active'));
    const activePill = document.getElementById(`ch-pill-${chapterNum}`);
    if (activePill) {
        activePill.classList.add('active');
        activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }

    const container = document.getElementById('verses-scroll-container');
    container.innerHTML = '';

    const chapterIndex = chapterNum - 1;
    const verses = (book.chapters && book.chapters[chapterIndex]) ? book.chapters[chapterIndex] : [];

    const headerEl = document.getElementById('chapter-header-text');
    if (headerEl) {
        const isLiveHere = (liveSongIndex === -1 && bookIdx === liveBookIndex && chapterNum === liveChapter);
        const liveBook = bibleData[liveBookIndex];
        const statusHtml = isLiveHere
            ? `<span class="live-status-pill live-here">🔴 LIVE: v.${liveVerse}</span>`
            : `<span class="live-status-pill live-other">📺 Screen: ${liveBook ? liveBook.name_en : ''} ${liveChapter}:${liveVerse}</span>`;
        headerEl.innerHTML = `${book.name_ml} (${book.name_en}) ${statusHtml}`;
    }

    verses.forEach(v => {
        const engText = getVerseEnglish(v);
        const isLive = (liveSongIndex === -1 && bookIdx === liveBookIndex && chapterNum === liveChapter && v.v === liveVerse);
        const card = document.createElement('div');
        card.className = `verse-card ${isLive ? 'selected-live' : ''}`;
        card.id = `verse-card-${v.v}`;
        card.innerHTML = `
            <div class="verse-num-badge">
                <span class="v-num">${v.v}</span>
                <span class="live-tag">LIVE</span>
            </div>
            <div class="verse-text-content">
                <div class="verse-ml" style="font-size: ${malFontSize}px;">${v.ml}</div>
                <div class="verse-en" style="font-size: ${engFontSize}px;">${engText}</div>
            </div>
        `;

        card.onclick = () => {
            projectVerse(bookIdx, chapterNum, v.v);
        };

        container.appendChild(card);
    });
}

function scrollToVerse(verseNum) {
    const card = document.getElementById(`verse-card-${verseNum}`);
    if (card) {
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function projectVerse(bookIdx, chapterNum, verseNum) {
    liveSongIndex = -1; // Clear live song
    liveStanzaIndex = -1;

    liveBookIndex = bookIdx;
    liveChapter = chapterNum;
    liveVerse = verseNum;

    viewingBookIndex = bookIdx;
    viewingChapter = chapterNum;

    if (displayMode !== 'VERSE') {
        displayMode = 'VERSE';
        updateDisplayModeUI();
    }

    const book = bibleData[bookIdx];
    const chapterIndex = chapterNum - 1;
    const verses = book.chapters[chapterIndex] || [];
    const verseObj = verses.find(x => x.v === verseNum) || verses[0] || { ml: '' };
    const engText = getVerseEnglish(verseObj);
    const versionLabel = currentEnglishVersion.toUpperCase();

    document.querySelectorAll('.book-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`book-btn-${bookIdx}`);
    if (activeBtn) activeBtn.classList.add('active');

    const chDropdown = document.getElementById('chapter-select-dropdown');
    if (chDropdown) chDropdown.value = chapterNum;
    document.querySelectorAll('.chapter-pill').forEach(p => p.classList.remove('active'));
    const activePill = document.getElementById(`ch-pill-${chapterNum}`);
    if (activePill) activePill.classList.add('active');

    const headerEl = document.getElementById('chapter-header-text');
    if (headerEl) {
        headerEl.innerHTML = `${book.name_ml} (${book.name_en}) <span class="live-status-pill live-here">🔴 LIVE: v.${verseNum}</span>`;
    }

    document.querySelectorAll('.verse-card').forEach(c => c.classList.remove('selected-live'));
    const activeCard = document.getElementById(`verse-card-${verseNum}`);
    if (activeCard) activeCard.classList.add('selected-live');

    addVerseToHistory(bookIdx, chapterNum, verseNum);

    // Update Live Mirror Box
    const previewRefEl = document.getElementById('preview-ref');
    if (previewRefEl) {
        if (scriptureLayout === 'malayalam') {
            previewRefEl.innerText = `${book.name_ml} ${chapterNum}:${verseNum} (BSI)`;
        } else if (scriptureLayout === 'english') {
            previewRefEl.innerText = `${book.name_en} ${chapterNum}:${verseNum} (${versionLabel})`;
        } else {
            previewRefEl.innerText = `${book.name_ml} ${chapterNum}:${verseNum} | ${book.name_en} (${versionLabel})`;
        }
    }
    const pMl = document.getElementById('preview-ml');
    const pEn = document.getElementById('preview-en');
    if (pMl) pMl.innerText = verseObj.ml;
    if (pEn) pEn.innerText = engText;

    // Send payload to Projector Window
    const payload = {
        type: 'VERSE_CHANGE',
        mode: 'VERSE',
        displayMode: 'VERSE',
        scriptureLayout: scriptureLayout,
        bookMl: book.name_ml,
        bookEn: book.name_en,
        chapter: chapterNum,
        verse: verseNum,
        textMl: verseObj.ml,
        textEn: engText,
        versionLabel: versionLabel,
        showWatermark: showWatermark,
        showChurchLogo: showWatermark,
        isBlank: false,
        theme: currentTheme,
        malFontSize: parseInt(document.getElementById('proj-font-ml').value),
        engFontSize: parseInt(document.getElementById('proj-font-en').value)
    };

    channel.postMessage(payload);
    localStorage.setItem('church_bible_state', JSON.stringify(payload));
    localStorage.setItem('church_live_state', JSON.stringify(payload));
}

function nextVerse() {
    const book = bibleData[liveBookIndex];
    if (!book) return;
    const chapterIndex = liveChapter - 1;
    const verses = book.chapters[chapterIndex] || [];

    if (liveVerse < verses.length) {
        const nextV = liveVerse + 1;
        if (viewingBookIndex !== liveBookIndex || viewingChapter !== liveChapter) {
            selectBookView(liveBookIndex, liveChapter);
        }
        projectVerse(liveBookIndex, liveChapter, nextV);
        scrollToVerse(nextV);
    } else if (liveChapter < book.chapter_count) {
        const nextCh = liveChapter + 1;
        selectBookView(liveBookIndex, nextCh);
        projectVerse(liveBookIndex, nextCh, 1);
        scrollToVerse(1);
    } else if (liveBookIndex < 65) {
        const nextBk = liveBookIndex + 1;
        selectBookView(nextBk, 1);
        projectVerse(nextBk, 1, 1);
        scrollToVerse(1);
    }
}

function prevVerse() {
    if (liveVerse > 1) {
        const prevV = liveVerse - 1;
        if (viewingBookIndex !== liveBookIndex || viewingChapter !== liveChapter) {
            selectBookView(liveBookIndex, liveChapter);
        }
        projectVerse(liveBookIndex, liveChapter, prevV);
        scrollToVerse(prevV);
    } else if (liveChapter > 1) {
        const prevCh = liveChapter - 1;
        const book = bibleData[liveBookIndex];
        const prevVerses = book.chapters[prevCh - 1] || [];
        const lastVerse = prevVerses.length || 1;
        selectBookView(liveBookIndex, prevCh);
        projectVerse(liveBookIndex, prevCh, lastVerse);
        scrollToVerse(lastVerse);
    } else if (liveBookIndex > 0) {
        const prevBk = liveBookIndex - 1;
        const book = bibleData[prevBk];
        const lastCh = book.chapter_count || 1;
        const verses = book.chapters[lastCh - 1] || [];
        const lastVerse = verses.length || 1;
        selectBookView(prevBk, lastCh);
        projectVerse(prevBk, lastCh, lastVerse);
        scrollToVerse(lastVerse);
    }
}

/* ========================================================= */
/* 3. VERSEVIEW SONGS FEATURE (BIBLE SONGS & HYMNS)          */
/* ========================================================= */
function loadCustomSongs() {
    try {
        const savedCustom = localStorage.getItem('church_custom_songs');
        if (savedCustom) {
            const parsed = JSON.parse(savedCustom);
            if (Array.isArray(parsed) && parsed.length > 0) {
                // Merge without duplicates
                parsed.forEach(customSong => {
                    if (!songsData.some(s => s.id === customSong.id || s.number === customSong.number)) {
                        songsData.push(customSong);
                    }
                });
            }
        }
    } catch (e) {
        console.error('Failed to parse custom songs', e);
    }
}

function renderSongList() {
    const container = document.getElementById('songs-list-container');
    const emptyMsg = document.getElementById('songs-empty-msg');
    if (!container) return;
    container.innerHTML = '';

    const cleanQuery = songSearchQuery.trim().toLowerCase();
    let visibleCount = 0;

    songsData.forEach((s, idx) => {
        // Filter by Category/Book
        if (songFilterCategory === 'MALAYALAM' && s.category === 'English Hymns') return;
        if (songFilterCategory === 'ENGLISH' && s.category !== 'English Hymns') return;

        // Search Query (Number, Title Malayalam, Title English, or Lyrics text)
        if (cleanQuery) {
            const matchNum = String(s.number) === cleanQuery || `song ${s.number}`.includes(cleanQuery) || `#${s.number}`.includes(cleanQuery);
            const matchTitleMl = s.title_ml ? s.title_ml.toLowerCase().includes(cleanQuery) : false;
            const matchTitleEn = s.title_en ? s.title_en.toLowerCase().includes(cleanQuery) : false;
            const matchCat = s.category ? s.category.toLowerCase().includes(cleanQuery) : false;
            
            let matchLyrics = false;
            if (s.stanzas) {
                matchLyrics = s.stanzas.some(st => 
                    (st.ml && st.ml.toLowerCase().includes(cleanQuery)) ||
                    (st.en && st.en.toLowerCase().includes(cleanQuery))
                );
            }

            if (!matchNum && !matchTitleMl && !matchTitleEn && !matchCat && !matchLyrics) {
                return;
            }
        }

        visibleCount++;

        const isViewing = (idx === viewingSongIndex);
        const isLive = (liveSongIndex === idx);

        const btn = document.createElement('button');
        btn.className = `song-item-btn ${isViewing ? 'active' : ''} ${isLive ? 'live-projecting' : ''}`;
        btn.id = `song-item-${idx}`;

        const songNumStr = (s.number < 10) ? `#0${s.number}` : `#${s.number}`;
        const stanzaCountStr = s.stanzas ? `${s.stanzas.length} stanzas` : '';

        btn.innerHTML = `
            <div class="song-item-left">
                <span class="song-num-badge">${songNumStr}</span>
                <div class="song-titles-col">
                    <span class="song-item-title-ml">${s.title_ml}</span>
                    <span class="song-item-title-en">${s.title_en}</span>
                </div>
            </div>
            <span class="song-meta-pill">${stanzaCountStr}</span>
        `;

        btn.onclick = () => selectSong(idx);
        container.appendChild(btn);
    });

    if (emptyMsg) {
        emptyMsg.style.display = (visibleCount === 0) ? 'flex' : 'none';
    }
}

function filterSongs(query) {
    songSearchQuery = query || '';
    const clearBtn = document.getElementById('song-search-clear-btn');
    if (clearBtn) {
        clearBtn.style.display = songSearchQuery ? 'block' : 'none';
    }
    renderSongList();
}

function clearSongSearch() {
    const input = document.getElementById('song-search-input');
    if (input) input.value = '';
    filterSongs('');
}

function setSongFilter(filter) {
    songFilterCategory = filter || 'ALL';
    document.querySelectorAll('.song-search-container .pill-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (filter === 'ALL') document.getElementById('song-tab-all')?.classList.add('active');
    if (filter === 'MALAYALAM') document.getElementById('song-tab-ml')?.classList.add('active');
    if (filter === 'ENGLISH') document.getElementById('song-tab-en')?.classList.add('active');
    renderSongList();
}

function selectSong(songIdx) {
    viewingSongIndex = songIdx;
    viewingStanzaIndex = 0;

    document.querySelectorAll('.song-item-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`song-item-${songIdx}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    renderSongView(songIdx);
}

function renderSongView(songIdx) {
    const song = songsData[songIdx];
    if (!song) return;

    // Header Details
    const elNum = document.getElementById('song-active-number');
    const elTitleMl = document.getElementById('song-active-title-ml');
    const elTitleEn = document.getElementById('song-active-title-en');
    const elCat = document.getElementById('song-active-category');

    if (elNum) elNum.innerText = (song.number < 10) ? `Song #0${song.number}` : `Song #${song.number}`;
    if (elTitleMl) elTitleMl.innerText = song.title_ml || '';
    if (elTitleEn) elTitleEn.innerText = `${song.title_en || ''} • ${song.book || 'VerseView Song'}`;
    if (elCat) elCat.innerText = song.category || 'Worship';

    // Stanzas Pills Bar
    const pillsBar = document.getElementById('stanzas-pills-bar');
    if (pillsBar) {
        pillsBar.innerHTML = '';
        (song.stanzas || []).forEach((st, stIdx) => {
            const pill = document.createElement('button');
            const isLive = (liveSongIndex === songIdx && liveStanzaIndex === stIdx);
            pill.className = `stanza-pill ${stIdx === viewingStanzaIndex ? 'active' : ''} ${isLive ? 'live-projecting' : ''}`;
            pill.id = `stanza-pill-${stIdx}`;
            pill.innerHTML = `<span>${st.label}</span>`;
            pill.onclick = () => {
                viewingStanzaIndex = stIdx;
                projectSong(songIdx, stIdx);
                scrollToStanza(stIdx);
            };
            pillsBar.appendChild(pill);
        });
    }

    // Stanzas Scrollable Cards Container
    const container = document.getElementById('stanzas-scroll-container');
    if (!container) return;
    container.innerHTML = '';

    (song.stanzas || []).forEach((st, stIdx) => {
        const isLive = (liveSongIndex === songIdx && liveStanzaIndex === stIdx);
        const card = document.createElement('div');
        card.className = `stanza-card ${stIdx === viewingStanzaIndex ? 'active' : ''} ${isLive ? 'live-projecting' : ''}`;
        card.id = `stanza-card-${stIdx}`;

        card.innerHTML = `
            <div class="stanza-card-top">
                <span class="stanza-label-badge">${st.label}</span>
                ${isLive ? '<span class="stanza-live-tag">🔴 LIVE ON PROJECTOR</span>' : ''}
            </div>
            <div class="stanza-text-ml" style="font-size: ${Math.round(malFontSize * 0.46)}px;">${st.ml}</div>
            <div class="stanza-text-en" style="font-size: ${Math.round(engFontSize * 0.48)}px;">${st.en || ''}</div>
        `;

        card.onclick = () => {
            viewingStanzaIndex = stIdx;
            projectSong(songIdx, stIdx);
        };

        container.appendChild(card);
    });
}

function scrollToStanza(stIdx) {
    const card = document.getElementById(`stanza-card-${stIdx}`);
    if (card) {
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function projectSong(songIdx, stanzaIdx) {
    liveSongIndex = songIdx;
    liveStanzaIndex = stanzaIdx;
    viewingSongIndex = songIdx;
    viewingStanzaIndex = stanzaIdx;

    if (displayMode !== 'VERSE') {
        displayMode = 'VERSE';
        updateDisplayModeUI();
    }

    const song = songsData[songIdx];
    if (!song) return;
    const stanza = (song.stanzas && song.stanzas[stanzaIdx]) ? song.stanzas[stanzaIdx] : { label: 'Stanza', ml: '', en: '' };

    // Update Pills & Cards active states
    renderSongView(songIdx);
    scrollToStanza(stanzaIdx);

    // Update Live Mirror Box
    const previewRefEl = document.getElementById('preview-ref');
    if (previewRefEl) {
        if (scriptureLayout === 'malayalam') {
            previewRefEl.innerText = `ഗാനം #${song.number}: ${song.title_ml} • [${stanza.label}]`;
        } else if (scriptureLayout === 'english') {
            previewRefEl.innerText = `Song #${song.number}: ${song.title_en} • [${stanza.label}]`;
        } else {
            previewRefEl.innerText = `ഗാനം #${song.number}: ${song.title_ml} | ${song.title_en} • [${stanza.label}]`;
        }
    }
    const pMl = document.getElementById('preview-ml');
    const pEn = document.getElementById('preview-en');
    if (pMl) pMl.innerText = stanza.ml;
    if (pEn) pEn.innerText = stanza.en || '';

    // Broadcast to Projector Window via BroadcastChannel
    const payload = {
        type: 'SONG_CHANGE',
        mode: 'VERSE',
        displayMode: 'VERSE',
        scriptureLayout: scriptureLayout,
        songNumber: song.number,
        songTitleMl: song.title_ml,
        songTitleEn: song.title_en,
        stanzaLabel: stanza.label,
        lyricsMl: stanza.ml,
        lyricsEn: stanza.en || '',
        showWatermark: showWatermark,
        showChurchLogo: showWatermark,
        isBlank: false,
        theme: currentTheme,
        malFontSize: parseInt(document.getElementById('proj-font-ml').value),
        engFontSize: parseInt(document.getElementById('proj-font-en').value)
    };

    channel.postMessage(payload);
    localStorage.setItem('church_live_state', JSON.stringify(payload));
}

function projectCurrentSongStanza() {
    projectSong(viewingSongIndex, viewingStanzaIndex);
}

function nextStanza() {
    if (liveSongIndex === -1) {
        // If not currently projecting song, project viewed stanza
        projectSong(viewingSongIndex, viewingStanzaIndex);
        return;
    }

    const song = songsData[liveSongIndex];
    if (!song || !song.stanzas) return;

    if (liveStanzaIndex < song.stanzas.length - 1) {
        const nextSt = liveStanzaIndex + 1;
        projectSong(liveSongIndex, nextSt);
    } else if (liveSongIndex < songsData.length - 1) {
        // Advance to next song, first stanza
        const nextSongIdx = liveSongIndex + 1;
        selectSong(nextSongIdx);
        projectSong(nextSongIdx, 0);
    }
}

function prevStanza() {
    if (liveSongIndex === -1) {
        projectSong(viewingSongIndex, viewingStanzaIndex);
        return;
    }

    if (liveStanzaIndex > 0) {
        const prevSt = liveStanzaIndex - 1;
        projectSong(liveSongIndex, prevSt);
    } else if (liveSongIndex > 0) {
        // Go to previous song, last stanza
        const prevSongIdx = liveSongIndex - 1;
        const prevSong = songsData[prevSongIdx];
        const lastStanzaIdx = (prevSong && prevSong.stanzas) ? prevSong.stanzas.length - 1 : 0;
        selectSong(prevSongIdx);
        projectSong(prevSongIdx, lastStanzaIdx);
    }
}

/* ========================================================= */
/* UNIFIED NAVIGATION (VERSES OR STANZAS)                    */
/* ========================================================= */
function navigateNext() {
    if (currentMainMode === 'SONGS') {
        nextStanza();
    } else {
        nextVerse();
    }
}

function navigatePrev() {
    if (currentMainMode === 'SONGS') {
        prevStanza();
    } else {
        prevVerse();
    }
}

/* ========================================================= */
/* ADD CUSTOM SONG MODAL (VerseView style)                   */
/* ========================================================= */
function openAddSongModal() {
    // Generate next song number
    const maxNum = songsData.reduce((acc, s) => Math.max(acc, s.number || 0), 0);
    document.getElementById('new-song-num').value = maxNum + 1;
    document.getElementById('new-song-cat').value = 'Worship';
    document.getElementById('new-song-title-ml').value = '';
    document.getElementById('new-song-title-en').value = '';
    document.getElementById('new-song-lyrics-ml').value = '';
    document.getElementById('new-song-lyrics-en').value = '';

    const modal = document.getElementById('add-song-modal');
    if (modal) modal.style.display = 'flex';
}

function closeAddSongModal() {
    const modal = document.getElementById('add-song-modal');
    if (modal) modal.style.display = 'none';
}

function saveCustomSong() {
    const num = parseInt(document.getElementById('new-song-num').value) || (songsData.length + 1);
    const cat = document.getElementById('new-song-cat').value.trim() || 'Custom Worship';
    const titleMl = document.getElementById('new-song-title-ml').value.trim();
    const titleEn = document.getElementById('new-song-title-en').value.trim();
    const rawMl = document.getElementById('new-song-lyrics-ml').value.trim();
    const rawEn = document.getElementById('new-song-lyrics-en').value.trim();

    if (!titleMl && !titleEn) {
        alert('Please enter a song title in Malayalam or English.');
        return;
    }
    if (!rawMl) {
        alert('Please enter the song lyrics.');
        return;
    }

    // Parse stanzas separated by blank lines
    const blocksMl = rawMl.split(/\n\s*\n/).map(b => b.trim()).filter(Boolean);
    const blocksEn = rawEn ? rawEn.split(/\n\s*\n/).map(b => b.trim()).filter(Boolean) : [];

    const stanzas = blocksMl.map((bText, idx) => {
        let label = `Stanza ${idx + 1} / ചരണം ${idx + 1}`;
        if (idx === 0 && (bText.startsWith('പല്ലവി') || bText.toLowerCase().startsWith('chorus'))) {
            label = 'Chorus / പല്ലവി';
        }
        return {
            label: label,
            tag: (idx === 0) ? 'C' : `S${idx}`,
            ml: bText,
            en: blocksEn[idx] || ''
        };
    });

    const newSong = {
        id: Date.now(),
        number: num,
        category: cat,
        book: 'Church of God Songs',
        title_ml: titleMl || titleEn,
        title_en: titleEn || titleMl,
        stanzas: stanzas
    };

    // Save to custom songs in localStorage
    try {
        let customList = [];
        const saved = localStorage.getItem('church_custom_songs');
        if (saved) customList = JSON.parse(saved);
        customList.push(newSong);
        localStorage.setItem('church_custom_songs', JSON.stringify(customList));
    } catch (e) {
        console.error('Failed to save custom song to localStorage', e);
    }

    songsData.push(newSong);
    renderSongList();
    closeAddSongModal();

    // Select and view the newly added song!
    const newIdx = songsData.length - 1;
    selectSong(newIdx);
    alert(`Song #${num} "${newSong.title_ml}" successfully added to your ChurchView library!`);
}

/* ========================================================= */
/* UNIFIED SEARCH (SCRIPTURES & SONGS)                       */
/* ========================================================= */
function parseAndSearchScripture(query) {
    if (!query) return;
    const clean = query.trim().toLowerCase();

    // If currently in Songs Mode, search songs
    if (currentMainMode === 'SONGS') {
        // 1. Check if user typed song number (e.g. "12", "#12", "song 12")
        const numMatch = clean.match(/^(?:song|#)?\s*(\d+)$/);
        if (numMatch) {
            const num = parseInt(numMatch[1]);
            const foundIdx = songsData.findIndex(s => s.number === num);
            if (foundIdx !== -1) {
                selectSong(foundIdx);
                projectSong(foundIdx, 0);
                document.getElementById('search-input').blur();
                return;
            }
        }

        // 2. Search song title
        const foundIdx = songsData.findIndex(s =>
            (s.title_en && s.title_en.toLowerCase().includes(clean)) ||
            (s.title_ml && s.title_ml.includes(clean))
        );
        if (foundIdx !== -1) {
            selectSong(foundIdx);
            projectSong(foundIdx, 0);
            document.getElementById('search-input').blur();
            return;
        }

        // 3. Filter song sidebar with query
        filterSongs(query);
        return;
    }

    // Bible Reference Search (e.g. "John 3:16", "യോഹ 3:16", "Gen 1:1")
    const refMatch = clean.match(/^([1-3]?\s*[\p{L}]+)?\s*(\d+)(?:[:\s\.](\d+))?$/u);

    if (refMatch) {
        let bookName = (refMatch[1] || '').trim().replace(/\s+/g, '');
        let ch = parseInt(refMatch[2]);
        let v = refMatch[3] ? parseInt(refMatch[3]) : 1;

        let targetBookIndex = viewingBookIndex;

        if (bookName) {
            if (BOOK_LOOKUP[bookName] !== undefined) {
                targetBookIndex = BOOK_LOOKUP[bookName];
            } else {
                const foundIdx = bibleData.findIndex(b =>
                    b.name_en.toLowerCase().startsWith(bookName) ||
                    b.name_ml.startsWith(bookName) ||
                    b.abbrev_en.toLowerCase().startsWith(bookName) ||
                    b.abbrev_ml.startsWith(bookName)
                );
                if (foundIdx !== -1) targetBookIndex = foundIdx;
            }
        }

        const book = bibleData[targetBookIndex];
        if (book) {
            if (ch > book.chapter_count) ch = book.chapter_count;
            if (ch < 1) ch = 1;

            selectBookView(targetBookIndex, ch);
            projectVerse(targetBookIndex, ch, v);
            scrollToVerse(v);
            document.getElementById('search-input').blur();
            return;
        }
    }

    // Keyword search in current chapter
    const currentVerses = bibleData[viewingBookIndex].chapters[viewingChapter - 1] || [];
    const found = currentVerses.find(x => {
        const eng = getVerseEnglish(x).toLowerCase();
        return x.ml.includes(query) || eng.includes(clean);
    });
    if (found) {
        projectVerse(viewingBookIndex, viewingChapter, found.v);
        scrollToVerse(found.v);
    }
}

/* ========================================================= */
/* DEFAULT SCREEN & BLANK TOGGLES                            */
/* ========================================================= */
function toggleDefaultScreen() {
    displayMode = (displayMode === 'DEFAULT') ? 'VERSE' : 'DEFAULT';
    updateDisplayModeUI();
    broadcastDisplayMode();
}

function toggleBlank() {
    displayMode = (displayMode === 'BLACK') ? 'VERSE' : 'BLACK';
    updateDisplayModeUI();
    broadcastDisplayMode();
}

function updateDisplayModeUI() {
    const defaultBtn = document.getElementById('default-screen-btn');
    const blankBtn = document.getElementById('blank-btn');
    const previewVerseMode = document.getElementById('preview-verse-mode');
    const previewDefaultMode = document.getElementById('preview-default-mode');
    const previewBlankOverlay = document.getElementById('preview-blank-overlay');

    if (defaultBtn) {
        defaultBtn.classList.toggle('active', displayMode === 'DEFAULT');
    }
    if (blankBtn) {
        blankBtn.classList.toggle('blank-active', displayMode === 'BLACK');
        blankBtn.innerHTML = (displayMode === 'BLACK') ? `<span class="icon">⬛</span> UNBLANK (B)` : `<span class="icon">⬛</span> BLANK (B)`;
    }

    if (previewVerseMode && previewDefaultMode && previewBlankOverlay) {
        if (displayMode === 'DEFAULT') {
            previewVerseMode.style.display = 'none';
            previewDefaultMode.style.display = 'flex';
            previewBlankOverlay.style.display = 'none';
        } else if (displayMode === 'BLACK') {
            previewVerseMode.style.display = 'flex';
            previewDefaultMode.style.display = 'none';
            previewBlankOverlay.style.display = 'flex';
        } else {
            // VERSE OR SONG
            previewVerseMode.style.display = 'flex';
            previewDefaultMode.style.display = 'none';
            previewBlankOverlay.style.display = 'none';
        }
    }
}

function broadcastDisplayMode() {
    const payload = {
        type: 'DISPLAY_MODE',
        mode: displayMode,
        displayMode: displayMode,
        isBlank: (displayMode === 'BLACK'),
        isDefaultScreen: (displayMode === 'DEFAULT'),
        showWatermark: showWatermark
    };
    channel.postMessage(payload);

    const saved = localStorage.getItem('church_live_state');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            parsed.mode = displayMode;
            parsed.displayMode = displayMode;
            parsed.isBlank = (displayMode === 'BLACK');
            localStorage.setItem('church_live_state', JSON.stringify(parsed));
        } catch (e) {}
    }
}

function openProjectorWindow() {
    window.open('projector.html', 'ChurchProjectorWindow', 'width=1280,height=720,menubar=no,toolbar=no,location=no,status=no');
}

/* ========================================================= */
/* EVENT LISTENERS & KEYBOARD SHORTCUTS                      */
/* ========================================================= */
function setupEventListeners() {
    // English Version dropdown
    const versionSelect = document.getElementById('english-version-select');
    if (versionSelect) {
        versionSelect.value = currentEnglishVersion;
        versionSelect.addEventListener('change', (e) => {
            currentEnglishVersion = e.target.value;
            loadChapter(viewingBookIndex, viewingChapter);
            if (liveSongIndex === -1) {
                projectVerse(liveBookIndex, liveChapter, liveVerse);
            }
            versionSelect.blur();
        });
    }

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
        // If typing in any input field or textarea
        if (document.activeElement && (
            document.activeElement.tagName === 'INPUT' || 
            document.activeElement.tagName === 'TEXTAREA'
        )) {
            if (e.key === 'Enter') {
                if (document.activeElement.id === 'search-input') {
                    parseAndSearchScripture(document.getElementById('search-input').value);
                } else if (document.activeElement.id === 'book-search-input') {
                    // Enter in book search selects top filtered book
                    const firstBookBtn = document.querySelector('.books-scroll-area .book-btn');
                    if (firstBookBtn) firstBookBtn.click();
                } else if (document.activeElement.id === 'song-search-input') {
                    // Enter in song search selects top filtered song
                    const firstSongBtn = document.querySelector('.songs-scroll-area .song-item-btn');
                    if (firstSongBtn) firstSongBtn.click();
                }
            }
            return;
        }

        if (document.activeElement && (document.activeElement.tagName === 'SELECT' || document.activeElement.tagName === 'BUTTON')) {
            if (e.key.startsWith('Arrow') || e.key === ' ') {
                document.activeElement.blur();
            }
        }

        switch (e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
            case 'PageDown':
            case ' ':
                e.preventDefault();
                navigateNext();
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
            case 'PageUp':
                e.preventDefault();
                navigatePrev();
                break;
            case 'w':
            case 'W':
                e.preventDefault();
                toggleDefaultScreen();
                break;
            case 'b':
            case 'B':
                e.preventDefault();
                toggleBlank();
                break;
            case 'o':
            case 'O':
                e.preventDefault();
                openProjectorWindow();
                break;
            case '/':
                e.preventDefault();
                document.getElementById('search-input').focus();
                document.getElementById('search-input').select();
                break;
            case 'm':
            case 'M':
                // Toggle between Bible and Songs
                e.preventDefault();
                switchMainMode(currentMainMode === 'BIBLE' ? 'SONGS' : 'BIBLE');
                break;
        }
    });

    // Font size sliders
    document.getElementById('proj-font-ml').addEventListener('input', (e) => {
        document.getElementById('val-font-ml').innerText = `${e.target.value}px`;
        channel.postMessage({
            type: 'STYLE_UPDATE',
            malFontSize: parseInt(e.target.value),
            engFontSize: parseInt(document.getElementById('proj-font-en').value),
            theme: currentTheme,
            showWatermark: showWatermark
        });
    });

    document.getElementById('proj-font-en').addEventListener('input', (e) => {
        document.getElementById('val-font-en').innerText = `${e.target.value}px`;
        channel.postMessage({
            type: 'STYLE_UPDATE',
            malFontSize: parseInt(document.getElementById('proj-font-ml').value),
            engFontSize: parseInt(e.target.value),
            theme: currentTheme,
            showWatermark: showWatermark
        });
    });

    // Theme selector
    document.getElementById('theme-select').addEventListener('change', (e) => {
        currentTheme = e.target.value;
        channel.postMessage({
            type: 'STYLE_UPDATE',
            theme: currentTheme,
            malFontSize: parseInt(document.getElementById('proj-font-ml').value),
            engFontSize: parseInt(document.getElementById('proj-font-en').value),
            showWatermark: showWatermark
        });
    });

    // Watermark toggle
    const watermarkCheck = document.getElementById('toggle-watermark-check');
    if (watermarkCheck) {
        watermarkCheck.addEventListener('change', (e) => {
            showWatermark = e.target.checked;
            const pWatermark = document.getElementById('preview-watermark-bg');
            const pCorner = document.getElementById('preview-corner-tag');
            if (pWatermark) pWatermark.style.display = showWatermark ? 'flex' : 'none';
            if (pCorner) pCorner.style.display = showWatermark ? 'block' : 'none';
            channel.postMessage({
                type: 'TOGGLE_WATERMARK',
                showWatermark: showWatermark
            });
        });
    }
}

/* ========================================================= */
/* DEFAULT / HOLDING SCREEN CUSTOMIZER                       */
/* ========================================================= */
const DEFAULT_HOLDING_CONFIG = {
    orgTitle: 'CHURCH OF GOD (FULL GOSPEL) IN INDIA',
    townName: 'ALAPPUZHA TOWN',
    motto: 'WELCOME • WORSHIP • FELLOWSHIP',
    quote: '“Let everything that has breath praise the LORD.” • Psalm 150:6',
    accentColor: '#be185d',
    logoDataUrl: ''
};
let currentHoldingConfig = { ...DEFAULT_HOLDING_CONFIG };

function loadHoldingConfig() {
    const saved = localStorage.getItem('church_default_screen_config');
    if (saved) {
        try {
            currentHoldingConfig = { ...DEFAULT_HOLDING_CONFIG, ...JSON.parse(saved) };
        } catch (e) {
            console.error('Error parsing holding config', e);
        }
    }
    applyHoldingConfigPresenter(currentHoldingConfig);
}

function applyHoldingConfigPresenter(config) {
    if (!config) return;
    const miniOrg = document.getElementById('mini-title-cog');
    const miniTown = document.getElementById('mini-title-town');
    const miniMotto = document.getElementById('mini-motto');
    const miniQuote = document.getElementById('mini-verse-quote');
    const miniImg = document.getElementById('mini-emblem-img');
    const miniBarTop = document.getElementById('mini-accent-bar-top');
    const miniBarBottom = document.getElementById('mini-accent-bar-bottom');

    if (miniOrg && config.orgTitle !== undefined) miniOrg.innerText = config.orgTitle;
    if (miniTown && config.townName !== undefined) {
        miniTown.innerText = config.townName;
        if (config.accentColor) miniTown.style.color = config.accentColor;
    }
    if (miniMotto && config.motto !== undefined) miniMotto.innerText = config.motto;
    if (miniQuote && config.quote !== undefined) miniQuote.innerText = config.quote;

    if (miniImg && config.logoDataUrl) {
        miniImg.src = config.logoDataUrl;
    } else if (miniImg && config.logoDataUrl === '') {
        miniImg.src = 'alappuzha_cog_logo.png';
    }

    if (config.accentColor) {
        const grad = `linear-gradient(90deg, ${config.accentColor}, #e11d48, ${config.accentColor})`;
        if (miniBarTop) miniBarTop.style.background = grad;
        if (miniBarBottom) miniBarBottom.style.background = grad;
    }
}

function openDefaultScreenModal() {
    document.getElementById('edit-def-org').value = currentHoldingConfig.orgTitle || '';
    document.getElementById('edit-def-town').value = currentHoldingConfig.townName || '';
    document.getElementById('edit-def-motto').value = currentHoldingConfig.motto || '';
    document.getElementById('edit-def-verse').value = currentHoldingConfig.quote || '';
    document.getElementById('edit-def-color').value = currentHoldingConfig.accentColor || '#be185d';
    document.getElementById('edit-def-logo-file').value = '';
    
    const statusHint = document.getElementById('logo-status-hint');
    if (statusHint) {
        statusHint.innerText = currentHoldingConfig.logoDataUrl ? 'Custom uploaded logo active' : 'Official COG Kerala Emblem';
    }

    const modal = document.getElementById('default-screen-modal');
    if (modal) modal.style.display = 'flex';
}

function closeDefaultScreenModal() {
    const modal = document.getElementById('default-screen-modal');
    if (modal) modal.style.display = 'none';
}

function saveDefaultScreenConfig() {
    const org = document.getElementById('edit-def-org').value.trim();
    const town = document.getElementById('edit-def-town').value.trim();
    const motto = document.getElementById('edit-def-motto').value.trim();
    const quote = document.getElementById('edit-def-verse').value.trim();
    const color = document.getElementById('edit-def-color').value;
    const fileInput = document.getElementById('edit-def-logo-file');

    const updateAndBroadcast = (logoUrl) => {
        currentHoldingConfig = {
            orgTitle: org || DEFAULT_HOLDING_CONFIG.orgTitle,
            townName: town || DEFAULT_HOLDING_CONFIG.townName,
            motto: motto || DEFAULT_HOLDING_CONFIG.motto,
            quote: quote || DEFAULT_HOLDING_CONFIG.quote,
            accentColor: color,
            logoDataUrl: (logoUrl !== undefined) ? logoUrl : currentHoldingConfig.logoDataUrl
        };

        localStorage.setItem('church_default_screen_config', JSON.stringify(currentHoldingConfig));
        applyHoldingConfigPresenter(currentHoldingConfig);

        channel.postMessage({
            type: 'UPDATE_DEFAULT_SCREEN',
            config: currentHoldingConfig
        });

        closeDefaultScreenModal();
    };

    if (fileInput && fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            updateAndBroadcast(e.target.result);
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        updateAndBroadcast();
    }
}

function resetDefaultScreenConfig() {
    if (confirm('Reset default screen text, colors and logo back to original Alappuzha Town settings?')) {
        currentHoldingConfig = { ...DEFAULT_HOLDING_CONFIG };
        localStorage.removeItem('church_default_screen_config');
        applyHoldingConfigPresenter(currentHoldingConfig);

        channel.postMessage({
            type: 'UPDATE_DEFAULT_SCREEN',
            config: currentHoldingConfig
        });

        closeDefaultScreenModal();
    }
}

/* ========================================================= */
/* DISPLAY LAYOUT MODES (DUAL, MALAYALAM, ENGLISH)          */
/* ========================================================= */
function loadScriptureLayout() {
    const saved = localStorage.getItem('church_scripture_layout');
    if (saved) {
        scriptureLayout = saved;
    }
    applyScriptureLayoutUI(scriptureLayout);
}

function setScriptureDisplayMode(mode) {
    scriptureLayout = mode || 'dual';
    localStorage.setItem('church_scripture_layout', scriptureLayout);
    applyScriptureLayoutUI(scriptureLayout);

    if (liveSongIndex !== -1) {
        projectSong(liveSongIndex, liveStanzaIndex);
    } else {
        projectVerse(liveBookIndex, liveChapter, liveVerse);
    }

    channel.postMessage({
        type: 'LAYOUT_CHANGE',
        scriptureLayout: scriptureLayout
    });
}

function applyScriptureLayoutUI(layout) {
    document.querySelectorAll('#screen-layout-control .seg-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-mode') === layout);
    });

    const layoutSelect = document.getElementById('scripture-layout-select');
    if (layoutSelect) layoutSelect.value = layout;

    const previewBox = document.getElementById('preview-box');
    if (previewBox) {
        previewBox.classList.remove('layout-dual', 'layout-malayalam', 'layout-english');
        previewBox.classList.add(`layout-${layout}`);
    }
}

/* ========================================================= */
/* RECENT VERSES HISTORY & QUICK RECALL                      */
/* ========================================================= */
function loadHistory() {
    const saved = localStorage.getItem('church_verse_history');
    if (saved) {
        try {
            verseHistory = JSON.parse(saved);
        } catch (e) {
            verseHistory = [];
        }
    }
    renderHistoryChips();
}

function addVerseToHistory(bookIdx, chapter, verse) {
    const book = bibleData[bookIdx];
    if (!book) return;

    const refEn = `${book.name_en} ${chapter}:${verse}`;
    const refMl = `${book.name_ml} ${chapter}:${verse}`;

    verseHistory = verseHistory.filter(item => !(item.bookIdx === bookIdx && item.chapter === chapter && item.verse === verse));

    verseHistory.unshift({
        bookIdx,
        chapter,
        verse,
        refEn,
        refMl,
        timestamp: Date.now()
    });

    if (verseHistory.length > 25) {
        verseHistory.pop();
    }

    localStorage.setItem('church_verse_history', JSON.stringify(verseHistory));
    renderHistoryChips();
}

function renderHistoryChips() {
    const container = document.getElementById('history-chips-list');
    if (!container) return;

    if (verseHistory.length === 0) {
        container.innerHTML = `<span class="history-empty-hint">Projected verses will appear here for 1-click recall</span>`;
        return;
    }

    container.innerHTML = '';
    verseHistory.forEach((item) => {
        const isCurrent = (liveSongIndex === -1 && item.bookIdx === liveBookIndex && item.chapter === liveChapter && item.verse === liveVerse);
        const chip = document.createElement('button');
        chip.className = `history-chip ${isCurrent ? 'current' : ''}`;
        chip.title = `Jump back to ${item.refMl} / ${item.refEn}`;
        chip.innerHTML = `<span>${item.refEn}</span> <span style="opacity: 0.65; font-size: 10px;">(${item.refMl})</span>`;
        chip.onclick = () => {
            selectBookView(item.bookIdx, item.chapter);
            projectVerse(item.bookIdx, item.chapter, item.verse);
            scrollToVerse(item.verse);
        };
        container.appendChild(chip);
    });
}

function clearVerseHistory() {
    verseHistory = [];
    localStorage.removeItem('church_verse_history');
    renderHistoryChips();
}

window.onload = init;
