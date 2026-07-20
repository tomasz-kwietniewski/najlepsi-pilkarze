# -*- coding: utf-8 -*-
"""
add_players.py - dodaje NOWYCH piłkarzy do players.json (krok 7 procedury aktualizacji).

W odróżnieniu od integrate_batch.py obsługuje pełny, dzisiejszy schemat rekordu:
`detail`, `natApp`, `natGoals`, `active` - i przepuszcza `detail` przez tę samą walidację
co merge_detail.py (liczba lat w detail musi zgadzać się z counts).

Wejście: JSON {"Nazwa": {position, appearances, goals, natApp, natGoals, source, counts, detail,
                         active?, notes?}}

Użycie:
  python tools/add_players.py public/data/players.json tmp/nowi.json --dry-run
  python tools/add_players.py public/data/players.json tmp/nowi.json
  python tools/add_players.py public/data/players.json tmp/nowi.json --min-points 100

--min-points odrzuca kandydatów poniżej progu (patrz spec/PROCEDURA-AKTUALIZACJI.md, krok 7)
i wypisuje ich z wyliczonym wynikiem, żeby było widać, kto był blisko.
"""
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scoring_weights import score_player
from merge_detail import validate, norm


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    sys.stdout.reconfigure(encoding="utf-8")   # nazwiska maja diakrytyki (İlkay Gündoğan)
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry-run" in argv
    min_pts = float(argv[argv.index("--min-points") + 1]) if "--min-points" in argv else None

    data = json.load(open(args[0], encoding="utf-8"))
    new = json.load(open(args[1], encoding="utf-8"))
    existing = {norm(p["name"]) for p in data["players"]}

    errs, added, skipped = [], [], []
    for name, e in new.items():
        if norm(name) in existing:
            errs.append("%s: juz jest w rankingu" % name)
            continue
        rec = {
            "name": name,
            "position": e["position"],
            "appearances": e["appearances"],
            "goals": e["goals"],
            "style": "counts",
            "dataComplete": True,
            "source": e.get("source", ""),
            "notes": e.get("notes", ""),
            "photo": "img/%s.jpg" % slug(name),
            "counts": e["counts"],
            "detail": {k: v for k, v in (e.get("detail") or {}).items() if isinstance(v, list) and v},
            "natApp": e.get("natApp", 0),
            "natGoals": e.get("natGoals", 0),
        }
        if e.get("active"):
            rec["active"] = True

        for key, arr in rec["detail"].items():
            for msg in validate(name, key, arr, rec["counts"]):
                errs.append("%s -> %s" % (name, msg))
        if rec["natApp"] > rec["appearances"] or rec["natGoals"] > rec["goals"]:
            errs.append("%s: kadra wieksza niz suma wystepow/goli" % name)

        pts = score_player(rec)
        if min_pts is not None and pts < min_pts:
            skipped.append((pts, name))
            continue
        added.append((pts, rec))

    if errs:
        print("BLEDY (nic nie zapisano):")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    if skipped:
        print("PONIZEJ PROGU %g pkt - pominieci:" % min_pts)
        for pts, name in sorted(skipped, reverse=True):
            print("   %6.1f  %s" % (pts, name))

    print("\nDODAWANI:")
    for pts, rec in sorted(added, reverse=True, key=lambda x: x[0]):
        print("   %6.1f  %-24s %s" % (pts, rec["name"], rec["photo"]))
        data["players"].append(rec)

    if dry:
        print("\n(--dry-run: bez zapisu)")
        return
    json.dump(data, open(args[0], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nZapisano %s - graczy w rankingu: %d" % (args[0], len(data["players"])))
    print("PAMIETAJ o zdjeciach: python tools/fetch_photos.py")


if __name__ == "__main__":
    main()
