# -*- coding: utf-8 -*-
"""Build a standalone review page from tools/photos.json.

This exists because the build machine cannot load images: the only way to be sure
a photograph matches the line it represents is for a person to look at it. Every
pick is shown at the size and crop the site will actually use.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def build(out_path):
    with open(os.path.join(HERE, "photos.json"), encoding="utf-8") as f:
        man = json.load(f)["photos"]

    cells = []
    for key, e in sorted(man.items()):
        cells.append(
            '<figure><img src="%s" alt="%s" loading="lazy">'
            '<figcaption><b>%s</b><span class="alt">%s</span>'
            '<span class="by">%s · searched &ldquo;%s&rdquo;</span></figcaption></figure>'
            % (e["url"], e["alt"].replace('"', "&quot;"), key, e["alt"],
               e["photographer"], e["query"]))

    TPL = """<meta charset="utf-8">
<title>Photo Review Sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#0E141B;--panel:#18212C;--line:#26333F;--ink:#EDF1F5;--muted:#8B9AA8;--ok:#3DDC97;--accent:#5B8DEF}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif;padding:26px clamp(14px,3vw,40px) 60px}
header{max-width:1400px;margin:0 auto 26px}
h1{font-size:clamp(20px,3vw,28px);margin:0 0 10px;letter-spacing:-.02em}
p{color:var(--muted);font-size:14.5px;line-height:1.65;margin:0 0 6px;max-width:75ch}
.count{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ok);
  border:1px solid var(--line);border-radius:4px;padding:6px 10px;display:inline-block;margin-top:12px}
.grid{max-width:1400px;margin:0 auto;display:grid;gap:16px;
  grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#222C38}
figcaption{padding:11px 13px 13px;display:grid;gap:5px}
b{font-size:13.5px;font-weight:600}
.alt{font-size:12px;color:var(--muted);line-height:1.45}
.by{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:#5E6E7C;letter-spacing:.02em}
</style>
<header>
  <h1>Photo review &mdash; @@N@@ picks</h1>
  <p>Every photograph below is a real Unsplash picture, chosen through the API and
     cropped to exactly the 4:3 frame the product tiles use. Nothing here is drawn.</p>
  <p>Look for anything that is plainly the wrong item &mdash; that is the whole job of
     this page. Tell me the names underneath and I will re-pick those.</p>
  <span class="count">@@N@@ photographs loaded from images.unsplash.com</span>
</header>
<div class="grid">@@CELLS@@</div>
"""
    html = (TPL.replace("@@N@@", str(len(cells)))
               .replace("@@CELLS@@", "".join(cells)))

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s (%d photos)" % (out_path, len(cells)))

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist", "photo-review.html"))
