---
title: "Cena Złota w Arkuszach Google"
date: 2020-09-25
slug: "jak-pobrac-cene-zlota-w-google-sheets"
permalink: /jak-pobrac-cene-zlota-w-google-sheets/
categories: ["Google Sheets"]
excerpt: "Prosty arkusz kalkulacyjny w Google Sheets może zastąpić Ci skomplikowane i często płatne aplikacje do monitorowania Twoich inwestycji (lub ogólnie Twojego majątku). Rozszerzony o dodatkowe…"
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
---

Prosty arkusz kalkulacyjny w Google Sheets może zastąpić Ci skomplikowane i często płatne aplikacje do monitorowania Twoich inwestycji (lub ogólnie Twojego majątku). Rozszerzony o dodatkowe funkcji, pozwoli Ci w prosty sposób monitorować na bieżąco także cenę złota.

Na początek polecam zapoznać się z funkcją `GOOGLEFINANCE`, której dokumentację znajdziesz [tu](https://support.google.com/docs/answer/3093281?hl=en), a której przydatne zastosowanie pokażę w innym wpisie.

Niestety są dane, których nie pobierzesz dzięki `GOOGLEFINANCE`. Jedną z nich jest aktualna cena złota. Na szczęście w Google Sheets można definiować własne funkcje pisane w JavaScript. Pierwszą z nich jest `GOLD_PRICE` – funkcja zwracająca cenę złota w podanej walucie.

#### Jak używać funkcji?

Przede wszystkim musisz najpierw mieć jej kod. Opis, skąd go wziąć i jak z niego w prosty sposób korzystać znajdziesz we wpisie [Google Sheets #3: Jak Używać Funkcji – Thesaurus](../jak-uzywac-funkcji-thesaurus/)  
Mając zainstalowany kod, wystarczy zawołać funkcję:

```
=GOLD_PRICE("PLN")
```

Cały kod znajdziesz tej oraz innych funkcji znajdziesz na [moim GitHubie](https://github.com/GrzesiekP/Thesaurus).

Jeśli widzisz, co można by usprawnić albo co byłoby przydatnej w tej lub podobnej funkcji, daj znać w komentarzu!
