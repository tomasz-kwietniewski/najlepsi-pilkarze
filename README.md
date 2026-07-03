# Najlepsi piłkarze

Hobbystyczny ranking piłkarzy wg autorskiego systemu punktowego (trofea, występy,
gole ważone pozycją, nagrody indywidualne). Projekt z lat 2008-2010 (Tomasz + Emil),
odświeżony i wystawiony jako statyczna strona.

Strona: https://najlepsipilkarze.tomaszkwietniewski.pl

## Jak to zbudowane

Czysta statyka - żadnego PHP ani bazy. Publikowany jest tylko katalog `public/`:

- `public/data/players.json` - surowe dane wejściowe (pozycja, występy, gole, policzone trofea).
- `public/scoring.js` - reguły punktacji (jedna funkcja: dane -> punkty). Zmiana wagi = jedna liczba.
- `public/index.html` - samodzielny, interaktywny raport (ranking, sortowanie, filtry, rozbicie punktów).

Folder `docs/` to lokalny katalog roboczy (dane źródłowe, notatki) - poza repo i poza publikacją.

> Uwaga: obecny `public/index.html` to jeszcze przykładowa strona ze startera (placeholder),
> póki budujemy właściwy ranking. Każdy push do `main` publikuje aktualną wersję.

## Publikacja (GitHub Pages)

Push do `main` -> GitHub Actions publikuje stronę pod subdomeną (workflow
`.github/workflows/deploy-pages.yml`, autoryzacja tokenem OIDC, bez sekretów).

Subdomena: plik `public/CNAME` + rekord DNS `CNAME` (`najlepsipilkarze` -> `tomasz-kwietniewski.github.io`).
Źródło w repo: Settings -> Pages -> Source: **GitHub Actions**.

Status i logi: zakładka **Actions**. Ręczny deploy: Actions -> Deploy na GitHub Pages -> Run workflow.
