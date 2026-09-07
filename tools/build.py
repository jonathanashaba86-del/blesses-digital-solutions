# -*- coding: utf-8 -*-
"""
Build step. Reads tools/catalog.py and writes:
  shop/assets/img/products/<slug>.svg   one tile per line
  shop/assets/img/aisles/<slug>.svg     an aisle banner per department
  shop/assets/img/scenes/*.svg          hero, rider, storefront
  shop/assets/img/brand/*.svg           logo, favicon, payment marks
  shop/assets/js/data.js                the catalogue the site reads

Run:  python3 tools/build.py
"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from svgkit import Defs, canvas, lighten, darken, mix, text, ground

def uid_prefix(key):
    """Per-file gradient id prefix so two of these SVGs can share one document."""
    h = 0
    for ch in key:
        h = (h * 131 + ord(ch)) & 0xFFFFFF
    return "%s%x_" % (re.sub(r"[^a-z]", "", key.lower())[:4] or "x", h)
import draw_produce as produce
import draw_fresh as fresh
import draw_packaged as packaged
import draw_scenes as scenes
import catalog

IMG = os.path.join(ROOT, "shop", "assets", "img")
MODULES = {"produce": produce, "fresh": fresh, "packaged": packaged}

# label palettes for the generic archetypes, keyed off the accent colour
def _generic_lines(spec_body, accent):
    """'TOP|BIG|sub' or 'BIG|sub' -> label_block lines."""
    bits = [b for b in spec_body.split("|") if b != ""]
    dark = darken(accent, .30)
    if len(bits) == 1:
        return [(bits[0], 26, dark, 800, 0)]
    if len(bits) == 2:
        return [(bits[0], 24, dark, 800, 6), (bits[1], 12, accent, 600, 0)]
    return [(bits[0], 16, accent, 700, 5), (bits[1], 26, dark, 800, 8),
            ("|rule|", 0, accent, 700, 8), (bits[2], 12, accent, 600, 0)]

def draw_fn(art):
    """Resolve a catalogue art spec to a drawing function."""
    if "." in art and ":" not in art:
        mod, fn = art.split(".")
        return getattr(MODULES[mod], fn)
    kind, body = art.split(":", 1)
    parts = body.split("|")
    accent = parts[-1] if parts[-1].startswith("#") else None
    if accent:
        body = "|".join(parts[:-1])
    return packaged.generic(kind, _generic_lines(body, accent or "#4A5A68"), accent)

def write(path, svg):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

def build_products(rows):
    for r in rows:
        d = Defs(prefix=uid_prefix(r["slug"]))
        art = draw_fn(r["art"])(d, r["tint"])
        svg = canvas(art, d, tint=r["tint"], title=r["n"])
        write(os.path.join(IMG, "products", r["slug"] + ".svg"), svg)
    return len(rows)

AISLE_ART = {
    "Fresh produce":   [("produce.tomato", "#C4453C"), ("produce.matooke", "#8FA85A"), ("produce.carrot", "#CE7A32")],
    "Butchery & fish": [("fresh.beef", "#9C3B3B"), ("fresh.whole_fish", "#9EA893"), ("fresh.chicken", "#D8A863")],
    "Dairy & eggs":    [("fresh.milk_pouch", "#DDE4EC"), ("fresh.eggs", "#D6BE94"), ("fresh.cheese", "#D3A245")],
    "Bakery":          [("fresh.white_loaf", "#D6BC8E"), ("fresh.mandazi", "#C89B58"), ("fresh.chapati", "#CFA96E")],
    "Pantry":          [("packaged.rice", "#DAD3BC"), ("packaged.cooking_oil", "#D7B646"), ("packaged.beans", "#A0705A")],
    "Drinks":          [("packaged.coffee", "#7A5236"), ("packaged.water", "#A9C4CE"), ("packaged.soda_crate", "#B24545")],
    "Household":       [("packaged.detergent", "#7FA0BE"), ("packaged.tissue", "#D2D2CB"), ("packaged.charcoal", "#5B5A55")],
    "Baby & personal": [("packaged.generic", "#9AD2DE")],
}
AISLE_TINT = {"Fresh produce": "#8FA85A", "Butchery & fish": "#9C3B3B", "Dairy & eggs": "#C8B98A",
              "Bakery": "#D6BC8E", "Pantry": "#C0A878", "Drinks": "#7A8FA8",
              "Household": "#7FA0BE", "Baby & personal": "#7EBCCE"}

def build_aisles():
    """Wide banner per department: three of its own products on a tinted ground."""
    n = 0
    for num, name, blurb in catalog.AISLES:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        tint = AISLE_TINT[name]
        d = Defs(prefix=uid_prefix("aisle-" + slug))
        picks = AISLE_ART.get(name) or []
        if name == "Baby & personal":
            picks = [("poly:BABY|NAPPIES|size 4|#2E9DB0", "#9AD2DE"),
                     ("tube:FRESH|MINT|150 ml|#1E7AA8", "#DCE8F0"),
                     ("bar:BATH SOAP|3 × 100 g|#B04A6E", "#E4B8C4")]
        o = [f'<rect width="1200" height="480" fill="{lighten(tint, .88)}"/>',
             f'<circle cx="980" cy="120" r="230" fill="{tint}" opacity=".12"/>',
             f'<circle cx="180" cy="430" r="200" fill="{tint}" opacity=".10"/>']
        xs = [180, 560, 930]
        for (art, atint), x in zip(picks, xs):
            fn = draw_fn(art)
            o.append(f'<g transform="translate({x - 246},{-52}) scale(.62)">{fn(d, atint)}</g>')
        o.append(f'<rect x="0" y="0" width="1200" height="480" fill="none"/>')
        svg = canvas("".join(o), d, w=1200, h=480, tint=tint, pad_bg=False, title=name)
        write(os.path.join(IMG, "aisles", slug + ".svg"), svg)
        n += 1
    return n

def build_scenes(accent="#1B3EE8", flash="#F5C518"):
    made = []
    for name, fn, w, h, tint in [
        ("hero",       lambda d: scenes.hero(d, accent, flash),       1200, 820, "#EDEFF3"),
        ("rider",      lambda d: scenes.rider(d, accent, flash),       800, 600, "#DCE6F5"),
        ("storefront", lambda d: scenes.storefront(d, accent, flash),  800, 600, "#F5EFE2"),
        ("showcase",   lambda d: scenes.showcase(d, accent, flash),   1200, 780, "#E7EAEF"),
        ("devices",    lambda d: scenes.devices(d, accent, flash),     900, 700, "#E7EAEF"),
    ]:
        d = Defs(prefix=uid_prefix("scene-" + name))
        write(os.path.join(IMG, "scenes", name + ".svg"),
              canvas(fn(d), d, w=w, h=h, tint=tint, title=name))
        made.append(name)
    # empty-basket illustration
    d = Defs(prefix=uid_prefix("scene-empty"))
    o = [scenes.logo_mark(d, accent, flash, 128)]
    write(os.path.join(IMG, "scenes", "empty.svg"),
          canvas(f'<g transform="translate(136,86) scale(2.1)" opacity=".22">{o[0]}</g>', d,
                 w=400, h=400, tint="#C6CBD4", title="Empty basket"))
    made.append("empty")
    return made

def build_brand(accent="#1B3EE8", flash="#F5C518"):
    d = Defs(prefix=uid_prefix("brand-logo"))
    write(os.path.join(IMG, "brand", "logo.svg"),
          canvas(scenes.logo_mark(d, accent, flash, 128), d, w=128, h=128, tint="#FFFFFF",
                 pad_bg=False, title="Shop logo"))
    d = Defs(prefix=uid_prefix("brand-favicon"))
    write(os.path.join(IMG, "brand", "favicon.svg"),
          canvas(scenes.logo_mark(d, accent, flash, 64), d, w=64, h=64, tint="#FFFFFF",
                 pad_bg=False, title="favicon"))
    for k in ("momo", "airtel", "card", "cash"):
        d = Defs(prefix=uid_prefix("brand-pay-" + k))
        write(os.path.join(IMG, "brand", "pay-" + k + ".svg"),
              canvas(scenes.payment_mark(d, k), d, w=120, h=76, tint="#FFFFFF",
                     pad_bg=False, title=k))
    return 6

def build_data(rows):
    """Emit the JS catalogue. Same numbers the artwork was drawn from."""
    aisles = [{"n": num, "c": name, "blurb": blurb,
               "slug": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")}
              for num, name, blurb in catalog.AISLES]
    out = []
    for r in rows:
        item = {"id": r["id"], "slug": r["slug"], "n": r["n"], "c": r["c"], "u": r["u"],
                "price": r["price"], "cost": r["cost"], "stock": r["stock"], "sold": r["sold"],
                "tint": r["tint"], "d": r["d"],
                "img": "assets/img/products/%s.svg" % r["slug"]}
        for k in ("was", "size", "origin", "expiry"):
            if r.get(k):
                item[k] = r[k]
        if r["tags"]:
            item["tags"] = r["tags"]
        out.append(item)
    js = ("/* Generated by tools/build.py from tools/catalog.py — do not edit by hand.\n"
          "   Add or change a line in the catalogue and rebuild; the artwork and these\n"
          "   numbers are produced together so they cannot drift apart. */\n"
          "window.AISLES = %s;\n\nwindow.CATALOG = %s;\n"
          % (json.dumps(aisles, ensure_ascii=False, indent=2),
             json.dumps(out, ensure_ascii=False, indent=1)))
    write(os.path.join(ROOT, "shop", "assets", "js", "data.js"), js)
    return len(out)

if __name__ == "__main__":
    rows = catalog.rows()
    print("products :", build_products(rows))
    print("aisles   :", build_aisles())
    print("scenes   :", ", ".join(build_scenes()))
    print("brand    :", build_brand())
    print("data.js  :", build_data(rows), "lines")
