# -*- coding: utf-8 -*-
"""
scoring_weights.py - czyta wagi punktacji WPROST z `public/scoring.js`.

Powód: wcześniej każdy skrypt w tools/ miał własną kopię WEIGHTS i kopie się rozjechały
(po zmianie ME 9 -> 10 i Copa 4,5 -> 5 w scoring.js skrypty nadal liczyły po staremu).
`public/scoring.js` jest jedynym źródłem prawdy - tutaj tylko go parsujemy.

Użycie:
    from scoring_weights import WEIGHTS, score_player, cat_points
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCORING_JS = os.path.join(_HERE, "..", "public", "scoring.js")


def load_weights(path=None):
    src = open(path or _SCORING_JS, encoding="utf-8").read()
    m = re.search(r"var\s+WEIGHTS\s*=\s*(\{.*?\n\s*\});", src, re.S)
    if not m:
        raise RuntimeError("Nie znaleziono obiektu WEIGHTS w scoring.js")
    body = m.group(1)
    body = re.sub(r"//[^\n]*", "", body)                  # komentarze
    body = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', body)  # klucze w cudzysłowy
    body = re.sub(r",(\s*[}\]])", r"\1", body)            # wiszące przecinki
    return json.loads(body)


WEIGHTS = load_weights()


def cat_points(key, val):
    """Punkty za jedną kategorię trofeów (val: liczba albo {win/final/semi} / {first/second/third})."""
    if val is None:
        return 0
    w = WEIGHTS[key]
    if isinstance(w, (int, float)):
        return (val or 0) * w
    return sum((val.get(p, 0) or 0) * wt for p, wt in w.items())


TROPHY_KEYS = ["wc", "euro", "copa", "league", "natCup", "leagueCup", "natSupercup",
               "ucl", "uefa", "conference", "euroSupercup", "intercontinental", "ballon", "fifa"]


def score_player(p):
    """Suma punktów gracza - odpowiednik scorePlayer() ze scoring.js (styl "counts")."""
    app = (p.get("appearances") or 0) / WEIGHTS["appearancesPer"]
    div = WEIGHTS["goalDivisor"].get(p.get("position"), WEIGHTS["goalDivisor"]["FWD"])
    goals = (p.get("goals") or 0) / div
    counts = p.get("counts") or {}
    return app + goals + sum(cat_points(k, counts.get(k)) for k in TROPHY_KEYS)
