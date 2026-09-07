#!/usr/bin/env python3
"""Bundle the VoiceCore app into one self-contained HTML file.

The client site and the owner's dashboard end up on a single page with the
engine, widget and both page scripts inlined — no server, no network, no
relative paths. Email it, put it on a USB stick, open it on a laptop with no
signal: the receptionist still works.

    python3 tools/build_standalone.py [output.html]

Defaults to dist/voicecore-standalone.html
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "app" / "voicecore"


def js_safe(js):
    """A literal </script anywhere in inlined JS closes the element early."""
    return js.replace("</script", "<\\/script")


def body_of(html):
    return re.search(r"<body[^>]*>(.*?)</body>", html, re.S).group(1)


def style_of(html):
    return re.search(r"<style>(.*?)</style>", html, re.S).group(1)


def strip_scripts(html):
    return re.sub(r"<script.*?</script>", "", html, flags=re.S)


def last_inline_script(html):
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    return blocks[-1] if blocks else ""


def scope_css(css, scope):
    """Prefix every selector with `scope` so the dashboard's dark palette
    cannot leak into the client site sharing the page."""
    out, i, n = [], 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(css[i:j])
            i = j
            continue
        j = css.find("{", i)
        if j == -1:
            out.append(css[i:])
            break
        head = css[i:j]
        stripped = head.strip()
        depth, k = 0, j
        while k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        body = css[j + 1:k]
        if stripped.startswith("@keyframes") or stripped.startswith("@font-face"):
            out.append(head + "{" + body + "}")
        elif stripped.startswith("@"):
            out.append(head + "{" + scope_css(body, scope) + "}")
        else:
            sels = [scope if s.strip() == ":root" else scope + " " + s.strip()
                    for s in head.split(",") if s.strip()]
            out.append("\n" + ",\n".join(sels) + "{" + body + "}")
        i = k + 1
    return "".join(out)


INTRO = """
<section class="vc-intro" id="owner">
  <div class="vc-intro-inner">
    <p class="vc-intro-eyebrow">The other half of the product</p>
    <h2>What reception captured</h2>
    <p>Everything the receptionist just handled is below, in the owner's dashboard —
      tagged, transcribed and counted. Talk to her above, then watch this fill in.</p>
  </div>
</section>
"""

EXTRA_CSS = """
.vc-intro{background:#050b1a;color:#93a2bb;border-top:1px solid rgba(255,255,255,.12);
  padding:clamp(2.5rem,6vw,4rem) clamp(1.1rem,4vw,2rem) 0;}
.vc-intro-inner{max-width:1240px;margin-inline:auto;}
.vc-intro-eyebrow{font-family:'Jost',sans-serif;font-size:.72rem;letter-spacing:.26em;
  text-transform:uppercase;color:#c9a227;font-weight:600;margin-bottom:.6rem;}
.vc-intro h2{font-family:'Jost',sans-serif;font-weight:400;color:#fff;
  font-size:clamp(1.8rem,4vw,2.6rem);letter-spacing:-.02em;margin-bottom:.6rem;}
.vc-intro p{max-width:60ch;}
.vc-dash{display:block;background:#050b1a;padding-top:1.5rem;padding-bottom:1px;}
.vc-dash .top{border-radius:14px;margin-inline:clamp(1.1rem,4vw,2rem);
  border:1px solid rgba(255,255,255,.12);}
"""

BRIDGE = """
(function () {
  document.querySelectorAll('a[href="#owner"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      document.getElementById('owner').scrollIntoView({ behavior: 'smooth' });
    });
  });
  document.querySelectorAll('a[href="#top"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
})();
"""


def build():
    engine = (APP / "engine.js").read_text(encoding="utf-8")
    widget = (APP / "widget.js").read_text(encoding="utf-8")
    demo = (APP / "demo.html").read_text(encoding="utf-8")
    dash = (APP / "index.html").read_text(encoding="utf-8")

    demo_css = style_of(demo)
    # The client site's nav is sticky on its own page; here it would float
    # over the dashboard section below it.
    demo_css = demo_css.replace(
        ".nav{border-bottom:1px solid var(--line);position:sticky;top:0;"
        "background:rgba(255,255,255,.92);backdrop-filter:blur(10px);z-index:40;}",
        ".nav{border-bottom:1px solid var(--line);position:relative;background:#fff;z-index:4;}")

    dash_css = scope_css(style_of(dash), ".vc-dash").replace(
        "position:sticky;top:0;z-index:50;", "position:relative;z-index:5;")

    demo_markup = strip_scripts(body_of(demo)) \
        .replace('<a href="index.html" class="solid">Open the owner dashboard</a>',
                 '<a href="#owner" class="solid">Jump to the owner dashboard</a>') \
        .replace('<a href="../../products/voicecore.html">Read the brief</a>', "")

    dash_markup = strip_scripts(body_of(dash)) \
        .replace('<a class="btn sm" href="demo.html">Open the client demo</a>',
                 '<a class="btn sm" href="#top">Back to the client site</a>') \
        .replace('href="../../index.html"', 'href="#top"')

    demo_js = last_inline_script(demo)
    dash_js = last_inline_script(dash).replace(
        "location.origin +", "'https://your-domain.com' +")

    # Exactly one widget on the merged page: the auto-mount is disabled and
    # demo.html's own script does the mounting.
    widget = widget.replace("var tag = document.currentScript;", "var tag = null;")

    return "\n".join([
        "<!DOCTYPE html>",
        '<html lang="en"><head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>VoiceCore Reception — a live demonstration</title>",
        '<meta name="theme-color" content="#08122a">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600&family=Jost:wght@300;400;500;600&display=swap">',
        "<style>" + demo_css + "\n" + EXTRA_CSS + "\n" + dash_css + "</style>",
        "</head><body>",
        '<div id="top"></div>',
        demo_markup,
        INTRO,
        '<div class="vc-dash">' + dash_markup + "</div>",
        "<script>" + js_safe(engine) + "</script>",
        "<script>" + js_safe(widget) + "</script>",
        "<script>" + js_safe(demo_js) + "</script>",
        "<script>" + js_safe(dash_js) + "</script>",
        "<script>" + js_safe(BRIDGE) + "</script>",
        "</body></html>",
    ])


def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "voicecore-standalone.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = build()
    out.write_text(page, encoding="utf-8")
    print("Wrote " + str(out) + " (" + str(round(len(page.encode()) / 1024)) + " KB, no external files)")


if __name__ == "__main__":
    main()
