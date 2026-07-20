# -*- coding: utf-8 -*-
"""
fetch_awards.py - pobiera z angielskiej Wikipedii PODIA (1./2./3. miejsce) nagród indywidualnych
i porównuje je z `counts.ballon` / `counts.fifa` w players.json.

To jest doroczny krok procedury: nowa Złota Piłka (przyznawana zwykle w październiku) i nowa
nagroda The Best (styczeń/luty) -> nowe punkty dla graczy w rankingu ORAZ lista nazwisk
spoza rankingu, które warto rozważyć.

Źródła:
  * "Ballon d'Or"                  - wszystkie edycje 1956-... (w tym FIFA Ballon d'Or 2010-2015)
  * "FIFA World Player of the Year"- edycje 1991-2009
  * "The Best FIFA Men's Player"   - edycje 2016-...
Nagroda połączona 2010-2015 liczy się TYLKO jako `ballon` (nie dublujemy w `fifa`).

Użycie (z katalogu głównego repo):
  python tools/fetch_awards.py                      # raport różnic vs players.json
  python tools/fetch_awards.py --json out.json      # dodatkowo zapis podiów do pliku
  python tools/fetch_awards.py --from-year 2024     # tylko edycje od danego roku (szybki przegląd)
  python tools/fetch_awards.py --apply              # nanieś podia (counts + detail) na players.json

--apply nadpisuje `counts.ballon` / `counts.fifa` oraz `detail.ballon` / `detail.fifa`
danymi z Wikipedii, więc detail z definicji zgadza się z counts (bramka merge_detail.py).
Uwaga: --apply działa tylko na graczy JUŻ obecnych w players.json.
"""
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
import time

API = "https://en.wikipedia.org/w/api.php"
UA = "najlepsi-pilkarze/1.0 (hobbystyczny ranking; https://najlepsipilkarze.tomaszkwietniewski.pl)"

# (kategoria, tytul artykulu, sekcja z tabela, rok_od, rok_do)
# Sekcja jest ISTOTNA: artykul "FIFA World Player of the Year" zawiera tez tabele nagrody KOBIET.
SOURCES = [
    ("ballon", "Ballon d'Or", "Winners", None, None),
    ("fifa", "FIFA World Player of the Year", "FIFA World Player of the Year", None, 2009),
    ("fifa", "The Best FIFA Men's Player", "Winners", 2016, None),
]
PLACES = {"1st": "first", "2nd": "second", "3rd": "third"}


def norm(s):
    s = s.replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().casefold().strip()


def wikitext(title):
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
        except Exception:
            if attempt == 5:
                raise
            time.sleep(4 * (attempt + 1))


def clean_name(cell):
    """'{{flagicon|ARG}} '''[[Lionel Messi]]'''' -> (tytul_artykulu, etykieta).

    Tytul artykulu jest TOZSAMOSCIA gracza - nie wolno obcinac dopisku w nawiasie,
    bo "Luis Suárez (footballer, born 1935)" to inny czlowiek niz "Luis Suárez".
    """
    m = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", cell)
    if not m:
        return None
    target = m.group(1).strip()
    label = (m.group(2) or m.group(1)).strip().strip("' ")
    return target, label


def section_text(wt, heading):
    """Tekst jednej sekcji (bez podsekcji nizszego rzedu az do nastepnego naglowka tego samego poziomu)."""
    m = re.search(r"^(=+)\s*" + re.escape(heading) + r"\s*\1\s*$", wt, re.M)
    if not m:
        return wt
    level = len(m.group(1))
    rest = wt[m.end():]
    nxt = re.search(r"^={1,%d}[^=]" % level, rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def parse_podiums(wt, heading=None, year_from=None, year_to=None):
    """Zwraca [(rok, miejsce, tytul_artykulu, etykieta)] z tabeli edycji nagrody."""
    if heading:
        wt = section_text(wt, heading)
    out, year = [], None
    for line in wt.splitlines():
        if "rowspan" in line:
            years = re.findall(r"(?:19|20)\d{2}", line)
            if years:
                year = int(years[-1])   # etykieta linku (ostatnia liczba) = rok edycji
        pm = re.search(r"\|\s*'*(1st|2nd|3rd)'*\s*$", line.strip())
        if pm and year:
            out.append([year, PLACES[pm.group(1)], None, None])
            continue
        if out and out[-1][2] is None and "[[" in line and year:
            nm = clean_name(line)
            if nm:
                out[-1][2], out[-1][3] = nm
    res = []
    for y, place, target, label in out:
        if target is None:
            continue
        if year_from and y < year_from:
            continue
        if year_to and y > year_to:
            continue
        res.append((y, place, target, label))
    return res


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    from_year = int(argv[argv.index("--from-year") + 1]) if "--from-year" in argv else None
    json_out = argv[argv.index("--json") + 1] if "--json" in argv else None
    players_path = argv[argv.index("--players") + 1] if "--players" in argv else "public/data/players.json"

    tally = {}   # tytul_artykulu -> {"label":..., "ballon": {...}, "fifa": {...}, "lata": [...]}
    for key, title, heading, yf, yt in SOURCES:
        print("Pobieram:", title, flush=True)
        rows = parse_podiums(wikitext(title), heading, yf, yt)
        for year, place, target, label in rows:
            if from_year and year < from_year:
                continue
            t = tally.setdefault(target, {"label": label,
                                          "ballon": {"first": 0, "second": 0, "third": 0},
                                          "fifa": {"first": 0, "second": 0, "third": 0}, "lata": []})
            t[key][place] += 1
            t["lata"].append("%d %s (%s)" % (year, key, place))
        print("  wpisow podium:", len(rows))
        time.sleep(1.5)

    if json_out:
        json.dump(tally, open(json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("Zapisano podia:", json_out)

    data = json.load(open(players_path, encoding="utf-8"))
    # Tozsamosc gracza = TYTUL artykulu na Wikipedii (pole `source`), z fallbackiem na nazwe.
    # Aliasy dla graczy, ktorzy maja w rankingu spolszczona nazwe albo puste `source`.
    ALIAS = {
        "ronaldo (brazilian footballer)": "Ronaldo (R9)",
        "andriy shevchenko": "Andrij Szewczenko",
        "pep guardiola": "Pep Guardiola",
        "dennis bergkamp": "Denis Bergkamp",
    }
    by = {}
    for p in data["players"]:
        by[norm(p["name"])] = p
        src = p.get("source") or ""
        if "/wiki/" in src:
            by[norm(urllib.parse.unquote(src.rsplit("/wiki/", 1)[1]).replace("_", " "))] = p
    for k, v in ALIAS.items():
        hit = next((p for p in data["players"] if p["name"] == v), None)
        if hit:
            by[k] = hit

    print("\n=== ROZBIEZNOSCI vs players.json (gracze W rankingu) ===")
    diffs, delta_total = 0, 0.0
    W = {"first": 5, "second": 3, "third": 1}
    for target, t in sorted(tally.items()):
        p = by.get(norm(target))
        if not p:
            continue
        for cat in ("ballon", "fifa"):
            cur = (p.get("counts") or {}).get(cat) or {}
            want = t[cat]
            if any((cur.get(k, 0) or 0) != want[k] for k in want):
                diffs += 1
                dp = sum((want[k] - (cur.get(k, 0) or 0)) * W[k] for k in W)
                delta_total += dp
                print("  %-24s %-7s obecnie %s -> Wikipedia %s  (%+g pkt)  [%s]" % (
                    p["name"], cat,
                    {k: cur.get(k, 0) or 0 for k in ("first", "second", "third")},
                    want, dp, ", ".join(x for x in t["lata"] if x.split()[1] == cat)))
    if not diffs:
        print("  brak - wszystko zgodne")
    else:
        print("  RAZEM: %d rozbieznosci, wplyw %+g pkt" % (diffs, delta_total))

    if "--apply" in argv and diffs:
        LABEL = {"first": "1.", "second": "2.", "third": "3."}
        ORDER = {"first": 0, "second": 1, "third": 2}
        applied = []
        for target, t in tally.items():
            p = by.get(norm(target))
            if not p:
                continue
            changed = False
            for cat in ("ballon", "fifa"):
                cur = (p.get("counts") or {}).get(cat) or {}
                want = t[cat]
                if all((cur.get(k, 0) or 0) == want[k] for k in want):
                    continue
                p.setdefault("counts", {})[cat] = dict(want)
                rows = []
                for entry in t["lata"]:
                    year, kind, place = entry.split()
                    if kind != cat:
                        continue
                    place = place.strip("()")
                    rows.append((ORDER[place], int(year), "%s (%s)" % (year, LABEL[place])))
                p.setdefault("detail", {})[cat] = [r[2] for r in sorted(rows)]
                if not p["detail"][cat]:
                    p["detail"].pop(cat, None)
                changed = True
            if changed:
                applied.append(p["name"])
        json.dump(data, open(players_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nZAPISANO %s - zaktualizowano podia u %d graczy: %s"
              % (players_path, len(applied), ", ".join(sorted(applied))))

    print("\n=== PODIA GRACZY SPOZA RANKINGU (kandydaci do rozwazenia) ===")
    outside = []
    for target, t in tally.items():
        if norm(target) in by:
            continue
        pts = sum(t[c][k] * W[k] for c in ("ballon", "fifa") for k in W)
        outside.append((pts, t["label"], t["lata"]))
    for pts, name, lata in sorted(outside, reverse=True)[:25]:
        print("  %5.0f pkt z nagrod  %-26s %s" % (pts, name, ", ".join(lata)))


if __name__ == "__main__":
    main()
