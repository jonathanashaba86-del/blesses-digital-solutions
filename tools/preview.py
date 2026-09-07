import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Defs, canvas
import cairosvg

def sheet(pairs, out, cols=4, cw=400, ch=300):
    """pairs = [(name, draw_fn, tint)] -> one PNG contact sheet for visual QA."""
    rows = (len(pairs) + cols - 1) // cols
    W, H = cols * cw, rows * (ch + 26)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
             f'<rect width="{W}" height="{H}" fill="#EEF0F3"/>']
    for i, (name, fn, tint) in enumerate(pairs):
        r, c = divmod(i, cols)
        x, y = c * cw, r * (ch + 26)
        d = Defs(prefix="p%d_" % i)
        svg = canvas(fn(d, tint), d, tint=tint, title=name)
        body = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
        parts.append(f'<g transform="translate({x},{y}) scale({cw/800})">{body}</g>')
        parts.append(f'<text x="{x+10}" y="{y+ch+18}" font-family="Arial" font-size="15" fill="#111">{name}</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=out, output_width=W, output_height=H)
    print("wrote", out)
