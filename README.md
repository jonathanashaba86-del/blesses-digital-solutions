# Blessed Digital Solutions

Kampala, Uganda — web development, online stores, brand identity and digital marketing.

This repository publishes three things from one branch, with no build step, no server and no
monthly platform fee:

| Path | What it is | Who it is for |
|---|---|---|
| `index.html` | **The agency front door** — services, work, pricing and the enquiry form | The public |
| `mannie/` | **MANNIE** — the flagship client storefront, 57 products that turn 360° | The public |
| `leads/` | **The Lead Desk** — where enquiries land, get scored and get chased | The studio, internal |
| `nyumba/` | **Nyumba Furniture Co.** — contract-furniture storefront with a live Profit Desk | The public |

Live at `https://jonathanashaba86-del.github.io/blesses-digital-solutions/`

---

## 1 · The front door

The page that sells the studio. Dark, fast, and built to be read on a phone on Ugandan data.

- **Published pricing** — four packages with starting figures, so a caller already knows the shape
  of the number. Clicking a package pre-fills the enquiry form with the matching service and budget.
- **An enquiry form that actually delivers.** It qualifies the lead (service, budget, timeline),
  validates the phone number, issues a reference like `BDS-260911-4K2`, and opens WhatsApp with the
  whole brief already written. Email and copy-to-clipboard are offered as fallbacks if WhatsApp
  does not open.
- **No invented proof.** There are no fabricated testimonials — the case study is a live site you
  can open and use. Add real client quotes as they arrive.
- Structured data, Open Graph, canonical URL and a sitemap, so it can be found.

### The four lines that make it yours

Near the bottom of `index.html`:

```js
var CFG = {
  wa       : '256777691011',                 // WhatsApp, international format, no +
  email    : 'jonathanashaba86@gmail.com',
  endpoint : '',                             // optional: a Formspree / Apps Script URL to also POST leads to
  ga       : ''                              // GA4 id — blank means no tracking loads at all
};
```

> **Confirm the prices before you share the link.** The figures in the pricing section
> (450k / 1.2M / 2.5M / 600k per month) are starting points set to Kampala SME rates.
> They are yours to change — edit the `.amt` values in the pricing cards.

---

## 2 · The Lead Desk — `leads/`

An enquiry is worth nothing until somebody works it. The desk is where that happens.

It is one HTML file. Every lead lives in that browser's own storage: nothing is uploaded, no
account is needed, and there is no monthly fee. That also means **the data is only on the device
you use it on** — take backups (Settings → Download backup) and restore them on any other device.

### How a lead reaches the desk

| Route | What happens |
|---|---|
| **The website form, same device** | The form leaves the brief in the browser; the desk picks it up the moment you open it. Nothing to do. |
| **A WhatsApp message on your phone** | Open the desk, hit **Paste enquiry**, paste the message. The desk reads the name, phone, email, business, service, budget, timeline and notes out of it. Several messages at once are fine. |
| **A call or a walk-in** | **+ New lead**, type what you know. Anything you do not know yet can stay blank. |
| **A form service** | Set `CFG.endpoint` on the front door to a Formspree or Apps Script URL and every brief is posted there too. |

Duplicates are caught on phone number and email before anything is added twice.

### What the desk works out for you

**A score out of 100, and it shows its working.** Six readable signals — budget (30), urgency (22),
service fit (14), how reachable they are (12), how engaged they are (14) and how fresh the lead is
(8). Open any lead and every signal is drawn as a bar with the reason behind it. Nothing is hidden:
the whole model is the `scoreOf()` function, and you can change any number in it.

- **Hot** is 72 and above, **Warm** 48–71, **Cold** below that.
- **Today** ranks every open lead by score plus how overdue it is, and puts the five you should
  actually call at the top.
- **Next best action** on every lead: what to do now, in a sentence, changing with the stage and
  the clock.
- **An SLA clock.** Reply to a new lead within 2 hours, follow up a contacted one within 2 days,
  quote within 3, chase within 3 — all editable in Settings. Miss one and the lead goes red
  everywhere it appears.
- **Drafted follow-ups.** Eight message templates — first reply, follow-up, qualifying questions,
  the quote, the chase, the quiet-lead close, the welcome, the review request — each written with
  the client's name, their service, the estimated figure and the sender's name already in place.
  Send on WhatsApp in one click, or copy and edit first. It writes a first draft; you read it
  before it goes.
- **Pipeline value.** Every lead gets an estimated value from its budget band, and the board totals
  each column weighted by how often that stage actually closes — so the forecast is honest.
- **Assignment across the team.** Five people by default, editable. New leads are suggested to
  whoever has the fewest open, and the leaderboard shows who is carrying what.
- **Reports.** Win rate, revenue won, weighted pipeline, average first-response time, the funnel,
  where leads come from, what they ask for, and the team leaderboard — all computed live.

### Running it

Open `leads/` and set a passcode on the first run.

> The passcode is a **soft lock** that keeps the page tidy on a shared laptop. It is not
> encryption, and anyone who can open the browser's developer tools can read around it. Treat it
> as a door you close, not a safe.

The desk is excluded from search engines in `robots.txt` and carries `noindex`.

Keyboard: `/` searches, `N` opens a new lead, `Esc` closes anything open.

---

## 3 · MANNIE — `mannie/`

The flagship client build. A fashion storefront where every garment sits on a turntable: drag it
and it turns a full 360°, front to back, so a customer reads the stitching before they commit.

| | |
|---|---|
| **57 products** | 14 categories — tops, outerwear, bottoms, dresses, sleep, footwear, bags, belts, eyewear, headwear, accessories, intimates, heritage |
| **126 photographs** | A front and a back frame for almost every piece |
| **3D vector fallback** | Every silhouette is also drawn as an extruded SVG garment, so a failed image never shows a broken box |
| **Live stock** | Per-size counts, "only N left" and sold-out states |
| **WhatsApp checkout** | The bag becomes a formatted order with a reference like `MN-260906-4K2` |
| **A bag that survives** | Bag, saved pieces, recently viewed and delivery details persist in the browser |
| **Sendable links** | Every piece has its own URL; back and forward work |
| **Search** | `/` or `⌘K`, matching name, category, material, fit, colourway and size |
| **Care pages** | Size guide with real measurements, shipping, returns, repairs, order tracking |
| **Installable** | Manifest, icons and a service worker — add to home screen, opens offline |
| **Photo Studio** | A built-in panel (⧉, bottom left) to swap any product's photography without touching the code |

Its own configuration block sits near the bottom of `mannie/index.html`, in the same shape as the
front door's. Reviews live in the `REVIEWS` array beside it and ship empty on purpose — the page
shows an honest invitation rather than invented praise.

### Replacing the photography

1. Open the site and click **⧉ Photo Studio** (bottom left).
2. Pick a product, paste a **front** image URL, optionally a **back** one.
3. For a true turntable, paste 8–36 frames (one per line) into the 360° box — dragging then scrubs
   the real frames.
4. **Apply** to preview, **Export code**, and paste the block over the `SHOTS` object near the top
   of the script.

Shooting a 360°: phone on a tripod, product on a turntable marked at 24 points, one frame per mark.
Never move the phone.

---

## Deploying

GitHub Pages serves this repository from the root of `main`, so **merging to `main` publishes** —
nothing to build, nothing to configure. Anything that serves static files works just as well:
drag the folder into Netlify or Vercel, or upload it to a cPanel `public_html`.

To move a site onto its own domain: point the domain at Pages, add a `CNAME` file, and set `site`
in that page's config block to the new address.

Adding the next client demo is the same shape: a new folder, a new card on the front door. The root
link never changes.

---

## Built by

**Blessed Digital Solutions** — web development, digital marketing, branding and content.
WhatsApp [+256 777 691011](https://wa.me/256777691011) · [jonathanashaba86@gmail.com](mailto:jonathanashaba86@gmail.com)

---

## 4 · Nyumba Furniture Co. — `nyumba/`

A contract-furniture storefront built to be shown to a buyer who answers to a board. Photography-led,
no illustrations, no placeholders — 38 pieces across eight rooms, each with real product imagery,
full specification, volume breaks and a working quotation flow.

### What makes it different from a catalogue

Most furniture sites stop at "here is a sofa, here is a price". This one carries a **Profit Desk** —
a live business-analytics layer that models the money behind the order:

| Panel | What it answers |
|---|---|
| **Revenue & gross margin** | 12-month trading, margin overlaid, best and softest months called out |
| **Profit mix** | Which rooms actually carry the annual profit pool, not just the turnover |
| **The money cycle** | Cash conversion cycle — stock days + build days + collection days − supplier credit. Four sliders, live re-price, and what one week off the cycle is worth in cash |
| **Margin lab** | Cost, sell, margin and monthly contribution per line, with a price-uplift slider that models demand elasticity at −1.4 |
| **Deposit terms** | 90-day cash position for a single order: peak funding gap, the deposit that closes it |
| **Dead-stock radar** | Days of cover per stocked line, cash standing still, and the clearing action |

Every figure recomputes from the catalogue — change a price or a stock level in `P[]` and the whole
desk moves with it. It ships with demo trading data; point it at a real sales file and it reads
real lines.

### The four lines that make it yours

Near the top of the script block in `nyumba/index.html`:

```js
var CFG = {
  wa    : '256777691011',          // WhatsApp, international format, no +
  email : 'hello@nyumba.co.ug',
  vat   : 0.18,                    // URA standard rate
  breaks: [{q:50,d:.22},{q:25,d:.17},{q:10,d:.11},{q:5,d:.06}]   // volume bands
};
```

### Photography

All imagery is hot-linked from Unsplash at `images.unsplash.com`. If an image ever fails to load,
it degrades to a branded gradient tile carrying the piece name — a client never sees a broken-image
icon. Swap in your own product photography by editing the `ph:[...]` array on each item in `P[]`.

> **Note:** the Unsplash photo IDs were taken from the Unsplash API, but the build environment
> blocks outbound requests to `images.unsplash.com`, so the images could not be rendered during
> testing. Open the page once on a normal connection and confirm they load before sending the link
> to a client.

### Tested

Rendered headless at 1440px and 390px: no JavaScript errors, no horizontal overflow on mobile,
light and dark themes both legible, and every interactive control exercised — filters, sort, search,
product detail, quantity, quotation drawer, volume calculator, all six Profit Desk panels, and form
validation through to the WhatsApp hand-off.
