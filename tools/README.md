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

Uwaga: schemat scoringu (wagi) jest w `public/scoring.js` - to jedyne źródło prawdy.
Przy zmianach wag zaktualizuj też repliki w skryptach powyżej oraz legendę w `public/index.html` i `README.md`.
