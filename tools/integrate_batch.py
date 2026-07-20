# -*- coding: utf-8 -*-
# Wpina batch (styl "counts", final methodology) do players.json.
# Dopasowanie po nazwie odporne na akcenty/wielkosc liter; zachowuje istniejace 'photo'.
import json, sys, unicodedata, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # katalog repo (dziala tez w git worktree)
batch_path = sys.argv[1]

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).casefold().strip()

db = json.load(open(os.path.join(ROOT,"public/data/players.json"), encoding="utf-8"))
players = db["players"]
idx = {}
for i,p in enumerate(players): idx.setdefault(norm(p["name"]), []).append(i)

batch = json.load(open(batch_path, encoding="utf-8"))
added=0; replaced=0; remove=set()
for e in batch:
    entry = {"name": e["name"], "position": e["position"], "appearances": e["appearances"],
             "goals": e["goals"], "style": "counts", "counts": e["counts"],
             "dataComplete": True, "source": e.get("src", e.get("source","")), "notes": e.get("notes","")}
    key = norm(e["name"])
    if key in idx:
        first = idx[key][0]
        if players[first].get("photo"): entry["photo"] = players[first]["photo"]
        players[first] = entry; replaced += 1
        for extra in idx[key][1:]: remove.add(extra)
    else:
        players.append(entry); added += 1
players = [p for i,p in enumerate(players) if i not in remove]
db["players"] = players
json.dump(db, open(os.path.join(ROOT,"public/data/players.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)

W={"wc":{"win":12,"final":8,"semi":6},"euro":{"win":9,"final":7,"semi":5},"copa":{"win":4.5,"final":3.5,"semi":2.5},
   "league":5,"natCup":3,"leagueCup":1,"natSupercup":1,"ucl":{"win":8,"final":5},"uefa":{"win":5,"final":3},
   "conference":{"win":2.5,"final":1.5},"euroSupercup":2,"intercontinental":2,
   "ballon":{"first":5,"second":3,"third":1},"fifa":{"first":5,"second":3,"third":1}}
GD={"GK":17,"DEF":3,"MID":8,"FWD":17}
def cp(k,v):
    w=W[k]; return (v or 0)*w if isinstance(w,(int,float)) else (sum((v.get(pl,0)or 0)*w[pl] for pl in w) if isinstance(v,dict) else 0)
def tot(p):
    t=p.get("appearances",0)/35+p.get("goals",0)/GD[p["position"]]
    return t+(sum(p["pts"].values()) if p.get("style")=="legacy" else sum(cp(k,p["counts"].get(k)) for k in W))
comp=sorted([p for p in players if p.get("dataComplete")],key=tot,reverse=True)
print(f"Podmieniono {replaced}, dodano {added}. Razem {len(players)}, sklasyfikowanych {len(comp)}, WIP {sum(1 for p in players if not p.get('dataComplete'))}")
bn={norm(e['name']) for e in batch}
print("Pozycje wpietych:")
for i,p in enumerate(comp,1):
    if norm(p['name']) in bn: print(f'  #{i}  {tot(p):6.1f}  {p["name"]}')
