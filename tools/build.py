#!/usr/bin/env python3
"""Static site generator for Blessed Digital Solutions.

Content lives in data/site.json and data/products.json; this script renders the
committed HTML so the site stays a zero-dependency static deploy while every
page keeps identical chrome. Run: python3 tools/build.py
"""

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
SPEC = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
BRAND = SPEC["brand"]
PRODUCTS = SPEC["products"]

# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
ICONS = {
    "phone": '<path d="M6.6 3h3.2l1.6 4-2 1.4a12 12 0 0 0 5.2 5.2l1.4-2 4 1.6v3.2A2.6 2.6 0 0 1 17.4 19 14.4 14.4 0 0 1 5 6.6 2.6 2.6 0 0 1 6.6 3Z"/>',
    "chart": '<path d="M4 20V9m5 11V4m5 16v-7m5 7V7"/>',
    "radar": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12 18 6"/>',
    "team": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19.5a5.5 5.5 0 0 1 11 0"/><path d="M16 5.4a3.2 3.2 0 0 1 0 5.2M17.5 14.4a5.5 5.5 0 0 1 3 5.1"/>',
    "code": '<path d="m8.5 8-4 4 4 4M15.5 8l4 4-4 4M13.5 4.5l-3 15"/>',
    "growth": '<path d="M4 19h16M7 16V9m5 7V5m5 11v-4"/>',
    "brush": '<path d="M4 20s3.5.5 5-1 .2-3.6-1-4-3.4.6-3.4 2.6c0 1.4-.6 2.4-.6 2.4Z"/><path d="M9.5 15 19 5.5a2 2 0 0 0-2.8-2.8L6.7 12.2"/>',
    "play": '<circle cx="12" cy="12" r="8.5"/><path d="M10.4 9.2 15 12l-4.6 2.8V9.2Z"/>',
    "stack": '<path d="m12 3 8.5 4.5L12 12 3.5 7.5 12 3Z"/><path d="m3.5 12 8.5 4.5L20.5 12M3.5 16.5 12 21l8.5-4.5"/>',
}


def icon(name, size=24):
    body = ICONS.get(name, ICONS["stack"])
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def esc(text):
    return html.escape(str(text), quote=True)


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------
NAV_ITEMS = [
    ("Product Lab", "products/", "products"),
    ("Services", "index.html#services", "services"),
    ("Method", "index.html#method", "method"),
    ("Work", "index.html#work", "work"),
    ("Company", "index.html#company", "company"),
]


def head(*, root, title, description, canonical, page_class="", jsonld=""):
    nav_font = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600&family=Jost:wght@300;400;500;600&display=swap">'
    )
    ld = f'\n<script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#08122a">
<meta name="author" content="{esc(SITE['legalName'])}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['legalName'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:locale" content="en_UG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
{nav_font}
<link rel="stylesheet" href="{root}assets/css/bds.css">{ld}
</head>
<body{f' class="{page_class}"' if page_class else ''}>
<a class="skip-link" href="#main">Skip to content</a>
"""


def logo(root, sub="Product Lab"):
    return f"""<a class="mark" href="{root}index.html" aria-label="{esc(SITE['legalName'])} — home">
        <span class="mark__glyph" aria-hidden="true">B</span>
        <span class="mark__text">
          <span class="mark__name">Blessed Digital</span>
          <span class="mark__sub">{esc(sub)}</span>
        </span>
      </a>"""


def header(root, active=""):
    links = []
    for label, href, key in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{root}{href}"{current}>{esc(label)}</a>')
    return f"""<header class="site-header">
  <div class="wrap">
    <nav class="nav" data-nav aria-label="Primary">
      {logo(root)}
      <button class="nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <div class="nav__links">
        {''.join(links)}
        <a class="btn btn--gold btn--sm nav__cta" href="{root}index.html#contact">Book a briefing</a>
      </div>
    </nav>
  </div>
</header>
"""


def footer(root):
    product_links = "".join(
        f'<li><a href="{root}products/{p["slug"]}.html">{esc(p["name"])}</a></li>' for p in PRODUCTS
    )
    social = "".join(
        f'<li><a href="{esc(url)}" rel="noopener">{esc(name)}</a></li>'
        for name, url in SITE["social"].items()
    )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        {logo(root, SITE['location'])}
        <p class="footer-note" style="margin-top:1rem;">{esc(SITE['descriptor'])}</p>
      </div>
      <div>
        <h4>Product Lab</h4>
        <ul>{product_links}<li><a href="{root}products/">All four briefs</a></li></ul>
      </div>
      <div>
        <h4>Studio</h4>
        <ul>
          <li><a href="{root}index.html#services">Services</a></li>
          <li><a href="{root}index.html#method">How we work</a></li>
          <li><a href="{root}index.html#work">Selected work</a></li>
          <li><a href="{root}index.html#company">Company</a></li>
          <li><a href="{root}index.html#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{esc(SITE['email'])}">{esc(SITE['email'])}</a></li>
          <li><a href="tel:{SITE['phone'].replace(' ', '')}">{esc(SITE['phone'])}</a></li>
          <li>{esc(SITE['hours'])}</li>
        </ul>
        <h4 style="margin-top:1.5rem;">Follow</h4>
        <ul>{social}</ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> {esc(SITE['legalName'])}. All rights reserved.</p>
      <p>{esc(BRAND['palette'])} &nbsp;·&nbsp; {esc(BRAND['principle'].title())} &nbsp;·&nbsp; {esc(SITE['location'])}</p>
    </div>
  </div>
</footer>
<script src="{root}assets/js/bds.js" defer></script>
</body>
</html>
"""


def contact_section(root, preselect=""):
    options = ['<option value="">Select a product or service</option>']
    for p in PRODUCTS:
        sel = " selected" if p["slug"] == preselect else ""
        options.append(f'<option{sel}>{esc(p["name"])} — {esc(p["category"])}</option>')
    for s in SITE["services"]:
        options.append(f'<option>{esc(s["name"])}</option>')
    options.append("<option>Something else</option>")
    return f"""<section class="section section--dark" id="contact">
  <div class="wrap">
    <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:clamp(2rem,5vw,4rem);align-items:start;">
      <div class="stack" data-reveal>
        <p class="eyebrow">Book a briefing</p>
        <h2>Tell us the number you need moved.</h2>
        <p class="lede">A briefing is a real conversation, not a demo. We look at how your business earns today, where it leaks customers, and which of the four lines — if any — is worth your money first. If none of them is, we will say so.</p>
        <hr class="rule">
        <ul class="feature-list" style="gap:.75rem;">
          <li>Reply within one working day</li>
          <li>Founding-client terms while each line is in build</li>
          <li>No obligation, and no sales script</li>
        </ul>
        <div class="stack" style="gap:.35rem;margin-top:.5rem;">
          <p><strong style="color:#fff;">{esc(SITE['email'])}</strong></p>
          <p class="muted" style="color:#93a2bb;">{esc(SITE['phone'])} &nbsp;·&nbsp; WhatsApp {esc(SITE['whatsapp'])}</p>
          <p class="muted" style="color:#93a2bb;">{esc(SITE['location'])} &nbsp;·&nbsp; {esc(SITE['hours'])}</p>
        </div>
      </div>
      <form class="form panel panel--dark" data-enquiry-form="{esc(SITE['email'])}" data-reveal>
        <div class="form__row">
          <div class="field">
            <label for="f-name">Your name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" placeholder="Full name" required>
          </div>
          <div class="field">
            <label for="f-company">Business</label>
            <input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Company name">
          </div>
        </div>
        <div class="form__row">
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@business.com" required>
          </div>
          <div class="field">
            <label for="f-phone">Phone / WhatsApp</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+256 ...">
          </div>
        </div>
        <div class="field">
          <label for="f-product">Interested in</label>
          <select id="f-product" name="product">{''.join(options)}</select>
        </div>
        <div class="field">
          <label for="f-message">What are you trying to fix?</label>
          <textarea id="f-message" name="message" rows="5" placeholder="Missed calls, slow loan decisions, invisible in AI search, no receptionist — tell us plainly."></textarea>
        </div>
        <button class="btn btn--gold" type="submit">Send the brief {ARROW}</button>
        <p class="form__status" data-form-status role="status"></p>
        <p class="form__note">This site is hosted statically, so the form opens your email client with the brief prefilled — nothing is stored on a third-party server.</p>
      </form>
    </div>
  </div>
</section>
"""


def product_card(p, root, reveal=True):
    rev = " data-reveal" if reveal else ""
    return f"""<article class="pcard"{rev}>
  <div class="pcard__top">
    <span class="card__icon">{icon(p['icon'], 22)}</span>
    <span class="pcard__index">{esc(p['index'])} / 04</span>
  </div>
  <div>
    <p class="pcard__cat">{esc(p['category'])}</p>
    <h3 class="pcard__name">{esc(p['name'])}</h3>
  </div>
  <p class="pcard__quote">{esc(p['quote'])}</p>
  <p>{esc(p['summary'])}</p>
  <a class="pcard__more stretched" href="{root}products/{p['slug']}.html">Read the full brief {ARROW}</a>
</article>"""


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------
def build_home():
    root = ""
    canonical = SITE["domain"] + "/"
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": SITE["legalName"],
        "description": SITE["descriptor"],
        "url": canonical,
        "email": SITE["email"],
        "telephone": SITE["phone"],
        "areaServed": "UG",
        "address": {"@type": "PostalAddress", "addressLocality": "Kampala", "addressCountry": "UG"},
        "founder": {"@type": "Person", "name": SITE["founder"], "jobTitle": SITE["founderRole"]},
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": p["name"],
                                               "description": p["category"]}} for p in PRODUCTS
        ],
    }, ensure_ascii=False)

    services = "".join(
        f"""<article class="card" data-reveal>
      <span class="card__icon">{icon(s['icon'], 22)}</span>
      <h3>{esc(s['name'])}</h3>
      <p>{esc(s['body'])}</p>
    </article>""" for s in SITE["services"]
    )
    capabilities = "".join(
        f"""<article class="card card--dark" data-reveal>
      <h3>{esc(c['name'])}</h3>
      <p>{esc(c['body'])}</p>
    </article>""" for c in SITE["capabilities"]
    )
    platforms = "".join(
        f"""<article class="card" data-reveal>
      <span class="card__icon">{icon('stack', 22)}</span>
      <h3>{esc(pl['name'])}</h3>
      <p>{esc(pl['body'])}</p>
    </article>""" for pl in SITE["platforms"]
    )
    method = "".join(
        f"""<div class="step">
      <h4>{esc(m['title'])}</h4>
      <p>{esc(m['body'])}</p>
    </div>""" for m in SITE["method"]
    )
    projects = "".join(
        f"""<article class="card" data-reveal>
      <span class="chip chip--gold" style="justify-self:start;">{esc(w['tag'])}</span>
      <h3>{esc(w['name'])}</h3>
      <p>{esc(w['body'])}</p>
    </article>""" for w in SITE["projects"]
    )
    testimonials = "".join(
        f"""<figure class="card" data-reveal>
      <div style="color:var(--gold-500);letter-spacing:.2em;">★★★★★</div>
      <blockquote class="serif-quote" style="font-size:var(--step-1);color:var(--navy-800);">“{esc(t['quote'])}”</blockquote>
      <figcaption class="muted" style="font-weight:600;">— {esc(t['author'])}</figcaption>
    </figure>""" for t in SITE["testimonials"]
    )
    faq = "".join(
        f"""<details>
      <summary>{esc(f['q'])}</summary>
      <p>{esc(f['a'])}</p>
    </details>""" for f in SITE["faq"]
    )
    cards = "".join(product_card(p, root) for p in PRODUCTS)
    hero_index = "".join(
        f'''<a href="{root}products/{p['slug']}.html">
        <span class="hero-index__no">{esc(p['index'])}</span>
        <span class="hero-index__name">{esc(p['name'])}</span>
        {ARROW}
        <span class="hero-index__cat">{esc(p['category'])}</span>
      </a>''' for p in PRODUCTS
    )

    body = f"""{header(root, "")}
<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero__layout">
    <div class="hero__inner">
      <p class="eyebrow" data-reveal>{esc(SITE['legalName'])}</p>
      <h1 data-reveal>Built to be <em>the obvious choice</em> in your market.</h1>
      <p class="hero__lede" data-reveal>{esc(SITE['descriptor'])}</p>
      <div class="btn-row" data-reveal>
        <a class="btn btn--gold" href="{root}products/">See the four new products {ARROW}</a>
        <a class="btn btn--ghost" href="#services">Studio services</a>
      </div>
      <div class="hero__meta" data-reveal>
        <span>{esc(SITE['location'])}</span>
        <span>{esc(SITE['teamSize'])}</span>
        <span>{esc(BRAND['principle'].title())}</span>
      </div>
    </div>
    <aside class="hero-index" data-reveal aria-label="The four product lines">
      <div class="hero-index__head"><span>{esc(BRAND['division'])}</span><span>04 lines</span></div>
      {hero_index}
    </aside>
    </div>
  </div>
</section>

<section class="section section--tight section--ink">
  <div class="wrap">
    <div class="metric-strip" data-reveal>
      <div class="metric"><b>04</b><span>Products in the lab</span></div>
      <div class="metric"><b>04</b><span>Platforms already running</span></div>
      <div class="metric"><b>05</b><span>People in the studio</span></div>
      <div class="metric"><b>24/7</b><span>AI reception, once live</span></div>
    </div>
  </div>
</section>

<section class="section" id="products">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center" data-reveal>{esc(BRAND['division'])}</p>
      <h2 data-reveal>Four new revenue lines, in build order.</h2>
      <p class="lede" data-reveal>Concept and design briefs for four new revenue lines — each one sold against a business outcome, never as a software licence.</p>
    </div>
    <div class="grid grid-2">{cards}</div>
    <div class="btn-row btn-row--center" style="margin-top:2.5rem;" data-reveal>
      <a class="btn btn--outline" href="{root}products/">Open the full specification {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--dark" id="services">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Studio services</p>
      <h2 data-reveal>The work that pays for the lab.</h2>
      <p class="lede" data-reveal>Websites, brand and marketing delivered to the same standard as the products — because every client we build for is also the warm audience for what comes next.</p>
    </div>
    <div class="grid grid-4" style="margin-bottom:clamp(2rem,5vw,3.5rem);">{services.replace('class="card"', 'class="card card--dark"')}</div>
    <hr class="rule">
    <div class="section-head" style="margin-top:clamp(2.5rem,5vw,3.5rem);">
      <p class="eyebrow" data-reveal>Capability</p>
      <h2 data-reveal>What we are actually good at.</h2>
    </div>
    <div class="grid grid-4">{capabilities}</div>
  </div>
</section>

<section class="section" id="method">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>How we work</p>
      <h2 data-reveal>Four steps, one weekly rhythm.</h2>
      <p class="lede" data-reveal>The same operating model we run on ourselves is the one we sell — which is why our reports look like reports and our products ship.</p>
    </div>
    <div class="steps" data-reveal>{method}</div>
  </div>
</section>

<section class="section section--ink" id="platforms">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Infrastructure in production</p>
      <h2 data-reveal>The four products are not starting from zero.</h2>
      <p class="lede" data-reveal>Each new line extends something BDS already runs. That is why the first version arrives in weeks and why the economics work.</p>
    </div>
    <div class="grid grid-4">{platforms.replace('class="card"', 'class="card card--dark"')}</div>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Selected work</p>
      <h2 data-reveal>Featured projects.</h2>
    </div>
    <div class="grid grid-3">{projects}</div>
  </div>
</section>

<section class="section section--tight" id="testimonials" style="background:#fffdf8;">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center" data-reveal>Client testimonials</p>
      <h2 data-reveal>What clients say.</h2>
    </div>
    <div class="grid grid-3">{testimonials}</div>
  </div>
</section>

<section class="section" id="company">
  <div class="wrap">
    <div class="editorial">
      <div class="editorial__block" data-reveal>
        <p class="eyebrow">The company</p>
        <h2>Blessed Digital Solutions</h2>
        <p>Blessed Digital Solutions helps businesses establish a strong online presence through professional website development, digital marketing, branding, and content creation. We focus on delivering modern digital solutions that drive growth and increase visibility.</p>
        <p>{esc(SITE['teamSize'])} based in {esc(SITE['location'])}, led by {esc(SITE['founder'])}, {esc(SITE['founderRole'].lower())}. We build on infrastructure we run ourselves, we report weekly, and we sell before we build — so nothing here is a prototype waiting for a customer.</p>
        <div class="chips" style="margin-top:.5rem;">
          <span class="chip">Web engineering</span>
          <span class="chip">Brand systems</span>
          <span class="chip">Growth marketing</span>
          <span class="chip">AI products</span>
        </div>
      </div>
      <div class="panel panel--gold" data-reveal>
        <p class="panel__title">Operating principle</p>
        <p class="serif-quote">“Build it once, sell it to five existing clients before opening the next line.”</p>
        <hr class="rule">
        <ul class="feature-list">
          <li>Every product extends infrastructure already in production</li>
          <li>Every document is designed to be handed to a board</li>
          <li>Every client relationship is measured weekly, not annually</li>
          <li>Every price is anchored to an outcome, never to a licence</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight" id="faq" style="background:#fffdf8;">
  <div class="wrap-narrow">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center" data-reveal>Questions</p>
      <h2 data-reveal>Frequently asked.</h2>
    </div>
    <div class="faq" data-reveal>{faq}</div>
  </div>
</section>

{contact_section(root)}
</main>
{footer(root)}"""

    page = head(
        root=root,
        title=f"{SITE['legalName']} — Web Development, Brand & AI Products in Uganda",
        description=SITE["descriptor"],
        canonical=canonical,
        jsonld=jsonld,
    ) + body
    (ROOT / "index.html").write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------
# Product Lab hub
# --------------------------------------------------------------------------
def build_hub():
    root = "../"
    canonical = SITE["domain"] + "/products/"
    cards = "".join(product_card(p, "") for p in PRODUCTS)

    rows = "".join(f"""<tr>
      <th scope="row">{esc(p['name'])}</th>
      <td>{esc(p['category'])}</td>
      <td>{esc(', '.join(p['idealFor'][:3]))}</td>
      <td>{esc(' + '.join(p['priceModel']))}</td>
      <td>{esc(p['buildNotes'].split('.')[0])}.</td>
    </tr>""" for p in PRODUCTS)

    sequence = "".join(f"""<li>
      <small>Line {esc(p['index'])} / 04</small>
      <h4>{esc(p['name'])} — {esc(p['category'])}</h4>
      <p>{esc(p['positioning'])}</p>
    </li>""" for p in PRODUCTS)

    body = f"""{header(root, "products")}
<main id="main">

<section class="hero cover">
  <div class="wrap">
    <div class="hero__inner">
      <p class="eyebrow eyebrow--center" data-reveal>{esc(SITE['legalName'])}</p>
      <h1 data-reveal>{esc(BRAND['docTitle'])}</h1>
      <p class="hero__lede" data-reveal>{esc(BRAND['subtitle'])}</p>
      <p class="cover__lineup" data-reveal>{esc(BRAND['lineup'])}</p>
      <div class="btn-row btn-row--center" data-reveal>
        <a class="btn btn--gold" href="voicecore.html">Start with VoiceCore {ARROW}</a>
        <a class="btn btn--ghost" href="#matrix">Compare all four</a>
      </div>
      <div class="hero__meta" style="justify-content:center;" data-reveal>
        <span>{esc(BRAND['preparedFor'])}</span>
        <span>{esc(BRAND['date'])}</span>
        <span>{esc(BRAND['palette'])}</span>
      </div>
    </div>
  </div>
</section>

<section class="section" id="briefs">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>{esc(BRAND['division'])}</p>
      <h2 data-reveal>The four briefs.</h2>
      <p class="lede" data-reveal>Each brief states the problem in the client’s language, the experience we intend to deliver, the capabilities that make it real, the signature touches that make it premium, the build notes that make it cheap for us to ship, and the position that makes it worth paying for.</p>
    </div>
    <div class="grid grid-2">{cards}</div>
  </div>
</section>

<section class="section section--dark" id="matrix">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>At a glance</p>
      <h2 data-reveal>Four lines, one comparison.</h2>
      <p class="lede" data-reveal>Read across: who it is for, how it is priced, and what it extends inside the business we already run.</p>
    </div>
    <div class="table-scroll" data-reveal>
      <table class="matrix">
        <caption class="visually-hidden" style="position:absolute;left:-9999px;">Comparison of the four BDS Product Lab lines</caption>
        <thead>
          <tr><th scope="col">Product</th><th scope="col">Category</th><th scope="col">Ideal client</th><th scope="col">Commercial model</th><th scope="col">Extends</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section" id="sequence">
  <div class="wrap">
    <div class="editorial">
      <div class="editorial__block" data-reveal>
        <p class="eyebrow">{esc(SPEC['startHere']['eyebrow'])}</p>
        <h2>{esc(SPEC['startHere']['title'])}</h2>
        <p>{esc(SPEC['startHere']['body'][0])}</p>
        <p><strong>{esc(SPEC['startHere']['body'][1])}</strong></p>
        <div class="btn-row" style="margin-top:.5rem;">
          <a class="btn btn--navy" href="voicecore.html">Read the VoiceCore brief {ARROW}</a>
        </div>
        <p class="muted" style="font-size:.8rem;letter-spacing:.18em;text-transform:uppercase;margin-top:1rem;">{esc(SPEC['startHere']['footline'])}</p>
      </div>
      <div class="panel" data-reveal>
        <p class="panel__title">Release order</p>
        <ul class="timeline">{sequence}</ul>
      </div>
    </div>
  </div>
</section>

{contact_section(root)}
</main>
{footer(root)}"""

    page = head(
        root=root,
        title=f"{BRAND['docTitle']} — {BRAND['division']}",
        description=(f"{BRAND['subtitle']}: VoiceCore, ScoreCore, RadarCore and EmployCore — "
                     "four premium AI product lines from Blessed Digital Solutions."),
        canonical=canonical,
    ) + body
    (ROOT / "products" / "index.html").write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------
# Product specification pages
# --------------------------------------------------------------------------
def build_product(p, prev_p, next_p):
    root = "../"
    canonical = f"{SITE['domain']}/products/{p['slug']}.html"
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["name"],
        "category": p["category"],
        "description": p["quote"],
        "brand": {"@type": "Brand", "name": SITE["legalName"]},
        "url": canonical,
        "offers": {"@type": "Offer", "availability": "https://schema.org/PreOrder",
                   "priceCurrency": "UGX", "priceSpecification": {
                       "@type": "PriceSpecification", "description": p["positioning"]}},
    }, ensure_ascii=False)

    caps = "".join(f"<li>{esc(c)}</li>" for c in p["capabilities"])
    sig = "".join(f"<li>{esc(s)}</li>" for s in p["signature"])
    metrics = "".join(
        f'<div class="metric"><b>{esc(m["value"])}</b><span>{esc(m["label"])}</span></div>'
        for m in p["metrics"]
    )
    ideal = "".join(f'<span class="chip">{esc(i)}</span>' for i in p["idealFor"])
    rollout = "".join(f"""<div class="step">
      <h4>{esc(r['title'])}</h4>
      <p>{esc(r['body'])}</p>
    </div>""" for r in p["rollout"])
    price_lines = "".join(f"<li>{esc(line)}</li>" for line in p["priceModel"])

    roles_block = ""
    if p.get("roles"):
        roles = "".join(f"""<article class="card" data-reveal>
      <span class="card__icon">{icon('team', 22)}</span>
      <h3>{esc(r['name'])}</h3>
      <p>{esc(r['body'])}</p>
    </article>""" for r in p["roles"])
        roles_block = f"""
<section class="section" id="roles">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>The roles</p>
      <h2 data-reveal>Hire one. Or hire the team.</h2>
      <p class="lede" data-reveal>Modular roles the client mixes — each one introduced by name, with a handbook, and read-only by default on anything sensitive.</p>
    </div>
    <div class="grid grid-4">{roles}</div>
  </div>
</section>"""

    pager = f"""<section class="section section--tight">
  <div class="wrap">
    <nav class="pager" aria-label="Product briefs">
      <a href="{prev_p['slug']}.html"><small>Previous brief</small><b>&larr; {esc(prev_p['name'])}</b><span class="muted">{esc(prev_p['category'])}</span></a>
      <a class="is-next" href="{next_p['slug']}.html"><small>Next brief</small><b>{esc(next_p['name'])} &rarr;</b><span class="muted">{esc(next_p['category'])}</span></a>
    </nav>
  </div>
</section>"""

    body = f"""{header(root, "products")}
<main id="main">

<section class="spec-hero" data-watermark="{esc(p['index'])}">
  <div class="wrap">
    <p class="crumb"><a href="{root}index.html">Home</a> <span>/</span> <a href="index.html">Product Lab</a> <span>/</span> {esc(p['name'])}</p>
    <div class="spec-hero__grid">
      <div>
        <p class="counter"><b>{esc(p['index'])}</b> / 04 &nbsp;·&nbsp; {esc(BRAND['division'])}</p>
        <h1>{esc(p['name'])}</h1>
        <p class="spec-hero__cat">{esc(p['category'])}</p>
      </div>
      <div>
        <blockquote class="spec-hero__quote">“{esc(p['quote'])}”</blockquote>
      </div>
    </div>
    <div class="metric-strip" style="margin-top:clamp(2rem,4vw,3rem);">{metrics}</div>
  </div>
</section>

<section class="section" id="brief">
  <div class="wrap">
    <div class="editorial">
      <div class="editorial__block" data-reveal>
        <p class="eyebrow">The problem</p>
        <h2>Why this exists.</h2>
        <p>{esc(p['problem'])}</p>
      </div>
      <div class="editorial__block" data-reveal>
        <p class="eyebrow">The experience</p>
        <h2>How it should feel.</h2>
        <p>{esc(p['experience'])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark" id="capabilities">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Specification</p>
      <h2 data-reveal>Core capabilities &amp; premium signature touches.</h2>
      <p class="lede" data-reveal>The left column is what the product does. The right column is why it is worth paying a premium for — the details a competitor will not bother to build.</p>
    </div>
    <div class="grid grid-2">
      <div class="panel panel--dark" data-reveal>
        <p class="panel__title">Core capabilities</p>
        <ul class="feature-list">{caps}</ul>
      </div>
      <div class="panel panel--dark" data-reveal>
        <p class="panel__title">Premium signature touches</p>
        <ul class="feature-list">{sig}</ul>
      </div>
    </div>
  </div>
</section>
{roles_block}
<section class="section" id="rollout">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Rollout</p>
      <h2 data-reveal>From signature to live, in four moves.</h2>
    </div>
    <div class="steps" data-reveal>{rollout}</div>
    <div class="stack" style="margin-top:clamp(2rem,4vw,3rem);" data-reveal>
      <p class="eyebrow">Ideal client</p>
      <div class="chips">{ideal}</div>
    </div>
  </div>
</section>

<section class="section section--ink" id="commercials">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;">
      <div class="panel panel--dark" data-reveal>
        <p class="panel__title">Build notes</p>
        <h3>What it extends.</h3>
        <p style="color:#a7b4cb;">{esc(p['buildNotes'])}</p>
      </div>
      <div class="callout" data-reveal>
        <p class="panel__title" style="color:var(--gold-400);">Position &amp; pricing</p>
        <h3>How {esc(p['name'])} is sold.</h3>
        <p class="serif-quote" style="color:#e6ecf7;">{esc(p['positioning'])}</p>
        <ul class="price-lines">{price_lines}</ul>
        <hr class="rule">
        <p class="muted" style="color:#93a2bb;">Exact figures are quoted after a briefing call — they depend on volume and scope. Founding-client terms apply while this line is in build.</p>
        <div class="btn-row">
          <a class="btn btn--gold" href="{root}index.html#contact">Book a {esc(p['name'])} briefing {ARROW}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{pager}
{contact_section(root, preselect=p['slug'])}
</main>
{footer(root)}"""

    page = head(
        root=root,
        title=f"{p['name']} — {p['category']} | {SITE['legalName']}",
        description=f"{p['quote']} {p['positioning']}",
        canonical=canonical,
        jsonld=jsonld,
    ) + body
    (ROOT / "products" / f"{p['slug']}.html").write_text(page, encoding="utf-8")


# --------------------------------------------------------------------------
# 404 + sitemap + robots
# --------------------------------------------------------------------------
def build_extras():
    root = ""
    body = f"""{header(root, "")}
<main id="main">
<section class="hero">
  <div class="wrap">
    <div class="hero__inner">
      <p class="eyebrow">Error 404</p>
      <h1>This page has moved on.</h1>
      <p class="hero__lede">The address you followed does not exist here. The four product briefs and the studio are one click away.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="{root}index.html">Back to the studio {ARROW}</a>
        <a class="btn btn--ghost" href="{root}products/">Open the Product Lab</a>
      </div>
    </div>
  </div>
</section>
</main>
{footer(root)}"""
    page = head(root=root, title=f"Page not found — {SITE['legalName']}",
                description="The page you requested could not be found.",
                canonical=SITE["domain"] + "/404.html") + body
    (ROOT / "404.html").write_text(page, encoding="utf-8")

    urls = ["/", "/products/"] + [f"/products/{p['slug']}.html" for p in PRODUCTS]
    entries = "".join(
        f"  <url><loc>{SITE['domain']}{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.9' if u == '/products/' else '0.8'}</priority></url>\n"
        for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# AI answer engines are welcome to read and cite this site.\n"
        "User-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {SITE['domain']}/sitemap.xml\n", encoding="utf-8")


def main():
    build_home()
    build_hub()
    for i, p in enumerate(PRODUCTS):
        prev_p = PRODUCTS[(i - 1) % len(PRODUCTS)]
        next_p = PRODUCTS[(i + 1) % len(PRODUCTS)]
        build_product(p, prev_p, next_p)
    build_extras()
    print("Built: index.html, products/index.html, "
          + ", ".join(f"products/{p['slug']}.html" for p in PRODUCTS)
          + ", 404.html, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
