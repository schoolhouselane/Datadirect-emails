# How we build these emails (the method)

This is the repeatable process for turning a **Figma email design** into a
production email that looks **exactly like the design on every client and
scales down proportionally on mobile** (true "zoom-out", no reflow).

There are two build styles in this repo. Use the one that fits the goal:

| Style | Folder | When to use |
|---|---|---|
| **Image-based (sliced)** ✅ default | `monthly-newsletter/image-version/` | When the design MUST match Figma pixel-for-pixel and behave like "zoom out to fit" on mobile (no columns stacking, no text reflow). This is what we shipped for the newsletter. |
| **Coded (HTML/CSS)** | `monthly-newsletter/`, `product-of-the-week/` | Simpler layouts where selectable text / accessibility matter more than pixel-exactness, and stacking on mobile is acceptable. |

---

## Why image-based for the newsletter

Real HTML/CSS emails **reflow** on mobile. Gmail iOS in particular does NOT
"zoom a fixed-width email to fit" — it re-lays-out the columns, which squishes
text and stacks images. So you can't keep a rich multi-column desktop layout
"just smaller" on mobile with HTML/CSS.

A responsive **image** (`width:100%`) scales perfectly and identically on
**every** client. So we render the design to images and let those scale.
Result: identical to Figma everywhere; on a narrow screen the whole thing
shrinks proportionally = the zoom-out the client asked for.

Trade-offs (accepted): text is baked into images (not selectable) → we add
real `alt` text per slice for accessibility and images-off; total size is
larger (~1–2 MB); keep some real text (preheader + alt + the ESP footer) so
spam filters stay happy.

---

## Step-by-step (image-based)

1. **Read the Figma design** with the Figma MCP: `get_metadata` for structure,
   `get_screenshot` to view, `get_design_context` for exact colours / fonts /
   sizes (only needed if you also build a coded version).

2. **Export the frame at 2x** for crisp images:
   `download_assets(nodeId, fileKey, defaultFormat="png", defaultScale=2)`
   → one tall PNG of the whole design (e.g. 1200 × 6278 for a 600-wide design).

3. **Slice** the tall export into ~5 horizontal sections with ImageMagick,
   cutting on clean full-width lines (band edges / cream gaps), and isolating
   any section that contains a CTA so it can be linked:
   ```
   magick full2x.png -crop 1200x3700+0+0    +repage slices/nl-1.png
   magick full2x.png -crop 1200x570+0+3700  +repage slices/nl-2.png
   ...
   ```

4. **Build the HTML** — outer full-width table (frame colour), inner table
   `max-width:600px`, each slice its own row:
   ```html
   <td style="padding:0; font-size:0; line-height:0;">
     <img src="nl-1.png" width="600"
          style="width:100%; max-width:600px; height:auto; display:block;"
          alt="…meaningful description…" />
   </td>
   ```
   `font-size:0; line-height:0` on the cells removes gaps so slices tile
   seamlessly. Wrap CTA slices in `<a href>` (mailto / URL).

5. **Alt text** on every slice (accessibility + shows when images are off).

6. **Host the slices** and put their URLs in the `src`:
   - **Production:** HubSpot File Manager (Marketing → Files) → CDN URLs.
     `index-hubspot.html` already points at the HubSpot base
     `https://146425634.fs1.hubspotusercontent-eu1.net/hubfs/146425634/nl-1.png …`.
   - **Quick preview:** any public image host (we used catbox.moe) or send a
     Gmail draft to yourself and open the received mail (images load with
     "Display images"). Note: Gmail's draft/compose view hides remote images —
     always test on the SENT/received copy, not the draft.

7. **Test at 600 / 375 / 320 px** (Playwright) — `document.body.scrollWidth`
   must equal the viewport (no horizontal scroll); the design just scales down.

## Tooling notes
- Fonts (Gilroy) only matter for the coded version; in image-based they're
  baked into the slices, so they render identically everywhere.
- Colours (from Figma): magenta `#FF00AA`, ink `#1B0E3B`, body `#3D3363`,
  deep navy badge `#2B1362`, cream `#FCF8F4`, frame `#E8E1D7`.
- ImageMagick + Python(Pillow) do all slicing/compositing; `cairosvg` renders
  thin-stroke SVG icons that ImageMagick drops.
