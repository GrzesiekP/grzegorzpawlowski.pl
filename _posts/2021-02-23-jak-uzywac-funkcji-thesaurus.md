---
title: "Jak używać funkcji – Thesaurus"
date: 2021-02-23
slug: "jak-uzywac-funkcji-thesaurus"
permalink: /jak-uzywac-funkcji-thesaurus/
categories: ["Google Sheets"]
excerpt: "Thesaurus (z łaciny skarbiec) – tak roboczo nazwałem projekt, w którym zebrałem kilka funkcji do używania przy monitorowaniu finansów w Arkuszach Google. W innych wpisach pokazywałem konkretne…"
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Instrukcja dotyczy [historycznego pliku z 2021 r.](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js). Dzisiejszy `master` ma inny interfejs i nie zawiera `GOLD_PRICE`, `NNTFI_FUND_PRICE` ani `THESAURUS_AVAILABLE`. Zrzuty przedstawiają dawny interfejs; edytor otwiera się obecnie przez **Rozszerzenia → Apps Script**. Nie wpisuj prawdziwego klucza do publicznego przykładu ani nie przyznawaj uprawnień bez sprawdzenia kodu.

  [Funkcje niestandardowe](https://developers.google.com/apps-script/guides/sheets/functions) mają limit 30 sekund i ograniczenia usług. Jednorazowe uruchomienie funkcji w edytorze nie znosi tych ograniczeń ani [limitów zapytań](https://developers.google.com/apps-script/guides/services/quotas).
---

Thesaurus (z łaciny skarbiec) – tak roboczo nazwałem projekt, w którym zebrałem kilka funkcji do używania przy monitorowaniu finansów w Arkuszach Google. W innych wpisach pokazywałem konkretne funkcje, ale teraz postanowiłem opublikować wszystkie skrypty w jednym pliku i opisać, jak z nich skorzystać – tak, żeby było to jak najłatwiejsze. Jest to prosta instalacja typu „copy-paste” 😎. Mam nadzieję, że uda Ci się wyciągnąć z tego projektu coś, czym kupisz sobie czas, wygodę i przejrzystość w monitorowaniu własnego skarbca.

#### Czego potrzebujesz?

- Kodu wersji opisanej we wpisie – znajdziesz go [w przypiętym commicie na GitHubie](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js).
- Do działania funkcji `CRYPTO_USD_PRICE` (opisałem ją we wpisie [Google Sheets #4: Cena kryptowaluty w Arkuszach Google](../cena-kryptowaluty-w-arkuszach-google/)) potrzebujesz klucza API CoinMarketCap (strony z kursami kryptowalut). Opis, jak go zdobyć, również znajdziesz we [wspomnianym wpisie](../cena-kryptowaluty-w-arkuszach-google/).

#### Instrukcja:

1. Otwórz edytor przez **Rozszerzenia → Apps Script**. Na historycznym zrzucie poniżej jest dawna ścieżka **Narzędzia → Edytor skryptów**.

![](../assets/images/b446d2d2-image-2.png)

2. Pojawi się kod skryptu ***Kod.gs***. Po przejrzeniu źródła zamień go na kod z [historycznej wersji *Thesaurus.js*](https://github.com/GrzesiekP/Thesaurus/blob/ec6600ee2090bfd0cb1e00055e1dcef49277d665/Thesaurus.js). Uwaga: odtwarza ona dawny przykład, nie gwarantuje działania nieaktualnych dostawców danych.

![](../assets/images/e19017ef-zamien-kod.gif)

3. Podmień w pierwszej linijce wartość `coinMarketCapApiKey` – zamiast `apiKey` wklej swój klucz API CoinMarketCap (**[skąd go wziąć?](../cena-kryptowaluty-w-arkuszach-google/)**) i kliknij ikonę zapisu, np.:

```
const coinMarketCapApiKey = "WKLEJ_WLASNY_KLUCZ";
```

4. W przypadku uruchamiania funkcji w edytorze może być potrzebna autoryzacja odpowiednich usług. Poniższe kroki i animacja ilustrują dawny ekran zgód. Sama funkcja niestandardowa wywołana z komórki nie wyświetla okna autoryzacji i nie może korzystać z dowolnych usług wymagających dostępu do danych użytkownika.

5. W górnym menu powinna być wybrana funkcja `THESAURUS_AVAILABLE`.

6. Kliknij ***Uruchom***, następnie ***Przejrzyj Uprawnienia***

7. Wybierz swoje konto Google.

8. Jeśli zobaczysz ostrzeżenie o niezweryfikowanej aplikacji, zatrzymaj się i sprawdź kod oraz żądane uprawnienia. To, że sam jesteś właścicielem skopiowanego projektu, nie oznacza, że cudzy kod jest bezpieczny.

9. Przejdź dalej tylko wtedy, gdy rozumiesz i akceptujesz dostęp, o który prosi projekt. „Projekt bez nazwy” to nazwa, którą możesz zmienić, a nie potwierdzenie zaufania.

10. Kliknij ***Zezwól***

![](../assets/images/decdd5ae-zeszwol-na-dostep-2.gif)

**Tak wyglądało uruchomienie historycznej wersji.** Do bieżącego użycia trzeba jeszcze sprawdzić dostępność dostawców, poprawność wyników i zgodność skryptu z limitami. Samo udzielenie zgód nie potwierdza działania funkcji.

Dokumentację i opis funkcji znajdziesz [na GitHubie](https://github.com/GrzesiekP/Thesaurus) oraz w innych wpisach z [serii Google Sheets](../category/google-sheets/).
