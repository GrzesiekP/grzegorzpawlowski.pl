---
title: "Cena złota w Arkuszach Google"
date: 2020-09-25
slug: "jak-pobrac-cene-zlota-w-google-sheets"
permalink: /jak-pobrac-cene-zlota-w-google-sheets/
categories: ["Google Sheets"]
excerpt: "Prosty arkusz kalkulacyjny w Google Sheets może zastąpić Ci skomplikowane i często płatne aplikacje do monitorowania Twoich inwestycji (lub ogólnie Twojego majątku). Rozszerzony o dodatkowe…"
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Ten wpis opisuje historyczną funkcję `GOLD_PRICE` z [wersji Thesaurusa z 2021 r.](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js), a nie aktualną gałąź `master`, w której tej funkcji już nie ma. Kod korzystał z niegwarantowanego zewnętrznego endpointu i zwracał kurs XAU (uncji trojańskiej), nie cenę grama ani cenę sprzedaży fizycznego złota. Nie potwierdzam dziś działania tego historycznego endpointu.

  [GOOGLEFINANCE](https://support.google.com/docs/answer/3093281?hl=en) nie jest kompletnym źródłem dowolnych notowań; dane mogą być opóźnione i nie są przeznaczone do podejmowania decyzji transakcyjnych.
---

Prosty arkusz kalkulacyjny w Google Sheets może zastąpić Ci skomplikowane i często płatne aplikacje do monitorowania Twoich inwestycji (lub ogólnie Twojego majątku). Rozszerzony o dodatkowe funkcje pozwoli Ci w prosty sposób monitorować na bieżąco także cenę złota.

Na początek polecam zapoznać się z funkcją `GOOGLEFINANCE`, której dokumentację znajdziesz [tu](https://support.google.com/docs/answer/3093281?hl=en), a której przydatne zastosowanie pokażę w innym wpisie.

Niestety `GOOGLEFINANCE` nie gwarantuje obsługi wszystkich instrumentów, rynków i atrybutów. Dlatego do tego przykładu przygotowałem własną funkcję w JavaScripcie: `GOLD_PRICE`, która pobierała notowanie złota w podanej walucie. Wynik dotyczył uncji trojańskiej (ok. 31,1035 g). Nie należy go mylić z ceną grama ani ofertą kupna sztabki — ta uwzględnia też m.in. spread i marżę sprzedawcy.

#### Jak używać funkcji?

Przede wszystkim musisz najpierw mieć jej kod. Opis, skąd go wziąć i jak z niego w prosty sposób korzystać, znajdziesz we wpisie [Google Sheets #3: Jak używać funkcji – Thesaurus](../jak-uzywac-funkcji-thesaurus/).

Mając zainstalowany kod, wystarczy zawołać funkcję:

```
=GOLD_PRICE("PLN")
```

Kod tej oraz pozostałych funkcji z czasu publikacji znajdziesz w [historycznej wersji na GitHubie](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js). Przykład dokumentuje pomysł integracji; przed ponownym użyciem trzeba sprawdzić dostawcę danych, warunki dostępu i obsługę błędów odpowiedzi.

Jeśli widzisz, co można by usprawnić albo co byłoby przydatne w tej lub podobnej funkcji, daj znać przez [stronę kontaktową](../kontakt/)!
