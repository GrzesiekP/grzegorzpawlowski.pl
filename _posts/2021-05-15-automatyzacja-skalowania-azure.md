---
title: "Automatyzacja Skalowania w Pionie"
date: 2021-05-15
slug: "automatyzacja-skalowania-azure"
permalink: /automatyzacja-skalowania-azure/
categories: ["Azure"]
excerpt: "Azure pozwala na skalowanie horyzontalne ( scale-in/scale-out , czyli zmiana ilości) lub wertykalne ( scale-down/scale-up tier , czyli zmiana poziomu) instancji usług (np. App Service Plan ).…"
image: "/assets/images/7552a937-AzureObrazekWyrozniajacy-1024x512.jpg"
layout: post
---

Azure pozwala na skalowanie horyzontalne (*scale-in/scale-out*, czyli zmiana ilości) lub wertykalne (*scale-down/scale-up tier*, czyli zmiana poziomu) instancji usług (np. *App Service Plan*). Automatyzacja skalowania jest domyślnie możliwa tylko horyzontalnie. Jeżeli z jakiegoś powodu potrzebujesz automatyzacji skalowania wertykalnego, można to zrobić za pomocą *Runbooka *i *Alertów*.

## Przykład: Automatyzacja skalowanie App Service Planu

W skrócie, Runbook uruchamia skrpyt PowetShell, który zmienia tier App Service Planu. Runbook można uruchomić za pomocą webhooka lub określić interwał czasowy. Jeśli skalowanie ma być reakcją za wzrost lub spadek użycia zasobów (CPU/RAM) App Service Planu, można wykorzystać Alert. Będzie on, monitorując metryki zużycia CPU i pamięci, wywoływał Runbook, gdy osiągną odpowiedni poziom.

### Instrukcja

#### Runbook

1. Stwórz Automation Account ( *Create Azure Run As account* na tak)
2. Zaimportuj odpowiednie moduły: Automation account -> shared resources -> modules -> browse. Wybierz AzureRM.Profile i AzureRM.Websites.
3. W utworzonym koncie przejdź do Runbooks i stwórz nowy Runbook. Możesz użyć też gotowych, klikając *Browse gallery* i znajdując skrypt, który spełnia Twoje wymagania. Ja w tym przykładzie sam napisałem [krótki i prosty skrypt](https://raw.githubusercontent.com/GrzesiekP/VerticalScaleUp/master/VerticalScaleUp.ps1) . Możecie go znaleźć w Galerii pod nazwą VerticalScaleUp i [na GitHubie](https://github.com/GrzesiekP/VerticalScaleUp) .
4. Wybierz typ PowerShell
5. Kliknij Edit i napisz kod, który skaluje App Service Plan
6. Zapisz i opublikuj. Runbook można przetestować, klikając „Start”.

```
Param
(
  [Parameter (Mandatory= $true)]
  [String] $resourceGroupName = "",

  [Parameter (Mandatory= $true)]
  [String] $appServicePlanName = "",

  [Parameter (Mandatory= $false)]
  [String] $maxAllowedTier = "F1"
)

$connectionName = "AzureRunAsConnection"

# Adjust tier levels and their order to fit your needs.
$tierLevels = @("F1", "D1", "B1", "B2", "B3", "S1", "S2", "S3", "P1", "P2", "P3")
$tierConfigs = @{
    F1=@("Free","");
    D1=@("Shared","");
    B1=@("Basic","Small");
    B2=@("Basic","Medium");
    B3=@("Basic","Large");
    S1=@("Standard","Small");
    S2=@("Standard","Medium");
    S3=@("Standard","Large");
    P1=@("Premium","Small");
    P2=@("Premium","Medium");
    P3=@("Premium","Large");
}

Function IndexOf {
    param (
        [array]$Array, [string]$Item
    )

    return (0..($Array.Count-1)) | Where-Object {$array[$_] -eq $Item}
}

try {
    $servicePrincipalConnection=Get-AutomationConnection -Name $connectionName
    Add-AzureRmAccount -ServicePrincipal -TenantId $servicePrincipalConnection.TenantId -ApplicationId $servicePrincipalConnection.ApplicationId -CertificateThumbprint $servicePrincipalConnection.CertificateThumbprint

    $currentPlan = Get-AzureRmAppServicePlan -ResourceGroupName $resourceGroupName -Name $appServicePlanName
    $currentTier = $currentPlan.Sku.Name
    Write-Output "Current tier: $currentTier"

    $currentTierIndex = IndexOf -Array $tierLevels -Item $currentTier
    Write-Output "Current tier index: $currentTierIndex"
    $indexOfMaxAllowedTier = IndexOf -Array $tierLevels -Item $maxAllowedTier
    $nextTier = $tierLevels[$currentTierIndex + 1]

    if ($currentTierIndex -lt $indexOfMaxAllowedTier) {
        Write-Output "Scaling $currentTier to $nextTier"

        $targetTierConfig = $tierConfigs[$nextTier]
        $targetTier = $targetTierConfig[0]
        $targetWorkerSize = $targetTierConfig[1]
        if ($targetWorkerSize -eq "") {
            Set-AzureRmAppServicePlan -ResourceGroupName $resourceGroupName -Name $appServicePlanName -Tier $targetTier
        } else {
            Set-AzureRmAppServicePlan -ResourceGroupName $resourceGroupName -Name $appServicePlanName -Tier $targetTier -WorkerSize $targetWorkerSize
        }
    } else {
        $ErrorMessage = "Cannot scale up to $nextTier. CuurentTier $currentTier is the higest allowed."
        throw $ErrorMessage
    }
}

catch {
    if (!$servicePrincipalConnection) {
        $ErrorMessage = "Connection $connectionName not found."
        throw $ErrorMessage 
    } 
    else { 
        Write-Error -Message $_.Exception 
        throw $_.Exception
    }
}
```

#### Alerting

1. Przejdź do Alertów Azure i dodaj „New alert rule”
2. W Scope wybierz Twoj App Service Plan
3. W Condition skonfiguruj warunek, po spełnieniu którego ma się wywołać akcja skalowania. Np. kiedy średnie zużycie pamięci przekroczy 75%.
4. W Actions stwórz nową grupę. W Actions wybierz Acion type Automation Runbook i wybierz stworzony Runbook
5. Kliknij Review + create i gotowe!

Automatyzacja skalowania to jedno. Osobną kwestią jest dobre skonfigurowanie, kiedy ASP powinien się skalować. To już kwestia indywidualna, która zależy od sposobu, w jaki jest używany. Jeśli hostujesz na nim API dla sklepu internetowego, z którego korzystają użytkownicy jednej strefy czasowej, to możliwe, że wykres użycia będzie wyglądał całkiem regularnie i można skalować np. o konkretnej godzinie, bez monitorowania metryk i ustawiania alertów. Ale kiedy zmienność zużycia jest mniej przewidywalna, trzeba mądrze dobrać poziomy, na których ma się skalować. Nieźle opisuje to [Dokumentacja Microsoftu](https://docs.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-best-practices#manual-scaling-is-reset-by-autoscale-min-and-max).

## Warto wiedzieć

Czasami z skryptach z *Runbooks gallery* pojawiają się problemy z kodowaniem, przez co w kodzie skryptu znajdują się niepożądane znaki specjalne. Warto przejrzeć kod przed użyciem.

Upewnij się, że Runbook ma uprawnienia do modyfikowania App Service Planu.

Aplikacje hostowane na App Service Planie będą przez chwilę niedostępne, ponieważ skalowanie wertykalnie wymaga ich restartu (są przenoszone na nowy, wyższy lub niższy plan). Podobny downtime występuje w przypadku innych usług, np. baz SQL. Podczas testów aplikacja była niedostępna przez co najwyżej kilka sekund, więc w przypadku produkcyjnym, jeśli aplikacja jest dobrze zaprojektowana, nie powinno być problemów.

Jeśli zastanawiasz się nad kosztami, jakie realnie generują poszczególnie poziomy App Service Planów, zobacz [mój wpis o Azure Pricing Calculator](/azure-pricing-calculator/)
