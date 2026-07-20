# -*- coding: utf-8 -*-
"""
merge_detail.py - dopisuje pole `detail` (trofea i lata) do graczy w players.json
i WALIDUJE, ze liczba wpisow zgadza sie z `counts` (punktacja). Dzieki temu
"Trofea i lata" nigdy nie rozjada sie z punktami.

Wejscie: plik JSON {"Nazwa gracza": { "<categoryKey>": ["...", ...], ... }, ...}
Dopasowanie nazw odporne na akcenty/wielkosc liter (NFKD + casefold), jak integrate_batch.py.

Format detail wg kategorii:
  - klubowe plaskie (league, natCup, leagueCup, natSupercup, euroSupercup, intercontinental):
      ["Klub: 1999, 2005, 2006", "PSG: 2022, 2023"]  -> liczba LAT (po przecinkach) == counts[key]
  - klubowe z miejscami (ucl, uefa, conference):
      same wygrane: ["Barcelona: 2006, 2009"]; przegrany final z tagiem: ["... (final)"]
      -> #lat-bez-tagu == win, #wpisow "(final)" == final
  - reprezentacyjne (wc, euro, copa): ["2022 (mistrz)", "2014 (final)", "2019 (polfinal)"]
      -> mistrz==win, final==final, polfinal==semi
  - nagrody (ballon, fifa): ["2009 (1.)", "2021 (2.)", "2018 (3.)"]
      -> "1."==first, "2."==second, "3."==third

Format wejscia (dwa warianty per gracz):
  A) tylko detail:  {"Nazwa": {"<categoryKey>": [...], ...}}
  B) audyt+detail:  {"Nazwa": {"counts": {...pelne counts wg Wikipedii...}, "detail": {...}}}
     -> nadpisuje counts, raportuje ROZNICE vs stare + wplyw na punkty, waliduje detail vs NOWE counts.

Uzycie:  python tools/merge_detail.py public/data/players.json path/to/detail.json
         (dodaj --dry-run, aby tylko zwalidowac i pokazac roznice bez zapisu)
"""
import json, sys, re, os, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Wagi czytane WPROST ze scoring.js - zero replik, zero rozjazdu (patrz scoring_weights.py).
from scoring_weights import WEIGHTS, cat_points, TROPHY_KEYS


def counts_diff(old, new):
    """Lista (key, old, new, delta_pkt) dla zmienionych kategorii."""
    out = []
    for key in TROPHY_KEYS:
        o, n = old.get(key), new.get(key)
        if o != n:
            dp = cat_points(key, n) - cat_points(key, o)
            if dp == 0 and cat_points(key, o) == 0 and cat_points(key, n) == 0:
                continue  # pomin strukturalne zera (np. dodanie pustego copa/conference)
            out.append((key, o, n, dp))
    return out

FLAT = {"league", "natCup", "leagueCup", "natSupercup", "euroSupercup", "intercontinental"}
PLACED_CLUB = {"ucl": ["win", "final"], "uefa": ["win", "final"], "conference": ["win", "final"]}
REP = {"wc": ["win", "final", "semi"], "euro": ["win", "final", "semi"], "copa": ["win", "final", "semi"]}
AWARD = {"ballon": ["first", "second", "third"], "fifa": ["first", "second", "third"]}

REP_TAG = {"mistrz": "win", "final": "final", u"finał": "final", "polfinal": "semi", u"półfinał": "semi"}
AWARD_TAG = {"1.": "first", "2.": "second", "3.": "third"}


def norm(s):
    # ł/Ł nie rozkladaja sie w NFKD i gina przy ascii-ignore ("finał"->"fina"); mapuj recznie
    s = s.replace(u"ł", "l").replace(u"Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().casefold().strip()


def count_years(entry):
    # "Klub: 1999, 2005, 2006" -> 3 ; "2022" -> 1
    part = entry.split(":", 1)[1] if ":" in entry else entry
    return len([y for y in re.findall(r"\d{4}", part)])


def validate(name, key, arr, counts):
    """Zwraca liste bledow spojnosci detail[key] vs counts[key]."""
    errs = []
    c = counts.get(key)
    if key in FLAT:
        want = c or 0
        got = sum(count_years(e) for e in arr)
        if got != want:
            errs.append(f"{key}: lat {got} != counts {want}")
    elif key in PLACED_CLUB:
        want = {p: (c or {}).get(p, 0) for p in PLACED_CLUB[key]}
        got = {"win": 0, "final": 0}
        for e in arr:
            m = re.search(r"\(([^)]+)\)", e)
            if m and norm(m.group(1)) == "final":
                got["final"] += 1   # przegrany final LM/PU z tagiem "(finał)"
            else:
                got["win"] += count_years(e)   # same lata = wygrane
        if got != want:
            errs.append(f"{key}: {got} != counts {want}")
    elif key in REP:
        want = {p: (c or {}).get(p, 0) for p in REP[key]}
        got = {"win": 0, "final": 0, "semi": 0}
        for e in arr:
            m = re.search(r"\(([^)]+)\)", e)
            tag = norm(m.group(1)) if m else ""
            slot = {"mistrz": "win", "final": "final", "polfinal": "semi"}.get(tag)
            if slot:
                got[slot] += 1
            else:
                errs.append(f"{key}: nieznany tag w '{e}'")
        if got != want:
            errs.append(f"{key}: {got} != counts {want}")
    elif key in AWARD:
        want = {p: (c or {}).get(p, 0) for p in AWARD[key]}
        got = {"first": 0, "second": 0, "third": 0}
        for e in arr:
            m = re.search(r"\(([123]\.)\)", e)
            slot = AWARD_TAG.get(m.group(1)) if m else None
            if slot:
                got[slot] += 1
            else:
                errs.append(f"{key}: nieznane miejsce w '{e}'")
        if got != want:
            errs.append(f"{key}: {got} != counts {want}")
    else:
        errs.append(f"{key}: nieznana kategoria")
    return errs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    players_path, detail_path = args[0], args[1]
    data = json.load(open(players_path, encoding="utf-8"))
    details = json.load(open(detail_path, encoding="utf-8"))

    by_norm = {norm(p["name"]): p for p in data["players"]}
    all_errs, applied, corrections = [], [], []
    for name, entry in details.items():
        p = by_norm.get(norm(name))
        if not p:
            all_errs.append(f"BRAK gracza: {name}")
            continue
        # Wariant B: {"counts":..., "detail":...}; wariant A: samo detail (mapa kategorii->lista).
        if isinstance(entry, dict) and ("detail" in entry or "counts" in entry):
            new_counts, detail = entry.get("counts"), entry.get("detail", {})
        else:
            new_counts, detail = None, entry
        if new_counts is not None:
            diff = counts_diff(p.get("counts") or {}, new_counts)
            if diff:
                corrections.append((p["name"], diff))
            counts = new_counts
        else:
            counts = p.get("counts") or {}
        for key, arr in detail.items():
            for e in validate(name, key, arr, counts):
                all_errs.append(f"{name} -> {e}")
        if new_counts is not None:
            p["counts"] = new_counts
        p["detail"] = detail
        applied.append(p["name"])

    if corrections:
        print("KOREKTY COUNTS (Wikipedia = zrodlo prawdy):")
        for nm, diff in corrections:
            tot = sum(d[3] for d in diff)
            print(f"  {nm}:")
            for key, o, n, dp in diff:
                print(f"    {key}: {o} -> {n}  ({dp:+g} pkt)")
            print(f"    RAZEM: {tot:+g} pkt")
    if all_errs:
        print("BLEDY SPOJNOSCI (detail vs counts):")
        for e in all_errs:
            print("  -", e)
        print("Nie zapisano. Popraw dane i uruchom ponownie.")
        sys.exit(1)

    print("OK - spojne z counts:", ", ".join(applied))
    if dry:
        print("(--dry-run: bez zapisu)")
        return
    json.dump(data, open(players_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Zapisano", players_path)


if __name__ == "__main__":
    main()
