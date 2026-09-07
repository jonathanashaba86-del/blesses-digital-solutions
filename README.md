# Blessed Digital Solutions

Company website, plus **RetailCore** — a complete, ready-to-sell shop and supermarket
website with a full back office.

Everything here is static HTML, CSS and vanilla JavaScript. There is no build step to
deploy, no framework to keep up with, and no dependency that can break on someone
else's schedule. Open `index.html` in a browser and it works.

---

## What is in here

| Path | What it is |
|---|---|
| `index.html` | Blessed Digital Solutions company site — services, process, pricing, enquiry form |
| `assets/css/site.css` | Styles for the company site |
| `shop/` | **RetailCore** — the shop product we sell to clients |
| `tools/` | The image generator and catalogue build step |

### The shop (`shop/`)

| Page | What a visitor does there |
|---|---|
| `index.html` | Home — aisles, this week's cuts, best sellers, delivery zones |
| `shop.html` | Full catalogue with aisle filters, sort, search and stock counts |
| `product.html?p=<slug>` | One product: shelf price, unit price, stock, best-before |
| `deals.html` | Every reduced line, plus everything close to date |
| `cart.html` | Basket with quantities, delivery zone and a free-delivery meter |
| `checkout.html` | Three steps — contact, delivery, payment — then confirmation |
| `order.html?ref=<ref>` | Live order tracking from picking to the rider |
| `account.html` | Past orders, saved details, loyalty points |
| `delivery.html` | Zones, fees, minimums and the FAQ |
| `about.html`, `contact.html`, `404.html` | The rest of the site |
| `admin/index.html` | **Back office** — ten screens, see below |

### The back office (`shop/admin/`)

Ten screens, grouped the way a shop actually thinks:

- **Trading** — Today (live KPIs, sales chart, alerts, order queue), Orders (pick →
  weigh → confirm → dispatch, with substitutions and out-of-stock handling), Till
  (a working counter POS with keypad, tender and change)
- **Stock** — Inventory (stock at cost, reorder levels, expiry watch, per-line margin),
  Purchasing (supplier-grouped draft purchase orders)
- **People** — Customers (spend, order counts, lifetime value), Staff (rota, tills,
  a role permission matrix)
- **Admin** — Reports (top lines, thinnest margins, payment mix, operations), EFRIS
  (URA fiscal invoice queue with retry), Settings

An order placed on the storefront in the same browser appears in the back office
order queue. That is the fastest way to show a client how the two halves connect.

---

## Making it a different shop

Almost everything a client wants changed lives in **one file**.

### 1. `shop/assets/js/config.js`

Name, tagline, phone, WhatsApp, email, address, opening hours, currency, VAT rate,
free-delivery threshold, weight tolerance, cut-off time, delivery zones, payment
methods, promises, reviews and the FAQ.

```js
window.SHOP = {
  name:      "Kira Superstore",
  currency:  "UGX",
  freeOver:  150000,
  theme:     "superstore",   // or "market"
  zones:     [ /* fee, minimum basket and window per zone */ ],
  payments:  [ /* turn a method off and it leaves checkout */ ]
};
```

### 2. Themes

Two ship in the box, set with `SHOP.theme`:

- `superstore` — cobalt and flash yellow, big-format supermarket
- `market` — crimson and warm paper, neighbourhood grocer

Both are defined as CSS custom properties at the top of `shop/assets/css/store.css`.
A third theme is about fifteen lines of colour tokens.

### 3. Products

The catalogue is generated. Edit `tools/catalog.py`, then:

```bash
python3 tools/build.py
```

That one command writes **both** the product artwork and `shop/assets/js/data.js`,
so the pictures and the prices are produced from the same source and cannot drift
apart. A row looks like this:

```python
("Tomatoes", "Fresh produce", "kg", 5500, 3800, 8, 47, "#C4453C", "produce.tomato", None,
 "Ripe salad tomatoes, hand sorted.", {"was": 6500, "expiry": "+2", "tags": ["deal"]}),
# name, aisle, unit, price, cost, stock, sold, tint, art, pack size, description, extras
```

The `art` field is either a named drawing (`produce.tomato`) or one of ten generic
packaging archetypes, which is how a new SKU gets a clean tile without anyone
drawing anything:

`pack` · `carton` · `tall` · `bottle` · `jar` · `can` · `tube` · `poly` · `tray` · `bar`

```python
("Salt 1kg", "Pantry", "pack", 2000, 1300, 82, 29, "#CFD8E2",
 "pack:SEA SALT|iodised 1 kg|#2F5A8A", 1000, "Iodised table salt.", {}),
```

### 4. Real photographs

Every product record carries an `img` path. To use a photograph instead of the
generated artwork, drop a 4:3 image into `shop/assets/img/products/` with the same
slug (`tomatoes.jpg`) and point the record at it. Mixing photographs and generated
tiles looks fine because the generated ones share one lighting and background recipe.

---

## The image system

There are no third-party image URLs anywhere in this project. Every picture — 73
products, 8 aisle banners, hero art, the delivery rider, the shopfront, the logo and
the payment marks — is an SVG generated by `tools/` and served from this repository.
Nothing can 404 because someone else's CDN changed, the whole set is about 750 KB,
and it stays sharp on any screen.

| File | What it does |
|---|---|
| `tools/svgkit.py` | Primitives — spheres, packs, cylinders, leaves, labels, shadows |
| `tools/draw_produce.py` | Fresh produce |
| `tools/draw_fresh.py` | Butchery, fish, dairy, bakery |
| `tools/draw_packaged.py` | Pantry, drinks, household, plus the generic archetypes |
| `tools/draw_scenes.py` | Hero, rider, shopfront, showcase, devices, logo, payment marks |
| `tools/catalog.py` | The catalogue itself — the single source of truth |
| `tools/build.py` | Writes every image and `data.js` |

Regenerate everything:

```bash
python3 tools/build.py
```

To preview the artwork as a contact sheet while editing it, `pip install cairosvg`
and use `tools/preview.py`.

---

## Running it locally

No build, no server required — but a local server avoids browser file:// restrictions:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Deploying

Upload the whole folder to any static host — Netlify, Vercel, GitHub Pages, cPanel,
or plain shared hosting. There is nothing to compile and no runtime to install.

---

## Before you hand a site to a client

- [ ] Replace the placeholder phone, WhatsApp and email in `shop/assets/js/config.js`
      **and** in `index.html` (search for `256700000000` and `hello@blesseddigital.ug`)
- [ ] Set the real trading name, address and opening hours
- [ ] Load the client's real catalogue in `tools/catalog.py` and rebuild
- [ ] Set delivery zones, fees and minimum baskets to the client's actual rounds
- [ ] Connect real payment gateways — checkout currently simulates the mobile money
      prompt so the flow can be demonstrated end to end
- [ ] Point EFRIS at the client's URA credentials
- [ ] Decide whether to keep the "Built by Blessed Digital Solutions" credit in the
      shop footer (`shop/assets/js/store.js`, in `footer()`)

## What is demonstration behaviour

Honest about what is real and what is staged, so nobody is surprised in a client
meeting:

- **Real:** the whole catalogue, basket maths, unit pricing, weighed-line estimates
  and settlement, delivery fees and minimums, free-delivery thresholds, VAT, search,
  filters, sorting, order references, order tracking, the basket persisting across
  pages and refreshes, and every back-office calculation shown on screen.
- **Simulated:** payment authorisation (the mobile money prompt resolves after a
  short delay), SMS notifications, the EFRIS submission to URA, and Excel exports.
  Each is a single integration point, wired to a real provider during a build.
- **Seeded:** the back office ships with six demo orders, suppliers, staff and
  customers so the screens are not empty in a demo. Storefront orders placed in the
  same browser are added to that queue live.
