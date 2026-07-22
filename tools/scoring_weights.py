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


def load_league_mult(path=None):
    """Mnoznik sily ligi z scoring.js (klucze juz w cudzyslowach: "Anglia": 1.0)."""
    src = open(path or _SCORING_JS, encoding="utf-8").read()
    m = re.search(r"var\s+LEAGUE_MULT\s*=\s*(\{.*?\n\s*\});", src, re.S)
    if not m:
        return {}
    body = re.sub(r"//[^\n]*", "", m.group(1))
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    return json.loads(body)


WEIGHTS = load_weights()
LEAGUE_MULT = load_league_mult()
NATIONAL_KEYS = {"league", "natCup", "leagueCup", "natSupercup"}


def league_mult(lg):
    return LEAGUE_MULT.get(lg, 1)


def national_points(key, by_league_for_key):
    """Punkty krajowej kategorii z rozbicia per liga: suma liczba x waga_bazowa x mnoznik."""
    base = WEIGHTS[key]
    return sum((n or 0) * base * league_mult(lg) for lg, n in (by_league_for_key or {}).items())


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
    """Suma punktów gracza - odpowiednik scorePlayer() ze scoring.js (styl "counts").
    Kategorie krajowe z pola byLeague liczone z mnoznikiem ligi; reszta plasko."""
    app = (p.get("appearances") or 0) / WEIGHTS["appearancesPer"]
    div = WEIGHTS["goalDivisor"].get(p.get("position"), WEIGHTS["goalDivisor"]["FWD"])
    goals = (p.get("goals") or 0) / div
    counts = p.get("counts") or {}
    by = p.get("byLeague") or {}
    total = app + goals
    for k in TROPHY_KEYS:
        if k in NATIONAL_KEYS and by.get(k):
            total += national_points(k, by[k])
        else:
            total += cat_points(k, counts.get(k))
    return total
