# -*- coding: utf-8 -*-
"""
Build single-file, self-contained versions of the storefront and the back office.

Why: a static multi-page site cannot be handed to someone as one link they can
open on a phone. These bundles inline every stylesheet, script and image (as
data: URIs) into one HTML file, and give the storefront a small client-side
router so all twelve pages work from that single file.

The bundles are a distribution format, not the source. Edit the real files under
shop/ and re-run this.

    python3 tools/bundle.py
"""
import os, re, base64, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOP = os.path.join(ROOT, "shop")
DIST = os.path.join(ROOT, "dist")

PAGES = ["index", "shop", "deals", "product", "cart", "checkout", "order",
         "account", "delivery", "about", "contact", "404"]

CHARSET = '<meta charset="utf-8">'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;'
         '12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600'
         '&display=swap" rel="stylesheet">')

def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as f:
        return f.read()

def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")

def image_map():
    """Every asset keyed by the path the source refers to."""
    out = {}
    base = os.path.join(SHOP, "assets", "img")
    for folder in ("products", "aisles", "scenes", "brand"):
        d = os.path.join(base, folder)
        for name in sorted(os.listdir(d)):
            if name.endswith(".svg"):
                out["assets/img/%s/%s" % (folder, name)] = data_uri(os.path.join(d, name))
    return out

def inline_images(text, imgs):
    """Swap literal asset paths (with or without a ../ prefix) for data URIs."""
    for path, uri in imgs.items():
        if path in text:
            text = text.replace("../" + path, uri).replace(path, uri)
    return text

def body_of(html):
    m = re.search(r'<main id="main">(.*?)</main>', html, re.S)
    return m.group(1).strip() if m else ""

# ---------------------------------------------------------------- storefront
def build_storefront(imgs):
    routes = {}
    for page in PAGES:
        routes[page] = inline_images(body_of(read(SHOP, page + ".html")), imgs)

    css = read(SHOP, "assets", "css", "store.css")
    js = []
    for f in ("config.js", "data.js", "pages.js", "store.js"):
        js.append(inline_images(read(SHOP, "assets", "js", f), imgs))

    router = """
/* ---------------------------------------------------------------------------
   Single-file router. Only used by this bundle — the real site is twelve
   ordinary HTML pages and needs none of it.
   --------------------------------------------------------------------------- */
(function () {
  var ROUTES = window.__ROUTES;
  var main = document.getElementById("main");

  function mount(page, query, push) {
    if (!ROUTES[page]) return false;
    window.__QUERY = new URLSearchParams(query || "");
    // controllers register these each time they run; clear the previous page's
    window.__onSearch = null; window.__onCartChange = null; window.__onZoneChange = null;
    document.body.dataset.page = page;
    main.innerHTML = ROUTES[page];
    document.body.classList.remove("lock");
    var scrim = document.getElementById("scrim"); if (scrim) scrim.classList.remove("on");
    var dr = document.getElementById("drawer"); if (dr) dr.classList.remove("on");
    window.RC.renderChrome(page);
    window.RC.renderCart();
    if (window.PAGES[page]) window.PAGES[page]();
    if (push !== false) window.scrollTo(0, 0);
    try { history.replaceState(null, "", "#" + page + (query ? "?" + query : "")); } catch (e) {}
    return true;
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href || /^(https?:|mailto:|tel:|data:)/.test(href)) return;
    if (href.charAt(0) === "#") return;
    var parts = href.split("?");
    var file = parts[0].replace(/^\\.\\//, "");
    if (file === "" ) return;
    var page = file.replace(/\\.html$/, "");
    if (file.indexOf("admin/") === 0) { return; }        // let the back-office link work
    if (file.indexOf("../") === 0) { return; }           // company site link
    if (!ROUTES[page]) return;
    e.preventDefault();
    mount(page, parts[1] || "");
  });

  var hash = (location.hash || "").replace(/^#/, "");
  var hp = hash.split("?");
  if (hp[0] && ROUTES[hp[0]]) mount(hp[0], hp[1] || "");
})();
"""

    html = ("%s<title>%s</title>\n%s\n<style>\n%s\n</style>\n"
            "<a class=\"skip\" href=\"#main\">Skip to content</a>\n"
            "<div id=\"siteHeader\"></div>\n<main id=\"main\">%s</main>\n"
            "<div id=\"siteFooter\"></div>\n<div id=\"siteOverlays\"></div>\n"
            "<script>window.__ROUTES = %s;\nwindow.__IMG = %s;</script>\n"
            "<script>%s</script>\n<script>%s</script>\n") % (
        CHARSET, "Kira Superstore", FONTS, css, routes["index"],
        json.dumps(routes), json.dumps(imgs),
        "\n".join(js), router)
    # the bundle opens on the home page
    html = html.replace('<body data-page="index">', "")
    return html

# ---------------------------------------------------------------- back office
def build_admin(imgs):
    page = read(SHOP, "admin", "index.html")
    inner = re.search(r"<body>(.*?)</body>", page, re.S).group(1)
    inner = re.sub(r"<script[^>]*></script>", "", inner)
    inner = inline_images(inner, imgs)

    css = read(SHOP, "assets", "css", "admin.css")
    js = []
    for f in ("config.js", "data.js", "admin.js"):
        t = read(SHOP, "assets", "js", f)
        if f == "admin.js":
            # admin.js prefixes catalogue paths with ../ to climb out of admin/.
            # Once inlined those values are absolute data: URIs, so drop the prefix.
            t = re.sub(r"\.\./' \+ esc\(p\.", "' + esc(p.", t)
        js.append(inline_images(t, imgs))

    return ("%s<title>RetailCore Back Office</title>\n%s\n<style>\n%s\n</style>\n%s\n<script>%s</script>\n"
            % (CHARSET, FONTS.replace("Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=", ""),
               css, inner, "\n".join(js)))

def build_company(imgs, shop_url=None, admin_url=None):
    """The agency site as one file. Demo links point at the published demos."""
    page = read(ROOT, "index.html")
    inner = re.search(r"<body>(.*?)</body>", page, re.S).group(1)
    inner = re.sub(r'<link rel="stylesheet"[^>]*>', "", inner)
    inner = inline_images(inner, imgs)
    inner = inner.replace('src="shop/assets/img/', 'src="assets/img/')
    inner = inline_images(inner, imgs)
    if shop_url:
        inner = re.sub(r'href="shop/(index|shop|delivery)\.html"',
                       'href="%s" target="_blank" rel="noopener"' % shop_url, inner)
    if admin_url:
        inner = inner.replace('href="shop/admin/index.html"',
                              'href="%s" target="_blank" rel="noopener"' % admin_url)
    css = read(ROOT, "assets", "css", "site.css")
    return "%s<title>Blessed Digital Solutions</title>\n%s\n<style>\n%s\n</style>\n%s\n" % (
        CHARSET, FONTS, css, inner)


if __name__ == "__main__":
    os.makedirs(DIST, exist_ok=True)
    imgs = image_map()
    print("images inlined :", len(imgs))
    import sys
    shop_url = sys.argv[1] if len(sys.argv) > 1 else None
    admin_url = sys.argv[2] if len(sys.argv) > 2 else None
    for name, html in (("shop-demo.html", build_storefront(imgs)),
                       ("back-office.html", build_admin(imgs)),
                       ("company-site.html", build_company(imgs, shop_url, admin_url))):
        path = os.path.join(DIST, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("%-18s %6.1f KB" % (name, os.path.getsize(path) / 1024))
