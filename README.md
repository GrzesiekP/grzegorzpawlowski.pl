# Grzegorz Pawłowski — blog

Prosta, statyczna strona na Jekyll i GitHub Pages. Artykuły są plikami Markdown w `_posts/`, a obrazy są przechowywane lokalnie w `assets/images/`. Nie ma WordPressa, bazy danych ani zewnętrznych usług potrzebnych do działania strony.

## Publikacja na GitHub Pages

1. Wypchnij repozytorium do GitHuba na domyślną gałąź (`main` lub `master`).
2. W repozytorium otwórz **Settings → Pages** i jako źródło wybierz **GitHub Actions**.
3. Workflow `Publish site` zbuduje i opublikuje stronę po każdym pushu.
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

Obrazki dodaj do `assets/images/`, a następnie zrób commit i push. `slug` oraz `permalink` pozwalają zachować czytelny adres i nie zmieniać go przy edycji tytułu.

## Import z WordPressa

`python scripts/import_wordpress.py` pobiera publiczne wpisy z API obecnej strony, konwertuje ich treść na Markdown i zapisuje używane obrazy lokalnie. Uruchom importer ponownie, jeśli przed migracją pojawią się nowe wpisy. Importer nadpisuje wygenerowane pliki w `_posts/` — ręczne zmiany treści w tych plikach wykonuj po ostatnim imporcie.
