# Reguły audytu trofeów (prompt dla agentów weryfikujących)

Ten plik jest źródłem prawdy przy mapowaniu sekcji **Honours** z angielskiej Wikipedii na `counts`
i `detail` w `public/data/players.json`. Używany zarówno przy dorocznej aktualizacji
(patrz `spec/PROCEDURA-AKTUALIZACJI.md`), jak i przy dodawaniu nowych piłkarzy.

## Zasada nadrzędna

**Wikipedia (sekcja Honours) = źródło prawdy.** Gdy dane w `players.json` rozjeżdżają się z Wikipedią,
poprawiamy `players.json`. Sekcja **Manager/Coach** nie liczy się - tylko kariera **zawodnicza**.

## Które rozgrywki się liczą

Do występów, goli i tytułów liczą się **tylko ligi top-7**:
Anglia, Hiszpania, Włochy, Niemcy, Francja, Portugalia, Holandia - oraz reprezentacja.

Nie liczy się **nic** z pozostałych lig (Arabia Saudyjska, MLS, Brazylia, Argentyna, Katar, Japonia,
Turcja, Szkocja, Austria, Szwajcaria, Chorwacja, Bułgaria, Polska, Norwegia, Meksyk...).
Trofeum zdobyte w takim klubie po prostu pomijamy.

Brak slotu w punktacji (pomijamy całkowicie): Puchar Konfederacji, Liga Narodów UEFA,
Puchar Narodów Afryki, Copa Libertadores/Sudamericana, igrzyska olimpijskie, tytuły stanowe,
mistrzostwa młodzieżowe (U17/U19/U21), trofea towarzyskie.

**Calciopoli**: nie liczymy Juventusowi Serie A 2004-05 i 2005-06 ani Interowi Serie A 2005-06
(tytuł przyznany po odebraniu Juve). Legalne tytuły Interu od 2006-07 zostają.

## Mapowanie Honours -> kategorie `counts`

| Wikipedia | klucz | struktura |
|---|---|---|
| FIFA World Cup (mistrz / runner-up / 3. lub 4. miejsce) | `wc` | `{win, final, semi}` |
| UEFA European Championship | `euro` | `{win, final, semi}` |
| Copa América | `copa` | `{win, final, semi}` |
| mistrzostwo ligi top-7 | `league` | liczba |
| puchar krajowy (FA Cup, Copa del Rey, Coppa Italia, DFB-Pokal, Coupe de France, Taça, KNVB) | `natCup` | liczba |
| puchar ligi (EFL Cup, Coupe de la Ligue, Taça da Liga) | `leagueCup` | liczba |
| superpuchar krajowy (Community Shield, Supercopa, Supercoppa, DFL-Supercup, Trophée des Champions, Johan Cruijff Schaal) | `natSupercup` | liczba |
| Liga Mistrzów / Puchar Europy | `ucl` | `{win, final}` |
| Puchar UEFA / Liga Europy / Puchar Zdobywców Pucharów | `uefa` | `{win, final}` |
| Liga Konferencji Europy | `conference` | `{win, final}` |
| Superpuchar Europy | `euroSupercup` | liczba |
| Puchar Interkontynentalny **+** Klubowe MŚ FIFA (łącznie) | `intercontinental` | liczba |
| Ballon d'Or (France Football) | `ballon` | `{first, second, third}` |
| FIFA World Player of the Year / The Best FIFA | `fifa` | `{first, second, third}` |

`semi` (półfinał) = drużyna **dotarła do półfinału i go przegrała**, czyli zajęła 3. lub 4. miejsce.
`final` = przegrany finał. Wikipedia nierzadko nie listuje 4. miejsca ani półfinału jako "honour" -
trzeba to brać z artykułu o turnieju + składu drużyny.

## Najczęstsze błędy (wyłapane w poprzednich audytach)

1. **Przegrane finały LM** są masowo pomijane w starych danych (Maldini miał 3 = 15 pkt).
2. **Półfinały MŚ/ME** reprezentacji - liczą się, a rzadko widnieją w Honours.
3. **Copa América** Brazylijczyków/Argentyńczyków bywa wpisana do `euro` zamiast `copa`.
4. **Superpuchary krajowe** (Trophée des Champions, DFL-Supercup) pomijane.
5. **Złota Piłka sprzed 2010** to nadal `ballon` (nie tylko lata 2010-15).
6. **Nagroda połączona 2010-2015** (FIFA Ballon d'Or) liczy się jako `ballon`, **nie dublować** w `fifa`.
7. **Podia nagród** (2. i 3. miejsce w Ballon d'Or / The Best) prawie nigdy nie są w Honours -
   brać z artykułów o edycjach nagrody, weryfikować gdy wątpliwe.
8. **Słabe ligi** wliczane przez pomyłkę (Galatasaray, Al-Nassr, Inter Miami, Dinamo Zagrzeb).
9. Artykuł bywa pod pełną nazwą (`Rodri (footballer, born 1996)`) - tytuł brać z pola `source`.
10. **Lionel Messi nie ma sekcji Honours** w swoim artykule (osobny artykuł
    "List of career achievements by Lionel Messi") - jego audyt robić ręcznie.

## Format `detail` (trofea i lata)

Rok = **rok zakończenia sezonu** (2005-06 -> `2006`).

```
"league":        ["Barcelona: 2005, 2006, 2009", "PSG: 2022, 2023"]
"ucl":           ["Barcelona: 2006, 2009", "Barcelona 2011 (finał)"]      # przegrany finał z tagiem
"wc"/"euro"/"copa": ["2022 (mistrz)", "2014 (finał)", "2019 (półfinał)"]
"ballon"/"fifa": ["2009 (1.)", "2021 (2.)", "2018 (3.)"]
```

`tools/merge_detail.py` **odrzuca zapis**, jeśli liczba lat/wpisów nie zgadza się z `counts` -
to jest bramka jakości, nie da się jej obejść.
