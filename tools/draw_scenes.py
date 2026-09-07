"""Hero art, aisle banners, delivery scene and brand marks."""
from svgkit import *
import draw_produce as P, draw_fresh as F, draw_packaged as K

def _place(inner, tx, ty, scale):
    return f'<g transform="translate({tx},{ty}) scale({scale})">{inner}</g>'

def grocery_bag(d, accent="#1B3EE8", flash="#F5C518"):
    """Hero subject — a full kraft bag, the week's shop standing up out of it."""
    o = [ground(d, 400, 706, 250, 34, .24)]
    kraft = "#D9B68C"
    inner = darken(kraft, .42)
    # inside of the bag, so goods have something to sit in
    o.append(f'<path d="M210,322 L590,322 L586,394 L214,394 Z" fill="{inner}"/>')
    # the shop itself, standing in the bag
    o.append(_place(P.pineapple(d, "#D2A234"), 60, 34, .46))
    o.append(_place(F.milk_pouch(d, "#DDE4EC"), 300, 40, .44))
    o.append(_place(P.matooke(d, "#8FA85A"), 150, 86, .44))
    o.append(_place(F.loaf(d, "#D6BC8E"), 244, 104, .40))
    o.append(_place(P.carrot(d, "#CE7A32"), 86, 118, .38))
    o.append(_place(P.greens(d, "#5C8748"), 296, 140, .34))
    o.append(_place(P.tomato(d, "#C4453C"), 178, 168, .36))
    # front panel of the bag, drawn over the goods
    g = d.linear3(darken(kraft, .20), lighten(kraft, .18), darken(kraft, .28), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M212,368 L588,368 L566,690 C565,706 553,714 536,714 L264,714 '
             f'C247,714 235,706 234,690 Z" fill="url(#{g})"/>')
    # folded top lip
    o.append(f'<path d="M208,344 L592,344 L588,384 L212,384 Z" fill="{lighten(kraft, .22)}"/>')
    o.append(f'<path d="M208,344 L592,344 L590,358 L210,358 Z" fill="{lighten(kraft, .40)}"/>')
    # side crease and paper texture
    o.append(f'<path d="M296,382 L292,712" stroke="{darken(kraft, .24)}" stroke-width="3" opacity=".28" fill="none"/>')
    o.append(f'<path d="M504,382 L508,712" stroke="{darken(kraft, .24)}" stroke-width="3" opacity=".28" fill="none"/>')
    o.append(f'<rect x="226" y="382" width="30" height="326" fill="#fff" opacity=".20"/>')
    o.append(f'<rect x="544" y="382" width="18" height="326" fill="#000" opacity=".07"/>')
    # printed band with the basket glyph — stands in for the shop\'s own logo
    o.append(f'<rect x="268" y="470" width="264" height="126" rx="12" fill="{accent}" opacity=".96"/>')
    o.append(f'<path d="M362,516 C362,500 438,500 438,516" stroke="{flash}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M348,520 L452,520 L442,568 C441,573 437,576 432,576 L368,576 C363,576 359,573 358,568 Z" fill="#FFFFFF"/>')
    o.append(f'<rect x="348" y="520" width="104" height="11" rx="3" fill="{flash}"/>')
    o.append(f'<rect x="292" y="614" width="216" height="7" rx="3.5" fill="#FFFFFF" opacity=".55"/>')
    o.append(f'<rect x="332" y="634" width="136" height="7" rx="3.5" fill="#FFFFFF" opacity=".32"/>')
    return "".join(o)

def hero(d, accent="#1B3EE8", flash="#F5C518", w=1200, h=820):
    """Warm studio ground with soft blobs, the bag centred."""
    o = [f'<circle cx="300" cy="250" r="240" fill="{accent}" opacity=".07"/>',
         f'<circle cx="920" cy="560" r="300" fill="{flash}" opacity=".12"/>',
         f'<circle cx="880" cy="200" r="130" fill="{accent}" opacity=".05"/>']
    # faint aisle floor line
    o.append(f'<path d="M0,700 L1200,700" stroke="{accent}" stroke-width="2" opacity=".10"/>')
    o.append(_place(grocery_bag(d, accent, flash), 208, 26, .96))
    return "".join(o)

def rider(d, accent="#1B3EE8", flash="#F5C518"):
    """Delivery rider — boda with an insulated box on the back."""
    o = [ground(d, 400, 470, 260, 26, .20)]
    tyre, rim = "#26313B", "#8A98A4"
    for cx in (232, 588):
        o.append(f'<circle cx="{cx}" cy="418" r="76" fill="{tyre}"/>')
        o.append(f'<circle cx="{cx}" cy="418" r="46" fill="{rim}"/>')
        o.append(f'<circle cx="{cx}" cy="418" r="14" fill="{darken(rim, .30)}"/>')
        for a in range(0, 360, 45):
            import math
            x2 = cx + 42 * math.cos(math.radians(a)); y2 = 418 + 42 * math.sin(math.radians(a))
            o.append(f'<path d="M{cx},418 L{x2:.1f},{y2:.1f}" stroke="{lighten(rim, .30)}" stroke-width="4"/>')
    # frame
    o.append(f'<path d="M232,418 L360,330 L470,330 L588,418" stroke="{accent}" stroke-width="20" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M360,330 L392,418" stroke="{accent}" stroke-width="16" fill="none" stroke-linecap="round"/>')
    # seat + tank
    o.append(f'<path d="M338,326 q66,-26 132,-4 q6,20 -14,24 l-104,2 Z" fill="#1E2A33"/>')
    # handlebars
    o.append(f'<path d="M600,406 L636,300" stroke="#41505C" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<path d="M604,304 q40,-16 74,-2" stroke="#41505C" stroke-width="13" stroke-linecap="round" fill="none"/>')
    # insulated delivery box
    o.append(rbox(d, 152, 208, 206, 148, 12, flash, top_face=26))
    o.append(f'<rect x="178" y="258" width="154" height="74" rx="8" fill="#FFFFFF" opacity=".94"/>')
    o.append(f'<rect x="178" y="258" width="154" height="10" rx="5" fill="{accent}"/>')
    o.append(f'<path d="M212,300 l18,18 l40,-44" stroke="{accent}" stroke-width="9" fill="none" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    # strut tying the box to the frame
    o.append(f'<path d="M256,356 L268,412" stroke="#41505C" stroke-width="11" stroke-linecap="round"/>')
    # motion lines
    for i, y in enumerate((300, 344, 388)):
        o.append(f'<path d="M{92 - i * 22},{y} L{176 - i * 12},{y}" stroke="{accent}" stroke-width="7" '
                 f'opacity="{.30 - i * .06}" stroke-linecap="round"/>')
    return "".join(o)

def storefront(d, accent="#1B3EE8", flash="#F5C518"):
    """Shopfront with striped awning and crates — used on About / Contact."""
    o = []
    o.append(f'<rect x="120" y="180" width="560" height="330" rx="10" fill="#F3F1EC"/>')
    o.append(f'<rect x="120" y="180" width="560" height="330" rx="10" fill="none" stroke="#D8D3C8" stroke-width="3"/>')
    # awning
    for i in range(8):
        c = flash if i % 2 == 0 else "#FFFFFF"
        o.append(f'<path d="M{112 + i * 72},248 L{112 + (i + 1) * 72},248 L{112 + (i + 1) * 72 - 10},312 '
                 f'L{112 + i * 72 - 10},312 Z" fill="{c}"/>')
    o.append(f'<rect x="106" y="236" width="588" height="20" rx="6" fill="{accent}"/>')
    o.append(f'<path d="M102,312 L698,312 L690,326 L110,326 Z" fill="{darken(accent, .30)}" opacity=".25"/>')
    # sign board
    o.append(f'<rect x="248" y="186" width="304" height="46" rx="8" fill="{accent}"/>')
    o.append(f'<rect x="266" y="200" width="268" height="6" rx="3" fill="{flash}" opacity=".9"/>')
    o.append(f'<rect x="266" y="214" width="180" height="6" rx="3" fill="#FFFFFF" opacity=".5"/>')
    # door + windows
    o.append(f'<rect x="352" y="352" width="96" height="158" rx="6" fill="{accent}" opacity=".18"/>')
    o.append(f'<rect x="352" y="352" width="96" height="158" rx="6" fill="none" stroke="{accent}" stroke-width="4"/>')
    o.append(f'<circle cx="434" cy="436" r="6" fill="{accent}"/>')
    for x in (168, 496):
        o.append(f'<rect x="{x}" y="352" width="140" height="104" rx="6" fill="#DCE6F5"/>')
        o.append(f'<rect x="{x}" y="352" width="140" height="104" rx="6" fill="none" stroke="#BFCBDC" stroke-width="3"/>')
        o.append(f'<path d="M{x + 8},{448} L{x + 60},{360}" stroke="#FFFFFF" stroke-width="14" opacity=".55"/>')
    # produce crates on the pavement
    o.append(_place(P.tomato(d, "#C4453C"), 88, 300, .26))
    o.append(_place(P.mango(d, "#D08A2E"), 468, 300, .26))
    for cx in (196, 576):
        o.append(f'<path d="M{cx - 82},478 L{cx + 82},478 L{cx + 66},536 L{cx - 66},536 Z" fill="#C29A62"/>')
        o.append(f'<path d="M{cx - 82},478 L{cx + 82},478 L{cx + 78},492 L{cx - 78},492 Z" fill="#DCB781"/>')
        for k in (-1, 0, 1):
            o.append(f'<path d="M{cx + k * 44 - 3},492 L{cx + k * 44 - 6},534" stroke="{darken("#C29A62", .26)}" '
                     f'stroke-width="4" opacity=".45"/>')
    return "".join(o)

# ------------------------------------------------------------------ marks
def payment_mark(d, kind, w=120, h=76):
    """Flat payment badges — no third-party logos, safe to ship."""
    palette = {
        "momo":   ("#FFCC00", "#1A1400", "MoMo"),
        "airtel": ("#E4002B", "#FFFFFF", "Airtel"),
        "card":   ("#1A1F71", "#FFFFFF", "Card"),
        "cash":   ("#0E8A5F", "#FFFFFF", "Cash"),
    }
    bg, fg, lab = palette[kind]
    o = [f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="10" fill="{bg}"/>']
    if kind == "card":
        o.append(f'<rect x="14" y="24" width="{w - 28}" height="12" rx="3" fill="{fg}" opacity=".85"/>')
        o.append(f'<rect x="14" y="46" width="34" height="9" rx="3" fill="{fg}" opacity=".5"/>')
    elif kind == "cash":
        o.append(f'<rect x="16" y="20" width="{w - 32}" height="34" rx="5" fill="{fg}" opacity=".9"/>')
        o.append(f'<circle cx="{w / 2}" cy="37" r="10" fill="{bg}"/>')
    else:
        o.append(f'<rect x="{w / 2 - 15}" y="16" width="30" height="44" rx="6" fill="{fg}" opacity=".9"/>')
        o.append(f'<rect x="{w / 2 - 10}" y="22" width="20" height="28" rx="2" fill="{bg}"/>')
    o.append(text(w / 2, h - 8, lab, 13, fg, 700, "middle", 1, max_w=w - 16))
    return "".join(o)

def logo_mark(d, accent="#1B3EE8", flash="#F5C518", size=128):
    """Basket glyph — works as favicon, app icon and header mark."""
    s = size / 128
    o = [f'<g transform="scale({s})">',
         f'<rect width="128" height="128" rx="28" fill="{accent}"/>',
         # handle
         f'<path d="M44,48 C44,30 84,30 84,48" stroke="{flash}" stroke-width="9" fill="none" stroke-linecap="round"/>',
         # basket body
         f'<path d="M26,54 L102,54 L92,100 C91,105 87,108 82,108 L46,108 C41,108 37,105 36,100 Z" fill="#FFFFFF"/>',
         f'<path d="M26,54 L102,54 L100,64 L28,64 Z" fill="{flash}"/>']
    for x in (52, 64, 76):
        o.append(f'<path d="M{x},70 L{x - 2},100" stroke="{accent}" stroke-width="5" opacity=".28" stroke-linecap="round"/>')
    o.append("</g>")
    return "".join(o)

# ------------------------------------------------------------------ agency showcase
def showcase(d, accent="#1B3EE8", flash="#F5C518"):
    """Browser frame with an abstract storefront inside — used on the agency site."""
    o = []
    # laptop-ish browser window
    o.append(f'<rect x="60" y="70" width="1080" height="640" rx="14" fill="#FFFFFF" '
             f'stroke="#D9DFE6" stroke-width="2"/>')
    o.append(f'<rect x="60" y="70" width="1080" height="46" rx="14" fill="#F1F3F6"/>')
    o.append(f'<rect x="60" y="102" width="1080" height="14" fill="#F1F3F6"/>')
    for i, c in enumerate(["#E06C5B", "#E8B84B", "#5CB37E"]):
        o.append(f'<circle cx="{92 + i * 22}" cy="93" r="6.5" fill="{c}"/>')
    o.append(f'<rect x="176" y="82" width="420" height="22" rx="11" fill="#FFFFFF" stroke="#E3E7EC"/>')
    o.append(f'<rect x="192" y="90" width="150" height="6" rx="3" fill="#C3CBD4"/>')
    # dark hero band
    o.append(f'<rect x="60" y="116" width="1080" height="250" fill="#0A1A2F"/>')
    o.append(f'<rect x="106" y="150" width="120" height="18" rx="4" fill="{flash}"/>')
    o.append(f'<rect x="106" y="190" width="420" height="26" rx="5" fill="#FFFFFF" opacity=".92"/>')
    o.append(f'<rect x="106" y="228" width="300" height="26" rx="5" fill="{flash}"/>')
    o.append(f'<rect x="106" y="278" width="470" height="8" rx="4" fill="#8FA3B8" opacity=".7"/>')
    o.append(f'<rect x="106" y="294" width="380" height="8" rx="4" fill="#8FA3B8" opacity=".5"/>')
    o.append(f'<rect x="106" y="322" width="140" height="30" rx="5" fill="{flash}"/>')
    o.append(f'<rect x="258" y="322" width="140" height="30" rx="5" fill="none" stroke="#FFFFFF" stroke-width="2" opacity=".6"/>')
    # bag artwork inside the hero
    o.append(f'<g transform="translate(640,116) scale(.30)">{grocery_bag(d, accent, flash)}</g>')
    # product grid below
    for col in range(5):
        x = 106 + col * 202
        o.append(f'<rect x="{x}" y="400" width="180" height="250" rx="6" fill="#FFFFFF" stroke="#E3E7EC" stroke-width="2"/>')
        o.append(f'<rect x="{x + 1}" y="401" width="178" height="126" rx="5" fill="#F6F8FA"/>')
        o.append(f'<rect x="{x + 14}" y="542" width="120" height="9" rx="4.5" fill="#C3CBD4"/>')
        o.append(f'<rect x="{x + 14}" y="560" width="90" height="7" rx="3.5" fill="#DCE2E8"/>')
        # the shelf-edge label, the product's signature
        o.append(f'<rect x="{x + 14}" y="580" width="152" height="30" rx="2" fill="#FFFFFF" stroke="#0A1A2F" stroke-width="2"/>')
        o.append(f'<rect x="{x + 22}" y="588" width="52" height="12" rx="2" fill="#0A1A2F"/>')
        o.append(f'<rect x="{x + 14}" y="620" width="152" height="20" rx="3" fill="#0A1A2F"/>')
    # a couple of real product tiles dropped into the grid
    for i, (fn, tint) in enumerate([(P.tomato, "#C4453C"), (P.pineapple, "#D2A234"),
                                    (F.white_loaf, "#D6BC8E"), (K.rice, "#DAD3BC"), (P.avocado, "#7C9A4E")]):
        o.append(f'<g transform="translate({107 + i * 202},401) scale(.2225)">{fn(d, tint)}</g>')
    return "".join(o)

def devices(d, accent="#1B3EE8", flash="#F5C518"):
    """Laptop plus phone — 'it works on both' in one picture."""
    o = []
    # laptop
    o.append(f'<rect x="70" y="90" width="700" height="430" rx="12" fill="#0A1A2F"/>')
    o.append(f'<rect x="84" y="104" width="672" height="392" rx="6" fill="#FFFFFF"/>')
    o.append(f'<rect x="84" y="104" width="672" height="120" fill="#0A1A2F"/>')
    o.append(f'<rect x="110" y="132" width="90" height="14" rx="4" fill="{flash}"/>')
    o.append(f'<rect x="110" y="158" width="250" height="20" rx="5" fill="#FFFFFF" opacity=".9"/>')
    o.append(f'<rect x="110" y="186" width="170" height="20" rx="5" fill="{flash}"/>')
    for col in range(4):
        x = 110 + col * 158
        o.append(f'<rect x="{x}" y="248" width="136" height="212" rx="6" fill="#F6F8FA" stroke="#E3E7EC" stroke-width="2"/>')
        o.append(f'<rect x="{x + 12}" y="384" width="90" height="8" rx="4" fill="#C3CBD4"/>')
        o.append(f'<rect x="{x + 12}" y="402" width="112" height="24" rx="2" fill="#FFF" stroke="#0A1A2F" stroke-width="2"/>')
        o.append(f'<rect x="{x + 12}" y="434" width="112" height="16" rx="3" fill="#0A1A2F"/>')
    for i, (fn, tint) in enumerate([(P.tomato, "#C4453C"), (K.cooking_oil, "#D7B646"),
                                    (F.eggs, "#D6BE94"), (P.carrot, "#CE7A32")]):
        o.append(f'<g transform="translate({111 + i * 158},249) scale(.1675)">{fn(d, tint)}</g>')
    o.append(f'<path d="M40,520 L800,520 L772,556 L68,556 Z" fill="#1E2A33"/>')
    o.append(f'<rect x="358" y="528" width="124" height="8" rx="4" fill="#3A4956"/>')
    # phone
    o.append(f'<rect x="640" y="230" width="230" height="410" rx="30" fill="#0A1A2F"/>')
    o.append(f'<rect x="652" y="242" width="206" height="386" rx="22" fill="#FFFFFF"/>')
    o.append(f'<rect x="652" y="242" width="206" height="96" rx="22" fill="{accent}"/>')
    o.append(f'<rect x="652" y="316" width="206" height="22" fill="{accent}"/>')
    o.append(f'<rect x="700" y="252" width="110" height="8" rx="4" fill="#FFFFFF" opacity=".6"/>')
    o.append(f'<rect x="670" y="276" width="170" height="30" rx="6" fill="#FFFFFF" opacity=".92"/>')
    for row in range(2):
        for col in range(2):
            x, y = 670 + col * 92, 356 + row * 130
            o.append(f'<rect x="{x}" y="{y}" width="80" height="118" rx="6" fill="#F6F8FA" stroke="#E3E7EC" stroke-width="2"/>')
            o.append(f'<rect x="{x + 8}" y="{y + 78}" width="52" height="7" rx="3.5" fill="#C3CBD4"/>')
            o.append(f'<rect x="{x + 8}" y="{y + 92}" width="64" height="16" rx="2" fill="#FFF" stroke="#0A1A2F" stroke-width="1.6"/>')
    for i, (fn, tint) in enumerate([(P.matooke, "#8FA85A"), (F.milk_pouch, "#DDE4EC"),
                                    (P.mango, "#D08A2E"), (K.tissue, "#D2D2CB")]):
        x, y = 671 + (i % 2) * 92, 357 + (i // 2) * 130
        o.append(f'<g transform="translate({x},{y}) scale(.0975)">{fn(d, tint)}</g>')
    o.append(f'<rect x="722" y="612" width="66" height="6" rx="3" fill="#0A1A2F" opacity=".3"/>')
    return "".join(o)
