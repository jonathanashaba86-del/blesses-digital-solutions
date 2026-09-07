/* ============================================================================
   RetailCore OS — back office.

   Reads the same catalogue the storefront reads, so stock, prices and margins
   are one set of numbers. Orders placed on the storefront in this browser turn
   up in the queue here, which is how the demo shows the two halves joined up.

   In production every list is a query behind row-level security; the shapes
   below are the shapes those queries return.
   ============================================================================ */
(function () {
"use strict";

var SHOP = window.SHOP, CAT = window.CATALOG || [], AISLES = window.AISLES || [];
var CUR = SHOP.currency;
var $ = function (s, r) { return (r || document).querySelector(s); };
var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
var money = function (n) { return CUR + " " + Math.round(n).toLocaleString(SHOP.locale); };
var num = function (n) { return Math.round(n).toLocaleString(SHOP.locale); };
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}
function toast(m) {
  var t = $("#toast"); t.textContent = m; t.classList.add("on");
  clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("on"); }, 2600);
}
var prod = function (slug) { for (var i = 0; i < CAT.length; i++) if (CAT[i].slug === slug) return CAT[i]; return null; };
var weighed = function (p) { return p.u === "kg"; };

/* ---------------------------------------------------------------- demo data */
function seedOrders() {
  var mk = function (ref, cust, phone, zone, fee, pay, paid, status, placed, note, lines) {
    return { ref: ref, cust: cust, phone: phone, zone: zone, fee: fee, pay: pay, paid: paid,
             status: status, placed: placed, note: note, lines: lines, channel: "online" };
  };
  return [
    mk("KS-4417", "Nakato Sarah", "0771 234 567", "Muyenga", 5000, "MTN MoMo", true, "new", "09:12",
       "Cut the beef for stew. Firm avocados.",
       [{ s: "beef-choice-cut", q: 1.5 }, { s: "avocado", q: 4 }, { s: "fresh-milk-1l", q: 2 }, { s: "white-loaf", q: 1 }]),
    mk("KS-4418", "Okello Brian", "0752 887 001", "Ntinda", 7000, "Airtel Money", true, "picking", "09:34", "",
       [{ s: "rice-5kg", q: 1 }, { s: "cooking-oil-3l", q: 1 }, { s: "maize-flour-2kg", q: 2 },
        { s: "eggs-tray-of-30", q: 1 }, { s: "detergent-1kg", q: 1 }]),
    mk("KS-4419", "Aine Patricia", "0703 445 219", "Kololo", 6000, "MTN MoMo", true, "weighing", "10:02",
       "No substitutions on the fish, call me instead.",
       [{ s: "nile-perch-fillet", q: 2 }, { s: "tomatoes", q: 1.5 }, { s: "green-pepper", q: 0.5 },
        { s: "fresh-milk-1l", q: 3 }]),
    mk("KS-4420", "Ssebugwawo Ivan", "0782 110 664", "Bugolobi", 5000, "Cash on delivery", false, "confirmed", "10:21", "",
       [{ s: "whole-chicken", q: 2 }, { s: "white-loaf", q: 3 }, { s: "fresh-milk-1l", q: 4 },
        { s: "tissue-10-rolls", q: 1 }]),
    mk("KS-4421", "Nabirye Grace", "0759 302 887", "Kajjansi", 12000, "Visa", true, "dispatched", "08:47",
       "Gate is opposite the mosque.",
       [{ s: "charcoal-sack", q: 1 }, { s: "rice-5kg", q: 2 }, { s: "soda-crate-24", q: 1 }]),
    mk("KS-4416", "Mugisha Denis", "0776 550 123", "Muyenga", 0, "MTN MoMo", true, "delivered", "07:55", "",
       [{ s: "beef-choice-cut", q: 3, w: 3.12 }, { s: "ugandan-coffee-250g", q: 2 },
        { s: "cheddar-200g", q: 2 }, { s: "rice-5kg", q: 3 }, { s: "cooking-oil-3l", q: 2 }])
  ];
}

/* pull anything the shopper placed on the storefront in this browser */
function importStorefrontOrders() {
  var key = "retailcore:" + (SHOP.name || "shop").toLowerCase().replace(/[^a-z0-9]+/g, "-");
  try {
    var raw = JSON.parse(localStorage.getItem(key) || "{}");
    return (raw.orders || []).map(function (o) {
      return {
        ref: o.ref, cust: o.customer.name || "Online customer", phone: o.customer.phone || "—",
        zone: (o.zone || "").split(" · ")[0], fee: o.fee,
        pay: (SHOP.payments.filter(function (p) { return p.id === o.pay; })[0] || {}).name || o.pay,
        paid: o.status === "paid", status: "new",
        placed: new Date(o.at).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }),
        note: o.customer.note || "",
        lines: o.lines.map(function (l) { return { s: l.slug, q: l.q }; }),
        channel: "online"
      };
    });
  } catch (e) { return []; }
}

var ORDERS = importStorefrontOrders().concat(seedOrders());

var EFRIS = [
  { inv: "INV-000841", ref: "KS-4416", amount: 214400, vat: 38592, status: "sent", fdn: "324018877401", at: "08:19" },
  { inv: "INV-000842", ref: "KS-4421", amount: 130000, vat: 23400, status: "sent", fdn: "324018877402", at: "09:03" },
  { inv: "INV-000843", ref: "KS-4420", amount: 99500, vat: 17910, status: "queued", fdn: null, at: "10:24" },
  { inv: "INV-000844", ref: "KS-4419", amount: 88750, vat: 15975, status: "failed", fdn: null, at: "10:31",
    err: "URA endpoint timed out after 30s. Nothing was submitted — safe to retry." }
];

var SUPPLIERS = [
  { id: "s1", n: "Kayunga Growers Co-op", cat: "Fresh produce", lead: "1 day", terms: "Cash on delivery", phone: "0772 111 222", rating: 4.6 },
  { id: "s2", n: "Nsambya Meat Supplies", cat: "Butchery & fish", lead: "1 day", terms: "7 days", phone: "0701 445 887", rating: 4.2 },
  { id: "s3", n: "Jesa Dairy Distributors", cat: "Dairy & eggs", lead: "2 days", terms: "14 days", phone: "0752 990 114", rating: 4.8 },
  { id: "s4", n: "Kampala Wholesale Ltd", cat: "Pantry", lead: "3 days", terms: "30 days", phone: "0414 232 118", rating: 4.0 },
  { id: "s5", n: "Nile Beverages", cat: "Drinks", lead: "2 days", terms: "14 days", phone: "0776 220 331", rating: 4.4 },
  { id: "s6", n: "Homecare Distributors", cat: "Household", lead: "3 days", terms: "30 days", phone: "0393 118 220", rating: 3.9 }
];

var STAFF = [
  { n: "Aisha Nakato", role: "Branch manager", shift: "07:00 – 16:00", on: true, till: "—", sales: 0 },
  { n: "Denis Mugisha", role: "Head picker", shift: "07:00 – 16:00", on: true, till: "—", sales: 0 },
  { n: "Grace Aciro", role: "Cashier", shift: "07:00 – 15:00", on: true, till: "Till 1", sales: 486500 },
  { n: "Ibrahim Ssali", role: "Butcher", shift: "06:00 – 15:00", on: true, till: "—", sales: 0 },
  { n: "Peter Okot", role: "Rider", shift: "12:00 – 20:00", on: true, till: "—", sales: 0 },
  { n: "Sarah Namuli", role: "Cashier", shift: "15:00 – 22:00", on: false, till: "Till 2", sales: 312000 }
];

var CUSTOMERS = [
  { n: "Mugisha Denis", phone: "0776 550 123", zone: "Muyenga", orders: 34, spend: 4120000, last: "today" },
  { n: "Nakato Sarah", phone: "0771 234 567", zone: "Muyenga", orders: 28, spend: 3180000, last: "today" },
  { n: "Nabirye Grace", phone: "0759 302 887", zone: "Kajjansi", orders: 19, spend: 2760000, last: "today" },
  { n: "Aine Patricia", phone: "0703 445 219", zone: "Kololo", orders: 22, spend: 2540000, last: "today" },
  { n: "Okello Brian", phone: "0752 887 001", zone: "Ntinda", orders: 16, spend: 1890000, last: "today" },
  { n: "Ssebugwawo Ivan", phone: "0782 110 664", zone: "Bugolobi", orders: 11, spend: 1240000, last: "today" },
  { n: "Kirabo Joan", phone: "0785 220 664", zone: "Ntinda", orders: 9, spend: 980000, last: "3 days ago" },
  { n: "Wasswa Tom", phone: "0700 118 990", zone: "Entebbe town", orders: 6, spend: 720000, last: "6 days ago" }
];

var WEEK = [
  { d: "Fri", v: 2140000 }, { d: "Sat", v: 3380000 }, { d: "Sun", v: 1620000 },
  { d: "Mon", v: 2010000 }, { d: "Tue", v: 2260000 }, { d: "Wed", v: 2480000 },
  { d: "Thu", v: 1642500, today: true }
];

var STATUS = {
  new: { l: "New", c: "st-new" }, picking: { l: "Picking", c: "st-pick" },
  weighing: { l: "Weighing", c: "st-weigh" }, confirmed: { l: "Confirmed", c: "st-conf" },
  dispatched: { l: "Out for delivery", c: "st-disp" }, delivered: { l: "Delivered", c: "st-done" }
};
var FLOW = ["new", "picking", "weighing", "confirmed", "dispatched", "delivered"];
var NEXT = { new: "picking", picking: "weighing", weighing: "confirmed", confirmed: "dispatched", dispatched: "delivered" };
var NEXT_LABEL = {
  new: "Start picking", picking: "Send to weighing", weighing: "Confirm weights & text customer",
  confirmed: "Dispatch with rider", dispatched: "Mark delivered"
};

/* ---------------------------------------------------------------- order maths */
var lineProd = function (l) { return prod(l.s); };
var weighedLine = function (l) { var p = lineProd(l); return p && weighed(p); };
var lineQty = function (l) { return l.w != null ? l.w : l.q; };
var lineVal = function (l) { var p = lineProd(l); return p ? p.price * lineQty(l) : 0; };
var lineCost = function (l) { var p = lineProd(l); return p ? p.cost * lineQty(l) : 0; };
var live = function (l) { return !l.out; };
var orderSub = function (o) { return o.lines.filter(live).reduce(function (s, l) { return s + lineVal(l); }, 0); };
var orderTot = function (o) { return orderSub(o) + o.fee; };
var orderCost = function (o) { return o.lines.filter(live).reduce(function (s, l) { return s + lineCost(l); }, 0); };
var hasUnweighed = function (o) {
  return o.lines.some(function (l) { return weighedLine(l) && l.w == null && !l.out; });
};

/* ---------------------------------------------------------------- charts */
function barChart(data) {
  var w = 640, h = 190, pad = 26, max = Math.max.apply(null, data.map(function (d) { return d.v; })) * 1.14;
  var bw = (w - pad * 2) / data.length;
  var bars = data.map(function (d, i) {
    var bh = (d.v / max) * (h - pad * 2);
    var x = pad + i * bw + bw * 0.18, y = h - pad - bh, ww = bw * 0.64;
    return '<rect class="bar ' + (d.today ? "today" : "") + '" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) +
      '" width="' + ww.toFixed(1) + '" height="' + Math.max(bh, 2).toFixed(1) + '" rx="2"/>' +
      '<text class="lbl" x="' + (x + ww / 2).toFixed(1) + '" y="' + (h - 9) + '" text-anchor="middle">' + d.d + '</text>' +
      '<text class="lbl" x="' + (x + ww / 2).toFixed(1) + '" y="' + (y - 6).toFixed(1) + '" text-anchor="middle">' +
      (d.v / 1000000).toFixed(1) + 'M</text>';
  }).join("");
  var gl = [0, .25, .5, .75, 1].map(function (f) {
    var y = (h - pad - f * (h - pad * 2)).toFixed(1);
    return '<line class="gl" x1="' + pad + '" y1="' + y + '" x2="' + (w - pad) + '" y2="' + y + '"/>';
  }).join("");
  return '<svg class="chart" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" ' +
    'aria-label="Sales, last seven days">' + gl + bars + '</svg>';
}
function bars(rows) {
  var max = Math.max.apply(null, rows.map(function (r) { return r.v; })) || 1;
  return rows.map(function (r) {
    return '<div class="bar-row"><span class="bar-lbl">' + esc(r.k) + '</span>' +
      '<span class="bar-track"><span class="bar-fill" style="width:' + (r.v / max * 100).toFixed(1) + '%' +
      (r.color ? ";background:" + r.color : "") + '"></span></span>' +
      '<span class="bar-val">' + (r.d != null ? esc(r.d) : num(r.v)) + '</span></div>';
  }).join("");
}

/* ---------------------------------------------------------------- views */
var VIEWS = [
  { id: "today", label: "Today", sub: "Live trading picture for this branch", group: "Trading" },
  { id: "orders", label: "Orders", sub: "Pick, weigh, confirm and dispatch", group: "Trading" },
  { id: "till", label: "Till", sub: "Serve a walk-in customer at the counter", group: "Trading" },
  { id: "stock", label: "Inventory", sub: "Stock on hand, low lines and expiry watch", group: "Stock" },
  { id: "purchasing", label: "Purchasing", sub: "Suppliers and purchase orders", group: "Stock" },
  { id: "customers", label: "Customers", sub: "Who shops with you and what they spend", group: "People" },
  { id: "staff", label: "Staff", sub: "Shifts, roles and till assignments", group: "People" },
  { id: "reports", label: "Reports", sub: "Sales, margin and payment mix", group: "Admin" },
  { id: "efris", label: "EFRIS", sub: "Fiscal invoice submissions to URA", group: "Admin" },
  { id: "settings", label: "Settings", sub: "How this shop is configured", group: "Admin" }
];
var VIEW = "today";

function navBadge(id) {
  if (id === "orders") return ORDERS.filter(function (o) { return o.status !== "delivered"; }).length;
  if (id === "stock") return CAT.filter(function (p) { return p.stock <= 10; }).length;
  if (id === "efris") { var n = EFRIS.filter(function (e) { return e.status !== "sent"; }).length; return n || ""; }
  return "";
}
function renderNav() {
  var html = "", group = "";
  VIEWS.forEach(function (v) {
    if (v.group !== group) { group = v.group; html += '<div class="sep">' + esc(group) + '</div>'; }
    var b = navBadge(v.id);
    html += '<button data-view="' + v.id + '" class="' + (v.id === VIEW ? "on" : "") + '">' + esc(v.label) +
      (b !== "" ? '<span class="n-badge">' + b + '</span>' : "") + '</button>';
  });
  $("#nav").innerHTML = html;
}

/* ---------------- Today ---------------- */
function vToday() {
  var liveOrders = ORDERS.filter(function (o) { return o.status !== "delivered"; });
  var revenue = ORDERS.reduce(function (s, o) { return s + orderTot(o); }, 0);
  var cost = ORDERS.reduce(function (s, o) { return s + orderCost(o); }, 0);
  var margin = revenue ? (revenue - cost) / revenue * 100 : 0;
  var basket = revenue / (ORDERS.length || 1);
  var low = CAT.filter(function (p) { return p.stock <= 10; });
  var expiring = CAT.filter(function (p) { return p.expiry && parseInt(String(p.expiry).replace("+", ""), 10) <= 3; });
  var failed = EFRIS.filter(function (e) { return e.status === "failed"; });

  var catRows = AISLES.map(function (a) {
    return { k: a.c, v: CAT.filter(function (p) { return p.c === a.c; })
      .reduce(function (s, p) { return s + p.price * p.sold; }, 0) };
  }).sort(function (x, y) { return y.v - x.v; })
    .map(function (r) { return { k: r.k, v: r.v, d: num(r.v / 1000) + "k" }; });

  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Sales today", num(revenue), "up", "▲ 9.7% on last Thursday") +
    kpi("Orders", ORDERS.length, "flat", liveOrders.length + " still open") +
    kpi("Average basket", num(basket), "up", "▲ 4.2% this week") +
    kpi("Gross margin", margin.toFixed(1) + "%", margin < 20 ? "down" : "up",
        margin < 20 ? "Below your 20% target" : "On target") +
  '</div>' +
  '<div class="grid g2" style="margin-bottom:14px">' +
    '<div class="card"><div class="card-hd"><div><h3>Sales, last seven days</h3>' +
      '<p>Today runs to the ' + esc(SHOP.cutoff) + ' cut-off, so it reads short until the evening batch closes.</p>' +
      '</div></div><div class="card-bd">' + barChart(WEEK) + '</div></div>' +
    '<div class="card"><div class="card-hd"><h3>Needs attention</h3></div><div class="card-bd flush">' +
      (failed.length ? alertRow("var(--bad)", failed.length + " fiscal invoice failed to submit",
        "URA endpoint timed out. Nothing was sent — safe to retry.", "efris", "Open EFRIS") : "") +
      (expiring.length ? alertRow("var(--warn)", expiring.length + " lines expire within three days",
        expiring.slice(0, 4).map(function (p) { return p.n; }).join(", ") +
        (expiring.length > 4 ? " and " + (expiring.length - 4) + " more" : ""), "stock", "Review") : "") +
      alertRow("var(--warn)", low.length + " lines at or below reorder level",
        low.slice(0, 3).map(function (p) { return p.n; }).join(", ") +
        (low.length > 3 ? " and " + (low.length - 3) + " more" : ""), "purchasing", "Reorder") +
      (ORDERS.some(function (o) { return o.status === "weighing"; })
        ? alertRow("var(--purple)", "Orders waiting at the scale",
            "Customers cannot be charged until weights are confirmed.", "orders", "Open queue") : "") +
    '</div></div>' +
  '</div>' +
  '<div class="grid g2">' +
    '<div class="card"><div class="card-hd"><div><h3>Live order queue</h3><p>Tap a row to open the order.</p></div>' +
      '<button class="btn btn-o btn-sm" data-go="orders">See all</button></div>' +
      '<div class="card-bd flush scrollx"><table><thead><tr><th>Order</th><th>Customer</th><th>Status</th>' +
      '<th class="num">Total</th></tr></thead><tbody>' +
      (liveOrders.length ? liveOrders.map(function (o) {
        return '<tr class="clickable" data-order="' + esc(o.ref) + '">' +
          '<td><span class="mono tw">' + esc(o.ref) + '</span><div class="sub">' + esc(o.placed) + ' · ' + esc(o.zone) + '</div></td>' +
          '<td>' + esc(o.cust) + '<div class="sub">' + esc(o.pay) + (o.paid ? "" : " · unpaid") + '</div></td>' +
          '<td><span class="st ' + STATUS[o.status].c + '">' + STATUS[o.status].l + '</span>' +
            (hasUnweighed(o) ? '<div class="sub">weights pending</div>' : "") + '</td>' +
          '<td class="num">' + num(orderTot(o)) + '</td></tr>';
      }).join("") : '<tr><td colspan="4"><div class="empty-s">Every order is delivered. Good day.</div></td></tr>') +
      '</tbody></table></div></div>' +
    '<div class="card"><div class="card-hd"><h3>Sales by aisle</h3></div>' +
      '<div class="card-bd">' + bars(catRows) + '</div></div>' +
  '</div>';
}
function kpi(k, v, dir, d) {
  return '<div class="card kpi"><div class="kpi-k">' + esc(k) + '</div><div class="kpi-v">' + esc(v) + '</div>' +
    '<div class="kpi-d ' + dir + '">' + esc(d) + '</div></div>';
}
function alertRow(color, title, sub, go, label) {
  return '<div class="alert"><span class="a-dot" style="background:' + color + '"></span>' +
    '<div><div class="a-t">' + esc(title) + '</div><div class="a-s">' + esc(sub) + '</div></div>' +
    '<span class="a-act"><button class="btn btn-o btn-sm" data-go="' + go + '">' + esc(label) + '</button></span></div>';
}

/* ---------------- Orders ---------------- */
var ORDER_FILTER = "open";
function vOrders() {
  var list = ORDER_FILTER === "all" ? ORDERS
    : ORDER_FILTER === "open" ? ORDERS.filter(function (o) { return o.status !== "delivered"; })
    : ORDERS.filter(function (o) { return o.status === ORDER_FILTER; });
  return '' +
  '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px">' +
    '<div class="seg">' +
      '<button data-filter="open" class="' + (ORDER_FILTER === "open" ? "on" : "") + '">Open (' +
        ORDERS.filter(function (o) { return o.status !== "delivered"; }).length + ')</button>' +
      '<button data-filter="weighing" class="' + (ORDER_FILTER === "weighing" ? "on" : "") + '">At the scale (' +
        ORDERS.filter(function (o) { return o.status === "weighing"; }).length + ')</button>' +
      '<button data-filter="all" class="' + (ORDER_FILTER === "all" ? "on" : "") + '">All (' + ORDERS.length + ')</button>' +
    '</div><span class="chip" style="margin-left:auto">Cut-off <b>' + esc(SHOP.cutoff) + '</b></span></div>' +
  '<div class="card"><div class="card-bd flush scrollx"><table><thead><tr>' +
    '<th>Order</th><th>Customer</th><th>Zone</th><th>Payment</th><th>Status</th>' +
    '<th class="num">Lines</th><th class="num">Total</th></tr></thead><tbody>' +
    (list.length ? list.map(function (o) {
      return '<tr class="clickable" data-order="' + esc(o.ref) + '">' +
        '<td><span class="mono tw">' + esc(o.ref) + '</span><div class="sub">placed ' + esc(o.placed) + '</div></td>' +
        '<td>' + esc(o.cust) + '<div class="sub mono">' + esc(o.phone) + '</div></td>' +
        '<td>' + esc(o.zone) + '<div class="sub">' + (o.fee === 0 ? "free delivery" : money(o.fee)) + '</div></td>' +
        '<td>' + esc(o.pay) + '<div class="sub" style="color:' + (o.paid ? "var(--ok)" : "var(--warn)") + '">' +
          (o.paid ? "Paid" : "Due on delivery") + '</div></td>' +
        '<td><span class="st ' + STATUS[o.status].c + '">' + STATUS[o.status].l + '</span>' +
          (hasUnweighed(o) ? '<div class="sub">weights pending</div>' : "") + '</td>' +
        '<td class="num">' + o.lines.length + '</td>' +
        '<td class="num tw">' + num(orderTot(o)) + '</td></tr>';
    }).join("") : '<tr><td colspan="7"><div class="empty-s">Nothing in this filter right now.</div></td></tr>') +
  '</tbody></table></div></div>';
}

/* ---------------- Till (POS) ---------------- */
var TILL = { cart: {}, q: "", tender: "", pay: "cash" };
function vTill() {
  var q = TILL.q.trim().toLowerCase();
  var list = CAT.filter(function (p) {
    return p.stock > 0 && (!q || (p.n + " " + p.c).toLowerCase().indexOf(q) > -1);
  }).slice(0, 40);
  var lines = Object.keys(TILL.cart).map(function (s) { return { p: prod(s), q: TILL.cart[s] }; })
    .filter(function (i) { return i.p; });
  var sub = lines.reduce(function (s, i) { return s + i.p.price * i.q; }, 0);
  var tendered = parseFloat(TILL.tender || "0") || 0;
  var change = tendered - sub;

  return '<div class="grid gpos">' +
    '<div class="card"><div class="card-hd"><div><h3>Ring up an item</h3>' +
      '<p>Scan a barcode or search. Walk-in sales post to the same day book as online orders.</p></div>' +
      '<span class="chip">Till <b>1</b> · Grace Aciro</span></div>' +
      '<div class="card-bd">' +
        '<div class="till-search"><input id="tillQ" placeholder="Scan barcode or type a product name…" ' +
          'value="' + esc(TILL.q) + '" autocomplete="off"></div>' +
        '<div class="till-grid">' + (list.length ? list.map(function (p) {
          return '<button class="till-item" data-till-add="' + esc(p.slug) + '">' +
            '<img src="../' + esc(p.img) + '" alt="" loading="lazy">' +
            '<span><span class="till-n">' + esc(p.n) + '</span>' +
            '<span class="till-p">' + num(p.price) + (weighed(p) ? " /kg" : "") + '</span></span></button>';
        }).join("") : '<div class="empty-s" style="grid-column:1/-1">Nothing matches that.</div>') + '</div>' +
      '</div></div>' +
    '<div class="card"><div class="card-hd"><h3>Current sale</h3>' +
      (lines.length ? '<button class="btn btn-o btn-sm" id="tillClear">Void sale</button>' : "") + '</div>' +
      '<div class="card-bd">' +
        (lines.length ? lines.map(function (i) {
          return '<div class="till-line"><span class="n">' + esc(i.p.n) +
            '<div class="q">' + num(i.p.price) + (weighed(i.p) ? " /kg" : " each") + '</div></span>' +
            '<button class="qbtn" data-till-step="-1" data-slug="' + esc(i.p.slug) + '">−</button>' +
            '<span class="q" style="min-width:52px;text-align:center">' +
              (weighed(i.p) ? i.q.toFixed(2) : i.q) + '</span>' +
            '<button class="qbtn" data-till-step="1" data-slug="' + esc(i.p.slug) + '">+</button>' +
            '<span class="mono" style="min-width:74px;text-align:right;font-weight:600">' +
              num(i.p.price * i.q) + '</span></div>';
        }).join("") : '<div class="empty-s">No items yet. Search or scan to begin.</div>') +
        '<div class="kv" style="margin-top:12px"><span>Items</span><span>' + lines.length + '</span></div>' +
        '<div class="kv"><span>VAT included (' + Math.round(SHOP.vatRate * 100) + '%)</span><span>' +
          num(sub - sub / (1 + SHOP.vatRate)) + '</span></div>' +
        '<div class="kv" style="font-weight:600"><span style="color:var(--ink)">Total</span>' +
          '<span style="font-size:15px">' + money(sub) + '</span></div>' +
        '<div class="tender">' + (TILL.tender ? num(tendered) : "0") + '</div>' +
        '<div class="keypad">' +
          ["1","2","3","4","5","6","7","8","9",".","0","⌫"].map(function (k) {
            return '<button data-key="' + k + '">' + k + '</button>';
          }).join("") + '</div>' +
        (tendered > 0 ? '<div class="kv" style="margin-top:10px"><span>Change due</span>' +
          '<span style="color:' + (change >= 0 ? "var(--ok)" : "var(--bad)") + ';font-size:15px;font-weight:600">' +
          (change >= 0 ? money(change) : "short " + money(-change)) + '</span></div>' : "") +
        '<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">' +
          '<button class="btn btn-o btn-sm" data-till-pay="cash" ' +
            (TILL.pay === "cash" ? 'style="border-color:var(--accent);color:var(--accent)"' : "") + '>Cash</button>' +
          '<button class="btn btn-o btn-sm" data-till-pay="momo" ' +
            (TILL.pay === "momo" ? 'style="border-color:var(--accent);color:var(--accent)"' : "") + '>Mobile money</button>' +
          '<button class="btn btn-o btn-sm" data-till-pay="card" ' +
            (TILL.pay === "card" ? 'style="border-color:var(--accent);color:var(--accent)"' : "") + '>Card</button>' +
        '</div>' +
        '<button class="btn btn-p btn-lg btn-block" id="tillPay" style="margin-top:12px" ' +
          (!lines.length || (TILL.pay === "cash" && change < 0) ? "disabled" : "") + '>' +
          (lines.length ? "Take payment · " + money(sub) : "Nothing to charge") + '</button>' +
        '<p class="hint">A fiscal receipt with the URA QR code prints automatically and the sale drops the ' +
          'stock count on those lines.</p>' +
      '</div></div>' +
  '</div>';
}

/* ---------------- Inventory ---------------- */
function vStock() {
  var low = CAT.filter(function (p) { return p.stock <= 10; })
    .sort(function (a, b) { return a.stock - b.stock; });
  var expiring = CAT.filter(function (p) { return p.expiry; })
    .map(function (p) { return { p: p, days: parseInt(String(p.expiry).replace("+", ""), 10) }; })
    .filter(function (x) { return x.days <= 6; })
    .sort(function (a, b) { return a.days - b.days; });
  var value = CAT.reduce(function (s, p) { return s + p.cost * p.stock; }, 0);
  var dead = CAT.filter(function (p) { return p.sold <= 5; });

  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Stock at cost", num(value), "flat", CAT.length + " lines tracked") +
    '<div class="card kpi"><div class="kpi-k">At reorder level</div>' +
      '<div class="kpi-v" style="color:var(--warn)">' + low.length + '</div>' +
      '<div class="kpi-d flat">Order today to trade tomorrow</div></div>' +
    '<div class="card kpi"><div class="kpi-k">Expiring ≤ 3 days</div>' +
      '<div class="kpi-v" style="color:var(--bad)">' +
      expiring.filter(function (x) { return x.days <= 3; }).length + '</div>' +
      '<div class="kpi-d flat">Discount or write off</div></div>' +
    kpi("Slow movers", dead.length, "flat", "5 or fewer sold this week") +
  '</div>' +
  '<div class="grid g2e" style="margin-bottom:14px">' +
    '<div class="card"><div class="card-hd"><div><h3>Below reorder level</h3>' +
      '<p>Online listings hide automatically at zero, so these are the lines you are about to lose sales on.</p></div>' +
      '<button class="btn btn-p btn-sm" data-go="purchasing">Draft purchase order</button></div>' +
      '<div class="card-bd flush scrollx"><table><thead><tr><th>Line</th><th class="num">On hand</th>' +
      '<th class="num">Sold 7d</th><th class="num">Suggest</th></tr></thead><tbody>' +
      low.map(function (p) {
        return '<tr><td><div style="display:flex;gap:9px;align-items:center">' +
          '<img class="thumb" src="../' + esc(p.img) + '" alt="" loading="lazy">' +
          '<span>' + esc(p.n) + '<div class="sub">' + esc(p.c) + '</div></span></div></td>' +
          '<td class="num" style="color:' + (p.stock <= 5 ? "var(--bad)" : "var(--warn)") + '">' +
            p.stock + ' ' + esc(p.u) + '</td>' +
          '<td class="num">' + p.sold + '</td>' +
          '<td class="num tw">' + Math.max(20, Math.ceil(p.sold * 1.4)) + '</td></tr>';
      }).join("") + '</tbody></table></div></div>' +
    '<div class="card"><div class="card-hd"><div><h3>Expiry watch</h3>' +
      '<p>Picked first-expired-first-out. Anything under three days should be marked down this morning.</p></div></div>' +
      '<div class="card-bd flush scrollx"><table><thead><tr><th>Line</th><th class="num">Expires</th>' +
      '<th class="num">At risk</th><th></th></tr></thead><tbody>' +
      (expiring.length ? expiring.map(function (x) {
        return '<tr><td>' + esc(x.p.n) + '<div class="sub">' + esc(x.p.c) + '</div></td>' +
          '<td class="num" style="color:' + (x.days <= 1 ? "var(--bad)" : x.days <= 3 ? "var(--warn)" : "var(--slate)") + '">' +
            (x.days <= 0 ? "today" : x.days === 1 ? "tomorrow" : "in " + x.days + " days") + '</td>' +
          '<td class="num">' + num(x.p.cost * x.p.stock) + '</td>' +
          '<td class="num"><button class="btn btn-o btn-sm" data-markdown="' + esc(x.p.slug) + '">Mark down</button></td></tr>';
      }).join("") : '<tr><td colspan="4"><div class="empty-s">Nothing close to date.</div></td></tr>') +
      '</tbody></table></div></div>' +
  '</div>' +
  '<div class="card"><div class="card-hd"><div><h3>All stock</h3>' +
    '<p>Margin is calculated per line from cost against shelf price.</p></div>' +
    '<div style="display:flex;gap:8px"><button class="btn btn-o btn-sm" id="expStock">Export to Excel</button>' +
    '<button class="btn btn-p btn-sm" id="addLine">Add a line</button></div></div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Line</th><th>Aisle</th><th class="num">On hand</th>' +
    '<th class="num">Cost</th><th class="num">Shelf</th><th class="num">Margin</th><th class="num">Sold 7d</th>' +
    '<th class="num">Value</th></tr></thead><tbody>' +
    CAT.map(function (p) {
      var m = (p.price - p.cost) / p.price * 100;
      return '<tr><td><div style="display:flex;gap:9px;align-items:center">' +
        '<img class="thumb" src="../' + esc(p.img) + '" alt="" loading="lazy">' +
        '<span class="tw">' + esc(p.n) + '</span></div></td>' +
        '<td>' + esc(p.c) + '</td>' +
        '<td class="num" style="color:' + (p.stock <= 10 ? "var(--warn)" : "inherit") + '">' + p.stock + ' ' + esc(p.u) + '</td>' +
        '<td class="num">' + num(p.cost) + '</td><td class="num">' + num(p.price) + '</td>' +
        '<td class="num" style="color:' + (m < 15 ? "var(--bad)" : m < 22 ? "var(--warn)" : "var(--ok)") + '">' +
          m.toFixed(1) + '%</td>' +
        '<td class="num">' + p.sold + '</td>' +
        '<td class="num">' + num(p.cost * p.stock) + '</td></tr>';
    }).join("") + '</tbody></table></div></div>';
}

/* ---------------- Purchasing ---------------- */
function vPurchasing() {
  var low = CAT.filter(function (p) { return p.stock <= 10; });
  var byAisle = {};
  low.forEach(function (p) { (byAisle[p.c] = byAisle[p.c] || []).push(p); });
  var poValue = low.reduce(function (s, p) { return s + p.cost * Math.max(20, Math.ceil(p.sold * 1.4)); }, 0);

  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Suppliers", SUPPLIERS.length, "flat", "Across " + Object.keys(byAisle).length + " departments") +
    kpi("Lines to reorder", low.length, "flat", "At or below reorder level") +
    kpi("Draft PO value", num(poValue), "flat", "At cost, before any discount") +
    kpi("Average lead time", "2 days", "flat", "Order today, trade Thursday") +
  '</div>' +
  '<div class="card" style="margin-bottom:14px"><div class="card-hd"><div><h3>Suggested purchase orders</h3>' +
    '<p>Grouped by the supplier who normally carries that department. Quantities cover the coming week ' +
    'at the current rate of sale.</p></div>' +
    '<button class="btn btn-p btn-sm" id="sendPOs">Send all to suppliers</button></div>' +
    '<div class="card-bd flush">' +
    (Object.keys(byAisle).length ? Object.keys(byAisle).map(function (aisle) {
      var sup = SUPPLIERS.filter(function (s) { return s.cat === aisle; })[0] || SUPPLIERS[3];
      var lines = byAisle[aisle];
      var val = lines.reduce(function (s, p) { return s + p.cost * Math.max(20, Math.ceil(p.sold * 1.4)); }, 0);
      return '<div style="padding:14px 16px;border-bottom:1px solid var(--line-2)">' +
        '<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:10px">' +
          '<div><div style="font-weight:600;font-size:13.5px">' + esc(sup.n) + '</div>' +
          '<div class="sub">' + esc(aisle) + ' · lead ' + esc(sup.lead) + ' · terms ' + esc(sup.terms) + '</div></div>' +
          '<span class="chip" style="margin-left:auto">' + money(val) + '</span>' +
          '<button class="btn btn-o btn-sm" data-po="' + esc(sup.id) + '">Send PO</button></div>' +
        '<div class="scrollx"><table><thead><tr><th>Line</th><th class="num">On hand</th>' +
        '<th class="num">Order</th><th class="num">Cost each</th><th class="num">Line total</th></tr></thead><tbody>' +
        lines.map(function (p) {
          var qty = Math.max(20, Math.ceil(p.sold * 1.4));
          return '<tr><td>' + esc(p.n) + '</td><td class="num">' + p.stock + '</td>' +
            '<td class="num tw">' + qty + ' ' + esc(p.u) + '</td>' +
            '<td class="num">' + num(p.cost) + '</td><td class="num">' + num(p.cost * qty) + '</td></tr>';
        }).join("") + '</tbody></table></div></div>';
    }).join("") : '<div class="empty-s">Nothing needs reordering today.</div>') +
  '</div></div>' +
  '<div class="card"><div class="card-hd"><div><h3>Suppliers</h3>' +
    '<p>Rating is your own — delivery reliability against what was ordered.</p></div>' +
    '<button class="btn btn-o btn-sm" id="addSupplier">Add supplier</button></div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Supplier</th><th>Department</th><th>Lead time</th>' +
    '<th>Terms</th><th>Phone</th><th class="num">Rating</th></tr></thead><tbody>' +
    SUPPLIERS.map(function (s) {
      return '<tr><td class="tw">' + esc(s.n) + '</td><td>' + esc(s.cat) + '</td><td>' + esc(s.lead) + '</td>' +
        '<td>' + esc(s.terms) + '</td><td class="mono" style="font-size:12px">' + esc(s.phone) + '</td>' +
        '<td class="num" style="color:' + (s.rating >= 4.5 ? "var(--ok)" : s.rating >= 4 ? "var(--warn)" : "var(--bad)") +
        '">' + s.rating.toFixed(1) + '</td></tr>';
    }).join("") + '</tbody></table></div></div>';
}

/* ---------------- Customers ---------------- */
function vCustomers() {
  var spend = CUSTOMERS.reduce(function (s, c) { return s + c.spend; }, 0);
  var repeat = CUSTOMERS.filter(function (c) { return c.orders > 5; }).length;
  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Customers", CUSTOMERS.length, "flat", "With at least one order") +
    kpi("Repeat customers", Math.round(repeat / CUSTOMERS.length * 100) + "%", "up", "More than five orders") +
    kpi("Lifetime value", num(spend / CUSTOMERS.length), "up", "Average across the book") +
    kpi("Ordered today", CUSTOMERS.filter(function (c) { return c.last === "today"; }).length, "flat", "Active this trading day") +
  '</div>' +
  '<div class="card"><div class="card-hd"><div><h3>Customer book</h3>' +
    '<p>Sorted by what they have spent with you. Phone number is the account.</p></div>' +
    '<button class="btn btn-o btn-sm" id="expCust">Export to Excel</button></div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Customer</th><th>Phone</th><th>Zone</th>' +
    '<th class="num">Orders</th><th class="num">Spent</th><th class="num">Average</th><th>Last order</th>' +
    '</tr></thead><tbody>' +
    CUSTOMERS.slice().sort(function (a, b) { return b.spend - a.spend; }).map(function (c) {
      return '<tr><td class="tw">' + esc(c.n) + '</td>' +
        '<td class="mono" style="font-size:12px">' + esc(c.phone) + '</td><td>' + esc(c.zone) + '</td>' +
        '<td class="num">' + c.orders + '</td><td class="num tw">' + num(c.spend) + '</td>' +
        '<td class="num">' + num(c.spend / c.orders) + '</td>' +
        '<td><span class="sub" style="margin:0">' + esc(c.last) + '</span></td></tr>';
    }).join("") + '</tbody></table></div></div>';
}

/* ---------------- Staff ---------------- */
function vStaff() {
  var onNow = STAFF.filter(function (s) { return s.on; }).length;
  var tillSales = STAFF.reduce(function (s, x) { return s + x.sales; }, 0);
  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("On shift now", onNow, "flat", "Of " + STAFF.length + " on the rota") +
    kpi("Till takings", num(tillSales), "up", "Walk-in sales today") +
    kpi("Tills open", STAFF.filter(function (s) { return s.till !== "—" && s.on; }).length, "flat", "Counter positions live") +
    kpi("Riders out", STAFF.filter(function (s) { return s.role === "Rider" && s.on; }).length, "flat", "On the road now") +
  '</div>' +
  '<div class="card"><div class="card-hd"><div><h3>Today\'s rota</h3>' +
    '<p>Who is on, what they are on, and what has gone through their till.</p></div>' +
    '<button class="btn btn-p btn-sm" id="addStaff">Add someone</button></div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Name</th><th>Role</th><th>Shift</th><th>Till</th>' +
    '<th class="num">Takings</th><th>Status</th></tr></thead><tbody>' +
    STAFF.map(function (s) {
      return '<tr><td class="tw">' + esc(s.n) + '</td><td>' + esc(s.role) + '</td>' +
        '<td class="mono" style="font-size:12px">' + esc(s.shift) + '</td><td>' + esc(s.till) + '</td>' +
        '<td class="num">' + (s.sales ? num(s.sales) : "—") + '</td>' +
        '<td><span class="st ' + (s.on ? "st-conf" : "st-done") + '">' + (s.on ? "on shift" : "off") + '</span></td></tr>';
    }).join("") + '</tbody></table></div></div>' +
  '<div class="card" style="margin-top:14px"><div class="card-hd"><div><h3>Permissions</h3>' +
    '<p>What each role can reach. Cashiers never see cost prices or margin.</p></div></div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Capability</th><th>Manager</th><th>Cashier</th>' +
    '<th>Picker</th><th>Rider</th></tr></thead><tbody>' +
    [["Take payment at the till", 1, 1, 0, 0],
     ["Pick and weigh orders", 1, 0, 1, 0],
     ["See cost price and margin", 1, 0, 0, 0],
     ["Change shelf prices", 1, 0, 0, 0],
     ["Raise a purchase order", 1, 0, 0, 0],
     ["Mark an order delivered", 1, 0, 0, 1],
     ["Refund or void a sale", 1, 0, 0, 0],
     ["Export reports", 1, 0, 0, 0]].map(function (r) {
      return '<tr><td>' + esc(r[0]) + '</td>' + r.slice(1).map(function (v) {
        return '<td style="color:' + (v ? "var(--ok)" : "var(--muted)") + '">' + (v ? "✓" : "—") + '</td>';
      }).join("") + '</tr>';
    }).join("") + '</tbody></table></div></div>';
}

/* ---------------- Reports ---------------- */
function vReports() {
  var rev = CAT.reduce(function (s, p) { return s + p.price * p.sold; }, 0);
  var cost = CAT.reduce(function (s, p) { return s + p.cost * p.sold; }, 0);
  var top = CAT.slice().sort(function (a, b) { return b.price * b.sold - a.price * a.sold; }).slice(0, 8)
    .map(function (p) { return { k: p.n, v: p.price * p.sold, d: num(p.price * p.sold / 1000) + "k" }; });
  var marg = CAT.map(function (p) {
    var m = (p.price - p.cost) / p.price * 100;
    return { k: p.n, v: m, d: m.toFixed(1) + "%" };
  }).sort(function (a, b) { return a.v - b.v; }).slice(0, 8);
  var pays = [{ k: "MTN Mobile Money", v: 54, d: "54%" }, { k: "Airtel Money", v: 22, d: "22%" },
              { k: "Cash on delivery", v: 16, d: "16%" }, { k: "Card", v: 8, d: "8%" }];
  return '' +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Revenue, 7 days", num(rev), "up", "▲ 6.1%") +
    kpi("Gross profit", num(rev - cost), "up", "▲ 4.4%") +
    kpi("Blended margin", ((rev - cost) / rev * 100).toFixed(1) + "%", "flat", "Target 22%") +
    kpi("Delivery cost / order", "4,180", "down", "▼ margin on small baskets") +
  '</div>' +
  '<div class="grid g2e" style="margin-bottom:14px">' +
    '<div class="card"><div class="card-hd"><div><h3>Top lines by revenue</h3><p>Seven days, this branch.</p></div></div>' +
      '<div class="card-bd">' + bars(top) + '</div></div>' +
    '<div class="card"><div class="card-hd"><div><h3>Thinnest margins</h3>' +
      '<p>These lines earn least per shilling sold. Renegotiate supply or reprice.</p></div></div>' +
      '<div class="card-bd">' + bars(marg.map(function (r) {
        return { k: r.k, v: r.v, d: r.d, color: r.v < 15 ? "var(--bad)" : r.v < 22 ? "var(--warn)" : "var(--ok)" };
      })) + '</div></div>' +
  '</div>' +
  '<div class="grid g2e">' +
    '<div class="card"><div class="card-hd"><div><h3>Payment mix</h3>' +
      '<p>Mobile money carries three quarters of takings — gateway fees land straight on margin.</p></div></div>' +
      '<div class="card-bd">' + bars(pays) + '</div></div>' +
    '<div class="card"><div class="card-hd"><div><h3>Operations</h3><p>Where orders lose time and money.</p></div>' +
      '<button class="btn btn-o btn-sm" id="expRep">Export to Excel</button></div><div class="card-bd">' +
      [["Average pick time", "18 min"], ["Substitution rate", "7.4%"], ["Weight variance vs estimate", "+3.1%"],
       ["Delivered inside promised window", "91%"], ["Cancelled after picking", "2.2%"],
       ["Abandoned baskets recovered by SMS", "14%"], ["Repeat order rate, 30 days", "62%"]].map(function (r) {
        return '<div class="kv"><span>' + esc(r[0]) + '</span><span>' + esc(r[1]) + '</span></div>';
      }).join("") + '</div></div>' +
  '</div>';
}

/* ---------------- EFRIS ---------------- */
function vEfris() {
  var failed = EFRIS.filter(function (e) { return e.status === "failed"; });
  var queued = EFRIS.filter(function (e) { return e.status === "queued"; });
  return '' +
  (failed.length ? '<div class="banner b-bad"><b>' + failed.length + ' submission failed.</b> ' +
    esc(failed[0].err) + ' Sales are not blocked — the queue retries on its own, and you can force a retry below.</div>' : "") +
  (!failed.length && !queued.length ? '<div class="banner b-ok"><b>All invoices submitted.</b> ' +
    'Every order today has a URA fiscal document number.</div>' : "") +
  '<div class="grid g4" style="margin-bottom:14px">' +
    kpi("Submitted today", EFRIS.filter(function (e) { return e.status === "sent"; }).length, "up", "FDN issued") +
    '<div class="card kpi"><div class="kpi-k">In queue</div><div class="kpi-v" style="color:' +
      (queued.length ? "var(--warn)" : "inherit") + '">' + queued.length + '</div>' +
      '<div class="kpi-d flat">Retries every 60s</div></div>' +
    '<div class="card kpi"><div class="kpi-k">Failed</div><div class="kpi-v" style="color:' +
      (failed.length ? "var(--bad)" : "inherit") + '">' + failed.length + '</div>' +
      '<div class="kpi-d flat">Needs a manual retry</div></div>' +
    kpi("VAT captured today", num(EFRIS.reduce(function (s, e) { return s + e.vat; }, 0)), "flat",
        Math.round(SHOP.vatRate * 100) + "% standard rate") +
  '</div>' +
  '<div class="card"><div class="card-hd"><div><h3>Submission queue</h3>' +
    '<p>Every invoice is transmitted to URA through the EFRIS API. The fiscal document number prints on the ' +
    'customer receipt as a QR code.</p></div>' +
    (failed.length ? '<button class="btn btn-p btn-sm" id="retryAll">Retry failed</button>' : "") + '</div>' +
    '<div class="card-bd flush scrollx"><table><thead><tr><th>Invoice</th><th>Order</th><th class="num">Amount</th>' +
    '<th class="num">VAT</th><th>FDN</th><th>Status</th><th></th></tr></thead><tbody>' +
    EFRIS.map(function (e) {
      return '<tr><td><span class="mono tw">' + esc(e.inv) + '</span><div class="sub">' + esc(e.at) + '</div></td>' +
        '<td class="mono">' + esc(e.ref) + '</td><td class="num">' + num(e.amount) + '</td>' +
        '<td class="num">' + num(e.vat) + '</td>' +
        '<td class="mono" style="font-size:12px;color:' + (e.fdn ? "var(--ink)" : "var(--muted)") + '">' +
          esc(e.fdn || "—") + '</td>' +
        '<td><span class="st ' + (e.status === "sent" ? "st-conf" : e.status === "queued" ? "st-pick" : "st-fail") +
          '">' + esc(e.status) + '</span></td>' +
        '<td class="num">' + (e.status !== "sent"
          ? '<button class="btn btn-o btn-sm" data-retry="' + esc(e.inv) + '">Retry</button>' : "") + '</td></tr>';
    }).join("") + '</tbody></table></div></div>';
}

/* ---------------- Settings ---------------- */
function vSettings() {
  return '' +
  '<div class="banner b-info">These values come from <b>assets/js/config.js</b>. Change them there and the ' +
    'storefront and this back office both follow — name, colours, zones, fees, payment methods and hours.</div>' +
  '<div class="grid g2e" style="margin-bottom:14px">' +
    '<div class="card"><div class="card-hd"><h3>Shop identity</h3></div><div class="card-bd">' +
      '<div class="fld-row two"><div class="fld"><label>Trading name</label>' +
        '<input value="' + esc(SHOP.name) + '"></div>' +
        '<div class="fld"><label>Legal name</label><input value="' + esc(SHOP.legalName) + '"></div></div>' +
      '<div class="fld"><label>Strapline</label><input value="' + esc(SHOP.strapline) + '"></div>' +
      '<div class="fld-row two"><div class="fld"><label>Phone</label><input value="' + esc(SHOP.phone) + '"></div>' +
        '<div class="fld"><label>Email</label><input value="' + esc(SHOP.email) + '"></div></div>' +
      '<div class="fld"><label>Address</label><input value="' + esc(SHOP.address) + '"></div>' +
      '<div class="fld"><label>Theme</label><select id="themeSel">' +
        '<option value="superstore"' + (SHOP.theme === "superstore" ? " selected" : "") + '>Superstore — cobalt</option>' +
        '<option value="market"' + (SHOP.theme === "market" ? " selected" : "") + '>Market — crimson</option>' +
        '</select></div>' +
      '<button class="btn btn-p" id="saveSettings">Save identity</button></div></div>' +
    '<div class="card"><div class="card-hd"><h3>Trading rules</h3></div><div class="card-bd">' +
      '<div class="fld-row two"><div class="fld"><label>Currency</label><input value="' + esc(SHOP.currency) + '"></div>' +
        '<div class="fld"><label>VAT rate</label><input value="' + Math.round(SHOP.vatRate * 100) + '%"></div></div>' +
      '<div class="fld-row two"><div class="fld"><label>Free delivery over</label>' +
        '<input value="' + num(SHOP.freeOver) + '"></div>' +
        '<div class="fld"><label>Weight tolerance</label><input value="' +
          Math.round(SHOP.tolerance * 100) + '%"></div></div>' +
      '<div class="fld-row two"><div class="fld"><label>Same-day cut-off</label>' +
        '<input value="' + esc(SHOP.cutoff) + '"></div>' +
        '<div class="fld"><label>Delivery window</label><input value="' + esc(SHOP.windowText) + '"></div></div>' +
      '<div class="fld"><label>Loyalty</label><input value="1 point per ' + num(100) + ' spent"></div>' +
      '<button class="btn btn-p" id="saveRules">Save rules</button></div></div>' +
  '</div>' +
  '<div class="grid g2e">' +
    '<div class="card"><div class="card-hd"><div><h3>Delivery zones</h3>' +
      '<p>Fee, minimum basket and promised window per zone.</p></div>' +
      '<button class="btn btn-o btn-sm" id="addZone">Add zone</button></div>' +
      '<div class="card-bd flush scrollx"><table><thead><tr><th>Zone</th><th class="num">Fee</th>' +
      '<th class="num">Minimum</th><th>Window</th></tr></thead><tbody>' +
      SHOP.zones.map(function (z) {
        return '<tr><td>' + esc(z.name) + '<div class="sub">' + esc(z.area) + '</div></td>' +
          '<td class="num">' + num(z.fee) + '</td><td class="num">' + num(z.min) + '</td>' +
          '<td class="mono" style="font-size:12px">' + esc(z.eta) + '</td></tr>';
      }).join("") + '</tbody></table></div></div>' +
    '<div class="card"><div class="card-hd"><div><h3>Payment methods</h3>' +
      '<p>Turn a method off here and it disappears from checkout.</p></div></div>' +
      '<div class="card-bd flush scrollx"><table><thead><tr><th></th><th>Method</th><th>Behaviour</th>' +
      '<th class="num">Status</th></tr></thead><tbody>' +
      SHOP.payments.map(function (p) {
        return '<tr><td style="width:60px"><img src="../' + esc(p.mark) + '" alt="" width="44" height="28" ' +
          'style="border-radius:3px"></td><td class="tw">' + esc(p.name) + '</td>' +
          '<td class="sub" style="margin:0">' + esc(p.note) + '</td>' +
          '<td class="num"><span class="st st-conf">on</span></td></tr>';
      }).join("") + '</tbody></table></div></div>' +
  '</div>';
}

/* ---------------------------------------------------------------- render */
function render() {
  var v = VIEWS.filter(function (x) { return x.id === VIEW; })[0];
  $("#vTitle").textContent = v.label;
  $("#vSub").textContent = v.sub;
  var map = { today: vToday, orders: vOrders, till: vTill, stock: vStock, purchasing: vPurchasing,
              customers: vCustomers, staff: vStaff, reports: vReports, efris: vEfris, settings: vSettings };
  $("#view").innerHTML = map[VIEW]();
  renderNav();
  if (VIEW === "till") {
    var t = $("#tillQ");
    if (t) { t.focus(); t.setSelectionRange(t.value.length, t.value.length); }
  }
}

/* ---------------------------------------------------------------- order detail */
var OPEN = null;
function openOrder(ref) {
  OPEN = ORDERS.filter(function (o) { return o.ref === ref; })[0];
  if (!OPEN) return;
  $("#dRef").textContent = OPEN.ref;
  $("#dCust").textContent = OPEN.cust + " · " + OPEN.phone;
  renderDetail();
  $("#detail").classList.add("on");
  $("#scrim").classList.add("on");
}
function closeDetail() {
  $("#detail").classList.remove("on");
  $("#scrim").classList.remove("on");
  OPEN = null;
}
function renderDetail() {
  var o = OPEN, idx = FLOW.indexOf(o.status), pending = hasUnweighed(o);
  var estTotal = o.lines.filter(live).reduce(function (s, l) {
    var p = lineProd(l); return s + (p ? p.price * l.q : 0);
  }, 0) + o.fee;
  var diff = orderTot(o) - estTotal;

  $("#dBody").innerHTML = '' +
    (o.status === "weighing" && pending ? '<div class="banner b-warn"><b>Weights not confirmed.</b> ' +
      'Enter the scale reading for each weighed line. The customer is charged the estimate until you confirm, ' +
      'then the difference settles on their mobile money.</div>' : "") +
    (o.note ? '<div class="banner b-warn"><b>Note from the customer:</b> ' + esc(o.note) + '</div>' : "") +
    '<div class="sect-t">Lines</div>' +
    o.lines.map(function (l, i) {
      var p = lineProd(l);
      if (!p) return "";
      var w = weighed(p), est = p.price * l.q, act = lineVal(l), d = act - est;
      return '<div class="oline" style="' + (l.out ? "opacity:.6" : "") + '">' +
        '<div class="ol-top"><div><div class="ol-n">' + esc(p.n) + '</div>' +
          '<div class="ol-m">' + (w ? "ordered " + l.q.toFixed(2) + " kg × " + num(p.price) + "/kg"
                                    : l.q + " × " + num(p.price) + " " + esc(p.u)) + '</div>' +
          (l.out ? '<span class="pill-out">Out of stock — refunded</span>' : "") +
          (l.sub ? '<span class="pill-out pill-sub">Substituted: ' + esc(l.sub) + '</span>' : "") +
        '</div><div><span class="ol-p">' + (l.out ? "—" : num(act)) + '</span>' +
          (w && l.w != null && d !== 0 ? '<span class="ol-was">est ' + num(est) + '</span>' : "") + '</div></div>' +
        (w && !l.out ? '<div class="weigh"><label for="w' + i + '">Scale</label>' +
          '<input id="w' + i + '" type="number" step="0.01" min="0" data-weigh="' + i + '" ' +
          'value="' + (l.w != null ? l.w : "") + '" placeholder="' + l.q.toFixed(2) + '">' +
          '<span style="font-family:var(--mono);font-size:12px;color:var(--muted)">kg</span>' +
          '<span class="delta" style="color:' + (d > 0 ? "var(--warn)" : d < 0 ? "var(--ok)" : "var(--muted)") + '">' +
            (l.w != null ? (d > 0 ? "+" : "") + num(d) : "awaiting scale") + '</span></div>' : "") +
        ((o.status === "picking" || o.status === "weighing")
          ? (l.out ? '<div class="ol-act"><button class="btn btn-o btn-sm" data-out="' + i + '">Restore — back in stock</button></div>'
                   : '<div class="ol-act"><button class="btn btn-o btn-sm" data-out="' + i + '">Mark out of stock</button>' +
                     '<button class="btn btn-o btn-sm" data-sub="' + i + '">Offer substitute</button></div>') : "") +
      '</div>';
    }).join("") +
    '<div class="sect-t">Totals</div><div class="card"><div class="card-bd">' +
      '<div class="kv"><span>Goods</span><span>' + num(orderSub(o)) + '</span></div>' +
      '<div class="kv"><span>Delivery · ' + esc(o.zone) + '</span><span>' +
        (o.fee === 0 ? "Free" : num(o.fee)) + '</span></div>' +
      (diff !== 0 ? '<div class="kv"><span>Weight adjustment</span><span style="color:' +
        (diff > 0 ? "var(--warn)" : "var(--ok)") + '">' + (diff > 0 ? "+" : "") + num(diff) + '</span></div>' : "") +
      '<div class="kv" style="font-weight:600"><span style="color:var(--ink)">Total</span>' +
        '<span style="font-size:14px">' + money(orderTot(o)) + '</span></div>' +
      '<div class="kv"><span>Cost of goods</span><span>' + num(orderCost(o)) + '</span></div>' +
      '<div class="kv"><span>Margin on this order</span><span style="color:var(--ok)">' +
        (orderSub(o) ? ((orderSub(o) - orderCost(o)) / orderSub(o) * 100).toFixed(1) : "0.0") + '%</span></div>' +
    '</div></div>' +
    '<div class="sect-t">Payment</div><div class="card"><div class="card-bd">' +
      '<div class="kv"><span>Method</span><span>' + esc(o.pay) + '</span></div>' +
      '<div class="kv"><span>Status</span><span style="color:' + (o.paid ? "var(--ok)" : "var(--warn)") + '">' +
        (o.paid ? "Verified by webhook" : "Due on delivery") + '</span></div>' +
      '<div class="kv"><span>Channel</span><span>' + esc(o.channel || "online") + '</span></div>' +
    '</div></div>' +
    '<div class="sect-t">Progress</div><div class="timeline">' +
      FLOW.map(function (s, i) {
        return '<div class="tl ' + (i < idx ? "done" : i === idx ? "now" : "") + '">' +
          '<div class="tl-t">' + STATUS[s].l + '</div>' +
          '<div class="tl-s">' + (i < idx ? "done" : i === idx ? "in progress" : "pending") + '</div></div>';
      }).join("") + '</div>';

  var blocked = o.status === "weighing" && pending;
  $("#dFoot").innerHTML = o.status === "delivered"
    ? '<button class="btn btn-o" id="dClose" style="flex:1">Close</button>'
    : '<button class="btn btn-o" id="dClose">Close</button>' +
      '<button class="btn btn-p" id="advance" style="flex:1"' + (blocked ? " disabled" : "") + '>' +
      (blocked ? "Confirm all weights first" : NEXT_LABEL[o.status]) + '</button>';
}

/* ---------------------------------------------------------------- events */
document.addEventListener("click", function (e) {
  var t = e.target, hit = function (s) { return t.closest ? t.closest(s) : null; };

  var nv = hit("[data-view]"); if (nv) { VIEW = nv.dataset.view; render(); return; }
  var go = hit("[data-go]");   if (go) { VIEW = go.dataset.go; render(); return; }
  var fl = hit("[data-filter]"); if (fl) { ORDER_FILTER = fl.dataset.filter; render(); return; }
  var row = hit("[data-order]"); if (row) { openOrder(row.dataset.order); return; }

  var tadd = hit("[data-till-add]");
  if (tadd) {
    var s = tadd.dataset.tillAdd, p = prod(s);
    TILL.cart[s] = (TILL.cart[s] || 0) + (weighed(p) ? 0.5 : 1);
    render(); return;
  }
  var tstep = hit("[data-till-step]");
  if (tstep) {
    var slug = tstep.dataset.slug, pp = prod(slug);
    var d = +tstep.dataset.tillStep * (weighed(pp) ? 0.5 : 1);
    TILL.cart[slug] = +((TILL.cart[slug] || 0) + d).toFixed(2);
    if (TILL.cart[slug] <= 0) delete TILL.cart[slug];
    render(); return;
  }
  var tpay = hit("[data-till-pay]");
  if (tpay) { TILL.pay = tpay.dataset.tillPay; render(); return; }
  var key = hit("[data-key]");
  if (key) {
    var k = key.dataset.key;
    if (k === "⌫") TILL.tender = TILL.tender.slice(0, -1);
    else if (k === "." && TILL.tender.indexOf(".") > -1) { /* one decimal point only */ }
    else TILL.tender += k;
    render(); return;
  }

  var out = hit("[data-out]");
  if (out && OPEN) {
    var i = +out.dataset.out, l = OPEN.lines[i], pr = lineProd(l);
    l.out = !l.out;
    renderDetail();
    toast(l.out ? pr.n + " marked out of stock — the customer is refunded automatically"
                : pr.n + " put back on the order");
    return;
  }
  var sb = hit("[data-sub]");
  if (sb && OPEN) {
    var j = +sb.dataset.sub, ln = OPEN.lines[j], base = lineProd(ln);
    var alt = CAT.filter(function (x) { return x.c === base.c && x.slug !== base.slug && x.stock > 10; })[0];
    ln.sub = alt ? alt.n : "customer to choose";
    renderDetail();
    toast("Substitute proposed — SMS sent to " + OPEN.cust.split(" ")[0] + " for approval");
    return;
  }
  var rt = hit("[data-retry]");
  if (rt) {
    var e2 = EFRIS.filter(function (x) { return x.inv === rt.dataset.retry; })[0];
    e2.status = "sent";
    e2.fdn = String(324018877400 + Math.floor(Math.random() * 90) + 10);
    render(); toast(e2.inv + " accepted by URA · FDN " + e2.fdn);
    return;
  }
  var md = hit("[data-markdown]");
  if (md) { toast(prod(md.dataset.markdown).n + " marked down 20% — the shelf label is queued to print"); return; }
  var po = hit("[data-po]");
  if (po) {
    var sup = SUPPLIERS.filter(function (x) { return x.id === po.dataset.po; })[0];
    toast("Purchase order sent to " + sup.n + " · " + sup.phone);
    return;
  }

  switch (t.id) {
    case "dX": case "scrim": case "dClose": closeDetail(); break;
    case "advance": {
      var o = OPEN, nx = NEXT[o.status];
      o.status = nx;
      if (nx === "confirmed") {
        toast("Final weights sent to " + o.cust.split(" ")[0] + " · total " + money(orderTot(o)));
        if (!EFRIS.some(function (x) { return x.ref === o.ref; })) {
          var amt = orderTot(o);
          EFRIS.push({ inv: "INV-0008" + (45 + EFRIS.length - 4), ref: o.ref, amount: amt,
            vat: Math.round(amt * SHOP.vatRate), status: "queued", fdn: null,
            at: new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }) });
        }
      } else if (nx === "dispatched") toast(o.ref + " handed to the rider · " + o.zone);
      else if (nx === "delivered") toast(o.ref + " delivered");
      else toast(o.ref + " → " + STATUS[nx].l);
      renderDetail(); render();
      break;
    }
    case "retryAll":
      EFRIS.filter(function (x) { return x.status !== "sent"; }).forEach(function (x) {
        x.status = "sent"; x.fdn = String(324018877400 + Math.floor(Math.random() * 90) + 10);
      });
      render(); toast("Queue cleared — every invoice accepted by URA");
      break;
    case "tillClear": TILL.cart = {}; TILL.tender = ""; render(); toast("Sale voided"); break;
    case "tillPay": {
      var lines = Object.keys(TILL.cart).length;
      var totalDue = Object.keys(TILL.cart).reduce(function (s, k2) { return s + prod(k2).price * TILL.cart[k2]; }, 0);
      TILL.cart = {}; TILL.tender = "";
      render();
      toast(lines + " lines · " + money(totalDue) + " taken — fiscal receipt printing");
      break;
    }
    case "sendPOs": toast("Purchase orders sent to " + SUPPLIERS.length + " suppliers"); break;
    case "addSupplier": toast("Supplier form opens here — wired to your supplier table"); break;
    case "addStaff": toast("Staff form opens here — wired to your rota"); break;
    case "addLine": toast("Add a line in tools/catalog.py, then run tools/build.py"); break;
    case "addZone": toast("Zones live in assets/js/config.js"); break;
    case "expStock": toast("Stock export ready · retailcore-stock.xlsx"); break;
    case "expRep": toast("Report export ready · retailcore-report.xlsx"); break;
    case "expCust": toast("Customer export ready · retailcore-customers.xlsx"); break;
    case "saveSettings": case "saveRules":
      toast("Saved. In production this writes to your settings table.");
      break;
  }
});

document.addEventListener("input", function (e) {
  if (e.target.id === "tillQ") {
    TILL.q = e.target.value;
    var pos = e.target.selectionStart;
    render();
    var t2 = $("#tillQ");
    if (t2) { t2.focus(); t2.setSelectionRange(pos, pos); }
    return;
  }
  var w = e.target.closest ? e.target.closest("[data-weigh]") : null;
  if (w && OPEN) {
    var i = +w.dataset.weigh, v = parseFloat(w.value);
    OPEN.lines[i].w = isNaN(v) || v <= 0 ? null : v;
    var lineEl = w.closest(".oline"), l = OPEN.lines[i], p = lineProd(l);
    var est = p.price * l.q, d = lineVal(l) - est;
    lineEl.querySelector(".ol-p").textContent = num(lineVal(l));
    var dl = lineEl.querySelector(".delta");
    dl.textContent = l.w != null ? (d > 0 ? "+" : "") + num(d) : "awaiting scale";
    dl.style.color = d > 0 ? "var(--warn)" : d < 0 ? "var(--ok)" : "var(--muted)";
    var blocked = OPEN.status === "weighing" && hasUnweighed(OPEN);
    var adv = $("#advance");
    if (adv) {
      adv.disabled = blocked;
      adv.textContent = blocked ? "Confirm all weights first" : NEXT_LABEL[OPEN.status];
    }
  }
});
document.addEventListener("change", function (e) {
  if (e.target.id === "themeSel") {
    document.documentElement.setAttribute("data-theme", e.target.value);
    toast("Theme previewed. Set SHOP.theme in config.js to keep it.");
  }
});
document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDetail(); });

function clock() {
  $("#clock").textContent = new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
}

/* ---------------------------------------------------------------- boot */
document.documentElement.setAttribute("data-theme", SHOP.theme || "superstore");
$("#tenantName").textContent = SHOP.name;
$("#tenantSub").textContent = "RetailCore OS · " + SHOP.address.split(",")[0];
$("#branchChip").innerHTML = "Branch <b>" + esc(SHOP.address.split(",")[0]) + "</b>";
clock(); setInterval(clock, 30000);
render();
})();
