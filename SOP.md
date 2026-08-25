# Newsletter Production SOP

How a Figma design becomes a live HubSpot email — the fixed, repeatable pipeline
across **Designer → Developer → HubSpot Manager**.

> **Core idea:** the HTML template is built *once* (`build.py`). After that, every
> newsletter — and every small fix like a price change — is **just a slice swap**.
> Same structure, same code, new images.

Pipeline: **Designer** (600px Figma frame + link map) → **Developer** (export 2×,
slice, build & host) → **HubSpot Manager** (upload slices, paste HTML, test, send).

---

## Why the email is built from image slices

Coded HTML re-flows on small screens — Gmail iOS in particular squishes multi-column
layouts down to one word per line, so the mobile email stops matching the design.
Cutting the design into **horizontal image slices** and letting each scale to
`width:100%` gives a true "zoom-out": mobile is the desktop design, shrunk — nothing
re-flows or stacks, pixel-identical to Figma everywhere (Outlook, Gmail, Gmail iOS,
Apple Mail).

Trade-off: text inside a slice isn't selectable. We recover that with accurate `alt`
text on every image (also good for accessibility and image-blocking clients).

---

## Phase 1 — Designer (in Figma)

Deliver a clean, sliceable design and a link map. **Leave cutting to the developer.**

1. **One vertical frame, exactly 600px wide.** The entire email is a single frame at
   600px (desktop width; mobile is the same frame scaled down).
2. **Design "zoom-out", not a separate mobile layout.** Whatever sits side-by-side
   stays side-by-side on phones. Keep text large enough to read at ~half width.
3. **Compose in clean horizontal bands.** The frame is cut into full-width horizontal
   slices — keep each section self-contained, never let an element straddle a boundary.
4. **Products row = 3 tappable cards side by side** (image + name + price + button).
   Becomes one heading slice + three column slices that tile back to full width.
5. **Hand off:**
   - Figma frame URL (node link)
   - **Link Map** — every clickable section / card → its destination URL
   - Alt-text notes for image-heavy sections (prices, product names)

> **Why the designer doesn't slice:** cuts must line up pixel-exactly with the code's
> band structure, the 2× export, the naming convention, and the product-column split.
> That's developer territory; the designer just marks where sections break.

---

## Phase 2 — Developer (export, slice, build, host)

The template already exists (`build.py`). A normal newsletter is: export → slice →
run the builder → host.

1. **Export the whole frame at 2×.** A 600px frame becomes **1200px** wide.
   Via Figma MCP: `download_assets(nodeId, defaultFormat="png", defaultScale=2)`.
2. **Slice into horizontal bands** (ImageMagick / PIL), top to bottom. Products row
   splits into a heading slice + three column slices tiling to full 1200px width.
3. **Name slices by convention** (see table below). Filenames are contractual —
   HubSpot links to them by exact name.
4. **Build the HTML from the template** (`build.py`). It emits each slice as a
   full-width table row and wraps clickable slices in `<a>`.
5. **Host images (two targets):**
   - **Preview → catbox.** ⚠️ Verify the upload is **non-empty** — catbox occasionally
     stores a 0-byte file and de-dupes by hash, returning a dead URL. Check the size;
     if broken, alter the bytes to force a fresh URL.
   - **Production → HubSpot CDN filenames** (manager uploads the actual files).
6. **Emit three outputs:**
   - `index-hubspot.html` — production (HubSpot CDN URLs)
   - `index-FINAL.html` — shareable preview (catbox URLs)
   - self-contained `PREVIEW.html` — images embedded as data-URIs; works offline,
     ideal for phone review
7. **QA, then commit as a new folder.** Open at 600 / 375 / 320px — no horizontal
   scroll, no clipping, every link correct. Each newsletter gets its **own folder**;
   never overwrite an older one.

---

## The standard template

This markup never changes between newsletters — only `src`, `height`, `href`, `alt` do.

**A full-width slice:**
```html
<tr><td style="padding:0;font-size:0;line-height:0;">
  <img src="…/nl4-3.png" width="600" height="373"
       alt="What we learned this month."
       style="display:block;width:100%;max-width:600px;height:auto;border:0;" />
</td></tr>
```

> **Height rule:** the export is 2×, so the `height` attribute = pixel height ÷ 2.
> A 746px-tall slice → `height="373"`. The explicit height stops mobile WebViews
> clipping the image before it loads.

**A clickable slice — wrap the image in a link:**
```html
<td style="padding:0;font-size:0;line-height:0;">
  <a href="https://www.datadirect.ie/products" target="_blank" style="display:block;line-height:0;">
    <img src="…/nl4-1.png" width="600" height="407" alt="Explore the store."
         style="display:block;width:100%;max-width:600px;height:auto;border:0;" />
  </a>
</td>
```

**The products row — 3 columns that scale together** (each `<td>` width % = column
pixel width ÷ 1200 × 100):
```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
  <td width="35.33%" valign="top" style="padding:0;font-size:0;line-height:0;">
    <a href="…/product-details?productId=CQ00959" target="_blank" style="display:block;line-height:0;">
      <img src="…/nl4-2b.png" width="212" height="222"
           alt="Apple iPhone Air 256GB, EUR 1058, view product"
           style="display:block;width:100%;height:auto;border:0;" />
    </a>
  </td>
  <!-- col-mid + col-right follow the same pattern -->
</tr></table>
```

All rows live inside one centered `width="600"` table with `max-width:100%`.
Globals: `table{border-collapse:collapse}` and `img{display:block}`. If a slice needs
rounded corners in HTML, switch that table to `border-collapse:separate`.

---

## Slice naming convention (newsletter *N*)

Top-to-bottom, products block uses letter suffixes. These filenames are what HubSpot
links to — keep them exact.

| Filename | What it is | Clickable? |
|---|---|---|
| `nlN-1` | First section (hero + primary CTA) | Yes → store |
| `nlN-2a` | Products — heading strip | No |
| `nlN-2b` | Products — left card | Yes → product URL |
| `nlN-2c` | Products — middle card | Yes → product URL |
| `nlN-2d` | Products — right card | Yes → product URL |
| `nlN-3 … nlN-M` | Remaining sections, in order down the page | Per link map |

> Never put a literal `"` in `alt` text — it closes the attribute early. Write
> `16-inch`, not `16"`.

---

## Phase 3 — HubSpot Manager (publish)

1. **Upload every slice to HubSpot Files** — into the **root of the file manager**,
   same portal each time (`146425634`, EU1). Keep filenames **exactly** (`nlN-1.png` …).
2. **Confirm the URLs match:**
   ```
   https://146425634.fs1.hubspotusercontent-eu1.net/hubfs/146425634/nlN-1.png
   ```
3. **Create the email with a Custom-HTML module** — paste `index-hubspot.html` into a
   **Custom HTML / source-code** module, not the drag-and-drop editor.
4. **Check every link** — store CTA, each product card, "see examples", LinkedIn, and
   `mailto:sales@datadirect.ie`.
5. **Send a test to yourself** — confirm images render and links work on **desktop and
   mobile** (Gmail iOS especially), then schedule / send.

> **Same portal, same folder, same names — every time.** A different portal or a
> sub-folder changes the URL and silently breaks the images.

---

## The recurring update — "just a slice change"

The everyday case: a price, image, or link changes on an already-published newsletter.
The template stays put.

1. **Developer re-slices only the affected band** — re-export at 2×, cut just that
   section at the same coordinates, re-host **only those images**, rebuild the HTML.
2. **Manager re-uploads only the changed slice(s)** — same filename → overwrite in
   HubSpot Files. Re-paste HTML **only if a link changed**; a pure image swap needs no
   HTML change.
3. **Hard-refresh before judging** — browsers/inboxes cache images aggressively. If an
   old value still shows, hard-refresh (⌘⇧R) or view the self-contained preview; the
   file on disk is the source of truth.

---

## Pre-send checklist & known gotchas

- [ ] **Explicit `height` on every `img`** (= pixel height ÷ 2). Missing heights cause
      half-rendered / clipped emails on mobile.
- [ ] **catbox uploads verified non-empty** — a 200 response can still be 0 bytes.
- [ ] **No literal `"` inside `alt`** — use `16-inch`.
- [ ] **Rounded corners need `border-collapse:separate`** — the global `collapse`
      disables radius.
- [ ] **Same HubSpot portal, root folder, exact filenames.**
- [ ] **No `position:absolute` for production** — HubSpot strips it; bake overlaps into
      the slice.
- [ ] **Tested at 600 / 375 / 320px** — no horizontal scroll, no stacking, matches Figma.
- [ ] **New folder per newsletter** — never overwrite a previous design.

---

## File map (per newsletter)

```
monthly-newsletter/<design>/index-hubspot.html   → give to HubSpot manager
monthly-newsletter/<design>/index-FINAL.html     → shareable catbox preview
monthly-newsletter/<design>/slices/              → the images to upload
```

Repository: `datadirect-emails` · builder `build.py` · this doc `SOP.md` · method notes `METHOD.md`
