# Liskov Substitution Principle (LSP) in C#

## Overview

The Liskov Substitution Principle is the **"L"** in SOLID and is arguably the most nuanced of all five principles. As an architect, understanding LSP deeply helps you design inheritance hierarchies that are truly polymorphic and avoid subtle bugs that appear when subclasses don't behave as expected.

Nuanced means that LSP is not just about "is-a" relationships. It's about ensuring that derived classes can be used interchangeably with their base classes without breaking the program's correctness. This means adhering to the same contracts, maintaining invariants, and not introducing unexpected behavior.

---

## 1. The Principle Defined

> **"Objects of a superclass should be replaceable with objects of its subclasses without affecting the correctness of the program."**
>
> — Barbara Liskov, 1987

### In Simple Terms

If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering the desirable properties of the program.

```
If Bird can Fly()
And Penguin is a Bird
Then Penguin should be able to Fly() ← PROBLEM!
```

---

## 2. Why LSP Matters

| Without LSP | With LSP |
|-------------|----------|
| Type checks everywhere (`if (obj is SpecificType)`) | Polymorphism works correctly |
| Unexpected exceptions from overridden methods | Substitutable objects behave predictably |
| Fragile base class problem | Stable inheritance hierarchies |
| Code that "works" but breaks subtly | Reliable, maintainable code |

---

## 3. LSP Rules (Contract Rules)

### 3.1 Preconditions Cannot Be Strengthened

A subclass cannot require MORE than the base class.

```
Base:     void SetAge(int age)  // accepts any int
Derived:  void SetAge(int age)  // throws if age < 0  ← VIOLATION!
```

### 3.2 Postconditions Cannot Be Weakened

A subclass must deliver AT LEAST what the base class promises.

```
Base:     int GetBalance()  // returns positive value
Derived:  int GetBalance()  // might return negative  ← VIOLATION!
```

### 3.3 Invariants Must Be Preserved

Properties that are always true in the base must remain true in derived.

```
Base:     Rectangle.Width > 0 && Rectangle.Height > 0  (always)
Derived:  Square.Width == Square.Height  (must not break rectangle invariant)
```

### 3.4 History Constraint

Subclass cannot modify state in a way the base class doesn't allow.

```
Base:     ImmutablePoint { X, Y }  // cannot change after creation
Derived:  MutablePoint { SetX() }  ← VIOLATION!
```

---

### Hands-On: Project Setup

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n SOLIDPrinciples
cd SOLIDPrinciples
```

Or if you already have it:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\SOLIDPrinciples"
```

---

## 4. Classic LSP Violations

### Exercise 1: The Rectangle-Square Problem

Create a file `RectangleSquareViolation.cs` and type the following:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// CLASSIC LSP VIOLATION: Square is-a Rectangle... or is it?
/// This is the most famous example of LSP violation.
/// </summary>
public static class RectangleSquareViolation
{
    public static void Run()
    {
        Console.WriteLine("=== RECTANGLE-SQUARE PROBLEM ===\n");

        // Using Rectangle directly - works fine
        Rectangle rect = new Rectangle();
        rect.Width = 5;
        rect.Height = 10;
        Console.WriteLine($"Rectangle: {rect.Width} x {rect.Height} = Area {rect.GetArea()}");

        // Using Square as Rectangle - BREAKS!
        Console.WriteLine("\n--- LSP Violation Demo ---");
        Rectangle square = new Square(); // Substituting Square for Rectangle
        SetDimensions(square, 5, 10);
        
        // Expected: 5 x 10 = 50
        // Actual: 10 x 10 = 100 (Square enforces equal sides!)
        Console.WriteLine($"Expected Area: 50, Actual Area: {square.GetArea()}");
        Console.WriteLine($"LSP Violated: {square.GetArea() != 50}");
    }

    // This method expects Rectangle behavior
    static void SetDimensions(Rectangle rect, int width, int height)
    {
        rect.Width = width;
        rect.Height = height;
        
        // This assertion should ALWAYS be true for a Rectangle
        // But Square breaks it!
        Console.WriteLine($"Set {width}x{height}, Got {rect.Width}x{rect.Height}");
    }
}

// Base class
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }

    public int GetArea() => Width * Height;
}

// Derived class - VIOLATES LSP!
public class Square : Rectangle
{
    private int _side;

    public override int Width
    {
        get => _side;
        set => _side = value; // Also changes Height!
    }

    public override int Height
    {
        get => _side;
        set => _side = value; // Also changes Width!
    }
}

// is here the violation that there is not separate variables for width and height? 
// Yes, the violation occurs because the Square class does not maintain separate width and height properties. Instead, it uses a single _side field for both, which breaks the Rectangle's contract that width and height can be set independently.
```

---

### Exercise 2: Fix Rectangle-Square with Composition

Create `RectangleSquareSolution.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// LSP-COMPLIANT SOLUTION: Use composition and interfaces
/// </summary>
public static class RectangleSquareSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== LSP-COMPLIANT SOLUTION ===\n");

        // Both implement IShape - substitutable!
        IShape rectangle = new RectangleShape(5, 10);
        IShape square = new SquareShape(5);

        PrintArea(rectangle); // 50
        PrintArea(square);    // 25

        // Using the factory
        Console.WriteLine("\n--- Using Factory ---");
        var shapes = new List<IShape>
        {
            ShapeFactory.CreateRectangle(4, 6),
            ShapeFactory.CreateSquare(5),
            ShapeFactory.CreateRectangle(3, 3)
        };

        foreach (var shape in shapes)
        {
            PrintArea(shape);
        }
    }

    static void PrintArea(IShape shape)
    {
        Console.WriteLine($"{shape.GetType().Name}: Area = {shape.GetArea()}");
    }
}

// Common interface - defines the CONTRACT
public interface IShape
{
    int GetArea();
}

// Optionally, interface for shapes that can be resized
public interface IResizableShape : IShape
{
    int Width { get; }
    int Height { get; }
    IResizableShape Resize(int width, int height);
}

// Immutable Rectangle - LSP compliant
public class RectangleShape : IResizableShape
{
    public int Width { get; }
    public int Height { get; }

    public RectangleShape(int width, int height)
    {
        if (width <= 0 || height <= 0)
            throw new ArgumentException("Dimensions must be positive");
        
        Width = width;
        Height = height;
    }

    public int GetArea() => Width * Height;

    public IResizableShape Resize(int width, int height)
    {
        return new RectangleShape(width, height);
    }
}

// Immutable Square - LSP compliant
public class SquareShape : IShape
{
    public int Side { get; }

    public SquareShape(int side)
    {
        if (side <= 0)
            throw new ArgumentException("Side must be positive");
        
        Side = side;
    }

    public int GetArea() => Side * Side;
}

// Factory for creating shapes
public static class ShapeFactory
{
    public static IShape CreateRectangle(int width, int height)
        => new RectangleShape(width, height);

    public static IShape CreateSquare(int side)
        => new SquareShape(side);
}
```

---

### Exercise 3: Bird-Penguin Problem

Create `BirdPenguinViolation.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// Another classic: Not all birds can fly!
/// </summary>
public static class BirdPenguinViolation
{
    public static void Run()
    {
        Console.WriteLine("\n=== BIRD-PENGUIN PROBLEM ===\n");

        // This looks reasonable...
        Bird sparrow = new Sparrow();
        Bird penguin = new Penguin();

        Console.WriteLine("Making birds fly:");
        
        MakeBirdFly(sparrow);  // Works!
        MakeBirdFly(penguin);  // THROWS EXCEPTION! LSP VIOLATED!
    }

    static void MakeBirdFly(Bird bird)
    {
        try
        {
            bird.Fly();
            Console.WriteLine($"  {bird.GetType().Name} is flying!");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"  {bird.GetType().Name}: {ex.Message} ← LSP VIOLATION!");
        }
    }
}

// Base class assumes all birds can fly
public abstract class Bird
{
    public abstract void Fly();
}

public class Sparrow : Bird
{
    public override void Fly()
    {
        // Sparrows can fly - no problem
    }
}

// VIOLATES LSP - Throws exception instead of flying
public class Penguin : Bird
{
    public override void Fly()
    {
        throw new InvalidOperationException("Penguins cannot fly!");
    }
}
```

---

### Exercise 4: Fix Bird-Penguin with Interface Segregation

Create `BirdPenguinSolution.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// LSP-COMPLIANT SOLUTION: Separate flying ability into its own interface
/// This also demonstrates ISP (Interface Segregation Principle)
/// </summary>
public static class BirdPenguinSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== LSP-COMPLIANT BIRD SOLUTION ===\n");

        // All birds
        var birds = new List<IBird>
        {
            new SparrowBird(),
            new PenguinBird(),
            new EagleBird()
        };

        Console.WriteLine("All birds can do bird things:");
        foreach (var bird in birds)
        {
            bird.Eat();
            bird.LayEgg();
        }

        // Only flying birds
        Console.WriteLine("\n--- Flying Birds Only ---");
        var flyingBirds = birds.OfType<IFlyingBird>();
        
        foreach (var bird in flyingBirds)
        {
            bird.Fly();
        }

        // Only swimming birds
        Console.WriteLine("\n--- Swimming Birds Only ---");
        var swimmingBirds = birds.OfType<ISwimmingBird>();
        
        foreach (var bird in swimmingBirds)
        {
            bird.Swim();
        }
    }
}

// Base interface - what ALL birds can do
public interface IBird
{
    void Eat();
    void LayEgg();
}

// Capability interfaces
public interface IFlyingBird : IBird
{
    void Fly();
}

public interface ISwimmingBird : IBird
{
    void Swim();
}

// Sparrow: Can fly, cannot swim
public class SparrowBird : IFlyingBird
{
    public void Eat() => Console.WriteLine("  Sparrow eating seeds");
    public void LayEgg() => Console.WriteLine("  Sparrow laying egg");
    public void Fly() => Console.WriteLine("  Sparrow flying through trees");
}

// Penguin: Cannot fly, can swim
public class PenguinBird : ISwimmingBird
{
    public void Eat() => Console.WriteLine("  Penguin eating fish");
    public void LayEgg() => Console.WriteLine("  Penguin laying egg");
    public void Swim() => Console.WriteLine("  Penguin swimming gracefully");
}

// Eagle: Can fly, cannot swim
public class EagleBird : IFlyingBird
{
    public void Eat() => Console.WriteLine("  Eagle eating prey");
    public void LayEgg() => Console.WriteLine("  Eagle laying egg");
    public void Fly() => Console.WriteLine("  Eagle soaring high");
}

// Duck: Can fly AND swim!
public class DuckBird : IFlyingBird, ISwimmingBird
{
    public void Eat() => Console.WriteLine("  Duck eating bread");
    public void LayEgg() => Console.WriteLine("  Duck laying egg");
    public void Fly() => Console.WriteLine("  Duck flying in V-formation");
    public void Swim() => Console.WriteLine("  Duck paddling in pond");
}
```

---

### Exercise 5: Precondition Violation

Create `PreconditionViolation.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// LSP Rule: Preconditions cannot be strengthened in subclass
/// </summary>
public static class PreconditionViolation
{
    public static void Run()
    {
        Console.WriteLine("\n=== PRECONDITION VIOLATION ===\n");

        // Base class works with any positive amount
        BankAccount baseAccount = new BankAccount(1000);
        baseAccount.Withdraw(100);  // Works
        baseAccount.Withdraw(5);    // Works
        Console.WriteLine($"Base Account Balance: {baseAccount.Balance}");

        // Derived class adds restriction - VIOLATES LSP!
        Console.WriteLine("\n--- Premium Account (Strengthened Precondition) ---");
        BankAccount premiumAccount = new PremiumAccount(1000);

        try
        {
            premiumAccount.Withdraw(100);  // Works (>= 100)
            premiumAccount.Withdraw(50);   // FAILS! (< 100 minimum)
        }
        catch (ArgumentException ex)
        {
            Console.WriteLine($"LSP Violation: {ex.Message}");
        }
    }
}

public class BankAccount
{
    public decimal Balance { get; protected set; }

    public BankAccount(decimal initialBalance)
    {
        Balance = initialBalance;
    }

    // Precondition: amount > 0 && amount <= Balance
    public virtual void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Amount must be positive");
        if (amount > Balance)
            throw new InvalidOperationException("Insufficient funds");

        Balance -= amount;
        Console.WriteLine($"  Withdrew {amount:C}, Balance: {Balance:C}");
    }
}

// VIOLATES LSP - Strengthens precondition
public class PremiumAccount : BankAccount
{
    public PremiumAccount(decimal initialBalance) : base(initialBalance) { }

    public override void Withdraw(decimal amount)
    {
        // VIOLATION: Adding new precondition not in base class!
        if (amount < 100)
            throw new ArgumentException("Premium accounts require minimum $100 withdrawal");

        base.Withdraw(amount);
    }
}
```

---

### Exercise 6: Precondition Fix

Create `PreconditionSolution.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// LSP-COMPLIANT: Don't strengthen preconditions
/// </summary>
public static class PreconditionSolution
{
    public static void Run()
    {
        Console.WriteLine("\n=== LSP-COMPLIANT PRECONDITIONS ===\n");

        // Using composition and explicit interface
        IWithdrawable regularAccount = new RegularBankAccount(1000);
        IWithdrawable premiumWithMin = new MinimumWithdrawalAccount(1000, minimumAmount: 100);

        // Client code knows what to expect based on the interface
        ProcessWithdrawal(regularAccount, 50);   // Works
        ProcessWithdrawal(regularAccount, 100);  // Works

        Console.WriteLine("\n--- Minimum Withdrawal Account ---");
        Console.WriteLine($"Minimum withdrawal: {((MinimumWithdrawalAccount)premiumWithMin).MinimumWithdrawal:C}");
        ProcessWithdrawal(premiumWithMin, 50);   // Client can check minimum first
        ProcessWithdrawal(premiumWithMin, 100);  // Works
    }

    static void ProcessWithdrawal(IWithdrawable account, decimal amount)
    {
        // Client can check constraints before calling
        if (account is IHasMinimumWithdrawal minAccount && amount < minAccount.MinimumWithdrawal)
        {
            Console.WriteLine($"  Skipping {amount:C} - below minimum {minAccount.MinimumWithdrawal:C}");
            return;
        }

        if (account.CanWithdraw(amount))
        {
            account.Withdraw(amount);
        }
        else
        {
            Console.WriteLine($"  Cannot withdraw {amount:C}");
        }
    }
}

// Core interface
public interface IWithdrawable
{
    decimal Balance { get; }
    bool CanWithdraw(decimal amount);
    void Withdraw(decimal amount);
}

// Optional capability interface
public interface IHasMinimumWithdrawal
{
    decimal MinimumWithdrawal { get; }
}

// Regular account - no minimum
public class RegularBankAccount : IWithdrawable
{
    public decimal Balance { get; private set; }

    public RegularBankAccount(decimal initialBalance)
    {
        Balance = initialBalance;
    }

    public bool CanWithdraw(decimal amount) => amount > 0 && amount <= Balance;

    public void Withdraw(decimal amount)
    {
        if (!CanWithdraw(amount))
            throw new InvalidOperationException("Cannot withdraw");

        Balance -= amount;
        Console.WriteLine($"  Withdrew {amount:C}, Balance: {Balance:C}");
    }
}

// Account with minimum - uses composition, not inheritance
public class MinimumWithdrawalAccount : IWithdrawable, IHasMinimumWithdrawal
{
    private readonly RegularBankAccount _innerAccount;
    public decimal MinimumWithdrawal { get; }

    public decimal Balance => _innerAccount.Balance;

    public MinimumWithdrawalAccount(decimal initialBalance, decimal minimumAmount)
    {
        _innerAccount = new RegularBankAccount(initialBalance);
        MinimumWithdrawal = minimumAmount;
    }

    // CanWithdraw includes our minimum check
    public bool CanWithdraw(decimal amount) =>
        amount >= MinimumWithdrawal && _innerAccount.CanWithdraw(amount);

    public void Withdraw(decimal amount)
    {
        if (!CanWithdraw(amount))
            throw new InvalidOperationException($"Minimum withdrawal is {MinimumWithdrawal:C}");

        _innerAccount.Withdraw(amount);
    }
}
```

---

### Exercise 7: Postcondition Violation

Create `PostconditionViolation.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// LSP Rule: Postconditions cannot be weakened in subclass
/// </summary>
public static class PostconditionViolation
{
    public static void Run()
    {
        Console.WriteLine("\n=== POSTCONDITION VIOLATION ===\n");

        // Base class guarantees sorted output
        DataProcessor baseProcessor = new DataProcessor();
        var baseResult = baseProcessor.Process(new[] { 5, 2, 8, 1, 9 });
        Console.WriteLine($"Base processor: [{string.Join(", ", baseResult)}]");
        Console.WriteLine($"Is sorted: {IsSorted(baseResult)}");

        // Derived class BREAKS the guarantee - VIOLATES LSP!
        Console.WriteLine("\n--- Violated Postcondition ---");
        DataProcessor brokenProcessor = new FilteringProcessor();
        var brokenResult = brokenProcessor.Process(new[] { 5, 2, 8, 1, 9 });
        Console.WriteLine($"Filtering processor: [{string.Join(", ", brokenResult)}]");
        Console.WriteLine($"Is sorted: {IsSorted(brokenResult)} ← VIOLATION if false!");
    }

    static bool IsSorted(IEnumerable<int> items)
    {
        var list = items.ToList();
        for (int i = 1; i < list.Count; i++)
        {
            if (list[i] < list[i - 1]) return false;
        }
        return true;
    }
}

public class DataProcessor
{
    // POSTCONDITION: Returns items in sorted order
    public virtual IEnumerable<int> Process(int[] items)
    {
        return items.OrderBy(x => x);
    }
}

// VIOLATES LSP - Weakens postcondition (doesn't guarantee sorted)
public class FilteringProcessor : DataProcessor
{
    public override IEnumerable<int> Process(int[] items)
    {
        // Filters but doesn't sort - BREAKS postcondition!
        return items.Where(x => x > 3);
    }
}
```

---

### Exercise 8: Real-World Example - File Storage

Create `FileStorageExample.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// Real-world LSP example: File storage abstraction
/// </summary>
public static class FileStorageExample
{
    public static void Run()
    {
        Console.WriteLine("\n=== FILE STORAGE - REAL WORLD LSP ===\n");

        // All implementations are substitutable
        var storages = new List<IFileStorage>
        {
            new LocalFileStorage("/tmp/local"),
            new CloudFileStorage("my-bucket"),
            new InMemoryFileStorage()
        };

        foreach (var storage in storages)
        {
            TestStorage(storage);
        }
    }

    static void TestStorage(IFileStorage storage)
    {
        Console.WriteLine($"--- {storage.GetType().Name} ---");

        string testFile = "test.txt";
        string content = "Hello, LSP!";

        // All operations work consistently regardless of implementation
        storage.Write(testFile, content);
        
        if (storage.Exists(testFile))
        {
            string read = storage.Read(testFile);
            Console.WriteLine($"  Written and read: '{read}'");
            
            storage.Delete(testFile);
            Console.WriteLine($"  Deleted. Exists: {storage.Exists(testFile)}");
        }
        Console.WriteLine();
    }
}

// Contract: defines what ALL file storage implementations must do
public interface IFileStorage
{
    void Write(string path, string content);
    string Read(string path);
    bool Exists(string path);
    void Delete(string path);
}

// Optional capability: some storages support listing
public interface IListableStorage : IFileStorage
{
    IEnumerable<string> List(string directory);
}

// Local file system implementation
public class LocalFileStorage : IListableStorage
{
    private readonly string _basePath;
    private readonly Dictionary<string, string> _files = new(); // Simulated

    public LocalFileStorage(string basePath)
    {
        _basePath = basePath;
    }

    public void Write(string path, string content)
    {
        _files[GetFullPath(path)] = content;
    }

    public string Read(string path)
    {
        var fullPath = GetFullPath(path);
        if (!_files.TryGetValue(fullPath, out var content))
            throw new FileNotFoundException($"File not found: {path}");
        return content;
    }

    public bool Exists(string path) => _files.ContainsKey(GetFullPath(path));

    public void Delete(string path) => _files.Remove(GetFullPath(path));

    public IEnumerable<string> List(string directory) =>
        _files.Keys.Where(k => k.StartsWith(GetFullPath(directory)));

    private string GetFullPath(string path) => Path.Combine(_basePath, path);
}

// Cloud storage implementation - fully substitutable
public class CloudFileStorage : IFileStorage
{
    private readonly string _bucket;
    private readonly Dictionary<string, string> _objects = new(); // Simulated

    public CloudFileStorage(string bucket)
    {
        _bucket = bucket;
    }

    public void Write(string path, string content)
    {
        _objects[$"{_bucket}/{path}"] = content;
    }

    public string Read(string path)
    {
        var key = $"{_bucket}/{path}";
        if (!_objects.TryGetValue(key, out var content))
            throw new FileNotFoundException($"Object not found: {path}");
        return content;
    }

    public bool Exists(string path) => _objects.ContainsKey($"{_bucket}/{path}");

    public void Delete(string path) => _objects.Remove($"{_bucket}/{path}");
}

// In-memory implementation - great for testing, fully substitutable
public class InMemoryFileStorage : IFileStorage
{
    private readonly Dictionary<string, string> _store = new();

    public void Write(string path, string content) => _store[path] = content;
    
    public string Read(string path)
    {
        if (!_store.TryGetValue(path, out var content))
            throw new FileNotFoundException($"Not found: {path}");
        return content;
    }

    public bool Exists(string path) => _store.ContainsKey(path);
    
    public void Delete(string path) => _store.Remove(path);
}
```

---

### Exercise 9: LSP Detection Checklist

Create `LSPChecklist.cs`:

```csharp
namespace SOLIDPrinciples.LSP;

/// <summary>
/// Practical checklist for detecting LSP violations in code reviews
/// </summary>
public static class LSPChecklist
{
    public static void Run()
    {
        Console.WriteLine("\n=== LSP VIOLATION DETECTION CHECKLIST ===\n");

        Console.WriteLine("🔍 CODE SMELLS that indicate LSP violations:\n");

        Console.WriteLine("1. TYPE CHECKING in client code:");
        Console.WriteLine("   ❌ if (animal is Dog) { ... } else if (animal is Cat) { ... }");
        Console.WriteLine("   ✅ animal.MakeSound(); // polymorphic behavior\n");

        Console.WriteLine("2. EMPTY METHOD implementations:");
        Console.WriteLine("   ❌ override void Fly() { /* do nothing */ }");
        Console.WriteLine("   ✅ Don't inherit IFlyable if you can't fly\n");

        Console.WriteLine("3. THROWING EXCEPTIONS for valid base operations:");
        Console.WriteLine("   ❌ override void Save() => throw new NotSupportedException();");
        Console.WriteLine("   ✅ Use different interface for read-only vs read-write\n");

        Console.WriteLine("4. BREAKING INVARIANTS:");
        Console.WriteLine("   ❌ Square.SetWidth() also changes Height");
        Console.WriteLine("   ✅ Use composition or separate interfaces\n");

        Console.WriteLine("5. DOCUMENTATION that says 'except when':");
        Console.WriteLine("   ❌ 'All birds can fly, except penguins'");
        Console.WriteLine("   ✅ Separate IFlyingBird from IBird\n");

        // Demonstrate detection
        Console.WriteLine("\n--- Live Detection Demo ---\n");
        DetectLSPViolation();
    }

    static void DetectLSPViolation()
    {
        // This code has a hidden LSP violation
        var items = new List<CollectionItem>
        {
            new MutableItem { Value = "Changeable" },
            new ImmutableItem { Value = "Fixed" }  // LSP violation waiting to happen
        };

        Console.WriteLine("Trying to modify all items:");
        foreach (var item in items)
        {
            try
            {
                item.Modify("New Value");
                Console.WriteLine($"  {item.GetType().Name}: Modified successfully");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"  {item.GetType().Name}: {ex.Message} ← LSP VIOLATION!");
            }
        }

        Console.WriteLine("\n✅ SOLUTION: Use IReadableItem and IModifiableItem interfaces");
    }
}

// Base class
public abstract class CollectionItem
{
    public string Value { get; set; } = "";
    public abstract void Modify(string newValue);
}

// Works as expected
public class MutableItem : CollectionItem
{
    public override void Modify(string newValue)
    {
        Value = newValue;
    }
}

// VIOLATES LSP - throws instead of modifying
public class ImmutableItem : CollectionItem
{
    public override void Modify(string newValue)
    {
        throw new InvalidOperationException("Cannot modify immutable item");
    }
}
```

---

## 5. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using SOLIDPrinciples.LSP;

Console.WriteLine("╔═══════════════════════════════════════════════════════════════╗");
Console.WriteLine("║   LISKOV SUBSTITUTION PRINCIPLE (LSP) - ARCHITECT TRAINING    ║");
Console.WriteLine("╚═══════════════════════════════════════════════════════════════╝");

RectangleSquareViolation.Run();
RectangleSquareSolution.Run();
BirdPenguinViolation.Run();
BirdPenguinSolution.Run();
PreconditionViolation.Run();
PreconditionSolution.Run();
PostconditionViolation.Run();
FileStorageExample.Run();
LSPChecklist.Run();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌─────────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ LSP COMPLIANCE CHECKLIST:                                       │");
Console.WriteLine("├─────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ ✅ Subclass can handle ALL inputs parent accepts               │");
Console.WriteLine("│ ✅ Subclass returns COMPATIBLE outputs                         │");
Console.WriteLine("│ ✅ Subclass maintains ALL parent invariants                    │");
Console.WriteLine("│ ✅ Subclass doesn't throw unexpected exceptions                │");
Console.WriteLine("│ ✅ Subclass doesn't have empty/no-op overrides                 │");
Console.WriteLine("│ ✅ No type checking needed in client code                      │");
Console.WriteLine("├─────────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ WHEN IN DOUBT:                                                  │");
Console.WriteLine("│ • Prefer COMPOSITION over inheritance                          │");
Console.WriteLine("│ • Use INTERFACES for capabilities                              │");
Console.WriteLine("│ • Apply INTERFACE SEGREGATION to separate behaviors            │");
Console.WriteLine("│ • Make objects IMMUTABLE when possible                         │");
Console.WriteLine("│ • Use FACTORIES to encapsulate object creation                 │");
Console.WriteLine("└─────────────────────────────────────────────────────────────────┘");
```

---

## 6. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\SOLIDPrinciples"
dotnet run
```

---

## 7. Architect's Cheat Sheet

### LSP Rules Summary

| Rule | Meaning | Example |
|------|---------|---------|
| **Preconditions** | Derived cannot require MORE | Base accepts any age, derived can't require age > 18 |
| **Postconditions** | Derived must deliver AT LEAST | If base returns sorted, derived must also sort |
| **Invariants** | Must stay TRUE | Rectangle width/height independent |
| **History** | Cannot allow missing mutations | Immutable object can't have setter in derived |

### Design Patterns That Help

```
1. COMPOSITION over Inheritance
   Instead of: Square extends Rectangle
   Use: Square has a Side, Rectangle has Width & Height

2. INTERFACE SEGREGATION
   Instead of: Bird.Fly() throws for Penguin
   Use: IFlyingBird, ISwimmingBird interfaces

3. STRATEGY PATTERN
   Instead of: Overriding behavior with exceptions
   Use: Inject different strategies

4. TEMPLATE METHOD
   Instead of: Allowing broken overrides
   Use: Final template with customizable steps

5. FACTORY PATTERN
   Instead of: new Square() as Rectangle
   Use: ShapeFactory.CreateSquare()
```

### Testing for LSP

```csharp
// Write tests that run against the BASE type
// but use DERIVED implementations
[Theory]
[InlineData(typeof(LocalFileStorage))]
[InlineData(typeof(CloudFileStorage))]
[InlineData(typeof(InMemoryFileStorage))]
public void AllStorages_ShouldBehaveIdentically(Type storageType)
{
    IFileStorage storage = (IFileStorage)Activator.CreateInstance(storageType)!;
    
    // Same test should pass for ALL implementations
    storage.Write("test.txt", "content");
    Assert.True(storage.Exists("test.txt"));
    Assert.Equal("content", storage.Read("test.txt"));
}
```

---

## 8. Common Interview Questions

### Q1: What is LSP in simple terms?

**Answer**: "If S is a subtype of T, then anywhere you use T, you should be able to use S without breaking the program. In other words, derived classes must be substitutable for their base classes."

### Q2: Why is Square/Rectangle a violation?

**Answer**: "Because when you set width and height independently on a Square (as you can on a Rectangle), the Square enforces that both dimensions are equal. This breaks the Rectangle's contract that width and height are independent properties."

### Q3: How do you fix LSP violations?

**Answer**: 
1. Use composition instead of inheritance
2. Define capability interfaces (IFlyable, ISwimmable)
3. Make objects immutable
4. Use the Template Method pattern. what is the template method pattern?The Template Method pattern is a design pattern that defines the skeleton of an algorithm in a base class, allowing subclasses to override specific steps without changing the overall structure. It promotes code reuse and helps maintain LSP compliance by preventing subclasses from breaking the algorithm's contract.

exmle:

```csharp
public abstract class DataProcessor
{
    // Template method - final, cannot be overridden
    public void ProcessData()
    {
        LoadData();
        TransformData();
        SaveData();
    }

    protected abstract void LoadData();
    protected abstract void TransformData();
    protected abstract void SaveData();
}

```
5. Apply Interface Segregation

### Q4: What's the relationship between LSP and OCP?

**Answer**: "LSP is about substitutability in inheritance hierarchies. OCP is about extension without modification. They work together: LSP ensures your extensions (new subclasses) work correctly, while OCP ensures you can add them without changing existing code."

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **LSP Core** | Subtypes must be substitutable for base types |
| **Preconditions** | Derived cannot strengthen (require more) |
| **Postconditions** | Derived cannot weaken (deliver less) |
| **Invariants** | Must be preserved in derived classes |
| **Type Checks** | If you need `is` or `as`, likely LSP violation |
| **Empty Methods** | No-op overrides signal design flaw |
| **Solution** | Composition + Interface Segregation |

---

**Next Step**: Move to **Interface Segregation Principle (ISP)** when ready!
