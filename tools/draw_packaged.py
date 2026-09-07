"""Pantry, drinks and household — packaged goods."""
from svgkit import *

def _seam(x, y, w, h, color):
    return (f'<path d="M{x},{y} L{x + w},{y}" stroke="{color}" stroke-width="3" opacity=".35"/>'
            f'<path d="M{x},{y + h} L{x + w},{y + h}" stroke="{color}" stroke-width="3" opacity=".25"/>')

def _pillow_pack(d, cx, top, w, h, color, ear=26):
    """Sealed pillow pack — crimped top and bottom. Flour, sugar, rice, detergent."""
    g = d.linear3(darken(color, .22), lighten(color, .20), darken(color, .30), x1="0", y1="0", x2="1", y2="0")
    x, b = cx - w / 2, top + h
    o = [f'<path d="M{x},{top + ear} Q{cx},{top - ear * .5} {x + w},{top + ear} '
         f'L{x + w},{b - ear} Q{cx},{b + ear * .5} {x},{b - ear} Z" fill="url(#{g})"/>']
    # crimped seals
    for yy, sc in ((top + ear * .55, 1), (b - ear * .55, 1)):
        o.append(f'<rect x="{x - 10}" y="{yy - 13}" width="{w + 20}" height="26" rx="6" fill="{darken(color, .38)}"/>')
        for k in range(7):
            o.append(f'<rect x="{x + 4 + k * (w - 8) / 7}" y="{yy - 7}" width="3" height="14" rx="1.5" '
                     f'fill="{lighten(color, .34)}" opacity=".40"/>')
    o.append(f'<rect x="{x + w * .06}" y="{top + ear * 1.2}" width="{w * .13}" height="{h - ear * 2.4}" rx="{w * .06}" '
             f'fill="#fff" opacity=".26"/>')
    return "".join(o)

def maize_flour(d, t):
    o = [ground(d, 400, 492, 175, 26)]
    o.append(_pillow_pack(d, 400, 208, 268, 286, t))
    o.append(label_block(d, 400, 286, 208, 132, [
        ("MAIZE", 30, "#8A6A22", 800, 2), ("FLOUR", 30, "#8A6A22", 800, 8),
        ("|rule|", 0, "#D9A62E", 700, 10), ("FINE POSHO · 2 kg", 14, "#A08340", 600, 0)]))
    return "".join(o)

def rice(d, t):
    o = [ground(d, 400, 494, 180, 26)]
    o.append(_pillow_pack(d, 400, 198, 282, 300, t))
    o.append(label_block(d, 400, 274, 224, 150, [
        ("LONG GRAIN", 18, "#6E7A3A", 700, 6), ("RICE", 42, "#3F5A2A", 800, 8),
        ("|rule|", 0, "#8CA84E", 700, 10), ("5 kg", 22, "#6E7A3A", 700, 0)]))
    # a few grains scattered at the base
    for i, (x, y, r) in enumerate([(268, 486, 9), (300, 494, 8), (508, 488, 9), (540, 496, 7), (240, 496, 7)]):
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .40}" fill="{lighten(t, .60)}" '
                 f'transform="rotate({i * 34 - 40} {x} {y})"/>')
    return "".join(o)

def sugar(d, t):
    o = [ground(d, 400, 492, 172, 26)]
    o.append(_pillow_pack(d, 400, 214, 262, 278, t))
    o.append(label_block(d, 400, 292, 200, 122, [
        ("SUGAR", 34, "#3F6BA8", 800, 8), ("|rule|", 0, "#5B90CE", 700, 9),
        ("GRANULATED WHITE", 12, "#6E8FB6", 600, 6), ("2 kg", 18, "#3F6BA8", 700, 0)]))
    return "".join(o)

def gnut_paste(d, t):
    o = [ground(d, 400, 486, 150, 26)]
    o.append(cylinder(d, 400, 258, 224, 216, t, cap_h=28, cap_color=darken(t, .30)))
    # lid
    o.append(f'<ellipse cx="400" cy="252" rx="112" ry="28" fill="{darken(t, .40)}"/>')
    o.append(f'<rect x="288" y="228" width="224" height="30" rx="8" fill="{darken(t, .34)}"/>')
    o.append(label_block(d, 400, 306, 188, 116, [
        ("G-NUT", 26, "#6B4423", 800, 2), ("PASTE", 26, "#6B4423", 800, 8),
        ("500 ml · pure", 13, "#9A7A55", 600, 0)], bg="#F6EFE2", r=6, op=.97))
    o.append(f'<path d="M310,282 q8,96 4,164" stroke="#fff" stroke-width="14" fill="none" opacity=".28"/>')
    return "".join(o)

def cooking_oil(d, t):
    """3 litre jerrycan with a handle."""
    o = [ground(d, 400, 492, 170, 26)]
    g = d.linear3(darken(t, .24), lighten(t, .26), darken(t, .32), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M292,246 L508,246 C520,246 526,256 526,270 L526,464 C526,480 516,488 500,488 '
             f'L300,488 C284,488 274,480 274,464 L274,270 C274,256 280,246 292,246 Z" fill="url(#{g})"/>')
    # neck + cap
    o.append(f'<rect x="368" y="196" width="64" height="56" rx="8" fill="{darken(t, .18)}"/>')
    o.append(f'<rect x="356" y="176" width="88" height="34" rx="10" fill="#2B3440"/>')
    o.append(f'<rect x="356" y="176" width="88" height="12" rx="6" fill="#4A5764"/>')
    # handle
    o.append(f'<path d="M436,214 q74,6 74,64 q0,58 -74,64" fill="none" stroke="{darken(t, .26)}" stroke-width="22" stroke-linecap="round"/>')
    o.append(f'<path d="M436,214 q74,6 74,64 q0,58 -74,64" fill="none" stroke="{lighten(t, .28)}" stroke-width="10" stroke-linecap="round" opacity=".55"/>')
    o.append(label_block(d, 388, 306, 176, 140, [
        ("PURE", 20, "#B08A12", 700, 4), ("OIL", 40, "#8A6A0E", 800, 8),
        ("|rule|", 0, "#DCB534", 700, 10), ("3 LITRES", 15, "#B08A12", 700, 0)], op=.94))
    o.append(f'<rect x="288" y="262" width="20" height="212" rx="10" fill="#fff" opacity=".35"/>')
    return "".join(o)

def beans(d, t):
    """Loose dry beans heaped in a bowl."""
    o = [ground(d, 400, 480, 200, 30)]
    bowl = "#B7BCC4"
    o.append(f'<path d="M212,364 L588,364 C588,452 508,492 400,492 C292,492 212,452 212,364 Z" fill="{darken(bowl, .16)}"/>')
    clip = d.uid()
    d.items.append(f'<clipPath id="{clip}"><path d="M216,296 L584,296 L584,368 L216,368 Z"/></clipPath>')
    o.append(f'<g clip-path="url(#{clip})">')
    o.append(scatter(d, 400, 358, 74, 21, t, 178, 34, seed=4, squash=.66, vary=.16))
    o.append("</g>")
    o.append(scatter(d, 400, 342, 46, 21, t, 168, 20, seed=9, squash=.66, vary=.16))
    o.append(f'<ellipse cx="400" cy="364" rx="188" ry="30" fill="none" stroke="{lighten(bowl, .30)}" stroke-width="9"/>')
    o.append(f'<path d="M232,392 q30,74 118,90" stroke="#fff" stroke-width="12" fill="none" opacity=".22"/>')
    return "".join(o)

# ------------------------------------------------------------------ drinks
def coffee(d, t):
    """Foil coffee pack with a degassing valve, beans at the foot."""
    o = [ground(d, 400, 486, 172, 26)]
    o.append(_pillow_pack(d, 400, 200, 250, 282, t, ear=22))
    o.append(f'<circle cx="400" cy="252" r="19" fill="{darken(t, .44)}"/>')
    o.append(f'<circle cx="400" cy="252" r="9" fill="{lighten(t, .30)}"/>')
    o.append(label_block(d, 400, 292, 196, 132, [
        ("MT ELGON", 15, "#8A6A46", 700, 6), ("COFFEE", 32, "#4A2E1C", 800, 8),
        ("|rule|", 0, "#8A6A46", 700, 9), ("ARABICA · 250g", 12, "#8A6A46", 600, 0)],
        bg="#F4EDE2", op=.96))
    for i, (x, y, rot) in enumerate([(252, 484, -20), (286, 494, 14), (516, 486, 24), (548, 496, -12)]):
        c = darken(t, .18)
        o.append(f'<g transform="rotate({rot} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="15" ry="11" fill="{c}"/>'
                 f'<path d="M{x - 13},{y} q13,-7 26,0 q-13,7 -26,0 Z" fill="{darken(c, .34)}"/></g>')
    return "".join(o)

def tea(d, t):
    o = [ground(d, 400, 470, 168, 26)]
    o.append(rbox(d, 274, 226, 252, 246, 10, t, top_face=32))
    o.append(label_block(d, 400, 296, 200, 132, [
        ("FORT PORTAL", 13, "#8A6A22", 700, 6), ("TEA", 44, "#2F5A34", 800, 8),
        ("|rule|", 0, "#4E8A46", 700, 9), ("LOOSE BLACK · 250g", 11, "#7A8A5E", 600, 0)],
        bg="#FFF8E8", op=.95))
    o.append(leaf(d, 344, 300, 52, 18, -34, "#4E8A46", curl=.5))
    o.append(leaf(d, 456, 300, 52, 18, 34, "#4E8A46", curl=.5))
    return "".join(o)

def water(d, t):
    """5 litre bottle with a carry handle."""
    o = [ground(d, 400, 496, 165, 24)]
    g = d.linear3(darken(t, .16), "#FFFFFF", darken(t, .22), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M330,214 L470,214 C486,238 512,258 512,292 L512,458 C512,480 498,492 476,492 '
             f'L324,492 C302,492 288,480 288,458 L288,292 C288,258 314,238 330,214 Z" fill="url(#{g})"/>')
    o.append(f'<rect x="362" y="176" width="76" height="46" rx="6" fill="{darken(t, .12)}" opacity=".9"/>')
    o.append(f'<rect x="352" y="158" width="96" height="30" rx="8" fill="#1E6FB8"/>')
    o.append(f'<rect x="352" y="158" width="96" height="10" rx="5" fill="#4C97D8"/>')
    o.append(f'<path d="M470,236 q60,10 60,60 q0,50 -60,58" fill="none" stroke="{darken(t, .20)}" stroke-width="20" stroke-linecap="round" opacity=".85"/>')
    # ribbing
    for k in range(4):
        o.append(f'<rect x="296" y="{330 + k * 34}" width="208" height="9" rx="4.5" fill="{darken(t, .22)}" opacity=".35"/>')
    o.append(label_block(d, 400, 288, 168, 34, [("PURIFIED WATER", 13, "#FFFFFF", 700, 0)],
        bg="#1E6FB8", r=5, op=.95))
    o.append(text(400, 470, "5 LITRES", 15, "#2E7FC4", 700, 2.4, max_w=200))
    o.append(f'<rect x="304" y="256" width="22" height="216" rx="11" fill="#fff" opacity=".55"/>')
    return "".join(o)

def soda_crate(d, t):
    """Crate of 24 bottles, seen from the front."""
    o = [ground(d, 400, 492, 210, 28)]
    crate = darken(t, .30)
    # bottles poking above the crate
    for col in range(6):
        cx = 226 + col * 70
        cap = ["#C0392B", "#E67E22", "#2E7D32", "#8E44AD", "#1B6CA8", "#C0392B"][col]
        o.append(f'<rect x="{cx - 18}" y="266" width="36" height="86" rx="10" fill="{lighten(cap, .30)}" opacity=".9"/>')
        o.append(f'<path d="M{cx - 18},290 q18,-30 36,0 Z" fill="{lighten(cap, .45)}" opacity=".8"/>')
        o.append(f'<rect x="{cx - 10}" y="248" width="20" height="30" rx="5" fill="{lighten(cap, .18)}"/>')
        o.append(f'<rect x="{cx - 13}" y="240" width="26" height="16" rx="4" fill="{cap}"/>')
        o.append(f'<rect x="{cx - 14}" y="300" width="28" height="34" rx="4" fill="#FFFFFF" opacity=".85"/>')
    # crate body
    o.append(f'<rect x="196" y="330" width="408" height="158" rx="12" fill="{crate}"/>')
    o.append(f'<rect x="196" y="330" width="408" height="26" rx="10" fill="{lighten(crate, .26)}"/>')
    for col in range(1, 6):
        o.append(f'<rect x="{196 + col * 68 - 3}" y="356" width="6" height="132" fill="{darken(crate, .26)}" opacity=".7"/>')
    o.append(f'<rect x="210" y="376" width="380" height="8" rx="4" fill="{darken(crate, .3)}" opacity=".5"/>')
    o.append(label_block(d, 400, 396, 176, 60, [
        ("CRATE OF 24", 15, darken(crate, .45), 800, 5),
        ("300 ml mixed", 11, darken(crate, .25), 600, 0)], r=6, op=.94))
    return "".join(o)

# ------------------------------------------------------------------ household
def detergent(d, t):
    o = [ground(d, 400, 490, 176, 26)]
    o.append(_pillow_pack(d, 400, 206, 274, 288, t))
    o.append(label_block(d, 400, 288, 208, 136, [
        ("WASHING", 16, "#1E5AA8", 700, 6), ("POWDER", 30, "#123E7C", 800, 8),
        ("|rule|", 0, "#3E86D8", 700, 9), ("MACHINE & HAND · 1 kg", 11, "#4A7CB8", 600, 0)]))
    # sparkle
    for cx, cy, r in [(320, 250, 15), (486, 262, 11), (352, 448, 10)]:
        o.append(f'<path d="M{cx},{cy - r} L{cx + r * .3},{cy - r * .3} L{cx + r},{cy} L{cx + r * .3},{cy + r * .3} '
                 f'L{cx},{cy + r} L{cx - r * .3},{cy + r * .3} L{cx - r},{cy} L{cx - r * .3},{cy - r * .3} Z" '
                 f'fill="#FFFFFF" opacity=".75"/>')
    return "".join(o)

def soap(d, t):
    """Stacked laundry bars."""
    o = [ground(d, 400, 470, 190, 28)]
    for i, (x, y, rot) in enumerate([(400, 414, 3), (386, 356, -6), (410, 300, 8)]):
        c = mix(t, "#D8E2C6", (i % 2) * .18)
        o.append(f'<g transform="rotate({rot} {x} {y})">')
        o.append(rbox(d, x - 148, y - 34, 296, 68, 12, c, top_face=16))
        o.append(f'<rect x="{x - 96}" y="{y - 12}" width="192" height="34" rx="6" fill="#FFFFFF" opacity=".9"/>')
        o.append(text(x, y + 13, "SOAP", 19, "#4A6B3A", 800, 3, max_w=170))
        o.append("</g>")
    return "".join(o)

def tissue(d, t):
    """Shrink-wrapped 10 roll pack."""
    o = [ground(d, 400, 486, 190, 28)]
    g = d.linear3(darken(t, .10), "#FFFFFF", darken(t, .16), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<rect x="228" y="240" width="344" height="250" rx="26" fill="url(#{g})" opacity=".92"/>')
    # rolls showing through the wrap
    for col in range(3):
        for row in range(2):
            cx, cy = 300 + col * 100, 306 + row * 116
            o.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="#FFFFFF" opacity=".85"/>')
            o.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{darken(t, .18)}" stroke-width="3" opacity=".5"/>')
            o.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{darken(t, .14)}" opacity=".55"/>')
    o.append(label_block(d, 400, 386, 264, 78, [
        ("SOFT TISSUE", 22, "#FFFFFF", 800, 7), ("2 PLY · 10 ROLLS", 13, "#BFE8DC", 600, 0)],
        bg="#2E8B72", op=.94))
    o.append(f'<rect x="248" y="252" width="26" height="222" rx="13" fill="#fff" opacity=".55"/>')
    return "".join(o)

def charcoal(d, t):
    """Full hardwood sack, tied at the neck."""
    o = [ground(d, 400, 494, 205, 28)]
    sack = mix(t, "#9A8A6E", .55)
    g = d.linear3(darken(sack, .26), lighten(sack, .18), darken(sack, .34), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M266,286 C240,352 232,430 244,472 C256,494 544,494 556,472 C568,430 560,352 534,286 Z" fill="url(#{g})"/>')
    # tied neck
    o.append(f'<path d="M300,300 C330,246 470,246 500,300 Z" fill="{darken(sack, .16)}"/>')
    o.append(f'<path d="M312,272 q88,-26 176,0" stroke="{darken(sack, .44)}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    # charcoal lumps spilling over the top
    o.append(scatter(d, 400, 250, 13, 28, "#3A3B3C", 92, 20, seed=6, squash=.78, vary=.28))
    o.append(f'<path d="M282,340 q120,-18 240,0" stroke="{lighten(sack, .26)}" stroke-width="4" fill="none" opacity=".5"/>')
    o.append(label_block(d, 400, 372, 190, 62, [
        ("HARDWOOD", 14, "#E8D8B8", 700, 5), ("CHARCOAL", 18, "#FFFFFF", 800, 0)],
        bg="#2B2C2D", r=6, op=.9))
    o.append(f'<path d="M282,330 q-14,90 -2,140" stroke="#fff" stroke-width="14" fill="none" opacity=".16"/>')
    return "".join(o)

# ------------------------------------------------------------------ generic packaging
# These cover the long tail of a supermarket catalogue. A shop adding a new SKU
# gets a clean, on-brand tile without anyone drawing anything.

def generic(kind, lines, accent=None):
    """Return a draw fn for a packaging archetype with copy on the label."""
    def draw(d, t):
        acc = accent or darken(t, .46)
        return _GENERIC[kind](d, t, lines, acc)
    return draw

def _g_pack(d, t, lines, acc):
    o = [ground(d, 400, 492, 176, 26)]
    o.append(_pillow_pack(d, 400, 206, 272, 288, t))
    o.append(label_block(d, 400, 288, 210, 136, lines))
    return "".join(o)

def _g_carton(d, t, lines, acc):
    o = [ground(d, 400, 476, 170, 26)]
    o.append(rbox(d, 272, 222, 256, 254, 10, t, top_face=32))
    o.append(label_block(d, 400, 292, 200, 136, lines))
    return "".join(o)

def _g_tall_carton(d, t, lines, acc):
    """Juice / long-life milk carton with a screw cap."""
    o = [ground(d, 400, 492, 150, 24)]
    g = d.linear3(darken(t, .20), lighten(t, .18), darken(t, .28), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<rect x="316" y="200" width="168" height="290" rx="8" fill="url(#{g})"/>')
    o.append(f'<path d="M316,200 L400,168 L484,200 Z" fill="{lighten(t, .30)}"/>')
    o.append(f'<rect x="378" y="150" width="44" height="34" rx="8" fill="{acc}"/>')
    o.append(label_block(d, 400, 262, 140, 150, lines))
    o.append(f'<rect x="326" y="212" width="18" height="266" rx="9" fill="#fff" opacity=".32"/>')
    return "".join(o)

def _g_bottle(d, t, lines, acc):
    o = [ground(d, 400, 494, 140, 24)]
    g = d.linear3(darken(t, .22), lighten(t, .24), darken(t, .30), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M356,208 L444,208 L444,246 C444,266 486,286 486,326 L486,462 '
             f'C486,482 472,492 452,492 L348,492 C328,492 314,482 314,462 L314,326 '
             f'C314,286 356,266 356,246 Z" fill="url(#{g})"/>')
    o.append(f'<rect x="352" y="176" width="96" height="40" rx="8" fill="{acc}"/>')
    o.append(f'<rect x="352" y="176" width="96" height="12" rx="6" fill="{lighten(acc, .34)}"/>')
    o.append(label_block(d, 400, 336, 156, 122, lines))
    o.append(f'<rect x="326" y="330" width="16" height="146" rx="8" fill="#fff" opacity=".38"/>')
    return "".join(o)

def _g_jar(d, t, lines, acc):
    o = [ground(d, 400, 486, 150, 26)]
    o.append(cylinder(d, 400, 268, 220, 208, t, cap_h=28, cap_color=lighten(t, .28)))
    o.append(f'<ellipse cx="400" cy="258" rx="110" ry="28" fill="{acc}"/>')
    o.append(f'<rect x="290" y="232" width="220" height="30" rx="8" fill="{acc}"/>')
    o.append(f'<rect x="290" y="232" width="220" height="9" rx="4" fill="{lighten(acc, .34)}"/>')
    o.append(label_block(d, 400, 312, 178, 118, lines))
    o.append(f'<path d="M312,292 q8,86 4,148" stroke="#fff" stroke-width="14" fill="none" opacity=".26"/>')
    return "".join(o)

def _g_can(d, t, lines, acc):
    o = [ground(d, 400, 480, 140, 24)]
    o.append(cylinder(d, 400, 268, 200, 202, t, cap_h=26, cap_color="#C9CED4"))
    o.append(f'<ellipse cx="400" cy="262" rx="100" ry="26" fill="#DCE1E6"/>')
    o.append(f'<ellipse cx="400" cy="262" rx="82" ry="19" fill="#C2C8CE"/>')
    o.append(f'<rect x="300" y="284" width="200" height="14" rx="4" fill="#C9CED4"/>')
    o.append(f'<rect x="300" y="440" width="200" height="14" rx="4" fill="#C9CED4"/>')
    o.append(label_block(d, 400, 306, 178, 126, lines))
    return "".join(o)

def _g_tube(d, t, lines, acc):
    o = [ground(d, 400, 486, 140, 24)]
    g = d.linear3(darken(t, .18), "#FFFFFF", darken(t, .24), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M344,236 L456,236 L456,452 C456,474 442,486 420,486 L380,486 '
             f'C358,486 344,474 344,452 Z" fill="url(#{g})"/>')
    o.append(f'<path d="M344,236 L456,236 L448,214 L352,214 Z" fill="{darken(t, .16)}"/>')
    o.append(f'<rect x="372" y="176" width="56" height="44" rx="8" fill="{acc}"/>')
    o.append(label_block(d, 400, 286, 104, 150, lines))
    o.append(f'<rect x="354" y="248" width="14" height="222" rx="7" fill="#fff" opacity=".42"/>')
    return "".join(o)

def _g_polybag(d, t, lines, acc):
    """Soft polybag — nappies, cotton wool, sanitary pads."""
    o = [ground(d, 400, 486, 190, 26)]
    g = d.linear3(darken(t, .18), lighten(t, .22), darken(t, .26), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M236,244 Q400,214 564,244 L554,462 Q400,496 246,462 Z" fill="url(#{g})"/>')
    o.append(f'<path d="M236,244 Q400,214 564,244 L562,282 Q400,254 238,282 Z" fill="{lighten(t, .34)}"/>')
    o.append(f'<rect x="352" y="222" width="96" height="24" rx="12" fill="{acc}" opacity=".9"/>')
    o.append(label_block(d, 400, 300, 236, 132, lines))
    o.append(f'<path d="M262,286 q-6,96 2,166" stroke="#fff" stroke-width="18" fill="none" opacity=".26"/>')
    return "".join(o)

def _g_tray(d, t, lines, acc):
    """Chilled tray — sausages, mince, cut meat."""
    o = [ground(d, 400, 476, 205, 28)]
    o.append(f'<path d="M186,300 L614,300 L582,462 Q400,492 218,462 Z" fill="#E7EAEE"/>')
    o.append(f'<path d="M186,300 L614,300 L606,330 L194,330 Z" fill="#F5F7F9"/>')
    clip = d.uid()
    d.items.append(f'<clipPath id="{clip}"><path d="M206,318 L594,318 L568,452 Q400,478 232,452 Z"/></clipPath>')
    o.append(f'<g clip-path="url(#{clip})">')
    for i in range(5):
        cy = 336 + i * 26
        o.append(f'<rect x="212" y="{cy}" width="376" height="22" rx="11" fill="{mix(t, "#FFFFFF", (i % 2) * .12)}"/>')
        o.append(f'<rect x="212" y="{cy}" width="376" height="7" rx="3.5" fill="#fff" opacity=".28"/>')
    o.append("</g>")
    # cling film sheen
    o.append(f'<path d="M228,330 L360,466" stroke="#fff" stroke-width="26" opacity=".28"/>')
    o.append(label_block(d, 400, 396, 208, 56, lines, op=.92))
    return "".join(o)

def _g_bar(d, t, lines, acc):
    """Wrapped bar — soap, chocolate, stock cubes."""
    o = [ground(d, 400, 456, 176, 26)]
    o.append(rbox(d, 244, 316, 312, 130, 12, t, top_face=22))
    o.append(label_block(d, 400, 352, 244, 82, lines))
    return "".join(o)

_GENERIC = {"pack": _g_pack, "carton": _g_carton, "tall": _g_tall_carton, "bottle": _g_bottle,
            "jar": _g_jar, "can": _g_can, "tube": _g_tube, "poly": _g_polybag,
            "tray": _g_tray, "bar": _g_bar}
