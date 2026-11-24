---
title: "Azure Cost Alerts – budżet pod kontrolą"
date: 2021-07-09
slug: "azure-cost-alerts-budzet-pod-kontrola"
permalink: /azure-cost-alerts-budzet-pod-kontrola/
categories: ["Azure"]
excerpt: "Azure Cost Management wysyła alerty o kosztach, ale budżet nie zatrzymuje naliczania opłat. Jak korzystać z progów i monitorować opóźnione dane?"
image: "/assets/images/7552a937-AzureObrazekWyrozniajacy-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  **Budżet ani alert nie blokują naliczania opłat.** Dane kosztowe są opóźnione, a budżety oceniane cyklicznie — nie jest to mechanizm gwarantujący „maksymalnie 0,01 EUR”. Poniższe zrzuty i ustawienia to przykład z 2021 r.; minimalna kwota i dostępne opcje zależą od bieżącego zakresu oraz API/portalu. Dodałem tę różnicę również do treści.

  Źródło: [Microsoft — tworzenie budżetów, opóźnienia i powiadomienia](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).
---

Jak monitorować wydatki na usługi w Azure i zmniejszyć ryzyko przekroczenia założonego budżetu? Szczególnie gdy korzystasz z Azure do niekomercyjnych projektów i najlepiej, żeby było całkowicie za darmo? Dobrze ustawiony alarm (Cost Alert) w **Cost Management** może pomóc, ale nie gwarantuje powiadomienia przed naliczeniem opłat.

Dane o kosztach są zwykle dostępne z opóźnieniem 8–24 godzin, budżety są oceniane co 24 godziny, a wysyłka powiadomienia również zajmuje czas. Prognoza nie musi być dostępna od razu. Zasoby nadal działają i naliczają koszty po przekroczeniu progu. Twardy limit wydatków, tam gdzie dany typ subskrypcji w ogóle go oferuje, jest osobnym mechanizmem; automatyczne wyłączanie zasobów także wymaga osobnej konfiguracji.

## Przykład: Wszystko za darmo

W konfiguracji przedstawionej na historycznych zrzutach nie dało się ustawić budżetu 0, więc użyłem progu 0,01 EUR. To próg powiadomienia, nie maksymalna opłata ani obietnica, że zapłacisz właśnie tyle.

![nosacz-co-tak-drogo](../assets/images/2d2c8e6c-nosacz.jpg)

W **Cost Management + Billing > Cost Management > Cost Alerts** dodaj nowy alert. Musisz ustawić:

- **Reset period** – okres rozliczeniowy, który może być miesięczny, kwartalny lub roczny. Dobierz go do sposobu kontroli kosztów; dłuższy okres sam w sobie nie zmniejsza faktury. Sprawdź też, jak dla danego zakresu oceniane są budżety kwartalne i roczne.
- **Creation date i Expiration Date** – tutaj spokojnie można ustawić ważność budżetu na kilka lat w przód – w razie potrzeby zawsze można go usunąć.
- **Budget Amount** – ustawiasz wysokość budżetu na dany okres rozliczeniowy. Na zrzutach użyłem 0,01 EUR; sprawdź aktualną walidację kwoty w swoim portalu i zakresie rozliczeń.

![cost-management-step-1](../assets/images/99ce6882-TworzenieAlertu1-1024x476.jpg)

Po ustawieniu nazwy i budżetu przechodzisz do następnego kroku – **Set alerts**. Tu po pierwsze ustawiasz warunek (jeśli przewidywany koszt przekroczy 100% budżetu), a po drugie podajesz adres e-mail, na który ma przyjść powiadomienie, w razie gdyby Twój budżet miał być przekroczony.

![cost-management-step-2](../assets/images/d0ce9fbe-TworzenieAlertu2-1024x491.jpg)

Klikasz **Create** i gotowe.

Pod **Cost alerts** jest zakładka **Budgets**, gdzie możesz przejrzeć i edytować utworzone budżety.

![cost-management-step-3](../assets/images/f49c0b42-StworzonyBudzet-1024x213.jpg)

## Jak ograniczyć koszty?

Wiemy już, jak skorzystać z budżetu w przypadku, gdy nie chcemy płacić nic. A co w przypadku, kiedy mamy założony budżet, ale okazuje się, że zasoby na Azure kosztują nas za dużo? Gdzie szukać oszczędności?

Wspomnę o kilku kwestiach, którym warto się przyjrzeć w tym kontekście:

- Czy zasoby, o których myślisz, że są darmowe, naprawdę takie są? Czy przy planowaniu budżetu szacujesz koszty dokładnie, używając np. [Azure Pricing Calculator](../azure-pricing-calculator/)?
- Czy wszystkie dane (za których przechowywanie płacisz od wielkości) są potrzebne? Czy nie masz starych, zapomnianych backupów, logów sprzed lat i innych resztek?
- Czy stosujesz skalowanie (planowane lub automatyczne, [pionowe](../automatyzacja-skalowania-azure/) lub poziome) tam, gdzie jest to możliwe?

Jeśli na którekolwiek z powyższych pytań odpowiedziałeś „Nie”, to zajrzyj do [pozostałych wpisów o Azure](../category/azure/) – mogą Ci w tych tematach pomóc!
