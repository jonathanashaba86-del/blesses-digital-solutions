"""
svgkit — small vector primitive library used to draw the RetailCore product art.

Everything here returns SVG fragment strings plus the <defs> they depend on, so a
product illustration is just a composition of primitives over a studio backdrop.
Light source is fixed top-left across every drawing, which is what keeps a shelf
of 60 different illustrations looking like one photoshoot.
"""
import math

# ---------------------------------------------------------------- colour utils
def _clamp(v): return max(0, min(255, int(round(v))))

def _hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _rgb2hex(t):
    return "#%02X%02X%02X" % tuple(_clamp(c) for c in t)

def lighten(h, amt):
    r, g, b = _hex2rgb(h)
    return _rgb2hex((r + (255 - r) * amt, g + (255 - g) * amt, b + (255 - b) * amt))

def darken(h, amt):
    r, g, b = _hex2rgb(h)
    return _rgb2hex((r * (1 - amt), g * (1 - amt), b * (1 - amt)))

def mix(a, b, t):
    ra, ga, ba = _hex2rgb(a)
    rb, gb, bb = _hex2rgb(b)
    return _rgb2hex((ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t))

def saturate(h, amt):
    """Push a colour away from its own grey — keeps produce looking fresh."""
    r, g, b = _hex2rgb(h)
    grey = 0.299 * r + 0.587 * g + 0.114 * b
    return _rgb2hex((grey + (r - grey) * (1 + amt),
                     grey + (g - grey) * (1 + amt),
                     grey + (b - grey) * (1 + amt)))

# ---------------------------------------------------------------- defs builder
class Defs:
    """Collects gradient/filter definitions and hands out unique ids."""
    def __init__(self, prefix="d"):
        self.items, self.prefix, self._n = [], prefix, 0

    def uid(self):
        self._n += 1
        return "%s%d" % (self.prefix, self._n)

    def sphere(self, color, cx="32%", cy="26%", r="78%", hi=0.62, lo=0.42):
        gid = self.uid()
        self.items.append(
            f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="{lighten(color, hi)}"/>'
            f'<stop offset=".46" stop-color="{color}"/>'
            f'<stop offset="1" stop-color="{darken(color, lo)}"/></radialGradient>')
        return gid

    def linear(self, c1, c2, x1="0", y1="0", x2="0", y2="1"):
        gid = self.uid()
        self.items.append(
            f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')
        return gid

    def linear3(self, c1, c2, c3, x1="0", y1="0", x2="1", y2="0"):
        gid = self.uid()
        self.items.append(
            f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/>'
            f'<stop offset=".5" stop-color="{c2}"/>'
            f'<stop offset="1" stop-color="{c3}"/></linearGradient>')
        return gid

    def soft_shadow(self, blur=18, dy=12, op=0.22):
        gid = self.uid()
        self.items.append(
            f'<filter id="{gid}" x="-30%" y="-30%" width="160%" height="170%">'
            f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="#0A1A2F" flood-opacity="{op}"/>'
            f'</filter>')
        return gid

    def blur(self, amount=10):
        gid = self.uid()
        self.items.append(
            f'<filter id="{gid}" x="-40%" y="-40%" width="180%" height="180%">'
            f'<feGaussianBlur stdDeviation="{amount}"/></filter>')
        return gid

    def render(self):
        return "<defs>%s</defs>" % "".join(self.items)

# ---------------------------------------------------------------- primitives
def sphere(d, cx, cy, r, color, squash=1.0, tilt=0, hi=0.62, lo=0.42, stroke=None):
    """A volumetric ball — the workhorse for fruit, veg and anything round."""
    gid = d.sphere(color, hi=hi, lo=lo)
    ry = r * squash
    tr = f' transform="rotate({tilt} {cx} {cy})"' if tilt else ""
    sk = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    spec_r = r * 0.26
    return (f'<g{tr}><ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="url(#{gid})"{sk}/>'
            f'<ellipse cx="{cx - r * .34}" cy="{cy - ry * .40}" rx="{spec_r}" ry="{spec_r * .68}" '
            f'fill="#fff" opacity=".34" transform="rotate(-24 {cx - r * .34} {cy - ry * .40})"/></g>')

def ground(d, cx, cy, rx, ry=None, op=0.20):
    """Contact shadow. Every subject sits on one so nothing floats."""
    ry = ry if ry is not None else rx * 0.20
    bl = d.blur(rx * 0.10)
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#22303C" '
            f'opacity="{op}" filter="url(#{bl})"/>')

def rbox(d, x, y, w, h, r, color, top_face=0, side=0.16):
    """Rounded pack. top_face>0 draws a lid so boxes read three-dimensional."""
    g = d.linear3(darken(color, .16), lighten(color, .10), darken(color, .26))
    out = []
    if top_face:
        tg = d.linear(lighten(color, .30), lighten(color, .12))
        out.append(f'<path d="M{x + r},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} '
                   f'L{x + w},{y + top_face} L{x},{y + top_face} L{x},{y + r} Q{x},{y} {x + r},{y} Z" fill="url(#{tg})"/>')
        y += top_face
        h -= top_face
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{g})"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w * side}" height="{h}" rx="{r}" fill="#fff" opacity=".14"/>')
    out.append(f'<rect x="{x + w * (1 - side)}" y="{y}" width="{w * side}" height="{h}" rx="{r}" fill="#000" opacity=".10"/>')
    return "".join(out)

def cylinder(d, cx, top, w, h, color, cap_h=None, cap_color=None):
    """Bottles, jars, tins, cups."""
    cap_h = cap_h if cap_h is not None else w * 0.16
    rx = w / 2
    body = d.linear3(darken(color, .22), lighten(color, .16), darken(color, .30))
    cap_c = cap_color or lighten(color, .22)
    return (f'<path d="M{cx - rx},{top} L{cx - rx},{top + h} A{rx},{cap_h} 0 0 0 {cx + rx},{top + h} '
            f'L{cx + rx},{top} Z" fill="url(#{body})"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{cap_h}" fill="{cap_c}"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{rx * .74}" ry="{cap_h * .70}" fill="{darken(cap_c, .16)}"/>')

def leaf(d, cx, cy, length, width, angle, color, curl=0.42):
    """One leaf blade; bunches are just many of these fanned out."""
    g = d.linear(lighten(color, .34), darken(color, .26))
    tipx, tipy = cx, cy - length
    c1x, c1y = cx - width, cy - length * curl
    c2x, c2y = cx + width, cy - length * curl
    return (f'<g transform="rotate({angle} {cx} {cy})">'
            f'<path d="M{cx},{cy} Q{c1x},{c1y} {tipx},{tipy} Q{c2x},{c2y} {cx},{cy} Z" fill="url(#{g})"/>'
            f'<path d="M{cx},{cy} L{tipx},{tipy}" stroke="{lighten(color, .40)}" '
            f'stroke-width="{max(1.6, width * .10)}" opacity=".55" fill="none"/></g>')

def stem(cx, cy, dx, dy, color, w=9):
    return (f'<path d="M{cx},{cy} Q{cx + dx * .3},{cy + dy * .8} {cx + dx},{cy + dy}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none"/>')

def label(d, x, y, w, h, color="#FFFFFF", r=6, op=0.94):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}" opacity="{op}"/>'

def band(x, y, w, h, color, op=1.0, r=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}" opacity="{op}"/>'

def esc(s):
    """XML-escape label copy — an unescaped & is the classic way to break an SVG."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def est_width(s, size, spacing=0.5, weight=700):
    """Rough Arial advance width. Good enough to stop a label overflowing its box."""
    per = 0.60 if weight >= 700 else 0.55
    wide = sum(0.30 if c in " .,:;'|!" else 0.86 if c in "MW" else 0.62 if c.isupper() else 0.52 for c in s)
    return wide * size * (per / 0.58) + max(0, len(s) - 1) * spacing

def text(x, y, s, size=22, color="#0A1A2F", weight=700, anchor="middle", spacing=0.5,
         family="Arial, Helvetica, sans-serif", max_w=None):
    """max_w shrinks the type until it fits — packaging copy never spills off the label."""
    s = str(s)
    if max_w:
        while size > 7 and est_width(s, size, spacing, weight) > max_w:
            size -= 0.5
            if spacing > 0.4:
                spacing = max(0.4, spacing * 0.94)
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size:g}" font-weight="{weight}" '
            f'letter-spacing="{spacing:g}" fill="{color}" text-anchor="{anchor}">{esc(s)}</text>')

def label_block(d, cx, y, w, h, lines, bg="#FFFFFF", r=8, op=0.95, border=None, pad=14):
    """White label panel with auto-fitted lines. lines = [(copy, size, colour, weight, gap)]."""
    o = [f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{bg}" opacity="{op}"/>']
    if border:
        o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" '
                 f'stroke="{border}" stroke-width="2.5"/>')
    inner = w - pad * 2
    total = sum(l[1] * 1.02 + (l[4] if len(l) > 4 else 6) for l in lines)
    cy = y + (h - total) / 2
    for ln in lines:
        copy, size, color = ln[0], ln[1], ln[2]
        weight = ln[3] if len(ln) > 3 else 700
        gap = ln[4] if len(ln) > 4 else 6
        if copy == "|rule|":
            cy += gap * .5
            o.append(f'<rect x="{cx - inner * .34}" y="{cy}" width="{inner * .68}" height="3" fill="{color}"/>')
            cy += 3 + gap
            continue
        cy += size
        o.append(text(cx, cy, copy, size, color, weight, "middle",
                      0.5 if size < 18 else 2.2, max_w=inner))
        cy += gap
    return "".join(o)

def scatter(d, cx, cy, count, r, color, spread_x, spread_y, seed=1, squash=0.82, vary=0.22):
    """Deterministic pseudo-random pile — beans, nuts, small fish, charcoal."""
    out = []
    s = seed * 9781 + 1
    items = []
    for i in range(count):
        s = (s * 1103515245 + 12345) % 2147483648
        fx = (s / 2147483648) * 2 - 1
        s = (s * 1103515245 + 12345) % 2147483648
        fy = (s / 2147483648) * 2 - 1
        s = (s * 1103515245 + 12345) % 2147483648
        fr = (s / 2147483648)
        x = cx + fx * spread_x
        y = cy + fy * spread_y
        rr = r * (1 - vary + fr * vary * 2)
        items.append((y, x, rr, fx))
    for y, x, rr, fx in sorted(items):
        c = mix(color, "#FFFFFF" if fx > 0 else "#000000", abs(fx) * 0.10)
        out.append(sphere(d, round(x, 1), round(y, 1), round(rr, 1), c, squash=squash, tilt=fx * 20, hi=.50, lo=.34))
    return "".join(out)

# ---------------------------------------------------------------- canvas
def canvas(inner, defs, w=800, h=600, tint="#8FA85A", pad_bg=True, title=""):
    """Studio backdrop + subject. Same lighting recipe on every tile."""
    d = defs
    bg = d.uid()
    wash = lighten(tint, 0.90)
    wash2 = lighten(tint, 0.72)
    defs.items.insert(0,
        f'<radialGradient id="{bg}" cx="34%" cy="22%" r="86%">'
        f'<stop offset="0" stop-color="#FFFFFF"/>'
        f'<stop offset=".55" stop-color="{wash}"/>'
        f'<stop offset="1" stop-color="{wash2}"/></radialGradient>')
    back = f'<rect width="{w}" height="{h}" fill="url(#{bg}"/>' if False else \
           f'<rect width="{w}" height="{h}" fill="url(#{bg})"/>'
    t = f'<title>{esc(title)}</title>' if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}">{t}{d.render()}{back if pad_bg else ""}{inner}</svg>')
