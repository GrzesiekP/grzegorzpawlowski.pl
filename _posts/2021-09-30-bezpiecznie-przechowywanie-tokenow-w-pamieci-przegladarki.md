---
title: "Bezpieczne przechowywanie tokenów w pamięci przeglądarki"
date: 2021-09-30
slug: "bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki"
permalink: /bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki/
categories: ["Bezpieczeństwo"]
excerpt: "Jest kilka rodzajów pamięci przeglądarki, w których można przechowywać wrażliwe dane, jak np. tokeny. Różnią się one między innymi funkcjonalnością, stopniem izolacji i możliwościami zabezpieczenia…"
image: "/assets/images/60233684-sejf.jpeg"
layout: post
updated: 2026-11-24
update_note: |
  Poprawiłem istotne błędy: `sessionStorage` nie chroni przed XSS w tej samej karcie, `HttpOnly` blokuje odczyt ciasteczka, ale nie działania w imieniu użytkownika, a domknięcie nie jest pełną ochroną przed XSS. Przykład Node.js zastąpiłem przeglądarkowym Web Workerem. Nie ma uniwersalnego „bezpiecznego magazynu”, który naprawi aplikację wykonującą złośliwy kod.

  Źródła: [OWASP — HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html), [MDN — sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage), [Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie), [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers).
---

Jest kilka rodzajów pamięci przeglądarki, w których można przechowywać wrażliwe dane, jak np. tokeny. Różnią się one między innymi funkcjonalnością, stopniem izolacji i możliwościami zabezpieczenia przed atakami. Które rozwiązanie jest najbezpieczniejsze?

## Rodzaje zagrożeń

Żeby mówić o bezpieczeństwie, spójrzmy najpierw na zagrożenie, przed którym mamy się bronić. W przypadku kodu na front-endzie, weźmy na warsztat następujące rodzaje ataków.

### XSS – Cross-Site Scripting

XSS polega na uruchomieniu w kontekście aplikacji złośliwego kodu, np. JavaScriptu odczytującego token. Może do tego dojść przez niebezpieczne wstawienie niezaufanych danych do HTML-a. Jeśli aplikacja pozwoli na atrybuty zdarzeń, ilustracją problemu jest `<img src="x" onerror="alert('Hacked!')">`. Sam adres obrazka nie staje się automatycznie kodem — istotny jest sposób jego użycia i sanitizacji.

### XDS – Cross-Directory Scripting

Pod tą nazwą opisuję problem aplikacji współdzielących origin, choć powinny być odizolowane. Przykład: `https://example.com/safeapp` i `https://example.com/notsafeapp`. Różne ścieżki nie tworzą różnych originów. Skrypt z jednej takiej aplikacji może mieć dostęp do wspólnego magazynu drugiej. Osobne domeny z poprzedniej wersji przykładu były błędem.

### CSRF – Cross-Site Request Forgery

CSRF to wymuszenie niepożądanego żądania z innej witryny, gdy przeglądarka dołącza poświadczenia, np. ciasteczko sesji. Nie wymaga XSS. Z kolei XSS w samej aplikacji może wykonywać uwierzytelnione żądania nawet bez odczytu tokena i często obchodzi zabezpieczenia CSRF. To dwa różne zagrożenia.

## CORS Policy i Same Origin Policy

Zanim przejdziemy do omawiania sposobów przechowywania i ich bezpieczeństwa, wyjaśnię jeszcze dwie kwestie: co to jest polityka CORS i Origin.

**Origin** to zestaw **protokół, host, port**. Jeśli zmieni się któraś ze składowych, zmieni się origin. Zobaczmy na przykładzie adresu, który warto znać, jak w górach spadnie śnieg: [https://kaukazwypozyczalnia.pl:443/cennik](https://kaukazwypozyczalnia.pl/cennik/)

| **URL** | **Różnica** | **Powód** |
| --- | --- | --- |
| `https://kaukazwypozyczalnia.pl:8080/cennik` | Inny Origin | Inny port |
| `http://kaukazwypozyczalnia.pl:443/cennik` | Inny Origin | Inny protokół |
| `https://kaukazwypozyczalnia.pl:443/kontakt` | Ten sam Origin | Zmiana ścieżki |
| `https://kaukazwypozyczalnia.net:443/cennik` | Inny Origin | Inna domena (host) |
| `https://kaukazwypozyczalnia.pl/cennik` | Ten sam Origin | Port niesprecyzowany |

**CORS** (Cross-Origin Resource Sharing) – współdzielenie zasobów pomiędzy originami. Polityka CORS określa, czy i na jakich zasadach może się to odbywać.

**Same Origin Policy** ogranicza przede wszystkim odczyt danych i interakcje między originami. Nie zakazuje każdego wysłania żądania cross-origin. CORS pozwala serwerowi kontrolować udostępnianie odpowiedzi skryptom innych originów; nie zastępuje uwierzytelnienia ani ochrony CSRF.

Jak Same Origin Policy ogranicza odczyt danych z obcej witryny? Rozpatrzmy scenariusz (to jeszcze nie XSS w aplikacji giełdy):

1. Użytkownik jest zalogowany np. do konta na giełdzie kryptowalut (np. BitBay – [archiwalna strona giełdy](https://web.archive.org/web/20210812222443/https://bitbay.net/pl)), więc przeglądarka przechowuje jakiś token dostępu.
2. Odwiedza złośliwą stronę `https://bezpiecznydarmowydogecoin.com`
3. Kod JS ze złośliwej strony chce wysłać żądanie do API giełdy (np. przelać wszystkie BTC ofiary na portfel atakującego), do czego potrzebuje tokena. A tu psikus! Origin `https://bezpiecznydarmowydogecoin.com`, z którego pochodzi złośliwy kod, i origin `https://bitbay.net` są różne, więc kod ze złośliwej strony nie będzie miał dostępu do danych pochodzących z origina `https://bitbay.net`.

*Jeśli trzymasz kryptowaluty na giełdzie, to przeczytaj np. [tutaj](../kryptowaluty-9-bledow-poczatkujacych/), dlaczego to nie jest bezpieczny pomysł.*

## Sposoby przechowywania

### Pamięć lokalna – Local Storage

Local Storage oferuje izolację przez Same Origin Policy, co oznacza (jak powyżej wyjaśniłem), że kod JS z origina A nie ma dostępu do zasobów w pamięci lokalnej pochodzących z origina B.

Dane są w tym przypadku przechowywane niezależnie od sesji, więc jeśli użytkownik zamknie okno lub kartę, a później otworzy ją ponownie, nadal będzie miał dostęp do danych z pamięci lokalnej.

Ataki XSS są możliwe, kiedy dane w pamięci pochodzą z tego samego origina. Przykład klasycznego XSS: użytkownik A wstrzykuje kod JS przez podatną aplikację (np. jako URL do obrazka), który uruchamia się u użytkownika B. Ten oczekiwał, że aplikacja jest bezpieczna i w kodzie JS przyjdzie tylko adres URL obrazka. Złośliwy kod ma dostęp do danych z pamięci lokalnej.

Pamięć lokalna jest także podatna na ataki XDS, opisane na początku.

Token z pamięci lokalnej nie jest automatycznie dołączany do żądań. W typowym API z nagłówkiem `Authorization` ogranicza to klasyczny CSRF, o ile serwer nie akceptuje równocześnie automatycznie dołączanych poświadczeń inną drogą. Nie chroni przed XSS ani błędami CORS i autoryzacji.

#### Podsumowanie

##### Zalety

- Izolacja per origin.
- Token nie jest automatycznie dołączany do żądań — ogranicza klasyczny CSRF w odpowiednio zaprojektowanym API.
- Dane są zachowywane pomiędzy sesjami – jest do nich dostęp z innych kart, okien czy po przeładowaniu strony.

##### Wady

- Dane są łatwo dostępne dla ataku XSS.

### Pamięć sesji – Session Storage

Ta opcja jest dzielona według origina **i karty najwyższego poziomu**. Dane przetrwają przeładowanie oraz nawigację w tej samej karcie; nie są po prostu kasowane przy otwarciu kolejnego linku. Iframe tego samego origina w tej karcie korzysta z tego samego magazynu. Rozważmy przykład:

1. Aplikacja zapisuje token w `sessionStorage`.
2. Podatna strona tej aplikacji uruchamia złośliwy skrypt w tej samej karcie i originie.
3. Skrypt może odczytać token — izolacja między kartami nie zapobiega temu XSS.
4. Osobna karta zwykle ma własny magazyn, ale nowa strona z `opener` może początkowo dostać kopię magazynu otwierającej strony. Nie jest to niezawodna granica ochrony tokena.

Różne ścieżki tego samego origina w jednej karcie nie są odizolowane przez `sessionStorage`. Ten magazyn nie rozwiązuje opisanego problemu XDS.

#### Podsumowanie

##### Zalety

- Izolacja per origin.
- Token nie jest automatycznie dołączany do żądań, podobnie jak w `localStorage`.
- Krótszy czas przechowywania i rozdzielenie kart ograniczają ekspozycję, ale nie eliminują XSS.

##### Wady

- Dane nadal dostępne dla ataku XSS w obrębie sesji.

### Ciasteczka

W przypadku ciasteczek, zabezpieczenie zależy od ustawionych flag, a konkretnie od `HttpOnly`.

Jeśli flaga `HttpOnly` jest włączona, ciasteczko jest niedostępne dla kodu JS, więc token w nim przechowywany jest zabezpieczony przed dostępem ze złośliwego kodu z ataku XSS. Jednocześnie jednak JS aplikacji frontendowej również nie ma dostępu do tokena, więc w przypadku niektórych aplikacji po prostu nie możemy z tego rozwiązania skorzystać ze względów funkcjonalnych. Biorąc jednak pod uwagę, że tokenów zazwyczaj używamy, żeby uwierzytelnić się w jakimś API, to ograniczenie jest raczej rzadkie.

`HttpOnly` uniemożliwia odczyt ciasteczka przez JavaScript, ale przeglądarka nadal może dołączyć je do żądania wykonanego przez złośliwy skrypt. To użycie sesji bez poznania tokena, a nie obejście `HttpOnly`. Dla sesji stosuj też HTTPS, flagę `Secure`, odpowiednie `SameSite` oraz serwerową ochronę CSRF tam, gdzie jest potrzebna. Ścieżka `Path` ciasteczka nie jest granicą bezpieczeństwa między aplikacjami.

Ciasteczka powinny mieć zawsze `HttpOnly:true`, jeśli zawierają wrażliwe dane. W innym przypadku można je wyciągnąć w prosty sposób:

```
document.cookie
   .split('; ')
    .find(r => r.startsWith('secretAccessToken='))
    ?.slice('secretAccessToken='.length)
```

Nawet nie znając klucza, pod jakim zapisany jest token, można po prostu pobrać wszystkie ciasteczka i poszukać, czy jest w nich coś przydatnego do ataku.

#### Podsumowanie

##### Zalety

- Z włączoną flagą `HttpOnly` żaden kod JS, w tym złośliwy, nie ma dostępu do ciasteczka.

##### Wady

- Rozwiązanie jest podatne na CSRF.
- Zaufany kod frontendowy też nie ma dostępu do danych w ciasteczkach.

### In-Memory

Pamięć procesu strony ogranicza trwałość tokena, ale nie jest automatycznie najbezpieczniejsza. Domknięcie ogranicza bezpośredni dostęp do zmiennej, nie odbiera jednak złośliwemu skryptowi możliwości działania w kontekście aplikacji.

**Rozważmy następujące przykłady**

Załóżmy, że w HTML jest pole `secretInput`, gdzie przesyłamy sekret, oraz metoda, która zapisuje go w pamięci (in-memory).

#### Przykład 1 – globalna zmienna

```
let secret;
function saveSecret() {
   secret = document.getElementById('secretInput').value;
}
```

Tutaj nie ma praktycznie żadnego zabezpieczenia. Zmienna `secret` jest globalnie dostępna dla złośliwego kodu. Jak można przechować sekret, żeby nie był tak wystawiony?

#### Przykład 2 – stała

```
const globalData = {};
function saveSecret() {
   const secret = document.getElementById('secretInput').value;
   globalData['secret'] = secret
}
```

Deklaracja `const` wewnątrz funkcji ogranicza zasięg wiązania do jej bloku. Samo `const` nie jest mechanizmem ochrony sekretów i nie czyni obiektów niemutowalnymi.

Problem może się pojawić, kiedy później wartość `secret` zostanie przypisana do innej zmiennej, która jest widoczna dla złośliwego kodu, jak w tym przypadku do `globalData`.

#### Przykład 3 – domknięcie (closure)

Obejściem powyższego problemu jest domknięcie funkcji (w celu emulacji metody prywatnej). W tym przykładzie wewnątrz funkcji `fetchToken` token jest pobierany z serwera i zapisywany do lokalnej zmiennej. Natomiast `fetchToken` jest zamknięta w zewnętrznej funkcji, dzięki czemu zmienne z `fetchToken` nie są dostępne poza zewnętrzną metodą.

```
let token = (function() {
  async function fetchToken() {
    let fetchedToken;
     const request = new Request("/token");
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

Ten fragment pokazuje tylko zasięg zmiennej: `fetchedToken` nie jest zwracany ani zachowywany do kolejnych wywołań, więc nie stanowi jeszcze użytecznego magazynu tokenów. Ujawnienie tokena przez publiczną metodę zniweczyłoby izolację. Co więcej, złośliwy kod może podmienić współdzielone funkcje, np. `fetch`. W poniższym demonstracyjnym interceptorze używam `clone()`, aby nie zużyć strumienia odpowiedzi przed aplikacją:

```
let fetch = window.fetch;
window.fetch = async function() { 
  let fetchPromise = fetch.apply(this, arguments);
  let resp = await fetchPromise;
   let json = await resp.clone().json();
  alert(JSON.stringify(json));
  return fetchPromise
};
```

W powyższym przykładzie podstawiony fałszywy `fetch` woła prawdziwą metodę `fetch`, przechwytuje zwracany z niej wynik, a następnie zwraca go, jak gdyby robiła to oryginalna metoda.

Można ograniczyć tę konkretną podmianę, ale nie naprawia to całego problemu XSS.

#### Przykład 4 – domknięcie + lokalna kopia podatnej metody

Tutaj zachowujemy referencję do bieżącego `window.fetch`. Pomaga to tylko wtedy, gdy zaufany kod wykona się przed jego podmianą; nie daje pewności, że przechwycona funkcja jest natywna.

```
let token = (function() {
  let localFetch = window.fetch;
  async function localFetchToken() {
    let fetchedToken ;
     const request = new Request("/token");
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

Późniejsza podmiana `window.fetch` nie zmieni zachowanej referencji. Inne punkty zaczepienia oraz możliwość wykonywania operacji przez XSS pozostają. Także ten fragment tylko pobiera i odrzuca dane, zamiast implementować pełną obsługę sesji.

Niestety, to rozwiązanie też nie jest idealne. Im więcej zewnętrznie zdefiniowanych funkcji używamy w naszej zamkniętej metodzie, tym więcej lokalnych kopii trzeba zrobić. To się po prostu źle skaluje. Jeśli do tego dodać, że możemy używać zewnętrznych bibliotek, to jest jeszcze gorzej – nie jesteśmy w stanie przecież zrobić lokalnych kopii wszystkich metod używanych wewnątrz tych bibliotek.

#### Problemy

Problemem jest przechowywanie danych poza zakresem funkcji. Z założenia dane wewnątrz funkcji mają być niedostępne z zewnątrz, więc w bardziej realistycznym scenariuszu skorzystanie z tego rozwiązania się komplikuje.

#### Podsumowanie

##### Zalety

- Dane są przechowywane tylko in-memory.
- Domknięcie utrudnia bezpośredni odczyt lokalnej zmiennej, nie gwarantuje odporności na XSS.
- Mamy kontrolę nad wysyłaniem danych.

##### Wady

- Implementacja jest bardziej skomplikowana. Trzeba używać domknięcia, żeby zabezpieczyć dane.
- Zachowanie referencji do funkcji ogranicza niektóre podmiany, lecz nie zapewnia pełnej ochrony tokena i sesji.
- Przechowywanie tokenów poza zakresem zamkniętej funkcji jest problematyczne.

### Web Workery

Web Workery uruchamiają JavaScript poza głównym wątkiem, we własnym kontekście globalnym. Komunikacja odbywa się przez `postMessage` i zdarzenia `message`; można też używać `MessageChannel`. To nie jest obietnica osobnego procesu systemowego.

W kontekście bezpieczeństwa istotne jest, że jakikolwiek kod, który chciałby mieć dostęp do tokena zapisanego w pamięci Web Workera, musi istnieć w tym Web Workerze. Zewnętrzny kod nie ma do niej dostępu. Jednak trzeba pamiętać, że token **nie może być zwracany z Web Workera** do aplikacji, bo atakujący mógłby podstawić fałszywy `MessageChannel` i uzyskać dostęp do zwracanej wartości (podobnie jak to było z fałszywym `fetch`).

XSS może wysyłać do workera takie same polecenia jak aplikacja. Trzeba więc ograniczyć interfejs komunikatów i uprawnienia; to nadużycie interfejsu przez XSS, nie klasyczny CSRF. Jeśli worker ma chronić token przed głównym wątkiem, nie powinien go temu wątkowi zwracać.

Poniżej przeglądarkowy przykład z atrapą tokena i API, bez żądań sieciowych. Uruchom pliki z tego samego origina przez HTTP(S). `worker_threads` z Node.js z pierwotnej wersji wpisu nie jest API Web Workerów w przeglądarce.

Sekret pozostaje w workerze, ale XSS nadal może poprosić go o dozwolone dane. Walidacja typu komunikatu nie rozpoznaje, czy wysłał go zaufany kod czy skrypt atakującego. Uwierzytelnienie i autoryzacja danych użytkownika muszą być egzekwowane przez prawdziwy backend.

**app.js**

```
const apiWorker = new Worker('./api-worker.js');
apiWorker.addEventListener('message', event => console.log(event.data));
apiWorker.postMessage({ type: 'GET_MY_DATA' });
```

**api-worker.js**

```
const token = 'DEMO_ONLY_NOT_A_REAL_SECRET';
function callFakeApiService(accessToken) {
    if (accessToken !== token) throw new Error('Bad token');
    return { data: [1, 2, 3] };
}
self.addEventListener('message', event => {
    const message = event.data;
    if (!message || message.type !== 'GET_MY_DATA' ||
        Object.keys(message).length !== 1) {
        self.postMessage({ error: 'Unsupported message' });
        return;
    }
    self.postMessage(callFakeApiService(token));
});
```

#### Problemy

Worker nie jest trwałym magazynem. Dedicated Worker jest związany ze swoim dokumentem; [SharedWorker](https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker) może obsługiwać kilka zgodnych kontekstów, np. kart, ale nie gwarantuje przetrwania zamknięcia przeglądarki czy kolejnej sesji. Nie buduj odzyskiwania sesji na założeniu, że proces workera będzie stale żył.

Worker nie ma `document.cookie`, ale jego `fetch` może wysyłać ciasteczka, także `HttpOnly`, zgodnie z regułami `credentials`, originów i `SameSite`. Odczyt wartości ciasteczka i dołączenie go przez przeglądarkę do żądania to różne rzeczy. Refresh tokena w ciasteczku `HttpOnly` nie odczyta ani główny wątek, ani worker.

#### Podsumowanie

##### Zalety

- Oddzielny kontekst JavaScriptu ogranicza bezpośredni odczyt danych przez główny wątek.
- Mamy kontrolę nad wysyłaniem danych.
- SharedWorker może współdzielić stan między kartami, ale nie jest trwałym magazynem między sesjami.

##### Wady

- Najbardziej skomplikowane z opisanych rozwiązań.
- Komplikuje się jeszcze bardziej, jeśli trzeba przechowywać token trwalej niż tylko chwilowo.
- XSS może nadużyć dozwolonych operacji workera; sam oddzielny wątek nie chroni sesji.
- Przy uwierzytelnianiu ciasteczkami nadal trzeba uwzględnić ochronę CSRF.

## Podsumowanie

| **Rozwiązanie** | **Bezpośredni odczyt przez XSS** | **Działania w imieniu ofiary przez XSS** | **Automatyczne dołączanie poświadczeń** |
| --- | --- | --- | --- |
| Local Storage | Tak | Możliwe | Nie |
| Session Storage | Tak, w tej samej karcie/originie | Możliwe | Nie |
| Ciasteczko HttpOnly | Nie przez JS | Możliwe | Tak, zależnie od reguł ciasteczek |
| Domknięcie in-memory | Utrudniony; zależy od interfejsu i implementacji | Możliwe | Nie |
| Web Worker | Nie bezpośrednio z głównego wątku | Możliwe przez interfejs workera | Zależy od sposobu uwierzytelniania |

To nie ranking odporności na każdy atak. Ścieżki jednego origina nie są odrębnymi strefami zaufania. Dla aplikacji z backendem warto rozważyć sesję w ciasteczku `HttpOnly; Secure` z odpowiednim `SameSite` i ochroną CSRF, zamiast udostępniać tokeny JavaScriptowi. Szczegóły zależą od architektury.

Każdy wariant wymaga zapobiegania XSS: bezpiecznych operacji na DOM, kodowania danych w odpowiednim kontekście, sanitizacji dopuszczanego HTML-a, kontroli zależności i CSP jako dodatkowej warstwy. Nie zakładaj, że „na pewno nie mamy XSS”, więc miejsce przechowywania sekretów przestaje mieć znaczenie.

Inspiracją do tego tekstu były teksty na [blogu Auth0](https://auth0.com/blog/secure-browser-storage-the-facts/) i [ropnop blog](https://blog.ropnop.com/storing-tokens-in-browser/), które z jednej strony nieco odchudziłem, a z drugiej uzupełniłem o pewne brakujące tam informacje.

Inne ciekawe linki w tym temacie:

- https://pragmaticwebsecurity.com/articles/oauthoidc/localstorage-xss.html
- https://pragmaticwebsecurity.com/files/cheatsheets/browsersecrets.pdf
- przykład ataku XSS na LS https://medium.com/redteam/stealing-jwts-in-localstorage-via-xss-6048d91378a0

Ten tekst był również opublikowany na OhMyDev (dawny adres: `https://ohmydev.pl/post/bezpiecznie-przechowywanie-tokenow-w-pamieci-przegladarki-icd`; serwis jest obecnie niedostępny).

**Pozdrowienia z jasnej strony mocy!**
