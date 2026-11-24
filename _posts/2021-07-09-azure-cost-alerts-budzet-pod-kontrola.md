---
title: "Azure Cost Alerts – budżet pod kontrolą"
date: 2021-07-09
slug: "azure-cost-alerts-budzet-pod-kontrola"
permalink: /azure-cost-alerts-budzet-pod-kontrola/
categories: ["Azure"]
excerpt: "Jak upewnić się, że Twoje wydatki na usługi w Azure nie przekroczą założonego budżetu? Szczególnie gdy korzystasz z Azure do niekomercyjnych projektów i najlepiej, żeby było całkowicie za darmo?…"
image: "/assets/images/7552a937-AzureObrazekWyrozniajacy-1024x512.jpg"
layout: post
---

Jak upewnić się, że Twoje wydatki na usługi w Azure nie przekroczą założonego budżetu? Szczególnie gdy korzystasz z Azure do niekomercyjnych projektów i najlepiej, żeby było całkowicie za darmo? Dobrze ustawiony alarm (Cost Alert) w **Cost Management** może być rozwiązaniem tego problemu – powiadomi Cię, jeśli spodziewany będzie wydatek nawet 0,01 EUR.

## Przykład: Wszystko za darmo

Niestety Azure nie pozwala ustawić budżetu 0, więc musisz przeboleć wydatek 0,01 EUR.

![nosacz-co-tak-drogo](../assets/images/2d2c8e6c-nosacz.jpg)

W **Cost Management + Billing > Cost Management > Cost Alerts** dodaj nowy alert. Musisz ustawić:

- **Reset period** – okres rozliczeniowy, który może być miesięczny, kwartalny lub roczny. W tym przypadku im dłuższy, tym lepiej. Dlaczego? Bo chcemy się zbliżyć z poniesionymi kosztami do zera, więc 0,01 EUR na rok to mniej niż 0,01 EUR na miesiąc.
- **Creation date i Expiration Date** – tutaj spokojnie można ustawić ważność budżetu na kilka lat w przód – w razie potrzeby zawsze można go usunąć.
- **Budget Amount** – ustawiasz wysokość budżetu na dany okres rozliczeniowy. 0,01 EUR to najmniejsza kwota, jaką można ustawić.

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
