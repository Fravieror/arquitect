# Law of Demeter (LoD) in C#

## Overview

The **Law of Demeter** (LoD), also known as the **Principle of Least Knowledge**, is a fundamental design guideline for developing software. As an architect, mastering LoD helps you create loosely coupled systems that are easier to maintain, test, and evolve.

---

## 1. The Principle Defined

> **"Only talk to your immediate friends. Don't talk to strangers."**
>
> — Karl Lieberherr, 1987

### The Formal Rule

A method `M` of object `O` should only call methods of:

1. **O itself** (the object's own methods)
2. **M's parameters** (objects passed into the method)
3. **Objects created within M** (locally instantiated objects)
4. **O's direct component objects** (fields/properties of O)
5. **Global objects accessible by O** (static/singleton references)

### The "One Dot" Rule (Simplified)

```csharp
// ❌ VIOLATION - Multiple dots = talking to strangers
customer.GetWallet().GetCreditCard().Charge(amount);

// ✅ COMPLIANT - One dot = talking to friends
customer.ChargePayment(amount);
```

---

## 2. Why LoD Matters

| Without LoD | With LoD |
|-------------|----------|
| High coupling between classes | Loose coupling |
| Changes ripple through codebase | Changes are localized |
| Difficult to test (many mocks) | Easy to test |
| Code "knows" internal structure | Code respects encapsulation |
| Fragile to refactoring | Resilient to change |

### The Train Wreck Anti-Pattern

```csharp
// This is called a "train wreck" - chained method calls
string city = order.GetCustomer().GetAddress().GetCity().ToUpper();

// If ANY class in the chain changes, this code breaks!
```

---

## 3. Hands-On: Project Setup

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n DesignPrinciples
cd DesignPrinciples
```

Or if you already have it:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DesignPrinciples"
```

---

## 4. LoD Violations and Fixes

### Exercise 1: The Classic Wallet Example

Create a file `WalletViolation.cs` and type the following:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// CLASSIC LOD VIOLATION: Reaching into objects to get what you need
/// </summary>
public static class WalletViolation
{
    public static void Run()
    {
        Console.WriteLine("=== WALLET EXAMPLE - LOD VIOLATION ===\n");

        var customer = new CustomerV1
        {
            Name = "John Doe",
            Wallet = new WalletV1
            {
                Cash = 100m,
                CreditCard = new CreditCardV1
                {
                    Number = "4111-1111-1111-1111",
                    AvailableCredit = 5000m
                }
            }
        };

        // The cashier "reaches into" customer's wallet - VIOLATION!
        var cashier = new CashierV1();
        cashier.ProcessPayment(customer, 75m);
    }
}

// ==================== VIOLATION CODE ====================

public class CreditCardV1
{
    public string Number { get; set; } = "";
    public decimal AvailableCredit { get; set; }

    public void Charge(decimal amount)
    {
        if (amount > AvailableCredit)
            throw new InvalidOperationException("Insufficient credit");
        AvailableCredit -= amount;
        Console.WriteLine($"  Charged ${amount} to card ending in {Number[^4..]}");
    }
}

public class WalletV1
{
    public decimal Cash { get; set; }
    public CreditCardV1? CreditCard { get; set; }
}

public class CustomerV1
{
    public string Name { get; set; } = "";
    public WalletV1 Wallet { get; set; } = new();
}

// THE PROBLEM: Cashier knows internal structure of Customer and Wallet
public class CashierV1
{
    public void ProcessPayment(CustomerV1 customer, decimal amount)
    {
        Console.WriteLine($"Cashier processing ${amount} payment from {customer.Name}");

        // ❌ VIOLATION: Reaching through customer -> wallet -> cash
        if (customer.Wallet.Cash >= amount)
        {
            customer.Wallet.Cash -= amount;
            Console.WriteLine($"  Paid ${amount} in cash");
        }
        // ❌ VIOLATION: Reaching through customer -> wallet -> creditCard
        else if (customer.Wallet.CreditCard != null &&
                 customer.Wallet.CreditCard.AvailableCredit >= amount)
        {
            customer.Wallet.CreditCard.Charge(amount);
        }
        else
        {
            Console.WriteLine("  Payment failed - insufficient funds");
        }

        // Problems with this approach:
        // 1. Cashier knows Customer has a Wallet
        // 2. Cashier knows Wallet has Cash and CreditCard
        // 3. Cashier knows CreditCard has AvailableCredit
        // 4. If ANY of these change, Cashier breaks!
    }
}
```

---

### Exercise 2: Fix the Wallet Example

Create `WalletSolution.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// LOD-COMPLIANT SOLUTION: Tell, don't ask
/// </summary>
public static class WalletSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== WALLET EXAMPLE - LOD COMPLIANT ===\n");

        var customer = new CustomerV2("Jane Doe", 100m, 5000m);

        // Cashier just asks customer to pay - doesn't care HOW
        var cashier = new CashierV2();
        cashier.ProcessPayment(customer, 75m);
        cashier.ProcessPayment(customer, 50m);  // Will use credit card
    }
}

// ==================== COMPLIANT CODE ====================

// Payment result - tells us what happened
public record PaymentResult(bool Success, string Method, string Message);

// Credit card encapsulates its own behavior
public class CreditCardV2
{
    private readonly string _number;
    private decimal _availableCredit;

    public CreditCardV2(string number, decimal availableCredit)
    {
        _number = number;
        _availableCredit = availableCredit;
    }

    public bool CanCharge(decimal amount) => amount <= _availableCredit;

    public PaymentResult Charge(decimal amount)
    {
        if (!CanCharge(amount))
            return new PaymentResult(false, "Credit", "Insufficient credit");

        _availableCredit -= amount;
        return new PaymentResult(true, "Credit", $"Charged to card ending in {_number[^4..]}");
    }
}

// Wallet encapsulates payment logic
public class WalletV2
{
    private decimal _cash;
    private readonly CreditCardV2? _creditCard;

    public WalletV2(decimal cash, CreditCardV2? creditCard = null)
    {
        _cash = cash;
        _creditCard = creditCard;
    }

    // Wallet decides HOW to pay - caller doesn't need to know
    public PaymentResult Pay(decimal amount)
    {
        // Try cash first
        if (_cash >= amount)
        {
            _cash -= amount;
            return new PaymentResult(true, "Cash", $"Paid ${amount} in cash");
        }

        // Try credit card
        if (_creditCard != null && _creditCard.CanCharge(amount))
        {
            return _creditCard.Charge(amount);
        }

        return new PaymentResult(false, "None", "Insufficient funds");
    }
}

// Customer exposes payment capability, not internal structure
public class CustomerV2
{
    public string Name { get; }
    private readonly WalletV2 _wallet;

    public CustomerV2(string name, decimal cash, decimal creditLimit)
    {
        Name = name;
        _wallet = new WalletV2(cash, new CreditCardV2("4111-1111-1111-1111", creditLimit));
    }

    // ✅ Customer handles payment - caller doesn't reach into wallet
    public PaymentResult MakePayment(decimal amount)
    {
        return _wallet.Pay(amount);
    }
}

// Cashier only talks to Customer (immediate friend)
public class CashierV2
{
    public void ProcessPayment(CustomerV2 customer, decimal amount)
    {
        Console.WriteLine($"Cashier processing ${amount} payment from {customer.Name}");

        // ✅ COMPLIANT: Only calling method on parameter (customer)
        var result = customer.MakePayment(amount);

        Console.WriteLine($"  {(result.Success ? "✓" : "✗")} {result.Message}");
    }
}
```

---

### Exercise 3: Order Processing Violation

Create `OrderProcessingViolation.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// Real-world example: E-commerce order processing
/// </summary>
public static class OrderProcessingViolation
{
    public static void Run()
    {
        Console.WriteLine("\n=== ORDER PROCESSING - VIOLATIONS ===\n");

        var order = new OrderV1
        {
            Id = "ORD-001",
            Customer = new OrderCustomer
            {
                Name = "Alice Smith",
                Address = new AddressV1
                {
                    Street = "123 Main St",
                    City = "Seattle",
                    State = "WA",
                    ZipCode = "98101"
                },
                Email = "alice@example.com"
            },
            Items = new List<OrderItem>
            {
                new() { ProductName = "Laptop", Price = 999.99m, Quantity = 1 },
                new() { ProductName = "Mouse", Price = 29.99m, Quantity = 2 }
            }
        };

        var processor = new OrderProcessorV1();
        processor.ProcessOrder(order);
    }
}

// Domain classes
public class AddressV1
{
    public string Street { get; set; } = "";
    public string City { get; set; } = "";
    public string State { get; set; } = "";
    public string ZipCode { get; set; } = "";
}

public class OrderCustomer
{
    public string Name { get; set; } = "";
    public AddressV1 Address { get; set; } = new();
    public string Email { get; set; } = "";
}

public class OrderItem
{
    public string ProductName { get; set; } = "";
    public decimal Price { get; set; }
    public int Quantity { get; set; }
}

public class OrderV1
{
    public string Id { get; set; } = "";
    public OrderCustomer Customer { get; set; } = new();
    public List<OrderItem> Items { get; set; } = new();
}

// VIOLATING ORDER PROCESSOR
public class OrderProcessorV1
{
    public void ProcessOrder(OrderV1 order)
    {
        Console.WriteLine($"Processing order {order.Id}");

        // ❌ VIOLATION: Reaching into order -> customer -> address -> city
        Console.WriteLine($"  Shipping to: {order.Customer.Address.City}, {order.Customer.Address.State}");

        // ❌ VIOLATION: Reaching into order -> customer -> name
        Console.WriteLine($"  Customer: {order.Customer.Name}");

        // ❌ VIOLATION: Iterating through items and accessing their internals
        decimal total = 0;
        foreach (var item in order.Items)
        {
            total += item.Price * item.Quantity;
            Console.WriteLine($"  - {item.ProductName} x{item.Quantity}: ${item.Price * item.Quantity}");
        }

        Console.WriteLine($"  Total: ${total}");

        // ❌ VIOLATION: Reaching into order -> customer -> email
        Console.WriteLine($"  Confirmation sent to: {order.Customer.Email}");
    }
}
```

---

### Exercise 4: Fix Order Processing

Create `OrderProcessingSolution.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// LOD-COMPLIANT: Order contains behavior, not just data
/// </summary>
public static class OrderProcessingSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== ORDER PROCESSING - LOD COMPLIANT ===\n");

        var customer = new CustomerDetails(
            "Bob Johnson",
            new ShippingAddress("456 Oak Ave", "Portland", "OR", "97201"),
            "bob@example.com"
        );

        var order = new OrderV2("ORD-002", customer);
        order.AddItem("Keyboard", 79.99m, 1);
        order.AddItem("Monitor", 299.99m, 2);

        var processor = new OrderProcessorV2();
        processor.ProcessOrder(order);
    }
}

// ==================== COMPLIANT CODE ====================

// Immutable value objects with behavior
public record ShippingAddress(string Street, string City, string State, string ZipCode)
{
    // Address knows how to format itself
    public string GetShippingLabel() => $"{City}, {State} {ZipCode}";
    public override string ToString() => $"{Street}, {City}, {State} {ZipCode}";
}

public record CustomerDetails(string Name, ShippingAddress Address, string Email)
{
    // Customer knows how to provide shipping info
    public string GetShippingDestination() => Address.GetShippingLabel();
}

// Order line with behavior
public class OrderLine
{
    public string ProductName { get; }
    public decimal UnitPrice { get; }
    public int Quantity { get; }

    public OrderLine(string productName, decimal unitPrice, int quantity)
    {
        ProductName = productName;
        UnitPrice = unitPrice;
        Quantity = quantity;
    }

    // Line knows how to calculate its total
    public decimal GetLineTotal() => UnitPrice * Quantity;

    // Line knows how to describe itself
    public string GetDescription() => $"{ProductName} x{Quantity}: ${GetLineTotal()}";
}

// Order with rich behavior
public class OrderV2
{
    public string Id { get; }
    private readonly CustomerDetails _customer;
    private readonly List<OrderLine> _lines = new();

    public OrderV2(string id, CustomerDetails customer)
    {
        Id = id;
        _customer = customer;
    }

    public void AddItem(string productName, decimal unitPrice, int quantity)
    {
        _lines.Add(new OrderLine(productName, unitPrice, quantity));
    }

    // ✅ Order calculates its own total
    public decimal GetTotal() => _lines.Sum(l => l.GetLineTotal());

    // ✅ Order knows where to ship
    public string GetShippingDestination() => _customer.GetShippingDestination();

    // ✅ Order knows customer name for display
    public string GetCustomerName() => _customer.Name;

    // ✅ Order knows where to send confirmation
    public string GetConfirmationEmail() => _customer.Email;

    // ✅ Order provides line item descriptions
    public IEnumerable<string> GetLineDescriptions() =>
        _lines.Select(l => l.GetDescription());
}

// COMPLIANT ORDER PROCESSOR - Only talks to Order
public class OrderProcessorV2
{
    public void ProcessOrder(OrderV2 order)
    {
        Console.WriteLine($"Processing order {order.Id}");

        // ✅ Only calling methods on our parameter (order)
        Console.WriteLine($"  Shipping to: {order.GetShippingDestination()}");
        Console.WriteLine($"  Customer: {order.GetCustomerName()}");

        foreach (var description in order.GetLineDescriptions())
        {
            Console.WriteLine($"  - {description}");
        }

        Console.WriteLine($"  Total: ${order.GetTotal()}");
        Console.WriteLine($"  Confirmation sent to: {order.GetConfirmationEmail()}");
    }
}
```

---

### Exercise 5: Service Layer Violations

Create `ServiceLayerViolation.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// Common violation in service-oriented architectures
/// </summary>
public static class ServiceLayerViolation
{
    public static void Run()
    {
        Console.WriteLine("\n=== SERVICE LAYER VIOLATIONS ===\n");

        var container = new ServiceContainerV1();
        var controller = new UserControllerV1(container);

        controller.GetUserInfo(1);
    }
}

// Simulated services
public class UserServiceV1
{
    public UserDataV1? GetUser(int id) => new UserDataV1
    {
        Id = id,
        Profile = new ProfileV1 { FullName = "Test User", Age = 30 }
    };
}

public class ProfileV1
{
    public string FullName { get; set; } = "";
    public int Age { get; set; }
}

public class UserDataV1
{
    public int Id { get; set; }
    public ProfileV1 Profile { get; set; } = new();
}

// Service container (like a simple DI container)
public class ServiceContainerV1
{
    public UserServiceV1 UserService { get; } = new();
    public LoggerV1 Logger { get; } = new();
}

public class LoggerV1
{
    public void Log(string message) => Console.WriteLine($"  [LOG] {message}");
}

// Controller with LoD violations
public class UserControllerV1
{
    private readonly ServiceContainerV1 _container;

    public UserControllerV1(ServiceContainerV1 container)
    {
        _container = container;
    }

    public void GetUserInfo(int userId)
    {
        // ❌ VIOLATION: Reaching through container -> userService
        var user = _container.UserService.GetUser(userId);

        // ❌ VIOLATION: Reaching through container -> logger
        _container.Logger.Log($"Fetched user {userId}");

        if (user != null)
        {
            // ❌ VIOLATION: Reaching through user -> profile -> fullName
            Console.WriteLine($"User: {user.Profile.FullName}");

            // ❌ VIOLATION: Reaching through user -> profile -> age
            Console.WriteLine($"Age: {user.Profile.Age}");
        }
    }
}
```

---

### Exercise 6: Fix Service Layer with DI

Create `ServiceLayerSolution.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// LOD-COMPLIANT: Use dependency injection properly
/// </summary>
public static class ServiceLayerSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== SERVICE LAYER - LOD COMPLIANT ===\n");

        // Proper DI - inject only what's needed
        var userService = new UserServiceV2();
        var logger = new LoggerV2();
        var controller = new UserControllerV2(userService, logger);

        controller.GetUserInfo(1);
    }
}

// ==================== COMPLIANT CODE ====================

// Interfaces for abstraction
public interface IUserService
{
    UserDto? GetUser(int id);
}

public interface ILogger
{
    void Log(string message);
}

// DTO with only needed data (no nested objects to reach into)
public record UserDto(int Id, string FullName, int Age);

// Implementation
public class UserServiceV2 : IUserService
{
    public UserDto? GetUser(int id)
    {
        // Service returns flat DTO, not nested object graph
        return new UserDto(id, "Jane Smith", 28);
    }
}

public class LoggerV2 : ILogger
{
    public void Log(string message) => Console.WriteLine($"  [LOG] {message}");
}

// Controller with proper DI - only immediate dependencies
public class UserControllerV2
{
    private readonly IUserService _userService;  // ✅ Direct dependency
    private readonly ILogger _logger;            // ✅ Direct dependency

    public UserControllerV2(IUserService userService, ILogger logger)
    {
        _userService = userService;
        _logger = logger;
    }

    public void GetUserInfo(int userId)
    {
        // ✅ Calling method on field (_userService)
        var user = _userService.GetUser(userId);

        // ✅ Calling method on field (_logger)
        _logger.Log($"Fetched user {userId}");

        if (user != null)
        {
            // ✅ Accessing properties of returned object (local variable)
            Console.WriteLine($"User: {user.FullName}");
            Console.WriteLine($"Age: {user.Age}");
        }
    }
}
```

---

### Exercise 7: Fluent APIs - When Multiple Dots Are OK

Create `FluentApiExample.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// Fluent APIs are NOT LoD violations because each method returns 'this'
/// </summary>
public static class FluentApiExample
{
    public static void Run()
    {
        Console.WriteLine("\n=== FLUENT APIs - ACCEPTABLE CHAINS ===\n");

        // ✅ This is NOT a violation - each method returns the same builder
        var query = new QueryBuilder()
            .Select("Name", "Email")
            .From("Users")
            .Where("Age > 18")
            .OrderBy("Name")
            .Build();

        Console.WriteLine($"Generated Query: {query}\n");

        // ✅ StringBuilder example - fluent interface
        var message = new System.Text.StringBuilder()
            .Append("Hello, ")
            .Append("World!")
            .AppendLine()
            .Append("Welcome to LoD training.")
            .ToString();

        Console.WriteLine($"Built String:\n{message}\n");

        // ✅ LINQ is fluent - each method returns IEnumerable
        var numbers = new[] { 5, 2, 8, 1, 9, 3 };
        var result = numbers
            .Where(n => n > 2)
            .OrderBy(n => n)
            .Select(n => n * 2)
            .ToList();

        Console.WriteLine($"LINQ Result: [{string.Join(", ", result)}]");
    }
}

// Example fluent builder
public class QueryBuilder
{
    private readonly List<string> _selectColumns = new();
    private string _tableName = "";
    private string _whereClause = "";
    private string _orderByColumn = "";

    // Each method returns 'this' - always talking to the same object
    public QueryBuilder Select(params string[] columns)
    {
        _selectColumns.AddRange(columns);
        return this;  // Returns same object - NOT reaching into another object
    }

    public QueryBuilder From(string tableName)
    {
        _tableName = tableName;
        return this;
    }

    public QueryBuilder Where(string condition)
    {
        _whereClause = condition;
        return this;
    }

    public QueryBuilder OrderBy(string column)
    {
        _orderByColumn = column;
        return this;
    }

    public string Build()
    {
        var select = string.Join(", ", _selectColumns);
        var query = $"SELECT {select} FROM {_tableName}";

        if (!string.IsNullOrEmpty(_whereClause))
            query += $" WHERE {_whereClause}";

        if (!string.IsNullOrEmpty(_orderByColumn))
            query += $" ORDER BY {_orderByColumn}";

        return query;
    }
}
```

---

### Exercise 8: When LoD Doesn't Apply

Create `LoDExceptions.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// Cases where chained calls are acceptable
/// </summary>
public static class LoDExceptions
{
    public static void Run()
    {
        Console.WriteLine("\n=== WHEN LOD DOESN'T APPLY ===\n");

        // 1. VALUE OBJECTS (immutable data containers)
        Console.WriteLine("1. Value Objects:");
        var address = new Address("123 Main St", new City("Seattle"), new ZipCode("98101"));
        
        // ✅ OK - Value objects are data, not behavior
        Console.WriteLine($"   {address.City.Name}, {address.ZipCode.Code}");

        // 2. DATA TRANSFER OBJECTS (DTOs)
        Console.WriteLine("\n2. DTOs:");
        var response = new ApiResponse
        {
            Data = new UserResponse { Name = "John", Email = "john@example.com" },
            Meta = new MetaInfo { RequestId = "ABC123" }
        };

        // ✅ OK - DTOs are just data carriers
        Console.WriteLine($"   User: {response.Data.Name}, Request: {response.Meta.RequestId}");

        // 3. FLUENT BUILDERS (return this)
        Console.WriteLine("\n3. Fluent Builders:");
        var config = new ConfigBuilder()
            .WithTimeout(30)
            .WithRetries(3)
            .WithLogging(true)
            .Build();
        Console.WriteLine($"   Config: Timeout={config.Timeout}, Retries={config.Retries}");

        // 4. EXTENSION METHODS (syntactic sugar)
        Console.WriteLine("\n4. Extension Methods:");
        var text = "  hello world  ";
        
        // ✅ OK - Extensions operate on the object, not reaching into it
        var result = text.Trim().ToUpper().Replace(" ", "-");
        Console.WriteLine($"   '{text}' -> '{result}'");

        // 5. NULL-SAFE NAVIGATION (when dealing with external data)
        Console.WriteLine("\n5. Null-Safe Navigation:");
        ExternalData? data = new ExternalData { Inner = new InnerData { Value = "Found!" } };
        
        // ✅ OK - Defensive coding with external data
        var value = data?.Inner?.Value ?? "Not found";
        Console.WriteLine($"   Value: {value}");
    }
}

// Value objects (immutable)
public record City(string Name);
public record ZipCode(string Code);
public record Address(string Street, City City, ZipCode ZipCode);

// DTOs, what it stands for? Data Transfer Objects - simple data carriers without behavior
// is this what the end user will see? No, it's just a way to move data around without exposing internal structure
// should it be different from domain models? Yes, it should be flat and only contain the data needed for a specific use case
// should it be different from entity models? Yes, it should not contain any behavior or logic, just data
// should it be different from view models? Yes, it should not contain any presentation logic, just data
public class UserResponse { public string Name { get; set; } = ""; public string Email { get; set; } = ""; }
public class MetaInfo { public string RequestId { get; set; } = ""; }
public class ApiResponse { public UserResponse Data { get; set; } = new(); public MetaInfo Meta { get; set; } = new(); }

// External nullable data
public class InnerData { public string Value { get; set; } = ""; }
public class ExternalData { public InnerData? Inner { get; set; } }

// Fluent builder
public record AppConfig(int Timeout, int Retries, bool Logging);

public class ConfigBuilder
{
    private int _timeout = 10;
    private int _retries = 1;
    private bool _logging = false;

    public ConfigBuilder WithTimeout(int seconds) { _timeout = seconds; return this; }
    public ConfigBuilder WithRetries(int count) { _retries = count; return this; }
    public ConfigBuilder WithLogging(bool enabled) { _logging = enabled; return this; }
    public AppConfig Build() => new(_timeout, _retries, _logging);
}
```

---

### Exercise 9: Refactoring Train Wrecks

Create `RefactoringTrainWrecks.cs`:

```csharp
namespace DesignPrinciples.LawOfDemeter;

/// <summary>
/// Systematic approach to fixing LoD violations
/// </summary>
public static class RefactoringTrainWrecks
{
    public static void Run()
    {
        Console.WriteLine("\n=== REFACTORING TRAIN WRECKS ===\n");

        // BEFORE: Train wreck
        Console.WriteLine("TECHNIQUE 1: Move Method");
        Console.WriteLine("───────────────────────────");
        Console.WriteLine("Before: customer.GetAccount().GetBalance().IsOverdrawn()");
        Console.WriteLine("After:  customer.IsOverdrawn()");
        Console.WriteLine();

        Console.WriteLine("TECHNIQUE 2: Extract and Move");
        Console.WriteLine("───────────────────────────────");
        Console.WriteLine("Before: order.GetCustomer().GetAddress().GetCity().ValidateForShipping()");
        Console.WriteLine("After:  order.ValidateShippingDestination()");
        Console.WriteLine();

        Console.WriteLine("TECHNIQUE 3: Create Feature Envy Solution");
        Console.WriteLine("──────────────────────────────────────────");
        Console.WriteLine("Before: emailService.Send(user.GetProfile().GetEmail(), ...)");
        Console.WriteLine("After:  user.SendNotification(emailService, ...)");
        Console.WriteLine();

        Console.WriteLine("TECHNIQUE 4: Delegation / Wrapper Method");
        Console.WriteLine("─────────────────────────────────────────");
        DemonstrateDelegation();
    }

    static void DemonstrateDelegation()
    {
        // Original train wreck scenario
        var company = new CompanyV2(
            new DepartmentV2(
                new ManagerV2("Alice", "alice@company.com")));

        // ❌ BEFORE: company.GetDepartment().GetManager().GetEmail()
        // ✅ AFTER: company.GetManagerEmail()
        Console.WriteLine($"Manager Email: {company.GetManagerEmail()}");
    }
}

// Refactored with delegation methods
public class ManagerV2
{
    public string Name { get; }
    public string Email { get; }

    public ManagerV2(string name, string email)
    {
        Name = name;
        Email = email;
    }
}

public class DepartmentV2
{
    private readonly ManagerV2 _manager;

    public DepartmentV2(ManagerV2 manager) => _manager = manager;

    // Delegation method
    public string GetManagerEmail() => _manager.Email;
    public string GetManagerName() => _manager.Name;
}

public class CompanyV2
{
    private readonly DepartmentV2 _department;

    public CompanyV2(DepartmentV2 department) => _department = department;

    // Delegation method - no chaining needed
    public string GetManagerEmail() => _department.GetManagerEmail();
    public string GetManagerName() => _department.GetManagerName();
}
```

---

## 5. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DesignPrinciples.LawOfDemeter;

Console.WriteLine("╔══════════════════════════════════════════════════════════════╗");
Console.WriteLine("║       LAW OF DEMETER (LoD) - ARCHITECT TRAINING              ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════════╝");

WalletViolation.Run();
WalletSolution.Run();
OrderProcessingViolation.Run();
OrderProcessingSolution.Run();
ServiceLayerViolation.Run();
ServiceLayerSolution.Run();
FluentApiExample.Run();
LoDExceptions.Run();
RefactoringTrainWrecks.Run();

Console.WriteLine("\n\n=== ARCHITECT'S LOD CHEAT SHEET ===");
Console.WriteLine("┌────────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ ✅ ALLOWED: Call methods on...                                │");
Console.WriteLine("│    • Yourself (this)                                          │");
Console.WriteLine("│    • Parameters passed to your method                         │");
Console.WriteLine("│    • Objects you create locally                               │");
Console.WriteLine("│    • Your fields/properties                                   │");
Console.WriteLine("│    • Global/static objects                                    │");
Console.WriteLine("├────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ ❌ AVOID: Don't reach through objects...                      │");
Console.WriteLine("│    • customer.GetWallet().GetCard().Charge()                  │");
Console.WriteLine("│    • order.GetCustomer().GetAddress().GetCity()               │");
Console.WriteLine("│    • service.GetRepository().GetConnection().Execute()        │");
Console.WriteLine("├────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ 📋 EXCEPTIONS (when chaining is OK):                          │");
Console.WriteLine("│    • Fluent interfaces (builder.A().B().C())                  │");
Console.WriteLine("│    • Value objects / DTOs (immutable data)                    │");
Console.WriteLine("│    • LINQ queries (Where().Select().ToList())                 │");
Console.WriteLine("│    • Null-safe navigation (obj?.Prop?.Value)                  │");
Console.WriteLine("└────────────────────────────────────────────────────────────────┘");
```

---

## 6. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DesignPrinciples"
dotnet run
```

---

## 7. Architect's Decision Guide

### When to Apply LoD Strictly

| Scenario | Apply LoD? | Reason |
|----------|------------|--------|
| Business logic / domain layer | ✅ Yes | Reduce coupling |
| Service-to-service calls | ✅ Yes | Maintainability |
| Repository interactions | ✅ Yes | Testability |
| DTOs / View Models | ⚠️ No | They're just data |
| Fluent builders | ⚠️ No | Same object returned |
| LINQ queries | ⚠️ No | Functional transformation |
| Value objects | ⚠️ No | Immutable data |

### Refactoring Steps

```
1. IDENTIFY: Find chains like a.GetB().GetC().DoSomething()

2. ANALYZE: Is it a violation?
   - If B and C are value objects/DTOs → probably OK
   - If B and C are services/entities → likely violation

3. REFACTOR OPTIONS:
   a) Move behavior to the owner (CustomerController → Customer)
   b) Add delegation methods (GetManagerEmail() instead of GetManager().GetEmail())
   c) Use dependency injection (inject what you need directly)
   d) Create abstractions (interfaces that hide structure)

4. TEST: Verify coupling is reduced
   - Mock count in tests should decrease
   - Changes to inner classes shouldn't break outer code
```

### Tell, Don't Ask

```csharp
// ❌ ASK - You're asking for data, then deciding what to do
if (customer.GetWallet().GetBalance() > amount)
{
    customer.GetWallet().Deduct(amount);
}

// ✅ TELL - You're telling the object what you need done
var result = customer.MakePayment(amount);
```

---

## 8. Common Interview Questions

### Q1: What is the Law of Demeter?

**Answer**: "LoD states that a method should only call methods on its immediate collaborators—objects it owns, receives as parameters, or creates. It's about minimizing knowledge coupling by not 'reaching through' objects to access their internals."

### Q2: How do you recognize LoD violations?

**Answer**: "Look for:
1. Multiple dots in method chains (train wrecks)
2. Methods that need to know the internal structure of other objects
3. Tests that require many mocks to set up
4. Code that breaks when internal classes change"

### Q3: When is method chaining acceptable?

**Answer**: "When:
1. Each method returns `this` (fluent interface)
2. You're working with value objects or DTOs
3. Functional transformations like LINQ
4. The chain represents a single conceptual operation"

### Q4: How does LoD relate to other principles?

**Answer**:
- **Encapsulation**: LoD enforces encapsulation by hiding internal structure
- **SRP**: Objects that follow LoD often have focused responsibilities
- **DIP**: LoD encourages depending on abstractions, not concrete chains
- **Tell, Don't Ask**: LoD is the structural implementation of this principle

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Core Rule** | Only talk to immediate friends |
| **One Dot Rule** | Simplification: avoid `a.GetB().GetC()` |
| **Train Wreck** | Anti-pattern of chained method calls |
| **Tell, Don't Ask** | Push behavior into objects, don't pull data |
| **Fluent APIs** | Exception - each call returns same object |
| **Value Objects** | Exception - immutable data containers |
| **Fix Strategy** | Move methods, add delegation, use DI |

---

**Next Step**: Move to **Composition Over Inheritance** when ready!
