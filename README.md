# Grzegorz Pawłowski — blog

Prosta, statyczna strona na Jekyll i GitHub Pages. Artykuły są plikami Markdown w `_posts/`, a obrazy są przechowywane lokalnie w `assets/images/`. Nie ma WordPressa, bazy danych ani zewnętrznych usług potrzebnych do działania strony.

## Publikacja na GitHub Pages

1. Wypchnij repozytorium do GitHuba na gałąź `master`.
2. W repozytorium otwórz **Settings → Pages** i jako źródło wybierz **GitHub Actions**.
3. Workflow `Publish site` zbuduje i opublikuje stronę po każdym pushu na `master` (nie uruchamia się dla pull requestów).
4. Dla domeny `grzegorzpawlowski.pl` ustaw rekordy DNS zgodnie z instrukcją GitHub Pages i w **Settings → Pages** włącz wymuszenie HTTPS. Plik `CNAME` jest już przygotowany.

Przed przełączeniem DNS sprawdź, czy strona opublikowała się poprawnie pod adresem GitHuba. Nie wyłączaj jeszcze WordPressa — najpierw zweryfikuj artykuły, obrazy i stare adresy wpisów na wersji testowej.

## Dodawanie wpisu

Utwórz plik w `_posts/` o nazwie `RRRR-MM-DD-krotki-adres.md`:

```markdown
---
title: "Tytuł wpisu"
date: 2026-11-24
slug: moj-wpis
permalink: /moj-wpis/
categories: [Programowanie]
excerpt: "Krótki opis widoczny na stronie głównej."
image: /assets/images/obrazek.jpg
layout: post
---

Treść wpisu w Markdownie.
```

Obrazki dodaj do `assets/images/`; w treści wpisu odwołuj się do nich ścieżką względną, np. `../assets/images/obrazek.jpg`. Takie ścieżki i linki pozostają poprawne zarówno pod adresem GitHub Pages z nazwą repozytorium w ścieżce, jak i na własnej domenie. Następnie zrób commit i push. `slug` oraz `permalink` pozwalają zachować czytelny adres i nie zmieniać go przy edycji tytułu.

## Import z WordPressa

`python scripts/import_wordpress.py` pobiera publiczne wpisy z API WordPressa, konwertuje ich treść na Markdown i zapisuje używane obrazy lokalnie. **Importer nadpisuje pliki w `_posts/`. Po ręcznej korekcie archiwum nie uruchamiaj go ponownie na tych plikach** — ewentualne nowe wpisy importuj do osobnej kopii i przenoś pojedynczo, żeby nie utracić poprawek.

## Kontrola linków i obrazów

Po zbudowaniu strony uruchom `python scripts/check_site.py _site` (albo podaj inną ścieżkę do wyniku budowania). Skrypt sprawdzi lokalne linki, kotwice i obrazy zarówno dla własnej domeny, jak i dla adresu GitHub Pages z nazwą repozytorium w ścieżce. Nie wymaga dodatkowych bibliotek ani dostępu do sieci.

## Aktualizacja merytoryczna wpisu

Datę pierwotnej publikacji (`date`) i adres (`permalink`) pozostaw bez zmian. Notkę o korekcie dodaj w nagłówku pliku Markdown:

```yaml
updated: 2026-11-24
update_note: |
  Krótkie podsumowanie zmian i ograniczeń historycznego przykładu.

  Źródło: [dokumentacja](https://example.com/).
```

Notka obsługuje Markdown i pojawia się pod tytułem, przed okładką oraz treścią. Popraw też błędne fragmenty w samej treści; notka nie zastępuje korekty. `updated` jest wykorzystywane również w RSS.
