/*
 * scoring.js - jedyne zrodlo prawdy o punktacji rankingu "Najlepsi pilkarze".
 *
 * Bierze surowy obiekt gracza i zwraca rozbicie punktow + sume.
 * Zmiana wagi = zmiana jednej liczby w WEIGHTS, bez ruszania danych.
 *
 * Dwa style danych wejsciowych (pole "style"):
 *   - "legacy": trofea trzymane juz jako PUNKTY (migracja z arkusza 2010).
 *   - "counts": trofea trzymane jako LICZBY zdobyc; punkty liczy ten plik z WEIGHTS.
 * Oba style daja ten sam ksztalt wyniku, wiec raport traktuje je jednakowo.
 */
(function (global) {
  "use strict";

  var WEIGHTS = {
    appearancesPer: 35,               // 1 pkt za 35 wystepow
    goalDivisor: { GK: 17, DEF: 3, MID: 8, FWD: 17 }, // 1 pkt za N goli wg pozycji
    wc: { win: 12, final: 8, semi: 6 },   // MS (1. miejsce podniesione 10 -> 12)
    euro: { win: 10, final: 7, semi: 5 }, // ME (1. miejsce podniesione 9 -> 10)
    copa: { win: 5, final: 3.5, semi: 2.5 }, // Copa America = polowa wag ME
    league: 5,          // mistrzostwo kraju (za kazde; TYLKO top ligi: Anglia/Hiszpania/Wlochy/Niemcy/Francja/Portugalia/Holandia)
    natCup: 3,          // puchar kraju
    leagueCup: 1,       // puchar ligi krajowej
    natSupercup: 1,     // superpuchar kraju
    ucl: { win: 8, final: 5 },   // Liga Mistrzow (zwyciestwo podniesione 7 -> 8)
    uefa: { win: 5, final: 3 },  // Puchar UEFA/Liga Europy + Puchar Zdobywcow Pucharow
    conference: { win: 2.5, final: 1.5 }, // Liga Konferencji = polowa Pucharu UEFA
    euroSupercup: 2,    // Superpuchar Europy
    intercontinental: 2,// Puchar Interkontynentalny (+ Klubowe MS)
    ballon: { first: 5, second: 3, third: 1 }, // Zlota Pilka France Football
    fifa: { first: 5, second: 3, third: 1 }    // Pilkarz Roku FIFA / The Best
  };

  // Kolejnosc i etykiety kategorii w rozbiciu (poza wystepami i golami).
  var CATEGORIES = [
    { key: "wc",              label: "Mistrzostwa Swiata" },
    { key: "euro",            label: "Mistrzostwa Europy" },
    { key: "copa",            label: "Copa America" },
    { key: "league",          label: "Mistrzostwo kraju" },
    { key: "natCup",          label: "Puchar kraju" },
    { key: "leagueCup",       label: "Puchar ligi" },
    { key: "natSupercup",     label: "Superpuchar kraju" },
    { key: "ucl",             label: "Liga Mistrzow" },
    { key: "uefa",            label: "Puchar UEFA / ZP" },
    { key: "conference",      label: "Liga Konferencji" },
    { key: "euroSupercup",    label: "Superpuchar Europy" },
    { key: "intercontinental",label: "Puchar Interkontynentalny / Klubowe MS" },
    { key: "ballon",          label: "Zlota Pilka" },
    { key: "fifa",            label: "Pilkarz Roku FIFA / The Best" }
  ];

  // Zwraca liczbe punktow dla jednej kategorii na podstawie LICZB (style "counts").
  function pointsForCount(key, val) {
    if (val == null) return 0;
    var w = WEIGHTS[key];
    if (typeof w === "number") {
      // kategoria plaska: val to liczba zdobyc
      return (val || 0) * w;
    }
    // kategoria z miejscami: val to obiekt {win/final/semi} albo {first/second/third}
    var sum = 0;
    for (var place in w) {
      if (w.hasOwnProperty(place) && val[place]) sum += val[place] * w[place];
    }
    return sum;
  }

  function goalDivisor(position) {
    return WEIGHTS.goalDivisor[position] || WEIGHTS.goalDivisor.FWD;
  }

  // Glowna funkcja: player -> rozbicie punktow + suma.
  function scorePlayer(p) {
    var appPts = (p.appearances || 0) / WEIGHTS.appearancesPer;
    var goalPts = (p.goals || 0) / goalDivisor(p.position);

    var categories = [];
    var trophyPts = 0;
    for (var i = 0; i < CATEGORIES.length; i++) {
      var key = CATEGORIES[i].key;
      var pts;
      if (p.style === "legacy") {
        pts = (p.pts && p.pts[key]) || 0;   // juz w punktach
      } else {
        pts = pointsForCount(key, p.counts ? p.counts[key] : 0);
      }
      trophyPts += pts;
      categories.push({ key: key, label: CATEGORIES[i].label, points: pts });
    }

    var total = appPts + goalPts + trophyPts;
    return {
      appPts: appPts,
      goalPts: goalPts,
      trophyPts: trophyPts,
      categories: categories,
      total: total
    };
  }

  var api = {
    WEIGHTS: WEIGHTS,
    CATEGORIES: CATEGORIES,
    scorePlayer: scorePlayer,
    pointsForCount: pointsForCount,
    goalDivisor: goalDivisor
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    global.Scoring = api;
  }
})(typeof window !== "undefined" ? window : globalThis);
