# Najlepsi piłkarze - odświeżenie rankingu i raport (specyfikacja)

Data: 2026-07-03
Autorzy pomysłu: Tomasz + Emil (projekt hobbystyczny z lat 2008-2010)

## Cel

Odświeżyć hobbystyczny ranking „Najlepsi piłkarze", zrobiony pierwotnie ręcznie
w Google Sheets i zamrożony w styczniu 2010. Zaktualizować kariery do dziś,
dodać współczesnych piłkarzy, przeliczyć wg (lekko poprawionego) autorskiego
systemu punktowego i zaprezentować jako interaktywny raport HTML opublikowany
w internecie - do pokazania m.in. Emilowi.

## Zakres

- Zakres czasowy: pełne kariery do dziś (2025). Ranking obejmuje piłkarzy od ~1990
  do teraz. Współcześni (Messi, Ronaldo, Lewandowski, Modrić itd.) dostają pełny,
  aktualny dorobek.
- Źródło danych: angielska Wikipedia (sekcje „Honours" + infobox występy/gole).
  Licencja CC BY-SA, dane budowane od zera - nie ufamy ręcznym cyfrom z 2010
  (zawierały błędy i niepełne dane).
- Publikacja: własny hosting użytkownika (np. podstrona/subdomena na kwietniewscy.pl).
  Sposób wgrania ustalany przy wdrożeniu.

## Architektura - trzy warstwy (rozdzielenie danych od punktacji)

Kluczowa zasada: surowe dane, reguły punktacji i prezentacja są rozdzielone,
żeby zmiana wag nie wymagała ponownego ściągania danych, a każdy wynik był audytowalny.

1. `data/players.json` - surowe dane wejściowe per piłkarz:
   - `name`, `position` (GK/DEF/MID/FWD - wyznacza dzielnik bramek),
   - `appearances` (łączne występy w liczonych rozgrywkach), `goals`,
   - `honours` - policzone trofea/nagrody w każdej kategorii systemu,
   - `source_url` (link do Wikipedii), `notes` (uwagi, wątpliwości, niepełne dane).
   Plik jest czytelny dla człowieka i stanowi jedyne źródło prawdy o danych wejściowych.

2. `scoring.js` - czysta funkcja: bierze jeden obiekt gracza i zwraca rozbicie
   punktów per kategoria oraz sumę. Cała logika wag w jednym miejscu. Zmiana wagi
   = zmiana jednej stałej, bez ruszania danych.

3. `index.html` - samodzielny plik raportu (bez serwera, bez zależności online),
   generujący ranking z powyższych. Cały CSS/JS/dane wbudowane w plik, żeby dało
   się go wrzucić na dowolny hosting jako pojedynczy plik.

Audytowalność: raport pokazuje per piłkarz rozwijane rozbicie „skąd te punkty",
więc suma jest odtwarzalna, a błąd w danych łatwo namierzyć i poprawić w jednym miejscu.

## Reguły punktacji

Zachowane 1:1 z oryginału, z jedną zatwierdzoną korektą (obrońcy).

- Występy: 1 pkt za 35 meczów.
- Bramki wg pozycji:
  - napastnik: 1 pkt za 17 goli,
  - pomocnik: 1 pkt za 8 goli,
  - obrońca: 1 pkt za 3 gole (ZMIENIONE z 1/2 - w oryginale windowało obrońców za wysoko),
  - bramkarz: dzielnik nieistotny (gole sporadyczne).
- MŚ: 1. miejsce 10, 2. miejsce 8, półfinał 6.
- ME (lub Copa America): 1. miejsce 9, 2. miejsce 7, półfinał 5.
- Mistrzostwo kraju: 5 pkt każde.
- Puchar kraju: 3. Puchar ligi: 1. Superpuchar kraju: 1.
- Liga Mistrzów: 1. miejsce 7, 2. miejsce 5.
- UEFA/Puchar Zdobywców Pucharów: 1. miejsce 5, 2. miejsce 3.
- Superpuchar Europy: 2. Puchar Interkontynentalny: 2.
- Złota Piłka France Football: 5 / 3 / 1 (za 1./2./3. miejsce).
- Piłkarz Roku FIFA: 5 / 3 / 1.

### Mapowanie nowych konkurencji (po 2010) na najbliższy odpowiednik

- Klubowe Mistrzostwa Świata FIFA -> Puchar Interkontynentalny (2 pkt).
- FIFA Ballon d'Or (2010-2015, połączona nagroda) oraz The Best FIFA (od 2016)
  -> liczone jako Piłkarz Roku FIFA / Złota Piłka odpowiednio; unikamy podwójnego
  liczenia tego samego roku 2010-2015 (jedna nagroda = jedna kategoria).
- Liga Konferencji UEFA -> pod UEFA/PZP.
- Liga Narodów UEFA -> pomijana (brak sensownego odpowiednika w systemie).

## Skład - workflow akceptacji

1. Przygotowanie listy kandydatów: 72 piłkarzy z oryginału (zaktualizowani) +
   propozycje nowych z pełnym uzasadnieniem i orientacyjnym progiem wejścia.
2. Użytkownik akceptuje/skreśla/dopisuje.
3. Dopiero po akceptacji: ściąganie danych z Wikipedii dla zatwierdzonego składu
   (partiami, z weryfikacją) i przeliczenie punktów.

Pozycja każdego gracza (a więc dzielnik bramek) jest w `players.json` i można ją
nadpisać ręcznie, gdyby klasyfikacja z Wikipedii była sporna.

## Raport HTML

Jeden samodzielny `index.html`, działający offline:
- podium (top 3) na górze,
- pełna tabela rankingowa: kolumny nazwa / pozycja / era / suma + kluczowe składowe,
- sortowanie po kliknięciu w nagłówek kolumny,
- filtr po pozycji i po erze,
- rozwijane rozbicie punktów per piłkarz (ile z występów, goli, każdego trofeum),
- link do źródła (Wikipedia) per piłkarz.

## Kolejność prac

1. Szkielet projektu + `scoring.js` + migracja 72 istniejących z nową regułą obrońców
   (od razu widać odświeżony ranking na dotychczasowych danych).
2. Lista kandydatów do akceptacji przez użytkownika.
3. Ściąganie z Wikipedii dla zatwierdzonego składu (partiami, weryfikacja poprawności).
4. Finalny raport HTML.
5. Publikacja na hostingu użytkownika (sposób wgrania ustalany na tym etapie).

## Testy i weryfikacja

- `scoring.js`: lekkie testy jednostkowe reguł (kilka graczy o znanym, ręcznie
  policzonym wyniku - w tym co najmniej jeden obrońca, jeden napastnik, jeden bramkarz).
- Migracja: suma punktów starych graczy po zmianie reguły obrońców zgodna z ręcznym
  przeliczeniem (weryfikacja na Maldinim, Hierro, Roberto Carlosie).
- Raport: uruchomienie w realnej przeglądarce i sprawdzenie asercjami, że sortowanie,
  filtry i rozwijane rozbicia działają, oraz że brak błędów w konsoli.
- Uczciwość danych: gdzie Wikipedia jest niepełna/sporna, oznaczamy to w `notes`
  i widocznie w raporcie, zamiast zgadywać.

## Poza zakresem (YAGNI)

- Backend/serwer, baza danych, logowanie.
- Automatyczny scraping Transfermarktu.
- Osobne „karty piłkarzy" jako oddzielne podstrony (rozbicie jest w rozwijanym wierszu).
- Liga Narodów i inne konkurencje bez odpowiednika w systemie.
