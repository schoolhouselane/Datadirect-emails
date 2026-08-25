# DataDirect Newsletter Production SOP

Use this process to turn a Figma newsletter into a slice-based HTML email with HubSpot-hosted images.

## Why the email is built from image slices

Coded HTML reflows on small screens. Gmail iOS can compress multi-column layouts until text appears one word per line, causing the mobile email to stop matching the design.

Image slices avoid this problem. Each slice scales to `width:100%`, so mobile displays a true zoomed-out version of the desktop design. Nothing reflows or stacks, and the email remains consistent across Outlook, Gmail, Gmail iOS, and Apple Mail.

The trade-off is that text inside an image is not selectable. Add accurate `alt` text to every slice for accessibility and email clients that block images.

## Phase 1 — Designer (in Figma)

- Create the newsletter in one `600 px` wide Figma frame.
- Provide the final Figma frame URL.
- Provide a link map for every clickable area.
- Confirm product names, prices, URLs, and image alt text.

## Phase 2 — Developer

### Create and export slices in Figma

1. The developer creates the required slice frames or export areas directly in Figma.
2. Use as many slices as the layout and links require.
3. Keep areas with different links in separate slices.
4. Export every slice from Figma as a PNG at `2x`.
5. Make sure the exported slices join without gaps and recreate the full design.

The newsletter remains `600 px` wide in HTML, so a full-width slice exports at `1200 px`. The HTML display size is half the exported pixel size. For example, a `424 × 444 px` slice displays at `212 × 222 px`.

### Name the campaign

Give every email a unique campaign ID:

```text
YYYY-MM-campaign
```

Examples:

```text
2026-09-monthly
2026-09-promo
2026-10-event
```

Use the campaign ID in every slice filename:

```text
2026-09-monthly-1.png
2026-09-monthly-2a.png
2026-09-monthly-2b.png
2026-09-monthly-3.png
```

Unique names prevent new HubSpot uploads from overwriting earlier campaigns.

### Build the HTML

Builder template:

```text
templates/newsletter-slice-builder/build.py
```

For each campaign:

1. Update the slice order, links, and alt text in the builder.
2. Match the builder's image names to the campaign's slice filenames.
3. Generate the HTML.
4. Save the campaign in its own folder:

```text
monthly-newsletter/2026-09-monthly/
├── index-relative.html
├── index-hubspot.html
└── slices/
```

`index-relative.html` uses local files for preview. `index-hubspot.html` uses public HubSpot image URLs.

## Phase 3 — Host images in HubSpot

1. Upload every slice to HubSpot Files in portal `146425634`, region `EU1`.
2. Keep the campaign filenames unchanged.
3. Set every image to public.
4. Use **Copy URL** in HubSpot for each uploaded image.
5. Confirm each URL opens in an incognito window without a HubSpot login.
6. Add the copied URLs to the matching `src` attributes in `index-hubspot.html`.

A typical public URL looks like this:

```text
https://146425634.fs1.hubspotusercontent-eu1.net/hubfs/146425634/2026-09-monthly-1.png
```

Always use the URL returned by HubSpot. Do not guess the path.
