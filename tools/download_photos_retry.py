# -*- coding: utf-8 -*-
import urllib.request, json, os, re, unicodedata, time
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # katalog repo (dziala tez w git worktree)
IMG = os.path.join(ROOT, "public/img")
UA = "najlepsi-pilkarze/1.0 (hobby; tomasz.kwietniewski@gmail.com)"

def slug(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read()

def up500(url):
    if "/thumb/" in url and re.search(r"/\d+px-[^/]+$", url):
        return re.sub(r"/\d+px-([^/]+)$", r"/500px-\1", url)
    return None

db = json.load(open(os.path.join(ROOT, "public/data/players.json"), encoding="utf-8"))
# tylko ci, ktorych photo NIE jest jeszcze lokalne, ale maja jakies photo (wiki URL)
todo = [p for p in db["players"] if p.get("photo") and not str(p["photo"]).startswith("img/")]
print("Do pobrania:", len(todo))
ok = 0; fail = []
for p in todo:
    sl = slug(p["name"]); dest = os.path.join(IMG, sl + ".jpg")
    photo = p["photo"]; data = None
    for cand in [up500(photo), photo]:
        if not cand: continue
        for attempt in range(3):
            try:
                data = fetch(cand); break
            except Exception:
                data = None; time.sleep(1.5 * (attempt + 1))
        if data: break
    if data:
        open(dest, "wb").write(data); p["photo"] = "img/" + sl + ".jpg"; ok += 1
    else:
        fail.append(p["name"])
    time.sleep(0.6)

json.dump(db, open(os.path.join(ROOT, "public/data/players.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
n_local = sum(1 for p in db["players"] if str(p.get("photo","")).startswith("img/"))
print("Dodano:", ok, "| lacznie lokalnie:", n_local, "/", len(db["players"]))
print("Nadal brak:", fail)
