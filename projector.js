// Audience / Projector Display Receiver
// Church of God (Full Gospel) in India, Alappuzha Town
const channel = new BroadcastChannel('church_bible_projector');

const elRef = document.getElementById('projector-ref');
const elMl = document.getElementById('projector-ml');
const elEn = document.getElementById('projector-en');
const elContainer = document.getElementById('projector-container');
const elBlackOverlay = document.getElementById('black-overlay');
const elDefaultOverlay = document.getElementById('default-screen-overlay');
const elWatermarkBg = document.getElementById('projector-watermark-bg');
const elWatermarkCorner = document.getElementById('projector-corner-watermark');

let currentMode = 'VERSE'; // 'VERSE' | 'DEFAULT' | 'BLACK'
let scriptureLayout = 'dual'; // 'dual' | 'malayalam' | 'english'
let currentBookMl = 'യോഹന്നാൻ';
let currentBookEn = 'John';
let currentChapterNum = 3;
let currentVerseNum = 16;
let currentVersionLabel = 'NKJV';

function setDisplayMode(mode) {
    currentMode = mode || 'VERSE';
    if (currentMode === 'BLACK') {
        if (elBlackOverlay) elBlackOverlay.classList.add('active');
        if (elDefaultOverlay) elDefaultOverlay.classList.remove('active');
    } else if (currentMode === 'DEFAULT') {
        if (elDefaultOverlay) elDefaultOverlay.classList.add('active');
        if (elBlackOverlay) elBlackOverlay.classList.remove('active');
    } else {
        // 'VERSE' mode
        if (elBlackOverlay) elBlackOverlay.classList.remove('active');
        if (elDefaultOverlay) elDefaultOverlay.classList.remove('active');
    }
}

function setScriptureLayout(layout) {
    scriptureLayout = layout || 'dual';
    document.body.classList.remove('layout-dual', 'layout-malayalam', 'layout-english');
    document.body.classList.add(`layout-${scriptureLayout}`);
    updateRefBadge();
}

let isCurrentSong = false;
let currentSongPayload = null;

function updateRefBadge() {
    if (!elRef) return;
    if (isCurrentSong && currentSongPayload) {
        const p = currentSongPayload;
        if (scriptureLayout === 'malayalam') {
            elRef.innerText = `ഗാനം #${p.songNumber}: ${p.songTitleMl} • [${p.stanzaLabel}]`;
        } else if (scriptureLayout === 'english') {
            elRef.innerText = `Song #${p.songNumber}: ${p.songTitleEn} • [${p.stanzaLabel}]`;
        } else {
            elRef.innerText = `ഗാനം #${p.songNumber}: ${p.songTitleMl} | ${p.songTitleEn} • [${p.stanzaLabel}]`;
        }
    } else {
        if (scriptureLayout === 'malayalam') {
            elRef.innerText = `${currentBookMl} ${currentChapterNum}:${currentVerseNum} (BSI)`;
        } else if (scriptureLayout === 'english') {
            elRef.innerText = `${currentBookEn} ${currentChapterNum}:${currentVerseNum} (${currentVersionLabel})`;
        } else {
            elRef.innerText = `${currentBookMl} ${currentChapterNum}:${currentVerseNum}  |  ${currentBookEn} (${currentVersionLabel})`;
        }
    }
}

function setWatermark(show) {
    const isVisible = (show !== false);
    if (elWatermarkBg) elWatermarkBg.classList.toggle('hidden', !isVisible);
    if (elWatermarkCorner) elWatermarkCorner.classList.toggle('hidden', !isVisible);
}

function setTheme(theme) {
    document.body.className = `projector-body theme-${theme || 'dark-midnight'} layout-${scriptureLayout}`;
}

function applyPayload(data) {
    if (!data) return;

    // 1. Watermark visibility
    if (data.showWatermark !== undefined) {
        setWatermark(data.showWatermark);
    } else if (data.showChurchLogo !== undefined) {
        setWatermark(data.showChurchLogo);
    }

    // 2. Scripture / Song Layout (Dual, Malayalam BSI Only, English Only)
    if (data.scriptureLayout) {
        setScriptureLayout(data.scriptureLayout);
    }

    // 3. Display mode (Blackout, Default Holding Screen, or Content)
    if (data.mode) {
        setDisplayMode(data.mode);
    } else if (data.displayMode) {
        setDisplayMode(data.displayMode);
    } else if (data.isBlank !== undefined && data.type !== 'VERSE_CHANGE' && data.type !== 'SONG_CHANGE') {
        setDisplayMode(data.isBlank ? 'BLACK' : 'VERSE');
    }

    // 4. Song Content (VerseView style)
    if (data.type === 'SONG_CHANGE') {
        if (elRef) elRef.style.display = 'none';
        isCurrentSong = true;
        currentSongPayload = data;
        if (elContainer) elContainer.classList.add('verse-fade');
        setTimeout(() => {
            updateRefBadge();

            if (elMl) elMl.innerText = data.lyricsMl || '';
            if (elEn) elEn.innerText = data.lyricsEn || '';

            if (data.malFontSize && elMl) elMl.style.fontSize = `${data.malFontSize}px`;
            if (data.engFontSize && elEn) elEn.style.fontSize = `${data.engFontSize}px`;
            if (data.theme) setTheme(data.theme);

            if (elContainer) elContainer.classList.remove('verse-fade');
        }, 120);

        if (!data.mode && !data.displayMode && !data.isBlank) {
            setDisplayMode('VERSE');
        }
    } else if (data.type === 'VERSE_CHANGE') {
        if (elRef) elRef.style.display = '';
        isCurrentSong = false;
        currentSongPayload = null;
        if (elContainer) elContainer.classList.add('verse-fade');
        setTimeout(() => {
            currentVersionLabel = data.versionLabel || 'NKJV';
            currentBookMl = data.bookMl || '';
            currentBookEn = data.bookEn || '';
            currentChapterNum = data.chapter || 1;
            currentVerseNum = data.verse || 1;

            updateRefBadge();

            if (elMl) elMl.innerText = data.textMl || '';
            if (elEn) elEn.innerText = data.textEn || '';

            if (data.malFontSize && elMl) elMl.style.fontSize = `${data.malFontSize}px`;
            if (data.engFontSize && elEn) elEn.style.fontSize = `${data.engFontSize}px`;
            if (data.theme) setTheme(data.theme);

            if (elContainer) elContainer.classList.remove('verse-fade');
        }, 120);

        // Transition back to Scripture mode when a new verse arrives
        if (!data.mode && !data.displayMode && !data.isBlank) {
            setDisplayMode('VERSE');
        }
    } else if (data.type === 'LAYOUT_CHANGE') {
        setScriptureLayout(data.scriptureLayout);
    } else if (data.type === 'DISPLAY_MODE') {
        setDisplayMode(data.mode);
    } else if (data.type === 'TOGGLE_BLANK') {
        setDisplayMode(data.isBlank ? 'BLACK' : 'VERSE');
    } else if (data.type === 'TOGGLE_DEFAULT_SCREEN') {
        setDisplayMode(data.isDefaultScreen ? 'DEFAULT' : 'VERSE');
    } else if (data.type === 'TOGGLE_WATERMARK' || data.type === 'TOGGLE_LOGO') {
        const show = (data.showWatermark !== undefined) ? data.showWatermark : data.showChurchLogo;
        setWatermark(show);
    } else if (data.type === 'UPDATE_DEFAULT_SCREEN') {
        applyHoldingConfig(data.config);
    } else if (data.type === 'STYLE_UPDATE') {
        if (data.malFontSize && elMl) elMl.style.fontSize = `${data.malFontSize}px`;
        if (data.engFontSize && elEn) elEn.style.fontSize = `${data.engFontSize}px`;
        if (data.theme) setTheme(data.theme);
        if (data.showWatermark !== undefined) setWatermark(data.showWatermark);
    }
}

function applyHoldingConfig(config) {
    if (!config) return;
    document.getElementById('default-screen-overlay')?.classList.toggle('use-attached-slide', config.useAttachedSlide !== false);
    const elTitle = document.getElementById('holding-title-main');
    const elTown = document.getElementById('holding-church-town');
    const elMotto = document.getElementById('holding-motto');
    const elQuote = document.getElementById('holding-verse-quote');
    const elImg = document.getElementById('holding-emblem-img');
    const barTop = document.getElementById('card-accent-bar-top');
    const barBottom = document.getElementById('card-accent-bar-bottom');

    if (elTitle && config.orgTitle !== undefined) elTitle.innerText = config.orgTitle;
    if (elTown && config.townName !== undefined) {
        elTown.innerText = config.townName;
        if (config.accentColor) elTown.style.color = config.accentColor;
    }
    if (elMotto && config.motto !== undefined) elMotto.innerText = config.motto;
    if (elQuote && config.quote !== undefined) elQuote.innerText = config.quote;

    if (elImg && config.logoDataUrl) {
        elImg.src = config.logoDataUrl;
    } else if (elImg && config.logoDataUrl === '') {
        elImg.src = 'church-logo.png';
    }

    if (config.accentColor) {
        const grad = `linear-gradient(90deg, ${config.accentColor}, #e11d48, ${config.accentColor})`;
        if (barTop) barTop.style.background = grad;
        if (barBottom) barBottom.style.background = grad;
    }
}

// Listen to live broadcast messages
channel.onmessage = (event) => {
    applyPayload(event.data);
};

// Handle initial load from localStorage
window.onload = () => {
    // 1. Live Scripture or Song state
    const saved = localStorage.getItem('church_live_state') || localStorage.getItem('church_bible_state');
    if (saved) {
        try {
            applyPayload(JSON.parse(saved));
        } catch (e) {
            console.error('Failed to parse saved state', e);
        }
    }

    // 2. Custom Holding Screen configuration
    const savedHolding = localStorage.getItem('church_default_screen_config');
    if (savedHolding) {
        try {
            applyHoldingConfig(JSON.parse(savedHolding));
        } catch (e) {
            console.error('Failed to parse saved holding config', e);
        }
    }

    // 3. Saved Scripture Layout (Dual, Malayalam, or English)
    const savedLayout = localStorage.getItem('church_scripture_layout');
    if (savedLayout) {
        setScriptureLayout(savedLayout);
    }
};

// Toggle Fullscreen function
if (new URLSearchParams(location.search).get('native') === '1') {
    let previousSnapshot = '';
    let polling = false;
    const pollPresenter = async () => {
        if (polling) return;
        polling = true;
        try {
            const response = await fetch('/__snapshot', { cache: 'no-store' });
            if (!response.ok) return;
            const text = await response.text();
            if (text === previousSnapshot) return;
            const snapshot = JSON.parse(text);
            if (snapshot.live) applyPayload(snapshot.live);
            if (snapshot.holding) applyHoldingConfig(snapshot.holding);
            previousSnapshot = text;
        } catch (error) { console.warn('Waiting for presenter', error); }
        finally { polling = false; }
    };
    pollPresenter();
    setInterval(pollPresenter, 250);
}

function showFullscreenPrompt() {
    if (document.fullscreenElement) return;
    let button = document.getElementById('enter-fullscreen-button');
    if (!button) {
        button = document.createElement('button');
        button.id = 'enter-fullscreen-button';
        button.textContent = 'Enter full screen';
        button.style.cssText = 'position:fixed;right:20px;top:20px;z-index:20000;padding:12px 20px;border:1px solid #ffffff66;border-radius:8px;background:#18212f;color:white;font:16px system-ui;cursor:pointer';
        button.onclick = () => document.documentElement.requestFullscreen({ navigationUI: 'hide' }).catch(() => { button.textContent = 'Press F11 for full screen'; });
        document.body.appendChild(button);
    }
    button.hidden = false;
}

document.addEventListener('fullscreenchange', () => {
    const button = document.getElementById('enter-fullscreen-button');
    if (button) button.hidden = Boolean(document.fullscreenElement);
});

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => console.log('Fullscreen error:', err));
    } else {
        document.exitFullscreen().catch(err => console.log('Exit fullscreen error:', err));
    }
}

// Double-click anywhere to toggle Fullscreen
document.addEventListener('dblclick', toggleFullscreen);

// Projector window keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'f' || e.key === 'F' || e.key === 'F11') {
        e.preventDefault();
        toggleFullscreen();
    } else if (e.key === 'w' || e.key === 'W') {
        e.preventDefault();
        const next = (currentMode === 'DEFAULT') ? 'VERSE' : 'DEFAULT';
        setDisplayMode(next);
    } else if (e.key === 'b' || e.key === 'B') {
        e.preventDefault();
        const next = (currentMode === 'BLACK') ? 'VERSE' : 'BLACK';
        setDisplayMode(next);
    } else if (e.key === 'Escape' || e.key === 'v' || e.key === 'V') {
        setDisplayMode('VERSE');
    }
});
