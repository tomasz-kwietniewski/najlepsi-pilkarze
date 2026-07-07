# -*- coding: utf-8 -*-
"""Dopisuje pole `active` (true = piłkarz wciąż gra) do graczy w players.json.
Wejście: JSON {"Nazwa": {"active": bool, "lastClub":..., "lastYears":...}, ...} (z fetch_active.py).
Dodaje active tylko gdy True (emeryci bez pola - render traktuje brak jako nieaktywny).
Uzycie: python tools/merge_active.py public/data/players.json active.json [--dry-run]
"""
import json, sys, unicodedata

def norm(s):
    s = s.replace(u"ł", "l").replace(u"Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().casefold().strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    data = json.load(open(args[0], encoding="utf-8"))
    act = json.load(open(args[1], encoding="utf-8"))
    by_norm = {norm(p["name"]): p for p in data["players"]}
    active_list, unknown = [], []
    for name, v in act.items():
        p = by_norm.get(norm(name))
        if not p:
            unknown.append(name); continue
        if v.get("active") is None:
            unknown.append(name + " (brak danych: " + str(v.get("lastYears")) + ")"); continue
        if v.get("active"):
            p["active"] = True
            active_list.append(p["name"] + " [" + str(v.get("lastClub")) + " " + str(v.get("lastYears")) + "]")
        else:
            p.pop("active", None)  # emeryt - usun ewentualne stare
    print("AKTYWNI (%d):" % len(active_list))
    for a in sorted(active_list):
        print("  +", a)
    if unknown:
        print("BEZ DANYCH / nierozpoznani:")
        for u in unknown:
            print("  ?", u)
    if dry:
        print("(--dry-run: bez zapisu)"); return
    json.dump(data, open(args[0], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Zapisano", args[0])

if __name__ == "__main__":
    main()
