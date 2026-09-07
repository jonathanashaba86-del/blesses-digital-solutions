# Blessed Digital Solutions — Studio Site & Product Lab

A zero-dependency static site for **Blessed Digital Solutions (BDS)**: the studio
homepage plus a full premium showcase for the four new product lines defined in
the *Premium Product Specifications* brief.

**Live sections**

| Page | Purpose |
| --- | --- |
| `index.html` | Studio homepage — positioning, the four products, services, capability, method, infrastructure, work, testimonials, FAQ, contact |
| `products/index.html` | Product Lab cover — all four briefs, comparison matrix, release order |
| `products/voicecore.html` | 01 / 04 — AI Reception & Call Intelligence |
| `products/scorecore.html` | 02 / 04 — AI Credit Intelligence for SACCOs |
| `products/radarcore.html` | 03 / 04 — AI Visibility Intelligence |
| `products/employcore.html` | 04 / 04 — White-Label AI Workforce |

## The four product lines

1. **VoiceCore** — *“The receptionist who never sleeps, never misses a call, and never forgets a customer.”*
   24/7 call, WhatsApp and web-chat answering with one shared memory, live booking,
   English/Luganda/Swahili, human hand-off with full transcript. Extends the Bulk-SMS
   Dashboard's Africa's Talking integration; bookings write into InvCore.
2. **ScoreCore** — *“Turn every mobile-money transaction into a lending decision a board can defend.”*
   MTN MoMo and Airtel Money pattern analysis, explainable credit memos, UMRA-ready audit
   trail. Sits beside ComplyCore UG and reports into PayCore UG.
3. **RadarCore** — *“Google isn't where your next customer is asking anymore.”*
   Multi-engine AI-mention auditing (ChatGPT, Gemini, Perplexity), head-to-head competitor
   visibility, schema implementation, answer-ready rewrites, live mention tracker.
4. **EmployCore** — *“The same AI team running BDS, now working for your business.”*
   Modular Reception / Bookkeeping / Marketing / Sales-follow-up roles, hired like staff,
   with handbooks, a weekly manager's report and a live activity log.

**Build order:** VoiceCore first — it rides infrastructure BDS already runs, and every
existing website client is a warm pitch. Sell it to five clients before opening the next line.

## VoiceCore — the working app

Line 01 is no longer a brief. `app/voicecore/` is a running AI receptionist that
needs no backend, no API keys and no build step.

| File | What it is |
| --- | --- |
| `app/voicecore/demo.html` | A client's site with the receptionist live on it — the page you pitch from |
| `app/voicecore/index.html` | The owner's dashboard: conversation feed, bookings, leads, Voice of the Customer brief, white-label setup |
| `app/voicecore/widget.js` | The embeddable widget — chat, browser voice, channel switching |
| `app/voicecore/engine.js` | Intent detection, slot filling, opening-hours logic, storage, reporting |

**What works today**

- 24/7 answering on web chat, with WhatsApp and phone channels sharing one memory
- Booking against the client's real opening hours, including rescheduling off a closed day
- English, Luganda and Kiswahili — the receptionist follows whichever the customer uses
- Browser speech in and out (Chrome/Edge for voice input; typing works everywhere)
- Automatic tagging as booking, lead, complaint or question — tags escalate, never downgrade
- Complaints flagged urgent; hand-off to a human carrying the full transcript
- A monthly Voice of the Customer brief generated from real conversations, print-ready
- White-labelling per client from the dashboard: business name, persona, hours, services, prices

**Try it**

```bash
python3 -m http.server 8000
# then open http://localhost:8000/app/voicecore/demo.html
# and http://localhost:8000/app/voicecore/index.html
```

Click **Load sample day** on the dashboard to populate a realistic day of calls
before a client demo.

**Put it on a client's site** — two tags before `</body>`:

```html
<script src="/app/voicecore/engine.js"></script>
<script src="/app/voicecore/widget.js"
        data-business="Nakawa Dental Clinic"
        data-persona="Maria"
        data-phone="+256 700 123 456"></script>
```

**One file to email a client**

```bash
python3 tools/build_standalone.py
# -> dist/voicecore-standalone.html  (~92 KB, no external files)
```

The client site and the owner's dashboard on one page, with everything inlined.
Works offline, from a USB stick, or as an email attachment — useful when the
meeting room's wifi is not.

**Deliberate limits, so nobody is misled in a sales meeting**

- Answers are deterministic, not generative: the receptionist quotes prices, hours
  and services from the configured profile and never invents one. Open questions it
  cannot place are handed to a human rather than guessed at.
- Storage is `localStorage`, so the feed is per-browser. A shared team inbox needs a
  server — that is the first upgrade.
- "Phone" and "WhatsApp" are channel modes in the widget, proving the shared-memory
  behaviour. Real phone lines connect through the Africa's Talking integration the
  Bulk-SMS Dashboard already runs.
- The Luganda and Kiswahili strings in `engine.js` should be read by a native speaker
  before a client sees them.

**The upgrade path** — the intent layer is the auditable floor, not a ceiling. Point
`Brain.reply()`'s `unknown` branch at the Claude API and open questions get answered
too, while booking, pricing and hours stay deterministic and defensible.

## Structure

```
├── index.html              # generated
├── 404.html                # generated
├── sitemap.xml             # generated
├── robots.txt              # generated
├── products/               # generated (hub + 4 spec pages)
├── data/
│   ├── site.json           # studio content: contact, services, work, FAQ, method
│   └── products.json       # the four product briefs, verbatim from the spec
├── assets/
│   ├── css/bds.css         # navy & gold design system (tokens, components, print)
│   ├── js/bds.js           # nav, scroll reveal, enquiry form — progressive enhancement
│   └── img/logo.svg        # brand mark, also used as favicon
├── app/voicecore/          # the working AI receptionist (engine, widget, dashboard, demo)
├── dist/                   # generated: the single-file VoiceCore demo
├── tools/
│   ├── build.py            # renders every HTML page from the JSON content
│   └── build_standalone.py # bundles the VoiceCore app into one HTML file
└── netlify.toml            # headers, caching, vanity redirects (/voicecore etc.)
```

## Editing content

**Never hand-edit the generated HTML** — it is overwritten on the next build. Change the
JSON, then rebuild:

```bash
python3 tools/build.py      # no dependencies beyond Python 3
python3 -m http.server 8000 # preview at http://localhost:8000
```

Adding a fifth product is a matter of appending one object to `data/products.json`;
the card, hub row, spec page, comparison matrix, sitemap and prev/next pager all follow.

## Before going live

These placeholders live in `data/site.json` and must be replaced with the real details:

- `domain` — currently `https://blesseddigitalsolutions.com` (used for canonical URLs, Open Graph and the sitemap)
- `email` — currently `hello@blesseddigitalsolutions.com`
- `phone` / `whatsapp` — currently `+256 700 000 000`
- `social` — Facebook, LinkedIn, Instagram and TikTok are `#` placeholders

The enquiry form is client-side only: it opens the visitor's mail client with the brief
prefilled, so nothing is stored on a third-party server. Swap `data-enquiry-form` handling
in `assets/js/bds.js` for a Netlify Form or a Supabase endpoint when a backend is wanted.

## Design system

Navy & gold, as specified. Tokens sit at the top of `assets/css/bds.css` — brand ramps
(`--navy-*`, `--gold-*`), a fluid type scale (`--step--1` … `--step-5`), spacing, radii and
shadows. Typography is Jost (display) over Inter (body), matching the spec document.

Accessibility and robustness: skip link, visible focus rings, `aria-current` on the active
nav item, keyboard-dismissible mobile nav, `prefers-reduced-motion` honoured, semantic
landmarks throughout, and a print stylesheet so any spec page prints as a clean leave-behind.

---

© Blessed Digital Solutions — Kampala, Uganda. Navy & Gold · Sell before build.
