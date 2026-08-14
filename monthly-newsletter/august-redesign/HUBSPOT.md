# Publishing this newsletter in HubSpot

This email is image-based: the design is 11 sliced images that scale to fit
any screen. You host the slices in HubSpot Files and paste one HTML file.

## 1. Upload the image slices
- Go to **Marketing → Files and Templates → Files**.
- Upload all 11 files from `slices/`:
  `nl2-1.png, nl2-2.png, nl2-3a.png, nl2-3b.png, nl2-3c.png, nl2-3d.png,
   nl2-4.png, nl2-5.png, nl2-6.png, nl2-7.png, nl2-8.png`
- Upload them to the SAME location the other assets use, so each public URL is:
  `https://146425634.fs1.hubspotusercontent-eu1.net/hubfs/146425634/<filename>`
- Tip: after uploading one file, click it and copy its URL. If the URL has an
  extra folder in it (e.g. `.../hubfs/146425634/newsletter/nl2-1.png`), then
  either move the files to the root, or Find & Replace the base URL in the HTML
  so it matches exactly.

## 2. Create the email
- **Marketing → Email → Create email → Custom / Code your own** (HTML email).
- Open `index-hubspot.html`, copy ALL of it, paste into the code editor.
  (Its image URLs already point at `hubfs/146425634/nl2-*.png`.)

## 3. Settings
- Set the **From name / From address**, **Subject line**, and **Preview text**
  (e.g. Subject: "Your month in DataDirect", Preview: "Winners, products of the
  week, and what's coming next").
- HubSpot automatically appends the required **unsubscribe / company address**
  footer — you do not need to add it in the HTML.

## 4. Test, then send
- Click **Send test email** to yourself and open it on desktop AND phone.
  On mobile the whole design should shrink to fit (zoom-out), not reflow.
- If images don't show in the test, tap "Display images"; also re-check the
  URLs from step 1 match exactly.
- When it looks right, pick the recipient list and **Send / Schedule**.

## Links already wired in the email
- Explore the Store / hero -> https://www.datadirect.ie
- Product 1 (iPhone Air) -> product-details?productId=CQ00075
- Product 2 (HP EliteBook) -> product-details?productId=CQ60626
- Product 3 (Samsung Galaxy Tab) -> product-details?productId=CQ00952
- See examples of our work -> https://www.datadirect.ie/it-solutions
- LinkedIn -> https://www.linkedin.com/company/data-direct/
- Tell us what you think -> mailto:sales@datadirect.ie

## Quick alternative (no upload)
`index-FINAL.html` uses images already hosted on an external CDN (catbox), so
you can paste it and send a test immediately without uploading anything — good
for a fast preview. For the real campaign, prefer `index-hubspot.html` with the
slices on HubSpot's own CDN.
