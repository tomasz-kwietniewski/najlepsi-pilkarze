# -*- coding: utf-8 -*-
import urllib.request, json, os, re, unicodedata, shutil
ROOT = "C:/Users/L857K/claude/najlepsi-pilkarze"
IMG = os.path.join(ROOT, "public/img")
os.makedirs(IMG, exist_ok=True)
UA = "najlepsi-pilkarze/1.0 (hobby; tomasz.kwietniewski@gmail.com)"

def slug(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read()

def up500(url):
    # zamien rozmiar thumbnaila na 500px, jesli to URL /thumb/
    if "/thumb/" in url and re.search(r"/\d+px-[^/]+$", url):
        return re.sub(r"/\d+px-([^/]+)$", r"/500px-\1", url)
    return None

db = json.load(open(os.path.join(ROOT, "public/data/players.json"), encoding="utf-8"))
ok = 0; fail = []
for p in db["players"]:
    photo = p.get("photo")
    if not photo:
        continue
    sl = slug(p["name"])
    dest = os.path.join(IMG, sl + ".jpg")
    data = None
    for cand in [up500(photo), photo]:
        if not cand:
            continue
        try:
            data = fetch(cand); break
        except Exception:
            data = None
    if data:
        open(dest, "wb").write(data)
        p["photo"] = "img/" + sl + ".jpg"; ok += 1
    else:
        fail.append(p["name"])

# Deco i Xavi z docs/
DOCS = os.path.join(ROOT, "docs")
manual = {"Xavi": "Xavi.jpg", "Deco": "deco-barcelona-1591366862-40626.jpg"}
for name, fname in manual.items():
    src = os.path.join(DOCS, fname)
    if os.path.exists(src):
        sl = slug(name); dest = os.path.join(IMG, sl + ".jpg")
        shutil.copyfile(src, dest)
        for p in db["players"]:
            if p["name"] == name:
                p["photo"] = "img/" + sl + ".jpg"; ok += 1
        print("z docs:", name, "->", sl + ".jpg")

json.dump(db, open(os.path.join(ROOT, "public/data/players.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
n_local = sum(1 for p in db["players"] if str(p.get("photo","")).startswith("img/"))
print("Pobrane/lokalne zdjecia:", n_local, "/", len(db["players"]))
print("Nieudane:", fail)
# rozmiar katalogu
tot = sum(os.path.getsize(os.path.join(IMG, f)) for f in os.listdir(IMG))
print("Rozmiar public/img:", round(tot/1024/1024, 1), "MB,", len(os.listdir(IMG)), "plikow")
