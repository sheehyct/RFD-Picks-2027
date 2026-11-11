# RFD 2027 Pick Planner

A personal planner for Richmond Fire 2027 vacation and holiday picks. Members choose their shift and mandatory OT group, build a wish list, mark what they are awarded, and get a ready-made list for ESO entry.

**Live link:** https://sheehyct.github.io/RFD-Picks-2027/
**Member guide:** https://sheehyct.github.io/RFD-Picks-2027/how-to.html

Picks are saved only on each member's own device. This is not the official record.

## Files

- `index.html` — the planner (single self-contained page)
- `how-to.html` — member guide
- `manifest.webmanifest`, `icon-*.png`, `apple-touch-icon.png` — home-screen install
- `sw.js` — offline support
- `.nojekyll` — tells GitHub Pages to serve the files as they are

## First-time setup

1. On github.com open this repository and choose **Add file → Upload files**.
2. Drag in every file from the upload folder (not the folder itself) and choose **Commit changes**.
3. Go to **Settings → Pages**. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch to **main** and folder to **/ (root)**, then **Save**.
4. Wait a minute or two, then open the live link above.

## Updating later

Upload the new `index.html` over the old one. If you want phones that already installed it to refresh their offline copy straight away, also change `v1` to `v2` in `sw.js`.
