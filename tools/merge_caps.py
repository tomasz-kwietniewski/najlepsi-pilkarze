# -*- coding: utf-8 -*-
"""Dopisuje natApp/natGoals (wystepy i gole w reprezentacji) do graczy w players.json.
Klub wyliczany na stronie jako appearances-natApp / goals-natGoals, wiec WALIDUJEMY,
ze natApp<=appearances i natGoals<=goals (inaczej klub wyszedlby ujemny).

Wejscie: JSON {"Nazwa": {"natApp": N, "natGoals": M, "natTeam": "..."}, ...}
  - pasuje wprost plik `infobox.json` z tools/fetch_wiki.py (doroczna aktualizacja).
Dopasowanie nazw odporne na akcenty/wielkosc liter (NFKD+casefold, ł->l).

Uzycie: python tools/merge_caps.py public/data/players.json caps.json [--dry-run] [--bump]

  --bump  DOROCZNA AKTUALIZACJA: przyrost wystepow/goli w kadrze (np. po mundialu) dolicza
          takze do `appearances`/`goals`, bo suma = klub + reprezentacja. Bez tej flagi
          zmienia sie tylko natApp/natGoals (czyli rozbicie klub/kadra), a suma zostaje.
          Uwaga: --bump zaklada, ze wystepy KLUBOWE sie nie zmienily (sezon klubowy zamkniety).
"""
import json, sys, unicodedata

def norm(s):
    s = s.replace(u"ł", "l").replace(u"Ł", "L")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().casefold().strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    bump = "--bump" in sys.argv
    data = json.load(open(args[0], encoding="utf-8"))
    caps = json.load(open(args[1], encoding="utf-8"))
    by_norm = {norm(p["name"]): p for p in data["players"]}
    errs, applied = [], []
    for name, v in caps.items():
        p = by_norm.get(norm(name))
        if not p:
            errs.append("BRAK gracza: " + name); continue
        na, ng = v.get("natApp"), v.get("natGoals")
        if na is None:
            errs.append(name + ": brak natApp (nie pobrano)"); continue
        d_app = na - (p.get("natApp") or 0)
        d_goals = (ng - (p.get("natGoals") or 0)) if ng is not None else 0
        if bump and d_app < 0:
            errs.append("%s: natApp spadlo %d -> %d (podejrzane, pomijam)"
                        % (name, p.get("natApp") or 0, na)); continue
        base_app = (p.get("appearances") or 0) + (d_app if bump else 0)
        base_goals = (p.get("goals") or 0) + (d_goals if bump else 0)
        if na > base_app:
            errs.append("%s: natApp %d > appearances %d" % (name, na, base_app)); continue
        if ng is not None and ng > base_goals:
            errs.append("%s: natGoals %d > goals %d" % (name, ng, base_goals)); continue
        if bump and (d_app or d_goals):
            p["appearances"], p["goals"] = base_app, base_goals
        p["natApp"] = na
        if ng is not None:
            p["natGoals"] = ng
        if d_app or d_goals:
            applied.append("%s (kadra %d wyst/%dg; %+d wyst, %+d goli)"
                           % (p["name"], na, ng if ng is not None else 0, d_app, d_goals))
    if errs:
        print("BLEDY:")
        for e in errs:
            print("  -", e)
        if not applied:
            sys.exit(1)
    print("OK:", "; ".join(applied))
    if dry:
        print("(--dry-run: bez zapisu)"); return
    json.dump(data, open(args[0], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Zapisano", args[0])

if __name__ == "__main__":
    main()
