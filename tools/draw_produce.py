"""Fresh produce illustrations."""
from svgkit import *

def matooke(d, t):
    """A hand of green cooking bananas — curved fingers fanned off one stalk."""
    o = [ground(d, 400, 486, 215, 32)]
    fingers = [(-46, 250, 372, 1.00), (-30, 292, 404, 1.08), (-14, 338, 426, 1.14),
               (2, 400, 434, 1.16), (18, 462, 426, 1.14), (34, 508, 404, 1.08), (50, 550, 372, 1.00)]
    for i, (ang, cx, cy, sc) in enumerate(fingers):
        c = mix(t, "#A8C468", (i % 3) * .14)
        g = d.linear3(darken(c, .34), lighten(c, .22), darken(c, .30), x1="0", y1="0", x2="1", y2="0")
        L = 210 * sc
        o.append(f'<g transform="rotate({ang} {cx} {cy}) translate({cx} {cy}) scale({sc})">'
                 # crescent banana: outer curve down-left, inner curve back
                 f'<path d="M0,64 C-52,20 -60,-70 -22,-{L*.62:.0f} C-14,-{L*.70:.0f} 2,-{L*.72:.0f} 10,-{L*.66:.0f} '
                 f'C24,-{L*.56:.0f} 22,-40 34,10 C42,44 30,72 12,76 C4,78 -2,74 0,64 Z" fill="url(#{g})"/>'
                 # ridge highlight
                 f'<path d="M-16,52 C-44,10 -46,-58 -18,-{L*.56:.0f}" stroke="{lighten(c, .46)}" stroke-width="8" '
                 f'fill="none" opacity=".45" stroke-linecap="round"/>'
                 # dark tip
                 f'<path d="M-22,-{L*.62:.0f} C-14,-{L*.70:.0f} 2,-{L*.72:.0f} 10,-{L*.66:.0f} L6,-{L*.60:.0f} '
                 f'C0,-{L*.64:.0f} -12,-{L*.62:.0f} -22,-{L*.62:.0f} Z" fill="{darken(c, .48)}"/>'
                 f'</g>')
    # cut stalk holding the hand together
    st = d.linear(lighten("#7C6A3E", .26), darken("#7C6A3E", .24))
    o.append(f'<path d="M352,430 Q400,414 448,430 L436,506 Q400,524 364,506 Z" fill="url(#{st})"/>')
    o.append(f'<ellipse cx="400" cy="430" rx="48" ry="15" fill="{lighten("#9A8552", .30)}"/>')
    o.append(f'<ellipse cx="400" cy="430" rx="30" ry="9" fill="{darken("#9A8552", .18)}" opacity=".7"/>')
    return "".join(o)

def _tuber(d, cx, cy, rx, ry, color, tilt, eyes=3, seed=2):
    g = d.sphere(color, hi=.46, lo=.40)
    o = [f'<g transform="rotate({tilt} {cx} {cy})">'
         f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{g})"/>']
    s = seed * 7717
    for i in range(eyes):
        s = (s * 1103515245 + 12345) % 2147483648
        fx = (s / 2147483648) * 2 - 1
        s = (s * 1103515245 + 12345) % 2147483648
        fy = (s / 2147483648) * 2 - 1
        o.append(f'<ellipse cx="{cx + fx * rx * .5}" cy="{cy + fy * ry * .5}" rx="{rx * .07}" ry="{rx * .05}" '
                 f'fill="{darken(color, .34)}" opacity=".7"/>')
    o.append(f'<ellipse cx="{cx - rx * .32}" cy="{cy - ry * .40}" rx="{rx * .26}" ry="{ry * .20}" fill="#fff" opacity=".26"/>')
    o.append("</g>")
    return "".join(o)

def sweet_potato(d, t):
    o = [ground(d, 400, 470, 220, 34)]
    o.append(_tuber(d, 300, 400, 140, 62, darken(t, .06), -16, 4, 3))
    o.append(_tuber(d, 500, 392, 132, 58, lighten(t, .10), 12, 4, 7))
    o.append(_tuber(d, 400, 452, 168, 66, t, -4, 5, 11))
    return "".join(o)

def irish_potato(d, t):
    o = [ground(d, 400, 472, 215, 32)]
    o.append(_tuber(d, 300, 396, 116, 92, darken(t, .05), -12, 5, 4))
    o.append(_tuber(d, 506, 388, 108, 86, lighten(t, .08), 14, 5, 8))
    o.append(_tuber(d, 400, 450, 140, 108, t, -3, 6, 12))
    return "".join(o)

def tomato(d, t):
    o = [ground(d, 400, 476, 205, 30)]
    for cx, cy, r in [(288, 400, 104), (512, 394, 96), (400, 442, 126)]:
        o.append(sphere(d, cx, cy, r, t, squash=.90, hi=.58, lo=.44))
        # calyx
        for a in range(0, 360, 72):
            o.append(f'<g transform="rotate({a} {cx} {cy - r * .82})">'
                     f'<path d="M{cx},{cy - r * .82} q-8,-26 0,-40 q8,14 0,40 Z" fill="#3E7A3A"/></g>')
        o.append(f'<circle cx="{cx}" cy="{cy - r * .84}" r="{r * .10}" fill="#2F6330"/>')
    return "".join(o)

def onion(d, t):
    """Red onions — papery purple skin, dried neck, fine root tuft."""
    o = [ground(d, 400, 480, 205, 32)]
    for cx, cy, r, sd in [(288, 400, 100, 1), (512, 394, 94, 2), (400, 446, 124, 3)]:
        g = d.sphere(t, cx="32%", cy="24%", hi=.50, lo=.44)
        # onion silhouette: round body pinched to a neck
        o.append(f'<path d="M{cx},{cy - r * .98} C{cx + r * .62},{cy - r * .92} {cx + r * 1.04},{cy - r * .34} '
                 f'{cx + r},{cy + r * .18} C{cx + r * .96},{cy + r * .76} {cx + r * .52},{cy + r},{cx},{cy + r} '
                 f'C{cx - r * .52},{cy + r} {cx - r * .96},{cy + r * .76} {cx - r},{cy + r * .18} '
                 f'C{cx - r * 1.04},{cy - r * .34} {cx - r * .62},{cy - r * .92} {cx},{cy - r * .98} Z" fill="url(#{g})"/>')
        # papery vertical striping
        for k in (-2, -1, 0, 1, 2):
            o.append(f'<path d="M{cx + k * r * .16},{cy - r * .94} C{cx + k * r * .40},{cy - r * .2} '
                     f'{cx + k * r * .44},{cy + r * .3} {cx + k * r * .22},{cy + r * .96}" '
                     f'stroke="{darken(t, .30)}" stroke-width="2.6" fill="none" opacity=".38"/>')
        o.append(f'<ellipse cx="{cx - r * .36}" cy="{cy - r * .34}" rx="{r * .26}" ry="{r * .20}" fill="#fff" '
                 f'opacity=".28" transform="rotate(-22 {cx - r * .36} {cy - r * .34})"/>')
        # dried neck
        o.append(f'<path d="M{cx - 11},{cy - r * .96} Q{cx},{cy - r * 1.34} {cx + 11},{cy - r * .96} '
                 f'Q{cx},{cy - r * .84} {cx - 11},{cy - r * .96} Z" fill="{darken(t, .46)}"/>')
        # roots
        for a in (-16, 0, 16):
            o.append(f'<path d="M{cx + a * .6},{cy + r * .96} q{a * .3},18 {a * .5},26" stroke="{lighten(t, .52)}" '
                     f'stroke-width="2.4" fill="none" opacity=".75" stroke-linecap="round"/>')
    return "".join(o)

def greens(d, t):
    o = [ground(d, 400, 486, 190, 28)]
    for i, ang in enumerate(range(-58, 59, 13)):
        c = mix(t, "#79A860", (i % 3) * .16)
        o.append(leaf(d, 400, 470, 250 + (i % 3) * 26, 88, ang, c, curl=.5))
    # tie
    o.append(f'<path d="M336,452 q64,26 128,0 q6,26 -6,34 q-58,20 -116,0 q-12,-8 -6,-34 Z" fill="#B0855A"/>')
    o.append(f'<path d="M336,462 q64,24 128,0" stroke="{darken("#B0855A", .28)}" stroke-width="4" fill="none"/>')
    return "".join(o)

def avocado(d, t):
    o = [ground(d, 400, 478, 190, 30)]
    # whole
    g = d.sphere(darken(t, .18), hi=.42, lo=.44)
    o.append(f'<path d="M292,300 C348,272 392,318 392,380 C392,448 348,486 300,486 C252,486 214,444 214,388 '
             f'C214,338 246,318 292,300 Z" fill="url(#{g})"/>')
    o.append(f'<ellipse cx="262" cy="360" rx="34" ry="46" fill="#fff" opacity=".16" transform="rotate(-18 262 360)"/>')
    o.append(stem(300, 300, 6, -34, "#6B5A3A", 12))
    # halved, with stone
    flesh = "#CBD97A"
    o.append(f'<path d="M508,296 C566,268 610,314 610,378 C610,448 566,486 518,486 C470,486 430,444 430,388 '
             f'C430,336 462,316 508,296 Z" fill="{darken(t, .30)}"/>')
    o.append(f'<path d="M508,312 C558,288 594,326 594,380 C594,440 556,472 518,472 C478,472 446,438 446,390 '
             f'C446,346 470,330 508,312 Z" fill="{flesh}"/>')
    o.append(f'<path d="M508,326 C550,306 580,336 580,382 C580,432 548,458 518,458 C486,458 460,430 460,390 '
             f'C460,354 478,342 508,326 Z" fill="{lighten(flesh, .22)}"/>')
    st = d.sphere("#8A6236", hi=.44, lo=.34)
    o.append(f'<ellipse cx="520" cy="392" rx="58" ry="62" fill="url(#{st})"/>')
    return "".join(o)

def passion_fruit(d, t):
    o = [ground(d, 400, 478, 200, 30)]
    for cx, cy, r in [(292, 404, 96), (516, 398, 88), (404, 444, 112)]:
        o.append(sphere(d, cx, cy, r, t, squash=.96, hi=.50, lo=.46))
        o.append(f'<ellipse cx="{cx - r * .3}" cy="{cy - r * .34}" rx="{r * .22}" ry="{r * .16}" fill="#fff" opacity=".22"/>')
    # cut half showing pulp
    o.append(f'<ellipse cx="404" cy="444" rx="112" ry="107" fill="{darken(t, .30)}" opacity="0"/>')
    return "".join(o)

def pineapple(d, t):
    """Golden body with a clipped diamond lattice and a proper spiky crown."""
    o = [ground(d, 400, 508, 165, 26)]
    gold = mix(t, "#E0A62E", .55)
    clip = d.uid()
    body_path = ("M400,182 C492,182 524,252 524,344 C524,438 478,504 400,504 "
                 "C322,504 276,438 276,344 C276,252 308,182 400,182 Z")
    d.items.append(f'<clipPath id="{clip}"><path d="{body_path}"/></clipPath>')
    body = d.linear3(darken(gold, .34), lighten(gold, .20), darken(gold, .40), x1="0", y1="0", x2="1", y2="0")
    # crown first, behind the body
    for i, ang in enumerate(range(-56, 57, 8)):
        c = mix("#3B7A44", "#79B160", (i % 4) * .26)
        o.append(leaf(d, 400, 214, 132 + (i % 4) * 30, 22, ang, c, curl=.34))
    o.append(f'<path d="{body_path}" fill="url(#{body})"/>')
    o.append(f'<g clip-path="url(#{clip})">')
    for row in range(11):
        y = 186 + row * 30
        for col in range(9):
            x = 250 + col * 34 + (17 if row % 2 else 0)
            o.append(f'<path d="M{x},{y - 15} L{x + 17},{y} L{x},{y + 15} L{x - 17},{y} Z" '
                     f'fill="none" stroke="{darken(gold, .42)}" stroke-width="2.6" opacity=".62"/>')
            o.append(f'<path d="M{x - 6},{y - 4} l12,8" stroke="{darken(gold, .50)}" stroke-width="3.4" '
                     f'opacity=".5" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="336" cy="286" rx="58" ry="96" fill="#fff" opacity=".16" transform="rotate(-16 336 286)"/>')
    o.append(f'<ellipse cx="500" cy="400" rx="52" ry="110" fill="#000" opacity=".10"/>')
    o.append("</g>")
    return "".join(o)

def mango(d, t):
    o = [ground(d, 400, 478, 195, 30)]
    for cx, cy, r, tilt in [(296, 402, 104, -18), (508, 396, 96, 14), (402, 446, 122, -4)]:
        g = d.sphere(t, hi=.56, lo=.40)
        o.append(f'<g transform="rotate({tilt} {cx} {cy})">'
                 f'<path d="M{cx - r},{cy} C{cx - r},{cy - r * .92} {cx + r * .2},{cy - r * .98} {cx + r * .72},{cy - r * .5} '
                 f'C{cx + r * 1.1},{cy - r * .06} {cx + r * .5},{cy + r * .86} {cx - r * .2},{cy + r * .82} '
                 f'C{cx - r * .78},{cy + r * .76} {cx - r},{cy + r * .4} {cx - r},{cy} Z" fill="url(#{g})"/>'
                 f'<ellipse cx="{cx - r * .30}" cy="{cy - r * .38}" rx="{r * .28}" ry="{r * .18}" fill="#fff" opacity=".30" '
                 f'transform="rotate(-22 {cx - r * .3} {cy - r * .38})"/>'
                 f'<ellipse cx="{cx + r * .34}" cy="{cy + r * .12}" rx="{r * .34}" ry="{r * .40}" fill="#C9422C" opacity=".26"/></g>')
    return "".join(o)

def cabbage(d, t):
    """Layered head — wrapper leaves behind and in front of a tight pale ball."""
    o = [ground(d, 400, 494, 195, 30)]
    outer = darken(t, .18)
    # wrapper leaves behind
    for cx, cy, rx, ry, rot in [(268, 384, 118, 96, -26), (534, 378, 112, 92, 24), (400, 262, 128, 84, 0)]:
        g = d.sphere(outer, hi=.34, lo=.34)
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{g})" transform="rotate({rot} {cx} {cy})"/>')
    # the head
    head = lighten(t, .30)
    g = d.sphere(head, cx="34%", cy="26%", hi=.44, lo=.36)
    o.append(f'<ellipse cx="400" cy="384" rx="172" ry="162" fill="url(#{g})"/>')
    # veins fanning from the core, not concentric rings
    for k in range(-4, 5):
        sx = 400 + k * 34
        o.append(f'<path d="M400,246 C{400 + k * 52},{330 + abs(k) * 8} {sx + k * 14},{420} {sx},{528}" '
                 f'stroke="{darken(head, .20)}" stroke-width="{4.5 - abs(k) * .35}" fill="none" opacity=".42"/>')
    for rx, ry, op in [(150, 140, .40), (104, 96, .34), (58, 52, .30)]:
        o.append(f'<ellipse cx="396" cy="378" rx="{rx}" ry="{ry}" fill="none" stroke="{lighten(head, .40)}" '
                 f'stroke-width="3" opacity="{op}"/>')
    o.append(f'<ellipse cx="352" cy="322" rx="62" ry="44" fill="#fff" opacity=".24" transform="rotate(-24 352 322)"/>')
    # wrapper leaves in front, ruffled edge
    for cx, cy, rx, ry, rot in [(276, 442, 116, 78, -18), (528, 436, 110, 74, 16)]:
        g2 = d.sphere(outer, hi=.40, lo=.30)
        o.append(f'<g transform="rotate({rot} {cx} {cy})">'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{g2})"/>'
                 f'<path d="M{cx - rx * .8},{cy} Q{cx},{cy - ry * .5} {cx + rx * .8},{cy}" stroke="{lighten(outer, .34)}" '
                 f'stroke-width="4" fill="none" opacity=".5"/></g>')
    return "".join(o)

def carrot(d, t):
    o = [ground(d, 400, 486, 200, 28)]
    for i, (cx, tilt) in enumerate([(292, -22), (400, -2), (508, 20)]):
        c = mix(t, "#E08A2E", (i % 2) * .2)
        g = d.linear3(darken(c, .26), lighten(c, .18), darken(c, .30), x1="0", y1="0", x2="1", y2="0")
        o.append(f'<g transform="rotate({tilt} {cx} 360)">'
                 f'<path d="M{cx - 46},250 Q{cx},232 {cx + 46},250 L{cx + 12},476 Q{cx},492 {cx - 12},476 Z" fill="url(#{g})"/>')
        for k in range(5):
            y = 280 + k * 38
            o.append(f'<path d="M{cx - 40 + k * 5},{y} q40,12 {80 - k * 10},0" stroke="{darken(c, .30)}" '
                     f'stroke-width="2.6" fill="none" opacity=".45"/>')
        for a in (-40, -14, 12, 38):
            o.append(leaf(d, cx, 248, 110, 26, a, "#4F8A44", curl=.5))
        o.append("</g>")
    return "".join(o)

def green_pepper(d, t):
    """Bell peppers — wide shoulders, three lobes at the base."""
    o = [ground(d, 400, 486, 200, 30)]
    for cx, cy, r, tilt in [(288, 396, 96, -10), (512, 392, 90, 11), (402, 448, 116, 0)]:
        g = d.sphere(t, cx="30%", cy="24%", hi=.52, lo=.44)
        o.append(f'<g transform="rotate({tilt} {cx} {cy})">'
                 f'<path d="M{cx},{cy - r * .94} '
                 f'C{cx + r * .78},{cy - r * .96} {cx + r * 1.06},{cy - r * .30} {cx + r * .98},{cy + r * .26} '
                 f'C{cx + r * .92},{cy + r * .74} {cx + r * .74},{cy + r * .98} {cx + r * .56},{cy + r * .92} '
                 f'C{cx + r * .40},{cy + r * .86} {cx + r * .34},{cy + r * 1.00} {cx + r * .18},{cy + r * 1.02} '
                 f'C{cx + r * .02},{cy + r * 1.04} {cx - r * .04},{cy + r * .88} {cx - r * .20},{cy + r * .96} '
                 f'C{cx - r * .40},{cy + r * 1.04} {cx - r * .62},{cy + r * .96} {cx - r * .80},{cy + r * .70} '
                 f'C{cx - r * 1.02},{cy + r * .34} {cx - r * 1.04},{cy - r * .40} {cx - r * .74},{cy - r * .86} '
                 f'C{cx - r * .48},{cy - r * 1.02} {cx - r * .22},{cy - r * .96} {cx},{cy - r * .94} Z" fill="url(#{g})"/>')
        for k in (-1, 1):
            o.append(f'<path d="M{cx + k * r * .48},{cy - r * .70} C{cx + k * r * .70},{cy - r * .1} '
                     f'{cx + k * r * .60},{cy + r * .44} {cx + k * r * .34},{cy + r * .90}" '
                     f'stroke="{darken(t, .32)}" stroke-width="3.2" fill="none" opacity=".45"/>')
        o.append(f'<ellipse cx="{cx - r * .42}" cy="{cy - r * .22}" rx="{r * .16}" ry="{r * .40}" fill="#fff" '
                 f'opacity=".28" transform="rotate(-10 {cx - r * .42} {cy - r * .22})"/>')
        o.append(stem(cx, cy - r * .88, 3, -40, "#3F7A3C", 14))
        o.append(f'<path d="M{cx - 30},{cy - r * .88} q30,-20 60,0 q-30,18 -60,0 Z" fill="#357036"/>')
        o.append("</g>")
    return "".join(o)


def citrus(d, t):
    """Oranges — one cut half showing segments."""
    o = [ground(d, 400, 478, 200, 30)]
    for cx, cy, r in [(300, 396, 104), (508, 388, 92)]:
        o.append(sphere(d, cx, cy, r, t, squash=.97, hi=.54, lo=.42))
        # dimpled peel
        s = int(cx) * 31
        for i in range(26):
            s = (s * 1103515245 + 12345) % 2147483648; fx = (s / 2147483648) * 2 - 1
            s = (s * 1103515245 + 12345) % 2147483648; fy = (s / 2147483648) * 2 - 1
            if fx * fx + fy * fy > .82: continue
            o.append(f'<circle cx="{cx + fx * r * .84:.0f}" cy="{cy + fy * r * .84:.0f}" r="2.6" '
                     f'fill="{darken(t, .26)}" opacity=".38"/>')
        o.append(f'<circle cx="{cx}" cy="{cy - r * .88}" r="{r * .11}" fill="{darken(t, .40)}"/>')
    # cut half
    cx, cy, r = 400, 452, 112
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{darken(t, .16)}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .90}" fill="{lighten(t, .62)}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .82}" fill="{lighten(t, .16)}"/>')
    import math
    for k in range(9):
        a0 = k * 40 + 4
        x1 = cx + r * .80 * math.cos(math.radians(a0)); y1 = cy + r * .80 * math.sin(math.radians(a0))
        x2 = cx + r * .80 * math.cos(math.radians(a0 + 32)); y2 = cy + r * .80 * math.sin(math.radians(a0 + 32))
        o.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r * .80},{r * .80} 0 0 1 {x2:.1f},{y2:.1f} Z" '
                 f'fill="{lighten(t, .34)}" stroke="{lighten(t, .70)}" stroke-width="3"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .10}" fill="{lighten(t, .72)}"/>')
    return "".join(o)

def watermelon(d, t):
    """Whole melon with a cut wedge."""
    o = [ground(d, 400, 480, 215, 30)]
    rind, flesh = mix(t, "#2F6B33", .7), "#E24A5A"
    g = d.sphere(rind, hi=.40, lo=.40)
    o.append(f'<ellipse cx="322" cy="378" rx="176" ry="146" fill="url(#{g})"/>')
    for k in range(-3, 4):
        o.append(f'<path d="M{322 + k * 40},{238} C{322 + k * 58},{318} {322 + k * 58},{438} {322 + k * 40},{518}" '
                 f'stroke="{darken(rind, .34)}" stroke-width="{13 - abs(k) * 2}" fill="none" opacity=".55"/>')
    o.append(f'<ellipse cx="262" cy="316" rx="62" ry="34" fill="#fff" opacity=".20" transform="rotate(-20 262 316)"/>')
    # wedge
    o.append(f'<path d="M470,470 L640,300 A230,230 0 0 1 660,470 Z" fill="{darken(rind, .20)}"/>')
    o.append(f'<path d="M482,462 L634,314 A210,210 0 0 1 650,462 Z" fill="{lighten(rind, .55)}"/>')
    o.append(f'<path d="M494,454 L630,326 A196,196 0 0 1 642,454 Z" fill="{flesh}"/>')
    for x, y in [(556, 396), (588, 372), (600, 424), (554, 436), (612, 400)]:
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="10" fill="#2B2118" transform="rotate(20 {x} {y})"/>')
    return "".join(o)
