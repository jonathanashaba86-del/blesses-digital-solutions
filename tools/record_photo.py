# -*- coding: utf-8 -*-
"""Append a verified Unsplash pick to tools/photos.json.

Each pick is recorded only after its alt text has been read and judged to match
the line it will represent — that check is why the manifest exists at all.

  python3 tools/record_photo.py <key> <kind> <hash> <id> <photographer> <username> <alt> <query>
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "photos.json")

SIZES = {"product": (800, 600), "aisle": (1200, 900), "scene": (1900, 1100)}

def url_for(h, kind):
    w, ht = SIZES[kind]
    return ("https://images.unsplash.com/photo-%s"
            "?ixlib=rb-4.1.0&fm=jpg&q=80&fit=crop&crop=entropy&w=%d&h=%d" % (h, w, ht))

def main():
    key, kind, h, pid, by, user, alt, query = sys.argv[1:9]
    man = {"photos": {}}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as f:
            man = json.load(f)
    man["photos"][key] = {
        "kind": kind, "hash": h, "id": pid, "query": query, "alt": alt,
        "photographer": by, "username": user,
        "profile": "https://unsplash.com/@" + user,
        "source": "https://unsplash.com/photos/" + pid,
        "url": url_for(h, kind),
        "download": url_for(h, kind).replace("&w=%d&h=%d" % SIZES[kind], "&w=1600&h=1200")
                    if kind == "product" else url_for(h, kind),
    }
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, ensure_ascii=False)
    print("recorded %-24s %s" % (key, alt))

if __name__ == "__main__":
    main()
