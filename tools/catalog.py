# -*- coding: utf-8 -*-
"""
The shop's master catalogue.

This one file is the source of truth. tools/build.py reads it to write BOTH the
product artwork (shop/assets/img/products/*.svg) and the site's data file
(shop/assets/js/data.js), so the pictures and the prices can never drift apart.

To add a line: add a row here and run `python3 tools/build.py`.
  art: either a named drawing, or a generic packaging archetype —
       pack | carton | tall | bottle | jar | can | tube | poly | tray | bar
"""

AISLES = [
    ("01", "Fresh produce",      "Picked at the market before opening"),
    ("02", "Butchery & fish",    "Cut to order at the counter"),
    ("03", "Dairy & eggs",       "Chilled the whole way to your door"),
    ("04", "Bakery",             "Baked on the premises every morning"),
    ("05", "Pantry",             "The staples, in family sizes"),
    ("06", "Drinks",             "Tea, coffee, water and the crate"),
    ("07", "Household",          "Cleaning, laundry and fuel"),
    ("08", "Baby & personal",    "Care lines kept behind the counter"),
]

# name, aisle, unit, price, cost, stock, sold, tint, art, size, desc, extras
P = [
 # ---------------------------------------------------------------- 01 produce
 ("Matooke", "Fresh produce", "bunch", 18000, 13500, 26, 31, "#8FA85A", "produce.matooke", None,
  "Green cooking banana, medium bunch. Cut at Kayunga this morning and in the shop before opening.",
  {"expiry": "+4", "origin": "Kayunga", "tags": ["local"]}),
 ("Sweet potatoes", "Fresh produce", "kg", 3500, 2400, 60, 24, "#C98B4B", "produce.sweet_potato", None,
  "Firm white-flesh potatoes, brushed clean. Good boiled or roasted.", {"origin": "Masaka"}),
 ("Irish potatoes", "Fresh produce", "kg", 4000, 2900, 74, 38, "#CBB077", "produce.irish_potato", None,
  "Kabale grown, medium size, low blemish. Holds together when boiled.", {"origin": "Kabale"}),
 ("Tomatoes", "Fresh produce", "kg", 5500, 3800, 8, 47, "#C4453C", "produce.tomato", None,
  "Ripe salad tomatoes, hand sorted. Ask the picker for firmer ones if you are storing them.",
  {"was": 6500, "expiry": "+2", "tags": ["deal"]}),
 ("Red onions", "Fresh produce", "kg", 6000, 4200, 44, 33, "#9C5A7A", "produce.onion", None,
  "Dry cured red onions, sold loose by the kilo.", {}),
 ("Dodo greens", "Fresh produce", "bunch", 1500, 900, 38, 52, "#5C8748", "produce.greens", None,
  "Amaranth greens tied in a bunch. Best used within two days.", {"expiry": "+2"}),
 ("Nakati", "Fresh produce", "bunch", 1500, 950, 31, 28, "#6E9450", "produce.greens", None,
  "African eggplant leaves. Slightly bitter, very good with g-nut sauce.", {"expiry": "+2"}),
 ("Avocado", "Fresh produce", "each", 2500, 1600, 52, 44, "#7C9A4E", "produce.avocado", None,
  "Large local avocado sold at eating ripeness. Say the word and we pick them firm.", {"expiry": "+5"}),
 ("Passion fruit", "Fresh produce", "kg", 9000, 6200, 19, 16, "#8C4A6E", "produce.passion_fruit", None,
  "Purple passion — wrinkled skin means ready. Roughly 22 fruit to the kilo.", {}),
 ("Pineapple", "Fresh produce", "each", 6000, 4000, 23, 27, "#D2A234", "produce.pineapple", None,
  "Sweet Kayunga pineapple, medium. We trim the crown on request.",
  {"was": 7000, "tags": ["deal"], "origin": "Kayunga"}),
 ("Mangoes", "Fresh produce", "kg", 7000, 4800, 33, 35, "#D08A2E", "produce.mango", None,
  "Local mango, in season, ripe and ready to eat.", {"tags": ["season"]}),
 ("Sweet bananas", "Fresh produce", "bunch", 5000, 3300, 29, 41, "#E8C444", "produce.matooke", None,
  "Small sweet bananas — ndizi. Sold as a hand.", {}),
 ("Oranges", "Fresh produce", "kg", 6500, 4400, 26, 19, "#E08A1E", "produce.citrus", None,
  "Thin skinned juicing oranges. Six or seven to the kilo.", {}),
 ("Watermelon", "Fresh produce", "each", 12000, 8000, 14, 11, "#3E8A46", "produce.watermelon", None,
  "Whole melon, about four kilos. We halve it for you at the counter.", {}),
 ("Cabbage", "Fresh produce", "each", 3000, 1900, 41, 22, "#93A86B", "produce.cabbage", None,
  "Tight headed green cabbage, outer leaves trimmed.", {}),
 ("Carrots", "Fresh produce", "kg", 5000, 3400, 29, 30, "#CE7A32", "produce.carrot", None,
  "Topped and washed. They snap clean when they are fresh.", {}),
 ("Green pepper", "Fresh produce", "kg", 8000, 5900, 12, 9, "#5F8C51", "produce.green_pepper", None,
  "Firm bell peppers, mixed sizes.", {"expiry": "+4"}),

 # ---------------------------------------------------------------- 02 butchery
 ("Beef, choice cut", "Butchery & fish", "kg", 18000, 14200, 14, 52, "#9C3B3B", "fresh.beef", None,
  "Boneless and trimmed. Tell the butcher how you want it cut — stew, steak or mince — in the order note.",
  {"expiry": "+1"}),
 ("Beef mince", "Butchery & fish", "kg", 17000, 13400, 11, 24, "#B0453E", "tray:BEEF MINCE|lean 80/20", None,
  "Minced to order from the same choice cut. Ask for extra lean in the note.", {"expiry": "+1"}),
 ("Goat meat", "Butchery & fish", "kg", 22000, 17600, 9, 18, "#8E4141", "fresh.goat", None,
  "Bone in, cut to size. The cut people ask for at Christmas and for luwombo.", {"expiry": "+1"}),
 ("Pork", "Butchery & fish", "kg", 16000, 12400, 13, 21, "#B2686B", "fresh.pork", None,
  "Fresh pork, mixed cut. Ask for ribs or belly in the order note.",
  {"was": 18000, "tags": ["deal"], "expiry": "+1"}),
 ("Whole chicken", "Butchery & fish", "each", 28000, 22500, 17, 22, "#D8A863", "fresh.chicken", 1400,
  "Farm chicken, cleaned and dressed. Around 1.4 kg each.", {"was": 31000, "tags": ["deal"]}),
 ("Beef sausages", "Butchery & fish", "pack", 14000, 10600, 19, 16, "#C4655C", "tray:BEEF SAUSAGES|500 g pack", 500,
  "Coarse butchery sausage, eight to the pack.", {"expiry": "+3"}),
 ("Nile perch fillet", "Butchery & fish", "kg", 26000, 21000, 6, 18, "#E0B0A2", "fresh.fish_fillet", None,
  "Boneless fillet off the lake, packed on ice. Travels in the chilled box.", {"expiry": "+1"}),
 ("Tilapia, whole", "Butchery & fish", "kg", 20000, 15800, 11, 14, "#9EA893", "fresh.whole_fish", None,
  "Gutted and scaled. Roughly two medium fish to the kilo.", {"expiry": "+1"}),
 ("Mukene", "Butchery & fish", "kg", 12000, 8600, 22, 12, "#C6C2A4", "fresh.small_fish", None,
  "Sun dried silver fish, sorted and cleaned.", {}),

 # ---------------------------------------------------------------- 03 dairy
 ("Fresh milk 1L", "Dairy & eggs", "each", 3500, 2750, 88, 96, "#DDE4EC", "fresh.milk_pouch", 1000,
  "Pasteurised whole milk. Keep it chilled and use within three days of opening.", {"expiry": "+3"}),
 ("Long life milk 1L", "Dairy & eggs", "each", 4200, 3400, 64, 38, "#BFD4E8", "tall:UHT|MILK|full cream 1 L|#1B6CA8", 1000,
  "UHT milk for the cupboard. Handy when the power goes.", {}),
 ("Yoghurt 500ml", "Dairy & eggs", "each", 7000, 5300, 34, 26, "#E4D3C2", "fresh.yoghurt", 500,
  "Plain set yoghurt, no added sugar.", {"expiry": "+8"}),
 ("Butter 250g", "Dairy & eggs", "each", 14000, 11200, 20, 12, "#DCC176", "fresh.butter", 250,
  "Salted dairy butter, foil wrapped.", {}),
 ("Margarine 500g", "Dairy & eggs", "each", 9500, 7400, 28, 17, "#E8C96A", "jar:BLUE BAND|SPREAD|500 g|#1B6CA8", 500,
  "Everyday spread for bread and baking.", {}),
 ("Eggs, tray of 30", "Dairy & eggs", "tray", 16000, 13200, 27, 29, "#D6BE94", "fresh.eggs", None,
  "Mixed size farm eggs. We candle every tray before it leaves.",
  {"was": 17500, "tags": ["deal"]}),
 ("Cheddar 200g", "Dairy & eggs", "each", 19000, 15400, 7, 4, "#D3A245", "fresh.cheese", 200,
  "Matured cheddar block, vacuum sealed.", {"expiry": "+18"}),

 # ---------------------------------------------------------------- 04 bakery
 ("White loaf", "Bakery", "loaf", 5500, 4100, 45, 73, "#D6BC8E", "fresh.white_loaf", 600,
  "Baked this morning. We slice it at the counter if you ask.", {"expiry": "+2"}),
 ("Brown loaf", "Bakery", "loaf", 6500, 4900, 31, 44, "#B08D5D", "fresh.brown_loaf", 600,
  "Wholemeal with a denser crumb. Baked daily.", {"expiry": "+2"}),
 ("Chapati, 5 pack", "Bakery", "pack", 4000, 2600, 24, 38, "#CFA96E", "fresh.chapati", None,
  "Soft chapati made fresh each morning. Warm them before serving.", {"expiry": "+2"}),
 ("Mandazi, 6 pack", "Bakery", "pack", 3000, 1900, 19, 31, "#C89B58", "fresh.mandazi", None,
  "Lightly spiced and fried this morning.", {"expiry": "+2"}),
 ("Sweet buns, 6 pack", "Bakery", "pack", 4500, 3000, 22, 18, "#E0C08A", "poly:BAKERY|SWEET BUNS|6 pack|#B0700E", None,
  "Soft milk buns, good for a school lunchbox.", {"expiry": "+3"}),

 # ---------------------------------------------------------------- 05 pantry
 ("Maize flour 2kg", "Pantry", "pack", 6500, 5200, 63, 41, "#D8CDA6", "packaged.maize_flour", 2000,
  "Fine posho flour, sifted. Sealed 2 kg pack.", {}),
 ("Rice 5kg", "Pantry", "pack", 26000, 22400, 38, 26, "#DAD3BC", "packaged.rice", 5000,
  "Long grain rice, low broken content.", {"was": 29000, "tags": ["deal"]}),
 ("Sugar 2kg", "Pantry", "pack", 9500, 7900, 57, 34, "#DDD9CB", "packaged.sugar", 2000,
  "Granulated white sugar, sealed pack.", {}),
 ("Salt 1kg", "Pantry", "pack", 2000, 1300, 82, 29, "#CFD8E2", "pack:SEA SALT|iodised 1 kg|#2F5A8A", 1000,
  "Iodised table salt.", {}),
 ("Cooking oil 3L", "Pantry", "each", 32000, 27800, 29, 19, "#D7B646", "packaged.cooking_oil", 3000,
  "Refined vegetable oil in a 3 litre jerrycan.", {"was": 35000, "tags": ["deal"]}),
 ("Dry beans", "Pantry", "kg", 5500, 3900, 48, 37, "#A0705A", "packaged.beans", None,
  "Sorted red beans, stones removed.", {}),
 ("G-nut paste 500ml", "Pantry", "each", 9000, 6800, 26, 21, "#B08052", "packaged.gnut_paste", 500,
  "Ground groundnut paste, nothing added. Stir before use.", {}),
 ("Spaghetti 500g", "Pantry", "pack", 5000, 3700, 44, 23, "#E0C88A", "pack:SPAGHETTI|durum wheat 500 g|#B0700E", 500,
  "Durum wheat spaghetti.", {}),
 ("Tomato paste 400g", "Pantry", "each", 4500, 3200, 51, 27, "#C4453C", "can:TOMATO|PASTE|400 g|#A82B1E", 400,
  "Double concentrated paste for stews and sauces.", {}),
 ("Baked beans 400g", "Pantry", "each", 5500, 4100, 39, 15, "#C4653C", "can:BAKED|BEANS|400 g|#1E5AA8", 400,
  "In tomato sauce. A breakfast standby.", {}),
 ("Curry powder 100g", "Pantry", "pack", 3500, 2200, 47, 18, "#D89A2E", "pack:CURRY|POWDER|100 g|#A05A0E", 100,
  "Mild household blend.", {}),
 ("Honey 500g", "Pantry", "each", 18000, 13500, 16, 8, "#D9A62E", "jar:PURE|HONEY|500 g|#C9962E", 500,
  "Raw honey from West Nile. It will crystallise — that is a good sign.", {"tags": ["local"]}),

 # ---------------------------------------------------------------- 06 drinks
 ("Ugandan coffee 250g", "Drinks", "each", 18000, 12500, 15, 7, "#7A5236", "packaged.coffee", 250,
  "Mount Elgon arabica, medium roast. Ground or whole bean — say which in the note.",
  {"tags": ["local"]}),
 ("Tea leaves 250g", "Drinks", "each", 7500, 5200, 22, 14, "#8A7141", "packaged.tea", 250,
  "Loose black tea from Fort Portal.", {"tags": ["local"]}),
 ("Drinking water 5L", "Drinks", "each", 4500, 3200, 70, 58, "#A9C4CE", "packaged.water", 5000,
  "Purified water, 5 litre bottle with a carry handle.", {}),
 ("Mango juice 1L", "Drinks", "each", 6500, 4800, 36, 22, "#E8B96A", "tall:MANGO|JUICE|1 litre|#E08A2E", 1000,
  "No added sugar, pressed from local fruit.", {}),
 ("Soda 500ml", "Drinks", "each", 2500, 1800, 96, 74, "#C4453C", "bottle:COLA|500 ml|#A82B1E", 500,
  "Chilled single bottle. Deposit does not apply to plastic.", {}),
 ("Soda crate, 24", "Drinks", "crate", 32000, 28500, 12, 11, "#B24545", "packaged.soda_crate", None,
  "Mixed 300 ml glass bottles. Crate deposit refunded on your next order.", {}),
 ("Energy drink 250ml", "Drinks", "each", 4000, 2900, 58, 33, "#3E8A46", "can:ENERGY|DRINK|250 ml|#2F6B33", 250,
  "Chilled, sold singly.", {}),

 # ---------------------------------------------------------------- 07 household
 ("Detergent 1kg", "Household", "pack", 12000, 9300, 33, 26, "#7FA0BE", "packaged.detergent", 1000,
  "Machine and hand wash powder.", {"was": 13500, "tags": ["deal"]}),
 ("Laundry bar soap", "Household", "each", 4500, 3100, 64, 48, "#B9C4A9", "packaged.soap", 800,
  "Long lasting laundry bar.", {}),
 ("Dish washing liquid", "Household", "each", 8500, 6300, 41, 22, "#4EA88C", "bottle:DISH|WASH|750 ml|#2E8B72", 750,
  "Cuts grease, gentle on hands.", {}),
 ("Bleach 1L", "Household", "each", 6500, 4700, 37, 19, "#9AC4DE", "bottle:BLEACH|1 litre|#1E6FB8", 1000,
  "Household bleach for floors and whites. Never mix it with other cleaners.", {}),
 ("Tissue, 10 rolls", "Household", "pack", 14000, 10800, 41, 16, "#D2D2CB", "packaged.tissue", None,
  "Two ply, ten roll pack.", {"was": 15500, "tags": ["deal"]}),
 ("Charcoal sack", "Household", "sack", 55000, 46000, 5, 3, "#5B5A55", "packaged.charcoal", None,
  "Hardwood charcoal, full sack. Heavy item — the rider brings it to the gate.", {}),
 ("Matches, 10 boxes", "Household", "pack", 2000, 1200, 73, 34, "#D8A05A", "carton:SAFETY|MATCHES|10 boxes|#A0500E", None,
  "Safety matches, ten boxes to the sleeve.", {}),
 ("Candles, 6 pack", "Household", "pack", 5000, 3400, 44, 21, "#E4E0D2", "poly:HOUSEHOLD|CANDLES|6 pack|#8A8A7A", None,
  "White household candles, six hours each.", {}),
 ("Mosquito coils", "Household", "pack", 3500, 2300, 52, 29, "#7A9A4E", "carton:MOSQUITO|COILS|10 coils|#4E7A2E", None,
  "Ten coils to the box, stands included.", {}),

 # ---------------------------------------------------------------- 08 baby & personal
 ("Baby nappies, size 4", "Baby & personal", "pack", 42000, 34500, 18, 12, "#9AD2DE", "poly:BABY|NAPPIES|size 4 · 30 pcs|#2E9DB0", None,
  "Thirty to the pack, 8–14 kg.", {}),
 ("Baby wipes", "Baby & personal", "pack", 9000, 6600, 26, 15, "#BCE0E8", "poly:BABY|WIPES|72 sheets|#2E9DB0", None,
  "Unscented, 72 sheets.", {}),
 ("Toothpaste 150ml", "Baby & personal", "each", 7500, 5400, 48, 27, "#DCE8F0", "tube:FRESH|MINT|150 ml|#1E7AA8", 150,
  "Fluoride toothpaste, family size.", {}),
 ("Bath soap, 3 pack", "Baby & personal", "pack", 7000, 5100, 39, 24, "#E4B8C4", "bar:BATH SOAP|3 × 100 g|#B04A6E", None,
  "Moisturising bath bars, three to the pack.", {}),
 ("Body lotion 400ml", "Baby & personal", "each", 14000, 10400, 23, 13, "#E8D4BC", "bottle:BODY|LOTION|400 ml|#B08A5A", 400,
  "Cocoa butter lotion for dry skin.", {}),
 ("Sanitary pads", "Baby & personal", "pack", 6500, 4700, 44, 31, "#E4C8DE", "poly:ULTRA|SANITARY PADS|10 pads|#A84A8E", None,
  "Ten pads with wings. Kept in a plain bag on request.", {}),
 ("Cotton wool 100g", "Baby & personal", "each", 4000, 2700, 31, 12, "#F0F0EC", "poly:COTTON|WOOL|100 g|#8A9AA8", 100,
  "Medical grade cotton wool roll.", {}),
]

def rows():
    """Normalised catalogue rows with slug and derived fields."""
    import re
    out = []
    for i, (name, aisle, unit, price, cost, stock, sold, tint, art, size, desc, extra) in enumerate(P, start=1):
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        out.append({
            "id": i, "slug": slug, "n": name, "c": aisle, "u": unit,
            "price": price, "cost": cost, "stock": stock, "sold": sold,
            "tint": tint, "art": art, "size": size, "d": desc,
            "was": extra.get("was"), "expiry": extra.get("expiry"),
            "origin": extra.get("origin"), "tags": extra.get("tags", []),
        })
    return out

if __name__ == "__main__":
    r = rows()
    print(len(r), "lines across", len(set(x["c"] for x in r)), "aisles")
    for a, _, _ in [(a, b, c) for a, b, c in AISLES]:
        pass
    for num, aisle, _ in AISLES:
        print(" ", num, aisle, "-", sum(1 for x in r if x["c"] == aisle))
