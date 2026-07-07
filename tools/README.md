# tools/ - skrypty pomocnicze (śledzone w repo, nie publikowane)

Uruchamiać z katalogu głównego repo: `python tools/<skrypt>.py [arg]`.

- **integrate_batch.py `<plik.json>`** - wpina batch nowych/uaktualnionych piłkarzy do
  `public/data/players.json`. Wejście: tablica obiektów `{name, src, position, appearances, goals, counts, notes?}`.
  Dopasowanie po nazwie odporne na akcenty/wielkość liter, zachowuje istniejące `photo`.
  Na końcu drukuje przeliczoną czołówkę (replika wag z scoring.js).

- **download_photos.py** / **download_photos_retry.py** - pobierają zdjęcia z Wikimedia
  do `public/img/<slug>.jpg` (500px z fallbackiem) i przestawiają `photo` na ścieżkę lokalną.
  UWAGA: Wikimedia zwraca 400 dla nietypowych rozmiarów i rate-limituje przy szybkich żądaniach -
  retry robi to wolniej. Slug: nazwa -> ascii, lower, myślniki.

- **legacy_to_counts.py** - JEDNORAZOWO użyty: zdekodował graczy legacy (punkty) na `counts`
  (liczby zdobyć), żeby wszyscy byli w jednym modelu i zmiany wag działały jednakowo. Już wykonany.

- **merge_detail.py `players.json <detail.json>` [--dry-run]** - dopisuje pole `detail` (trofea i lata
  per klub) i - w wariancie audytu `{"Nazwa":{"counts":{...},"detail":{...}}}` - nadpisuje `counts`,
  raportując różnice i wpływ na punkty. **WALIDUJE spójność**: liczba lat/wpisów w detail musi = counts,
  inaczej odrzuca zapis. Format detail: klubowe `["Klub: 1999, 2005"]`; reprezentacyjne `["2022 (mistrz)"]`;
  przegrany finał LM `"Klub 2018 (finał)"`; nagrody `["2009 (1.)"]`. Uwaga: norm() mapuje ł->l.

- **merge_caps.py `players.json <caps.json>` [--dry-run]** - dopisuje `natApp`/`natGoals` (występy i gole
  w reprezentacji). Waliduje `natApp<=appearances` i `natGoals<=goals` (klub liczony na stronie jako różnica).

- **merge_active.py `players.json <active.json>` [--dry-run]** - dopisuje `active:true` dla wciąż grających
  (emeryci bez pola). Wypisuje listę aktywnych z ostatnim klubem.

Skrypty POBIERAJĄCE z Wikipedii (sekcje Honours, infoboksy: caps, status aktywności) były uruchamiane
doraźnie ze scratchpada (nie w repo). Wszystkie mają retry na HTTP 429 (Wikipedia rate-limituje przy
szybkich żądaniach - pobierać z przerwami / partiami).

Uwaga: schemat scoringu (wagi) jest w `public/scoring.js` - to jedyne źródło prawdy.
Przy zmianach wag zaktualizuj też repliki w skryptach powyżej oraz legendę w `public/index.html` i `README.md`.
