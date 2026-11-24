---
title: "Jak Pobrać Aktualną Cenę TFI w Google Sheets"
date: 2021-01-08
slug: "jak-pobrac-aktualna-cene-tfi"
permalink: /jak-pobrac-aktualna-cene-tfi/
categories: ["Google Sheets"]
excerpt: "TFI w ramach IKE/IKZE to popularny sposób inwestowania. Stwierdziłem, że skoro chcę mieć w swoim arkuszu szybki podgląd na stan inwestycji, to warto, żeby i moje TFI się tam znalazły (mimo, że…"
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
---

TFI w ramach IKE/IKZE to popularny sposób inwestowania. Stwierdziłem, że skoro chcę mieć w swoim arkuszu szybki podgląd na stan inwestycji, to warto, żeby i moje TFI się tam znalazły (mimo, że kwoty są niewielkie). Nie chcę jednak za każdym razem wchodzić na stronę NN TFI i spisywać aktualnych cen.

**Na początek zaznaczę, że opisywana tutaj funkcja do Arkuszy Google to jedna z kilku, które znacznie ułatwiają używanie Arkuszy, jako narzędzia do monitorowania finansów. Jeśli chciałbyś je wykorzystać, żeby usprawnić swój arkusz, zajrzyj do wpisu [Google Sheets #3: Jak Używać Funkcji – Thesaurus](/jak-uzywac-funkcji-thesaurus/)**

A teraz do rzeczy!

### Ceny funduszy NN TFI w jednym miejscu

Napisałem funkcję `NN_FUND_PRICE`, żeby nie musieć wchodzić na stronę notować za każdym razem, gdy chcę sprawdzić wartość środków w ramach IKE/IKZE w NN TFI.

### **Jak jej użyć**?

Potrzebujesz dwóch zmiennych – kategorii i nazwy funduszu. Wejdź na stronę z notowaniami interesującego funduszu i skopiuj je z adresu URL np.:  
  
*[https://www.nntfi.pl/fundusze-inwestycyjne/fundusze-obligacji/nn-obligacji?unitsCategoryId=K](https://www.nntfi.pl/fundusze-inwestycyjne/fundusze-obligacji/nn-obligacji?unitsCategoryId=K)*  
  
Zaznaczyłem na zielono kategorię funduszu, a na niebiesko nazwę.

Podaj kategorię jako pierwszy argument, a nazwę jako drugi

`=NN_FUND_PRICE("fundusze-obligacji"; "nn-obligacji")`

## Szczegóły techniczne

Jeśli nie czujesz JS-a, parsowania HTML-a regexem lub nie interesują Cię szczegół techniczne, to możesz spokojnie pominąć tę część.

### Pierwsze podejście – API

W dobrej wierze i zakładając, że IT mocno weszło w świat finansów, zacząłem od szukania API – najpierw udostępnionego przez NN TFI, a potem jakiegokolwiek innego, gdzie podaję jakiś indywidualny identyfikator fundusz i dostaję jego ceną – tak, jak można to zrobić np. z kryptowalutami. Niestety, zawiodłem się. **Gdybyś Ty natrafił na tego typu API, to będę bardzo wdzięczny, jeśli podzielisz się informacją w komentarzu.**

### Proste podejście – HTML

Skazano mnie na wyciąganie ceny funduszu z HTML-a. Pomyślałem przez chwilę o parsowaniu go Regexem, ale mam do tego dziwną awersję

![Parsing HTML with regex meme](/assets/images/5afa18fe-regex.jpg)https://devhumor.com/media/using-regex-to-parse-html

Do prostego wyciągnięcia jednego stringa z HTML-a wystarczą proste operacje na stringach. Podobno *jak coś jest głupie, ale działa, to nie jest głupie*.

```
    const pattern = '<div class="end_date_price"><span class="fund_value">'
    const startIndex = result.lastIndexOf(pattern) + pattern.length
    const newString = result.substring(startIndex)
    const endIndex = newString.indexOf(' <')
    const priceString = newString.substr(0, endIndex).replace(',', '.')

    const price = parseFloat(priceString)
```

Cały kod tej i pozostałych funkcji znajdziesz, jak zawsze, na [moim GitHubie](https://github.com/GrzesiekP/Thesaurus).  
Jeśli widzisz, co można by usprawnić albo co byłoby przydatnej w tej lub podobnej funkcji, daj znać w komentarzu!
