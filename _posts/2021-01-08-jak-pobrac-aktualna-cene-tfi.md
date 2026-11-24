---
title: "Jak pobrać aktualną cenę TFI w Google Sheets"
date: 2021-01-08
slug: "jak-pobrac-aktualna-cene-tfi"
permalink: /jak-pobrac-aktualna-cene-tfi/
categories: ["Google Sheets"]
excerpt: "Historyczny przykład pobierania wyceny jednostki funduszu do Arkuszy Google: funkcja NNTFI_FUND_PRICE i ograniczenia parsowania dawnej strony NN TFI."
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Poprawna nazwa funkcji w [kodzie z 2021 r.](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js) to `NNTFI_FUND_PRICE`, nie `NN_FUND_PRICE`. Historyczny URL NN TFI już nie działa, a bieżąca gałąź `master` nie zawiera tej funkcji. Poniżej pozostaje przykład parsowania dawnej strony, nie działająca instrukcja pobierania dzisiejszych wycen.

  Wycenę jednostki funduszu odróżniaj od ceny transakcyjnej i danych na żywo. Parser powinien odrzucać błędny HTTP, brak znacznika oraz wynik nienumeryczny, zamiast zwracać przypadkowy fragment HTML-a.
---

Fundusze inwestycyjne zarządzane przez TFI mogą być jedną z form inwestowania w ramach IKE/IKZE. TFI to towarzystwo zarządzające funduszami, nie sam instrument finansowy. Stwierdziłem, że skoro chcę mieć w swoim arkuszu szybki podgląd stanu inwestycji, to warto, żeby znalazły się tam także wyceny moich jednostek funduszy. Nie chcę jednak za każdym razem wchodzić na stronę NN TFI i spisywać cen.

**Na początek zaznaczę, że opisywana tutaj funkcja do Arkuszy Google to jedna z kilku, które znacznie ułatwiają używanie Arkuszy jako narzędzia do monitorowania finansów. Jeśli chciałbyś je wykorzystać, żeby usprawnić swój arkusz, zajrzyj do wpisu [Google Sheets #3: Jak używać funkcji – Thesaurus](../jak-uzywac-funkcji-thesaurus/).**

A teraz do rzeczy!

### Ceny funduszy NN TFI w jednym miejscu

Napisałem funkcję `NNTFI_FUND_PRICE`, żeby nie musieć wchodzić na stronę notowań za każdym razem, gdy chcę sprawdzić wartość środków w ramach IKE/IKZE w NN TFI.

### Jak jej użyć?

Potrzebujesz dwóch zmiennych – kategorii i nazwy funduszu. Wejdź na stronę z notowaniami interesującego funduszu i skopiuj je z adresu URL, np.:

`https://www.nntfi.pl/fundusze-inwestycyjne/fundusze-obligacji/nn-obligacji?unitsCategoryId=K`

To adres z oryginalnego przykładu, obecnie niedostępny. Kategoria to `fundusze-obligacji`, a nazwa funduszu to `nn-obligacji`.

Podaj kategorię jako pierwszy argument, a nazwę jako drugi:

`=NNTFI_FUND_PRICE("fundusze-obligacji"; "nn-obligacji")`

## Szczegóły techniczne

Jeśli nie czujesz JS-a, parsowania HTML-a regexem lub nie interesują Cię szczegóły techniczne, to możesz spokojnie pominąć tę część.

### Pierwsze podejście – API

W dobrej wierze i zakładając, że IT mocno weszło w świat finansów, zacząłem od szukania API – najpierw udostępnionego przez NN TFI, a potem jakiegokolwiek innego, gdzie podaję jakiś indywidualny identyfikator funduszu i dostaję jego cenę – tak jak można to zrobić np. z kryptowalutami. Niestety, zawiodłem się. **Gdybyś Ty natrafił na tego typu API, to będę bardzo wdzięczny, jeśli podzielisz się informacją przez [stronę kontaktową](../kontakt/).**

### Proste podejście – HTML

Skazano mnie na wyciąganie ceny funduszu z HTML-a. Pomyślałem przez chwilę o parsowaniu go regexem, ale mam do tego dziwną awersję.

![Mem o parsowaniu HTML-a wyrażeniami regularnymi](../assets/images/5afa18fe-regex.jpg)

Źródło: [DevHumor – Using regex to parse HTML](https://devhumor.com/media/using-regex-to-parse-html).

Do prostego wyciągnięcia jednego stringa z HTML-a wystarczą proste operacje na stringach. Podobno *jak coś jest głupie, ale działa, to nie jest głupie*.

Poniższy fragment działa na przekazanym tekście HTML, nie pobiera danych z wyłączonego serwisu. Dodaję brakujące sprawdzenie znacznika i wyniku:

```javascript
function parseHistoricalFundPrice(result) {
    const pattern = '<div class="end_date_price"><span class="fund_value">';
    const markerIndex = result.lastIndexOf(pattern);
    if (markerIndex < 0) throw new Error('Nie znaleziono wyceny w HTML-u.');

    const rest = result.slice(markerIndex + pattern.length);
    const endIndex = rest.indexOf('<');
    if (endIndex < 0) throw new Error('Niekompletny znacznik wyceny.');

    const value = rest.slice(0, endIndex).trim()
        .replace(/&nbsp;|&#160;/g, '')
        .replace(/[\s\u00a0]/g, '').replace(',', '.');
    if (!/^\d+(\.\d+)?$/.test(value)) throw new Error('Niepoprawna wycena.');

    const price = Number(value);
    if (!Number.isFinite(price)) throw new Error('Wycena poza zakresem.');
    return price;
}
```

To nadal parser konkretnego, historycznego formatu. Po stronie pobierania trzeba osobno sprawdzić kod HTTP, a zmiana struktury strony wymaga aktualizacji parsera. Jeśli dostawca oferuje udokumentowany eksport lub API, będzie to stabilniejsza podstawa integracji.

Historyczny kod znajdziesz w [przypiętej wersji Thesaurusa](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js); powyższe dodatkowe sprawdzenia parsera są korektą w tym wpisie, nie częścią tamtego commita.
Jeśli widzisz, co można by usprawnić albo co byłoby przydatne w tej lub podobnej funkcji, daj znać przez [stronę kontaktową](../kontakt/)!
