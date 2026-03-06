# Abstraction in C#

## 📖 Overview

**Abstraction** is one of the four fundamental pillars of OOP. It's the process of **hiding complex implementation details** and **exposing only the essential features** of an object. Users interact with a simplified interface without needing to understand the underlying complexity.

---

## 🎯 What is Abstraction?

Abstraction enables you to:
1. **Hide complexity** - Internal workings are hidden from users
2. **Show only essentials** - Expose what users need, nothing more
3. **Reduce coupling** - Users depend on interface, not implementation
4. **Manage complexity** - Break down complex systems into manageable parts

### Real-World Analogy

Think of **driving a car**:
- You use the **steering wheel, pedals, gear shift** (abstraction layer)
- You DON'T need to know **how the engine combustion works**
- You DON'T need to understand **transmission mechanics**
- The car **abstracts** all complexity behind a simple interface

```
    ┌─────────────────────────────────────────────────────────────┐
    │                        DRIVER                               │
    │              (Only sees the interface)                      │
    └─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────┐
    │               ABSTRACTION LAYER (Interface)                 │
    │    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
    │    │ Steering│  │  Gas    │  │  Brake  │  │  Gear   │      │
    │    │  Wheel  │  │  Pedal  │  │  Pedal  │  │  Shift  │      │
    │    └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
    └─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────┐
    │               HIDDEN COMPLEXITY                             │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
    │  │ Engine   │ │ Trans-   │ │ Brake    │ │ Steering │       │
    │  │ 1000s of │ │ mission  │ │ Hydraulic│ │ Mechanism│       │
    │  │ parts    │ │ Gears    │ │ System   │ │ Linkages │       │
    │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
    └─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Abstraction vs Encapsulation

| Aspect | Abstraction | Encapsulation |
|--------|-------------|---------------|
| **Focus** | WHAT an object does | HOW an object does it |
| **Purpose** | Hide complexity | Protect data |
| **Level** | Design level | Implementation level |
| **Achieved by** | Abstract classes, Interfaces | Access modifiers (private, public) |
| **Example** | Car has Start() method | Engine details are private |

```
┌─────────────────────────────────────────────────────────────────┐
│                        BOTH WORK TOGETHER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ABSTRACTION                    ENCAPSULATION                  │
│   ├── "A car can Start()"        ├── "private _engineState"    │
│   ├── "A car can Stop()"         ├── "private _fuelLevel"      │
│   └── Defines the contract       └── Protects implementation   │
│                                                                 │
│   Interface IVehicle             class Car : IVehicle           │
│   {                              {                              │
│       void Start();                  private bool _isRunning;  │
│       void Stop();                   public void Start() {..}  │
│   }                              }                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Abstraction in C#: Two Mechanisms

```
┌─────────────────────────────────────────────────────────────────┐
│                    ABSTRACTION IN C#                            │
├──────────────────────────┬──────────────────────────────────────┤
│    ABSTRACT CLASSES      │         INTERFACES                   │
├──────────────────────────┼──────────────────────────────────────┤
│ • Can have implementation│ • No implementation (until C# 8)    │
│ • Can have fields        │ • No fields                         │
│ • Can have constructors  │ • No constructors                   │
│ • Single inheritance     │ • Multiple inheritance              │
│ • "is-a" relationship    │ • "can-do" relationship             │
│ • Use: shared base code  │ • Use: define contracts             │
└──────────────────────────┴──────────────────────────────────────┘
```

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

Open your terminal and run:

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n Abstraction
cd Abstraction
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;
using System.Collections.Generic;

namespace AbstractionDemo
{
    // ═══════════════════════════════════════════════════════════════
    // PART 1: ABSTRACTION WITH ABSTRACT CLASSES
    // ═══════════════════════════════════════════════════════════════
    
    // Abstract class - CANNOT be instantiated directly
    public abstract class PaymentProcessor
    {
        // Regular property - inherited by all
        public string MerchantId { get; protected set; }
        public DateTime ProcessedAt { get; protected set; }
        
        // Constructor - CAN exist in abstract class
        protected PaymentProcessor(string merchantId)
        {
            MerchantId = merchantId;
        }
        
        // ─────────────────────────────────────────────────────────────
        // ABSTRACT METHOD - No implementation, MUST be overridden
        // This is the "contract" - derived classes define HOW
        // ─────────────────────────────────────────────────────────────
        public abstract bool ProcessPayment(decimal amount);
        public abstract bool RefundPayment(string transactionId, decimal amount);
        public abstract string GetProviderName();
        
        // ─────────────────────────────────────────────────────────────
        // CONCRETE METHOD - Has implementation, shared by all
        // ─────────────────────────────────────────────────────────────
        public void LogTransaction(string message)
        {
            Console.WriteLine($"  [{DateTime.Now:HH:mm:ss}] [{GetProviderName()}] {message}");
        }
        
        // Virtual method - CAN be overridden
        public virtual void DisplayReceipt(decimal amount)
        {
            Console.WriteLine($"\n  ══════════════════════════════");
            Console.WriteLine($"  RECEIPT");
            Console.WriteLine($"  Provider: {GetProviderName()}");
            Console.WriteLine($"  Merchant: {MerchantId}");
            Console.WriteLine($"  Amount: ${amount:N2}");
            Console.WriteLine($"  Date: {ProcessedAt:yyyy-MM-dd HH:mm:ss}");
            Console.WriteLine($"  ══════════════════════════════\n");
        }
    }
    
    // Concrete implementation - Stripe
    public class StripePayment : PaymentProcessor
    {
        private readonly string _apiKey;
        
        public StripePayment(string merchantId, string apiKey) : base(merchantId)
        {
            _apiKey = apiKey;
        }
        
        public override string GetProviderName() => "Stripe";
        
        public override bool ProcessPayment(decimal amount)
        {
            LogTransaction($"Connecting to Stripe API...");
            LogTransaction($"Authenticating with key: {_apiKey[..8]}...");
            LogTransaction($"Processing ${amount:N2}...");
            
            // Simulate API call
            ProcessedAt = DateTime.Now;
            
            LogTransaction("✅ Payment successful!");
            return true;
        }
        
        public override bool RefundPayment(string transactionId, decimal amount)
        {
            LogTransaction($"Refunding ${amount:N2} for transaction {transactionId}");
            LogTransaction("✅ Refund processed!");
            return true;
        }
    }
    
    // Concrete implementation - PayPal
    public class PayPalPayment : PaymentProcessor
    {
        private readonly string _clientId;
        private readonly string _secret;
        
        public PayPalPayment(string merchantId, string clientId, string secret) : base(merchantId)
        {
            _clientId = clientId;
            _secret = secret;
        }
        
        public override string GetProviderName() => "PayPal";
        
        public override bool ProcessPayment(decimal amount)
        {
            LogTransaction("Connecting to PayPal...");
            LogTransaction($"OAuth authentication with client: {_clientId[..6]}...");
            LogTransaction($"Creating payment of ${amount:N2}...");
            
            ProcessedAt = DateTime.Now;
            
            LogTransaction("✅ PayPal payment approved!");
            return true;
        }
        
        public override bool RefundPayment(string transactionId, decimal amount)
        {
            LogTransaction($"PayPal refund initiated for ${amount:N2}");
            LogTransaction("✅ Refund complete!");
            return true;
        }
        
        // Override virtual method with custom implementation
        public override void DisplayReceipt(decimal amount)
        {
            Console.WriteLine($"\n  ══════════════════════════════");
            Console.WriteLine($"  🅿️ PayPal RECEIPT");
            Console.WriteLine($"  ──────────────────────────────");
            Console.WriteLine($"  Merchant: {MerchantId}");
            Console.WriteLine($"  Amount: ${amount:N2}");
            Console.WriteLine($"  PayPal Fee: ${amount * 0.029m:N2}");
            Console.WriteLine($"  Net: ${amount * 0.971m:N2}");
            Console.WriteLine($"  Date: {ProcessedAt:yyyy-MM-dd HH:mm:ss}");
            Console.WriteLine($"  ══════════════════════════════\n");
        }
    }
    
    // Concrete implementation - Square
    public class SquarePayment : PaymentProcessor
    {
        public string LocationId { get; }
        
        public SquarePayment(string merchantId, string locationId) : base(merchantId)
        {
            LocationId = locationId;
        }
        
        public override string GetProviderName() => "Square";
        
        public override bool ProcessPayment(decimal amount)
        {
            LogTransaction($"Square POS at location {LocationId}");
            LogTransaction($"Processing ${amount:N2}...");
            
            ProcessedAt = DateTime.Now;
            
            LogTransaction("✅ Square payment complete!");
            return true;
        }
        
        public override bool RefundPayment(string transactionId, decimal amount)
        {
            LogTransaction($"Square refund: ${amount:N2}");
            return true;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 2: ABSTRACTION WITH INTERFACES
    // ═══════════════════════════════════════════════════════════════
    
    // Interface - Pure abstraction (defines WHAT, not HOW)
    public interface INotificationService
    {
        // All members are implicitly public and abstract
        bool Send(string recipient, string message);
        bool SendBulk(IEnumerable<string> recipients, string message);
        string GetServiceName();
    }
    
    // Another interface - can implement multiple
    public interface ITemplatable
    {
        void SetTemplate(string templateName);
        string RenderTemplate(Dictionary<string, string> variables);
    }
    
    // Concrete: Email notification
    public class EmailNotification : INotificationService, ITemplatable
    {
        private string _currentTemplate = "default";
        
        public string GetServiceName() => "Email";
        
        public bool Send(string recipient, string message)
        {
            Console.WriteLine($"  📧 Email to: {recipient}");
            Console.WriteLine($"     Subject: Notification");
            Console.WriteLine($"     Body: {message}");
            return true;
        }
        
        public bool SendBulk(IEnumerable<string> recipients, string message)
        {
            Console.WriteLine($"  📧 Sending bulk email...");
            foreach (var recipient in recipients)
            {
                Console.WriteLine($"     → {recipient}");
            }
            return true;
        }
        
        public void SetTemplate(string templateName)
        {
            _currentTemplate = templateName;
            Console.WriteLine($"  📧 Email template set to: {templateName}");
        }
        
        public string RenderTemplate(Dictionary<string, string> variables)
        {
            var result = $"[Template: {_currentTemplate}] ";
            foreach (var kvp in variables)
            {
                result += $"{kvp.Key}={kvp.Value} ";
            }
            return result;
        }
    }
    
    // Concrete: SMS notification
    public class SmsNotification : INotificationService
    {
        public string GetServiceName() => "SMS";
        
        public bool Send(string recipient, string message)
        {
            Console.WriteLine($"  📱 SMS to: {recipient}");
            Console.WriteLine($"     Message: {message}");
            return true;
        }
        
        public bool SendBulk(IEnumerable<string> recipients, string message)
        {
            Console.WriteLine($"  📱 Sending bulk SMS...");
            foreach (var recipient in recipients)
            {
                Console.WriteLine($"     → {recipient}");
            }
            return true;
        }
    }
    
    // Concrete: Push notification
    public class PushNotification : INotificationService
    {
        public string GetServiceName() => "Push";
        
        public bool Send(string recipient, string message)
        {
            Console.WriteLine($"  🔔 Push to device: {recipient}");
            Console.WriteLine($"     Alert: {message}");
            return true;
        }
        
        public bool SendBulk(IEnumerable<string> recipients, string message)
        {
            Console.WriteLine($"  🔔 Broadcasting push notification...");
            Console.WriteLine($"     Devices: {string.Join(", ", recipients)}");
            return true;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 3: LAYERED ABSTRACTION (Real-World Architecture)
    // ═══════════════════════════════════════════════════════════════
    
    // Repository interface - abstracts data access
    public interface IOrderRepository
    {
        Order GetById(int id);
        void Save(Order order);
        IEnumerable<Order> GetByCustomer(string customerId);
    }
    
    // Simple Order class
    public class Order
    {
        public int Id { get; set; }
        public string CustomerId { get; set; }
        public decimal Total { get; set; }
        public string Status { get; set; }
    }
    
    // Concrete: In-memory repository (for testing/development)
    public class InMemoryOrderRepository : IOrderRepository
    {
        private readonly Dictionary<int, Order> _orders = new();
        private int _nextId = 1;
        
        public Order GetById(int id)
        {
            Console.WriteLine($"  💾 [InMemory] Fetching order {id}...");
            return _orders.TryGetValue(id, out var order) ? order : null;
        }
        
        public void Save(Order order)
        {
            if (order.Id == 0)
            {
                order.Id = _nextId++;
            }
            _orders[order.Id] = order;
            Console.WriteLine($"  💾 [InMemory] Saved order {order.Id}");
        }
        
        public IEnumerable<Order> GetByCustomer(string customerId)
        {
            Console.WriteLine($"  💾 [InMemory] Finding orders for customer {customerId}...");
            foreach (var order in _orders.Values)
            {
                if (order.CustomerId == customerId)
                    yield return order;
            }
        }
    }
    
    // Concrete: SQL repository (for production)
    public class SqlOrderRepository : IOrderRepository
    {
        private readonly string _connectionString;
        
        public SqlOrderRepository(string connectionString)
        {
            _connectionString = connectionString;
        }
        
        public Order GetById(int id)
        {
            Console.WriteLine($"  🗄️ [SQL] SELECT * FROM Orders WHERE Id = {id}");
            // Simulate database call
            return new Order { Id = id, CustomerId = "CUST001", Total = 99.99m, Status = "Pending" };
        }
        
        public void Save(Order order)
        {
            Console.WriteLine($"  🗄️ [SQL] INSERT INTO Orders VALUES ({order.Id}, '{order.CustomerId}', {order.Total})");
        }
        
        public IEnumerable<Order> GetByCustomer(string customerId)
        {
            Console.WriteLine($"  🗄️ [SQL] SELECT * FROM Orders WHERE CustomerId = '{customerId}'");
            yield return new Order { Id = 1, CustomerId = customerId, Total = 50.00m, Status = "Complete" };
        }
    }
    
    // Service that depends on ABSTRACTION, not concrete class
    public class OrderService
    {
        private readonly IOrderRepository _repository;      // Abstraction!
        private readonly INotificationService _notifier;    // Abstraction!
        private readonly PaymentProcessor _paymentProcessor; // Abstraction!
        
        // Constructor Injection - receive abstractions
        public OrderService(
            IOrderRepository repository, 
            INotificationService notifier,
            PaymentProcessor paymentProcessor)
        {
            _repository = repository;
            _notifier = notifier;
            _paymentProcessor = paymentProcessor;
        }
        
        public void PlaceOrder(Order order)
        {
            Console.WriteLine($"\n  🛒 Processing order...\n");
            
            // Process payment (doesn't know which payment provider)
            if (_paymentProcessor.ProcessPayment(order.Total))
            {
                order.Status = "Paid";
                
                // Save order (doesn't know if InMemory or SQL)
                _repository.Save(order);
                
                // Send notification (doesn't know Email, SMS, or Push)
                _notifier.Send(
                    order.CustomerId, 
                    $"Your order #{order.Id} for ${order.Total:N2} has been placed!"
                );
                
                _paymentProcessor.DisplayReceipt(order.Total);
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN PROGRAM
    // ═══════════════════════════════════════════════════════════════
    
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("╔═══════════════════════════════════════════════╗");
            Console.WriteLine("║        ABSTRACTION DEMONSTRATION              ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 1: Abstract Class - Cannot Instantiate
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("📌 DEMO 1: Abstract Class Basics\n");
            
            // This would cause compile error:
            // PaymentProcessor processor = new PaymentProcessor("MERCH001");  // ❌ Cannot instantiate abstract class
            
            Console.WriteLine("⚠️ Cannot do: new PaymentProcessor() - it's abstract!\n");
            
            // Must use concrete implementations
            PaymentProcessor stripe = new StripePayment("MERCH001", "sk_test_abc123xyz");
            PaymentProcessor paypal = new PayPalPayment("MERCH002", "client_123", "secret_456");
            PaymentProcessor square = new SquarePayment("MERCH003", "LOC_001");
            
            Console.WriteLine("✅ Can create concrete implementations:\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 2: Using Abstract Interface
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 2: Using Abstraction (Payment Processors)\n");
            
            // All stored as abstract type
            List<PaymentProcessor> processors = new() { stripe, paypal, square };
            
            foreach (var processor in processors)
            {
                Console.WriteLine($"Processing with {processor.GetProviderName()}:");
                processor.ProcessPayment(49.99m);
                Console.WriteLine();
            }
            
            Console.WriteLine("⚡ Same interface, different implementations!\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 3: Interface Abstraction
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 3: Interface Abstraction\n");
            
            // Different notification services
            INotificationService email = new EmailNotification();
            INotificationService sms = new SmsNotification();
            INotificationService push = new PushNotification();
            
            string message = "Your order has shipped!";
            
            email.Send("user@email.com", message);
            Console.WriteLine();
            
            sms.Send("+1-555-0123", message);
            Console.WriteLine();
            
            push.Send("device_token_abc", message);
            
            Console.WriteLine("\n⚡ Same INotificationService interface, 3 different implementations!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 4: Multiple Interface Implementation
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 4: Multiple Interfaces\n");
            
            // EmailNotification implements BOTH INotificationService AND ITemplatable
            var emailService = new EmailNotification();
            
            // Use as INotificationService
            INotificationService notifier = emailService;
            notifier.Send("user@test.com", "Hello!");
            
            Console.WriteLine();
            
            // Use as ITemplatable
            ITemplatable templatable = emailService;
            templatable.SetTemplate("welcome_email");
            var rendered = templatable.RenderTemplate(new Dictionary<string, string>
            {
                ["name"] = "John",
                ["product"] = "Widget"
            });
            Console.WriteLine($"  Rendered: {rendered}");
            
            Console.WriteLine("\n⚡ One class, multiple abstraction contracts!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 5: Real-World Layered Architecture
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 5: Layered Abstraction (Architecture)\n");
            
            Console.WriteLine("── Configuration 1: Development (InMemory + Email + Stripe) ──\n");
            
            var devService = new OrderService(
                new InMemoryOrderRepository(),    // Easy to test
                new EmailNotification(),          // Developer email
                new StripePayment("DEV_MERCH", "sk_test_dev123")
            );
            
            devService.PlaceOrder(new Order 
            { 
                CustomerId = "dev@test.com", 
                Total = 29.99m 
            });
            
            Console.WriteLine("\n── Configuration 2: Production (SQL + SMS + PayPal) ──\n");
            
            var prodService = new OrderService(
                new SqlOrderRepository("Server=prod;Database=Orders"),
                new SmsNotification(),            // SMS for immediate alerts
                new PayPalPayment("PROD_MERCH", "prod_client", "prod_secret")
            );
            
            prodService.PlaceOrder(new Order 
            { 
                CustomerId = "+1-555-0100", 
                Total = 149.99m 
            });
            
            Console.WriteLine("\n⚡ Same OrderService code works with ANY implementation!");
            Console.WriteLine("   Swap databases, notification methods, payment providers");
            Console.WriteLine("   WITHOUT changing the OrderService class!");

            // ─────────────────────────────────────────────────────────────
            // KEY TAKEAWAYS
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("🎯 KEY TAKEAWAYS:");
            Console.WriteLine("═══════════════════════════════════════════════════");
            Console.WriteLine("1. ABSTRACT CLASS: Can have implementation + abstract methods");
            Console.WriteLine("2. INTERFACE: Pure contract, no implementation (mostly)");
            Console.WriteLine("3. HIDE COMPLEXITY: Users see interface, not internals");
            Console.WriteLine("4. DEPEND ON ABSTRACTIONS: Not concrete classes");
            Console.WriteLine("5. ENABLES: Testing, flexibility, maintainability");
            Console.WriteLine("6. REAL USE: Repositories, services, plugins, providers");
            Console.WriteLine("═══════════════════════════════════════════════════");

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
```

### Step 3: Run the Program

```powershell
dotnet run
```

---

## 📝 Expected Output

```
╔═══════════════════════════════════════════════╗
║        ABSTRACTION DEMONSTRATION              ║
╚═══════════════════════════════════════════════╝

📌 DEMO 1: Abstract Class Basics

⚠️ Cannot do: new PaymentProcessor() - it's abstract!

✅ Can create concrete implementations:

──────────────────────────────────────────────────
📌 DEMO 2: Using Abstraction (Payment Processors)

Processing with Stripe:
  [10:30:45] [Stripe] Connecting to Stripe API...
  [10:30:45] [Stripe] Authenticating with key: sk_test_...
  [10:30:45] [Stripe] Processing $49.99...
  [10:30:45] [Stripe] ✅ Payment successful!

Processing with PayPal:
  [10:30:45] [PayPal] Connecting to PayPal...
...
```

---

## 🧠 Quick Quiz - Test Your Understanding

1. **What's the main difference between abstract class and interface?**
   <details>
   <summary>Click for answer</summary>
   - **Abstract class**: Can have implementation, fields, constructors; single inheritance
   - **Interface**: Pure contract (until C# 8), no fields; multiple inheritance
   </details>

2. **Why can't we instantiate an abstract class?**
   <details>
   <summary>Click for answer</summary>
   Because it's incomplete - it may have abstract methods without implementation. It exists only to be inherited and extended.
   </details>

3. **Why should OrderService depend on IOrderRepository instead of SqlOrderRepository?**
   <details>
   <summary>Click for answer</summary>
   - Enables switching implementations (SQL, InMemory, MongoDB) without code changes
   - Makes testing easier (inject mock/fake repository)
   - Follows Dependency Inversion Principle (SOLID)
   </details>

4. **Can a class implement multiple interfaces?**
   <details>
   <summary>Click for answer</summary>
   Yes! C# supports multiple interface inheritance: `class MyClass : IInterface1, IInterface2`
   </details>

---

## 🎨 When to Use What

```
┌─────────────────────────────────────────────────────────────────┐
│              ABSTRACT CLASS vs INTERFACE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  USE ABSTRACT CLASS WHEN:                                       │
│  ├── Classes share common code (not just contract)             │
│  ├── Need constructors or fields                               │
│  ├── Want to provide default implementation                    │
│  └── "Is-a" relationship: Dog IS AN Animal                     │
│                                                                 │
│  USE INTERFACE WHEN:                                            │
│  ├── Define a contract/capability                              │
│  ├── Unrelated classes need same behavior                      │
│  ├── Need multiple inheritance                                 │
│  └── "Can-do" relationship: Duck CAN swim (ISwimmable)         │
│                                                                 │
│  COMBINE BOTH:                                                  │
│  abstract class Animal : IFeedable, ITrackable                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architectural Benefits

```
┌─────────────────────────────────────────────────────────────────┐
│           WITHOUT ABSTRACTION (Tightly Coupled)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  class OrderService                                             │
│  {                                                              │
│      private SqlOrderRepository _repo = new();  // ❌ Concrete │
│      private StripePayment _payment = new();    // ❌ Concrete │
│                                                                 │
│      // Can't test without real database                       │
│      // Can't switch to PayPal without code change             │
│      // Can't use different database                           │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│           WITH ABSTRACTION (Loosely Coupled)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  class OrderService                                             │
│  {                                                              │
│      private IOrderRepository _repo;        // ✅ Abstraction  │
│      private PaymentProcessor _payment;     // ✅ Abstraction  │
│                                                                 │
│      public OrderService(IOrderRepository r, PaymentProcessor p)│
│      {                                                          │
│          _repo = r;                                             │
│          _payment = p;                                          │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  // ✅ Easy testing with mocks                                  │
│  // ✅ Swap implementations without code changes                │
│  // ✅ Different configs for dev/test/prod                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
---

## ✅ Summary

| Concept | Abstract Class | Interface |
|---------|----------------|-----------|
| **Keyword** | `abstract class` | `interface` |
| **Instantiate?** | No | No |
| **Implementation?** | Yes (can have) | No (until C# 8 default methods) |
| **Fields?** | Yes | No |
| **Constructors?** | Yes | No |
| **Inheritance** | Single | Multiple |
| **Relationship** | "Is-a" | "Can-do" |

---

Create an example of how to use an interface with implementation in a real-world scenario, such as a notification system that can send emails, SMS, and push notifications.

you mention until C# 8, but now we have default interface methods. Can you show an example of how to use default interface methods in C# 8 and later?

can the Log method be overridden by the implementing classes? If so, how would that look in code? 

```csharp
public interface INotificationService
{
    void Send(string recipient, string message);

    // Default interface method
    void Log(string message)
    {
        Console.WriteLine($"Log: {message}");
    }
}

public class EmailNotificationService : INotificationService
{
    public void Send(string recipient, string message)
    {
        // Logic to send email
        Console.WriteLine($"Email sent to {recipient}: {message}");
    }

    // Override default interface method, this don't require the 'override' keyword, but it's good practice to include it for clarity. looks like this:

    public override void Log(string message)
    {
        Console.WriteLine($"Email Log: {message}");
    }

    // or this way without the 'override' keyword, but it's less clear that we're overriding a default method from the interface:
    // public void Log(string message)
    // {
    //     Console.WriteLine($"Email Log: {message}");
    // }
}

public class SmsNotificationService : INotificationService
{
    public void Send(string recipient, string message)
    {
        // Logic to send SMS
        Console.WriteLine($"SMS sent to {recipient}: {message}");
    }
}

public class PushNotificationService : INotificationService
{
    public void Send(string recipient, string message)
    {
        // Logic to send push notification
        Console.WriteLine($"Push notification sent to {recipient}: {message}");
    }
}

```

## 📚 Next Steps

Once you understand Abstraction, move on to:
- [ ] **Interfaces vs Abstract Classes** - Deep dive comparison
- [ ] **Composition vs Inheritance** - Design decisions
- [ ] **SOLID Principles** - Especially Dependency Inversion

---

*Happy Learning! 🚀*
