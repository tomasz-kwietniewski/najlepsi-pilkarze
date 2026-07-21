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
- **Mistrzostwa Świata**: 1. miejsce **12**, finał **8**, półfinał **6**.
- **Mistrzostwa Europy**: 1. miejsce **10**, finał **7**, półfinał **5**.
- **Copa America**: połowa wag ME - **5 / 3,5 / 2,5**.

Za "półfinał" liczymy dotarcie do najlepszej czwórki (3.-4. miejsce MŚ, top-4 ME/Copa), gdy piłkarz
był w kadrze turnieju. Copa America liczymy osobno od Mistrzostw Europy (częsty błąd u zawodników
z Ameryki Płd.). Nations League i Puchar Konfederacji nie liczą się.

### Trofea klubowe
- Mistrzostwo kraju: **5** (za każde). Puchar kraju: **3**. Puchar ligi: **1**. Superpuchar kraju: **1**.
- **Liga Mistrzów**: zwycięstwo **8**, przegrany finał **5**.
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
- **Calciopoli**: tytuły Serie A 2004/05 i 2005/06 odebrane Juventusowi nie liczą się -
  ani Juventusowi, ani Interowi (Scudetto 2005/06 przyznane administracyjnie, nie zdobyte na boisku).

## Skąd dane

Angielska Wikipedia - sekcje "Honours" (trofea) oraz infoboksy (występy i gole klubowe, występy
i gole w reprezentacji). Każdy dorobek trofeowy jest **zweryfikowany wg Wikipedii jako źródła prawdy** -
przy weryfikacji poprawiliśmy sporo błędów w obie strony (zawyżenia z lig spoza czołówki, ale też
pominięcia - np. przegrane finały Ligi Mistrzów czy półfinały reprezentacji). Piłkarze dodawani są
po akceptacji; nowych typujemy m.in. z podiów Złotej Piłki i The Best z ostatnich lat.

Ranking jest odświeżany po każdym dużym turnieju i po nagrodach indywidualnych - krok po kroku
opisuje to [`spec/PROCEDURA-AKTUALIZACJI.md`](spec/PROCEDURA-AKTUALIZACJI.md).
**Stan: 21 lipca 2026** (po MŚ 2026), 150 piłkarzy.

## Co widać na stronie

- **Podium** trzech najlepszych i pełny, sortowalny ranking (po pozycji, występach, golach, punktach).
- Filtr pozycji, szukajka, zdjęcia z powiększeniem (lightbox).
- Po kliknięciu wiersza - **rozwinięcie piłkarza**:
  - rozbicie punktów z derywacją (np. "3 mistrzostwa x 5"),
  - **występy i gole w podziale na klub i reprezentację**,
  - **"Trofea i lata"** - przy każdej kategorii kluby i lata zdobycia (rok = zakończenie sezonu),
    tylko z czołowych lig; przegrane finały oznaczone.
- **Zielona pulsująca kropka** przy piłkarzach wciąż aktywnych - ich pozycja może się jeszcze zmienić.
- **Widok mobilny** - na telefonie ranking mieści się bez poziomego przewijania: tabela pokazuje
  kluczowe kolumny (piłkarz, pozycja, punkty), a występy i gole widać po rozwinięciu wiersza; podium
  i filtry są dopasowane do wąskiego ekranu.

## Jak to zbudowane (technicznie)

Czysta strona statyczna, bez serwera i bazy. Trzy warstwy:
- `public/data/players.json` - dane każdego piłkarza. Pola: `name`, `position`, `appearances`, `goals`,
  `counts` (liczby trofeów wg kategorii), `detail` (trofea i lata per klub), `natApp`/`natGoals`
  (występy i gole w reprezentacji - klub liczony jako różnica), `active` (czy wciąż gra), `photo`, `source`.
- `public/scoring.js` - reguły punktacji (jedno źródło prawdy; zmiana wagi = jedna liczba).
- `public/index.html` - interaktywny raport.

Narzędzia pomocnicze w `tools/` (Python) - opis w [`tools/README.md`](tools/README.md):
pobieranie danych z Wikipedii (`fetch_wiki.py` - trofea i infoboksy, `fetch_awards.py` - podia Złotej
Piłki i nagród FIFA, `fetch_photos.py` - zdjęcia), nanoszenie zmian (`merge_detail.py` - trofea/lata
z **walidacją spójności** z punktacją, `merge_caps.py` - występy/gole reprezentacji, `merge_active.py` -
status aktywności, `add_players.py` - nowi piłkarze). Wagi punktacji skrypty czytają wprost
ze `scoring.js` (`scoring_weights.py`), więc nie da się ich rozjechać z jedynym źródłem prawdy.

Publikacja: push do `main` -> GitHub Actions publikuje na GitHub Pages pod subdomeną
(bez sekretów, autoryzacja tokenem OIDC). Folder `docs/` to lokalny katalog roboczy (poza repo).
