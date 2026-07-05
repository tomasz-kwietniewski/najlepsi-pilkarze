# Lista zadań - Najlepsi piłkarze

## Metodologia (ustalona z użytkownikiem) - WDROŻONE
- [x] Obrońca 1 pkt za 3 gole (było 2).
- [x] MŚ 1. miejsce 12 (było 10). Liga Mistrzów zwycięstwo 8 (było 7).
- [x] Copa America = połowa wag ME (4,5 / 3,5 / 2,5). Kategoria `copa`.
- [x] Liga Konferencji = połowa Pucharu UEFA (2,5 / 1,5). Kategoria `conference`.
- [x] Tylko ligi top-7 (Anglia, Hiszpania, Włochy, Niemcy, Francja, Portugalia, Holandia) -
      występy, gole i tytuły. Reszta (saudyjska, MLS, brazylijska, katarska, japońska, austriacka,
      szwajcarska, szkocka, turecka, bułgarska...) nie liczy się wcale. Puchar Konfederacji: nie liczymy.
- [x] Nowe konkurencje mapowane na najbliższy odpowiednik (Klubowe MŚ -> Interkontynentalny itd.).

## Dane - KOMPLETNE
- [x] 110 piłkarzy, wszyscy sklasyfikowani (0 w uzupełnianiu).
- [x] Wszyscy w jednolitym modelu `counts` (legacy zdekodowane).
- [x] Występy/gole doprecyzowane do samych top-lig (wszystkie rozgrywki + reprezentacja).

## Strona - WDROŻONE
- [x] Miniatury zdjęć z Wikipedii (108/110; Deco i Xavi bez - Wikipedia nie oddaje miniatury),
      awatar w wierszu/podium/szczegółach, kliknięcie = powiększenie (lightbox).
- [x] Rozbicie punktów pokazuje derywację ("3 mistrzostwa x 5 = 15").
- [x] Rozwijany opis metodologii i historii u dołu.
- [x] Sortowanie po pozycji (pełne nazwy), występach, golach, punktach.

## README - WDROŻONE
- [x] Pełny opis: po co, jak, historia (Tomasz + Emil), metodologia.

## Publikacja - DZIAŁA
- [x] GitHub Pages + subdomena najlepsipilkarze.tomaszkwietniewski.pl (HTTPS).

## W TOKU (główne zadanie na następną sesję)
- [ ] "Trofea i lata" w rozwinięciu piłkarza: przy każdej kategorii pokazać KLUBY i LATA
      (rok = zakończenie sezonu, np. 1999), grupowane per klub, tylko top-ligi.
      RENDER GOTOWY (index.html: detailHtml + CSS, czyta pole `player.detail`).
      BRAKUJE: zebrać `detail` dla 110 graczy z Wikipedii (Honours -> nasze kategorie) i dopisać do players.json.
      Format detail: { categoryKey: ["Klub: 1999, 2005", ...] }; wc/euro/copa: ["2022 (mistrz)"]; ballon/fifa: ["2009 (1.)"].

## Zrobione dodatkowo
- [x] Zdjęcia self-hostowane w public/img/ (110/110, w tym Deco i Xavi z plików usera).
- [x] Występy/gole = wszystkie rozgrywki, tylko top-ligi + reprezentacja.

## Opcjonalne
- [ ] Dokładniejsza weryfikacja występów/goli co do meczu (kosmetyka, ~1 pkt różnicy).
