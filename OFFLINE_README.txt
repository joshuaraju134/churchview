CHURCHVIEW - OFFLINE COPY

1. Double-click START_OFFLINE.bat in this folder.
2. Keep the server window open while using ChurchView.
3. Your browser opens http://localhost:8765 (this is your PC, not the internet).
4. Click OPEN PROJECTOR in the app and move that window to your second screen.
5. Close the server window when finished.

No installation, Python, Node.js, or internet connection is required on Windows 10/11.
Keep the whole folder together. Do not open index.html directly.
Fonts, Bible data, songs and images are included locally.
Use the same browser and localhost address to retain custom songs/settings.
Custom songs/settings are stored in the browser; copying this folder does not copy them.

Source: https://github.com/joshuaraju134/churchview
This is a real Git clone; upstream history is preserved in .git.
Offline changes: bundled fonts + font licenses, local CSS import, and a
PowerShell-only START_OFFLINE.bat to avoid Windows Python installation aliases.

The offline launcher uses offline_server.ps1, a loopback-only TCP server.
It avoids administrator privileges required by the original HttpListener server.
Verified: dashboard/projector HTML, scripts, styles, both databases and all 12 fonts
served successfully over local HTTP. No external URLs remain in runtime HTML/JS/CSS.
Full browser/projector interaction has not been manually tested.

SECOND SCREEN: Set Windows + P to Extend. Refresh the dashboard, click OPEN
PROJECTOR, and allow Window management if Chrome/Edge asks. The projector
will be placed on the other screen. Double-click its display for full screen.
If permissions are denied, use Windows + Shift + Right Arrow to move it.
Automatic placement also retries when screens are connected or disconnected.
Placement logic verified with simulated multiple/single-screen and permission cases;
physical second-screen behavior still needs checking on your connected display.

HOLDING SCREEN: Your supplied Default Screen.pptx is rendered locally as
holding-screen.png (1920x1080). Your logo is church-logo.png. Press W to show
the holding screen. To edit its text instead, open Customize Default / Welcome
Screen and uncheck Use the attached PowerPoint holding screen.

EVENTS / SAVED SONGS: Click Events / Saved Songs, then + New Event. Select
an event, click Add songs from library, and star songs for quick access. Use
the up/down controls to arrange the service order. Changes save automatically.
Malayalam and English verse sizes now restore automatically after reopening.
Use the same browser profile and http://localhost:8765. Browser storage holds
your events, custom songs and font sizes; clearing browser data removes them.

CLEAR PROJECTION: The large central watermark is removed. The corner logo
is off by default; it can be enabled in Projector Settings. Songs default to
Malayalam only. Toggle Show English lyrics in the Songs panel to include
English/transliteration. The choice is saved separately from Bible language.

LYRIC SIZES: The Songs panel now has separate Malayalam/English size sliders.
Sizes save automatically (defaults: 64px Malayalam, 42px English). Song titles,
numbers and stanza headings are hidden on the audience screen; Bible references
remain visible. Refresh both dashboard and projector after updating.

FULL SCREEN: Projector now attempts full screen automatically when opened.
If the browser requires another gesture, click Enter full screen on the
projector. Esc exits full screen. The existing projector window is reused.

NATIVE FULLSCREEN PROJECTOR: The Projector button now asks the local server
to launch Microsoft Edge in fullscreen kiosk mode. Alt+F4 closes that window.
It selects the non-primary Windows display when one is connected. Connect the
projector and choose Windows+P > Extend before launching. The projector uses a
separate temporary browser profile and receives content over a local-only relay.
No internet is required. Dashboard events/settings stay in your normal browser.
BIBLE SIZES: Malayalam now supports 30-110px; English supports 20-90px.
Large verses may need a smaller font to fit all text. Selected sizes are saved.
