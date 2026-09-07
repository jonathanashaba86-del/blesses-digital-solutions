/* ============================================================================
   RetailCore storefront engine.

   One script drives every page. Each page carries data-page on <body>; this
   file renders the shared chrome, then hands off to that page's controller.

   The basket lives in localStorage so it survives a refresh and follows the
   shopper from the home page to checkout. In production the same functions
   would post to an API; the shapes here are deliberately the shapes an order
   endpoint would accept.
   ============================================================================ */
(function () {
"use strict";

var SHOP = window.SHOP, CATALOG = window.CATALOG || [], AISLES = window.AISLES || [];
var KEY = "retailcore:" + (SHOP.name || "shop").toLowerCase().replace(/[^a-z0-9]+/g, "-");

/* ---------------------------------------------------------------- helpers */
var $  = function (s, r) { return (r || document).querySelector(s); };
var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
var byId = function (id) { return document.getElementById(id); };

function money(n) {
  return SHOP.currency + " " + Math.round(n).toLocaleString(SHOP.locale || "en-UG");
}
function num(n) { return Math.round(n).toLocaleString(SHOP.locale || "en-UG"); }
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}
function weighed(p) { return p.u === "kg"; }
function stepFor(p) { return weighed(p) ? 0.25 : 1; }
function startQty(p) { return weighed(p) ? 1 : 1; }   // people buy a kilo, not a quarter
function maxFor(p) { return weighed(p) ? 20 : 40; }
function product(slug) { for (var i = 0; i < CATALOG.length; i++) if (CATALOG[i].slug === slug) return CATALOG[i]; return null; }
function productById(id) { for (var i = 0; i < CATALOG.length; i++) if (CATALOG[i].id === +id) return CATALOG[i]; return null; }
function aisleOf(name) { for (var i = 0; i < AISLES.length; i++) if (AISLES[i].c === name) return AISLES[i]; return { n: "00", c: name, slug: "" }; }
function qs(k) { return new URLSearchParams(location.search).get(k); }
function daysTo(expiry) {
  if (!expiry) return null;
  if (/^\+\d+$/.test(expiry)) return parseInt(expiry.slice(1), 10);
  return Math.round((new Date(expiry) - new Date()) / 86400000);
}

/* ---------------------------------------------------------------- state */
var S = {
  zone: SHOP.zones[0],
  cart: {},          // slug -> qty
  qty: {},           // slug -> chosen qty on the card
  pay: SHOP.payments[0].id,
  form: { name: "", phone: "", area: "", landmark: "", note: "" },
  orders: []
};

function load() {
  try {
    var raw = JSON.parse(localStorage.getItem(KEY) || "{}");
    if (raw.cart) S.cart = raw.cart;
    if (raw.form) S.form = Object.assign(S.form, raw.form);
    if (raw.pay) S.pay = raw.pay;
    if (raw.orders) S.orders = raw.orders;
    if (raw.zone) {
      for (var i = 0; i < SHOP.zones.length; i++) if (SHOP.zones[i].id === raw.zone) S.zone = SHOP.zones[i];
    }
  } catch (e) { /* private mode, or corrupt value — start fresh */ }
  CATALOG.forEach(function (p) { S.qty[p.slug] = S.cart[p.slug] || startQty(p); });
}
function save() {
  try {
    localStorage.setItem(KEY, JSON.stringify({
      cart: S.cart, form: S.form, pay: S.pay, zone: S.zone.id, orders: S.orders.slice(0, 12)
    }));
  } catch (e) { /* storage full or blocked — the page still works for this visit */ }
}

/* ---------------------------------------------------------------- basket maths */
function items() {
  return Object.keys(S.cart).map(function (slug) {
    return { p: product(slug), q: S.cart[slug] };
  }).filter(function (i) { return i.p; });
}
function lineTotal(p, q) { return p.price * q; }
function subtotal() { return items().reduce(function (s, i) { return s + lineTotal(i.p, i.q); }, 0); }
function unitCount() { return items().reduce(function (s, i) { return s + (weighed(i.p) ? 1 : i.q); }, 0); }
function savings() {
  return items().reduce(function (s, i) { return s + (i.p.was ? (i.p.was - i.p.price) * i.q : 0); }, 0);
}
function anyWeighed() { return items().some(function (i) { return weighed(i.p); }); }
function fee() {
  var sub = subtotal();
  if (sub === 0) return 0;
  return sub >= SHOP.freeOver ? 0 : S.zone.fee;
}
function total() { return subtotal() + fee(); }
function belowMin() { return subtotal() > 0 && subtotal() < S.zone.min; }
function vat() { return Math.round(total() - total() / (1 + SHOP.vatRate)); }

/* ---------------------------------------------------------------- chrome */
function icon(name) {
  var d = {
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    user:   '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    pin:    '<path d="M12 21s7-5.7 7-11a7 7 0 1 0-14 0c0 5.3 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
    cart:   '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.5a2 2 0 0 0 2-1.6L21 8H6"/><circle cx="10" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/>'
  }[name] || "";
  return '<svg viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>';
}

function header(active) {
  var nav = [["index.html", "Home"], ["shop.html", "Shop"], ["deals.html", "Offers"],
             ["delivery.html", "Delivery"], ["about.html", "About"], ["contact.html", "Contact"]];
  return '' +
  '<div class="strip"><div class="wrap strip-in">' +
    '<span>ORDER BY ' + esc(SHOP.cutoff).toUpperCase() + ' · DELIVERED TODAY ' + esc(SHOP.windowText).toUpperCase() + '</span>' +
    '<span>FREE DELIVERY OVER <b>' + esc(money(SHOP.freeOver)) + '</b> · ' +
      SHOP.payments.map(function (p) { return esc(p.name.toUpperCase()); }).join(" · ") + '</span>' +
  '</div></div>' +
  '<header class="hdr"><div class="wrap hdr-in">' +
    '<a href="index.html" class="mark" aria-label="' + esc(SHOP.name) + ' home">' +
      '<img src="assets/img/brand/logo.svg" alt="" width="38" height="38">' +
      '<span class="mark-t"><span class="mark-n">' + brandMarkup() + '</span>' +
      '<span class="mark-s">' + esc(SHOP.strapline) + '</span></span></a>' +
    '<div class="search"><span class="ic">' + icon("search") + '</span>' +
      '<label class="sr" for="q">Search the shop</label>' +
      '<input id="q" type="search" placeholder="Search ' + CATALOG.length + ' lines — rice, beef, milk…" autocomplete="off">' +
      '<button class="clr" id="qClear" type="button" aria-label="Clear search">✕</button></div>' +
    '<div class="hdr-r">' +
      '<button class="pill" id="zonePill">Deliver to <b id="zoneLbl">' + esc(S.zone.name.split(" · ")[0]) + '</b></button>' +
      '<a class="icon-btn" href="account.html" aria-label="Your account">' + icon("user") + '</a>' +
      '<button class="basket" id="basketBtn"><span class="lbl">Basket</span>' +
        '<span class="basket-n" id="bCount">0</span></button>' +
    '</div>' +
  '</div></header>' +
  '<nav class="aisles" aria-label="Sections"><div class="wrap"><div class="aisles-in">' +
    nav.map(function (n) {
      return '<a class="aisle-tab' + (n[0] === active ? " on" : "") + '" href="' + n[0] + '">' + esc(n[1]) + '</a>';
    }).join("") +
  '</div></div></nav>';
}

function brandMarkup() {
  var w = SHOP.name.split(" ");
  if (w.length < 2) return esc(SHOP.name);
  return esc(w[0]) + "<em>" + esc(w.slice(1).join(" ")) + "</em>";
}

function footer() {
  var aisleLinks = AISLES.slice(0, 5).map(function (a) {
    return '<li><a href="shop.html?aisle=' + encodeURIComponent(a.c) + '">' + esc(a.c) + '</a></li>';
  }).join("");
  return '<footer class="ft"><div class="wrap"><div class="ftg">' +
    '<div><p class="ftm">' + esc(SHOP.name) + '</p>' +
      '<p class="ftb">' + esc(SHOP.blurb) + '</p>' +
      '<p style="font-family:var(--mono);font-size:11.5px;color:#68809A;margin:0">' +
        esc(SHOP.address) + '<br>' + esc(SHOP.phone) + ' · ' + esc(SHOP.email) + '</p>' +
      '<div class="ft-pay">' + SHOP.payments.map(function (p) {
        return '<img src="' + esc(p.mark) + '" alt="' + esc(p.name) + '" width="46" height="29" loading="lazy">';
      }).join("") + '</div></div>' +
    '<div><h5>Aisles</h5><ul>' + aisleLinks + '</ul></div>' +
    '<div><h5>Service</h5><ul>' +
      '<li><a href="delivery.html">Delivery zones</a></li>' +
      '<li><a href="delivery.html#faq">Questions</a></li>' +
      '<li><a href="account.html">Your orders</a></li>' +
      '<li><a href="contact.html#trade">Corporate accounts</a></li>' +
      '<li><a href="contact.html">Contact us</a></li></ul></div>' +
    '<div><h5>Opening hours</h5><ul>' + SHOP.hours.map(function (h) {
        return '<li>' + esc(h.d) + '<br><span style="color:#68809A">' + esc(h.h) + '</span></li>';
      }).join("") + '</ul></div>' +
    '</div><div class="ftbar">' +
      '<span>© ' + new Date().getFullYear() + ' ' + esc(SHOP.legalName).toUpperCase() + ' · ' + esc(SHOP.address).toUpperCase() + '</span>' +
      '<span>BUILT BY <a href="../index.html">BLESSED DIGITAL SOLUTIONS</a> · <a href="admin/index.html">STAFF LOGIN</a></span>' +
    '</div></div></footer>';
}

function overlays() {
  return '<div class="scrim" id="scrim"></div>' +
    '<aside class="drawer" id="drawer" role="dialog" aria-label="Your basket" aria-modal="true">' +
      '<div class="dhd"><h2>Your basket</h2><button class="x" id="dX" aria-label="Close basket">✕</button></div>' +
      '<div class="dbody" id="dBody"></div><div class="dfoot" id="dFoot"></div></aside>' +
    '<div class="modal" id="modal" role="dialog" aria-label="Details" aria-modal="true">' +
      '<div class="mhd"><h2 id="mTitle">Details</h2><button class="x" id="mX" aria-label="Close">✕</button></div>' +
      '<div class="mbody" id="mBody"></div></div>' +
    '<div class="toast" id="toast" role="status" aria-live="polite"></div>' +
    '<div class="mobar" id="mobar"><div class="mobar-t"><div class="mobar-k" id="mobarK">Basket</div>' +
      '<div class="mobar-v" id="mobarV">—</div></div>' +
      '<a class="btn b-accent b-sm" href="cart.html">View basket</a></div>';
}

function toast(msg) {
  var t = byId("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("on");
  clearTimeout(t._h);
  t._h = setTimeout(function () { t.classList.remove("on"); }, 2600);
}

/* ---------------------------------------------------------------- product card */
function comparePrice(p) {
  if (weighed(p)) return "<b>" + num(p.price / 10) + "</b> per 100g";
  if (p.size) {
    var per100 = p.price / (p.size / 100);
    var liquid = /ml|litre|juice|oil|water|milk|lotion|wash|bleach/i.test(p.n + " " + p.u);
    return "<b>" + num(per100) + "</b> per " + (liquid ? "100ml" : "100g");
  }
  return "<b>" + num(p.price) + "</b> per " + esc(p.u);
}

function shelfLabel(p) {
  var save = p.was ? p.was - p.price : 0;
  return '<div class="shelf"><div class="shelf-main">' +
      '<span class="shelf-price">' + num(p.price) + '</span>' +
      '<span>' + (p.was ? '<span class="shelf-was">' + num(p.was) + '</span> ' : "") +
        '<span class="shelf-unit">' + (weighed(p) ? "/KG" : "EA") + '</span></span></div>' +
    '<div class="shelf-cmp"><span>' + comparePrice(p) + '</span>' +
      '<span' + (save ? ' class="save"' : "") + '>' + (save ? "SAVE " + num(save) : esc(SHOP.currency)) + '</span>' +
    '</div></div>';
}

function stockLabel(p) {
  if (p.stock === 0) return { cls: "out", txt: "Finished" };
  if (p.stock <= 10) return { cls: "low", txt: p.stock + " left" };
  return { cls: "", txt: "In stock" };
}

function qtyLabel(p, q) {
  return weighed(p) ? q.toFixed(2) + " kg" : q + " × " + p.u;
}

function card(p) {
  var q = S.qty[p.slug] || startQty(p), inCart = S.cart[p.slug] != null;
  var out = p.stock === 0, st = stockLabel(p);
  var flag = "";
  if (p.was) flag = '<span class="flag">Cut ' + num(p.was - p.price) + '</span>';
  else if (p.tags && p.tags.indexOf("local") > -1) flag = '<span class="flag local">Local</span>';
  else if (p.tags && p.tags.indexOf("season") > -1) flag = '<span class="flag new">In season</span>';
  return '<article class="prod" data-slug="' + esc(p.slug) + '">' +
    '<a class="tile' + (out ? " sold" : "") + '" href="product.html?p=' + esc(p.slug) + '">' + flag +
      '<span class="tag-stock ' + st.cls + '">' + esc(st.txt) + '</span>' +
      '<img src="' + esc(p.img) + '" alt="' + esc(p.n) + '" loading="lazy" width="800" height="600"></a>' +
    '<div class="pb"><h3 class="pn"><a href="product.html?p=' + esc(p.slug) + '">' + esc(p.n) + '</a></h3>' +
      '<p class="pd">' + esc(p.d) + '</p>' + shelfLabel(p) +
      '<div class="pf"><div class="dial">' +
        '<button data-step="-1" data-slug="' + esc(p.slug) + '" aria-label="Less ' + esc(p.n) + '">−</button>' +
        '<span class="dial-v">' + esc(qtyLabel(p, q)) + '</span>' +
        '<button data-step="1" data-slug="' + esc(p.slug) + '" aria-label="More ' + esc(p.n) + '">+</button></div>' +
      '<div class="est"><span>' + (weighed(p) ? "Estimated" : "Subtotal") + '</span>' + esc(money(lineTotal(p, q))) + '</div>' +
      '<button class="add' + (inCart ? " in" : "") + '" data-add="' + esc(p.slug) + '"' + (out ? " disabled" : "") + '>' +
        (out ? "Finished today" : inCart ? "In basket · add more" : "Add to basket") + '</button>' +
    '</div></div></article>';
}

/* ---------------------------------------------------------------- basket UI */
function renderCart() {
  var list = items(), n = unitCount();
  var bc = byId("bCount"); if (bc) bc.textContent = n;
  var mobar = byId("mobar");
  if (mobar) {
    mobar.classList.toggle("on", n > 0 && document.body.dataset.page !== "cart" && document.body.dataset.page !== "checkout");
    byId("mobarK").textContent = n + (n === 1 ? " item" : " items") + (belowMin() ? " · below minimum" : "");
    byId("mobarV").textContent = money(total());
  }
  var body = byId("dBody"), foot = byId("dFoot");
  if (!body) return;
  if (!list.length) {
    body.innerHTML = '<div class="empty" style="border:0;background:none;padding:44px 6px">' +
      '<img src="assets/img/scenes/empty.svg" alt="" width="112" height="112">' +
      '<h3>Basket is empty</h3><p>Start in Aisle 01 — a few lines are reduced this week.</p>' +
      '<a class="btn b-ghost" href="shop.html">Open the aisles</a></div>';
    foot.innerHTML = "";
    return;
  }
  body.innerHTML = freeBar() +
    (belowMin() ? '<div class="warn">Add ' + money(S.zone.min - subtotal()) + ' more to reach the ' +
      money(S.zone.min) + ' minimum for ' + esc(S.zone.name.split(" · ")[0]) + '.</div>' : "") +
    list.map(function (i) { return cartLine(i.p, i.q); }).join("") +
    (anyWeighed() ? '<p class="note">Lines marked <em style="font-style:normal;color:var(--accent)">est.</em> are ' +
      'weighed at the counter. The total can move up to ' + Math.round(SHOP.tolerance * 100) +
      '% either way — we text you the exact figure before the rider leaves.</p>' : "");
  var free = fee() === 0 && subtotal() > 0, sv = savings();
  foot.innerHTML =
    (sv ? '<div class="tot"><span>You saved</span><span class="save-badge">' + money(sv) + '</span></div>' : "") +
    '<div class="tot"><span>Subtotal</span><span>' + money(subtotal()) + '</span></div>' +
    '<div class="tot' + (free ? " free" : "") + '"><span>Delivery · ' + esc(S.zone.name.split(" · ")[0]) + '</span>' +
      '<span>' + (free ? "Free" : money(fee())) + '</span></div>' +
    '<div class="tot g"><span>Total</span><span>' + money(total()) + '</span></div>' +
    '<a class="btn b-accent b-block' + (belowMin() ? " is-off" : "") + '" href="checkout.html" style="margin-top:15px">' +
      (belowMin() ? "Minimum basket not reached" : "Checkout") + '</a>' +
    '<button class="btn b-ghost b-block" id="waOrder" style="margin-top:8px">Send basket on WhatsApp</button>';
}

function cartLine(p, q) {
  return '<div class="line">' +
    '<a class="ltile" href="product.html?p=' + esc(p.slug) + '"><img src="' + esc(p.img) + '" alt="" width="56" height="56" loading="lazy"></a>' +
    '<div><div class="ln">' + esc(p.n) + '</div><div class="lm">' +
      (weighed(p) ? q.toFixed(2) + " kg × " + num(p.price) + "/kg · <em>est.</em>"
                  : q + " × " + num(p.price)) + '</div></div>' +
    '<div class="lr"><span class="lp">' + money(lineTotal(p, q)) + '</span>' +
      '<button class="lrm" data-rm="' + esc(p.slug) + '">Remove</button></div></div>';
}

function freeBar() {
  var sub = subtotal();
  if (!sub) return "";
  var pct = Math.min(100, sub / SHOP.freeOver * 100);
  var done = sub >= SHOP.freeOver;
  return '<div class="freebar"><div class="freebar-t">' +
    (done ? "<b>Delivery is on us</b> — you passed " + money(SHOP.freeOver) + "."
          : "Add <b>" + money(SHOP.freeOver - sub) + "</b> more for free delivery.") +
    '</div><div class="freebar-track"><div class="freebar-fill' + (done ? " done" : "") +
    '" style="width:' + pct.toFixed(1) + '%"></div></div></div>';
}

function addToCart(slug, silent) {
  var p = product(slug);
  if (!p || p.stock === 0) return;
  S.cart[slug] = S.qty[slug] || startQty(p);
  save(); renderCart(); refreshCards();
  if (!silent) toast(p.n + " added · " + qtyLabel(p, S.cart[slug]));
}
function removeFromCart(slug) {
  var p = product(slug);
  delete S.cart[slug];
  save(); renderCart(); refreshCards();
  if (p) toast(p.n + " removed from the basket");
}
function bumpQty(slug, dir) {
  var p = product(slug); if (!p) return;
  var step = stepFor(p) * dir;
  var next = Math.min(maxFor(p), Math.max(stepFor(p), +((S.qty[slug] || stepFor(p)) + step).toFixed(2)));
  S.qty[slug] = next;
  if (S.cart[slug] != null) S.cart[slug] = next;
  save(); renderCart(); refreshCards();
}
function refreshCards() {
  $$("[data-slug]").forEach(function (el) {
    if (!el.classList.contains("prod")) return;
    var p = product(el.dataset.slug); if (!p) return;
    var q = S.qty[p.slug] || startQty(p);
    var dv = $(".dial-v", el); if (dv) dv.textContent = qtyLabel(p, q);
    var est = $(".est", el);
    if (est) est.innerHTML = '<span>' + (weighed(p) ? "Estimated" : "Subtotal") + '</span>' + money(lineTotal(p, q));
    var add = $(".add", el);
    if (add && p.stock > 0) {
      var inCart = S.cart[p.slug] != null;
      add.classList.toggle("in", inCart);
      add.textContent = inCart ? "In basket · add more" : "Add to basket";
    }
  });
  if (window.__onCartChange) window.__onCartChange();
}

function openDrawer() {
  renderCart();
  byId("drawer").classList.add("on");
  byId("scrim").classList.add("on");
  document.body.classList.add("lock");
}
function closeAll() {
  var d = byId("drawer"), m = byId("modal"), s = byId("scrim");
  if (d) d.classList.remove("on");
  if (m) m.classList.remove("on");
  if (s) s.classList.remove("on");
  document.body.classList.remove("lock");
}
function openModal(title, html) {
  byId("mTitle").textContent = title;
  byId("mBody").innerHTML = html;
  byId("modal").classList.add("on");
  byId("scrim").classList.add("on");
  document.body.classList.add("lock");
}

function whatsappHref() {
  var lines = items().map(function (i) {
    return "• " + i.p.n + " — " + qtyLabel(i.p, i.q) + " — " + money(lineTotal(i.p, i.q));
  }).join("\n");
  var msg = "Hello " + SHOP.name + ", I would like to order:\n\n" + lines +
    "\n\nDelivery: " + S.zone.name + "\nSubtotal: " + money(subtotal()) +
    "\nDelivery: " + money(fee()) + "\nTotal: " + money(total());
  return "https://wa.me/" + SHOP.whatsapp + "?text=" + encodeURIComponent(msg);
}

function setZone(id) {
  for (var i = 0; i < SHOP.zones.length; i++) {
    if (SHOP.zones[i].id === id) S.zone = SHOP.zones[i];
  }
  var lbl = byId("zoneLbl");
  if (lbl) lbl.textContent = S.zone.name.split(" · ")[0];
  save(); renderCart();
  $$("[data-zone]").forEach(function (b) { b.classList.toggle("on", b.dataset.zone === S.zone.id); });
  if (window.__onZoneChange) window.__onZoneChange();
}

/* ---------------------------------------------------------------- orders */
function makeRef() {
  var initials = SHOP.name.split(" ").map(function (w) { return w[0]; }).join("").slice(0, 2).toUpperCase();
  return initials + "-" + (Math.floor(Math.random() * 9000) + 1000);
}
function placeOrder(extra) {
  var order = {
    ref: makeRef(),
    at: new Date().toISOString(),
    lines: items().map(function (i) {
      return { slug: i.p.slug, n: i.p.n, q: i.q, u: i.p.u, price: i.p.price, weighed: weighed(i.p) };
    }),
    sub: subtotal(), fee: fee(), total: total(), vat: vat(),
    zone: S.zone.name, eta: S.zone.eta, pay: S.pay,
    customer: Object.assign({}, S.form),
    status: "placed"
  };
  Object.assign(order, extra || {});
  S.orders.unshift(order);
  S.cart = {};
  save(); renderCart(); refreshCards();
  return order;
}

/* ---------------------------------------------------------------- global events */
function wireGlobal() {
  document.addEventListener("click", function (e) {
    var t = e.target;
    var hit = function (sel) { return t.closest ? t.closest(sel) : null; };

    var step = hit("[data-step]");
    if (step) { bumpQty(step.dataset.slug, +step.dataset.step); return; }

    var add = hit("[data-add]");
    if (add) { addToCart(add.dataset.add); return; }

    var rm = hit("[data-rm]");
    if (rm) { removeFromCart(rm.dataset.rm); return; }

    var zone = hit("[data-zone]");
    if (zone) {
      setZone(zone.dataset.zone);
      toast("Delivering to " + S.zone.name.split(" · ")[0] + " · " +
            (subtotal() >= SHOP.freeOver ? "free" : money(S.zone.fee)));
      return;
    }

    var id = t.id || (t.closest("[id]") ? t.closest("[id]").id : "");
    switch (id) {
      case "basketBtn": openDrawer(); break;
      case "dX": case "scrim": case "mX": closeAll(); break;
      case "zonePill":
        if (document.body.dataset.page === "delivery") {
          var z = byId("zoneSec"); if (z) z.scrollIntoView({ behavior: "smooth" });
        } else { location.href = "delivery.html#zoneSec"; }
        break;
      case "waOrder": window.open(whatsappHref(), "_blank", "noopener"); break;
      case "qClear":
        var q = byId("q"); if (q) { q.value = ""; q.dispatchEvent(new Event("input", { bubbles: true })); q.focus(); }
        break;
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll();
    if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
      var q = byId("q"); if (q) { e.preventDefault(); q.focus(); }
    }
  });

  var q = byId("q");
  if (q) {
    q.addEventListener("input", function () {
      if (window.__onSearch) { window.__onSearch(q.value); return; }
      if (q.value.trim()) {
        clearTimeout(q._t);
        q._t = setTimeout(function () {
          location.href = "shop.html?q=" + encodeURIComponent(q.value.trim());
        }, 700);
      }
    });
    q.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && q.value.trim() && !window.__onSearch) {
        location.href = "shop.html?q=" + encodeURIComponent(q.value.trim());
      }
    });
  }
}

/* ---------------------------------------------------------------- boot */
function boot() {
  document.documentElement.setAttribute("data-theme", SHOP.theme || "superstore");
  load();
  var page = document.body.dataset.page || "index";
  var head = byId("siteHeader"), foot = byId("siteFooter"), over = byId("siteOverlays");
  if (head) head.innerHTML = header(page === "index" ? "index.html" : page + ".html");
  if (over) over.innerHTML = overlays();
  if (foot) foot.innerHTML = footer();
  document.title = document.title.replace("{shop}", SHOP.name);
  // fill any [data-shop-*] placeholder straight from the config
  var bind = { name: SHOP.name, tagline: SHOP.tagline, phone: SHOP.phone, email: SHOP.email,
               address: SHOP.address, map: SHOP.mapNote, cutoff: SHOP.cutoff, window: SHOP.windowText,
               free: money(SHOP.freeOver) };
  Object.keys(bind).forEach(function (k) {
    $$("[data-shop-" + k + "]").forEach(function (el) { el.textContent = bind[k]; });
  });
  var wa = byId("waLink");
  if (wa) wa.href = "https://wa.me/" + SHOP.whatsapp;
  var tel = $$("[data-shop-tel]");
  tel.forEach(function (el) { el.href = "tel:" + SHOP.phoneRaw; });
  wireGlobal();
  renderCart();
  if (window.PAGES && window.PAGES[page]) window.PAGES[page]();
}

/* expose the bits page controllers need */
window.RC = {
  S: S, SHOP: SHOP, CATALOG: CATALOG, AISLES: AISLES,
  $: $, $$: $$, byId: byId, esc: esc, money: money, num: num,
  weighed: weighed, product: product, productById: productById, aisleOf: aisleOf,
  card: card, shelfLabel: shelfLabel, stockLabel: stockLabel, qtyLabel: qtyLabel,
  comparePrice: comparePrice, lineTotal: lineTotal, subtotal: subtotal, fee: fee,
  total: total, vat: vat, savings: savings, items: items, unitCount: unitCount,
  belowMin: belowMin, anyWeighed: anyWeighed, freeBar: freeBar, cartLine: cartLine,
  addToCart: addToCart, removeFromCart: removeFromCart, renderCart: renderCart,
  refreshCards: refreshCards, setZone: setZone, openModal: openModal, closeAll: closeAll,
  toast: toast, save: save, qs: qs, daysTo: daysTo, placeOrder: placeOrder,
  whatsappHref: whatsappHref, icon: icon, stepFor: stepFor, startQty: startQty, makeRef: makeRef
};

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
})();
