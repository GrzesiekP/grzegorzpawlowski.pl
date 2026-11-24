---
title: "Automatyzacja skalowania w pionie"
date: 2021-05-15
slug: "automatyzacja-skalowania-azure"
permalink: /automatyzacja-skalowania-azure/
categories: ["Azure"]
excerpt: "Azure pozwala na skalowanie horyzontalne (scale-in/scale-out, czyli zmianę liczby) lub wertykalne (scale-down/scale-up tier, czyli zmianę poziomu) instancji usług (np. App Service Plan).…"
image: "/assets/images/7552a937-AzureObrazekWyrozniajacy-1024x512.jpg"
layout: post
updated: 2026-11-24
update_note: |
  Konta Run As wycofano 30.09.2023 r., a AzureRM nie jest już wspieranym modułem do nowych wdrożeń. Przykład zaktualizowałem do modułów Az i Managed Identity, z jawnym wyborem subskrypcji i domyślnym trybem bez zmiany zasobów. Uprościłem go do skalowania S1 → S2 → S3, żeby nie sugerować uniwersalnej kolejności wszystkich SKU. Skalowanie wymaga testów dostępności i limitów kosztu.

  Źródła: [migracja Run As](https://learn.microsoft.com/en-us/azure/automation/migrate-run-as-accounts-managed-identity), [Managed Identity w Automation](https://learn.microsoft.com/en-us/azure/automation/enable-managed-identity-for-automation), [Set-AzAppServicePlan](https://learn.microsoft.com/en-us/powershell/module/az.websites/set-azappserviceplan).
---

Azure oferuje skalowanie horyzontalne (*scale-in/scale-out*, czyli zmianę liczby instancji) i wertykalne (*scale-down/scale-up*, czyli zmianę rozmiaru lub poziomu usługi). Dostępne mechanizmy automatyzacji zależą od konkretnej usługi i planu — nie można powiedzieć, że w całym Azure automatyzacja działa tylko poziomo. Ten przykład dotyczy zmiany SKU **App Service Planu** przez runbook i alert, a nie automatycznego skalowania dowolnej usługi.

## Przykład: Automatyzacja skalowania App Service Planu

W skrócie, Runbook uruchamia skrypt PowerShell, który zmienia tier App Service Planu. Runbook można uruchomić za pomocą webhooka lub określić interwał czasowy. Jeśli skalowanie ma być reakcją na wzrost lub spadek użycia zasobów (CPU/RAM) App Service Planu, można wykorzystać alert. Będzie on, monitorując metryki zużycia CPU i pamięci, wywoływał Runbook, gdy osiągną odpowiedni poziom.

### Instrukcja

#### Runbook

1. Stwórz Automation Account i włącz jego systemową Managed Identity.
2. Nadaj tej tożsamości uprawnienia do odczytu i zmiany **konkretnego** App Service Planu, zamiast uprawnień administratora całej subskrypcji.
3. W środowisku wykonawczym runbooka udostępnij zgodne wersje `Az.Accounts` i `Az.Websites` oraz wybierz wspierany runtime PowerShell.
4. Utwórz runbook PowerShell. Poniższy przykład obsługuje wyłącznie rodzinę Standard: S1, S2 i S3. Sprawdź dostępność i cenę tych SKU dla własnego systemu operacyjnego, regionu i planu.
5. Zapisz i opublikuj. Najpierw uruchom go **bez** `Apply`: zaloguje się, odczyta plan i wypisze proponowaną zmianę, ale jej nie wykona.
6. Dopiero po testach na środowisku nieprodukcyjnym świadomie ustaw `Apply`. Zmiana może zwiększyć rachunek i wpłynąć na wszystkie aplikacje współdzielące plan.

```powershell
param (
    [Parameter(Mandatory = $true)]
    [string] $SubscriptionId,
    [Parameter(Mandatory = $true)]
    [string] $ResourceGroupName,
    [Parameter(Mandatory = $true)]
    [string] $AppServicePlanName,
    [ValidateSet('S1', 'S2', 'S3')]
    [string] $MaxAllowedSku = 'S3',
    [switch] $Apply
)

$ErrorActionPreference = 'Stop'
Disable-AzContextAutosave -Scope Process | Out-Null
$context = (Connect-AzAccount -Identity).Context
$context = Set-AzContext -SubscriptionId $SubscriptionId -DefaultProfile $context
$plan = Get-AzAppServicePlan -ResourceGroupName $ResourceGroupName `
    -Name $AppServicePlanName -DefaultProfile $context

$steps = @('S1', 'S2', 'S3')
$currentIndex = [Array]::IndexOf($steps, $plan.Sku.Name)
$maxIndex = [Array]::IndexOf($steps, $MaxAllowedSku)
if ($currentIndex -lt 0) {
    throw 'This example only supports Standard S1/S2/S3 plans.'
}
if ($currentIndex -ge $maxIndex) {
    Write-Output 'At or above the configured limit; no change.'
    return
}

$nextSku = $steps[$currentIndex + 1]
$sizes = @{ S1 = 'Small'; S2 = 'Medium'; S3 = 'Large' }
Write-Output ("Proposed change: {0} -> {1}" -f $plan.Sku.Name, $nextSku)
if (-not $Apply) {
    Write-Output 'Preview only. Set Apply explicitly to change the plan.'
    return
}

Set-AzAppServicePlan -ResourceGroupName $ResourceGroupName `
    -Name $AppServicePlanName -Tier 'Standard' -WorkerSize $sizes[$nextSku] `
    -NumberofWorkers $plan.NumberOfWorkers -DefaultProfile $context
```

To przykład dydaktyczny, nie gotowy kontroler autoskalowania. Nie obsługuje równoległych uruchomień, histerezy ani skalowania w dół. Ustaw ograniczenia częstotliwości i przetestuj scenariusze błędów, zanim powiążesz go z alertem. [Dawne repozytorium VerticalScaleUp](https://github.com/GrzesiekP/VerticalScaleUp) zawiera historyczny kod AzureRM, nie powyższy wariant Az.

#### Alerting

1. Przejdź do Alertów Azure i dodaj „New alert rule”
2. W Scope wybierz Twój App Service Plan.
3. W Condition skonfiguruj warunek, po spełnieniu którego ma się wywołać akcja skalowania. Np. kiedy średnie zużycie pamięci przekroczy 75%.
4. W Actions stwórz nową grupę. Jako Action type wybierz Automation Runbook, a następnie wskaż stworzony Runbook. Skonfiguruj wymagane parametry i przetestuj sposób przekazania danych alertu; payload webhooka nie jest automatycznie dowolnym zestawem parametrów skryptu. Nie włączaj `Apply`, dopóki nie sprawdzisz zachowania automatyzacji.
5. Kliknij Review + create i gotowe!

Automatyzacja skalowania to jedno. Osobną kwestią jest dobre skonfigurowanie, kiedy ASP powinien się skalować. To już kwestia indywidualna, która zależy od sposobu, w jaki jest używany. Jeśli hostujesz na nim API dla sklepu internetowego, z którego korzystają użytkownicy jednej strefy czasowej, to możliwe, że wykres użycia będzie wyglądał całkiem regularnie i można skalować np. o konkretnej godzinie, bez monitorowania metryk i ustawiania alertów. Ale kiedy zmienność zużycia jest mniej przewidywalna, trzeba mądrze dobrać poziomy, na których ma się skalować. Nieźle opisuje to [Dokumentacja Microsoftu](https://docs.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-best-practices#manual-scaling-is-reset-by-autoscale-min-and-max).

## Warto wiedzieć

Czasami w skryptach z *Runbooks gallery* pojawiają się problemy z kodowaniem, przez co w kodzie skryptu znajdują się niepożądane znaki specjalne. Warto przejrzeć kod przed użyciem.

Upewnij się, że Runbook ma uprawnienia do modyfikowania App Service Planu.

Zmiana rozmiaru planu może wiązać się z przenoszeniem obciążeń i restartami. Nie zakładaj stałego, kilkusekundowego czasu niedostępności: zależy on od usługi, liczby instancji, aplikacji i sposobu wdrożenia. Wynik pojedynczego testu nie jest SLA. Przed zmianą produkcji przetestuj dostępność, zachowanie długich żądań, gotowość instancji i scenariusz powrotu do poprzedniego SKU. Skalowanie baz SQL ma własne zasady i nie należy utożsamiać go ze skalowaniem App Service.

Jeśli zastanawiasz się nad kosztami, jakie realnie generują poszczególne poziomy App Service Planów, zobacz [mój wpis o Azure Pricing Calculator](../azure-pricing-calculator/).
