/* ============================================================================
   SHOP CONFIGURATION — the only file most shops ever need to touch.
   Change the values here and the whole storefront and back office follow:
   name, colours, delivery zones, fees, payment methods, opening hours.
   ============================================================================ */
window.SHOP = {

  /* ---------- identity ---------- */
  name:      "Kira Superstore",
  legalName: "Kira Superstore Ltd",
  tagline:   "Everything on your list, delivered",
  strapline: "Seven aisles · One delivery",
  blurb:     "A full weekly shop — produce, butchery, bakery and pantry — picked the " +
             "morning you order it and delivered across Kampala the same day.",

  /* ---------- contact ---------- */
  phone:    "+256 700 000 000",
  phoneRaw: "256700000000",
  whatsapp: "256700000000",
  email:    "orders@kirasuperstore.ug",
  address:  "Kira Road, Kampala, Uganda",
  mapNote:  "Opposite the Shell station, next to the pharmacy",
  hours: [
    { d: "Monday – Friday", h: "7:00am – 10:00pm" },
    { d: "Saturday",        h: "7:00am – 10:00pm" },
    { d: "Sunday",          h: "9:00am – 8:00pm"  }
  ],
  socials: [
    { n: "WhatsApp",  u: "https://wa.me/256700000000" },
    { n: "Facebook",  u: "#" },
    { n: "Instagram", u: "#" },
    { n: "TikTok",    u: "#" }
  ],

  /* ---------- money & trading rules ---------- */
  currency:   "UGX",
  locale:     "en-UG",
  vatRate:    0.18,          // shown on the fiscal receipt
  freeOver:   150000,        // free delivery above this basket value
  tolerance:  0.10,          // weighed lines may settle ±10% after the scale
  cutoff:     "2:00 PM",     // same-day cut-off
  windowText: "4:00 – 7:00 PM",
  loyaltyRate: 0.01,         // 1 point per 100 spent

  /* ---------- look ---------- */
  theme: "superstore",       // "superstore" (cobalt) or "market" (crimson)

  /* ---------- delivery ---------- */
  zones: [
    { id:"z1", name:"Muyenga · Bugolobi · Luzira", area:"Tank Hill, Kabalagala, Port Bell",
      fee:5000,  min:30000, eta:"Today, 4–6pm" },
    { id:"z2", name:"Kololo · Nakasero · Naguru",  area:"City centre and the hills",
      fee:6000,  min:30000, eta:"Today, 4–6pm" },
    { id:"z3", name:"Ntinda · Bukoto · Kisaasi",   area:"Northern suburbs",
      fee:7000,  min:40000, eta:"Today, 5–7pm" },
    { id:"z4", name:"Entebbe Road · Kajjansi",     area:"Seguku, Kajjansi, Abaita Ababiri",
      fee:12000, min:60000, eta:"Today, 5–7pm" },
    { id:"z5", name:"Entebbe town",                area:"Kitoolo, Nakiwogo, Kiwafu",
      fee:15000, min:80000, eta:"Tomorrow, 10am–1pm" }
  ],

  /* ---------- payment ---------- */
  payments: [
    { id:"momo",   name:"MTN Mobile Money",   note:"Approve the prompt on your phone",
      mark:"assets/img/brand/pay-momo.svg",   needsNumber:true },
    { id:"airtel", name:"Airtel Money",       note:"Approve the prompt on your phone",
      mark:"assets/img/brand/pay-airtel.svg", needsNumber:true },
    { id:"card",   name:"Visa or Mastercard", note:"Secure hosted checkout",
      mark:"assets/img/brand/pay-card.svg",   needsNumber:false },
    { id:"cod",    name:"Cash on delivery",   note:"Pay the rider at your door",
      mark:"assets/img/brand/pay-cash.svg",   needsNumber:false }
  ],

  /* ---------- promises shown across the site ---------- */
  promises: [
    { k:"SHELF PRICES", t:"The same price as in the shop",
      d:"What you see online is what is on the shelf tag. No online mark-up, ever." },
    { k:"WEIGHED LINES", t:"Priced at the scale, not guessed",
      d:"Meat, fish and loose produce are weighed at the counter. You get the exact figure by SMS before the rider leaves." },
    { k:"SUBSTITUTIONS", t:"We call, we never guess",
      d:"If a line is finished the picker rings you with an alternative. Nothing goes in the bag without your word." },
    { k:"RECEIPTS", t:"A fiscal receipt every time",
      d:"Every order carries a URA-verified receipt with a QR code, delivered with your shopping." }
  ],

  /* ---------- what shoppers say ---------- */
  reviews: [
    { n:"Nakato S.", z:"Muyenga", r:5,
      t:"I ordered at half nine and the matooke was at my gate before six, still cool. The weights text is what sold me — no arguing at the door." },
    { n:"Okello B.", z:"Ntinda", r:5,
      t:"The picker called about the fish being finished and offered tilapia instead. Small thing, but nobody else does it." },
    { n:"Aine P.", z:"Kololo", r:4,
      t:"Prices match the shop exactly. I checked, twice. The rice deal saved me thirty thousand this month." }
  ],

  /* ---------- FAQ ---------- */
  faq: [
    { q:"How late can I order for same-day delivery?",
      a:"Order before 2:00 PM and your shopping goes out in the same afternoon run, delivered between 4:00 and 7:00 PM depending on your zone. Anything after the cut-off is picked first thing the next morning." },
    { q:"How are meat, fish and loose produce priced?",
      a:"They are weighed at the counter when your order is picked. You are charged the estimate shown here, then we text you the exact weight and settle the difference on the same mobile money number — up or down. The difference is capped at 10%." },
    { q:"What happens if something is out of stock?",
      a:"The picker calls you before substituting anything. You can accept the alternative, drop the line for a refund, or ask us to hold the order until the delivery comes in." },
    { q:"Which payments do you take?",
      a:"MTN Mobile Money, Airtel Money, Visa and Mastercard, or cash to the rider at your door. Mobile money is the fastest — you approve a prompt on your phone and the order confirms itself." },
    { q:"Do you deliver outside Kampala?",
      a:"We run down Entebbe Road as far as Entebbe town. Entebbe town orders placed after midday are delivered the following morning between 10am and 1pm." },
    { q:"Can I return something?",
      a:"Anything chilled or fresh that arrives in poor condition is refunded or replaced on the spot — show the rider. Sealed pantry goods can be returned unopened within seven days with the receipt." },
    { q:"Do you supply offices and restaurants?",
      a:"Yes. Corporate accounts get a monthly invoice, a named account manager and standing weekly orders. Call us and ask for the trade desk." }
  ]
};
