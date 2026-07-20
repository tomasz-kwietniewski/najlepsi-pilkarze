# Procedura aktualizacji rankingu

Ranking żyje: co roku dochodzą trofea, występy, nagrody i nazwiska. Ten plik opisuje, **co i kiedy
zrobić, żeby dane były aktualne** - tak, żeby dało się to wywołać jednym poleceniem do Claude Code:

> „Zrób aktualizację rankingu wg `spec/PROCEDURA-AKTUALIZACJI.md`."

Zasada nadrzędna: **angielska Wikipedia = źródło prawdy**. Reguły mapowania trofeów na kategorie
punktowe są w [`tools/REGULY_AUDYTU.md`](../tools/REGULY_AUDYTU.md) - ten plik opisuje **proces**,
tamten **treść**.

---

## Kalendarz - kiedy co robić

| Kiedy | Co się wydarzyło | Które kroki |
|---|---|---|
| **czerwiec** (po sezonie klubowym) | mistrzostwa, puchary, finał Ligi Mistrzów | 1, 2, 5, 6, 7 |
| **lipiec** (co 2 lata: MŚ / ME / Copa América) | wielki turniej reprezentacji | 1-7 (pełna procedura) |
| **październik / listopad** | Złota Piłka | 1, 3, 4, 6, 7 |
| **styczeń / luty** | The Best FIFA | 1, 3, 6, 7 |

Minimalna wersja („nic wielkiego się nie działo"): kroki 1, 3, 6, 7 - zajmuje kilkanaście minut.

---

## Krok 1. Przygotowanie

```bash
git checkout main && git pull
git checkout -b claude/update-ranking-<rok>
cp public/data/players.json /tmp/players.backup.json     # punkt odwrotu
```

Ustal, co się zmieniło od ostatniej aktualizacji: data ostatniego commita danych + jakie turnieje
i nagrody były w międzyczasie.

---

## Krok 2. Wielki turniej reprezentacji (MŚ / ME / Copa América)

Wikipedia **nie odnotowuje** 4. miejsca ani półfinału w sekcji Honours zawodnika, a runner-up
i 3. miejsce pojawiają się z opóźnieniem. Dlatego turniej ustala się **od strony turnieju**, nie gracza:

1. Artykuł turnieju -> mistrz, finalista, 3. i 4. miejsce.
   Punktowo: mistrz -> `win`, przegrany finał -> `final`, **3. ORAZ 4. miejsce -> `semi`**.
2. Artykuł `<rok> FIFA World Cup squads` (albo `UEFA Euro <rok> squads`) -> pełne składy tych
   czterech drużyn. Liczy się **obecność w kadrze**, nie rozegrane minuty.
3. Przecięcie składów z `players.json` -> lista graczy do zmiany.

Pomocniczy skrypt do wyciągnięcia składów jest w `tools/fetch_wiki.py` (patrz krok 3);
same składy najprościej pobrać przez API sekcjami artykułu `... squads`.

> Pułapka: zbiorcze strony `*_squads` bywają ucinane przy pobieraniu przez WebFetch - przy
> wątpliwości weryfikuj protokołem konkretnego meczu (finał / mecz o 3. miejsce) albo artykułem gracza.

---

## Krok 3. Pobranie świeżych danych z Wikipedii

```bash
# sekcje Honours + infobox (kadra, kluby, lata) dla wszystkich wciąż grających
python tools/fetch_wiki.py --out tmp/wiki --active

# podia Złotej Piłki i nagród FIFA - raport różnic vs players.json
python tools/fetch_awards.py
```

`fetch_wiki.py` zapisuje `tmp/wiki/honours/<slug>.txt` (wikitext sekcji Honours)
oraz `tmp/wiki/infobox.json` (występy/gole w reprezentacji, kluby z latami, obecny klub).

---

## Krok 4. Audyt trofeów („przetrzepanie" aktywnych)

Dla graczy z `active: true` porównaj `counts`/`detail` ze świeżym Honours. Przy większej liczbie
graczy rozdziel to na **subagentów po 5-6 nazwisk**, każdemu dając:

- `tools/REGULY_AUDYTU.md` (reguły mapowania),
- plik `tmp/wiki/honours/<slug>.txt`,
- obecne dane gracza z `players.json`,
- polecenie: **zgłaszaj wyłącznie rozbieżności z dowodem i poziomem pewności**, nie przepisuj całości.

Agenci pracują wtedy offline (bez sieci) i są tani. Ich ustalenia **weryfikujesz sam** - historycznie
~6 błędów na 82 graczy, wszystkie wyłapane bramką z kroku 5.

Nagrody indywidualne robi automat:

```bash
python tools/fetch_awards.py --apply    # nadpisuje counts.ballon/fifa + detail.ballon/fifa
```

---

## Krok 5. Naniesienie zmian (z bramką spójności)

Wszystkie zmiany `counts` idą przez `tools/merge_detail.py`, który **odrzuca zapis**, gdy liczba lat
w `detail` nie zgadza się z `counts`:

```bash
python tools/merge_detail.py public/data/players.json tmp/delta.json --dry-run   # raport + walidacja
python tools/merge_detail.py public/data/players.json tmp/delta.json             # zapis
```

Format `tmp/delta.json`: `{"Nazwa": {"counts": {...PEŁNE...}, "detail": {...PEŁNE...}}}`.

> **Uwaga:** `merge_detail.py` **podmienia całe** `detail` gracza, a nie dokleja kategorie.
> Zawsze buduj wpis na bazie obecnych danych (wczytaj gracza, zmodyfikuj, zapisz), inaczej
> skasujesz pozostałe kategorie.

Występy i gole w reprezentacji (po turnieju rosną):

```bash
python tools/merge_caps.py public/data/players.json tmp/wiki/infobox.json --bump --dry-run
python tools/merge_caps.py public/data/players.json tmp/wiki/infobox.json --bump
```

`--bump` dolicza przyrost kadry także do `appearances`/`goals` (suma = klub + reprezentacja).
Zakłada, że występy klubowe się nie zmieniły - czyli **uruchamiaj po zamknięciu sezonu klubowego**.
Występy klubowe (wszystkie rozgrywki, tylko ligi top-7) aktualizuje się ręcznie z sekcji
„Career statistics" - warto raz w roku, po sezonie.

---

## Krok 6. Status „wciąż gra" (`active: true`)

Zielona pulsująca kropka przy nazwisku. Reguła:

- gracz jest **aktywny**, dopóki Wikipedia pisze *„is a professional footballer who plays for..."* -
  **brak klubu nie oznacza końca kariery** (wolny zawodnik nadal jest aktywny; tak są dziś opisani
  m.in. Ramos, Modrić, Salah, Casemiro);
- gracz jest **emerytem**, gdy artykuł mówi o zakończeniu **kariery klubowej/piłkarskiej** -
  uwaga, sekcja „Retirement" często dotyczy tylko **rezygnacji z gry w reprezentacji** (Cavani 2024,
  Ramos 2023), co statusu **nie** zmienia;
- emeryci **nie mają** pola `active` (nie `false` - pola po prostu nie ma).

```bash
python tools/merge_active.py public/data/players.json tmp/active.json --dry-run
```

---

## Krok 7. Nowe nazwiska

Ranking nie jest zamknięty. Raz w roku sprawdź, kto powinien do niego dołączyć.

**Skąd brać kandydatów:**

1. `python tools/fetch_awards.py` - sekcja „PODIA GRACZY SPOZA RANKINGU" wypisuje wszystkich
   z podium Złotej Piłki / nagrody FIFA, których nie ma w `players.json`, posortowanych po punktach.
2. Kadry finalistów ostatniego wielkiego turnieju (krok 2) - nazwiska spoza rankingu.
3. Zwycięzcy Ligi Mistrzów i mistrzowie top-lig z ostatnich sezonów - gracze z długą kolekcją trofeów
   potrafią uzbierać dużo punktów bez ani jednej nagrody indywidualnej (klasyczny przykład:
   Thomas Müller, dodany w 2026 r. z wynikiem plasującym go w czołowej dziesiątce).

**Próg wejścia:** kandydat wchodzi, jeśli po policzeniu punktów mieści się w **pierwszej pięćdziesiątce**
(w 2026 r. było to ok. 100 pkt). Ranking ma być listą wielkich karier, nie katalogiem wszystkich piłkarzy.

**Co trzeba przygotować dla nowego gracza:** `name`, `position`, `appearances`, `goals`, `natApp`,
`natGoals`, `counts`, `detail`, `source`, `style:"counts"`, `dataComplete:true`, `active` (jeśli gra)
oraz **zdjęcie** (`tools/download_photos.py` - zdjęcia hostujemy lokalnie w `public/img/`,
hotlink do Wikimedii NIE działa).

```bash
python tools/integrate_batch.py tmp/nowi.json          # wpięcie do players.json
python tools/download_photos.py                        # zdjęcia dla brakujących
```

---

## Krok 8. Weryfikacja i publikacja

```bash
node test/scoring.test.js                              # testy punktacji
python -c "import json;d=json.load(open('public/data/players.json',encoding='utf-8'));print(len(d['players']))"
```

Potem **obejrzyj stronę w przeglądarce** (nie tylko testy): podium, sortowanie tabeli, rozwinięcie
kilku zmienionych graczy (rozbicie punktów + „Trofea i lata"), widok mobilny 375 px.

```bash
git add -A && git commit -m "Aktualizacja <rok>: <co>"
git checkout main && git merge --no-ff claude/update-ranking-<rok> && git push
```

Push do `main` publikuje stronę przez GitHub Actions (tylko katalog `public/`).
Jeśli krok „Deploy na Pages" zwróci przejściowo *„Deployment failed, try again later"* -
`gh workflow run deploy-pages.yml` i po sprawie.

Na koniec zaktualizuj `README.md` (liczba graczy, czołówka, data aktualizacji).

---

## Bramki jakości (nie da się ich obejść)

1. `merge_detail.py` odrzuca zapis, gdy `detail` nie zgadza się z `counts`.
2. `merge_caps.py` odrzuca `natApp > appearances` i spadek liczby występów w kadrze.
3. `test/scoring.test.js` pilnuje samej punktacji.
4. Wagi są **wyłącznie** w `public/scoring.js`; skrypty Pythona czytają je przez
   `tools/scoring_weights.py`. Nie kopiuj wag do skryptów - w 2026 r. taka kopia rozjechała się
   z oryginałem (ME 9 vs 10, Copa 4,5 vs 5) i cicho zaniżała raporty.

## Pułapki (sprawdzone boleśnie)

- **Messi nie ma sekcji Honours** w swoim artykule (osobny artykuł z osiągnięciami) - jego zmiany rób ręcznie.
- Wikipedia **rate-limituje** (HTTP 429) po kilku szybkich zapytaniach - skrypty mają retry i przerwy,
  ale nie odpalaj równolegle wielu agentów sięgających do Wikipedii.
- Podia nagród (2./3. miejsce) **nie występują** w sekcjach Honours - dlatego jest `fetch_awards.py`.
- Nazwy: dopasowanie graczy musi być odporne na akcenty i wielkość liter; „Luis Suárez" z lat 60.
  to **inny człowiek** niż Urugwajczyk - tożsamością jest tytuł artykułu (pole `source`), nie nazwisko.
- Trofea z lig spoza top-7 (Arabia, MLS, Meksyk, Brazylia, Turcja, Austria) **nie liczą się wcale** -
  agenci regularnie próbują je doliczyć.
