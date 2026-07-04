/*
 * Lekkie testy scoring.js - bez frameworka, sam node:assert.
 * Uruchom: node test/scoring.test.js
 */
const assert = require("node:assert");
const S = require("../public/scoring.js");

let pass = 0;
function check(name, cond) {
  assert.ok(cond, "FAIL: " + name);
  pass++;
  console.log("  ok  " + name);
}
function near(a, b) { return Math.abs(a - b) < 0.01; }

// 1. Wystepy: 1 pkt za 35 meczow
const app = S.scorePlayer({ position: "MID", appearances: 350, goals: 0, style: "counts", counts: {} });
check("wystepy 350/35 = 10", near(app.appPts, 10));

// 2. Dzielnik goli wg pozycji
check("napastnik 17 goli = 1 pkt", near(S.scorePlayer({ position: "FWD", goals: 17, style: "counts", counts: {} }).goalPts, 1));
check("pomocnik 8 goli = 1 pkt",   near(S.scorePlayer({ position: "MID", goals: 8,  style: "counts", counts: {} }).goalPts, 1));
check("obronca 3 gole = 1 pkt (nowa regula)", near(S.scorePlayer({ position: "DEF", goals: 3, style: "counts", counts: {} }).goalPts, 1));
check("bramkarz 0 goli = 0 pkt",   near(S.scorePlayer({ position: "GK", goals: 0, style: "counts", counts: {} }).goalPts, 0));

// 3. Styl "counts" - kategorie z miejscami i plaskie
const c = S.scorePlayer({
  position: "FWD", appearances: 0, goals: 0, style: "counts",
  counts: {
    wc: { win: 1 },          // 10
    euro: { semi: 1 },       // 5
    league: 5,               // 25
    ucl: { win: 2, final: 1 }, // 14+5 = 19
    ballon: { first: 1, third: 2 }, // 5 + 2 = 7
    intercontinental: 3      // 6
  }
});
check("counts: MS win = 12", near(c.categories.find(x => x.key === "wc").points, 12));
check("counts: 5 mistrzostw = 25", near(c.categories.find(x => x.key === "league").points, 25));
check("counts: LM 2 wygrane + 1 final = 21", near(c.categories.find(x => x.key === "ucl").points, 21));
check("counts: Zlota Pilka 1x1 + 2x3 = 7", near(c.categories.find(x => x.key === "ballon").points, 7));
check("counts: suma trofeow = 76", near(c.trophyPts, 12 + 5 + 25 + 21 + 7 + 6));

// 4. Styl "legacy" - punkty sumowane wprost, gole liczone nowa regula
// Maldini: 1028 wyst, 40 goli (DEF), pts z arkusza (suma kategorii = 114)
const maldiniPts = { wc: 8, euro: 7, league: 35, natCup: 3, leagueCup: 0, natSupercup: 5,
                     ucl: 35, uefa: 0, euroSupercup: 10, intercontinental: 6, ballon: 2, fifa: 3 };
const m = S.scorePlayer({ position: "DEF", appearances: 1028, goals: 40, style: "legacy", pts: maldiniPts });
check("legacy Maldini wystepy 1028/35 = 29.37", near(m.appPts, 29.371));
check("legacy Maldini gole 40/3 = 13.33 (obronca)", near(m.goalPts, 13.333));
check("legacy Maldini suma trofeow = 114", near(m.trophyPts, 114));
check("legacy Maldini total = 156.70", near(m.total, 29.371 + 13.333 + 114));

console.log("\nPRZESZLO: " + pass + " asercji");
