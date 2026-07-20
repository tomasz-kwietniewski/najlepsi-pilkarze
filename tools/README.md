# tools/ - skrypty pomocnicze (śledzone w repo, nie publikowane)

Uruchamiać z katalogu głównego repo: `python tools/<skrypt>.py [arg]`.
Proces, w którym się ich używa, opisuje [`spec/PROCEDURA-AKTUALIZACJI.md`](../spec/PROCEDURA-AKTUALIZACJI.md);
reguły merytoryczne (co się liczy, a co nie) - [`REGULY_AUDYTU.md`](REGULY_AUDYTU.md).

## Punktacja

- **scoring_weights.py** - czyta wagi WPROST z `public/scoring.js` i udostępnia je Pythonowi
  (`WEIGHTS`, `cat_points`, `score_player`). **Nie kopiuj wag do skryptów** - wcześniejsze repliki
  rozjechały się z oryginałem (ME 9 vs 10, Copa 4,5 vs 5) i cicho zaniżały raporty.

## Pobieranie danych z Wikipedii

- **fetch_wiki.py `--out <kat>` `--active|--names "A|B"|--titles "A|B"`** - zapisuje sekcje Honours
  (`<kat>/honours/<slug>.txt`) i dane z infoboksu (`<kat>/infobox.json`: występy/gole w reprezentacji,
  kluby z latami, obecny klub). Retry na HTTP 429, przerwy między zapytaniami.

- **fetch_awards.py [`--apply`] [`--json out.json`] [`--from-year R`]** - podia (1./2./3.) Złotej Piłki,
  FIFA World Player of the Year i The Best FIFA. Raportuje różnice vs `players.json`, a z `--apply`
  nanosi je razem z `detail`. Wypisuje też **graczy spoza rankingu** z podium - to główne źródło
  nowych nazwisk. Tożsamością gracza jest tytuł artykułu (pole `source`), nie nazwisko:
  „Luis Suárez" z lat 60. to inny człowiek niż Urugwajczyk.

- **fetch_photos.py [`--size N`] [`--force`]** - dociąga brakujące zdjęcia do `public/img/<slug>.jpg`
  z API Wikipedii. Zdjęcia hostujemy lokalnie - hotlink do Wikimedia nie działa (rate limit + HTTP 400).

- **download_photos.py** / **download_photos_retry.py** - starsze warianty pobierania zdjęć
  z URL-a zapisanego w polu `photo` (używane przy pierwszym self-hoście).

## Nanoszenie zmian na players.json

- **merge_detail.py `players.json <detail.json>` [`--dry-run`]** - dopisuje `detail` (trofea i lata),
  a w wariancie audytu `{"Nazwa":{"counts":{...},"detail":{...}}}` nadpisuje też `counts`,
  raportując różnice i wpływ na punkty. **WALIDUJE**: liczba lat/wpisów w `detail` musi równać się
  `counts`, inaczej odrzuca zapis. Uwaga: **podmienia całe** `detail` gracza - buduj wpis na bazie
  obecnych danych, nie od zera.

- **merge_caps.py `players.json <caps.json>` [`--dry-run`] [`--bump`]** - ustawia `natApp`/`natGoals`.
  Przyjmuje wprost `infobox.json` z `fetch_wiki.py`. `--bump` dolicza przyrost kadry także do
  `appearances`/`goals` (doroczna aktualizacja po turnieju; zakłada zamknięty sezon klubowy).
  Waliduje `natApp<=appearances` i odrzuca podejrzany spadek liczby występów.

- **merge_active.py `players.json <active.json>` [`--dry-run`]** - ustawia `active:true` dla wciąż
  grających (emeryci nie mają tego pola). Kryterium - patrz krok 6 procedury.

- **add_players.py `players.json <nowi.json>` [`--dry-run`] [`--min-points N`]** - dodaje NOWYCH graczy
  w pełnym schemacie (`detail`, `natApp`, `natGoals`, `active`), waliduje `detail` tak samo jak
  `merge_detail.py` i odsiewa kandydatów poniżej progu punktowego.

- **integrate_batch.py `<plik.json>`** - starszy wariant wpinania batcha (bez `detail`/`natApp`);
  zostaje dla zgodności, do nowych graczy używaj `add_players.py`.

- **legacy_to_counts.py** - JEDNORAZOWO użyty przy migracji z modelu punktowego na `counts`.

Uwaga: schemat punktacji (wagi) jest w `public/scoring.js` - to jedyne źródło prawdy.
Przy zmianach wag zaktualizuj legendę w `public/index.html` i `README.md`
(skrypty Pythona czytają wagi same, przez `scoring_weights.py`).
