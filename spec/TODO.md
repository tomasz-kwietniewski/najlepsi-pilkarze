# Lista zadań - Najlepsi piłkarze

## Metodologia (ustalona z użytkownikiem) - WDROŻONE
- [x] Obrońca 1 pkt za 3 gole (było 2).
- [x] MŚ 1. miejsce 12 (było 10). Liga Mistrzów zwycięstwo 8 (było 7).
- [x] ME 1. miejsce 10 (było 9): wagi 10 / 7 / 5.
- [x] Copa America = połowa wag ME (5 / 3,5 / 2,5). Kategoria `copa`.
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
- [x] Sortowanie ulepszone: pozycja w kolejności boiskowej (GK->OBR->POM->NAP, nie alfabetycznie);
      wskaźniki na WSZYSTKICH kolumnach (przyciemniony ▾ = sortowalna, aktywna ▼/▲ na zielono).

## README - WDROŻONE
- [x] Pełny opis: po co, jak, historia (Tomasz + Emil), metodologia.

## Publikacja - DZIAŁA
- [x] GitHub Pages + subdomena najlepsipilkarze.tomaszkwietniewski.pl (HTTPS).

## Trofea, audyt i rozbicie - WDROŻONE (kompletne 110/110)
- [x] "Trofea i lata" w rozwinięciu piłkarza: przy każdej kategorii KLUBY i LATA (rok = zakończenie sezonu),
      grupowane per klub, tylko top-ligi; przegrane finały LM z tagiem "(finał)". Zebrane dla WSZYSTKICH 110.
- [x] AUDYT counts wg Wikipedii (źródło prawdy) - poprawione liczby trofeów wszystkich 110. Top-28 ręcznie,
      reszta subagentami (10 partii wg scratchpad/REGULY_AUDYTU.md), każda walidowana tools/merge_detail.py.
- [x] Rozbicie występów i goli na KLUB vs REPREZENTACJA (pola natApp/natGoals; klub = różnica). 110/110.
- [x] Znacznik AKTYWNYCH (pole active) - zielona pulsująca kropka + notka; 28 wciąż grających.
- [x] Calciopoli: odjęto Interowi Scudetto 2005/06 (Figo, Zanetti, Verón) - spójnie z odjęciem Juventusowi.
- [x] Cachebust przy fetch players.json (świeże dane po deploy).

## Zrobione dodatkowo
- [x] Zdjęcia self-hostowane w public/img/ (110/110, w tym Deco i Xavi z plików usera).
- [x] Występy/gole = wszystkie rozgrywki, tylko top-ligi + reprezentacja.

## Aktualizacja po MŚ 2026 (20.07.2026) - WDROŻONE
- [x] **Procedura aktualizacji** spisana: `spec/PROCEDURA-AKTUALIZACJI.md` (kalendarz + kroki + bramki
      jakości) oraz `tools/REGULY_AUDYTU.md` (reguły mapowania trofeów, prompt dla agentów).
- [x] MŚ 2026 (Hiszpania - Argentyna 1:0 po dogrywce, 3. Anglia, 4. Francja): mistrzostwo, finał
      i półfinały naniesione; występy/gole w kadrze zaktualizowane po turnieju.
- [x] "Przetrzepanie" 28 aktywnych: audyt trofeów wg świeżych sekcji Honours + weryfikacja udziału
      w kadrach turniejów. Wyłapane stare luki, m.in. półfinały MŚ/ME (Neuer 2010, Kane 2018,
      van Dijk ME 2024, Suárez i Cavani MŚ 2010, Neymar MŚ 2014) i superpuchary (Neymar, CR7).
- [x] **Podia nagród** (2. i 3. miejsce Złotej Piłki i nagrody FIFA) - dotąd niekompletne, teraz
      pobierane automatycznie z Wikipedii przez `tools/fetch_awards.py --apply` (27 poprawek).
- [x] 15 nowych piłkarzy powyżej progu 100 pkt (m.in. Müller, Alaba, Matthäus, Marquinhos, Robben,
      van Basten, Gullit) wraz ze zdjęciami. Razem 125 piłkarzy, 35 aktywnych.
- [x] Wagi punktacji czytane przez skrypty wprost ze `scoring.js` (`tools/scoring_weights.py`) -
      koniec z rozjeżdżającymi się replikami. Ścieżki w tools/ liczone od repo (działa w git worktree).

## Rozszerzenie rankingu (21.07.2026) - WDROŻONE
- [x] Lautaro Martínez dodany (98,3 pkt) na wyraźną prośbę usera, mimo progu 100.
- [x] Przejrzano ~40 dalszych kandydatów (bramkarze, obrońcy, pomocnicy, napastnicy). Weszło 21
      powyżej progu 100 pkt: Scholes 144, Chiellini, Thiago, Bonucci, Khedira, Evra, Vidal, David Silva,
      Agüero, Varane, Fàbregas, Mascherano, Jordi Alba, Verratti, Valdés, Higuaín, Isco, Walker, Matuidi,
      Rakitić, Courtois. Poniżej progu (nie dodani): Ederson 98, Stanković, Čech, Alexis, Makélélé, Özil,
      Sneijder, Pogba, Cambiasso, Džeko, Sterling, Rüdiger, Alisson.
- [x] **Granica epok**: dodano Maradonę i Platiniego (decyzja usera). Platini 137,8 (top-32).
      Maradona 64,9 (ok. 135. miejsca) - system premiuje kolekcję tytułów w top-ligach i Ligę Mistrzów,
      a nie profil "geniusz + MŚ + Napoli", więc wypada nisko. Reszta legend sprzed 1990 (Cruyff,
      Beckenbauer, Gerd Müller, Di Stéfano...) świadomie POZA rankingiem - to wybór, nie przeoczenie.
- [x] Razem 149 piłkarzy, 41 aktywnych.

## Audyt półfinałów reprezentacji u nieaktywnych (21.07.2026) - WDROŻONE
- [x] Półfinały MŚ/ME (3./4. miejsce = semi) rzadko są w sekcji Honours, więc stare counts miały luki.
      Weryfikacja turniej-po-turnieju (4 subagenci, potwierdzenie obecności w kadrach) poprawiła 21 graczy:
      ME 1996 Francja (Thuram, Deschamps, Desailly, Lizarazu, Blanc), Holandia (de Boer +3 ME, Stam,
      Kluivert, van Nistelrooy, Bergkamp), Niemcy (Kroos -> top 10, Schweinsteiger), Nedved, Bale,
      Shearer, Deco, Godín. Przy okazji brakujące FINAŁY: Vieira (MŚ 2006), Inzaghi (ME 2000),
      Dunga (MŚ 1998 + Copa 1995), Zanetti (Copa 2004/2007).
- [x] Weryfikacja ochroniła przed błędami: odrzucono Zanetti Copa 1995 (Argentyna odpadła w ćwierćfinale,
      4. miejsce = USA), Cafu Copa 1995 (nie w kadrze), Verón Copa 2004 (poza kadrą w erze Bielsy).
      LEKCJA: przesłanka o "Copa 1995 Argentyna 4. miejsce" była moim błędem - subagent go wychwycił.

## Opcjonalne / na przyszłość
- [ ] Dokładniejsza weryfikacja występów/goli co do meczu (kosmetyka, ~1 pkt różnicy).
- [ ] Jeśli user zechce jeszcze szerzej: kolejni kandydaci ~90-100 pkt (Ederson, Stanković, Čech,
      Alexis Sánchez) i ewentualnie pełne otwarcie na legendy lat 50.-80.
- [ ] Ewentualnie audyt brakujących copa WIN/FINAL u Brazylijczyków/Argentyńczyków (np. czy ktoś
      nie pomija Copa América, w której był w kadrze mistrza) - przy okazji semi wyszło kilka finałów.
