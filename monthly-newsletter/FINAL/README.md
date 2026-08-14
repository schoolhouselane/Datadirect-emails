# ✅ FINAL — DataDirect Monthly Newsletter (image-based, tested & approved)

This is the shipped version. The whole Figma design is exported and sliced into
5 responsive images (`slices/nl-1…5.png`). Each image is `width:100%` so on any
screen the entire design **scales down proportionally (zoom-out)** — identical
to Figma, no reflow, no column stacking, no text drop — and it renders the same
in every client (Gmail incl. iOS, Outlook, Apple Mail).

## Files
- **`index-FINAL.html`** — the tested file. Slice URLs point at an external
  image host (catbox.moe) so it renders anywhere immediately (preview / send).
- `index-hubspot.html` — same HTML, slice URLs point at the HubSpot CDN
  (`hubfs/146425634/nl-1…5.png`). Use this for the real HubSpot send after
  uploading the 5 slices to HubSpot Files.
- `index-relative.html` — slice URLs are local `slices/nl-X.png` (local preview).
- `slices/` — the 5 image slices to host.
- `preview-desktop.png` / `preview-mobile.png`.

## To send from HubSpot
1. Upload `slices/nl-1.png … nl-5.png` to HubSpot → Marketing → Files.
2. Paste `index-hubspot.html` into a HubSpot Custom/Coded email.
3. Send test → check on phone (it zooms out to fit).

Build method for the whole repo: see `../../METHOD.md`.
