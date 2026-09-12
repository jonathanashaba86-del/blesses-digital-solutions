# Blessed Digital Solutions — storefront portfolio

Three complete, working online stores built by **Blessed Digital Solutions** (Kampala, Uganda).
Every one is a single HTML file: no build step, no server, no npm, no monthly platform fee.
Upload the folder anywhere that serves static files and it runs.

| | What it is | Live |
|---|---|---|
| **`index.html`** | The agency front door | [/blesses-digital-solutions/](https://jonathanashaba86-del.github.io/blesses-digital-solutions/) |
| **`furniture/`** | **NYUMBA** — furniture & fit-out supply, trade + retail | [/furniture/](https://jonathanashaba86-del.github.io/blesses-digital-solutions/furniture/) |
| **`camaratech/`** | **CAMARA TECH** — phones, laptops and Dubai sourcing | [/camaratech/](https://jonathanashaba86-del.github.io/blesses-digital-solutions/camaratech/) |
| **`mannie/`** | **MANNIE** — fashion, every garment turns 360° | [/mannie/](https://jonathanashaba86-del.github.io/blesses-digital-solutions/mannie/) |

---

## NYUMBA — furniture & fit-out supply

A storefront for a business that sells furniture to walk-in customers **and** to hotels, offices,
schools and other furniture shops. Most furniture businesses need both, and most furniture
websites only do the first.

### The commercial layer

| | |
|---|---|
| **Three price tiers** | Retail, Trade (−15%) and Contract (−25%). Apply in four fields and **every price on the site changes** — catalogue, product pages, room planner and bill of quantities. No "call for pricing", no separate trade catalogue to maintain |
| **Volume breaks that stack** | 5, 10, 25 and 50+ bands, up to a further 18% off, **on top of** the tier discount. The product page shows the whole ladder and tells you how many more units it takes to drop a band |
| **Quotes, not carts** | A furniture business does not check out — it asks for a quotation, shows it to someone, and comes back. The basket issues a numbered, dated, VAT-itemised quotation valid for 21 days, printable to PDF, sendable on WhatsApp, exportable to CSV |
| **MOQ and lead times** | Per piece. Ex-stock shows the number on the floor; made-to-order shows the real week count |
| **Deposits** | 50% on made-to-order, calculated and stated before anyone commits |
| **Trade terms** | 30 days from invoice on approved accounts, stated on the quotation |

### The tools that sell the job

| | |
|---|---|
| **Room planner** | Set your room in centimetres, drag pieces onto a to-scale floor plan, rotate them, nudge with the arrow keys. It costs the room live, colour-codes by category, draws rugs underneath the furniture, and warns you at 32% and 45% floor coverage — because above 45% a room stops having walkways. "Add all to my quote" moves the whole room across |
| **Container load calculator** | Every piece carries a real packed volume and gross weight. Pick 20ft, 40ft or 40ft high-cube and it shows the fill percentage, how many containers, **whether volume or weight is the limiting factor**, and an indicative freight cost. Usable volume is nominal less 14% — furniture does not tessellate |
| **Made-to-measure pricing** | Give it a type, dimensions, timber and finish and it returns the real rate-card number, live as you type, with lead time and deposit. Most of what a furniture workshop builds is not in its catalogue |
| **Projects & BOQ** | Specify one room type, set how many rooms there are, and the bill of quantities writes itself. Change "32 rooms" to "40" and the whole job reprices. Export the BOQ as CSV for the QS |
| **Live fabric & timber** | Seven fabrics, six timber finishes, four metals. Pick one and **the drawing repaints in it** — on the product page and on the catalogue cards. Order real swatches to a Ugandan address, free on a trade account |
| **Compare** | Four pieces, every row: price, volume, weight, pieces per container, warranty, full specification. Best value in each row marked |

### Also in there

Owner dashboard (order book, collected vs outstanding, production board, stock to watch, CSV export) ·
order tracking with a real production timeline · command palette on `⌘K` · a helper that answers
lead-time, trade-pricing, delivery and freight questions instantly and hands over to WhatsApp ·
light and dark themes · UGX / USD / KES / EUR · installable and works offline · `FurnitureStore`,
`Product`, `WebSite` and `FAQPage` structured data.

### Why the furniture is drawn and not photographed

Every one of the 38 pieces is a hand-built SVG. That is deliberate:

- a drawing **repaints instantly** in the customer's chosen timber and fabric — a photograph cannot
- it weighs nothing on a Kampala mobile connection
- it works with no connection at all
- it never 404s, and the shop is ready to sell before the photographer is booked

Shoot your real pieces later and drop the URL into `PRODUCTS[].photo`. The drawing stays as the fallback.

---

## CAMARA TECH — gadgets, priced in the open

A phone, laptop and accessories store for Uganda, with the three things its customers kept asking for.

| | |
|---|---|
| **Dubai landed-cost calculator** | Take a price off Amazon.ae or Noon and see the entire bill — freight by air express, air economy or sea, import duty, VAT, withholding, clearing, insurance and our service fee, **each as its own line**. Live as you type, with an arrival window and the deposit. Nobody gets surprised at the airport |
| **Trade-in valuation** | Make, model, honest condition and four checkboxes → a real figure in thirty seconds, plus what you would then pay for each upgrade. 8% more if you trade against a purchase |
| **IMEI & warranty check** | Fifteen digits, validated with the same Luhn check a real IMEI passes, against our register. Catches a fake phone and tells you whether it is covered |
| **Side-by-side compare** | Up to four products, every spec on one row, the strongest number in each row marked |
| **Instalment plans** | 3, 6 or 12 months with a 30% deposit, calculated on the product page |
| **Bundles** | Accessories added with a device come in 5% cheaper than buying them later |
| **Stock & price alerts** | One SMS, only when it actually happens — and the alerts become the owner's restock list |

Plus a saved cart and wishlist that survive a closed tab, multi-currency (UGX / USD / AED / KES),
light and dark themes, a `⌘K` command palette, an instant-answer helper, Camara Club points and
referral codes, a printable receipt, a WhatsApp order handoff, an owner's dashboard with CSV export,
and an installable offline app.

---

## MANNIE — fashion in the round

57 pieces, 126 photographs, and a turntable on every one: drag a garment and it turns a full 360°,
front to back, so a customer reads the stitching before they commit. Colourways recolour the piece
live, every size shows its real stock count, and the bag checks out over WhatsApp.
Full detail in the store itself; the Photo Studio panel (⧉, bottom left) swaps any product's
photography without opening the code.

---

## Making one of them yours

Each store has a single configuration block near the top of its `<script>`. Nothing else needs touching.

**`furniture/index.html`**

```js
const BIZ = { name:'Nyumba Furniture Co.', wa:'256777691011', email:'…', workshop:'…', … };
const CFG = { vat:18, adminPin:'7788', quoteDays:21, depositPct:50, creditDays:30, ga:'' };
const TIERS  = { retail:{off:0}, trade:{off:15}, contract:{off:25} };   // your discounts
const BREAKS = [{min:1,off:0},{min:5,off:4},{min:10,off:8},…];          // your volume ladder
const ZONES  = [ … ];                                                   // your delivery rates
const FINISHES / FABRICS / METALS = [ … ];                              // your real materials
const PRODUCTS = [ … ];                                                 // your catalogue
```

**`camaratech/index.html`**

```js
const BIZ    = { name:'Camara Tech', wa:'256790890630', momo:'…', … };
const CFG    = { ga:'', adminPin:'2468', instalment:{deposit:30, fee:4}, bundleSave:5 };
const LANDED = { aed:1035, vat:18, wht:6, clear:85000, service:7, modes:[…], cats:[…] };
const TRADE  = { Apple:{…}, Samsung:{…} };                              // trade-in price book
```

Set `CFG.ga` to a GA4 id and analytics starts flowing (`view_item`, `add_to_quote`, `purchase`,
`generate_lead`). Leave it blank and **no tracking script loads at all**.

---

## What none of these do

They are complete storefronts, not shops with a warehouse behind them. There is no payment
processor, no user accounts on a server, and no shared database: a quote, a cart, a saved list,
a project and a room plan all live in the customer's own browser, and nothing reaches anybody
until they press a button that says it will. That is the right architecture for a business that
sells on WhatsApp and takes MoMo — and when one of these clients outgrows it, the data shapes in
the config block are the API contract to build against.

## Deploying

```bash
# GitHub Pages — already live. Merging to main publishes.
# Netlify / Vercel — drag the folder in. No build command.
# Any cPanel host — upload the folder to public_html.
```

Pages serves `main` from the repository root. Nothing to build, nothing to configure.
To move a store onto its own domain: point the domain at Pages, add a `CNAME`, and set
`BIZ.site` / `CFG.site` in that store's config block.

## Tested

Both new storefronts ship with a browser test suite run against Chromium — 33 assertions for
Camara Tech, 58 for Nyumba — covering every route, the pricing engine, tier and volume discounts,
quote-to-order, the room planner drag, all four calculators, persistence across reloads, the
dashboard, and zero horizontal overflow at 390px. All passing.

## Built by

**Blessed Digital Solutions** — web development, digital marketing, branding and content.
WhatsApp [+256 777 691011](https://wa.me/256777691011) · [jonathanashaba86@gmail.com](mailto:jonathanashaba86@gmail.com)
