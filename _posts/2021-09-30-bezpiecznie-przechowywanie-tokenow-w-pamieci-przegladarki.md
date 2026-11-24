---
title: "Bezpieczne Przechowywanie Tokenów w Pamięci Przeglądarki"
date: 2021-09-30
slug: "bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki"
permalink: /bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki/
categories: ["Bezpieczeństwo"]
excerpt: "Jest kilka rodzajów pamięci przeglądarki, w których można przechowywać wrażliwe dane, jak np tokeny. Różnią się one między innymi funkcjonalnością, stopniem izolacji i możliwościami zabezpieczenia…"
image: "/assets/images/60233684-sejf.jpeg"
layout: post
---

Jest kilka rodzajów pamięci przeglądarki, w których można przechowywać wrażliwe dane, jak np tokeny. Różnią się one między innymi funkcjonalnością, stopniem izolacji i możliwościami zabezpieczenia przed atakami. Które rozwiązanie jest najbezpieczniejsze?

## Rodzaje zagrożeń

Żeby mówić o bezpieczeństwie, spójrzmy najpierw na zagrożenie, przed którym mamy się bronić. W przypadku kodu na front-endzie, weźmy na warsztat następujące rodzaje ataków.

### XSS – Cross-Site Scripting

XSS polega na uruchomieniu w przeglądarce kodu JavaScript, który wykona jakiś atak, np. odczyta token i prześle go do atakującego. Zazwyczaj ma miejsce, gdy złośliwy kod JS jest jakoś wstrzyknięty do aplikacji i uruchomiony po stronie klienta, w przeglądarce innego użytkownika – ofiary. Np. jeśli na jakiejś stronie można publikować własny HTML, można zawrzeć w nim taki obrazek `<img src='x' onerror='alert('Hacked!')'/>`, który w przeglądarce ofiary wykona kod `onerror`.

### XDS – Cross-Directory Scripting

XDS ma taki sam cel, jak XSS, ale inną drogę działania. Jest możliwy, kiedy aplikacje, które powinny być odizolowane wcale takie nie są. Na przykład, kiedy są na tej samej domenie, ale pod inną ścieżką: `[https://grzegorzpawlowski.pl/safeapp](/)` oraz  `[https://example.com/notsafeapp](https://grzegorzpawlowski.pl/safeapp)`. W obu przypadkach mamy ten sam origin (poniżej wyjaśnienie, czym jest origin), więc zabezpieczenia polegające na izolacji per origin nie zadziałają.

### CSRF (XSS+CSRF) – Cross-Site Request Forgery

CSRF to wykonanie niepożądanego requestu w imieniu ofiary ataku. Przykład: atakiem XSS wstrzykujemy złośliwy kod JS, który wykonuje takie żądanie to api zabezpieczonego tokenem. Nie musimy mieć dostępu do samego tokena, ale możemy robić autoryzowanie nim żądania do backendu. Przed CSRF można się chronić, ale to temat na osobny tekst.

## CORS Policy i Same Origin Policy

Zanim przejdziemy do omawiania sposobów przechowywania i ich bezpieczeństwa, wyjaśnię jeszcze dwie kwestie: co to jest polityka CORS i Origin.

**Origin** to zestaw **protokół, host, port**. Jeśli zmieni się któraś ze składowych, zmieni się origin. Zobaczmy na przykładzie adresu, który warto znać, jak w górach spadnie śnieg: [https://kaukazwypozyczalnia.pl:443/cennik](https://kaukazwypozyczalnia.pl/cennik/)

| **URL** | **Różnica** | **Powód** |
| --- | --- | --- |
| https://kaukazwypozyczalnia.pl:8080/cennik | Inny Origin | Inny port |
| http://kaukazwypozyczalnia.pl:443/cennik | Inny Origin | Inny protokół |
| https://kaukazwypozyczalnia.pl:443/kontakt | Ten sam Origin | Zmiana ścieżki |
| https://kaukazwypozyczalnia.net:443/cennik | Inny Origin | Inna domena (host) |
| https://kaukazwypozyczalnia.pl/cennik | Ten sam Origin | Port niesprecyzowany |

**CORS** (Cross-Origin Resource Sharing) – współdzielenie zasobów pomiędzy originami. Polityka CORS określa, czy i na jakich zasadach może się to odbywać.

**Same Origin Policy** (ten sam origin) oznacza po prostu, że zasoby są niedostępne dla innego originu.

Jak Same Origin Policy może zablokować atak XSS? Rozpatrzmy bardzo podstawowy scenariusz:

1. Użytkownik jest zalogowany np. do konta na giełdzie kryptowalut (np. [BitBay](https://auth.bitbay.net/ref/446BpO5Lw0Ic) )*, więc przeglądarka przechowuje jakiś token dostępu.
2. Odwiedza złośliwą stronę `https://bezpiecznydarmowydogecoin.com`
3. Kod JS ze złośliwej strony chce wysłać żądanie do API giełdy (np. przelać wszystkie BTC ofiary na portfel atakującego), do czego potrzebuje tokena. A tu psikus! Origin `https://bezpiecznydarmowydogecoin.com` , z którego pochodzi złośliwy kod i origin https://bitbay.net są różne, więc kod ze złośliwej strony nie będzie miał dostępu do danych pochodzących z origina `https://bitbay.net` .

**Jeśli trzymasz kryptowaluty na giełdzie, to przeczytaj np. [tutaj](/kryptowaluty-9-bledow-poczatkujacych/), dlaczego to nie jest bezpieczny pomysł.*

## Sposoby Przechowywania

### Pamięć Lokalna – Local Storage

Local Storage oferuje izolację przez Same Origin Policy, co oznacza (jak powyżej wyjaśniłem), że kod JS z origina A nie ma dostępu do zasobów w pamięci lokalnej pochodzących z origina B.

Dane są w tym przypadku przechowywane niezależnie od sesji, więc jeśli użytkownik zamknie okno lub kartę, a później otworzy ją ponownie, nadal będzie miał dostęp do danych z pamięci lokalnej.

Ataki XSS są możliwe, kiedy dane w pamięci pochodzą z tego samego origina. Przykład klasycznego XSS: użytkownik A wstrzykuje kod JS przez podatną aplikację (np jako url do obrazka), który uruchamia się u użytkownika B, który oczekiwał, że aplikacja jest bezpieczna i w kodzie JS przyjdzie tylko adres URL obrazka. Złośliwy kod ma dostęp do danych z pamięci lokalnej

Pamięć lokalna jest także podatna na ataki XDS, opisane na początku.

Istotny jest fakt, że token z pamięci lokalnej, żeby został wysłany do backendu, musi zostać w kodzie frontendowym odczytany z pamięci i przesłany np. w nagłówku. Z jednej strony jest to dodatkowa rzecz do zaimplementowania, z drugiej daje kontrolę nad danymi i zabezpiecza przed atakiem CSRF.

#### Podsumowanie

##### Zalety

- Izolacja per origin.
- Dane nie mogą zostać automatycznie wysłane do backendu – zabezpieczenie przed CSRF.
- Dane są zachowywane pomiędzy sesjami – jest do nich dostęp z innych kart, okna, czy po przeładowaniu strony.

##### Wady

- Dane są łatwo dostępne dla ataku XSS.

### Pamięć Sesji – Session Storage

Ta opcja też oferuje izolację zgodnie z Same Origin Policy. Różnica jest jednak taka, że dane są usuwane, kiedy kończy się sesja. Dane nie są współdzielone między kartami, oknami czy iframe’ami, co daje kolejną korzyść z punktu widzenia bezpieczeństwa. Rozważmy przykład:

1. Użytkownik jest zalogowany do strony (np. Facebook), sesja jest aktywna, a token przechowywany w pamięci sesji.
2. Klika złośliwy link, pod którym kryje się atak XSS.
3. Link otwiera się albo w nowej lub tej samej karcie.
4. W obu przypadkach z poprzedniego punktu będzie to nowa sesja, która nie ma dostępu do pamięci sesji poprzedniej (z Facebooka), więc złośliwy kod nie będzie miał dostępu do tokena.

Fakt, że dane w pamięci sesji nie są współdzielone między sesjami uniemożliwia już atak XDS, na które byliśmy narażeni używając pamięci lokalnej.

#### Podsumowanie

##### Zalety

- Izolacja per origin.
- Dane nie mogą zostać automatycznie wysłane do backendu, więc jest zabezpieczenie przed CSRF.
- Atak XSS nie jest możliwy poza obrębem sesji.

##### Wady

- Dane nadal dostępne dla ataku XSS w obrębie sesji.

### Ciasteczka

W przypadku ciasteczek, zabezpieczenie zależy od ustawionych flag, a konkretnie od `HttpOnly`.

Jeśli `HttpOnly`jest włączona, ciasteczko jest niedostępne dla kodu JS, więc token w nim przechowywany jest zabezpieczony przed dostępem ze złośliwego kodu z ataku XSS. Jednocześnie jednak JS aplikacji frontendowej również nie ma dostępu do tokena, więc w przypadku niektórych aplikacji po prostu nie możemy z tego rozwiązania skorzystać ze względów funkcjonalnych. Biorąc jednak pod uwagę, że tokenów zazwyczaj używamy, żeby uwierzytelnić się w jakimś API, to ograniczenie jest raczej rzadkie.

Token w ciasteczku `HttpOnly`jest zabezpieczony przed atakiem XSS, ale nadal można się do niego dostać przy pomocy ataku XSS+CSRF.

Ciasteczka powinny mieć zawsze `HttpOnly:true` jeśli zawierają wrażliwe dane. W innym przypadku można je wyciągnąć w prosty sposób:

```
document.cookie
   .split('; ')
   .find(r => r.startsWith('secretAccessToken'))
   .split('=')[1]
```

Nawet nie znając klucza, pod jakim zapisany jest token można po prostu pobrać wszystkie ciasteczka i poszukać, czy jest w nich coś przydatnego do ataku.

#### Podsumowanie

##### Zalety

- Z włączoną flagą `HttpOnly` , żaden kod JS, w tym złośliwy nie ma dostępu do ciasteczka.

##### Wady

- Rozwiązanie jest podatne na CSRF.
- Zaufany kod frontendowy też nie ma dostępu do danych w ciasteczkach.

### In-Memory

Wydaje się to być najbezpieczniejszy z omawianych sposobów na przechowywanie wrażliwych danych. Jednak samo stwierdzenie, że można bezpiecznie przechowywać dane in-memory jest błędne, bo wszystko zależy od implementacji tego rozwiązania.

**Rozważmy następujące przykłady**

Załóżmy, że w HTML jest pole `secretInput`, gdzie przesyłamy sekret oraz metoda , która zapisuje go w pamięci (in-memory).

#### Przykład 1 – globalna zmienna

```
funtion saveSecret() {
   secret = document.getElementById('secretInput').value;
}
```

Tutaj nie ma praktycznie żadnego zabezpieczenia. Zmienna `secret` jest globalnie dostępna dla złośliwego kodu. Jak można przechować sekret, żeby nie był tak wystawiony?

#### Przykład 2 – stała

```
funtion saveSecret() {
   const secret = document.getElementById('secretInput').value;
   globalData['secret'] = secret
}
```

Zapisanie do stałej `secret`, powoduje, że jest ona dostępna tylko w zakresie funkcji `saveSecret`.

Problem może się pojawić, kiedy później wartość `secret`zostanie przypisana do innej zmiennej, która jest widoczna do złośliwego kodu, jak w tym przypadku do `globalData`.

#### Przykład 3 – domknięcie (closure)

Obejściem powyższego problemu jest domknięcie funkcji (w celu emulacji metody prywatnej). W tym przykładzie wewnątrz funkcji `fetchToken`, token jest pobierany z serwera i zapisywany do lokalnej zmiennej. Natomiast`fetchToken`jest zamknięta w zewnętrznej funkcji, dzięki czemu zmienne z`fetchToken`nie są dostępne poza zewnętrzną metodą.

```
let token = (function() {
  async function fetchToken() {
    let fetchedToken;
    const request = new Request("http://example.com/token");
    let response = await window.fetch(request)
    fetchedToken = await response.json()
  }

  return {
    value: function() {
      return fetchToken();
    }
  };
})();
```

Takie zabezpieczenie działa pod dwoma warunkami. Po pierwsze, zamknięta funkcja **nie może zwracać zmiennej zawierającej token**. Zwracana z funkcji wartość będzie widoczna dla złośliwego kodu, więc token zostanie odkryty w przypadku ataku. Po drugie, jeśli zamknięta metoda korzysta z zewnętrznie zdefiniowanych metod, np. natywnej `fetch`, **można zaatakować podstawiając swój kod za tę metodę**. Takie podstawienie można zrobić wstrzykując następujący kod:

```
let fetch = window.fetch;
window.fetch = async function() { 
  let fetchPromise = fetch.apply(this, arguments);
  let resp = await fetchPromise;
  let json = await resp.json();
  alert(JSON.stringify(json));
  return fetchPromise
};
```

W powyższym przykładzie podstawiony fałszywy `fetch` woła prawdziwą metodę `fetch`, przechwytuje zwracany z niej wynik, a następnie zwraca go, jak gdyby robiła to oryginalna metoda.

Jest i na to zabezpieczenie.

#### Przykład 4 – domknięcie + lokalna kopia podatnej metody

W tym przypadku wszystko wygląda tak samo za wyjątkiem tego, że na początku do lokalnej zmiennej przypisujemy natywną metodę `window.fetch`, żeby mieć pewność, że korzystamy z niej, a nie z podstawionej.

```
let token = (function() {
  let localFetch = window.fetch;
  async function localFetchToken() {
    let fetchedToken ;
    const request = new Request("http://localhost:3000/secret");
    let response = await localFetch(request)
    fetchedToken = await response.json()
  }

  return {
    value: function() {
      return localFetchToken();
    }
  };
})();
```

W tym przypadku podstawiona metoda nie przechwyci tokena, ponieważ wewnątrz `localFetchToken` wołamy lokalną kopię `window.fetch`, a nie po prostu `fetch`, która może zostać podstawiona.

Niestety, to rozwiązanie też nie jest idealne. Im więcej zewnętrznie zdefiniowanych funkcji używamy w naszej zamkniętej metodzie, tym więcej lokalnych kopii trzeba zrobić. To się po prostu źle skaluje. Jeśli do tego dodać, że możemy używać zewnętrznych bibliotek, to jest jeszcze gorzej – nie jesteśmy w stanie przecież zrobić lokalnych kopii wszystkich metod używanych wewnątrz tych bibliotek.

#### Problemy

Problemem jest przechowywanie danych poza zakresem funkcji. Z założenia dane wewnątrz funkcji mają być niedostępne z zewnątrz, więc w bardziej realistycznym scenariuszy skorzystanie z tego rozwiązania się komplikuje.

#### Podsumowanie

##### Zalety

- Dane są przechowywane tylko in-memory.
- Dane są zabezpieczone przed dostępem z poziomu wstrzykniętego złośliwego kodu.
- Mamy kontrolę nad wysyłaniem danych.

##### Wady

- Implementacja jest bardziej skomplikowana. Trzeba używać domknięcia, żeby zabezpieczyć dane.
- Trzeba korzystać z lokalnych kopii funkcji, żeby całkowicie zabezpieczyć token, co powoduje problemy ze skalowaniem i wykorzystaniem zewnętrznych bibliotek.
- Przechowywanie tokenów poza zakresem zamkniętej funkcji jest problematyczne.

### Web Workery

Web Workery pozwalają uruchomić kod JS w osobnym (odseparowanym od głównego) wątku. Z frontendem komunikują się specjalnym kanałem `MessageChannel`. Aplikacja może wysłać tym kanałem wiadomość – żądanie jakiejś akcji, którą Web Worker ma wykonać, po czym zwrócić dane do aplikacji.

W kontekście bezpieczeństwa istotne jest, że jakikolwiek kod, który chciałby mieć dostęp do tokena zapisanego w pamięci Web Workera musi istnieć w tym Web Workerze. Zewnętrzny kod nie ma do niej dostępu. Jednak trzeba pamiętać, że token **nie może być zwracany z Web Workera** do aplikacji, bo atakujący mógłby podstawić fałszywy `MessageChannel`i uzyskać dostęp do zwracanej wartości (podobnie, jak to było z fałszywym `fetch`).

Mimo, że atakujący nie ma dostępu do samego tokena, to mógłby wysłać do Web Workera polecenie np. wysłania jakiegoś żądania do backendu, więc mamy podatność na CSRF – podobnie, jak w przypadku ciasteczek. Jednak w przeciwieństwie do ciasteczek, zaufany kod JS ma dostęp do tokena, więc nie mamy już tego ograniczenia funkcjonalnego.

Poniżej mamy przykład kodu z wykorzystaniem Web Workera w NodeJS. W głównym wątku jest uruchamiana właściwa aplikacja frontendowa (`app.js`), a w osobnym wątku Web Worker (`api-worker.js`).

Cała logika z pobieraniem i wykorzystaniem tokena znajduje się w Web Workerze, odizolowana od głównego wątku aplikacji. Zakładając, że uda się atak XSS, tylko kod głównej aplikacji możemy uznać za niebezpieczny. Odizolowany proces Web Workera jest nadal czysty, więc przechowywany tam token jest bezpieczny.

**app.js**

```
const { Worker } = require('worker_threads');

const apiWorker = new Worker('./api-worker.js');

const callback = (data) => console.log(data)

apiWorker.on('message', messageFromWorker => callback(messageFromWorker));  

apiWorker.postMessage({ userId: 'user1'}); 
```

**api-worker.js**

```
const { parentPort } = require('worker_threads');

tokenCache = {}

const callFakeTokenService = function() {
    return { token: 'secretToken123' }
}

const callFakeApiService = function(token, userId) {
    if (token === 'secretToken123') {
        return { data: [1,2,3], user: userId }
    } else {
        return 'bad token'
    }
}

parentPort.once('message',
    message => 
    {
        let userId = message.userId

        let token = ''
        if (!tokenCache[userId]) {
            let tokenResponse = callFakeTokenService()
            token = tokenResponse.token
        } else {
            token = tokenCache[userId]
        }
        
        tokenCache[userId] = token

        let apiResponse = callFakeApiService(token, userId)

        return parentPort.postMessage(apiResponse);
    }
); 
```

#### Problemy

Problem pojawia się, jeśli potrzebujemy przechować token w pamięci, np. pomiędzy sesjami. Zwykły Web Worker z powyższego przykładu się nie sprawdzi, ponieważ będzie żył tylko do momentu zakończenia swojej pracy. Rozwiązaniem tego problemu jest zastosowanie [Shared Workera](https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker), do którego mamy dostęp z różnych kontekstów – różnych okien przeglądarki itp.. Jest to nieco bardziej skomplikowane, szczególnie jeśli używamy jakiegoś frameworka – np. Angulara. Jednak to również jest osobny temat, niezwiązany już z bezpieczeństwem.

Dodatkowo, z powodu opisanej wcześniej izolacji, Web Workera nie ma dostępu do ciasteczek, do których ma dostęp kod w głównym wątku. Może to być problemem na przykład w sytuacji, kiedy w Web Workerze chcemy pobrać access token, a żeby to zrobić musimy użyć refresh tokena, który jest w głównym wątku.

#### Podsumowanie

##### Zalety

- Dane istnieją tylko w obrębie odizolowanego procesu, w którym działa Web Worker – zabezpieczone przed złośliwym kodem, który infekuje aplikacje w głównym wątku.
- Mamy kontrolę nad wysyłaniem danych.
- Dane są zachowane między sesjami – do momentu aż przechowujący je Web Worker zostanie zatrzymany.

##### Wady

- Najbardziej skomplikowane z opisanych rozwiązań.
- Komplikuje się jeszcze bardziej, jeśli trzeba przechowywać token trwalej niż tylko chwilowo.
- Żądania wysyłane z kontekstu Web Workera nie mają dostępu do ciasteczek HttpOnly z głównego wątku.
- Możliwy jest atak CSRF.

## Podsumowanie

| **Rozwiązanie** | **XSS** | **XDS** | **CSRF** |
| --- | --- | --- | --- |
| Local Storage | Podatny | Podatny | Bezpieczny |
| Session Storage | Podatny | Bezpieczny | Bezpieczny |
| Ciasteczka HttpOnly | Bezpieczny | Bezpieczny | Podatny |
| In-memory* | Bezpieczny | Bezpieczny | Bezpieczny |
| Web Worker | Bezpieczny | Bezpieczny | Podatny |

*Pod warunkiem implementacji domknięcia i lokalnych kopii funkcji

Bezpieczeństwo pamięci przeglądarki to jedna sprawa, ale na bezpieczeństwo trzeba patrzeć szerzej. Wszystko, co tutaj opisałem jest możliwe dopiero, jeśli atakującemu uda się wykonać atak XSS/XDS. Więc dopóki mamy pewność, że aplikacja nie jest podatna na atak, to nawet w local storage token jest bezpieczny.

Inspiracją do tego tekstu były teksty na [blogu Auth0](https://auth0.com/blog/secure-browser-storage-the-facts/) i [ropnop blog](https://blog.ropnop.com/storing-tokens-in-browser/), które z jednej strony nieco odchudziłem, a z drugiej uzupełniłem o pewne brakujące tam informacje.

Inne ciekawe linki w tym temacie:

- https://pragmaticwebsecurity.com/articles/oauthoidc/localstorage-xss.html
- https://pragmaticwebsecurity.com/files/cheatsheets/browsersecrets.pdf
- przykład ataku XSS na LS https://medium.com/redteam/stealing-jwts-in-localstorage-via-xss-6048d91378a0

Ten tekst możecie też znaleźć [na OhMyDev](https://ohmydev.pl/post/bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki-icd)!

**Pozdrowienia z jasnej strony mocy!**
