# -*- coding: utf-8 -*-
"""
Search terms for sourcing a real photograph per catalogue line.

Kept separate from the catalogue so the wording can be tuned without touching
prices or stock. Terms are deliberately plain and singular-subject: stock
libraries match "ripe tomatoes" far better than "Tomatoes 1kg loose".

`local` marks lines a stock library will not cover honestly — Ugandan staples
that need the client's own photographs. Those are listed for the handover so
nobody discovers them at go-live.
"""

# slug -> (search term, needs_own_photo)
QUERIES = {
    # ---- fresh produce
    "matooke":            ("green cooking bananas plantain bunch", True),
    "sweet-potatoes":     ("sweet potatoes", False),
    "irish-potatoes":     ("raw potatoes", False),
    "tomatoes":           ("ripe tomatoes", False),
    "red-onions":         ("red onions", False),
    "dodo-greens":        ("amaranth greens bunch", True),
    "nakati":             ("african leafy greens bunch", True),
    "avocado":            ("avocado halved", False),
    "passion-fruit":      ("passion fruit", False),
    "pineapple":          ("fresh pineapple", False),
    "mangoes":            ("ripe mangoes", False),
    "sweet-bananas":      ("bananas bunch", False),
    "oranges":            ("fresh oranges", False),
    "watermelon":         ("watermelon slice", False),
    "cabbage":            ("green cabbage", False),
    "carrots":            ("fresh carrots", False),
    "green-pepper":       ("green bell peppers", False),

    # ---- butchery & fish
    "beef-choice-cut":    ("raw beef steak butcher", False),
    "beef-mince":         ("raw minced beef", False),
    "goat-meat":          ("raw goat meat", True),
    "pork":               ("raw pork belly", False),
    "whole-chicken":      ("raw whole chicken", False),
    "beef-sausages":      ("raw beef sausages", False),
    "nile-perch-fillet":  ("raw white fish fillet", False),
    "tilapia-whole":      ("whole tilapia fish", False),
    "mukene":             ("dried small silver fish", True),

    # ---- dairy & eggs
    "fresh-milk-1l":      ("milk carton", False),
    "long-life-milk-1l":  ("milk carton shelf", False),
    "yoghurt-500ml":      ("plain yoghurt tub", False),
    "butter-250g":        ("butter block", False),
    "margarine-500g":     ("margarine tub", False),
    "eggs-tray-of-30":    ("tray of eggs", False),
    "cheddar-200g":       ("cheddar cheese block", False),

    # ---- bakery
    "white-loaf":         ("white bread loaf", False),
    "brown-loaf":         ("brown bread loaf", False),
    "chapati-5-pack":     ("chapati flatbread stack", False),
    "mandazi-6-pack":     ("fried dough mandazi", True),
    "sweet-buns-6-pack":  ("bread buns", False),

    # ---- pantry
    "maize-flour-2kg":    ("maize flour bag", True),
    "rice-5kg":           ("bag of rice", False),
    "sugar-2kg":          ("white sugar bag", False),
    "salt-1kg":           ("table salt", False),
    "cooking-oil-3l":     ("cooking oil bottle", False),
    "dry-beans":          ("dried red beans", False),
    "g-nut-paste-500ml":  ("peanut butter jar", False),
    "spaghetti-500g":     ("spaghetti pasta packet", False),
    "tomato-paste-400g":  ("tomato paste tin", False),
    "baked-beans-400g":   ("tin of baked beans", False),
    "curry-powder-100g":  ("curry powder spice", False),
    "honey-500g":         ("honey jar", False),

    # ---- drinks
    "ugandan-coffee-250g": ("coffee beans bag", False),
    "tea-leaves-250g":     ("loose black tea leaves", False),
    "drinking-water-5l":   ("large water bottle", False),
    "mango-juice-1l":      ("mango juice carton", False),
    "soda-500ml":          ("cola bottle", False),
    "soda-crate-24":       ("crate of soda bottles", False),
    "energy-drink-250ml":  ("energy drink can", False),

    # ---- household
    "detergent-1kg":      ("laundry detergent powder", False),
    "laundry-bar-soap":   ("bar of laundry soap", False),
    "dish-washing-liquid":("dish soap bottle", False),
    "bleach-1l":          ("bleach bottle cleaning", False),
    "tissue-10-rolls":    ("toilet paper rolls pack", False),
    "charcoal-sack":      ("charcoal sack", True),
    "matches-10-boxes":   ("box of matches", False),
    "candles-6-pack":     ("white candles", False),
    "mosquito-coils":     ("mosquito coil", True),

    # ---- baby & personal care
    "baby-nappies-size-4":("baby nappies pack", False),
    "baby-wipes":         ("baby wipes pack", False),
    "toothpaste-150ml":   ("toothpaste tube", False),
    "bath-soap-3-pack":   ("bar soap toiletries", False),
    "body-lotion-400ml":  ("body lotion bottle", False),
    "sanitary-pads":      ("sanitary pads pack", False),
    "cotton-wool-100g":   ("cotton wool roll", False),
}

# Wider scene photography for the aisle banners and marketing pages.
SCENES = {
    "aisle-fresh-produce":   "supermarket fresh produce aisle",
    "aisle-butchery-fish":   "butcher counter meat display",
    "aisle-dairy-eggs":      "supermarket dairy fridge",
    "aisle-bakery":          "bakery bread shelf",
    "aisle-pantry":          "supermarket grocery shelves",
    "aisle-drinks":          "supermarket drinks aisle",
    "aisle-household":       "supermarket household cleaning aisle",
    "aisle-baby-personal":   "pharmacy toiletries shelf",
    "hero":                  "grocery shopping bag vegetables",
    "rider":                 "delivery motorcycle courier",
    "storefront":            "small grocery shop front",
    "showcase":              "woman shopping groceries phone",
}

def summary():
    own = [s for s, (_, need) in QUERIES.items() if need]
    return len(QUERIES), len(SCENES), own

if __name__ == "__main__":
    n, s, own = summary()
    print("%d product queries, %d scene queries" % (n, s))
    print("\n%d lines need the client's own photograph (stock will not cover them honestly):" % len(own))
    for slug in own:
        print("  -", slug)
