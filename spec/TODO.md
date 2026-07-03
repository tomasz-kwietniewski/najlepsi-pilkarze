# Lista zadań - Najlepsi piłkarze

## Metodologia (ustalona z użytkownikiem - do wdrożenia w danych)
- [x] Obrońca 1 pkt za 3 gole (było 2).
- [x] Copa America = połowa wag ME (4,5 / 3,5 / 2,5). Osobna kategoria `copa` w scoring.js.
- [x] Liga Konferencji = połowa Pucharu UEFA (2,5 / 1,5). Kategoria `conference`.
- [ ] TYLKO ligi top: Anglia, Hiszpania, Włochy, Niemcy, Francja, Portugalia, Holandia.
      Wszystko inne (saudyjska, MLS, brazylijska, katarska, japońska, austriacka, szwajcarska,
      szkocka, bułgarska, chorwacka, rosyjska, liberyjska...) NIE liczy się wcale -
      ani tytuły, ani występy/gole. Puchar Konfederacji: nie liczymy (towarzyski).

## Dane - zbieranie i przetwarzanie (Wikipedia EN)
- [x] Migracja 71 z arkusza 2010 (styl legacy).
- [x] Batch 1 (12 gwiazd) zebrany i opublikowany - ALE wg starej metodologii.
      DO POPRAWY: Copa America pełną skalą (Messi) -> na pół; występy z lig słabych
      (Messi/MLS, CR7/Arabia, Xavi/Katar, Iniesta/Japonia, Ronaldinho+Kaká/Brazylia) -> odjąć.
- [ ] Wave 2 (35 graczy) zebrany (scratch: wave2/raw.json) - DO PRZETWORZENIA wg nowych zasad
      (odjąć tytuły i występy z lig spoza top-7; Copa America -> pole `copa`) i integracji.
- [ ] Powtórzyć batch, który padł na limicie: Lewandowski, Ibrahimović, Suárez, Cavani, Kane.
- [ ] Dobrać ostatnią falę ~32 klasycznych graczy ról: Fernando Torres, Gerrard, Eto'o,
      Rio Ferdinand, Rooney, Drogba, Terry, Del Piero, Nesta, Pirlo, Totti, Ballack, Kluivert,
      Larsson, Ashley Cole, Cannavaro, Batistuta, Mendieta, Morientes, Trezeguet, Vieira,
      Beckham, Casillas, Buffon, van der Sar, Nistelrooy, Anelka, Owen, Zanetti, Deco, Lampard, Dunga.
- [ ] Ujednolicić dopasowanie po nazwiskach ODPORNIE na akcenty/wielkość liter (uniknąć duplikatów jak Raúl).

## Strona (prośby użytkownika)
- [ ] Miniaturka zdjęcia piłkarza w rozwiniętych szczegółach (z Wikipedii).
- [ ] Pokazać SPOSÓB wyliczenia każdej punktacji, żeby dało się zweryfikować
      (skąd dana liczba pkt za dane osiągnięcie - np. "3 mistrzostwa x 5 = 15").
- [ ] Rozwijany przycisk u dołu strony głównej z pełnym opisem metodologii i historii projektu
      (powielić treść z README).

## README
- [ ] Zaktualizować README: po co powstał ranking, jak powstał (Tomasz + Emil, 2008-2010),
      pełny opis metodologii i systemu punktowego.

## Publikacja
- [x] GitHub Pages + subdomena najlepsipilkarze.tomaszkwietniewski.pl (działa, HTTPS).
