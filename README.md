# MANNIE — Fashion in the Round

A single-file, dependency-free storefront built by **Blessed Digital Solutions** (Kampala, Uganda).

Every garment, bag, shoe and accessory on the site sits on a turntable: drag it and it turns a
full 360°, front to back, so a customer reads the stitching before they commit. Colourways recolour
the piece live, every size shows its real stock count, and the bag checks out over WhatsApp.

**Live file:** [`index.html`](index.html) — open it in a browser. No build step, no server, no npm.

---

## What is in the box

| | |
|---|---|
| **57 products** | 14 categories — tops, outerwear, bottoms, dresses, sleep, footwear, bags, belts, eyewear, headwear, accessories, intimates, heritage |
| **126 photographs** | A front and a back frame for almost every piece, so the turntable shows two real angles |
| **3D vector fallback** | Every silhouette is also drawn as an extruded SVG garment. If a photo ever fails to load, the piece falls back to it silently — a client never sees a broken image |
| **Live stock** | Per-size counts, "only N left" and sold-out states drive the badges and the buttons |
| **WhatsApp checkout** | The bag becomes a formatted message to `+256 777 691011` |
| **Photo Studio** | A built-in panel (⧉, bottom left) to swap any product's photography without opening the code |
| **Zero dependencies** | Two Google Fonts and the image CDN. Everything else is hand-written HTML, CSS and JS |

## Photography

The site ships with real photography served from the Unsplash CDN — free for commercial use,
no API key, no expiry, no attribution required (we credit it anyway in the footer).

Images are pulled at two sizes: a light **620px** crop for the 57 grid cards and a **1100px** crop
inside the studio, all lazily loaded, so the page stays fast on a Kampala mobile connection.

### Replacing them with your own shoot

1. Open the site and click **⧉ Photo Studio** (bottom left).
2. Pick a product, paste a **front** image URL, optionally a **back** one.
3. For a true turntable, paste 8–36 frames (one URL per line) into the 360° box — dragging then
   scrubs the real frames and the object genuinely rotates.
4. Hit **Apply** to preview, then **Export code** and paste the block over the `SHOTS` object near
   the top of the `<script>` in `index.html`.

Shooting a 360°: phone on a tripod, product on a turntable marked at 24 points, one frame per mark.
Never move the phone.

## Deploying

The whole site is one file, so anything that serves static files works:

```bash
# GitHub Pages — Settings → Pages → deploy from branch → root
# Netlify / Vercel — drag the folder in, no build command
# Any cPanel host — upload index.html to public_html
```

Set the canonical domain in the `<link rel="canonical">` tag and the Open Graph URLs in `<head>`
before going live.

## Repository contents

- `index.html` — the MANNIE storefront (this project)
- `blessed-digital-solutions.html` — the earlier Blessed Digital Solutions agency page, kept intact
- `README.md` — you are here

## Built by

**Blessed Digital Solutions** — web development, digital marketing, branding and content.
WhatsApp [+256 777 691011](https://wa.me/256777691011) · [jonathanashaba86@gmail.com](mailto:jonathanashaba86@gmail.com)
