# Polymorphism in C#

## 📖 Overview

**Polymorphism** (from Greek: "many forms") is one of the four fundamental pillars of OOP. It allows objects of different types to be treated as objects of a common base type, while each object responds to the same method call in its own way.

---

## 🎯 What is Polymorphism?

Polymorphism enables:
1. **One interface, multiple implementations** - Same method name, different behaviors
2. **Flexibility** - Write code that works with base types, handles derived types
3. **Extensibility** - Add new types without changing existing code
4. **Runtime decisions** - Correct method called based on actual object type

### Real-World Analogy

Think of a **remote control**:
- Press "Power" button on ANY device remote
- TV turns on/off, AC turns on/off, Stereo turns on/off
- Same action ("press power"), different behavior based on device

---

## 🔄 Types of Polymorphism in C#

```
┌─────────────────────────────────────────────────────────────────┐
│                    TYPES OF POLYMORPHISM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. COMPILE-TIME (Static) Polymorphism                         │
│     ├── Method Overloading (same name, different parameters)   │
│     └── Operator Overloading (custom behavior for operators)   │
│                                                                 │
│  2. RUN-TIME (Dynamic) Polymorphism                            │
│     ├── Method Overriding (virtual/override)                   │
│     └── Interface Implementation                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Visual: Runtime Polymorphism

```
                        ┌─────────────────┐
                        │   Animal        │
                        │─────────────────│
                        │ virtual Speak() │
                        └────────┬────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
    │     Dog       │    │     Cat       │    │     Bird      │
    │───────────────│    │───────────────│    │───────────────│
    │override Speak │    │override Speak │    │override Speak │
    │  "Woof!"      │    │  "Meow!"      │    │  "Chirp!"     │
    └───────────────┘    └───────────────┘    └───────────────┘
    
    
    Animal animal = GetRandomAnimal();  // Could be Dog, Cat, or Bird
    animal.Speak();  // ← Which sound? Determined at RUNTIME!
```

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

Open your terminal and run:

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n Polymorphism
cd Polymorphism
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;
using System.Collections.Generic;

namespace PolymorphismDemo
{
    // ═══════════════════════════════════════════════════════════════
    // PART 1: COMPILE-TIME POLYMORPHISM (Method Overloading)
    // ═══════════════════════════════════════════════════════════════
    
    public class Calculator
    {
        // Same method name, different parameters = OVERLOADING
        
        public int Add(int a, int b)
        {
            Console.WriteLine("  → Using Add(int, int)");
            return a + b;
        }
        
        public double Add(double a, double b)
        {
            Console.WriteLine("  → Using Add(double, double)");
            return a + b;
        }
        
        public int Add(int a, int b, int c)
        {
            Console.WriteLine("  → Using Add(int, int, int)");
            return a + b + c;
        }
        
        public string Add(string a, string b)
        {
            Console.WriteLine("  → Using Add(string, string)");
            return a + b;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 2: RUNTIME POLYMORPHISM (Method Overriding)
    // ═══════════════════════════════════════════════════════════════
    
    // Base class with virtual methods
    public abstract class Shape
    {
        public string Name { get; protected set; }
        public string Color { get; set; }
        
        protected Shape(string name, string color)
        {
            Name = name;
            Color = color;
        }
        
        // Abstract method - MUST be implemented by derived classes
        public abstract double CalculateArea();
        
        // Virtual method - CAN be overridden
        public virtual double CalculatePerimeter()
        {
            return 0;  // Default implementation
        }
        
        // Virtual method - common display, can be extended
        public virtual void Display()
        {
            Console.WriteLine($"  Shape: {Name}");
            Console.WriteLine($"  Color: {Color}");
            Console.WriteLine($"  Area: {CalculateArea():F2}");
            Console.WriteLine($"  Perimeter: {CalculatePerimeter():F2}");
        }
        
        // Non-virtual method - same for all shapes
        public void PrintType()
        {
            Console.WriteLine($"  I am a {Name}");
        }
    }
    
    public class Circle : Shape
    {
        public double Radius { get; set; }
        
        public Circle(double radius, string color) : base("Circle", color)
        {
            Radius = radius;
        }
        
        // MUST override abstract method
        public override double CalculateArea()
        {
            return Math.PI * Radius * Radius;
        }
        
        public override double CalculatePerimeter()
        {
            return 2 * Math.PI * Radius;
        }
        
        public override void Display()
        {
            base.Display();  // Call parent's Display
            // can just calling Display() do the same? Yes, but this way we can add extra info specific to Circle
            Console.WriteLine($"  Radius: {Radius}");
        }
    }
    
    public class Rectangle : Shape
    {
        public double Width { get; set; }
        public double Height { get; set; }
        
        public Rectangle(double width, double height, string color) 
            : base("Rectangle", color)
        {
            Width = width;
            Height = height;
        }
        
        public override double CalculateArea()
        {
            return Width * Height;
        }
        
        public override double CalculatePerimeter()
        {
            return 2 * (Width + Height);
        }
        
        public override void Display()
        {
            base.Display();
            Console.WriteLine($"  Width: {Width}, Height: {Height}");
        }
    }
    
    public class Triangle : Shape
    {
        public double Base { get; set; }
        public double Height { get; set; }
        public double Side1 { get; set; }
        public double Side2 { get; set; }
        public double Side3 { get; set; }
        
        public Triangle(double @base, double height, double s1, double s2, double s3, string color) 
            : base("Triangle", color)
        {
            Base = @base;
            Height = height;
            Side1 = s1;
            Side2 = s2;
            Side3 = s3;
        }
        
        public override double CalculateArea()
        {
            return 0.5 * Base * Height;
        }
        
        public override double CalculatePerimeter()
        {
            return Side1 + Side2 + Side3;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 3: INTERFACE POLYMORPHISM
    // ═══════════════════════════════════════════════════════════════
    
    public interface IPaymentProcessor
    {
        bool ProcessPayment(decimal amount);
        string GetPaymentMethod();
    }
    
    public class CreditCardPayment : IPaymentProcessor
    {
        public string CardNumber { get; set; }
        
        public CreditCardPayment(string cardNumber)
        {
            CardNumber = cardNumber;
        }
        
        public bool ProcessPayment(decimal amount)
        {
            Console.WriteLine($"  💳 Processing ${amount} via Credit Card ending in {CardNumber[^4..]}");
            // Simulate payment processing
            Console.WriteLine("  ✅ Credit card payment successful!");
            return true;
        }
        
        public string GetPaymentMethod() => "Credit Card";
    }
    
    public class PayPalPayment : IPaymentProcessor
    {
        public string Email { get; set; }
        
        public PayPalPayment(string email)
        {
            Email = email;
        }
        
        public bool ProcessPayment(decimal amount)
        {
            Console.WriteLine($"  📧 Processing ${amount} via PayPal ({Email})");
            Console.WriteLine("  ✅ PayPal payment successful!");
            return true;
        }
        
        public string GetPaymentMethod() => "PayPal";
    }
    
    public class CryptoPayment : IPaymentProcessor
    {
        public string WalletAddress { get; set; }
        public string CryptoCurrency { get; set; }
        
        public CryptoPayment(string wallet, string crypto)
        {
            WalletAddress = wallet;
            CryptoCurrency = crypto;
        }
        
        public bool ProcessPayment(decimal amount)
        {
            Console.WriteLine($"  🪙 Processing ${amount} via {CryptoCurrency}");
            Console.WriteLine($"     Wallet: {WalletAddress[..8]}...{WalletAddress[^4..]}");
            Console.WriteLine("  ✅ Crypto payment successful!");
            return true;
        }
        
        public string GetPaymentMethod() => $"Crypto ({CryptoCurrency})";
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 4: PRACTICAL EXAMPLE - Plugin System
    // ═══════════════════════════════════════════════════════════════
    
    public interface ILogger
    {
        void Log(string message);
        void LogError(string message);
    }
    
    public class ConsoleLogger : ILogger
    {
        public void Log(string message)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"  [CONSOLE] {DateTime.Now:HH:mm:ss} - {message}");
            Console.ResetColor();
        }
        
        public void LogError(string message)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"  [CONSOLE ERROR] {DateTime.Now:HH:mm:ss} - {message}");
            Console.ResetColor();
        }
    }
    
    public class FileLogger : ILogger
    {
        private readonly string _fileName;
        
        public FileLogger(string fileName)
        {
            _fileName = fileName;
        }
        
        public void Log(string message)
        {
            Console.WriteLine($"  [FILE:{_fileName}] {DateTime.Now:HH:mm:ss} - {message}");
            // In real code: File.AppendAllText(_fileName, message);
        }
        
        public void LogError(string message)
        {
            Console.WriteLine($"  [FILE ERROR:{_fileName}] {DateTime.Now:HH:mm:ss} - {message}");
        }
    }
    
    public class CloudLogger : ILogger
    {
        private readonly string _endpoint;
        
        public CloudLogger(string endpoint)
        {
            _endpoint = endpoint;
        }
        
        public void Log(string message)
        {
            Console.WriteLine($"  [CLOUD → {_endpoint}] {DateTime.Now:HH:mm:ss} - {message}");
        }
        
        public void LogError(string message)
        {
            Console.WriteLine($"  [CLOUD ERROR → {_endpoint}] {DateTime.Now:HH:mm:ss} - {message}");
        }
    }
    
    // Application that uses logging - doesn't care WHICH logger!
    public class OrderService
    {
        private readonly ILogger _logger;  // Depends on abstraction, not concrete class
        
        public OrderService(ILogger logger)
        {
            _logger = logger;
        }
        
        public void PlaceOrder(string orderId)
        {
            _logger.Log($"Starting order: {orderId}");
            // ... business logic ...
            _logger.Log($"Order {orderId} placed successfully!");
        }
        
        public void CancelOrder(string orderId)
        {
            _logger.LogError($"Order {orderId} was cancelled");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 5: OPERATOR OVERLOADING
    // ═══════════════════════════════════════════════════════════════
    
    public class Money
    {
        public decimal Amount { get; }
        public string Currency { get; }
        
        public Money(decimal amount, string currency)
        {
            Amount = amount;
            Currency = currency;
        }
        
        // Operator overloading - custom behavior for +
        public static Money operator +(Money a, Money b)
        {
            if (a.Currency != b.Currency)
                throw new InvalidOperationException("Cannot add different currencies");
            
            return new Money(a.Amount + b.Amount, a.Currency);
        }
        
        // Operator overloading for -
        public static Money operator -(Money a, Money b)
        {
            if (a.Currency != b.Currency)
                throw new InvalidOperationException("Cannot subtract different currencies");
            
            return new Money(a.Amount - b.Amount, a.Currency);
        }
        
        // Operator overloading for * (scalar)
        public static Money operator *(Money a, decimal multiplier)
        {
            return new Money(a.Amount * multiplier, a.Currency);
        }
        
        // Comparison operators
        public static bool operator >(Money a, Money b) => a.Amount > b.Amount;
        public static bool operator <(Money a, Money b) => a.Amount < b.Amount;
        public static bool operator ==(Money a, Money b) => a.Amount == b.Amount && a.Currency == b.Currency;
        public static bool operator !=(Money a, Money b) => !(a == b);
        
        public override string ToString() => $"{Currency} {Amount:N2}";
        
        public override bool Equals(object obj) => obj is Money m && this == m;
        public override int GetHashCode() => HashCode.Combine(Amount, Currency);
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN PROGRAM
    // ═══════════════════════════════════════════════════════════════
    
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("╔═══════════════════════════════════════════════╗");
            Console.WriteLine("║       POLYMORPHISM DEMONSTRATION              ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 1: Compile-Time Polymorphism (Method Overloading)
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("📌 DEMO 1: Method Overloading (Compile-Time)\n");
            
            var calc = new Calculator();
            
            Console.WriteLine("calc.Add(5, 3):");
            Console.WriteLine($"  Result: {calc.Add(5, 3)}\n");
            
            Console.WriteLine("calc.Add(5.5, 3.3):");
            Console.WriteLine($"  Result: {calc.Add(5.5, 3.3)}\n");
            
            Console.WriteLine("calc.Add(1, 2, 3):");
            Console.WriteLine($"  Result: {calc.Add(1, 2, 3)}\n");
            
            Console.WriteLine("calc.Add(\"Hello, \", \"World!\"):");
            Console.WriteLine($"  Result: {calc.Add("Hello, ", "World!")}\n");
            
            Console.WriteLine("⚡ Compiler decides which method to call based on arguments!\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 2: Runtime Polymorphism (Method Overriding)
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 2: Method Overriding (Runtime)\n");
            
            // Create different shapes
            Shape circle = new Circle(5, "Red");
            Shape rectangle = new Rectangle(4, 6, "Blue");
            Shape triangle = new Triangle(3, 4, 3, 4, 5, "Green");
            
            // Store them in a collection of Shape (base type)
            List<Shape> shapes = new List<Shape> { circle, rectangle, triangle };
            
            Console.WriteLine("Processing different shapes with ONE loop:\n");
            
            foreach (Shape shape in shapes)
            {
                Console.WriteLine("─".PadRight(40, '─'));
                shape.Display();  // Each shape responds differently!
            }
            
            Console.WriteLine("\n⚡ Same method call, different behavior based on actual object type!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 3: The Power of Polymorphism - Calculating Total Area
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 3: Polymorphism in Action\n");
            
            double totalArea = CalculateTotalArea(shapes);
            Console.WriteLine($"Total area of all shapes: {totalArea:F2}\n");
            
            // Add a new shape type - code above STILL WORKS!
            Console.WriteLine("Adding more shapes...");
            shapes.Add(new Circle(3, "Yellow"));
            shapes.Add(new Rectangle(10, 2, "Purple"));
            
            totalArea = CalculateTotalArea(shapes);
            Console.WriteLine($"New total area: {totalArea:F2}\n");
            
            Console.WriteLine("⚡ We added new shapes WITHOUT changing CalculateTotalArea!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 4: Interface Polymorphism
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 4: Interface Polymorphism\n");
            
            decimal orderAmount = 99.99m;
            
            // Different payment methods - all implement IPaymentProcessor
            IPaymentProcessor creditCard = new CreditCardPayment("4532015112830366");
            IPaymentProcessor paypal = new PayPalPayment("user@email.com");
            IPaymentProcessor crypto = new CryptoPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f", "ETH");
            
            Console.WriteLine("Processing same order with different payment methods:\n");
            
            ProcessOrder(creditCard, orderAmount);
            Console.WriteLine();
            ProcessOrder(paypal, orderAmount);
            Console.WriteLine();
            ProcessOrder(crypto, orderAmount);
            
            Console.WriteLine("\n⚡ ProcessOrder works with ANY IPaymentProcessor!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 5: Dependency Injection with Polymorphism
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 5: Real-World Plugin System\n");
            
            Console.WriteLine("Same OrderService, different loggers:\n");
            
            // Inject different loggers
            var consoleService = new OrderService(new ConsoleLogger());
            consoleService.PlaceOrder("ORD-001");
            
            Console.WriteLine();
            
            var fileService = new OrderService(new FileLogger("orders.log"));
            fileService.PlaceOrder("ORD-002");
            
            Console.WriteLine();
            
            var cloudService = new OrderService(new CloudLogger("logs.myapp.com"));
            cloudService.PlaceOrder("ORD-003");
            cloudService.CancelOrder("ORD-003");
            
            Console.WriteLine("\n⚡ OrderService doesn't know or care which logger it uses!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 6: Operator Overloading
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 6: Operator Overloading\n");
            
            var price1 = new Money(100.00m, "USD");
            var price2 = new Money(49.99m, "USD");
            
            Console.WriteLine($"  price1 = {price1}");
            Console.WriteLine($"  price2 = {price2}");
            Console.WriteLine();
            
            var total = price1 + price2;
            Console.WriteLine($"  price1 + price2 = {total}");
            
            var difference = price1 - price2;
            Console.WriteLine($"  price1 - price2 = {difference}");
            
            var doubled = price1 * 2;
            Console.WriteLine($"  price1 * 2 = {doubled}");
            
            Console.WriteLine($"  price1 > price2 = {price1 > price2}");
            Console.WriteLine($"  price1 == price2 = {price1 == price2}");

            // ─────────────────────────────────────────────────────────────
            // KEY TAKEAWAYS
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("🎯 KEY TAKEAWAYS:");
            Console.WriteLine("═══════════════════════════════════════════════════");
            Console.WriteLine("1. COMPILE-TIME: Method overloading (same name, diff params)");
            Console.WriteLine("2. RUNTIME: Method overriding (virtual/override)");
            Console.WriteLine("3. INTERFACE: Multiple classes, same contract");
            Console.WriteLine("4. BENEFIT: Write flexible, extensible code");
            Console.WriteLine("5. BENEFIT: Add new types without changing existing code");
            Console.WriteLine("6. OPERATOR: Custom behavior for +, -, *, etc.");
            Console.WriteLine("═══════════════════════════════════════════════════");

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
        
        // This method works with ANY Shape - that's polymorphism!
        static double CalculateTotalArea(List<Shape> shapes)
        {
            double total = 0;
            foreach (var shape in shapes)
            {
                total += shape.CalculateArea();  // Calls the correct override
            }
            return total;
        }
        
        // This method works with ANY payment processor - that's polymorphism!
        static void ProcessOrder(IPaymentProcessor processor, decimal amount)
        {
            Console.WriteLine($"Using: {processor.GetPaymentMethod()}");
            processor.ProcessPayment(amount);
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
║       POLYMORPHISM DEMONSTRATION              ║
╚═══════════════════════════════════════════════╝

📌 DEMO 1: Method Overloading (Compile-Time)

calc.Add(5, 3):
  → Using Add(int, int)
  Result: 8

calc.Add(5.5, 3.3):
  → Using Add(double, double)
  Result: 8.8

...

📌 DEMO 2: Method Overriding (Runtime)

Processing different shapes with ONE loop:

────────────────────────────────────────
  Shape: Circle
  Color: Red
  Area: 78.54
  Perimeter: 31.42
  Radius: 5
────────────────────────────────────────
  Shape: Rectangle
  Color: Blue
  Area: 24.00
  ...
```

---

## 🧠 Quick Quiz - Test Your Understanding

1. **What's the difference between overloading and overriding?**
   <details>
   <summary>Click for answer</summary>
   - **Overloading**: Same method name, different parameters (compile-time)
   - **Overriding**: Same signature, replace base implementation (runtime)
   </details>

2. **Why can we store a Circle in a Shape variable?**
   <details>
   <summary>Click for answer</summary>
   Because Circle inherits from Shape. A Circle "is a" Shape, so it can be treated as one.
   </details>

3. **When `shape.CalculateArea()` is called, how does C# know which version to execute?**
   <details>
   <summary>Click for answer</summary>
   At runtime, C# checks the actual object type (not the variable type) and calls the appropriate override. This is called "dynamic dispatch" or "late binding."
   </details>

4. **Why is interface polymorphism powerful?**
   <details>
   <summary>Click for answer</summary>
   It allows completely unrelated classes to be used interchangeably as long as they implement the same interface. This enables loose coupling and plugin architectures.
   </details>

---

## 🎨 Polymorphism Decision Chart

```
┌─────────────────────────────────────────────────────────────────┐
│           WHICH TYPE OF POLYMORPHISM TO USE?                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Need same method name with different parameter types?          │
│  └──► METHOD OVERLOADING                                       │
│                                                                 │
│  Need derived classes to customize base class behavior?         │
│  └──► METHOD OVERRIDING (virtual/override)                     │
│                                                                 │
│  Need unrelated classes to share common behavior?               │
│  └──► INTERFACE POLYMORPHISM                                   │
│                                                                 │
│  Need custom +, -, *, ==, etc. for your class?                 │
│  └──► OPERATOR OVERLOADING                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


---
```
gimme an example of operator overloading in c#: 
```csharp
public class Complex
{
    public double Real { get; set; }
    public double Imaginary { get; set; }

    public Complex(double real, double imaginary)
    {
        Real = real;
        Imaginary = imaginary;
    }

    // Overload the + operator
    public static Complex operator +(Complex c1, Complex c2)
    {
        return new Complex(c1.Real + c2.Real, c1.Imaginary + c2.Imaginary);
        // what does it mean c1.Real + c2.Real? It means we are adding the real parts of two complex numbers together, and similarly for the imaginary parts. So if we have two complex numbers, say c1 = 1 + 2i and c2 = 3 + 4i, then c1.Real is 1, c1.Imaginary is 2, c2.Real is 3, and c2.Imaginary is 4. When we add them using the overloaded + operator, we get a new Complex number where the real part is (1 + 3) = 4 and the imaginary part is (2 + 4) = 6, resulting in 4 + 6i.

        // how should we call this method? We can call it using the + operator directly on Complex objects. For example:
        // Complex c1 = new Complex(1, 2);
        // Complex c2 = new Complex(3, 4);
        // Complex sum = c1 + c2;  // Uses overloaded + operator

        // I don't get it: The operator overloading allows us to use the + operator with Complex objects as if it were a built-in type. When we write c1 + c2, C# automatically calls the overloaded + method we defined in the Complex class, which takes two Complex objects as parameters and returns a new Complex object that represents their sum. This way, we can work with Complex numbers in a natural and intuitive way, just like we would with primitive types like int or double.

        // can be done this just via the constructor? No, the constructor is used to create instances of the Complex class, while operator overloading allows us to define how operators like + work with those instances. The constructor initializes the properties of a Complex object, while the overloaded operator defines how two Complex objects interact when we use the + operator. They serve different purposes and are both necessary for creating and manipulating Complex numbers effectively.

        // is it posible to create a method like this with a different name? Yes, we can create a method with a different name to perform the addition of two Complex numbers, but it would not allow us to use the + operator directly. For example, we could define a method like this:
        // public Complex Add(Complex other)
        // {
        //     return new Complex(this.Real + other.Real, this.Imaginary + other.Imaginary);
        // }

        // if this is possible, then why do we need operator overloading? Operator overloading provides a more natural and intuitive way to work with custom types. It allows us to use standard operators (like +, -, *, etc.) directly with our objects, making the code cleaner and easier to read. If we only had a method like Add, we would have to call it explicitly every time we want to add two Complex numbers (e.g., c1.Add(c2)), which can be less convenient and less readable than simply writing c1 + c2. Operator overloading enhances the expressiveness of our code and allows us to use our custom types in a way that feels more like built-in types.

        // how would look like it with the * operator? We can overload the * operator in a similar way to how we overloaded the + operator. For example, if we want to define multiplication of two Complex numbers, we can do it like this:
        // public static Complex operator *(Complex c1, Complex c2)
        // {
        //     double realPart = c1.Real * c2.Real - c1.Imaginary * c2.Imaginary;
        //     double imaginaryPart = c1.Real * c2.Imaginary + c1.Imaginary * c2.Real;
        //     return new Complex(realPart, imaginaryPart);
        // }
    }

    public override string ToString()
    {
        return $"{Real} + {Imaginary}i";
    }
}

class Program
{
    static void Main()
    {
        Complex c1 = new Complex(1, 2);
        Complex c2 = new Complex(3, 4);
        Complex sum = c1 + c2;  // Uses overloaded + operator
        Console.WriteLine(sum);  // Output: 4 + 6i
    }
}
```

## 🏗️ Architectural Benefits

```
┌─────────────────────────────────────────────────────────────────┐
│              WITHOUT POLYMORPHISM (BAD)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  void ProcessPayment(object processor, decimal amount)          │
│  {                                                              │
│      if (processor is CreditCardPayment cc)                    │
│          cc.ProcessCreditCard(amount);                         │
│      else if (processor is PayPalPayment pp)                   │
│          pp.ProcessPayPal(amount);                             │
│      else if (processor is CryptoPayment crypto)               │
│          crypto.ProcessCrypto(amount);                         │
│      // Add new payment? Must modify this method!              │
│  }                                                              │
│                                                                 │
│  ❌ Violates Open/Closed Principle                              │
│  ❌ Every new payment type = code change                        │
│  ❌ Fragile, hard to maintain                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│               WITH POLYMORPHISM (GOOD)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  void ProcessPayment(IPaymentProcessor processor, decimal amt) │
│  {                                                              │
│      processor.ProcessPayment(amt);  // That's it!             │
│  }                                                              │
│                                                                 │
│  ✅ Open for extension, closed for modification                │
│  ✅ Add new payment type = just add new class                  │
│  ✅ Clean, maintainable, testable                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Keywords Summary

| Keyword | Purpose | Example |
|---------|---------|---------|
| `virtual` | Allow method to be overridden | `public virtual void Speak()` |
| `override` | Replace base method implementation | `public override void Speak()` |
| `abstract` | Force derived classes to implement | `public abstract void Draw();` |
| `new` | Hide base method (not polymorphism!) | `public new void Method()` |
| `sealed override` | Override but prevent further overriding | `public sealed override void M()` |

---

## ⚠️ Common Pitfall: `new` vs `override`

```csharp
public class Animal
{
    public virtual void Speak() => Console.WriteLine("Animal speaks");
}

public class Dog : Animal
{
    public override void Speak() => Console.WriteLine("Woof!");  // ✅ Polymorphic
}

public class Cat : Animal
{
    public new void Speak() => Console.WriteLine("Meow!");  // ⚠️ Hides, not polymorphic
}

// Test:
Animal dog = new Dog();
Animal cat = new Cat();

dog.Speak();  // "Woof!"    - override works with polymorphism
cat.Speak();  // "Animal speaks" - new does NOT participate in polymorphism!

Cat actualCat = new Cat();
actualCat.Speak();  // "Meow!" - only works when variable type is Cat
```

---

## ✅ Summary

| Type | Mechanism | Determined At |
|------|-----------|---------------|
| **Overloading** | Same name, different parameters | Compile time |
| **Overriding** | virtual/override keywords | Runtime |
| **Interface** | Multiple classes implement same interface | Runtime |
| **Operators** | Custom +, -, *, etc. | Compile time |

---

## 📚 Next Steps

Once you understand Polymorphism, move on to:
- [ ] **Abstraction** - Hiding complexity
- [ ] **Interfaces vs Abstract Classes** - When to use which
- [ ] **SOLID Principles** - Especially Open/Closed Principle

---

*Happy Learning! 🚀*
