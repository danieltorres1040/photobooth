# DIY Photo Booth — iPad + Canon SELPHY CP1300

Guests pick a frame and a style (b&w / vintage / color) → press start → 8 photos → pick their favorites → print.
Each 4×6 postcard sheet holds **two identical 2×6 strips** — cut down the middle (tick marks top and bottom).

**What's in this folder**

| File | What it is |
|---|---|
| `index.html` | The booth app |
| `logo.png` | Your logo — start screen + strip footer. Replace with your own file of the same name to change it. |
| `fonts/` | Inter font, bundled so it works offline |
| `sw.js`, `manifest.json`, `icon.png` | Make the booth installable and work offline |
| `start-booth.command` | Double-click on a Mac to start hands-free printing (Setup B) |
| `print_server.py` | The program `start-booth.command` runs |
| `qr.js` | Makes the QR codes (works offline) |
| `README.md` | This guide |

---

## Part 1 — Put the booth on GitHub Pages (free, one time)

You need a computer for this part (Mac or PC, any browser).

### 1. Make a GitHub account
Go to **github.com** → **Sign up**. Pick your username carefully — it becomes part of the booth's web address.

### 2. Create a repository
1. Signed in, click the **+** in the top-right corner → **New repository**.
2. **Repository name:** `photobooth` (lowercase, no spaces).
3. Choose **Public**. (Free GitHub Pages needs a public repository. Nothing private is in it — guests' photos never leave the iPad.)
4. Leave everything else as is → **Create repository**.

### 3. Upload the files
1. Unzip `photobooth.zip` on your computer.
2. On the new repository's page, click the link **uploading an existing file** (or **Add file → Upload files**).
3. Open the unzipped `photobooth` folder and **select everything inside it** — `index.html`, `logo.png`, `icon.png`, `manifest.json`, `sw.js`, `print_server.py`, `README.md` **and the `fonts` folder** — and drag them into the browser window.
   - Drag the **contents**, not the `photobooth` folder itself, so `index.html` ends up at the top level.
   - Chrome, Edge and Safari keep the `fonts` folder intact when you drag it in. Check the list shows `fonts/Inter-Regular.woff` etc. before continuing.
4. Scroll down → **Commit changes**.

Your repository should now list: `fonts/`, `README.md`, `icon.png`, `index.html`, `logo.png`, `manifest.json`, `print_server.py`, `sw.js`.

### 4. Turn on GitHub Pages
1. In the repository, click **Settings** (top tab bar) → **Pages** (left sidebar).
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. **Branch:** `main`, folder **`/ (root)`** → **Save**.
4. Wait 1–2 minutes (progress shows under the **Actions** tab). Refresh the Pages settings — it will show **"Your site is live at https://YOUR-USERNAME.github.io/photobooth/"**.

Open that address on your computer: you should see the booth's start screen with your logo. That address is the one you'll use on the iPad.

### 5. Changing things later
- **Logo:** upload a new file named exactly `logo.png` (Add file → Upload files) — it replaces the old one. A transparent PNG works best.
- **Any other file:** upload the new version the same way, or click the file → pencil icon to edit it in the browser.
- **After any change,** open `sw.js` → pencil icon → change `booth-v3` to `booth-v4` (then v5, v6…) → Commit. This tells iPads to fetch the new version.
- Then on the iPad, while it's on normal internet: open the booth, close it, open it again.

Event name, footer text, colors, countdown, and a custom logo can also be changed right on the iPad in the hidden settings (below) without touching GitHub.

---

## Part 2 — Install it on the iPad (needs internet once)

1. On normal Wi-Fi, open **Safari** → go to `https://YOUR-USERNAME.github.io/photobooth/`.
2. Tap a look → **Allow** camera access → let it take the four photos (this also caches everything for offline use).
3. Tap the **Share** button → **Add to Home Screen** → Add.
4. Open the booth from the new home-screen icon once while still online.
5. Tap the **top-left corner 5 times** to open settings. Check it says **Offline ready: yes ✓**. Set your event name, footer line (date / hashtag), colors, logo size, countdown.

From now on the booth runs with no internet at all.

---

## Part 3 — At the show

### Setup A — iPad + Selphy only
```
iPad (booth app, offline)  ──Selphy's own Wi-Fi──▶  SELPHY CP1300
```
1. Turn on the Selphy's network (Selphy menu → Wi-Fi → Direct Connection), and join it from the iPad in **Settings → Wi-Fi**.
2. Open the booth from the home screen.
3. Settings → **Print test sheet**.

**How printing works:** after the review screen, the guest taps **print my strip** → the iPad's share menu opens → **Print** → (first time only: choose **SELPHY** as the printer) → **Print**.
This prints the strip as a photo, so there's **no URL / date / page-number header or footer** on it.

Tip: in the share menu, scroll to the bottom → **Edit Actions** → add **Print** to Favorites so it's always at the top.

iPadOS always asks for that confirmation when a web page prints, so a booth helper (or a little "tap print!" sign) is the plan here. For no taps at all, use Setup B.

### Setup B — fully hands-free (add a MacBook)
```
iPad  ──same Wi-Fi──▶  MacBook (start-booth)  ──▶  SELPHY CP1300   (no taps)
```
1. Put the `photobooth` folder somewhere easy on the Mac, e.g. the Desktop.
2. Join the Mac to the **same Wi-Fi as the Selphy** and add the printer: System Settings → Printers & Scanners → **Add Printer…** → pick the SELPHY → Add. Print one photo from the Photos app at *Postcard* size to confirm.
3. Double-click **start-booth.command**. First time only: if macOS blocks it, go to System Settings → Privacy & Security → scroll down → **Open Anyway**, then double-click again. Leave the window open.
4. The window shows a line like `On the iPad, open: https://192.168.x.x:8443/`.
5. iPad on the **same Wi-Fi** → Safari → type that address exactly → **Show Details → visit this website → Visit Website** (one time) → tap a look → **Allow** camera.
6. Settings (top-left corner 5×) should say **Print server: found ✓**. Tap **Print test sheet** — it prints with no taps.
7. Share → **Add to Home Screen** to get a booth icon for this address.

Use the Mac's address, not the GitHub address, for hands-free mode. If the iPad can't open the Mac's address on the Selphy's own network, put all three on one regular network instead (home Wi-Fi, a travel router like GL.iNet, or an iPhone hotspot with "Maximize Compatibility" on), add the Selphy to it from its Wi-Fi menu, and redo steps 2–5.

---

## Frames

The booth shows every frame listed in **`frames.json`**. Guests pick a frame and a style, take 8 photos, then pick their favorites. The number of favorites equals the number of photo windows in the frame (your current frames have 3; the built-in "classic" frame has 4). Favorites always print top to bottom in the order they were taken.

### Making a new frame (Illustrator)
1. Artboard **2 × 6 in** (or any 1:3 size). Keep text and important art at least **0.1 in** from every edge; the printer trims a hair off.
2. Leave the photo windows **empty** (no white box behind them). Photos show through wherever the PNG is transparent. Windows are found automatically, top to bottom. Art may overlap a window (stars, cats…); it prints on top of the photo.
3. **File → Export → Export As… → PNG**, Background: **Transparent**, resolution **300 ppi** (gives 600 × 1800 px).
   - If you forget and export with white windows, the booth tries to detect plain white rectangles itself, but transparent is more reliable.
4. Frames that aren't exactly 1:3 still work: they're shrunk to fit, never cropped or stretched, and the leftover space is filled with the frame's edge color.

### Adding it to the booth (GitHub)
1. In your repository, open the **frames** folder → **Add file → Upload files** → drop in your PNG (e.g. `spooky.png`) → **Commit changes**.
2. Open **frames.json** → pencil icon → add a line for it, e.g.
   `{ "name": "spooky", "file": "frames/spooky.png" },`
   Every line except the last needs a comma at the end. The order here is the order on the start screen. Remove a line to hide a frame.
3. Open **sw.js** → pencil icon → bump the `booth-v…` number by one → Commit.
4. On the iPad, on normal internet: open the booth, close it, open it again.

For the MacBook (hands-free), copy the same PNG into `photobooth/frames/` and make the same `frames.json` edit there.

---

## Digital copies (QR code)

When it's turned on, each strip is uploaded the moment the guest taps print, and a QR code appears on the printing screen (optionally also printed small on the strip). Guests scan it, the strip opens on their phone, and they tap & hold to save it.

Needs **internet on the iPad**: venue Wi-Fi, or an iPhone hotspot with cellular data. Without internet, strips are saved on the iPad and uploaded automatically once it's back online, so a QR code scanned later still works.

### One-time setup (free Cloudinary account)
1. Sign up at **cloudinary.com** (free plan).
2. Your **cloud name** is shown on the Console home / dashboard (a short code like `dxyz123ab`).
3. Go to **Settings (gear) → Upload → Upload presets → Add upload preset**. Set **Signing mode** to **Unsigned**, give it a name (e.g. `photobooth`), **Save**.
4. On the iPad: settings (top-left corner 5×) → **Digital copies** → enter the cloud name and preset name → **Test digital upload**. You should see "Upload works ✓".
5. Optional: tick **Also print a small QR code on the strip** and pick its corner, then **Print test sheet** to check it doesn't cover your frame art.

Notes: anyone with a strip's link can see that strip (links are random and can't be guessed). Uploaded strips appear in your Cloudinary **Media Library** where you can download or delete them all after the show. Leave the two fields blank to turn digital copies off.

---

## Hidden settings (tap top-left corner 5×)
Event name · footer line · welcome text · print method (Automatic = server if found, otherwise share-sheet AirPrint) · copies · countdown · pause between photos · front/back camera · mirror · auto-print delay (server mode) · idle timeout · strip colors · logo (built-in / upload / none) · **logo size on strip** · test print · download last strip · paper counter.

## Lock it down for guests
- **Guided Access** (Settings → Accessibility → Guided Access): triple-click the side/top button inside the booth to lock the iPad to it.
- **Auto-Lock → Never**, iPad plugged in.

## Supplies & show-day checklist
- [ ] **KP-108IN** paper/ink: 108 sheets = 216 strips. Cassette holds 18 sheets (the booth warns when ~2 are left); each ink cartridge does 36.
- [ ] Spare cassette pre-loaded, spare ink, paper trimmer
- [ ] Good front light — a ring light makes the biggest difference
- [ ] Using **flash**? Turn the iPad's brightness all the way up (Control Center). The flash is the screen lighting the face, so it's strongest in a dim space
- [ ] Test sheet printed on site
- [ ] Selphy takes ~45–60 s per sheet; plan for the line

## Troubleshooting
| Problem | Fix |
|---|---|
| GitHub Pages shows a 404 | Wait 2 minutes; make sure `index.html` is at the top level of the repository (not inside a `photobooth` folder) and Pages is set to `main` / `(root)`. |
| Fonts look like the default system font | The `fonts` folder didn't upload. Upload the three `.woff` files into a folder named `fonts` (in the upload screen you can type `fonts/` in front of the file name). |
| Camera doesn't start | Must be the https address or the home-screen app. iPad Settings → Safari → Camera → Allow. |
| Booth won't open on the Selphy network | It wasn't cached yet — open it once on internet and check **Offline ready: yes ✓**. |
| Old version still showing | Bump the `booth-v…` number in `sw.js`, then open/close/reopen the booth on internet. |
| Share menu has no Print option | Scroll to the bottom → Edit Actions → enable Print. |
| Print sheet doesn't list the SELPHY | Is the iPad still on the Selphy's Wi-Fi? Restart the Selphy's Direct Connection. |
| Wrong size / borders (Setup B) | `--list`, then e.g. `python3 print_server.py --media "PageSize=Postcard"`; try `--scaling fit` if edges get cut. |
