# DIY Photo Booth — iPad + Canon SELPHY CP1300

Guests tap a look (b&w / vintage / color) → 3-2-1 countdown × 4 poses → strip preview → print.
Each 4×6 postcard sheet holds **two identical 2×6 strips** — cut down the middle (tick marks top and bottom).

**What's in this folder**

| File | What it is |
|---|---|
| `index.html` | The booth app |
| `logo.png` | Your logo — start screen + strip footer. Replace with your own file of the same name to change it. |
| `fonts/` | Inter font, bundled so it works offline |
| `sw.js`, `manifest.json`, `icon.png` | Make the booth installable and work offline |
| `print_server.py` | Optional — only for hands-free printing from a Mac (Setup B) |
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

### Setup B — fully hands-free (add a Mac)
```
iPad  ──Wi-Fi──▶  Mac running print_server.py  ──▶  SELPHY CP1300   (no taps)
```
1. Put the Mac on the same network as the iPad and Selphy (the Selphy's own network, or a travel router — see note), and add the printer: System Settings → Printers & Scanners → Add Printer → SELPHY. Test-print a photo from Photos at *Postcard* size.
2. Copy this folder to the Mac. In Terminal, in this folder: `python3 print_server.py` (`--list` shows printer names and paper sizes).
3. It shows an address like `https://192.168.x.x:8443/` — open that on the iPad (accept the one-time certificate warning: *Show Details → visit this website*).
4. The booth finds the server by itself (settings shows **Print server: found ✓**) and prints silently. Every sheet is also saved in `strips/` on the Mac.

Note: some printer direct-connect networks don't let two devices talk to each other. If the iPad can't open the Mac's address, use a small travel router (e.g. GL.iNet) for all three devices — the Selphy only does 2.4 GHz 802.11b/g.

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
