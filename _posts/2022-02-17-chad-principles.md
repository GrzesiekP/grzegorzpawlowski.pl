---
title: "CHAD Principles!"
date: 2022-02-17
slug: "chad-principles"
permalink: /chad-principles/
categories: ["Git"]
excerpt: "Każdy zna i słyszał o SOLID, KISS, DRY, DI, HWDP i innych popularnych zestawach dobrych praktyk w programowaniu."
image: "/assets/images/24c89722-7fc3c89a979643ebeb552a6bd1ed83fc.jpg"
layout: post
---

Każdy zna i słyszał o SOLID, KISS, DRY, DI, HWDP i innych popularnych zestawach dobrych praktyk w programowaniu.

Ale założę się, że nikt nie zna pryncypiów **CHAD** dotyczących dobrych praktyk korzystania z systemu kontroli wersji i recenzji kodu.

## Do rzeczy!

![](../assets/images/dbf3a4aa-cover5.jpg)

## C – Clear History

Historia ma być czysta, jak Twój pokój po przeczytaniu książki Jordana Petersona! Ewentualnie jak dobra polska gorzałka! Każdy commit ma być sensowny i ma mieć znaczenie, żadnych „quick fix”, „small refactoring”. I żadnych gównobranczy sprzed 5 lat…

## H – Hermetic PR

Jak robisz PR, to ten PR ma dotyczyć konkretnej zmiany – konkretnej funkcjonalności albo jej logicznej części. A jak się nie da w osobnych PR-ach, bo się nie buduje, to rusz głową, żeby dać lepszy tytuł niż „Add new table + add migration + add some test + fix some issues + use new table in code”.

## A – Alternative Review

Code review nie polega na tym, że patrzysz, czy testy są zielone i czy u Ciebie działa. Nawet nie wystarczy, że przejdziesz przez checklistę SOLID, KISS, MPK, MPO, PDK… Pomyśl, czy nie da się tego zrobić lepiej, niż zrobił to autor PR-a. Jak się da, to zaproponuj – pomyślcie razem.

## D – Detailed Comment

Bardziej szczegółowe C. Napisz porządnie tę wiadomość. Wiem, że zostałeś programistą, bo ledwo Cię przepuścili w gimbazie za oblanie 99% sprawdzianów z polskiego, ale jak już masz te 20k, umiesz te śmieszne cyferki i literki, to dobrze by było, jakbyś umiał opisać słowami to, co zrobiłeś w kodzie. Nie jakieś gunwo typu „use new method”, „fix bug”, „modify interface”.

Stosujesz czy jesteś lamus?
