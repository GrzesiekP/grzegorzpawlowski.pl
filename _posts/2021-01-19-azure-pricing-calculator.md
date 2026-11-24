---
title: "Azure Pricing Calculator"
date: 2021-01-19
slug: "azure-pricing-calculator"
permalink: /azure-pricing-calculator/
categories: ["Azure"]
excerpt: "Azure Pricing Calculator to bardzo przydatne narzędzie, kiedy projektujesz rozwiązania z wykorzystaniem Azure i chciałbyś oszacować koszty utrzymania. Przydaje się także, kiedy tworzysz cokolwiek…"
image: "/assets/images/7552a937-AzureObrazekWyrozniajacy-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Kwoty i zrzuty poniżej to historyczny przykład z przełomu 2020/2021 r., nie aktualny cennik. Model rozliczania App Service Environment v3 różni się od dawnego Isolated/Stamp Fee; nawet puste środowisko może generować opłaty. Kalkulator podaje szacunek zależny m.in. od regionu, waluty, umowy i konfiguracji, a nie gwarantowaną fakturę.

  Aktualne źródła: [kalkulator Azure](https://azure.microsoft.com/en-gb/pricing/calculator/), [model cenowy ASE v3](https://learn.microsoft.com/en-us/azure/app-service/environment/overview#pricing).
---

Azure Pricing Calculator to bardzo przydatne narzędzie, kiedy projektujesz rozwiązania z wykorzystaniem Azure i chciałbyś oszacować koszty utrzymania. Przydaje się także, kiedy tworzysz cokolwiek na Azurze, żeby sprawdzić, ile za to zapłacisz i co na ten koszt się składa. W skrócie, pomaga wyliczyć, ile rzeczywiście kosztuje Azure.

Kalkulator sam w sobie jest bardzo wygodny w użyciu. Po prostu wchodzimy na [stronę kalkulatora](https://azure.microsoft.com/en-gb/pricing/calculator/), dodajemy interesujące nas zasoby do wyliczenia, klikając na nie, i dostosowujemy parametry (np. system operacyjny, region, liczbę instancji itp.).

![App Service - configuration in calculator](../assets/images/bf2d0acf-Screen1-1-1024x416.jpg)

Mamy podsumowanie kosztów każdego zasobu oraz koszt sumaryczny na samym dole. Wyliczeniom można nadać nazwę – np. nazwę projektu. Dzięki temu można lepiej odnaleźć się przy kilku wyliczeniach. Można je też zapisać lub wyeksportować do Excela.

Teoretycznie Azure Portal sam w sobie pokazuje koszty zasobu przy jego tworzeniu i są one także dostępne w [dokumentacji](https://azure.microsoft.com/en-gb/pricing/details/app-service/windows/). Nie zawsze jednak pokazana tam cena uwzględnia wszystkie koszty, a różnice potrafią być znaczące.

![Isolated - documentation pricing](../assets/images/333ebd8a-Screen2-1024x650.jpg)

W historycznym przykładzie App Service w wersji *ISOLATED* (OS Windows, region West Europe) wg ówczesnej dokumentacji kosztował ok. 219 USD miesięcznie. Wyliczenie tej konfiguracji w Azure Pricing Calculator pokazywało kwotę 1347 USD. Skromne 1128 USD różnicy. Tych kwot nie należy używać do dzisiejszych wycen.

![Pricing summary](../assets/images/02646de5-Screen3-1024x691.png)

Skąd aż taka różnica? Ówczesna dokumentacja wyjaśniała: “In addition to the price per Isolated plan instance, there is also a flat **Stamp Fee for each App Service Environment of $1.546/hour(~$1,128.360/month)**”. Cena $219 na historycznym zrzucie dotyczyła samej instancji, bez dawnego *Stamp Fee*.

Podczas przygotowania wpisu pod koniec grudnia 2020 r. pojawił się *Isolated v2 Plan<sup>PREVIEW</sup>* z innym modelem opłat, jeszcze niedostępny w moim ówczesnym widoku kalkulatora. Dzisiejsze zasady ASE v3 sprawdź w dokumentacji podanej u góry; brak starego Stamp Fee nie oznacza braku minimalnego kosztu środowiska.

![Isolated v2 App Service Plan](../assets/images/17b62fa7-Screen4-1024x311.jpg)

Interesujesz się Azure? Już niedługo pojawią się kolejne wpisy w cyklu [Azure](../category/azure/).
