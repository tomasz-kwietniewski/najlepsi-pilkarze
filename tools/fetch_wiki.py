# -*- coding: utf-8 -*-
"""
fetch_wiki.py - pobiera z angielskiej Wikipedii dane potrzebne do dorocznej aktualizacji rankingu:
  * sekcje "Honours" (trofea) -> <out>/honours/<slug>.txt
  * dane z infoboksu: wystepy/gole w reprezentacji (caps), kluby i lata -> <out>/infobox.json

Uzycie (z katalogu glownego repo):
  python tools/fetch_wiki.py --out tmp/wiki --active
  python tools/fetch_wiki.py --out tmp/wiki --names "Pedri|Nico Williams"
  python tools/fetch_wiki.py --out tmp/wiki --titles "Pedri|Nico_Williams"   (gracze spoza players.json)

  --active  bierze graczy z players.json majacych active:true
  --names   bierze wskazanych graczy z players.json (tytul Wiki z pola source)
  --titles  bierze tytuly artykulow Wikipedii wprost (kandydaci jeszcze nieobecni w rankingu)

Wikipedia rate-limituje szybkie zapytania (HTTP 429) - skrypt robi przerwy i retry.
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

API = "https://en.wikipedia.org/w/api.php"
UA = "najlepsi-pilkarze/1.0 (hobbystyczny ranking; https://najlepsipilkarze.tomaszkwietniewski.pl)"
PAUSE = 2.0  # sekundy miedzy zapytaniami


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def api_wikitext(title):
    url = API + "?" + urllib.parse.urlencode(
        {"action": "parse", "page": title, "prop": "wikitext", "format": "json", "redirects": "1"}
    )
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            if "error" in data:
                raise RuntimeError(data["error"].get("info", "blad API"))
            return data["parse"]["wikitext"]["*"]
        except Exception as e:
            if attempt == 5:
                raise
            time.sleep(4 * (attempt + 1))  # retry m.in. na HTTP 429


def title_from_source(url, name):
    if url and "/wiki/" in url:
        return urllib.parse.unquote(url.rsplit("/wiki/", 1)[1])
    return name.replace(" ", "_")


def honours_section(wikitext):
    """Tekst sekcji Honours (do nastepnego naglowka tego samego poziomu)."""
    m = re.search(r"^==\s*Honou?rs\s*==\s*$", wikitext, re.M | re.I)
    if not m:
        return ""
    rest = wikitext[m.end():]
    nxt = re.search(r"^==[^=]", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def num(val):
    """Wyluskuje liczbe z pola infoboksu: '{{0}}12', '[[...|191]]', '191<ref .../>' -> int."""
    if val is None:
        return None
    v = re.sub(r"<ref[^>]*?/>|<ref.*?</ref>", "", val, flags=re.S)
    v = re.sub(r"<!--.*?-->", "", v, flags=re.S)
    v = re.sub(r"\{\{0+\}\}", "", v)          # {{0}} to wyrownanie kolumn, nie liczba
    v = v.split("|")[-1].replace("]", "").replace("[", "")
    nums = re.findall(r"\d+", v)
    return int(nums[-1]) if nums else None


def field(wikitext, key):
    m = re.search(r"^\s*\|\s*" + key + r"\s*=([^\n]*)$", wikitext, re.M)
    return m.group(1).strip() if m else None


def infobox(wikitext):
    """Reprezentacja (ostatni wpis = seniorska kadra A) + kluby z latami (do statusu aktywnosci)."""
    out = {"natApp": None, "natGoals": None, "natTeam": None, "clubs": [], "currentClub": None}
    best_idx = -1
    for i in range(1, 12):
        team = field(wikitext, "nationalteam%d" % i)
        if not team:
            continue
        # pomijamy kadry mlodziezowe/olimpijskie - liczy sie seniorska (zwykle bez U.. w nazwie)
        if re.search(r"U-?\d{2}|Olympic|Youth", team, re.I):
            continue
        caps = num(field(wikitext, "nationalcaps%d" % i))
        if caps is None:
            continue
        if i > best_idx:
            best_idx = i
            out["natTeam"] = re.sub(r"[\[\]]", "", team).split("|")[-1].strip()
            out["natApp"] = caps
            out["natGoals"] = num(field(wikitext, "nationalgoals%d" % i)) or 0
    for i in range(1, 20):
        club = field(wikitext, "clubs%d" % i)
        if not club:
            continue
        years = field(wikitext, "years%d" % i) or ""
        years = re.sub(r"<!--.*?-->", "", years, flags=re.S).strip()
        out["clubs"].append(
            {
                "club": re.sub(r"[\[\]']", "", club).split("|")[-1].strip(),
                "years": years,
                "caps": num(field(wikitext, "caps%d" % i)),
                "goals": num(field(wikitext, "goals%d" % i)),
            }
        )
    cc = field(wikitext, "currentclub")
    if cc:
        out["currentClub"] = re.sub(r"[\[\]']", "", cc).split("|")[-1].strip()
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]

    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    out_dir = opt("--out", "tmp/wiki")
    players_path = opt("--players", "public/data/players.json")

    targets = []  # (nazwa wyswietlana, tytul Wiki)
    if "--titles" in argv:
        for t in opt("--titles").split("|"):
            targets.append((t.replace("_", " "), t))
    else:
        data = json.load(open(players_path, encoding="utf-8"))
        want = None
        if "--names" in argv:
            want = {n.strip().casefold() for n in opt("--names").split("|")}
        for p in data["players"]:
            if "--active" in argv and not p.get("active"):
                continue
            if want is not None and p["name"].casefold() not in want:
                continue
            targets.append((p["name"], title_from_source(p.get("source", ""), p["name"])))

    if not targets:
        print("Brak graczy do pobrania (podaj --active, --names albo --titles).")
        sys.exit(1)

    os.makedirs(os.path.join(out_dir, "honours"), exist_ok=True)
    box = {}
    for i, (name, title) in enumerate(targets, 1):
        print("[%d/%d] %s (%s)" % (i, len(targets), name, title), flush=True)
        wt = api_wikitext(title)
        h = honours_section(wt)
        with open(os.path.join(out_dir, "honours", slug(name) + ".txt"), "w", encoding="utf-8") as f:
            f.write("# " + name + " | " + title + "\n\n" + h)
        box[name] = infobox(wt)
        box[name]["title"] = title
        box[name]["honoursChars"] = len(h)
        time.sleep(PAUSE)

    with open(os.path.join(out_dir, "infobox.json"), "w", encoding="utf-8") as f:
        json.dump(box, f, ensure_ascii=False, indent=1)
    print("\nZapisano: %s/honours/*.txt oraz %s/infobox.json" % (out_dir, out_dir))


if __name__ == "__main__":
    main()
