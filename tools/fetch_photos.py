# -*- coding: utf-8 -*-
"""
fetch_photos.py - dociąga BRAKUJĄCE zdjęcia do public/img/<slug>.jpg prosto z Wikipedii.

Zdjęcia hostujemy lokalnie. Hotlink do Wikimedia NIE działa (rate limit + HTTP 400 na
nietypowych rozmiarach miniatur) - dlatego pobieramy plik raz i trzymamy w repo.

Skrypt bierze tytuł artykułu z pola `source` gracza, pyta API o miniaturę (domyślnie 500 px)
i zapisuje ją jako JPG. Rusza tylko graczy, którym pliku brakuje - jest więc bezpieczny
do wielokrotnego uruchamiania.

Użycie:
  python tools/fetch_photos.py                 # uzupełnia braki
  python tools/fetch_photos.py --size 800      # inna szerokość miniatury
  python tools/fetch_photos.py --force         # nadpisz także istniejące
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "public", "img")
PLAYERS = os.path.join(ROOT, "public", "data", "players.json")
API = "https://en.wikipedia.org/w/api.php"
UA = "najlepsi-pilkarze/1.0 (hobbystyczny ranking; https://najlepsipilkarze.tomaszkwietniewski.pl)"


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
            return raw if binary else json.loads(raw.decode("utf-8"))
        except Exception:
            if attempt == 4:
                raise
            time.sleep(3 * (attempt + 1))


def thumb_url(title, size):
    url = API + "?" + urllib.parse.urlencode({
        "action": "query", "prop": "pageimages", "piprop": "thumbnail",
        "pithumbsize": size, "titles": title, "format": "json", "redirects": "1",
    })
    pages = get(url)["query"]["pages"]
    page = list(pages.values())[0]
    return (page.get("thumbnail") or {}).get("source")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    size = int(argv[argv.index("--size") + 1]) if "--size" in argv else 500
    force = "--force" in argv

    data = json.load(open(PLAYERS, encoding="utf-8"))
    os.makedirs(IMG, exist_ok=True)
    todo, ok, fail = [], 0, []
    for p in data["players"]:
        dest = os.path.join(IMG, slug(p["name"]) + ".jpg")
        if os.path.exists(dest) and not force:
            continue
        todo.append((p, dest))

    if not todo:
        print("Wszyscy gracze maja zdjecia - nic do zrobienia.")
        return

    for p, dest in todo:
        src = p.get("source") or ""
        title = urllib.parse.unquote(src.rsplit("/wiki/", 1)[1]) if "/wiki/" in src else p["name"]
        try:
            url = thumb_url(title, size)
            if not url:
                fail.append((p["name"], "brak miniatury w artykule"))
                continue
            open(dest, "wb").write(get(url, binary=True))
            p["photo"] = "img/" + os.path.basename(dest)
            ok += 1
            print("  OK  %-24s <- %s" % (p["name"], url.rsplit("/", 1)[-1][:60]))
        except Exception as e:
            fail.append((p["name"], str(e)))
        time.sleep(1.5)

    json.dump(data, open(PLAYERS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nPobrano %d zdjec do %s" % (ok, IMG))
    for name, why in fail:
        print("  BRAK: %-24s %s" % (name, why))
    if fail:
        print("Braki uzupelnij recznie (plik public/img/<slug>.jpg, 500 px, JPG).")


if __name__ == "__main__":
    main()
