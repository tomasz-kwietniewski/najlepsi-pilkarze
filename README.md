# Najlepsi piłkarze

Ranking piłkarzy wszech czasów wg autorskiego systemu punktowego. Strona:
**https://najlepsipilkarze.tomaszkwietniewski.pl**

## Po co ten ranking

To projekt hobbystyczny, który zaczęliśmy z przyjacielem **Emilem** jeszcze na studiach,
w latach 2008-2010. Chcieliśmy przeliczyć osiągnięcia piłkarzy, których dobrze wspominamy
z lat 90. i 2000., na jeden system punktowy - żeby dało się ich uczciwie porównać i docenić
najlepszych. Wtedy robiliśmy to ręcznie w arkuszu, na danych z angielskiej Wikipedii.
Ta wersja to odświeżenie tamtego pomysłu: pełne kariery do dziś, współcześni piłkarze
i porządny, interaktywny raport.

## Jak liczymy punkty

Punkty sumują się z trzech źródeł: **występów**, **goli** (ważonych pozycją) oraz **trofeów
i nagród indywidualnych**.

### Występy i gole
- Występy: **1 pkt za 35 meczów**.
- Gole zależnie od pozycji (gol napastnika jest "tańszy" niż obrońcy):
  - napastnik: 1 pkt za **17** goli,
  - pomocnik: 1 pkt za **8** goli,
  - obrońca: 1 pkt za **3** gole,
  - bramkarz: liczony jak napastnik (gole sporadyczne).

### Trofea reprezentacyjne
- **Mistrzostwa Świata**: 1. miejsce **10**, finał **8**, półfinał **6**.
- **Mistrzostwa Europy**: 1. miejsce **9**, finał **7**, półfinał **5**.
- **Copa America**: połowa wag ME - **4,5 / 3,5 / 2,5**.

### Trofea klubowe
- Mistrzostwo kraju: **5** (za każde). Puchar kraju: **3**. Puchar ligi: **1**. Superpuchar kraju: **1**.
- **Liga Mistrzów**: zwycięstwo **7**, przegrany finał **5**.
- **Puchar UEFA / Liga Europy / Puchar Zdobywców Pucharów**: **5 / 3**.
- **Liga Konferencji**: połowa tego - **2,5 / 1,5**.
- Superpuchar Europy: **2**. Puchar Interkontynentalny / Klubowe MŚ: **2**.

### Nagrody indywidualne
- **Złota Piłka** (France Football): za 1./2./3. miejsce **5 / 3 / 1**.
- **Piłkarz Roku FIFA / The Best**: **5 / 3 / 1**.
  (Połączoną nagrodę FIFA Ballon d'Or z lat 2010-2015 liczymy jako Złotą Piłkę, żeby nie dublować.)

### Zasady szczegółowe
- **Liczą się tylko czołowe ligi europejskie**: Anglia, Hiszpania, Włochy, Niemcy, Francja,
  Portugalia, Holandia. Występy, gole i tytuły ze słabszych rozgrywek (saudyjska, MLS,
  brazylijska, katarska, japońska, austriacka, szwajcarska, szkocka itd.) **nie liczą się wcale**.
- Puchar Konfederacji i inne turnieje towarzyskie: nie liczymy.
- Nowe rozgrywki mapujemy na najbliższy odpowiednik (Klubowe MŚ -> Puchar Interkontynentalny,
  The Best -> Piłkarz Roku FIFA, Liga Konferencji -> pod Puchar UEFA z połową wagi).

## Skąd dane

Angielska Wikipedia - sekcje "Honours" (trofea) i infoboksy (występy, gole). Piłkarze dodawani
są po akceptacji; nowych typujemy m.in. z podiów Złotej Piłki i The Best z ostatnich lat.

## Jak to zbudowane (technicznie)

Czysta strona statyczna, bez serwera i bazy. Trzy warstwy:
- `public/data/players.json` - surowe dane wejściowe każdego piłkarza,
- `public/scoring.js` - reguły punktacji (jedno źródło prawdy; zmiana wagi = jedna liczba),
- `public/index.html` - interaktywny raport (ranking, sortowanie, filtry, rozbicie punktów).

Publikacja: push do `main` -> GitHub Actions publikuje na GitHub Pages pod subdomeną
(bez sekretów, autoryzacja tokenem OIDC). Folder `docs/` to lokalny katalog roboczy (poza repo).
