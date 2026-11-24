---
title: "Wzorzec Builder do budowania danych testowych"
date: 2022-02-22
slug: "builder-do-budowania-danych-testowych"
permalink: /builder-do-budowania-danych-testowych/
categories: ["Inne"]
excerpt: "Pisząc testy jednostkowe, często potrzebujemy danych testowych. Częścią tych danych mogą być instancje jednej konkretnej klasy, ale różniące się wartościami właściwości w przypadku poszczególnych…"
image: "/assets/images/27f5b253-bob.jpg"
layout: post
---

Pisząc testy jednostkowe, często potrzebujemy danych testowych. Częścią tych danych mogą być instancje jednej konkretnej klasy, ale różniące się wartościami właściwości w przypadku poszczególnych testów. Część właściwości będzie jednak wspólna lub obojętna dla większości testów. W celu uniknięcia powtarzania kodu w testach warto zastosować jakiś automat – świetnie sprawdza się tu wzorzec **Budowniczy (Builder)**.

## Do przykładu!

### Mamy następujący kod

**Klasę** `Order`, w której wszystkie właściwości są wymagane – ich wartości trzeba podać w konstruktorze.

```
    public class Order
    {
        public Order(DateTime createdDate, decimal totalPrice, string currency, string description)
        {
            Id = Guid.NewGuid();
            CreatedDate = createdDate;
            TotalPrice = totalPrice;
            Currency = currency;
            Description = description;
        }
        
        public Guid Id { get; }
        public DateTime CreatedDate { get; }
        public decimal TotalPrice { get; }
        public string Currency { get; }
        public string Description { get; }
    }
```

Następnie mamy **serwis**, który wykonuje jakieś akcje na obiekcie `Order`. Jak widać, w różnych metodach różne właściwości obiektu `Order` będą potrzebne.

```
public class OrderService
    {
        private readonly decimal _vatPercentage;
        private readonly string _baseCurrency;

        public OrderService(decimal vatPercentage, string baseCurrency)
        {
            _vatPercentage = vatPercentage;
            _baseCurrency = baseCurrency;
        }

        public decimal CalculateTotalPrice(Order order)
        {
            if (order.TotalPrice == decimal.Zero)
            {
                throw new ArgumentException();
            }

            return order.TotalPrice + (order.TotalPrice * _vatPercentage);
        }

        public decimal CalculateTotalPriceInBaseCurrency(Order order)
        {
            var totalPrice = CalculateTotalPrice(order);

            if (string.IsNullOrEmpty(order.Currency))
            {
                throw new ArgumentException();
            }

            var exchangeRate = GetDummyExchangeRate(order.Currency, _baseCurrency);

            return totalPrice * exchangeRate;
        }

        public static void SendEmail(Order order)
        {
            if (string.IsNullOrEmpty(order.Description))
            {
                throw new ArgumentNullException();
            }

            var title = $"Order {order.Id} placed {order.CreatedDate}";
            var content = order.Description;
            
            DummySendEmail(title, content);
        }

        private static void DummySendEmail(string title, string content)
        {
            Console.WriteLine($"{title}. {content}");
        }

        private static decimal GetDummyExchangeRate(string from, string to)
        {
            return 2m;
        }
    }
```

No i oczywiście nasze **testy**. Testujemy jeden serwis i jego 3 metody, w każdym teście potrzebny jest nieco inny `Order`. Wygląda na to, że w każdym teście powtarzamy częściowo wywołanie konstruktora, podając dane, które dla danego testu są obojętne. Np. `TotalPrice` nie ma żadnego znaczenia przy testowaniu metody `SendMail`.

```
    [TestClass]
    public class OrderServiceTests
    {
        private readonly OrderService _orderService;
        
        public OrderServiceTests()
        {
            _orderService = new OrderService(0.23m, "PLN");
        }

        [TestMethod]
        public void CalculateTotalPrice()
        {
            var order = new Order(DateTime.Now, 100m, "PLN", "");

            const decimal expectedTotalPrice = 123m;
            var actualTotalPrice = _orderService.CalculateTotalPrice(order);
            
            Assert.AreEqual(expectedTotalPrice, actualTotalPrice);
        }
        
        [TestMethod]
        public void CalculateTotalPriceInBaseCurrency()
        {
            var order = new Order(DateTime.Now, 100m, "USD", "");

            const decimal expectedTotalPrice = 246m;
            var actualTotalPrice = _orderService.CalculateTotalPriceInBaseCurrency(order);
            
            Assert.AreEqual(expectedTotalPrice, actualTotalPrice);
        }
        
        [TestMethod]
        public void SendMail()
        {
            var order = new Order(DateTime.Now, 100m, "PLN", "This is description of the order");

            // Assert not throws
            OrderService.SendEmail(order);
        }
    }
```

Jak użyć Buildera, żeby trochę poprawić sytuację? Potrzebujemy zdefiniować w nim jakieś domyślne wartości i metody, które pozwolą utworzyć instancję ze zmodyfikowanymi konkretnymi właściwościami.

**Oto jak działa nasz Budowniczy.**

- Właściwości, które są nam totalnie obojętne (np. `CreatedDate`), możemy podać w konstruktorze klasy `Order` w metodzie `Build`.
- Właściwości, nad którymi chcemy mieć kontrolę, będziemy przypisywać ze zmiennych przechowywanych w Builderze. W konstruktorze Buildera ustawimy je na jakieś wartości domyślne, a w razie potrzeby będzie je można zmodyfikować metodami `With...`, w których podajemy żądaną wartość.

```
public class OrderBuilder
    {
        private decimal _totalPrice;
        private string _currency;
        private string _description;

        public OrderBuilder()
        {
            _totalPrice = 10m;
            _currency = "USD";
            _description = "";
        }

        public OrderBuilder WithTotalPrice(decimal totalPrice)
        {
            _totalPrice = totalPrice;
            return this;
        }

        public OrderBuilder WithCurrency(string currency)
        {
            _currency = currency;
            return this;
        }

        public OrderBuilder WithDescription(string description)
        {
            _description = description;
            return this;
        }
        
        public Order Build()
        {
            return new Order(DateTime.Now, _totalPrice, _currency, _description);
        }
    }
```

OK, a teraz nasze testy po małej refaktoryzacji z użyciem Buildera. Nie musimy już przejmować się obojętnymi nam właściwościami, wywołując za każdym razem konstruktor. Zamiast tego budujemy sobie obiekt `Order` z interesującymi nas wartościami dla danych właściwości.

```
    public class OrderBuilder
    {
        private decimal _totalPrice;
        private string _currency;
        private string _description;

        public OrderBuilder()
        {
            _totalPrice = 10m;
            _currency = "USD";
            _description = "";
        }

        public OrderBuilder WithTotalPrice(decimal totalPrice)
        {
            _totalPrice = totalPrice;
            return this;
        }

        public OrderBuilder WithCurrency(string currency)
        {
            _currency = currency;
            return this;
        }

        public OrderBuilder WithDescription(string description)
        {
            _description = description;
            return this;
        }
        
        public Order Build()
        {
            return new Order(DateTime.Now, _totalPrice, _currency, _description);
        }
    }
```

Oczywiście prawdziwą moc Budowniczy pokazuje dopiero przy bardziej skomplikowanych implementacjach. Tutaj starałem się to pokazać na w miarę prostym przykładzie, żeby zobrazować ideę.

## Podsumowując

Na koniec kilka dobrych praktyk związanych z tym rozwiązaniem:

- Domyślne dane powinny być w miarę możliwości prawidłowe. W moim przykładzie ustawiłem sensowne `TotalPrice` (10) i `Currency` (USD), ale złamałem tę zasadę, przypisując pusty string do `Description`.
- Dodawaj tylko te metody rozszerzające (`With...`), których potrzebujesz. Jeśli dla danego przypadku (tutaj dla testów) jedna wartość jest zawsze OK, to ustaw ją jako domyślną. Ja np. mógłbym tutaj podać jako domyślną wartość `TotalPrice` 100, a nie 10, bo w obu testach, gdzie potrzebuję `TotalPrice`, mogę użyć tej samej wartości.
- Staraj się w każdym teście używać nowej instancji Buildera. Zastosowanie jednej instancji dla całej klasy testowej może spowodować, że jeden test zmodyfikuje dane testowe innego testu, czym złamiemy zasadę izolacji testów.

Daj znać, czy używasz Buildera do testów? Może masz jakieś podpowiedzi, co jeszcze można robić lepiej?
