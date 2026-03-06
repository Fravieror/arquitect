# Encapsulation in C#

## 📖 Overview

**Encapsulation** is one of the four fundamental pillars of Object-Oriented Programming (OOP). It's the practice of **bundling data and methods** that operate on that data within a single unit (class), while **restricting direct access** to some of the object's components.

---

## 🎯 What is Encapsulation?

Encapsulation is about:
1. **Hiding internal state** - Keep fields private
2. **Controlling access** - Expose data through properties/methods
3. **Protecting integrity** - Validate data before changes
4. **Reducing coupling** - External code depends on interface, not implementation

### Real-World Analogy

Think of a **car**:
- You interact through the **steering wheel, pedals, gear shift** (public interface)
- You **cannot directly access** the engine internals (private implementation)
- The car **protects itself** - won't start without key, won't shift to reverse at 100mph

---

## 🔐 Access Modifiers in C#

| Modifier | Access Level | Scope |
|----------|--------------|-------|
| `public` | Open | Accessible from anywhere |
| `private` | Restricted | Only within the same class |
| `protected` | Limited | Same class + derived classes |
| `internal` | Assembly | Same assembly/project only |
| `protected internal` | Hybrid | Same assembly OR derived classes |
| `private protected` | Most restricted hybrid | Same assembly AND derived classes |

---

## 🔄 Without vs With Encapsulation

```
WITHOUT ENCAPSULATION (BAD)          WITH ENCAPSULATION (GOOD)
┌─────────────────────────┐          ┌─────────────────────────┐
│ class BankAccount       │          │ class BankAccount       │
│ {                       │          │ {                       │
│   public decimal Balance│          │   private decimal _bal; │
│ }                       │          │                         │
│                         │          │   public decimal Balance│
│ // Anyone can do this:  │          │   {                     │
│ account.Balance = -1000;│          │     get => _bal;        │
│ // Invalid state! 💔    │          │   }                     │
│                         │          │                         │
│                         │          │   public void Deposit() │
│                         │          │   {                     │
│                         │          │     // Validation here  │
│                         │          │   }                     │
│                         │          │ }                       │
│                         │          │                         │
│                         │          │ // Controlled access ✅ │
└─────────────────────────┘          └─────────────────────────┘
```

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

Open your terminal and run:

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n Encapsulation
cd Encapsulation
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;

namespace EncapsulationDemo
{
    // ═══════════════════════════════════════════════════════════════
    // EXAMPLE 1: BAD - No Encapsulation (Don't do this!)
    // ═══════════════════════════════════════════════════════════════
    public class BadBankAccount
    {
        // Public fields - ANYONE can modify directly!
        public string AccountNumber;
        public decimal Balance;
        public string OwnerName;

        // Problems:
        // 1. No validation - balance can be set to negative
        // 2. No control - anyone can change account number
        // 3. No audit trail - changes aren't tracked
    }

    // ═══════════════════════════════════════════════════════════════
    // EXAMPLE 2: GOOD - Proper Encapsulation
    // ═══════════════════════════════════════════════════════════════
    public class BankAccount
    {
        // ─────────────────────────────────────────────────────────────
        // PRIVATE FIELDS - Hidden from outside world
        // ─────────────────────────────────────────────────────────────
        private string _accountNumber;
        private decimal _balance;
        private string _ownerName;
        private readonly List<string> _transactionHistory;

        // ─────────────────────────────────────────────────────────────
        // CONSTRUCTOR - Only way to initialize the account
        // ─────────────────────────────────────────────────────────────
        public BankAccount(string accountNumber, string ownerName, decimal initialDeposit)
        {
            // Validation during creation
            if (string.IsNullOrWhiteSpace(accountNumber))
                throw new ArgumentException("Account number cannot be empty");
            
            if (string.IsNullOrWhiteSpace(ownerName))
                throw new ArgumentException("Owner name cannot be empty");
            
            if (initialDeposit < 0)
                throw new ArgumentException("Initial deposit cannot be negative");

            _accountNumber = accountNumber;
            _ownerName = ownerName;
            _balance = initialDeposit;
            _transactionHistory = new List<string>
            {
                $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Account created with initial deposit: ${initialDeposit:N2}"
            };
        }

        // ─────────────────────────────────────────────────────────────
        // PROPERTIES - Controlled access to private fields
        // ─────────────────────────────────────────────────────────────

        // Read-only property - No setter, cannot be changed
        public string AccountNumber => _accountNumber;

        // Read-only property with getter only
        public decimal Balance
        {
            get { return _balance; }
            // No setter! Balance can only be changed through Deposit/Withdraw
        }

        // Property with validation in setter
        public string OwnerName
        {
            get { return _ownerName; }
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Owner name cannot be empty");
                
                LogTransaction($"Owner name changed from '{_ownerName}' to '{value}'");
                _ownerName = value;
            }
        }

        // Read-only computed property
        public string AccountSummary => $"Account {_accountNumber} | Owner: {_ownerName} | Balance: ${_balance:N2}";

        // ─────────────────────────────────────────────────────────────
        // PUBLIC METHODS - Controlled operations
        // ─────────────────────────────────────────────────────────────

        public bool Deposit(decimal amount)
        {
            // Validation
            if (amount <= 0)
            {
                Console.WriteLine("❌ Deposit amount must be positive");
                return false;
            }

            // Modify internal state
            _balance += amount;
            
            // Track the transaction
            LogTransaction($"Deposited: ${amount:N2} | New Balance: ${_balance:N2}");
            
            Console.WriteLine($"✅ Deposited ${amount:N2}. New balance: ${_balance:N2}");
            return true;
        }

        public bool Withdraw(decimal amount)
        {
            // Validation
            if (amount <= 0)
            {
                Console.WriteLine("❌ Withdrawal amount must be positive");
                return false;
            }

            if (amount > _balance)
            {
                Console.WriteLine($"❌ Insufficient funds. Available: ${_balance:N2}");
                return false;
            }

            // Modify internal state
            _balance -= amount;
            
            // Track the transaction
            LogTransaction($"Withdrew: ${amount:N2} | New Balance: ${_balance:N2}");
            
            Console.WriteLine($"✅ Withdrew ${amount:N2}. New balance: ${_balance:N2}");
            return true;
        }

        public void PrintTransactionHistory()
        {
            Console.WriteLine($"\n📜 Transaction History for {_accountNumber}:");
            Console.WriteLine("─".PadRight(60, '─'));
            foreach (var transaction in _transactionHistory)
            {
                Console.WriteLine($"  {transaction}");
            }
            Console.WriteLine("─".PadRight(60, '─'));
        }

        // ─────────────────────────────────────────────────────────────
        // PRIVATE METHODS - Internal helpers, hidden from outside
        // ─────────────────────────────────────────────────────────────

        private void LogTransaction(string message)
        {
            _transactionHistory.Add($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] {message}");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // EXAMPLE 3: Auto-Implemented Properties (Modern C#)
    // ═══════════════════════════════════════════════════════════════
    public class Person
    {
        // Auto-implemented property with private setter
        public string FirstName { get; private set; }
        
        // Auto-implemented read-only property (set only in constructor)
        public string LastName { get; }
        
        // Auto-implemented with init-only setter (C# 9+)
        public DateTime BirthDate { get; init; }
        
        // Regular auto-property
        public string Email { get; set; }

        // Computed property (no backing field)
        public string FullName => $"{FirstName} {LastName}";
        
        public int Age => DateTime.Now.Year - BirthDate.Year;

        public Person(string firstName, string lastName)
        {
            FirstName = firstName;
            LastName = lastName;  // Can only be set here!
        }

        public void UpdateFirstName(string newName)
        {
            // private set allows internal modification
            FirstName = newName;
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // EXAMPLE 4: Encapsulation with Validation
    // ═══════════════════════════════════════════════════════════════
    public class Temperature
    {
        private double _celsius;

        public double Celsius
        {
            get => _celsius;
            set
            {
                // Validate: can't go below absolute zero
                if (value < -273.15)
                    throw new ArgumentException("Temperature cannot be below absolute zero (-273.15°C)");
                _celsius = value;
            }
        }

        // Computed property - converts from Celsius
        public double Fahrenheit
        {
            get => (_celsius * 9 / 5) + 32;
            set => Celsius = (value - 32) * 5 / 9;  // Converts and validates
        }

        public double Kelvin
        {
            get => _celsius + 273.15;
            set => Celsius = value - 273.15;  // Converts and validates
        }

        public Temperature(double celsius)
        {
            Celsius = celsius;  // Uses property setter for validation
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
            Console.WriteLine("║       ENCAPSULATION DEMONSTRATION             ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 1: Problems WITHOUT Encapsulation
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("📌 WITHOUT Encapsulation (Bad):\n");
            
            var badAccount = new BadBankAccount();
            badAccount.Balance = -5000;        // ❌ Invalid state allowed!
            badAccount.AccountNumber = "";      // ❌ Empty account number!
            badAccount.OwnerName = null;        // ❌ Null owner!
            
            Console.WriteLine($"Bad Account Balance: ${badAccount.Balance}");
            Console.WriteLine("⚠️ Object is in invalid state - no protection!\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 2: Proper Encapsulation
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("─".PadRight(50, '─'));
            Console.WriteLine("📌 WITH Encapsulation (Good):\n");

            var account = new BankAccount("ACC-001", "John Doe", 1000);
            Console.WriteLine(account.AccountSummary);
            
            // Try to directly set balance - WON'T COMPILE!
            // account.Balance = -5000;  // ❌ Error: Balance has no setter
            
            // Try to change account number - WON'T COMPILE!
            // account.AccountNumber = "HACKED";  // ❌ Error: AccountNumber is read-only
            
            Console.WriteLine("\n📌 Controlled Operations:\n");
            
            account.Deposit(500);
            account.Deposit(250);
            account.Withdraw(100);
            account.Withdraw(10000);  // Will fail - insufficient funds
            account.Deposit(-50);      // Will fail - negative amount
            
            account.PrintTransactionHistory();

            // ─────────────────────────────────────────────────────────────
            // DEMO 3: Property Access Levels
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 Property Access Levels:\n");
            
            var person = new Person("Jane", "Smith")
            {
                BirthDate = new DateTime(1990, 5, 15),
                Email = "jane@example.com"
            };
            
            Console.WriteLine($"Full Name: {person.FullName}");
            Console.WriteLine($"Age: {person.Age}");
            Console.WriteLine($"Email: {person.Email}");
            
            // person.FirstName = "Janet";  // ❌ Error: private setter
            person.UpdateFirstName("Janet");  // ✅ OK: through public method
            Console.WriteLine($"Updated Name: {person.FullName}");
            
            // person.LastName = "Jones";  // ❌ Error: no setter at all

            // ─────────────────────────────────────────────────────────────
            // DEMO 4: Validation through Properties
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 Validation through Properties:\n");
            
            var temp = new Temperature(25);
            Console.WriteLine($"Celsius: {temp.Celsius}°C");
            Console.WriteLine($"Fahrenheit: {temp.Fahrenheit}°F");
            Console.WriteLine($"Kelvin: {temp.Kelvin}K");
            
            temp.Fahrenheit = 212;  // Set in Fahrenheit
            Console.WriteLine($"\nAfter setting to 212°F:");
            Console.WriteLine($"Celsius: {temp.Celsius}°C");
            
            try
            {
                temp.Celsius = -300;  // Below absolute zero
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"\n❌ Validation prevented invalid state: {ex.Message}");
            }

            // ─────────────────────────────────────────────────────────────
            // KEY TAKEAWAYS
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("🎯 KEY TAKEAWAYS:");
            Console.WriteLine("═══════════════════════════════════════════════════");
            Console.WriteLine("1. Make fields PRIVATE by default");
            Console.WriteLine("2. Expose data through PROPERTIES with getters/setters");
            Console.WriteLine("3. VALIDATE data in setters to maintain object integrity");
            Console.WriteLine("4. Use READ-ONLY properties for data that shouldn't change");
            Console.WriteLine("5. Provide PUBLIC METHODS for controlled operations");
            Console.WriteLine("6. Keep internal helper methods PRIVATE");
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
║       ENCAPSULATION DEMONSTRATION             ║
╚═══════════════════════════════════════════════╝

📌 WITHOUT Encapsulation (Bad):

Bad Account Balance: $-5000
⚠️ Object is in invalid state - no protection!

──────────────────────────────────────────────────
📌 WITH Encapsulation (Good):

Account ACC-001 | Owner: John Doe | Balance: $1,000.00

📌 Controlled Operations:

✅ Deposited $500.00. New balance: $1,500.00
✅ Deposited $250.00. New balance: $1,750.00
✅ Withdrew $100.00. New balance: $1,650.00
❌ Insufficient funds. Available: $1,650.00
❌ Deposit amount must be positive

📜 Transaction History for ACC-001:
────────────────────────────────────────────────────────────
  [2026-03-05 10:30:00] Account created with initial deposit: $1,000.00
  [2026-03-05 10:30:00] Deposited: $500.00 | New Balance: $1,500.00
  ...
```

---

## 🧠 Quick Quiz - Test Your Understanding

1. **What access modifier should fields typically have?**
   <details>
   <summary>Click for answer</summary>
   `private` - Fields should be private to hide internal state
   </details>

2. **How do you expose private fields safely?**
   <details>
   <summary>Click for answer</summary>
   Through **properties** with `get` and `set` accessors
   </details>

3. **What's the difference between `{ get; }` and `{ get; private set; }`?**
   <details>
   <summary>Click for answer</summary>
   - `{ get; }` - Read-only, can only be set in constructor
   - `{ get; private set; }` - Read-only externally, but can be changed inside the class
   </details>

4. **Why is encapsulation important for architecture?**
   <details>
   <summary>Click for answer</summary>
   - Reduces coupling between components
   - Allows internal implementation to change without affecting clients
   - Ensures objects are always in a valid state
   - Makes code easier to maintain and test
   </details>

---

## 🎨 Property Patterns Quick Reference

```csharp
// 1. Full property with backing field
private string _name;
public string Name
{
    get { return _name; }
    set { _name = value; }
}

// 2. Auto-implemented property
public string Name { get; set; }

// 3. Read-only property (set in constructor only)
public string Name { get; }

// 4. Property with private setter
public string Name { get; private set; }

// 5. Init-only property (C# 9+)
// what does it mean init-only? It means that the property can only be set during object initialization (e.g., in the constructor or through an object initializer) and cannot be modified afterward.
public string Name { get; init; }

// create an example of Init-only with object initializer
var person = new Person { Name = "John Doe" };

// 6. Expression-bodied property (computed)
// can be this updated afterwards? No, expression-bodied properties are read-only and cannot be updated after they are defined. They compute their value based on other data and do not have a setter.
public string FullName => $"{FirstName} {LastName}";

// 7. Property with validation
public int Age
{
    get => _age;
    set => _age = value >= 0 ? value : throw new ArgumentException("Age cannot be negative");
}
```

---

## 🏗️ Architectural Benefits of Encapsulation

```
┌─────────────────────────────────────────────────────────────────┐
│                      WITHOUT ENCAPSULATION                      │
│                                                                 │
│   Client A ─┐                                                   │
│             ├──► Direct access to internal fields               │
│   Client B ─┤    (Tight coupling, fragile code)                │
│             │                                                   │
│   Client C ─┘    If internals change, ALL clients break! 💥    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       WITH ENCAPSULATION                        │
│                                                                 │
│   Client A ─┐      ┌────────────────┐      ┌────────────────┐  │
│             │      │   PUBLIC API   │      │   PRIVATE      │  │
│   Client B ─┼────► │  (Properties,  │ ───► │   INTERNALS    │  │
│             │      │   Methods)     │      │   (Fields)     │  │
│   Client C ─┘      └────────────────┘      └────────────────┘  │
│                                                                 │
│   Internals can change without affecting clients! ✅            │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Summary

| Principle | Implementation |
|-----------|----------------|
| **Hide Data** | Use `private` fields |
| **Control Access** | Use properties with `get`/`set` |
| **Validate Input** | Add logic in property setters |
| **Immutability** | Use `{ get; }` or `{ get; init; }` |
| **Controlled Operations** | Use public methods for complex changes |

---

## 📚 Next Steps

Once you understand Encapsulation, move on to:
- [ ] **Inheritance** - Creating class hierarchies
- [ ] **Polymorphism** - Same interface, different behaviors
- [ ] **Abstraction** - Hiding complexity

---

*Happy Learning! 🚀*
