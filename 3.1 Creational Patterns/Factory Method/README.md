# Factory Method Pattern in C#

## Overview

The **Factory Method** is one of the most frequently used design patterns in production code. As a senior architect, you'll use it to decouple object creation from the code that uses those objects, enabling extensibility and adhering to the Open/Closed Principle.

Can you say this in plain English? The Factory Method allows you to define an interface for creating objects, but lets subclasses decide which class to instantiate. This means you can add new types of products without changing existing code, making your system more flexible and maintainable.

gimme an analogy: Imagine you're at a restaurant. The menu (factory) offers different dishes (products). When you order, the chef (creator) prepares the dish based on your choice. If the restaurant wants to add new dishes, they just update the menu and train the chef, without changing how customers order.

---

## 1. The Pattern Defined

> **"Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses."**
>
> — Gang of Four

### Structure

```
┌─────────────────┐         ┌─────────────────┐
│    Creator      │         │    Product      │
│ (abstract)      │         │  (interface)    │
├─────────────────┤         ├─────────────────┤
│ +FactoryMethod()│────────▶│ +Operation()    │
│ +SomeOperation()│         └─────────────────┘
└────────┬────────┘                  ▲
         │                           │
         │                 ┌─────────┴─────────┐
         │                 │                   │
┌────────┴────────┐   ┌────┴────┐       ┌─────┴─────┐
│ConcreteCreatorA │   │ProductA │       │ ProductB  │
├─────────────────┤   └─────────┘       └───────────┘
│+FactoryMethod() │
│ return ProductA │
└─────────────────┘
```

### Key Participants

| Participant | Role |
|-------------|------|
| **Product** | Interface/abstract class for objects the factory creates |
| **ConcreteProduct** | Implements the Product interface |
| **Creator** | Declares the factory method (abstract or default) |
| **ConcreteCreator** | Overrides factory method to return ConcreteProduct |

---

## 2. Why Factory Method Matters

| Problem | Factory Method Solution |
|---------|------------------------|
| `new` keyword creates tight coupling | Factory encapsulates object creation |
| Can't extend without modifying code | Add new creators without changing existing code |
| Complex construction logic scattered | Centralized in factory method |
| Hard to test (concrete dependencies) | Easy to mock/substitute factories |
| Violates Open/Closed Principle | New products = new creators, no modifications |

---

## 3. Hands-On: Project Setup

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n DesignPatterns
cd DesignPatterns
```

Or if you already have it:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DesignPatterns"
```

---

## 4. Factory Method Implementations

### Exercise 1: Classic Factory Method (GoF Style)

Create a file `ClassicFactoryMethod.cs` and type the following:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// CLASSIC FACTORY METHOD: The Gang of Four original pattern
/// Use when: You need subclasses to determine which objects to create
/// </summary>
public static class ClassicFactoryMethod
{
    public static void Run()
    {
        Console.WriteLine("=== CLASSIC FACTORY METHOD (GoF) ===\n");

        // Client works with Creator abstraction, not concrete products
        Document[] documents = 
        {
            new Report(),
            new Resume(),
            new Letter()
        };

        foreach (var doc in documents)
        {
            doc.CreatePages();
            Console.WriteLine($"{doc.GetType().Name} created with pages:");
            foreach (var page in doc.Pages)
            {
                Console.WriteLine($"  - {page.GetType().Name}");
            }
            Console.WriteLine();
        }
    }
}

// ==================== PRODUCT HIERARCHY ====================

// Abstract Product
public abstract class Page
{
    public abstract void Render();
}

// Concrete Products
public class SkillsPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Skills Page");
}

public class EducationPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Education Page");
}

public class ExperiencePage : Page
{
    public override void Render() => Console.WriteLine("Rendering Experience Page");
}

public class IntroductionPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Introduction Page");
}

public class ResultsPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Results Page");
}

public class ConclusionPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Conclusion Page");
}

public class SummaryPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Summary Page");
}

public class BibliographyPage : Page
{
    public override void Render() => Console.WriteLine("Rendering Bibliography Page");
}

// ==================== CREATOR HIERARCHY ====================

// Abstract Creator - defines the factory method
public abstract class Document
{
    public List<Page> Pages { get; } = new();

    // Factory Method - subclasses override this
    public abstract void CreatePages();
}

// Concrete Creators - each creates different pages
public class Resume : Document
{
    public override void CreatePages()
    {
        Pages.Add(new SkillsPage());
        Pages.Add(new EducationPage());
        Pages.Add(new ExperiencePage());
    }
}

public class Report : Document
{
    public override void CreatePages()
    {
        Pages.Add(new IntroductionPage());
        Pages.Add(new ResultsPage());
        Pages.Add(new ConclusionPage());
        Pages.Add(new SummaryPage());
        Pages.Add(new BibliographyPage());
    }
}

public class Letter : Document
{
    public override void CreatePages()
    {
        Pages.Add(new IntroductionPage());
        Pages.Add(new ConclusionPage());
    }
}
```

---

### Exercise 2: Factory Method with Interface

Create `InterfaceFactoryMethod.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// INTERFACE-BASED FACTORY METHOD: More flexible, C# idiomatic
/// Use when: You want looser coupling than abstract class hierarchy
/// </summary>
public static class InterfaceFactoryMethod
{
    public static void Run()
    {
        Console.WriteLine("=== INTERFACE-BASED FACTORY METHOD ===\n");

        // Different factories create different transports
        ITransportFactory[] factories =
        {
            new TruckFactory(),
            new ShipFactory(),
            new AirplaneFactory()
        };

        foreach (var factory in factories)
        {
            // Client code works with factory interface
            var transport = factory.CreateTransport();
            var cargo = new Cargo("Electronics", 5000);

            Console.WriteLine($"Using {factory.GetType().Name}:");
            transport.Deliver(cargo);
            Console.WriteLine();
        }
    }
}

// ==================== PRODUCT ====================

public record Cargo(string Description, decimal WeightKg);
// what is a record? A record is a reference type that provides built-in functionality for encapsulating data. It is immutable by default and comes with value-based equality, meaning two record instances are considered equal if their properties are equal. Records are ideal for representing data models, DTOs, and other simple data structures where immutability and value semantics are desired.

// whats the difference between class and record? The main differences between a class and a record in C# are:
// 1. Immutability: Records are immutable by default, meaning their properties cannot be changed after initialization. Classes are mutable unless you explicitly make them immutable.
// 2. Value-based equality: Records compare instances based on their property values, while classes compare instances based on reference equality.
// 3. Concise syntax: Records provide a more concise syntax for defining data-centric types, especially with positional parameters.

// Product interface
public interface ITransport
{
    void Deliver(Cargo cargo);
    decimal CalculateCost(decimal distanceKm);
}

// Concrete Products
public class Truck : ITransport
{
    public void Deliver(Cargo cargo)
    {
        Console.WriteLine($"  🚚 Delivering {cargo.Description} ({cargo.WeightKg}kg) by road");
    }

    public decimal CalculateCost(decimal distanceKm)
    {
        return distanceKm * 1.5m; // $1.50 per km
    }
}

public class Ship : ITransport
{
    public void Deliver(Cargo cargo)
    {
        Console.WriteLine($"  🚢 Delivering {cargo.Description} ({cargo.WeightKg}kg) by sea");
    }

    public decimal CalculateCost(decimal distanceKm)
    {
        return distanceKm * 0.5m; // $0.50 per km (cheaper for bulk)
    }
}

public class Airplane : ITransport
{
    public void Deliver(Cargo cargo)
    {
        Console.WriteLine($"  ✈️ Delivering {cargo.Description} ({cargo.WeightKg}kg) by air");
    }

    public decimal CalculateCost(decimal distanceKm)
    {
        return distanceKm * 5.0m; // $5.00 per km (expensive but fast)
    }
}

// ==================== FACTORY ====================

// Factory interface
public interface ITransportFactory
{
    ITransport CreateTransport();
}

// Concrete Factories
public class TruckFactory : ITransportFactory
{
    public ITransport CreateTransport() => new Truck();
}

public class ShipFactory : ITransportFactory
{
    public ITransport CreateTransport() => new Ship();
}

public class AirplaneFactory : ITransportFactory
{
    public ITransport CreateTransport() => new Airplane();
}

// it allows to add new transport types (e.g., Train, Drone) by simply creating new classes that implement ITransport and new factories that implement ITransportFactory, without modifying existing code. This adheres to the Open/Closed Principle and promotes extensibility.

// example using the factory method with a parameter to decide which transport to create: 

public class ParameterizedTransportFactory
{
    public ITransport CreateTransport(string type)
    {
        return type.ToLower() switch
        {
            "truck" => new Truck(),
            "ship" => new Ship(),
            "airplane" => new Airplane(),
            _ => throw new ArgumentException($"Unknown transport type: {type}")
        };
    }
}
```

---

### Exercise 3: Parameterized Factory Method

Create `ParameterizedFactory.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// PARAMETERIZED FACTORY METHOD: Uses parameter to decide which product to create
/// Use when: You want a single factory that can create multiple product types
/// </summary>
public static class ParameterizedFactory
{
    public static void Run()
    {
        Console.WriteLine("=== PARAMETERIZED FACTORY METHOD ===\n");

        var factory = new NotificationFactory();

        // Create different notifications using parameters
        var notifications = new[]
        {
            factory.CreateNotification(NotificationType.Email),
            factory.CreateNotification(NotificationType.SMS),
            factory.CreateNotification(NotificationType.Push),
            factory.CreateNotification(NotificationType.Slack)
        };

        var message = new Message("System Alert", "Server CPU usage is high!");

        foreach (var notification in notifications)
        {
            notification.Send(message);
        }
    }
}

// ==================== PRODUCT ====================

public record Message(string Subject, string Body);

public interface INotification
{
    void Send(Message message);
    bool CanSend();
}

public class EmailNotification : INotification
{
    public void Send(Message message)
    {
        Console.WriteLine($"📧 EMAIL: [{message.Subject}] {message.Body}");
    }

    public bool CanSend() => true; // Assume email is always available
}

public class SmsNotification : INotification
{
    public void Send(Message message)
    {
        // SMS has character limit
        var truncatedBody = message.Body.Length > 160 
            ? message.Body[..157] + "..." 
            : message.Body;
        Console.WriteLine($"📱 SMS: {truncatedBody}");
    }

    public bool CanSend() => true;
}

public class PushNotification : INotification
{
    public void Send(Message message)
    {
        Console.WriteLine($"🔔 PUSH: {message.Subject} - {message.Body}");
    }

    public bool CanSend() => true;
}

public class SlackNotification : INotification
{
    public void Send(Message message)
    {
        Console.WriteLine($"💬 SLACK: *{message.Subject}*\n   {message.Body}");
    }

    public bool CanSend() => true;
}

// ==================== FACTORY ====================

public enum NotificationType
{
    Email,
    SMS,
    Push,
    Slack
}

public class NotificationFactory
{
    // Parameterized factory method
    public INotification CreateNotification(NotificationType type)
    {
        return type switch
        {
            NotificationType.Email => new EmailNotification(),
            NotificationType.SMS => new SmsNotification(),
            NotificationType.Push => new PushNotification(),
            NotificationType.Slack => new SlackNotification(),
            _ => throw new ArgumentException($"Unknown notification type: {type}")
        };
    }
}
```

---

### Exercise 4: Factory Method with Registration (Plugin Pattern)

Create `RegistrationFactory.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// REGISTRATION-BASED FACTORY: Register creators dynamically
/// Use when: You need extensibility without modifying factory code (plugins)
/// </summary>
public static class RegistrationFactory
{
    public static void Run()
    {
        Console.WriteLine("=== REGISTRATION-BASED FACTORY ===\n");

        var factory = new PaymentProcessorFactory();

        // Register processors (could come from config, plugins, etc.)
        factory.Register("creditcard", () => new CreditCardProcessor());
        factory.Register("paypal", () => new PayPalProcessor());
        factory.Register("crypto", () => new CryptoProcessor());
        factory.Register("applepay", () => new ApplePayProcessor());

        // List available processors
        Console.WriteLine("Registered payment methods:");
        foreach (var method in factory.GetAvailableMethods())
        {
            Console.WriteLine($"  - {method}");
        }
        Console.WriteLine();

        // Process payments using different methods
        var payments = new[]
        {
            ("creditcard", 99.99m),
            ("paypal", 45.50m),
            ("crypto", 1000.00m),
            ("applepay", 25.00m)
        };

        foreach (var (method, amount) in payments)
        {
            var processor = factory.Create(method);
            processor.ProcessPayment(amount);
        }
    }
}

// ==================== PRODUCT ====================

public interface IPaymentProcessor
{
    void ProcessPayment(decimal amount);
    bool ValidatePayment(decimal amount);
}

public class CreditCardProcessor : IPaymentProcessor
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"💳 Processing ${amount:F2} via Credit Card");
    }

    public bool ValidatePayment(decimal amount) => amount > 0 && amount < 10000;
}

public class PayPalProcessor : IPaymentProcessor
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"🅿️ Processing ${amount:F2} via PayPal");
    }

    public bool ValidatePayment(decimal amount) => amount > 0;
}

public class CryptoProcessor : IPaymentProcessor
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"₿ Processing ${amount:F2} via Cryptocurrency");
    }

    public bool ValidatePayment(decimal amount) => amount >= 10; // Min $10 for crypto
}

public class ApplePayProcessor : IPaymentProcessor
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"🍎 Processing ${amount:F2} via Apple Pay");
    }

    public bool ValidatePayment(decimal amount) => amount > 0 && amount < 5000;
}

// ==================== FACTORY ====================

public class PaymentProcessorFactory
{
    private readonly Dictionary<string, Func<IPaymentProcessor>> _creators = new();

    // Register new processor types at runtime
    public void Register(string key, Func<IPaymentProcessor> creator)
    {
        _creators[key.ToLowerInvariant()] = creator;
    }

    // Factory method
    public IPaymentProcessor Create(string key)
    {
        var normalizedKey = key.ToLowerInvariant();
        
        if (!_creators.TryGetValue(normalizedKey, out var creator))
        {
            throw new ArgumentException($"Unknown payment method: {key}");
        }

        return creator();
    }

    public bool CanCreate(string key) => _creators.ContainsKey(key.ToLowerInvariant());

    public IEnumerable<string> GetAvailableMethods() => _creators.Keys;
}
```

---

### Exercise 5: Generic Factory Method

Create `GenericFactory.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// GENERIC FACTORY METHOD: Type-safe factory using generics
/// Use when: You want compile-time type safety for factory creation
/// </summary>
public static class GenericFactory
{
    public static void Run()
    {
        Console.WriteLine("=== GENERIC FACTORY METHOD ===\n");

        // Type-safe factory usage
        var userRepo = RepositoryFactory.Create<User>();
        var orderRepo = RepositoryFactory.Create<Order>();
        var productRepo = RepositoryFactory.Create<Product>();

        // Use repositories
        userRepo.Add(new User(1, "Alice"));
        userRepo.Add(new User(2, "Bob"));

        orderRepo.Add(new Order(100, 1, 299.99m));
        orderRepo.Add(new Order(101, 2, 149.50m));

        productRepo.Add(new Product(1000, "Laptop", 999.99m));

        Console.WriteLine("Users:");
        foreach (var user in userRepo.GetAll())
        {
            Console.WriteLine($"  {user}");
        }

        Console.WriteLine("\nOrders:");
        foreach (var order in orderRepo.GetAll())
        {
            Console.WriteLine($"  {order}");
        }

        Console.WriteLine("\nProducts:");
        foreach (var product in productRepo.GetAll())
        {
            Console.WriteLine($"  {product}");
        }
    }
}

// ==================== ENTITIES ====================

public record User(int Id, string Name);
public record Order(int Id, int UserId, decimal Total);
public record Product(int Id, string Name, decimal Price);

// ==================== REPOSITORY ====================

public interface IRepository<T>
{
    void Add(T entity);
    T? GetById(int id);
    IEnumerable<T> GetAll();
    void Delete(int id);
}

public class InMemoryRepository<T> : IRepository<T>
{
    private readonly List<T> _items = new();

    public void Add(T entity) => _items.Add(entity);

    public T? GetById(int id)
    {
        // Simple implementation - assumes T has Id property
        return _items.FirstOrDefault(item => 
            (int)(item?.GetType().GetProperty("Id")?.GetValue(item) ?? -1) == id);
    }

    public IEnumerable<T> GetAll() => _items.AsReadOnly();

    public void Delete(int id)
    {
        var item = GetById(id);
        if (item != null) _items.Remove(item);
    }
}

// ==================== GENERIC FACTORY ====================

public static class RepositoryFactory
{
    // Generic factory method
    public static IRepository<T> Create<T>() where T : class
    {
        // Could add logic here to return different implementations
        // based on T or configuration
        return new InMemoryRepository<T>();
    }

    // Overload with custom configuration
    public static IRepository<T> Create<T>(Action<RepositoryOptions> configure) where T : class
    {
        var options = new RepositoryOptions();
        configure(options);

        // Could return different implementations based on options
        return new InMemoryRepository<T>();
    }

    // how the Action<RepositoryOptions> relates to the factory method? The Action<RepositoryOptions> allows the caller to provide custom configuration for the repository being created. This way, the factory method can create repositories with different behaviors or settings based on the options provided, while still maintaining type safety and flexibility.

    // example usage of the overload with configuration:
    
    var userRepo = RepositoryFactory.Create<User>(options =>
    {
        options.EnableCaching = true;
        options.MaxItems = 500;
        options.CacheDuration = TimeSpan.FromMinutes(10);
    });    
    
}

public class RepositoryOptions
{
    public bool EnableCaching { get; set; }
    public int MaxItems { get; set; } = 1000;
    public TimeSpan? CacheDuration { get; set; }
}
```

---

### Exercise 6: Factory Method with Dependency Injection

Create `DIFactoryMethod.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// FACTORY METHOD WITH DI: Modern approach using dependency injection
/// Use when: Working with ASP.NET Core or other DI containers
/// </summary>
public static class DIFactoryMethod
{
    public static void Run()
    {
        Console.WriteLine("=== FACTORY METHOD WITH DI ===\n");

        // Simulate DI container setup
        var serviceProvider = BuildServiceProvider();

        // Get factory from DI
        var reportFactory = serviceProvider.GetService<IReportFactory>();

        // Generate different reports
        var reports = new[]
        {
            reportFactory!.CreateReport(ReportType.Sales), // what does the ! operator do here? The ! operator is the null-forgiving operator in C#. It tells the compiler that you are confident that the expression will not be null, even if the type allows for null. In this case, it is used to suppress the warning that reportFactory could be null when calling CreateReport. It indicates that you expect the DI container to have successfully resolved an instance of IReportFactory.
            reportFactory.CreateReport(ReportType.Inventory),
            reportFactory.CreateReport(ReportType.Financial)
        };

        var reportData = new ReportData(
            StartDate: DateTime.Now.AddMonths(-1),
            EndDate: DateTime.Now,
            Department: "Engineering");

        foreach (var report in reports)
        {
            report.Generate(reportData);
            Console.WriteLine();
        }
    }

    // Simulate building a DI container
    static SimpleServiceProvider BuildServiceProvider()
    {
        var provider = new SimpleServiceProvider();

        // Register dependencies
        provider.Register<ILogger>(() => new ConsoleLogger());
        provider.Register<IDataSource>(() => new DatabaseDataSource());
        
        // Register factory with dependencies
        provider.Register<IReportFactory>(() => new ReportFactory(
            provider.GetService<ILogger>()!,
            provider.GetService<IDataSource>()!));

        return provider;
    }
}

// ==================== DEPENDENCIES ====================

public interface ILogger
{
    void Log(string message);
}

public class ConsoleLogger : ILogger
{
    public void Log(string message) => Console.WriteLine($"[LOG] {message}");
}

public interface IDataSource
{
    object GetData(string query);
}

public class DatabaseDataSource : IDataSource
{
    public object GetData(string query) => $"Data from query: {query}";
}

// ==================== SIMPLE DI CONTAINER ====================

public class SimpleServiceProvider
{
    private readonly Dictionary<Type, Func<object>> _registrations = new();

    public void Register<T>(Func<T> factory) where T : class
    {
        _registrations[typeof(T)] = factory;
    }

    public T? GetService<T>() where T : class
    {
        if (_registrations.TryGetValue(typeof(T), out var factory))
        {
            return (T)factory();
        }
        return null;
    }
}

// ==================== PRODUCT ====================

public record ReportData(DateTime StartDate, DateTime EndDate, string Department);

public interface IReport
{
    void Generate(ReportData data);
    byte[] Export();
}

public class SalesReport : IReport
{
    private readonly ILogger _logger;
    private readonly IDataSource _dataSource;

    public SalesReport(ILogger logger, IDataSource dataSource)
    {
        _logger = logger;
        _dataSource = dataSource;
    }

    public void Generate(ReportData data)
    {
        _logger.Log($"Generating Sales Report for {data.Department}");
        var salesData = _dataSource.GetData($"SELECT * FROM Sales WHERE Date BETWEEN '{data.StartDate}' AND '{data.EndDate}'");
        Console.WriteLine($"📊 Sales Report: {salesData}");
    }

    public byte[] Export() => Array.Empty<byte>();
}

public class InventoryReport : IReport
{
    private readonly ILogger _logger;
    private readonly IDataSource _dataSource;

    public InventoryReport(ILogger logger, IDataSource dataSource)
    {
        _logger = logger;
        _dataSource = dataSource;
    }

    public void Generate(ReportData data)
    {
        _logger.Log($"Generating Inventory Report for {data.Department}");
        var inventoryData = _dataSource.GetData("SELECT * FROM Inventory");
        Console.WriteLine($"📦 Inventory Report: {inventoryData}");
    }

    public byte[] Export() => Array.Empty<byte>();
}

public class FinancialReport : IReport
{
    private readonly ILogger _logger;
    private readonly IDataSource _dataSource;

    public FinancialReport(ILogger logger, IDataSource dataSource)
    {
        _logger = logger;
        _dataSource = dataSource;
    }

    public void Generate(ReportData data)
    {
        _logger.Log($"Generating Financial Report for {data.Department}");
        var financialData = _dataSource.GetData("SELECT * FROM Financials");
        Console.WriteLine($"💰 Financial Report: {financialData}");
    }

    public byte[] Export() => Array.Empty<byte>();
}

// ==================== FACTORY ====================

public enum ReportType { Sales, Inventory, Financial }

public interface IReportFactory
{
    IReport CreateReport(ReportType type);
}

// Factory with injected dependencies
public class ReportFactory : IReportFactory
{
    private readonly ILogger _logger;
    private readonly IDataSource _dataSource;

    public ReportFactory(ILogger logger, IDataSource dataSource)
    {
        _logger = logger;
        _dataSource = dataSource;
    }

    public IReport CreateReport(ReportType type)
    {
        return type switch
        {
            ReportType.Sales => new SalesReport(_logger, _dataSource),
            ReportType.Inventory => new InventoryReport(_logger, _dataSource),
            ReportType.Financial => new FinancialReport(_logger, _dataSource),
            _ => throw new ArgumentException($"Unknown report type: {type}")
        };
    }
}
```

---

### Exercise 7: Factory Method vs Simple Factory vs Abstract Factory

Create `FactoryComparison.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// COMPARISON: Understanding when to use each factory variant
/// </summary>
public static class FactoryComparison
{
    public static void Run()
    {
        Console.WriteLine("=== FACTORY PATTERNS COMPARISON ===\n");

        // 1. SIMPLE FACTORY (not a GoF pattern, but commonly used)
        Console.WriteLine("1. SIMPLE FACTORY (Static Factory Method):");
        Console.WriteLine("   Use when: Simple creation logic, no need for extension");
        // what does it mean by "no need for extension"? It means that the simple factory is suitable when you have a fixed set of products and you don't anticipate needing to add new product types in the future. If you need to extend the product line, you would have to modify the existing factory code, which violates the Open/Closed Principle. In contrast, the Factory Method and Abstract Factory patterns allow for easier extension without modifying existing code.
        var button1 = SimpleButtonFactory.CreateButton("windows");
        button1.Render();
        Console.WriteLine();

        // 2. FACTORY METHOD (this pattern)
        Console.WriteLine("2. FACTORY METHOD:");
        Console.WriteLine("   Use when: Subclasses should decide what to create");
        // what does it mean by "subclasses should decide what to create"? It means that in the Factory Method pattern, you define an abstract creator class with a factory method, and then you create concrete subclasses that override this factory method to instantiate specific products. This allows each subclass to determine which product it creates, enabling more flexibility and adherence to the Open/Closed Principle. The client code interacts with the creator abstraction, and the actual product creation is deferred to the subclasses.
        DialogCreator dialog = new WindowsDialog();
        dialog.RenderWindow();
        Console.WriteLine();

        // 3. ABSTRACT FACTORY (creates families of objects)
        Console.WriteLine("3. ABSTRACT FACTORY:");
        Console.WriteLine("   Use when: Need to create families of related objects");
        // whats the difference between factory method and abstract factory? The Factory Method pattern focuses on creating a single product, where subclasses decide which specific product to instantiate. In contrast, the Abstract Factory pattern is designed to create families of related products without specifying their concrete classes. It provides an interface for creating multiple types of products that are related or dependent on each other, ensuring that the products created by a factory are compatible with each other. The Factory Method is more about defining a single method for object creation, while the Abstract Factory is about creating a suite of related objects.
        IGUIFactory factory = new WindowsGUIFactory();
        var button2 = factory.CreateButton();
        var checkbox = factory.CreateCheckbox();
        button2.Render();
        checkbox.Render();
    }
}

// ==================== 1. SIMPLE FACTORY ====================
// Not a GoF pattern, but useful for simple scenarios

public interface IButton
{
    void Render();
}

public class WindowsButton : IButton
{
    public void Render() => Console.WriteLine("   [Windows Button]");
}

public class MacButton : IButton
{
    public void Render() => Console.WriteLine("   [Mac Button]");
}

// Simple factory - static method, no inheritance
public static class SimpleButtonFactory
{
    public static IButton CreateButton(string os)
    {
        return os.ToLower() switch
        {
            "windows" => new WindowsButton(),
            "mac" => new MacButton(),
            _ => throw new ArgumentException($"Unknown OS: {os}")
        };
    }
}

// ==================== 2. FACTORY METHOD ====================
// Subclasses decide which concrete class to instantiate

public abstract class DialogCreator
{
    // Factory method - subclasses override this
    public abstract IButton CreateButton();

    // Template method - uses the factory method
    public void RenderWindow()
    {
        Console.WriteLine("   Rendering dialog window...");
        var button = CreateButton();  // Factory method call
        button.Render();
        Console.WriteLine("   Dialog rendered!");
    }
}

public class WindowsDialog : DialogCreator
{
    public override IButton CreateButton() => new WindowsButton();
}

public class MacDialog : DialogCreator
{
    public override IButton CreateButton() => new MacButton();
}

// ==================== 3. ABSTRACT FACTORY ====================
// Creates families of related objects
// how do you define a family of related objects? A family of related objects refers to a group of products that are designed to work together and are often created by the same factory. For example, in a GUI application, you might have a family of related objects that includes buttons, checkboxes, textboxes, and menus. Each family corresponds to a specific theme or platform (e.g., Windows, Mac, Linux), and the products within that family are compatible with each other in terms of design and functionality. The Abstract Factory pattern allows you to create these families of related objects without specifying their concrete classes, ensuring that the products created by a factory are consistent and can work together seamlessly.

// what could be the families for a accounting software? In an accounting software, you could have families of related objects such as:
// 1. Report Generators: This family could include different types of report generators like FinancialReportGenerator, TaxReportGenerator, and AuditReportGenerator, each responsible for creating specific types of financial reports.
// 2. Data Exporters: This family could consist of various data exporters such as CsvExporter, ExcelExporter, and PdfExporter, which handle exporting financial data in different formats.
// 3. Chart Creators: This family could include different chart creators like BarChartCreator, PieChartCreator, and LineChartCreator, which generate visual representations of financial data for analysis and presentation purposes.


public interface ICheckbox
{
    void Render();
}

public class WindowsCheckbox : ICheckbox
{
    public void Render() => Console.WriteLine("   [Windows Checkbox]");
}

public class MacCheckbox : ICheckbox
{
    public void Render() => Console.WriteLine("   [Mac Checkbox]");
}

// Abstract factory interface - creates family of objects
public interface IGUIFactory
{
    IButton CreateButton();
    ICheckbox CreateCheckbox();
    // Could add: CreateTextBox(), CreateMenu(), etc.
}

public class WindowsGUIFactory : IGUIFactory
{
    public IButton CreateButton() => new WindowsButton();
    public ICheckbox CreateCheckbox() => new WindowsCheckbox();
}

public class MacGUIFactory : IGUIFactory
{
    public IButton CreateButton() => new MacButton();
    public ICheckbox CreateCheckbox() => new MacCheckbox();
}
```

---

### Exercise 8: Real-World Example - Logging Framework

Create `LoggingFactoryExample.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// REAL-WORLD: Logging framework similar to Serilog/NLog pattern
/// </summary>
public static class LoggingFactoryExample
{
    public static void Run()
    {
        Console.WriteLine("=== REAL-WORLD: LOGGING FACTORY ===\n");

        // Configure logging (like ASP.NET Core's logging)
        var loggerFactory = new LoggerFactory()
            .AddConsole(LogLevel.Debug)
            .AddFile("app.log", LogLevel.Warning)
            .AddJson("logs/structured.json", LogLevel.Info);

        // Get logger for a specific category
        var appLogger = loggerFactory.CreateLogger("Application");
        var dbLogger = loggerFactory.CreateLogger("Database");

        // Use loggers
        appLogger.LogDebug("Application starting...");
        appLogger.LogInfo("Processing request #12345");
        appLogger.LogWarning("Response time exceeded threshold");
        appLogger.LogError("Failed to connect to external service");

        Console.WriteLine();

        dbLogger.LogDebug("Executing query...");
        dbLogger.LogInfo("Query returned 150 rows");
        dbLogger.LogError("Connection timeout occurred");
    }
}

// ==================== LOG LEVELS ====================

public enum LogLevel
{
    Debug = 0,
    Info = 1,
    Warning = 2,
    Error = 3,
    Critical = 4
}

// ==================== SINK (OUTPUT) ====================

// what does it mean SINK? In logging frameworks, a "sink" refers to the destination or output target where log messages are sent. It is the component responsible for handling the actual writing of log entries to a specific medium, such as the console, a file, a database, or an external logging service. Each sink can have its own configuration, such as minimum log level, formatting, and filtering rules. The concept of sinks allows for flexible and extensible logging architectures, enabling developers to easily add new output targets without modifying the core logging logic.

public interface ILogSink
{
    void Write(LogLevel level, string category, string message);
    LogLevel MinimumLevel { get; }
}

public class ConsoleSink : ILogSink
{
    public LogLevel MinimumLevel { get; }

    public ConsoleSink(LogLevel minimumLevel) => MinimumLevel = minimumLevel;

    public void Write(LogLevel level, string category, string message)
    {
        if (level < MinimumLevel) return;

        var color = level switch
        {
            LogLevel.Debug => ConsoleColor.Gray,
            LogLevel.Info => ConsoleColor.White,
            LogLevel.Warning => ConsoleColor.Yellow,
            LogLevel.Error => ConsoleColor.Red,
            LogLevel.Critical => ConsoleColor.DarkRed,
            _ => ConsoleColor.White
        };

        Console.ForegroundColor = color;
        Console.WriteLine($"[{level}] {category}: {message}");
        Console.ResetColor();
    }
}

public class FileSink : ILogSink
{
    private readonly string _path;
    public LogLevel MinimumLevel { get; }

    public FileSink(string path, LogLevel minimumLevel)
    {
        _path = path;
        MinimumLevel = minimumLevel;
    }

    public void Write(LogLevel level, string category, string message)
    {
        if (level < MinimumLevel) return;
        
        // Simulate file write
        Console.WriteLine($"[FILE → {_path}] [{level}] {category}: {message}");
    }
}

public class JsonSink : ILogSink
{
    private readonly string _path;
    public LogLevel MinimumLevel { get; }

    public JsonSink(string path, LogLevel minimumLevel)
    {
        _path = path;
        MinimumLevel = minimumLevel;
    }

    public void Write(LogLevel level, string category, string message)
    {
        if (level < MinimumLevel) return;

        var json = $"{{\"level\":\"{level}\",\"category\":\"{category}\",\"message\":\"{message}\",\"timestamp\":\"{DateTime.UtcNow:O}\"}}";
        Console.WriteLine($"[JSON → {_path}] {json}");
    }
}

// ==================== LOGGER ====================

public interface ILogger
{
    void Log(LogLevel level, string message);
    void LogDebug(string message) => Log(LogLevel.Debug, message);
    void LogInfo(string message) => Log(LogLevel.Info, message);
    void LogWarning(string message) => Log(LogLevel.Warning, message);
    void LogError(string message) => Log(LogLevel.Error, message);
    void LogCritical(string message) => Log(LogLevel.Critical, message);
}

public class Logger : ILogger
{
    private readonly string _category;
    private readonly List<ILogSink> _sinks;

    public Logger(string category, List<ILogSink> sinks)
    {
        _category = category;
        _sinks = sinks;
    }

    public void Log(LogLevel level, string message)
    {
        foreach (var sink in _sinks)
        {
            sink.Write(level, _category, message);
        }
    }
}

// ==================== FACTORY ====================

public class LoggerFactory
{
    private readonly List<ILogSink> _sinks = new();

    // Fluent configuration methods
    public LoggerFactory AddConsole(LogLevel minimumLevel = LogLevel.Info)
    {
        _sinks.Add(new ConsoleSink(minimumLevel));
        return this;
    }

    public LoggerFactory AddFile(string path, LogLevel minimumLevel = LogLevel.Warning)
    {
        _sinks.Add(new FileSink(path, minimumLevel));
        return this;
    }

    public LoggerFactory AddJson(string path, LogLevel minimumLevel = LogLevel.Info)
    {
        _sinks.Add(new JsonSink(path, minimumLevel));
        return this;
    }

    // Factory method
    public ILogger CreateLogger(string category)
    {
        return new Logger(category, new List<ILogSink>(_sinks));
    }

    // Generic factory method
    public ILogger CreateLogger<T>()
    {
        return CreateLogger(typeof(T).Name);
    }
}
```

---

### Exercise 9: Testing with Factory Method

Create `TestableFactory.cs`:

```csharp
namespace DesignPatterns.FactoryMethod;

/// <summary>
/// TESTABILITY: How Factory Method enables easier testing
/// </summary>
public static class TestableFactory
{
    public static void Run()
    {
        Console.WriteLine("=== FACTORY METHOD FOR TESTABILITY ===\n");

        // Production code
        Console.WriteLine("PRODUCTION MODE:");
        var prodService = new OrderService(new ProductionDependencyFactory());
        prodService.ProcessOrder(new OrderRequest("PROD-001", 5, 99.99m));

        Console.WriteLine();

        // Test code - swap factory for testing
        Console.WriteLine("TEST MODE:");
        var testService = new OrderService(new TestDependencyFactory());
        testService.ProcessOrder(new OrderRequest("TEST-001", 3, 49.99m));

        Console.WriteLine();

        // Verify test expectations
        Console.WriteLine("TEST VERIFICATIONS:");
        TestVerifications();
    }

    static void TestVerifications()
    {
        // Using test doubles created by factory
        var testFactory = new TestDependencyFactory();
        var service = new OrderService(testFactory);

        service.ProcessOrder(new OrderRequest("VERIFY-001", 1, 10.00m));

        // Access test doubles for verification
        var mockPayment = (MockPaymentGateway)testFactory.CreatePaymentGateway();
        var mockEmail = (MockEmailService)testFactory.CreateEmailService();

        Console.WriteLine($"  ✓ Payment processed: {mockPayment.ProcessedCount} time(s)");
        Console.WriteLine($"  ✓ Email sent: {mockEmail.SentCount} time(s)");
    }
}

// ==================== DEPENDENCIES ====================

public record OrderRequest(string OrderId, int Quantity, decimal Price);

public interface IPaymentGateway
{
    bool ProcessPayment(decimal amount);
}

public interface IEmailService
{
    void SendConfirmation(string orderId);
}

public interface IInventoryService
{
    bool ReserveStock(int quantity);
}

// ==================== PRODUCTION IMPLEMENTATIONS ====================

public class StripePaymentGateway : IPaymentGateway
{
    public bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"  💳 Stripe: Processing ${amount:F2}...");
        return true;
    }
}

public class SendGridEmailService : IEmailService
{
    public void SendConfirmation(string orderId)
    {
        Console.WriteLine($"  📧 SendGrid: Confirmation sent for {orderId}");
    }
}

public class WarehouseInventoryService : IInventoryService
{
    public bool ReserveStock(int quantity)
    {
        Console.WriteLine($"  📦 Warehouse: Reserved {quantity} items");
        return true;
    }
}

// ==================== TEST DOUBLES ====================

public class MockPaymentGateway : IPaymentGateway
{
    public int ProcessedCount { get; private set; }
    public bool ShouldSucceed { get; set; } = true;

    public bool ProcessPayment(decimal amount)
    {
        ProcessedCount++;
        Console.WriteLine($"  [MOCK] Payment: ${amount:F2} - Success: {ShouldSucceed}");
        return ShouldSucceed;
    }
}

public class MockEmailService : IEmailService
{
    public int SentCount { get; private set; }
    public List<string> SentOrders { get; } = new();

    public void SendConfirmation(string orderId)
    {
        SentCount++;
        SentOrders.Add(orderId);
        Console.WriteLine($"  [MOCK] Email: Would send confirmation for {orderId}");
    }
}

public class MockInventoryService : IInventoryService
{
    public int ReservedCount { get; private set; }
    public bool ShouldSucceed { get; set; } = true;

    public bool ReserveStock(int quantity)
    {
        ReservedCount += quantity;
        Console.WriteLine($"  [MOCK] Inventory: {quantity} items - Success: {ShouldSucceed}");
        return ShouldSucceed;
    }
}

// ==================== FACTORY ====================

public interface IDependencyFactory
{
    IPaymentGateway CreatePaymentGateway();
    IEmailService CreateEmailService();
    IInventoryService CreateInventoryService();
}

// Production factory
public class ProductionDependencyFactory : IDependencyFactory
{
    public IPaymentGateway CreatePaymentGateway() => new StripePaymentGateway();
    public IEmailService CreateEmailService() => new SendGridEmailService();
    public IInventoryService CreateInventoryService() => new WarehouseInventoryService();
}

// Test factory - returns test doubles
public class TestDependencyFactory : IDependencyFactory
{
    // Keep references to mocks for verification
    private readonly MockPaymentGateway _payment = new();
    private readonly MockEmailService _email = new();
    private readonly MockInventoryService _inventory = new();

    public IPaymentGateway CreatePaymentGateway() => _payment;
    public IEmailService CreateEmailService() => _email;
    public IInventoryService CreateInventoryService() => _inventory;
}

// ==================== SERVICE ====================

public class OrderService
{
    private readonly IDependencyFactory _factory;

    public OrderService(IDependencyFactory factory)
    {
        _factory = factory;
    }

    public void ProcessOrder(OrderRequest request)
    {
        Console.WriteLine($"Processing Order: {request.OrderId}");

        // Get dependencies from factory
        var payment = _factory.CreatePaymentGateway();
        var inventory = _factory.CreateInventoryService();
        var email = _factory.CreateEmailService();

        // Process order
        if (inventory.ReserveStock(request.Quantity))
        {
            var total = request.Quantity * request.Price;
            if (payment.ProcessPayment(total))
            {
                email.SendConfirmation(request.OrderId);
            }
        }
    }
}
```

---

## 5. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DesignPatterns.FactoryMethod;

Console.WriteLine("╔══════════════════════════════════════════════════════════════╗");
Console.WriteLine("║       FACTORY METHOD PATTERN - ARCHITECT TRAINING            ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════════╝");

ClassicFactoryMethod.Run();
InterfaceFactoryMethod.Run();
ParameterizedFactory.Run();
RegistrationFactory.Run();
GenericFactory.Run();
DIFactoryMethod.Run();
FactoryComparison.Run();
LoggingFactoryExample.Run();
TestableFactory.Run();

Console.WriteLine("\n\n=== ARCHITECT'S FACTORY METHOD GUIDE ===");
Console.WriteLine("┌────────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ WHEN TO USE FACTORY METHOD:                                    │");
Console.WriteLine("│  ✅ Don't know exact types at compile time                    │");
Console.WriteLine("│  ✅ Want to let subclasses decide instantiation               │");
Console.WriteLine("│  ✅ Complex object creation logic                              │");
Console.WriteLine("│  ✅ Need to decouple client from concrete classes             │");
Console.WriteLine("│  ✅ Want to enable easy testing with mock factories           │");
Console.WriteLine("├────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ VARIANTS:                                                       │");
Console.WriteLine("│  • Classic (GoF)    → Subclass overrides factory method       │");
Console.WriteLine("│  • Parameterized    → Single factory, parameter decides type  │");
Console.WriteLine("│  • Registration     → Dynamic registration (plugins)          │");
Console.WriteLine("│  • Generic          → Type-safe with generics                 │");
Console.WriteLine("│  • With DI          → Modern approach with containers         │");
Console.WriteLine("├────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ RELATED PATTERNS:                                               │");
Console.WriteLine("│  • Simple Factory   → Static method, no inheritance           │");
Console.WriteLine("│  • Abstract Factory → Creates families of related objects     │");
Console.WriteLine("│  • Builder          → Step-by-step complex object creation    │");
Console.WriteLine("│  • Prototype        → Clone existing objects                  │");
Console.WriteLine("└────────────────────────────────────────────────────────────────┘");
```

---

## 6. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DesignPatterns"
dotnet run
```

---

## 7. Architect's Decision Guide

### When to Use Each Variant

| Scenario | Recommended Variant |
|----------|-------------------|
| Simple creation, few types | Simple Factory (static method) |
| Subclasses define products | Classic Factory Method |
| Runtime type selection | Parameterized Factory |
| Plugin architecture | Registration Factory |
| Type-safe generic creation | Generic Factory |
| ASP.NET Core / DI containers | Factory with DI |
| Family of related objects | Abstract Factory |

### Factory Method vs Alternatives

```
┌─────────────────────┬─────────────────────────────────────┐
│ Pattern             │ Use When                            │
├─────────────────────┼─────────────────────────────────────┤
│ Factory Method      │ Single product, subclass decision   │
│ Abstract Factory    │ Family of products, consistent set  │
│ Builder             │ Complex construction, many params   │
│ Prototype           │ Costly creation, clone existing     │
│ Dependency Injection│ External configuration, testability │
└─────────────────────┴─────────────────────────────────────┘
```

### SOLID Alignment

| Principle | How Factory Method Helps |
|-----------|-------------------------|
| **S**RP | Factory has single responsibility: creation |
| **O**CP | New products = new factories, no modifications |
| **L**SP | Products are substitutable via interface |
| **I**SP | Factories can have specific interfaces |
| **D**IP | Depend on Product interface, not concrete |

---

## 8. Common Interview Questions

### Q1: What is the Factory Method pattern?

**Answer**: "Factory Method defines an interface for creating objects but lets subclasses decide which class to instantiate. It's about delegating the instantiation logic to child classes, promoting loose coupling and following the Open/Closed Principle."

### Q2: Factory Method vs Abstract Factory?

**Answer**: 
- **Factory Method**: Creates ONE product, uses inheritance (subclass overrides method)
- **Abstract Factory**: Creates FAMILIES of products, uses composition (factory object creates multiple related products)

### Q3: When would you NOT use Factory Method?

**Answer**: 
- Simple applications where direct instantiation is sufficient
- When the overhead of additional classes isn't justified
- When types are known at compile time and won't change
- When using a DI container that handles creation

### Q4: How does Factory Method support testability?

**Answer**: "By injecting a factory interface instead of concrete classes, you can substitute test factories that create mock objects. This isolates the system under test from its dependencies."

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Intent** | Delegate instantiation to subclasses |
| **Core Idea** | "Define interface, let subclasses decide" |
| **Key Benefit** | Decouples client from concrete classes |
| **Variants** | Classic, Parameterized, Registration, Generic, DI |
| **OCP Compliance** | New products = new creators, no modifications |
| **Testability** | Swap factories to inject test doubles |

---

**Next Step**: Move to **Abstract Factory** when ready!
