# -*- coding: utf-8 -*-
"""Dodaje pole byLeague (rozbicie 4 krajowych trofeow per liga) do players.json.
Zrodlem jest pole detail (Klub: lata). Waliduje, ze sumy == counts."""
import json, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "public", "data", "players.json")
CATS = ["league", "natCup", "leagueCup", "natSupercup"]

CLUB2LEAGUE = [
 (re.compile(r"Manchester United|Manchester City|Chelsea|Arsenal|Liverpool|Leicester|Blackburn|Leeds|Tottenham|Everton|Middlesbrough|Aston Villa|Portsmouth|Wigan|Southampton|Sunderland|Newcastle|Nottingham", re.I), "Anglia"),
 (re.compile(r"Barcelona|Real Madryt|Atl[eé]tico|Atletico|Valencia|Deportivo|Sevilla|Villarreal|Mallorca|Zaragoza|Real Sociedad|Betis|Athletic|Espanyol|Celta", re.I), "Hiszpania"),
 (re.compile(r"Juventus|Milan|Inter|Napoli|Lazio|Roma|Sampdoria|Fiorentina|Parma|Bologna|Torino|Atalanta", re.I), "Włochy"),
 (re.compile(r"Bayern|Dortmund|Werder|Stuttgart|Kaiserslautern|Wolfsburg|Leverkusen|Bayer\b|Schalke|Borussia M|Eintracht|Hamburg|Lipsk|Leipzig", re.I), "Niemcy"),
 (re.compile(r"PSG|Paris|Lyon|Marsyli|Marseille|Olympique|Monaco|Bordeaux|Lille|Nantes|Lens|Auxerre|Montpellier|Saint-Germain|Saint-[EÉ]tienne|Nancy|Rennes|Strasbourg|Guingamp|Sochaux|Nicea|Nice", re.I), "Francja"),
 (re.compile(r"Porto|Benfica|Sporting|Boavista|Braga|Vit[oó]ria", re.I), "Portugalia"),
 (re.compile(r"Ajax|PSV|Feyenoord|Twente|\bAZ\b|Eindhoven|Utrecht|Vitesse", re.I), "Holandia"),
]
def club_to_league(club):
    for rx, lg in CLUB2LEAGUE:
        if rx.search(club): return lg
    return None

def main():
    data = json.load(open(PATH, encoding="utf-8"))
    players = data["players"]
    unknown, mism = set(), []
    for p in players:
        detail = p.get("detail") or {}
        counts = p.get("counts") or {}
        by = {}
        for k in CATS:
            per = {}
            for entry in (detail.get(k) or []):
                i = entry.rfind(":")
                club = entry[:i].strip()
                years = [y for y in entry[i+1:].split(",") if y.strip()]
                lg = club_to_league(club)
                if lg is None: unknown.add(club + " [" + k + "]")
                per[lg] = per.get(lg, 0) + len(years)
            if per:
                total = sum(per.values())
                if total != (counts.get(k) or 0):
                    mism.append((p["name"], k, total, counts.get(k) or 0))
                by[k] = {lg: n for lg, n in per.items() if lg is not None}
        if by:
            p["byLeague"] = by
    print("Nierozpoznane kluby:", " | ".join(sorted(unknown)) if unknown else "BRAK")
    print("Niezgodnosci suma vs counts:", len(mism))
    for m in mism: print("  ", m)
    if unknown or mism:
        print("PRZERWANO - napraw mapowanie/dane przed zapisem."); sys.exit(1)
    json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Zapisano byLeague dla", sum(1 for p in players if "byLeague" in p), "graczy.")

if __name__ == "__main__":
    main()
