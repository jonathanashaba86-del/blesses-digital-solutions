/* ============================================================================
   Page controllers. store.js renders the shared chrome, then calls the
   controller named after <body data-page>.
   ============================================================================ */
window.PAGES = (function () {
"use strict";
function assetURL(p) { return (window.__IMG && window.__IMG[p]) || p; }

var R;   // filled on first call — store.js publishes window.RC before dispatch

function init() { R = window.RC; }

/* ---------------------------------------------------------------- shared bits */
var SHOP_CTX = null, CO_CTX = null;

function sortItems(list, how) {
  var l = list.slice();
  if (how === "price-asc")  l.sort(function (a, b) { return a.price - b.price; });
  else if (how === "price-desc") l.sort(function (a, b) { return b.price - a.price; });
  else if (how === "name")  l.sort(function (a, b) { return a.n.localeCompare(b.n); });
  else if (how === "popular") l.sort(function (a, b) { return b.sold - a.sold; });
  else if (how === "deals") l.sort(function (a, b) { return (b.was ? b.was - b.price : 0) - (a.was ? a.was - a.price : 0); });
  return l;
}

function matches(p, q) {
  if (!q) return true;
  q = q.trim().toLowerCase();
  return (p.n + " " + p.c + " " + p.d + " " + (p.origin || "") + " " + (p.tags || []).join(" "))
    .toLowerCase().indexOf(q) > -1;
}

function grid(list) {
  if (!list.length) {
    return '<div class="grid"><div class="empty">' +
      '<img src="assets/img/scenes/empty.svg" alt="" width="112" height="112">' +
      '<h3>Nothing matches that</h3><p>Try a shorter word, or open a different aisle.</p>' +
      '<button class="btn b-ghost" data-reset="1">Clear filters</button></div></div>';
  }
  return '<div class="grid">' + list.map(R.card).join("") + '</div>';
}

function aisleGroups(list) {
  return R.AISLES.filter(function (a) {
    return list.some(function (p) { return p.c === a.c; });
  }).map(function (a) {
    var mine = list.filter(function (p) { return p.c === a.c; });
    var cuts = mine.filter(function (p) { return p.was; }).length;
    return '<section class="aisle-sec" id="aisle-' + a.slug + '">' +
      '<div class="aisle-hd"><div class="aisle-tag">' +
        '<span class="aisle-num">AISLE ' + a.n + '</span>' +
        '<h2 class="aisle-name">' + R.esc(a.c) + '</h2></div>' +
      '<span class="aisle-meta">' + mine.length + ' LINES' + (cuts ? " · " + cuts + " REDUCED" : "") + '</span></div>' +
      grid(mine) + '</section>';
  }).join("");
}

function zoneList() {
  return R.SHOP.zones.map(function (z) {
    return '<button class="zone' + (z.id === R.S.zone.id ? " on" : "") + '" data-zone="' + z.id + '">' +
      '<span><span class="z-n">' + R.esc(z.name) + '</span>' +
      '<span class="z-a">' + R.esc(z.area) + ' · ' + R.esc(z.eta) + '</span></span>' +
      '<span class="z-f">' + R.money(z.fee) + '</span>' +
      '<span class="z-m">min ' + R.num(z.min) + '</span></button>';
  }).join("");
}

function promiseBand() {
  return R.SHOP.promises.map(function (p) {
    return '<div class="bcell"><div class="bnum">' + R.esc(p.k) + '</div>' +
      '<h4>' + R.esc(p.t) + '</h4><p>' + R.esc(p.d) + '</p></div>';
  }).join("");
}

/* ---------------------------------------------------------------- home */
function home() {
  init();
  var rider = R.sceneImage('rider', null);
  if (rider) R.$$('img[src*="scenes/rider"]').forEach(function (im) { im.src = rider; });
  var deals = R.CATALOG.filter(function (p) { return p.was && p.stock > 0; });
  var top = sortItems(R.CATALOG.filter(function (p) { return p.stock > 0; }), "popular").slice(0, 12);

  R.byId("heroStats").innerHTML = [
    [R.CATALOG.length, "Lines stocked online today"],
    [R.SHOP.cutoff.replace(":00", ""), "Cut-off for same-day delivery"],
    [R.SHOP.zones.length, "Delivery zones we cover"],
    ["±" + Math.round(R.SHOP.tolerance * 100) + "%", "Price tolerance on weighed items"]
  ].map(function (s) {
    return '<div class="stat"><div class="stat-v">' + R.esc(s[0]) + '</div><div class="stat-k">' + R.esc(s[1]) + '</div></div>';
  }).join("");

  R.byId("heroKicker").textContent = "This week · " + deals.length + " lines reduced";

  R.byId("aisleCards").innerHTML = R.AISLES.map(function (a) {
    var n = R.CATALOG.filter(function (p) { return p.c === a.c; }).length;
    return '<a class="acard" href="shop.html?aisle=' + encodeURIComponent(a.c) + '">' +
      '<span class="shot"><img src="' + assetURL(R.aisleImage(a.slug)) + '" alt="" loading="lazy" ' +
        'width="1200" height="480">' +
      '<span class="acard-b"><span class="acard-n">' + R.esc(a.c) + '</span>' +
      '<span class="acard-m">AISLE ' + a.n + ' · ' + n + ' LINES</span></span></span></a>';
  }).join("");

  R.byId("dealGrid").innerHTML = '<div class="grid">' + deals.slice(0, 6).map(R.card).join("") + '</div>';
  R.byId("dealCount").textContent = deals.length + " lines reduced";
  R.byId("topGrid").innerHTML = '<div class="grid">' + top.slice(0, 6).map(R.card).join("") + '</div>';
  R.byId("promiseBand").innerHTML = promiseBand();
  R.byId("zones").innerHTML = zoneList();
  R.byId("reviews").innerHTML = R.SHOP.reviews.map(function (r) {
    return '<div class="review"><div class="stars" aria-label="' + r.r + ' out of 5">' +
      "★".repeat(r.r) + '<span style="color:var(--line)">' + "★".repeat(5 - r.r) + '</span></div>' +
      '<p>“' + R.esc(r.t) + '”</p><div class="review-w">' + R.esc(r.n) + '</div>' +
      '<div class="review-z">' + R.esc(r.z) + '</div></div>';
  }).join("");
}

/* ---------------------------------------------------------------- shop */
function shop() {
  init();
  var state = {
    aisle: R.qs("aisle") || "All",
    q: R.qs("q") || "",
    sort: "popular",
    only: R.qs("only") || ""      // "deals" | "local" | ""
  };
  var qInput = R.byId("q");
  if (qInput && state.q) qInput.value = state.q;

  function visible() {
    var l = R.CATALOG.filter(function (p) {
      if (state.aisle !== "All" && p.c !== state.aisle) return false;
      if (state.only === "deals" && !p.was) return false;
      if (state.only === "local" && (p.tags || []).indexOf("local") < 0) return false;
      if (state.only === "instock" && p.stock === 0) return false;
      return matches(p, state.q);
    });
    return sortItems(l, state.sort);
  }

  function draw() {
    var list = visible();
    R.byId("chips").innerHTML =
      '<button class="chip' + (state.aisle === "All" ? " on" : "") + '" data-aisle="All">Everything</button>' +
      R.AISLES.map(function (a) {
        return '<button class="chip' + (state.aisle === a.c ? " on" : "") + '" data-aisle="' + R.esc(a.c) + '">' +
          R.esc(a.c) + '</button>';
      }).join("");
    R.byId("filters").innerHTML =
      ["", "deals", "local", "instock"].map(function (f) {
        var label = { "": "No filter", deals: "Reduced", local: "Local", instock: "In stock" }[f];
        return '<button class="chip' + (state.only === f ? " on" : "") + '" data-only="' + f + '">' + label + '</button>';
      }).join("");
    R.byId("count").textContent = list.length + " of " + R.CATALOG.length + " lines";
    R.byId("results").innerHTML = state.aisle === "All" && !state.q && !state.only
      ? aisleGroups(list) : grid(list);
    var url = new URL(location.href);
    url.search = "";
    if (state.aisle !== "All") url.searchParams.set("aisle", state.aisle);
    if (state.q) url.searchParams.set("q", state.q);
    if (state.only) url.searchParams.set("only", state.only);
    history.replaceState(null, "", url);
  }

  window.__onSearch = function (v) { state.q = v; draw(); };

  // The handler is attached once and reads the live context, so the controller
  // is safe to run again when a single-file build routes back to this page.
  SHOP_CTX = { state: state, draw: draw, qInput: qInput };
  if (!shop._wired) {
    shop._wired = true;
    document.addEventListener("click", function (e) {
      if (!SHOP_CTX || document.body.dataset.page !== "shop") return;
      var c = SHOP_CTX;
      var a = e.target.closest("[data-aisle]");
      if (a) {
        c.state.aisle = a.dataset.aisle; c.draw();
        window.scrollTo({ top: R.byId("results").offsetTop - 130, behavior: "smooth" });
        return;
      }
      var o = e.target.closest("[data-only]");
      if (o) { c.state.only = o.dataset.only; c.draw(); return; }
      if (e.target.closest("[data-reset]")) {
        c.state.aisle = "All"; c.state.only = ""; c.state.q = "";
        if (c.qInput) c.qInput.value = "";
        c.draw();
      }
    });
  }
  R.byId("sort").addEventListener("change", function (e) { state.sort = e.target.value; draw(); });
  draw();
}

/* ---------------------------------------------------------------- deals */
function deals() {
  init();
  var list = R.CATALOG.filter(function (p) { return p.was; })
    .sort(function (a, b) { return (b.was - b.price) - (a.was - a.price); });
  var saveTotal = list.reduce(function (s, p) { return s + (p.was - p.price); }, 0);
  R.byId("dealStats").innerHTML = [
    [list.length, "Lines reduced this week"],
    [R.money(saveTotal).replace(R.SHOP.currency + " ", ""), "Total off if you took one of each"],
    [Math.round(list.reduce(function (s, p) { return s + (p.was - p.price) / p.was * 100; }, 0) / (list.length || 1)) + "%", "Average cut"],
    [R.SHOP.cutoff.replace(":00", ""), "Order by, for today"]
  ].map(function (s) {
    return '<div class="stat"><div class="stat-v">' + R.esc(s[0]) + '</div><div class="stat-k">' + R.esc(s[1]) + '</div></div>';
  }).join("");
  R.byId("dealResults").innerHTML = grid(list);
  var expiring = R.CATALOG.filter(function (p) {
    var d = R.daysTo(p.expiry); return d !== null && d <= 3 && p.stock > 0;
  });
  R.byId("expiring").innerHTML = expiring.length
    ? grid(expiring)
    : '<p class="sec-s">Nothing is close to date today — the shelves turned over well this week.</p>';
}

/* ---------------------------------------------------------------- product */
function productPage() {
  init();
  var p = R.product(R.qs("p") || "");
  var host = R.byId("productView");
  if (!p) {
    host.innerHTML = '<div class="empty" style="margin:40px 0">' +
      '<h3>We could not find that line</h3><p>It may have been renamed or taken off the shelf.</p>' +
      '<a class="btn b-accent" href="shop.html">Back to the aisles</a></div>';
    return;
  }
  document.title = p.n + " — " + R.SHOP.name;
  var a = R.aisleOf(p.c), st = R.stockLabel(p), days = R.daysTo(p.expiry);

  R.byId("crumbs").innerHTML = '<a href="index.html">Home</a><span>/</span>' +
    '<a href="shop.html">Shop</a><span>/</span>' +
    '<a href="shop.html?aisle=' + encodeURIComponent(p.c) + '">' + R.esc(p.c) + '</a><span>/</span>' + R.esc(p.n);

  function view() {
    var q = R.S.qty[p.slug] || R.startQty(p);
    var inCart = R.S.cart[p.slug] != null;
    host.innerHTML = '<div class="pv" data-slug="' + R.esc(p.slug) + '">' +
      '<div class="pv-media"><div class="main">' +
        '<img src="' + R.esc(R.productImage(p)) + '" alt="' + R.esc(p.n) + '" width="800" height="600"></div>' +
        (R.photoCredit(p.slug) ? '<p class="note" style="margin-top:8px">Photograph by <a href="' +
          R.esc(R.photoCredit(p.slug).at) + '" target="_blank" rel="noopener" style="text-decoration:underline">' +
          R.esc(R.photoCredit(p.slug).by) + '</a> on Unsplash</p>' : "") + '</div>' +
      '<div><div class="eyebrow">Aisle ' + a.n + ' · ' + R.esc(p.c) + '</div>' +
        '<h1>' + R.esc(p.n) + '</h1>' +
        '<p class="pv-d">' + R.esc(p.d) + ' ' +
          (R.weighed(p) ? "Weighed at the counter — the price follows the scale."
                        : "Sold as a sealed unit.") + '</p>' +
        R.shelfLabel(p) +
        '<div class="spec"><span>Sold by</span><span>' + R.esc(p.u) + '</span></div>' +
        (p.size ? '<div class="spec"><span>Pack size</span><span>' + p.size +
                  (/ml|litre|juice|oil|water|milk|lotion|wash|bleach/i.test(p.n) ? " ml" : " g") + '</span></div>' : "") +
        (p.origin ? '<div class="spec"><span>Grown at</span><span>' + R.esc(p.origin) + '</span></div>' : "") +
        '<div class="spec"><span>On the shelf</span><span>' +
          (p.stock === 0 ? "Finished today" : p.stock + " " + (R.weighed(p) ? "kg" : p.u)) + '</span></div>' +
        (days !== null ? '<div class="spec"><span>Best before</span><span>' +
          (days <= 1 ? "tomorrow" : "in " + days + " days") + '</span></div>' : "") +
        '<div class="spec"><span>Delivery</span><span>' + R.esc(R.S.zone.eta) + '</span></div>' +
        (p.was ? '<div class="spec"><span>Was</span><span>' + R.money(p.was) +
                 ' · save ' + R.money(p.was - p.price) + '</span></div>' : "") +
        '<div class="dial" style="margin-top:20px">' +
          '<button data-step="-1" data-slug="' + R.esc(p.slug) + '" aria-label="Less">−</button>' +
          '<span class="dial-v">' + R.esc(R.qtyLabel(p, q)) + '</span>' +
          '<button data-step="1" data-slug="' + R.esc(p.slug) + '" aria-label="More">+</button></div>' +
        '<div class="est"><span>' + (R.weighed(p) ? "Estimated" : "Subtotal") + '</span>' +
          R.money(R.lineTotal(p, q)) + '</div>' +
        '<button class="btn b-accent b-block" data-add="' + R.esc(p.slug) + '" style="margin-top:14px"' +
          (p.stock === 0 ? " disabled" : "") + '>' +
          (p.stock === 0 ? "Finished today" : inCart ? "In basket · add more" : "Add to basket") + '</button>' +
        '<a class="btn b-ghost b-block" href="cart.html" style="margin-top:8px">Go to basket</a>' +
        (R.weighed(p) ? '<p class="note">This line is weighed at the counter. We charge the estimate now and settle ' +
          'the difference — up or down, capped at ' + Math.round(R.SHOP.tolerance * 100) +
          '% — on the same number after weighing.</p>' : "") +
      '</div></div>';
  }
  window.__onCartChange = view;
  view();

  var same = R.CATALOG.filter(function (x) { return x.c === p.c && x.slug !== p.slug; }).slice(0, 6);
  R.byId("related").innerHTML = '<div class="grid">' + same.map(R.card).join("") + '</div>';
  R.byId("relatedTitle").textContent = "More in " + p.c;
}

/* ---------------------------------------------------------------- cart */
function cart() {
  init();
  function view() {
    var list = R.items();
    var host = R.byId("cartView");
    if (!list.length) {
      host.innerHTML = '<div class="empty" style="margin:30px 0">' +
        '<img src="assets/img/scenes/empty.svg" alt="" width="112" height="112">' +
        '<h3>Your basket is empty</h3>' +
        '<p>Seven aisles are open and a few lines are reduced this week.</p>' +
        '<a class="btn b-accent" href="shop.html">Start shopping</a></div>';
      return;
    }
    host.innerHTML = '<div class="split"><div>' +
      '<div class="card"><div class="card-bd">' + R.freeBar() +
        (R.belowMin() ? '<div class="warn">Add ' + R.money(R.S.zone.min - R.subtotal()) +
          ' more to reach the ' + R.money(R.S.zone.min) + ' minimum for ' +
          R.esc(R.S.zone.name.split(" · ")[0]) + '.</div>' : "") +
        list.map(function (i) { return fullLine(i.p, i.q); }).join("") +
      '</div></div>' +
      (R.anyWeighed() ? '<div class="info" style="margin-top:14px"><b>Some of these are weighed at the counter.</b> ' +
        'We charge the estimate now, weigh at the scale, then text you the exact figure and settle the difference ' +
        'on the same number — capped at ' + Math.round(R.SHOP.tolerance * 100) + '% either way.</div>' : "") +
      '<div style="margin-top:18px"><a class="btn b-ghost" href="shop.html">Keep shopping</a></div>' +
    '</div><aside class="sticky"><div class="card"><div class="card-bd">' +
      '<h3 style="margin-bottom:14px">Order summary</h3>' +
      (R.savings() ? '<div class="tot"><span>You saved</span><span class="save-badge">' + R.money(R.savings()) + '</span></div>' : "") +
      '<div class="tot"><span>Subtotal · ' + list.length + ' lines</span><span>' + R.money(R.subtotal()) + '</span></div>' +
      '<div class="tot' + (R.fee() === 0 ? " free" : "") + '"><span>Delivery · ' +
        R.esc(R.S.zone.name.split(" · ")[0]) + '</span><span>' +
        (R.fee() === 0 ? "Free" : R.money(R.fee())) + '</span></div>' +
      '<div class="tot g"><span>Total</span><span>' + R.money(R.total()) + '</span></div>' +
      '<p class="note">Includes ' + R.money(R.vat()) + ' VAT at ' + Math.round(R.SHOP.vatRate * 100) + '%.</p>' +
      '<a class="btn b-accent b-block' + (R.belowMin() ? " is-off" : "") + '" href="checkout.html" style="margin-top:12px">' +
        (R.belowMin() ? "Minimum basket not reached" : "Checkout") + '</a>' +
      '<button class="btn b-ghost b-block" id="waOrder" style="margin-top:8px">Send basket on WhatsApp</button>' +
      '</div></div>' +
      '<div class="card" style="margin-top:14px"><div class="card-bd">' +
        '<h3 style="font-size:16px;margin-bottom:12px">Delivering to</h3>' +
        '<div class="zones">' + zoneList() + '</div></div></div>' +
    '</aside></div>';
  }

  function fullLine(p, q) {
    return '<div class="line" data-slug="' + R.esc(p.slug) + '">' +
      '<a class="ltile" href="product.html?p=' + R.esc(p.slug) + '">' +
        '<img src="' + R.esc(R.productImage(p)) + '" alt="" width="56" height="56" loading="lazy"></a>' +
      '<div><div class="ln"><a href="product.html?p=' + R.esc(p.slug) + '">' + R.esc(p.n) + '</a></div>' +
        '<div class="lm">' + (R.weighed(p) ? R.num(p.price) + "/kg · <em>est.</em>" : R.num(p.price) + " each") + '</div>' +
        '<div class="dial" style="max-width:150px;margin-top:9px">' +
          '<button data-step="-1" data-slug="' + R.esc(p.slug) + '" aria-label="Less">−</button>' +
          '<span class="dial-v">' + R.esc(R.qtyLabel(p, q)) + '</span>' +
          '<button data-step="1" data-slug="' + R.esc(p.slug) + '" aria-label="More">+</button></div></div>' +
      '<div class="lr"><span class="lp">' + R.money(R.lineTotal(p, q)) + '</span>' +
        '<button class="lrm" data-rm="' + R.esc(p.slug) + '">Remove</button></div></div>';
  }

  window.__onCartChange = view;
  window.__onZoneChange = view;
  view();
}

/* ---------------------------------------------------------------- checkout */
function checkout() {
  init();
  var step = 1;
  var host = R.byId("checkoutView");

  function summary() {
    return '<div style="border-top:1.5px solid var(--line);margin-top:22px;padding-top:14px">' +
      '<div class="tot"><span>Subtotal · ' + R.items().length + ' lines</span><span>' + R.money(R.subtotal()) + '</span></div>' +
      '<div class="tot"><span>Delivery</span><span>' + (R.fee() === 0 ? "Free" : R.money(R.fee())) + '</span></div>' +
      '<div class="tot g"><span>Total</span><span>' + R.money(R.total()) + '</span></div></div>';
  }
  function rail() {
    return '<div class="rail">' +
      ['1 · Contact', '2 · Delivery', '3 · Payment'].map(function (l, i) {
        var n = i + 1;
        return '<div class="' + (step === n ? "on" : step > n ? "done" : "") + '">' + l + '</div>';
      }).join("") + '</div>';
  }

  function view() {
    if (!R.items().length && step < 5) {
      host.innerHTML = '<div class="empty"><h3>Your basket is empty</h3>' +
        '<p>Add a few lines and the checkout will open.</p>' +
        '<a class="btn b-accent" href="shop.html">Start shopping</a></div>';
      return;
    }
    var f = R.S.form;
    if (step === 1) {
      host.innerHTML = rail() +
        '<div class="fields two">' +
          '<div class="f"><label for="fName">Your name</label>' +
            '<input id="fName" value="' + R.esc(f.name) + '" placeholder="Nakato Sarah" autocomplete="name">' +
            '<div class="f-e" id="eName"></div></div>' +
          '<div class="f"><label for="fPhone">Phone number</label>' +
            '<input id="fPhone" inputmode="tel" value="' + R.esc(f.phone) + '" placeholder="0771 234 567" autocomplete="tel">' +
            '<div class="f-h">Order updates come here by SMS. This is also your account.</div>' +
            '<div class="f-e" id="ePhone"></div></div>' +
        '</div>' + summary() +
        '<button class="btn b-accent b-block" id="next" style="margin-top:18px">Continue to delivery</button>';
    } else if (step === 2) {
      host.innerHTML = rail() +
        '<div class="f" style="margin-bottom:14px"><label for="fZone">Delivery zone</label>' +
          '<select id="fZone" class="sel" style="width:100%;height:46px">' +
            R.SHOP.zones.map(function (z) {
              return '<option value="' + z.id + '"' + (z.id === R.S.zone.id ? " selected" : "") + '>' +
                R.esc(z.name) + " — " + R.money(z.fee) + '</option>';
            }).join("") + '</select>' +
          '<div class="f-h">' + R.esc(R.S.zone.eta) + ' · minimum basket ' + R.money(R.S.zone.min) + '</div></div>' +
        '<div class="f" style="margin-bottom:14px"><label for="fArea">Area or estate</label>' +
          '<input id="fArea" value="' + R.esc(f.area) + '" placeholder="Tank Hill Road, Muyenga">' +
          '<div class="f-e" id="eArea"></div></div>' +
        '<div class="f" style="margin-bottom:14px"><label for="fLand">Nearest landmark</label>' +
          '<input id="fLand" value="' + R.esc(f.landmark) + '" placeholder="Behind the police post, blue gate">' +
          '<div class="f-h">The rider navigates by landmark and calls when he is close.</div>' +
          '<div class="f-e" id="eLand"></div></div>' +
        '<div class="f"><label for="fNote">Note for the picker</label>' +
          '<textarea id="fNote" placeholder="Cut the beef for stew. Firm avocados. No substitutions on the fish.">' +
          R.esc(f.note) + '</textarea></div>' + summary() +
        '<div style="display:flex;gap:10px;margin-top:18px">' +
          '<button class="btn b-ghost" id="back">Back</button>' +
          '<button class="btn b-accent" id="next" style="flex:1">Continue to payment</button></div>';
    } else if (step === 3) {
      var sel = R.SHOP.payments.filter(function (x) { return x.id === R.S.pay; })[0];
      host.innerHTML = rail() +
        '<div class="pays">' + R.SHOP.payments.map(function (m) {
          return '<button class="pay' + (m.id === R.S.pay ? " on" : "") + '" data-pay="' + m.id + '">' +
            '<img src="' + R.esc(m.mark) + '" alt="">' +
            '<span><span class="pnm">' + R.esc(m.name) + '</span>' +
            '<span class="pnt">' + R.esc(m.note) + '</span></span></button>';
        }).join("") + '</div>' +
        (sel.needsNumber ? '<div class="f"><label for="fPay">' + R.esc(sel.name) + ' number</label>' +
          '<input id="fPay" inputmode="tel" value="' + R.esc(f.phone) + '" placeholder="0771 234 567">' +
          '<div class="f-h">We send a payment request to this number. Approve it on your phone and the order ' +
          'confirms itself.</div></div>' : "") +
        (R.S.pay === "cod" ? '<p class="f-h">The rider carries change. On weighed lines, keep a little extra ready ' +
          'in case the scale reads over.</p>' : "") +
        (R.anyWeighed() ? '<div class="warn" style="margin-top:15px">Your basket has weighed lines. We charge the ' +
          'estimate now and settle the difference after weighing, on the same number.</div>' : "") +
        summary() +
        '<div style="display:flex;gap:10px;margin-top:18px">' +
          '<button class="btn b-ghost" id="back">Back</button>' +
          '<button class="btn b-accent" id="pay" style="flex:1">Pay ' + R.money(R.total()) + '</button></div>';
    } else if (step === 4) {
      host.innerHTML = '<div class="done-b"><div class="pulse"></div>' +
        '<h3 style="margin-top:20px">Check your phone</h3>' +
        '<p>We sent a payment request to ' + R.esc(R.S.form.phone || "your number") +
        '. Approve it and this page confirms itself.</p></div>';
    } else {
      var o = window.__lastOrder;
      host.innerHTML = '<div class="done-b"><h3>Order placed</h3>' +
        '<div class="ref">' + R.esc(o.ref) + '</div>' +
        '<p>Picking starts at ' + R.esc(R.SHOP.cutoff) + '. We text you the final weights, then again when the ' +
        'rider leaves. Delivery ' + R.esc(o.eta.toLowerCase()) + '. Your fiscal receipt travels with the order.</p>' +
        '<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:22px">' +
          '<a class="btn b-accent" href="order.html?ref=' + encodeURIComponent(o.ref) + '">Track this order</a>' +
          '<a class="btn b-ghost" href="shop.html">Back to the aisles</a></div></div>';
    }
  }

  function saveStep() {
    var f = R.S.form, ok = true;
    if (step === 1) {
      f.name = (R.byId("fName").value || "").trim();
      f.phone = (R.byId("fPhone").value || "").trim();
      if (f.name.length < 2) { R.byId("eName").textContent = "Enter the name the rider should ask for."; ok = false; }
      if (f.phone.replace(/\D/g, "").length < 9) { R.byId("ePhone").textContent = "Enter a number we can reach you on."; ok = false; }
    } else if (step === 2) {
      f.area = (R.byId("fArea").value || "").trim();
      f.landmark = (R.byId("fLand").value || "").trim();
      f.note = (R.byId("fNote").value || "").trim();
      if (!f.area) { R.byId("eArea").textContent = "We need an area to route the rider."; ok = false; }
      if (!f.landmark) { R.byId("eLand").textContent = "A landmark gets the rider to your gate."; ok = false; }
    }
    R.save();
    return ok;
  }

  CO_CTX = {
    get step() { return step; }, set step(v) { step = v; },
    view: view, saveStep: saveStep
  };
  if (!checkout._wired) {
    checkout._wired = true;
    document.addEventListener("click", function (e) {
      if (!CO_CTX || document.body.dataset.page !== "checkout") return;
      var view = CO_CTX.view, saveStep = CO_CTX.saveStep;
      var pay = e.target.closest("[data-pay]");
      if (pay) { R.S.pay = pay.dataset.pay; R.save(); view(); return; }
      var id = e.target.id;
      if (id === "next") { if (saveStep()) { CO_CTX.step++; view(); } }
      else if (id === "back") { CO_CTX.step--; view(); }
      else if (id === "pay") {
        var sel = R.SHOP.payments.filter(function (x) { return x.id === R.S.pay; })[0];
        if (sel.needsNumber) {
          var el = R.byId("fPay");
          if (el) R.S.form.phone = (el.value || R.S.form.phone).trim();
          CO_CTX.step = 4; view();
          setTimeout(function () {
            window.__lastOrder = R.placeOrder({ status: "paid" });
            CO_CTX.step = 5; CO_CTX.view();
          }, 2600);
        } else {
          window.__lastOrder = R.placeOrder({ status: R.S.pay === "cod" ? "placed" : "paid" });
          CO_CTX.step = 5; view();
        }
      }
    });
    document.addEventListener("change", function (e) {
      if (!CO_CTX || document.body.dataset.page !== "checkout") return;
      if (e.target.id === "fZone") { R.setZone(e.target.value); CO_CTX.view(); }
    });
  }
  window.__onZoneChange = function () { if (step < 4) view(); };
  view();
}

/* ---------------------------------------------------------------- order tracking */
var FLOW = [
  ["placed",     "Order received",        "We have your list and payment."],
  ["picking",    "Picking in the aisles", "A picker is walking your order."],
  ["weighing",   "At the scale",          "Weighed lines are being confirmed."],
  ["confirmed",  "Weights confirmed",     "We texted you the exact total."],
  ["dispatched", "Out for delivery",      "The rider has your shopping."],
  ["delivered",  "Delivered",             "Signed for at your gate."]
];

function orderPage() {
  init();
  var ref = R.qs("ref");
  var o = R.S.orders.filter(function (x) { return x.ref === ref; })[0] || R.S.orders[0];
  var host = R.byId("orderView");
  if (!o) {
    host.innerHTML = '<div class="empty"><h3>No order to show yet</h3>' +
      '<p>Once you place an order it appears here, with live progress from the shop floor.</p>' +
      '<a class="btn b-accent" href="shop.html">Start shopping</a></div>';
    return;
  }
  // demo progress: an order moves along the flow with the minutes since it was placed
  var mins = (Date.now() - new Date(o.at)) / 60000;
  var idx = o.status === "delivered" ? 5 : Math.min(4, Math.floor(mins / 3));
  host.innerHTML = '<div class="split"><div>' +
    '<div class="card"><div class="card-bd">' +
      '<div class="eyebrow">Order ' + R.esc(o.ref) + '</div>' +
      '<h2 class="sec-t" style="font-size:26px">' + R.esc(FLOW[idx][1]) + '</h2>' +
      '<p class="sec-s" style="margin-bottom:20px">' + R.esc(FLOW[idx][2]) +
        ' Delivery ' + R.esc(o.eta.toLowerCase()) + ' to ' + R.esc(o.zone.split(" · ")[0]) + '.</p>' +
      '<div class="track">' + FLOW.map(function (f, i) {
        return '<div class="tl ' + (i < idx ? "done" : i === idx ? "now" : "") + '">' +
          '<div class="tl-t">' + R.esc(f[1]) + '</div>' +
          '<div class="tl-s">' + (i < idx ? "done" : i === idx ? "in progress" : "pending") + '</div></div>';
      }).join("") + '</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:14px"><div class="card-bd">' +
      '<h3 style="font-size:17px;margin-bottom:12px">What you ordered</h3>' +
      o.lines.map(function (l) {
        return '<div class="tot"><span>' + R.esc(l.n) + ' · ' +
          (l.weighed ? l.q.toFixed(2) + " kg" : l.q + " × " + l.u) + '</span>' +
          '<span>' + R.money(l.price * l.q) + '</span></div>';
      }).join("") +
      '<div class="tot"><span>Delivery</span><span>' + (o.fee ? R.money(o.fee) : "Free") + '</span></div>' +
      '<div class="tot g"><span>Total</span><span>' + R.money(o.total) + '</span></div>' +
      '<p class="note">Fiscal receipt including ' + R.money(o.vat) + ' VAT travels with the order.</p>' +
    '</div></div></div>' +
    '<aside class="sticky"><div class="card"><div class="card-bd">' +
      '<h3 style="font-size:17px;margin-bottom:12px">Delivering to</h3>' +
      '<div class="spec"><span>Name</span><span>' + R.esc(o.customer.name || "—") + '</span></div>' +
      '<div class="spec"><span>Phone</span><span>' + R.esc(o.customer.phone || "—") + '</span></div>' +
      '<div class="spec"><span>Area</span><span>' + R.esc(o.customer.area || "—") + '</span></div>' +
      '<div class="spec"><span>Landmark</span><span>' + R.esc(o.customer.landmark || "—") + '</span></div>' +
      '<div class="spec"><span>Zone</span><span>' + R.esc(o.zone.split(" · ")[0]) + '</span></div>' +
      (o.customer.note ? '<div class="spec"><span>Note</span><span style="max-width:60%">' +
        R.esc(o.customer.note) + '</span></div>' : "") +
      '<a class="btn b-ghost b-block" href="' + R.esc("https://wa.me/" + R.SHOP.whatsapp) + '" style="margin-top:14px">' +
        'Message the shop</a>' +
    '</div></div></aside></div>';
}

/* ---------------------------------------------------------------- account */
function account() {
  init();
  var host = R.byId("accountView");
  var orders = R.S.orders;
  var spend = orders.reduce(function (s, o) { return s + o.total; }, 0);
  var points = Math.floor(spend * R.SHOP.loyaltyRate / 100);
  host.innerHTML = '<div class="split"><div>' +
    '<div class="sec-hd"><div><h2 class="sec-t" style="font-size:26px">Your orders</h2>' +
      '<p class="sec-s">Orders placed on this device. Sign-in with your phone number keeps them on every device.</p></div></div>' +
    (orders.length ? orders.map(function (o) {
      return '<div class="card" style="margin-bottom:12px"><div class="card-bd" style="display:flex;gap:16px;' +
        'align-items:center;flex-wrap:wrap">' +
        '<div style="flex:1;min-width:180px"><div class="mono" style="font-weight:600">' + R.esc(o.ref) + '</div>' +
        '<div style="font-size:12.5px;color:var(--muted);margin-top:3px">' +
          new Date(o.at).toLocaleString(R.SHOP.locale) + ' · ' + o.lines.length + ' lines · ' +
          R.esc(o.zone.split(" · ")[0]) + '</div></div>' +
        '<div class="mono" style="font-weight:600">' + R.money(o.total) + '</div>' +
        '<a class="btn b-ghost b-sm" href="order.html?ref=' + encodeURIComponent(o.ref) + '">Track</a>' +
        '</div></div>';
    }).join("") : '<div class="empty"><h3>No orders yet</h3><p>Your first order will show here with live tracking.</p>' +
      '<a class="btn b-accent" href="shop.html">Start shopping</a></div>') +
  '</div><aside class="sticky">' +
    '<div class="card"><div class="card-bd">' +
      '<h3 style="font-size:17px;margin-bottom:14px">Your details</h3>' +
      '<div class="fields"><div class="f"><label for="aName">Name</label>' +
        '<input id="aName" value="' + R.esc(R.S.form.name) + '" placeholder="Your name"></div>' +
        '<div class="f"><label for="aPhone">Phone</label>' +
        '<input id="aPhone" value="' + R.esc(R.S.form.phone) + '" placeholder="0771 234 567"></div>' +
        '<div class="f"><label for="aArea">Default area</label>' +
        '<input id="aArea" value="' + R.esc(R.S.form.area) + '" placeholder="Tank Hill Road, Muyenga"></div>' +
        '<div class="f"><label for="aLand">Landmark</label>' +
        '<input id="aLand" value="' + R.esc(R.S.form.landmark) + '" placeholder="Blue gate"></div></div>' +
      '<button class="btn b-accent b-block" id="saveMe" style="margin-top:14px">Save details</button>' +
    '</div></div>' +
    '<div class="card" style="margin-top:14px"><div class="card-bd">' +
      '<h3 style="font-size:17px;margin-bottom:12px">Loyalty</h3>' +
      '<div class="tot"><span>Spent with us</span><span>' + R.money(spend) + '</span></div>' +
      '<div class="tot"><span>Points earned</span><span>' + points + '</span></div>' +
      '<p class="note">One point per ' + R.money(100) + ' spent. A hundred points takes ' +
        R.money(10000) + ' off a shop.</p></div></div>' +
    '<div class="card" style="margin-top:14px"><div class="card-bd">' +
      '<h3 style="font-size:17px;margin-bottom:12px">Delivery zone</h3>' +
      '<div class="zones">' + zoneList() + '</div></div></div>' +
  '</aside></div>';

  if (account._wired) return;
  account._wired = true;
  document.addEventListener("click", function (e) {
    if (e.target.id !== "saveMe" || document.body.dataset.page !== "account") return;
    R.S.form.name = R.byId("aName").value.trim();
    R.S.form.phone = R.byId("aPhone").value.trim();
    R.S.form.area = R.byId("aArea").value.trim();
    R.S.form.landmark = R.byId("aLand").value.trim();
    R.save();
    R.toast("Details saved on this device");
  });
}

/* ---------------------------------------------------------------- delivery */
function delivery() {
  init();
  R.byId("zones").innerHTML = zoneList();
  R.byId("faq").innerHTML = R.SHOP.faq.map(function (f) {
    return '<details><summary>' + R.esc(f.q) + '</summary><div class="acc-b">' + R.esc(f.a) + '</div></details>';
  }).join("");
  R.byId("promiseBand").innerHTML = promiseBand();
  window.__onZoneChange = function () {
    R.byId("zoneNote").innerHTML = '<b>' + R.esc(R.S.zone.name) + '</b> — ' + R.esc(R.S.zone.eta) +
      ', ' + R.money(R.S.zone.fee) + ' delivery, minimum basket ' + R.money(R.S.zone.min) +
      '. Free above ' + R.money(R.SHOP.freeOver) + '.';
  };
  window.__onZoneChange();
}

/* ---------------------------------------------------------------- contact */
function contact() {
  init();
  R.byId("hours").innerHTML = R.SHOP.hours.map(function (h) {
    return '<div class="spec"><span>' + R.esc(h.d) + '</span><span>' + R.esc(h.h) + '</span></div>';
  }).join("");
  R.byId("contactForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var f = e.target;
    if (!f.checkValidity()) { f.reportValidity(); return; }
    R.toast("Thank you — we reply within one working day.");
    f.reset();
  });
}

/* ---------------------------------------------------------------- about */
function about() {
  init();
  R.byId("promiseBand").innerHTML = promiseBand();
  R.byId("aboutStats").innerHTML = [
    [R.CATALOG.length, "Lines on the shelf"],
    [R.SHOP.zones.length, "Delivery zones"],
    ["4", "Riders on the road"],
    ["7am", "Doors open, six days"]
  ].map(function (s) {
    return '<div class="stat"><div class="stat-v">' + R.esc(s[0]) + '</div><div class="stat-k">' + R.esc(s[1]) + '</div></div>';
  }).join("");
}

return {
  index: home, shop: shop, deals: deals, product: productPage, cart: cart,
  checkout: checkout, order: orderPage, account: account, delivery: delivery,
  contact: contact, about: about
};
})();
