# -*- coding: utf-8 -*-
# Konwersja legacy (punkty) -> counts (liczby zdobyc), dekodujac wg STARYCH wag.
import json, itertools, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # katalog repo (dziala tez w git worktree)
db = json.load(open(os.path.join(ROOT, "public/data/players.json"), encoding="utf-8"))

# stare wagi, ktorymi liczono punkty w arkuszu
OLD = {
    "wc":   [("win",10),("final",8),("semi",6)],
    "euro": [("win",9),("final",7),("semi",5)],
    "ucl":  [("win",7),("final",5)],
    "uefa": [("win",5),("final",3)],
    "ballon":[("first",5),("second",3),("third",1)],
    "fifa": [("first",5),("second",3),("third",1)],
}
FLAT = {"league":5,"natCup":3,"leagueCup":1,"natSupercup":1,"euroSupercup":2,"intercontinental":2}

def decode(V, weights):
    """Znajdz counts (dict) sumujace do V, minimalizujac liczbe zdobyc; preferuj wyzsze wagi."""
    V = int(round(V or 0))
    if V == 0: return {k:0 for k,_ in weights}
    best = None
    ws = [w for _,w in weights]
    lim = [V//w + 1 for w in ws]
    for combo in itertools.product(*[range(l+1) for l in lim]):
        if sum(c*w for c,w in zip(combo,ws)) == V:
            cnt = sum(combo)
            # klucz: min liczba, potem wiecej wyzszych wag (combo[0] wieksze)
            key = (cnt, tuple(-c for c in combo))
            if best is None or key < best[0]:
                best = (key, combo)
    if best is None:
        # brak dokladnego rozkladu - najwyzsza waga + reszta pominmieta
        return {k:0 for k,_ in weights}
    return {weights[i][0]: best[1][i] for i in range(len(weights))}

converted = 0
issues = []
for p in db["players"]:
    if p.get("style") != "legacy":
        continue
    pts = p.get("pts", {})
    counts = {}
    for cat, weights in OLD.items():
        counts[cat] = decode(pts.get(cat,0), weights)
        # kontrola: czy dekodowanie odtwarza punkty
        rec = sum(counts[cat][k]*w for k,w in weights)
        if rec != int(round(pts.get(cat,0) or 0)):
            issues.append((p["name"], cat, pts.get(cat), rec))
    for k,w in FLAT.items():
        val = pts.get(k,0) or 0
        counts[k] = int(round(val / w))
    counts["copa"] = {"win":0,"final":0,"semi":0}
    counts["conference"] = {"win":0,"final":0}
    p["style"] = "counts"
    p["counts"] = counts
    p.pop("pts", None)
    converted += 1

json.dump(db, open(os.path.join(ROOT, "public/data/players.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("Skonwertowano legacy->counts:", converted)
print("Problemy dekodowania:", issues if issues else "brak")

# przelicz NOWYMI wagami
W={"wc":{"win":12,"final":8,"semi":6},"euro":{"win":9,"final":7,"semi":5},"copa":{"win":4.5,"final":3.5,"semi":2.5},
   "league":5,"natCup":3,"leagueCup":1,"natSupercup":1,"ucl":{"win":8,"final":5},"uefa":{"win":5,"final":3},
   "conference":{"win":2.5,"final":1.5},"euroSupercup":2,"intercontinental":2,
   "ballon":{"first":5,"second":3,"third":1},"fifa":{"first":5,"second":3,"third":1}}
GD={"GK":17,"DEF":3,"MID":8,"FWD":17}
def cp(k,v):
    w=W[k]; return (v or 0)*w if isinstance(w,(int,float)) else (sum((v.get(pl,0)or 0)*w[pl] for pl in w) if isinstance(v,dict) else 0)
def tot(p):
    return p.get("appearances",0)/35 + p.get("goals",0)/GD[p["position"]] + sum(cp(k,p["counts"].get(k)) for k in W)
comp=sorted([p for p in db["players"] if p.get("dataComplete")],key=tot,reverse=True)
print("\nCZOLOWKA po nowych wagach (top 15):")
for i,p in enumerate(comp[:15],1):
    print(f'  {i:2d}. {tot(p):6.1f}  {p["position"]:3s}  {p["name"]}')
