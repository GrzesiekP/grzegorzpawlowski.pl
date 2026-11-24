---
title: "Synchronizacja i porządek w repozytorium Git"
date: 2021-01-26
slug: "synchronizacja-i-porzadek-w-repozytorium"
permalink: /synchronizacja-i-porzadek-w-repozytorium/
categories: ["Git"]
excerpt: "Zdarzyło Ci się kiedyś rozsynchronizować swoją gałąź z masterem tak, że najsensowniejszym wyjściem było ją usunąć i utworzyć nową? A jeśli do tego dochodzi brak synchronizacji lokalnej gałęzi z…"
image: "/assets/images/0dd89b09-jest_git-1024x680.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Reset gałęzi nie jest zwykłą synchronizacją — odrzuca jej dotychczasowy stan. Dodałem warunek czystego katalogu roboczego, gałąź zapasową i zapis oczekiwanego stanu serwera. Zamiast bezwarunkowego `--force` używam `--force-with-lease` z konkretnym SHA. Przykłady są dla Basha; nazwy `master` i `feature-1` trzeba dopasować do repozytorium.

  Źródła: [git reset](https://git-scm.com/docs/git-reset), [git push i ograniczenia force-with-lease](https://git-scm.com/docs/git-push).
---

Zdarzyło Ci się kiedyś rozsynchronizować swoją gałąź z masterem tak, że najsensowniejszym wyjściem było ją usunąć i utworzyć nową? A jeśli do tego dochodzi brak synchronizacji lokalnej gałęzi z jej wersją na originie? Albo pomiędzy forkiem a upstreamem? Przyznam, że mnie się to zdarzało. Najlepszym rozwiązaniem jest oczywiście bardziej uważna praca z Gitem, żeby tego uniknąć, ale jeśli już jesteśmy w tej sytuacji, to kilka komend pozwoli zresetować naszą gałąź (lokalną i w originie) do dokładnie tego samego stanu, co master.

Jak to zrobić?

**Najpierw sprawdź, czy naprawdę chcesz nadpisać historię.** Jeżeli chcesz zachować zmiany z obu gałęzi, rozważ merge albo rebase, a nie reset. `git status --short` musi nie pokazywać zmian; w przeciwnym razie najpierw świadomie je zapisz. Gałąź zapasowa chroni commity, ale nie niezacommitowane pliki. `reset --hard` może także nadpisać nieśledzone pliki kolidujące z docelowym stanem. Nie wykonuj tych operacji na współdzielonej gałęzi bez uzgodnienia z zespołem.

### Synchronizacja branch-master (brak forka)

Załóżmy, że nasza gałąź nazywa się **feature-1**.

1. Przejdź na gałąź i upewnij się, że katalog roboczy jest czysty.
2. Pobierz aktualny stan serwera.
3. Utwórz gałąź zapasową pod nieużywaną nazwą i zapamiętaj SHA zdalnej gałęzi.
4. Dopiero wtedy zresetuj gałąź i wypchnij zmianę z kontrolą oczekiwanego SHA.

```bash
git checkout feature-1
git status --short
# Kontynuuj tylko, jeśli powyższe polecenie nic nie wypisało.
git fetch origin
git branch backup-feature-1
expected=$(git rev-parse origin/feature-1)
git reset --hard origin/master
git push --force-with-lease=refs/heads/feature-1:"$expected" origin HEAD:refs/heads/feature-1
```

Jeśli lease odrzuci push, nie obchodź go przez `--force`. Sprawdź nowe commity na serwerze i uzgodnij sposób ich zachowania. Polecenia wykonuj po kolei; po dowolnym błędzie przerwij.

### Synchronizacja upstream-fork

Tutaj pokażę to na przykładzie repozytorium *tslint-to-eslint-config*, z którego stworzyłem forka.

Dodałem jedną małą, ale bardzo ważną zmianę w Readme 😎

![](../assets/images/045573c8-small_change_in_code.jpg)

Jednocześnie trochę namieszałem 😱

![](../assets/images/45b02649-mess_in_git-1024x345.jpg)

A teraz jak z tego wybrnąć bez konieczności tworzenia forka od nowa?

Najpierw sprawdzam, czy mam poprawnie zdefiniowany origin: `git remote -v`. Powinienem zobaczyć coś takiego:

![](../assets/images/c775ad40-git_remote_-v.gif)

Robię zapasową gałąź, na której będą wszystkie commity, w tym superważna zmiana w README.

```bash
git checkout master
git status --short
# Kontynuuj tylko przy czystym katalogu roboczym.
git branch backup-master
git fetch origin
expected=$(git rev-parse origin/master)
```

Teraz, podobnie jak przy synchronizacji master-branch, resetuję mojego mastera do stanu upstreama:

```bash
git fetch upstream master
git reset --hard FETCH_HEAD
```

Na koniec jeszcze zbieram superważnego commita z mojej zapasowej gałęzi.

```bash
# Użyj SHA własnego commita odczytanego z backup-master.
git log --oneline backup-master
git cherry-pick SHA_COMMITA_DO_ZACHOWANIA
git push --force-with-lease=refs/heads/master:"$expected" origin HEAD:refs/heads/master
```

Zapis `SHA_COMMITA_DO_ZACHOWANIA` zastąp właściwym hashem; nie jest dosłownym argumentem. `FETCH_HEAD` powyżej oznacza wynik bezpośrednio poprzedzającego fetch — nie wykonuj między tymi poleceniami innego pobierania. Przy konfliktach najpierw je rozwiąż albo przerwij cherry-pick; nie przechodź do pushowania niegotowego stanu.

Teraz mogę podejrzeć na GitHubie, czy udało się zrobić porządek.

![](../assets/images/3cb8f79a-after_cleanup-1024x347.jpg)

### Bonus

Oczywiście zamiast pisać tyle komend, można to sobie opakować w skrypt i trzymać go pod aliasem, tak jak opisałem np. we wpisie [Alias w Gicie – jak i po co?](../alias-w-gicie-jak-i-po-co/).
