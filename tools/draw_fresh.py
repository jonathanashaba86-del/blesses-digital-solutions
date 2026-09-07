"""Butchery, fish, dairy and bakery illustrations."""
from svgkit import *

# ------------------------------------------------------------------ butchery
def _marbling(cx, cy, rx, ry, color, seed=3, n=9):
    o, s = [], seed * 3313
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648; fx = (s / 2147483648) * 2 - 1
        s = (s * 1103515245 + 12345) % 2147483648; fy = (s / 2147483648) * 2 - 1
        x, y = cx + fx * rx * .62, cy + fy * ry * .58
        o.append(f'<path d="M{x - 16},{y} q16,-11 32,-2 q-14,10 -32,2 Z" fill="{color}" opacity=".72" '
                 f'transform="rotate({fx * 44:.0f} {x} {y})"/>')
    return "".join(o)

def beef(d, t):
    """Trimmed boneless steaks — flat slabs with a fat cap along one edge."""
    o = [ground(d, 400, 468, 215, 32)]
    for cx, cy, w, h, rot in [(324, 356, 300, 176, -12), (462, 440, 316, 184, 8)]:
        g = d.sphere(t, cx="34%", cy="26%", hi=.40, lo=.36)
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="M{cx - w * .5},{cy - h * .10} C{cx - w * .48},{cy - h * .46} {cx - w * .22},{cy - h * .58} '
                 f'{cx + w * .06},{cy - h * .54} C{cx + w * .38},{cy - h * .50} {cx + w * .52},{cy - h * .22} '
                 f'{cx + w * .50},{cy + h * .06} C{cx + w * .48},{cy + h * .38} {cx + w * .24},{cy + h * .54} '
                 f'{cx - w * .10},{cy + h * .52} C{cx - w * .40},{cy + h * .50} {cx - w * .52},{cy + h * .24} '
                 f'{cx - w * .5},{cy - h * .10} Z" fill="url(#{g})"/>')
        # creamy fat cap hugging the top edge
        o.append(f'<path d="M{cx - w * .50},{cy - h * .12} C{cx - w * .48},{cy - h * .46} {cx - w * .22},{cy - h * .58} '
                 f'{cx + w * .06},{cy - h * .54} C{cx + w * .38},{cy - h * .50} {cx + w * .52},{cy - h * .22} '
                 f'{cx + w * .50},{cy + h * .06} L{cx + w * .40},{cy + h * .04} '
                 f'C{cx + w * .42},{cy - h * .20} {cx + w * .30},{cy - h * .40} {cx + w * .04},{cy - h * .44} '
                 f'C{cx - w * .20},{cy - h * .47} {cx - w * .40},{cy - h * .36} {cx - w * .40},{cy - h * .12} Z" '
                 f'fill="{lighten(t, .66)}"/>')
        o.append(_marbling(cx - w * .02, cy + h * .08, w * .38, h * .34, lighten(t, .50), int(cx), 12))
        o.append(f'<ellipse cx="{cx - w * .16}" cy="{cy - h * .18}" rx="{w * .18}" ry="{h * .14}" fill="#fff" opacity=".13"/>')
        o.append("</g>")
    return "".join(o)

def goat(d, t):
    """Bone-in pieces, cut to size — cubed chunks with bone showing at an edge."""
    o = [ground(d, 400, 472, 205, 32)]
    chunks = [(300, 386, 104, -14, 1), (508, 378, 96, 16, 0), (400, 448, 116, -3, 1), (398, 316, 84, 8, 0)]
    for cx, cy, s, rot, has_bone in chunks:
        g = d.linear3(darken(t, .28), lighten(t, .16), darken(t, .34), x1="0", y1="0", x2="1", y2="1")
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="M{cx - s * .9},{cy - s * .5} q{s * .3},{-s * .34} {s * .9},{-s * .22} '
                 f'q{s * .8},{s * .1} {s * .9},{s * .5} q{s * .1},{s * .5} {-s * .5},{s * .74} '
                 f'q{-s * .7},{s * .24} {-s * 1.2},{-s * .1} q{-s * .4},{-s * .32} {-s * .1},{-s * .92} Z" fill="url(#{g})"/>')
        o.append(_marbling(cx, cy, s * .7, s * .5, lighten(t, .46), int(cx + cy), 6))
        if has_bone:
            bx, by = cx + s * .52, cy + s * .12
            o.append(f'<ellipse cx="{bx}" cy="{by}" rx="{s * .22}" ry="{s * .19}" fill="{lighten(t, .74)}"/>'
                     f'<ellipse cx="{bx}" cy="{by}" rx="{s * .11}" ry="{s * .09}" fill="{mix(t, "#E8D2BE", .55)}"/>')
        o.append(f'<ellipse cx="{cx - s * .3}" cy="{cy - s * .32}" rx="{s * .3}" ry="{s * .18}" fill="#fff" opacity=".16"/>')
        o.append("</g>")
    return "".join(o)

def pork(d, t):
    """Belly / mixed cut with clear fat striping."""
    o = [ground(d, 400, 474, 205, 32)]
    for cx, cy, w, h, rot in [(300, 372, 250, 118, -10), (500, 448, 262, 122, 6)]:
        g = d.linear(lighten(t, .26), darken(t, .28))
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h * .38}" fill="url(#{g})"/>')
        for k in range(3):
            o.append(f'<rect x="{cx - w / 2 + 12}" y="{cy - h / 2 + 16 + k * 30}" width="{w - 24}" height="12" rx="6" '
                     f'fill="{lighten(t, .62)}" opacity=".92"/>')
        o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h * .3}" rx="{h * .2}" fill="#fff" opacity=".12"/>')
        o.append("</g>")
    return "".join(o)

def chicken(d, t):
    """Roast-ready bird — broad breast with both drumsticks sitting up over the front."""
    o = [ground(d, 400, 486, 190, 30)]
    skin = mix(t, "#E8BE7E", .42)
    g = d.sphere(skin, cx="34%", cy="20%", hi=.52, lo=.34)
    # wings behind
    for k in (-1, 1):
        o.append(f'<ellipse cx="{400 + k * 156}" cy="392" rx="54" ry="38" fill="{darken(skin, .22)}" '
                 f'transform="rotate({k * -24} {400 + k * 156} 392)"/>')
    # body
    o.append(f'<path d="M400,272 C512,272 578,330 578,400 C578,462 508,498 400,498 C292,498 222,462 222,400 '
             f'C222,330 288,272 400,272 Z" fill="url(#{g})"/>')
    o.append(f'<path d="M400,286 C424,344 424,428 400,482" stroke="{darken(skin, .24)}" stroke-width="5" fill="none" opacity=".40"/>')
    o.append(f'<ellipse cx="320" cy="332" rx="64" ry="32" fill="#fff" opacity=".30" transform="rotate(-16 320 332)"/>')
    o.append(f'<ellipse cx="486" cy="446" rx="70" ry="32" fill="{darken(skin, .18)}" opacity=".30" transform="rotate(-10 486 446)"/>')
    # drumsticks ON TOP of the body, splayed up and out
    for k in (-1, 1):
        hx, hy = 400 + k * 96, 330
        o.append(f'<g transform="rotate({k * 34} {hx} {hy})">'
                 f'<path d="M{hx - 40},{hy + 96} C{hx - 56},{hy + 20} {hx - 32},{hy - 40} {hx},{hy - 46} '
                 f'C{hx + 32},{hy - 40} {hx + 56},{hy + 20} {hx + 40},{hy + 96} '
                 f'C{hx + 18},{hy + 112} {hx - 18},{hy + 112} {hx - 40},{hy + 96} Z" fill="{lighten(skin, .06)}"/>'
                 f'<path d="M{hx - 34},{hy + 70} C{hx - 44},{hy + 16} {hx - 26},{hy - 26} {hx - 4},{hy - 34}" '
                 f'stroke="#fff" stroke-width="10" fill="none" opacity=".28" stroke-linecap="round"/>'
                 # exposed bone knuckle
                 f'<ellipse cx="{hx}" cy="{hy - 44}" rx="27" ry="21" fill="#F4E7D2"/>'
                 f'<ellipse cx="{hx}" cy="{hy - 48}" rx="19" ry="14" fill="#FBF3E5"/>'
                 f'<path d="M{hx - 11},{hy - 62} q11,-18 22,0 q-11,9 -22,0 Z" fill="#EFE0C6"/></g>')
    # trussing string across the breast
    o.append(f'<path d="M316,452 q84,28 168,0" stroke="#F6EBD6" stroke-width="5" fill="none" opacity=".85"/>')
    return "".join(o)

def fish_fillet(d, t):
    """Two thin perch fillets — long tapered slabs, one dark lateral line, no segments."""
    o = [ground(d, 400, 468, 220, 30)]
    flesh = mix(t, "#F8E3DA", .48)
    for cx, cy, rot in [(388, 348, -7), (412, 428, 5)]:
        g = d.linear3(lighten(flesh, .34), flesh, darken(flesh, .22), x1="0", y1="0", x2="0", y2="1")
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="M{cx - 214},{cy - 22} C{cx - 150},{cy - 40} {cx - 20},{cy - 42} {cx + 108},{cy - 24} '
                 f'C{cx + 180},{cy - 14} {cx + 216},{cy - 2} {cx + 212},{cy + 6} '
                 f'C{cx + 208},{cy + 16} {cx + 140},{cy + 28} {cx + 10},{cy + 32} '
                 f'C{cx - 108},{cy + 36} {cx - 190},{cy + 30} {cx - 212},{cy + 20} '
                 f'C{cx - 220},{cy + 14} {cx - 220},{cy - 14} {cx - 214},{cy - 22} Z" fill="url(#{g})"/>'
                 # single lateral line, the way a fillet actually looks
                 f'<path d="M{cx - 196},{cy - 2} C{cx - 100},{cy - 12} {cx + 40},{cy - 6} {cx + 186},{cy + 4}" '
                 f'stroke="{darken(flesh, .20)}" stroke-width="3.4" fill="none" opacity=".55"/>'
                 # soft flesh sheen
                 f'<path d="M{cx - 186},{cy - 14} C{cx - 96},{cy - 30} {cx + 40},{cy - 28} {cx + 150},{cy - 10}" '
                 f'stroke="#fff" stroke-width="12" fill="none" opacity=".42"/>'
                 # silver skin, bottom edge only
                 f'<path d="M{cx - 212},{cy + 20} C{cx - 190},{cy + 30} {cx - 108},{cy + 36} {cx + 10},{cy + 32} '
                 f'C{cx + 140},{cy + 28} {cx + 208},{cy + 16} {cx + 212},{cy + 6} '
                 f'L{cx + 210},{cy + 15} C{cx + 204},{cy + 26} {cx + 138},{cy + 38} {cx + 10},{cy + 42} '
                 f'C{cx - 110},{cy + 46} {cx - 192},{cy + 40} {cx - 212},{cy + 30} Z" fill="{mix(t, "#A6B4B9", .74)}"/>'
                 # squared-off cut end at the thick side
                 f'<path d="M{cx - 214},{cy - 22} C{cx - 220},{cy - 14} {cx - 220},{cy + 14} {cx - 212},{cy + 20} '
                 f'L{cx - 194},{cy + 22} C{cx - 202},{cy + 12} {cx - 202},{cy - 12} {cx - 196},{cy - 22} Z" '
                 f'fill="{lighten(flesh, .46)}"/></g>')
    return "".join(o)

def whole_fish(d, t):
    """Gutted and scaled tilapia."""
    o = [ground(d, 400, 482, 215, 30)]
    g = d.linear3(lighten(t, .30), darken(t, .10), darken(t, .34), x1="0", y1="0", x2="0", y2="1")
    o.append(f'<path d="M188,388 C250,296 360,268 452,286 C548,304 606,352 620,388 '
             f'C606,424 548,472 452,490 C360,508 250,480 188,388 Z" fill="url(#{g})"/>')
    # tail
    o.append(f'<path d="M188,388 L104,318 C120,368 120,408 104,458 Z" fill="{darken(t, .24)}"/>')
    # fins
    o.append(f'<path d="M340,284 L376,220 L436,286 Z" fill="{darken(t, .18)}"/>')
    o.append(f'<path d="M340,492 L378,548 L436,490 Z" fill="{darken(t, .18)}"/>')
    # gill + eye
    o.append(f'<path d="M556,318 C528,360 528,414 556,458" stroke="{darken(t, .30)}" stroke-width="5" fill="none" opacity=".6"/>')
    o.append(f'<circle cx="580" cy="372" r="17" fill="#F4F2EC"/><circle cx="580" cy="372" r="9" fill="#20262B"/>')
    o.append(f'<circle cx="584" cy="367" r="3.4" fill="#fff"/>')
    # scales
    for row in range(4):
        for col in range(9):
            x, y = 250 + col * 36 + (18 if row % 2 else 0), 330 + row * 32
            o.append(f'<path d="M{x - 15},{y} a15,15 0 0 1 30,0" fill="none" stroke="{lighten(t, .40)}" '
                     f'stroke-width="2.2" opacity=".42"/>')
    o.append(f'<path d="M230,342 C300,300 400,290 470,300" stroke="#fff" stroke-width="12" fill="none" opacity=".22"/>')
    return "".join(o)

def small_fish(d, t):
    """Mukene — dense heap of dried silver fish, contained inside the basket."""
    o = [ground(d, 400, 476, 215, 34)]
    basket = "#B9925C"
    o.append(f'<path d="M204,372 L596,372 L560,474 Q400,512 240,474 Z" fill="{darken(basket, .16)}"/>')
    for k in range(5):
        y = 388 + k * 19
        o.append(f'<path d="M{212 + k * 7},{y} L{588 - k * 7},{y}" stroke="{darken(basket, .30)}" stroke-width="2.5" opacity=".45"/>')
    clip = d.uid()
    d.items.append(f'<clipPath id="{clip}"><path d="M206,346 L594,346 L566,452 Q400,486 234,452 Z"/></clipPath>')
    silver = mix(t, "#D2D4CC", .62)
    o.append(f'<g clip-path="url(#{clip})">')
    s = 7717
    for i in range(240):
        s = (s * 1103515245 + 12345) % 2147483648; fx = (s / 2147483648) * 2 - 1
        s = (s * 1103515245 + 12345) % 2147483648; fy = (s / 2147483648) * 2 - 1
        x, y = 400 + fx * 180, 386 + fy * 48
        c = mix(silver, "#FFFFFF" if fy < 0 else "#87856F", abs(fy) * .40)
        o.append(f'<g transform="rotate({fx * 22:.0f} {x:.0f} {y:.0f})">'
                 f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="14" ry="3.4" fill="{c}"/>'
                 f'<path d="M{x + 13:.0f},{y:.0f} l8,-4 v8 Z" fill="{darken(c, .24)}"/>'
                 f'<circle cx="{x - 9:.0f}" cy="{y - .5:.0f}" r="1.4" fill="{darken(c, .48)}"/></g>')
    o.append("</g>")
    o.append(f'<path d="M204,372 Q400,344 596,372 Q400,404 204,372 Z" fill="{lighten(basket, .36)}" opacity=".45"/>')
    return "".join(o)

def milk_pouch(d, t):
    """Gable-top carton — unmistakably milk, and the label always fits."""
    o = [ground(d, 400, 488, 165, 26)]
    body = mix(t, "#FFFFFF", .5)
    g = d.linear3(darken(body, .14), "#FFFFFF", darken(body, .20), x1="0", y1="0", x2="1", y2="0")
    # gable roof
    o.append(f'<path d="M302,232 L400,182 L498,232 L498,262 L302,262 Z" fill="{darken(body, .12)}"/>')
    o.append(f'<path d="M302,232 L400,182 L400,262 L302,262 Z" fill="{lighten(body, .40)}"/>')
    o.append(f'<rect x="386" y="176" width="28" height="26" rx="6" fill="#1B3EE8"/>')
    # body
    o.append(f'<rect x="302" y="258" width="196" height="230" rx="8" fill="url(#{g})"/>')
    o.append(label_block(d, 400, 306, 196, 92, [
        ("FRESH", 27, "#FFFFFF", 800, 6), ("WHOLE MILK", 14, "#C3D0FF", 600, 0)],
        bg="#1B3EE8", r=0, op=.95))
    o.append(text(400, 442, "1 LITRE", 18, darken(body, .58), 700, 2.6, max_w=170))
    o.append(f'<path d="M348,418 q52,-14 104,0" stroke="{darken(body, .18)}" stroke-width="3" fill="none" opacity=".6"/>')
    o.append(f'<rect x="314" y="266" width="20" height="214" rx="10" fill="#fff" opacity=".55"/>')
    return "".join(o)

def yoghurt(d, t):
    """Tapered tub with a coloured lid."""
    o = [ground(d, 400, 486, 150, 26)]
    tub = mix(t, "#FFFFFF", .72)
    g = d.linear3(darken(tub, .16), "#FFFFFF", darken(tub, .22), x1="0", y1="0", x2="1", y2="0")
    o.append(f'<path d="M290,268 L510,268 L484,470 A118,26 0 0 1 316,470 Z" fill="url(#{g})"/>')
    o.append(label_block(d, 400, 320, 180, 104, [
        ("YOGHURT", 25, "#7C4A2E", 800, 5), ("PLAIN · SET", 13, "#A6866E", 600, 5),
        ("500 ml", 14, "#7C4A2E", 700, 0)], r=6, op=.96, border=darken(t, .24)))
    # lid
    lid = mix(t, "#C0432F", .62)
    o.append(f'<ellipse cx="400" cy="268" rx="112" ry="28" fill="{lighten(lid, .18)}"/>')
    o.append(f'<ellipse cx="400" cy="262" rx="112" ry="28" fill="{lid}"/>')
    o.append(f'<ellipse cx="400" cy="262" rx="88" ry="20" fill="{darken(lid, .14)}"/>')
    o.append(f'<path d="M312,286 q10,104 6,176" stroke="#fff" stroke-width="14" fill="none" opacity=".5"/>')
    return "".join(o)

def butter(d, t):
    o = [ground(d, 400, 452, 180, 28)]
    o.append(rbox(d, 246, 296, 308, 148, 12, lighten(t, .26), top_face=34))
    o.append(label_block(d, 400, 336, 224, 82, [
        ("BUTTER", 30, "#8A6A1E", 800, 5), ("SALTED · 250g", 15, "#B39448", 600, 0)], r=6, op=.92))
    o.append(f'<rect x="246" y="296" width="308" height="16" rx="8" fill="#fff" opacity=".4"/>')
    return "".join(o)

def eggs(d, t):
    """Open tray of 30."""
    o = [ground(d, 400, 486, 220, 30)]
    tray = darken(t, .30)
    o.append(f'<path d="M168,318 L632,318 L610,470 Q400,500 190,470 Z" fill="{tray}"/>')
    o.append(f'<path d="M168,318 L632,318 L624,346 L176,346 Z" fill="{lighten(tray, .24)}"/>')
    for row in range(3):
        for col in range(6):
            cx = 218 + col * 73 + (row % 2) * 12
            cy = 330 + row * 52
            o.append(f'<ellipse cx="{cx}" cy="{cy + 12}" rx="30" ry="20" fill="{darken(tray, .30)}" opacity=".5"/>')
            o.append(sphere(d, cx, cy, 31, lighten(t, .34), squash=1.16, hi=.52, lo=.22))
    o.append(f'<path d="M168,318 L632,318 L610,470 Q400,500 190,470 Z" fill="none" stroke="{darken(tray, .24)}" stroke-width="3"/>')
    return "".join(o)

def cheese(d, t):
    o = [ground(d, 400, 470, 180, 28)]
    # wedge
    g = d.linear(lighten(t, .34), darken(t, .18))
    o.append(f'<path d="M212,432 L212,336 L540,286 L588,392 L560,442 Z" fill="url(#{g})"/>')
    o.append(f'<path d="M212,336 L540,286 L588,392 L252,430 Z" fill="{lighten(t, .46)}" opacity=".55"/>')
    o.append(f'<path d="M540,286 L588,392 L560,442 L522,352 Z" fill="{darken(t, .30)}"/>')
    for cx, cy, r in [(300, 372, 13), (368, 352, 9), (432, 380, 15), (492, 344, 8)]:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * .82}" fill="{darken(t, .26)}" opacity=".5"/>')
    o.append(label_block(d, 333, 388, 190, 44, [("CHEDDAR", 21, "#FFFFFF", 800, 0)],
        bg="#B3261E", r=6, op=.95))
    return "".join(o)

# ------------------------------------------------------------------ bakery
def loaf(d, t, brown=False):
    """Tin loaf with two cut slices leaning against it."""
    o = [ground(d, 400, 480, 210, 30)]
    crust = darken(t, .34 if brown else .18)
    crumb = lighten(t, .34 if brown else .58)
    g = d.linear3(darken(crust, .18), lighten(crust, .24), darken(crust, .26), x1="0", y1="0", x2="1", y2="0")
    # loaf body
    o.append(f'<path d="M232,462 L232,344 C232,286 296,252 412,252 C528,252 588,286 588,344 L588,462 '
             f'C588,476 578,482 560,482 L260,482 C242,482 232,476 232,462 Z" fill="url(#{g})"/>')
    # domed, glazed top
    o.append(f'<path d="M232,348 C232,288 296,252 412,252 C528,252 588,288 588,348 C500,312 320,312 232,348 Z" '
             f'fill="{lighten(crust, .22)}"/>')
    for k in range(4):
        x = 282 + k * 84
        o.append(f'<path d="M{x},304 q26,-24 56,-8" stroke="{darken(crust, .36)}" stroke-width="7" fill="none" '
                 f'opacity=".5" stroke-linecap="round"/>')
    o.append(f'<path d="M320,272 C400,260 500,266 556,290" stroke="#fff" stroke-width="10" fill="none" opacity=".26"/>')
    # two slices leaning in front, showing the crumb
    for i, (sx, sy, rot) in enumerate([(268, 400, -9), (196, 414, -17)]):
        o.append(f'<g transform="rotate({rot} {sx} {sy})">'
                 f'<path d="M{sx - 74},{sy + 78} L{sx - 74},{sy - 24} C{sx - 74},{sy - 66} {sx - 40},{sy - 86} '
                 f'{sx},{sy - 86} C{sx + 40},{sy - 86} {sx + 74},{sy - 66} {sx + 74},{sy - 24} L{sx + 74},{sy + 78} Z" '
                 f'fill="{crust}"/>'
                 f'<path d="M{sx - 62},{sy + 70} L{sx - 62},{sy - 22} C{sx - 62},{sy - 58} {sx - 34},{sy - 74} '
                 f'{sx},{sy - 74} C{sx + 34},{sy - 74} {sx + 62},{sy - 58} {sx + 62},{sy - 22} L{sx + 62},{sy + 70} Z" '
                 f'fill="{crumb}"/>')
        s = 4211 + i * 733
        for k in range(14):
            s = (s * 1103515245 + 12345) % 2147483648; fx = (s / 2147483648)
            s = (s * 1103515245 + 12345) % 2147483648; fy = (s / 2147483648)
            o.append(f'<circle cx="{sx - 54 + fx * 108:.0f}" cy="{sy - 62 + fy * 126:.0f}" r="{2.4 + fx * 3.6:.1f}" '
                     f'fill="{darken(crumb, .16)}" opacity=".45"/>')
        o.append("</g>")
    return "".join(o)

def white_loaf(d, t): return loaf(d, t, False)
def brown_loaf(d, t): return loaf(d, t, True)

def chapati(d, t):
    """A stack of soft chapati, lightly blistered."""
    o = [ground(d, 400, 470, 220, 30)]
    for i, (cx, cy, rot) in enumerate([(400, 430, 3), (392, 396, -7), (406, 362, 9), (396, 330, -4), (400, 300, 6)]):
        c = mix(t, "#EBD3A4", (i % 2) * .18)
        g = d.sphere(c, cx="36%", cy="30%", hi=.34, lo=.22)
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="204" ry="42" fill="url(#{g})"/>'
                 f'<ellipse cx="{cx}" cy="{cy - 4}" rx="204" ry="40" fill="{lighten(c, .18)}" opacity=".5"/>')
        for k in range(6):
            s = 1000 + i * 97 + k * 53
            fx = ((s * 1103515245 + 12345) % 997) / 997 * 2 - 1
            o.append(f'<ellipse cx="{cx + fx * 150:.0f}" cy="{cy + fx * 9 - 4:.0f}" rx="{13 + k * 2}" ry="5.5" '
                     f'fill="{darken(c, .26)}" opacity=".30"/>')
        o.append("</g>")
    o.append(f'<ellipse cx="330" cy="288" rx="86" ry="16" fill="#fff" opacity=".30"/>')
    return "".join(o)

def mandazi(d, t):
    """Puffed triangular mandazi, fried golden."""
    o = [ground(d, 400, 478, 200, 30)]
    for cx, cy, s, rot in [(292, 392, 96, -16), (512, 386, 90, 18), (400, 446, 108, -4), (400, 314, 82, 6)]:
        c = mix(t, "#D9A martial", 0) if False else t
        g = d.sphere(c, cx="34%", cy="26%", hi=.46, lo=.30)
        # rounded triangle with puffed sides
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<path d="M{cx},{cy - s * .82} '
                 f'C{cx + s * .40},{cy - s * .72} {cx + s * .96},{cy + s * .14} {cx + s * .86},{cy + s * .48} '
                 f'C{cx + s * .74},{cy + s * .86} {cx - s * .74},{cy + s * .86} {cx - s * .86},{cy + s * .48} '
                 f'C{cx - s * .96},{cy + s * .14} {cx - s * .40},{cy - s * .72} {cx},{cy - s * .82} Z" fill="url(#{g})"/>'
                 # puffed centre
                 f'<path d="M{cx},{cy - s * .52} C{cx + s * .34},{cy - s * .40} {cx + s * .58},{cy + s * .16} '
                 f'{cx + s * .48},{cy + s * .40} C{cx + s * .30},{cy + s * .62} {cx - s * .30},{cy + s * .62} '
                 f'{cx - s * .48},{cy + s * .40} C{cx - s * .58},{cy + s * .16} {cx - s * .34},{cy - s * .40} '
                 f'{cx},{cy - s * .52} Z" fill="{lighten(c, .22)}" opacity=".7"/>'
                 f'<path d="M{cx - s * .70},{cy + s * .34} q{s * .70},{s * .22} {s * 1.40},0" '
                 f'stroke="{darken(c, .30)}" stroke-width="4" fill="none" opacity=".40"/>'
                 f'<ellipse cx="{cx - s * .26}" cy="{cy - s * .22}" rx="{s * .24}" ry="{s * .14}" fill="#fff" opacity=".30" '
                 f'transform="rotate(-22 {cx - s * .26} {cy - s * .22})"/></g>')
    return "".join(o)

