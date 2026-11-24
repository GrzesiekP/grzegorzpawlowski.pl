---
title: "Cena Kryptowaluty w Arkuszach Google"
date: 2021-02-23
slug: "cena-kryptowaluty-w-arkuszach-google"
permalink: /cena-kryptowaluty-w-arkuszach-google/
categories: ["Google Sheets", "Kryptowaluty"]
excerpt: "Kolejny skrypt rozszerzający funkcjonalność Arkuszy Google przy wykorzystaniu ich do monitorowania finansów przyda się inwestującym w kryptowaluty. To funkcja CRYPTO_USD_PRICE , która zwraca cenę…"
image: "/assets/images/61039a30-GoogleSheetsCategoryLogo-1024x512.jpg"
layout: post
---

Kolejny skrypt rozszerzający funkcjonalność Arkuszy Google przy wykorzystaniu ich do monitorowania finansów przyda się inwestującym w kryptowaluty. To funkcja `CRYPTO_USD_PRICE`, która zwraca cenę danej kryptowaluty w dolarach według kursu [CoinMarketCap](https://coinmarketcap.com/) (jedna z najpopularniejszych stron z kursami).

Co prawda, ceny najpopularniejszych krypto jak BTC i ETH można pobrać korzystając z `GOOGLEFINANCE`, ale jeśli masz jakieś mniej popularne altcoiny, nie uda Ci się. Dzięki tej funkcji w praktyce, możesz pobrać cenę każdej kryptowaluty, która jest dostępna na CoinMarketCap.

#### Jak jej używać?

Po pierwsze, potrzebujesz klucza API CoinMarketCap – to sposób, w jaki zabezpieczają swoje API przed przeciążeniem zbyt dużą liczbą zapytań. Zdobycie klucza jest bezproblemowe:

1. Wchodzisz na [stronę rejestracji API CoinMarketCap](https://pro.coinmarketcap.com/signup) i zakładasz konto.
2. Po założeniu konta logujesz się i wchodzisz na [pro.coinmarketcap.com/account](https://pro.coinmarketcap.com/account) .
3. Po najechaniu kursorem (jak na poniższym gifie) zobaczysz swój API Key i będziesz mógł go skopiować.

![](/assets/images/56acf205-copy_cmc_apiKey.gif)

Następnie klucz trzeba podmienić w kodzie, który musisz skopiować do edytora skryptów w Arkuszach Google tak, jak to opisałem we wpisie **[Google Sheets #3: Jak Używać Funkcji](/jak-uzywac-funkcji-thesaurus/)**

Mając to wszystko, wystarczy podać ticker (symbol danej kryptowaluty, który znajdziesz na CoinMarketCap – zaznaczony na obrazku poniżej) jako argument, np. :

```
=CRYPTO_USD_PRICE("BTC")
```

![](/assets/images/7a4aff79-image-4-1024x227.png)

Jak zawsze, kod znajdziesz [na GitHubie](https://github.com/GrzesiekP/Thesaurus). Jeśli chcesz poczytać o kryptowalutach dla początkujących, sprawdź serię [Krypto Dla Leniwych](/category/kryptowaluty/), gdzie staram się w prosty sposób przekazać to, co najważniejsze w temacie.
