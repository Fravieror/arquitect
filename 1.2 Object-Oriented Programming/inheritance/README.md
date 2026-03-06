# Inheritance in C#

## 📖 Overview

**Inheritance** is one of the four fundamental pillars of Object-Oriented Programming (OOP). It allows a class to **inherit** properties and methods from another class, promoting **code reuse** and establishing a **hierarchical relationship** between classes.

---

## 🎯 What is Inheritance?

Inheritance enables you to:
1. **Reuse code** - Don't repeat common functionality
2. **Extend behavior** - Add new features to existing classes
3. **Create hierarchies** - Model "is-a" relationships
4. **Override behavior** - Customize inherited methods

### Real-World Analogy

Think of **biological inheritance**:
- A **Dog** IS AN **Animal** (Dog inherits from Animal)
- Dog has all Animal traits (breathing, eating) PLUS dog-specific traits (barking)
- A **GermanShepherd** IS A **Dog** IS AN **Animal**

---

## 🔑 Key Terminology

| Term | Description | C# Keyword |
|------|-------------|------------|
| **Base Class** | The class being inherited FROM (parent) | - |
| **Derived Class** | The class that inherits (child) | `:` |
| **Override** | Replace inherited method implementation | `override` |
| **Virtual** | Allow method to be overridden | `virtual` |
| **Sealed** | Prevent further inheritance | `sealed` |
| **Abstract** | Must be implemented by derived class | `abstract` |
| **Base** | Call parent class members | `base` |

---

## 🔄 Inheritance Hierarchy

```
                    ┌─────────────────┐
                    │     Animal      │  ◄── BASE CLASS (Parent)
                    │─────────────────│
                    │ + Name          │
                    │ + Age           │
                    │ + Eat()         │
                    │ + Sleep()       │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │      Dog      │ │      Cat      │ │     Bird      │  ◄── DERIVED CLASSES
    │───────────────│ │───────────────│ │───────────────│
    │ + Breed       │ │ + IsIndoor    │ │ + Wingspan    │
    │ + Bark()      │ │ + Meow()      │ │ + Fly()       │
    │ + Fetch()     │ │ + Scratch()   │ │ + Chirp()     │
    └───────┬───────┘ └───────────────┘ └───────────────┘
            │
            ▼
    ┌───────────────┐
    │ GermanShepherd│  ◄── MULTI-LEVEL INHERITANCE
    │───────────────│
    │ + IsPolice    │
    │ + Guard()     │
    └───────────────┘
```

---

## 🚫 C# Inheritance Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    C# INHERITANCE RULES                         │
├─────────────────────────────────────────────────────────────────┤
│  ✅ Single Inheritance    - One base class only                │
│  ✅ Multi-level           - A : B : C (chain)                  │
│  ✅ Interface Multiple    - Class can implement many interfaces│
│  ❌ Multiple Inheritance  - NOT allowed (no class A : B, C)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

Open your terminal and run:

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n Inheritance
cd Inheritance
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;

namespace InheritanceDemo
{
    // ═══════════════════════════════════════════════════════════════
    // BASE CLASS (Parent)
    // ═══════════════════════════════════════════════════════════════
    public class Animal
    {
        // Properties inherited by all derived classes
        public string Name { get; set; }
        public int Age { get; set; }
        protected string _healthStatus;  // Protected: accessible in derived classes

        // Constructor
        public Animal(string name, int age)
        {
            Name = name;
            Age = age;
            _healthStatus = "Healthy";
            Console.WriteLine($"  📦 Animal constructor called for {name}");
        }

        // Regular method - inherited as-is
        public void Sleep()
        {
            Console.WriteLine($"💤 {Name} is sleeping...");
        }

        // Virtual method - CAN be overridden by derived classes
        public virtual void Eat()
        {
            Console.WriteLine($"🍽️ {Name} is eating.");
        }

        // Virtual method - WILL be overridden
        public virtual void MakeSound()
        {
            Console.WriteLine($"🔊 {Name} makes a sound.");
        }

        // Virtual method with default implementation
        public virtual void DisplayInfo()
        {
            Console.WriteLine($"══════════════════════════════════════");
            Console.WriteLine($"  Name: {Name}");
            Console.WriteLine($"  Age: {Age} years");
            Console.WriteLine($"  Health: {_healthStatus}");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // DERIVED CLASS: Dog (inherits from Animal)
    // ═══════════════════════════════════════════════════════════════
    public class Dog : Animal  // Dog IS AN Animal
    {
        // Additional properties specific to Dog
        public string Breed { get; set; }
        public bool IsTrained { get; set; }

        // Constructor - must call base constructor
        public Dog(string name, int age, string breed) 
            : base(name, age)  // Calls Animal's constructor
        {
            Breed = breed;
            IsTrained = false;
            Console.WriteLine($"  🐕 Dog constructor called for {name}");
        }

        // Override the virtual method
        public override void MakeSound()
        {
            Console.WriteLine($"🐕 {Name} says: WOOF WOOF!");
        }

        // Override Eat with custom behavior
        public override void Eat()
        {
            Console.WriteLine($"🐕 {Name} is eating dog food eagerly!");
        }

        // Override DisplayInfo - extend the base implementation
        public override void DisplayInfo()
        {
            base.DisplayInfo();  // Call parent's implementation first
            Console.WriteLine($"  Breed: {Breed}");
            Console.WriteLine($"  Trained: {(IsTrained ? "Yes" : "No")}");
            Console.WriteLine($"══════════════════════════════════════");
        }

        // New method specific to Dog
        public void Fetch()
        {
            Console.WriteLine($"🎾 {Name} is fetching the ball!");
        }

        public void Train()
        {
            IsTrained = true;
            Console.WriteLine($"📚 {Name} has been trained!");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // DERIVED CLASS: Cat (inherits from Animal)
    // ═══════════════════════════════════════════════════════════════
    public class Cat : Animal
    {
        public bool IsIndoor { get; set; }
        public int LivesRemaining { get; private set; }

        public Cat(string name, int age, bool isIndoor) 
            : base(name, age)
        {
            IsIndoor = isIndoor;
            LivesRemaining = 9;
            Console.WriteLine($"  🐱 Cat constructor called for {name}");
        }

        public override void MakeSound()
        {
            Console.WriteLine($"🐱 {Name} says: MEOW!");
        }

        public override void Eat()
        {
            Console.WriteLine($"🐱 {Name} is eating gracefully...");
        }

        public override void DisplayInfo()
        {
            base.DisplayInfo();
            Console.WriteLine($"  Indoor: {(IsIndoor ? "Yes" : "No")}");
            Console.WriteLine($"  Lives: {LivesRemaining}");
            Console.WriteLine($"══════════════════════════════════════");
        }

        public void Scratch()
        {
            Console.WriteLine($"😼 {Name} scratches the furniture!");
        }

        public void Purr()
        {
            Console.WriteLine($"😻 {Name} is purring contentedly...");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // MULTI-LEVEL INHERITANCE: GermanShepherd : Dog : Animal
    // ═══════════════════════════════════════════════════════════════
    public class GermanShepherd : Dog
    {
        public bool IsPoliceK9 { get; set; }

        public GermanShepherd(string name, int age, bool isPolice) 
            : base(name, age, "German Shepherd")  // Calls Dog's constructor
        {
            IsPoliceK9 = isPolice;
            Console.WriteLine($"  🦮 GermanShepherd constructor called for {name}");
        }

        public override void MakeSound()
        {
            Console.WriteLine($"🦮 {Name} says: WOOF! (deep, authoritative bark)");
        }

        public override void DisplayInfo()
        {
            base.DisplayInfo();  // This calls Dog's DisplayInfo which calls Animal's
            // Note: base.DisplayInfo() already prints the closing line
        }

        public void Guard()
        {
            Console.WriteLine($"🛡️ {Name} is guarding the premises!");
        }

        public void TrackScent()
        {
            Console.WriteLine($"👃 {Name} is tracking a scent...");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // SEALED CLASS - Cannot be inherited
    // ═══════════════════════════════════════════════════════════════
    public sealed class Goldfish : Animal
    {
        public string TankSize { get; set; }

        public Goldfish(string name, int age) : base(name, age)
        {
            TankSize = "10 gallons";
        }

        public override void MakeSound()
        {
            Console.WriteLine($"🐟 {Name} makes bubbles... (fish don't talk!)");
        }

        // Sealed classes CAN still override virtual methods
        public override void Eat()
        {
            Console.WriteLine($"🐟 {Name} nibbles on fish flakes.");
        }
    }

    // This would cause a compile error:
    // public class FancyGoldfish : Goldfish { }  // ❌ Cannot inherit from sealed class

    // ═══════════════════════════════════════════════════════════════
    // ABSTRACT CLASS - Cannot be instantiated, must be inherited
    // ═══════════════════════════════════════════════════════════════
    public abstract class Vehicle
    {
        public string Brand { get; set; }
        public int Year { get; set; }

        protected Vehicle(string brand, int year)
        {
            Brand = brand;
            Year = year;
        }

        // Abstract method - NO implementation, derived classes MUST implement
        public abstract void StartEngine();
        
        // Abstract method
        public abstract void StopEngine();

        // Regular method - inherited as-is
        public void DisplayVehicleInfo()
        {
            Console.WriteLine($"  {Brand} ({Year})");
        }

        // Virtual method - CAN be overridden
        public virtual void Honk()
        {
            Console.WriteLine("🔔 Beep beep!");
        }
    }

    public class Car : Vehicle
    {
        public int NumberOfDoors { get; set; }

        public Car(string brand, int year, int doors) : base(brand, year)
        {
            NumberOfDoors = doors;
        }

        // MUST implement abstract methods
        public override void StartEngine()
        {
            Console.WriteLine($"🚗 {Brand} car engine started: Vroom!");
        }

        public override void StopEngine()
        {
            Console.WriteLine($"🚗 {Brand} car engine stopped.");
        }

        public override void Honk()
        {
            Console.WriteLine($"🚗 {Brand} honks: BEEP BEEP!");
        }
    }

    public class Motorcycle : Vehicle
    {
        public bool HasSidecar { get; set; }

        public Motorcycle(string brand, int year) : base(brand, year)
        {
            HasSidecar = false;
        }

        public override void StartEngine()
        {
            Console.WriteLine($"🏍️ {Brand} motorcycle roars to life: VROOM VROOM!");
        }

        public override void StopEngine()
        {
            Console.WriteLine($"🏍️ {Brand} motorcycle engine off.");
        }

        // Using default Honk() from Vehicle
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN PROGRAM
    // ═══════════════════════════════════════════════════════════════
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("╔═══════════════════════════════════════════════╗");
            Console.WriteLine("║        INHERITANCE DEMONSTRATION              ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 1: Basic Inheritance
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("📌 DEMO 1: Basic Inheritance\n");
            Console.WriteLine("Creating a Dog (inherits from Animal):");
            
            var dog = new Dog("Buddy", 3, "Golden Retriever");
            
            Console.WriteLine("\nDog can use inherited methods:");
            dog.Sleep();           // Inherited from Animal
            dog.Eat();             // Overridden in Dog
            dog.MakeSound();       // Overridden in Dog
            dog.Fetch();           // Dog's own method
            
            Console.WriteLine("\nDog's full info:");
            dog.DisplayInfo();

            // ─────────────────────────────────────────────────────────────
            // DEMO 2: Different Derived Classes
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 2: Different Derived Classes\n");
            
            Console.WriteLine("Creating a Cat:");
            var cat = new Cat("Whiskers", 5, true);
            
            Console.WriteLine("\nComparing behaviors (Polymorphism preview):");
            
            Console.WriteLine("\nDog:");
            dog.MakeSound();
            dog.Eat();
            
            Console.WriteLine("\nCat:");
            cat.MakeSound();
            cat.Eat();
            cat.Purr();

            // ─────────────────────────────────────────────────────────────
            // DEMO 3: Multi-Level Inheritance
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 3: Multi-Level Inheritance\n");
            Console.WriteLine("GermanShepherd → Dog → Animal (3 levels):\n");
            
            var k9 = new GermanShepherd("Rex", 4, true);
            
            Console.WriteLine("\nRex can use methods from ALL ancestor classes:");
            k9.Sleep();        // From Animal
            k9.Eat();          // From Dog
            k9.Fetch();        // From Dog
            k9.MakeSound();    // Overridden in GermanShepherd
            k9.Guard();        // GermanShepherd's own
            k9.TrackScent();   // GermanShepherd's own

            // ─────────────────────────────────────────────────────────────
            // DEMO 4: Constructor Chain
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 4: Constructor Chain\n");
            Console.WriteLine("Watch the constructor order when creating GermanShepherd:\n");
            
            var max = new GermanShepherd("Max", 2, false);
            
            Console.WriteLine("\n↑ Notice: Constructors called from BASE to DERIVED");
            Console.WriteLine("  Animal → Dog → GermanShepherd");

            // ─────────────────────────────────────────────────────────────
            // DEMO 5: Sealed Class
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 5: Sealed Class\n");
            
            var goldie = new Goldfish("Goldie", 1);
            goldie.MakeSound();
            goldie.Eat();
            
            Console.WriteLine("\n⚠️ Goldfish is SEALED - no class can inherit from it");
            Console.WriteLine("   Useful for: security, performance, design intent");

            // ─────────────────────────────────────────────────────────────
            // DEMO 6: Abstract Class
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 6: Abstract Class\n");
            
            // Cannot instantiate abstract class:
            // Vehicle v = new Vehicle("Test", 2024);  // ❌ Compile error
            
            Console.WriteLine("Vehicle is ABSTRACT - cannot be instantiated directly.\n");
            
            var car = new Car("Tesla", 2024, 4);
            var motorcycle = new Motorcycle("Harley", 2023);
            
            Console.WriteLine("Car:");
            car.DisplayVehicleInfo();
            car.StartEngine();
            car.Honk();
            car.StopEngine();
            
            Console.WriteLine("\nMotorcycle:");
            motorcycle.DisplayVehicleInfo();
            motorcycle.StartEngine();
            motorcycle.Honk();  // Uses default from Vehicle
            motorcycle.StopEngine();

            // ─────────────────────────────────────────────────────────────
            // DEMO 7: Treating Derived as Base (Polymorphism Preview)
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n📌 DEMO 7: Using Base Type References\n");
            
            // Can treat derived objects as base type
            Animal animal1 = new Dog("Spot", 2, "Beagle");
            Animal animal2 = new Cat("Luna", 3, false);
            
            Console.WriteLine("\nBoth stored as Animal type, but behavior differs:");
            animal1.MakeSound();  // Calls Dog's override
            animal2.MakeSound();  // Calls Cat's override
            
            // But can't access derived-specific methods without casting:
            // animal1.Fetch();  // ❌ Error: Animal doesn't have Fetch()
            
            // Must cast to access derived-specific members:
            if (animal1 is Dog spotDog)
            {
                spotDog.Fetch();  // ✅ Now we can call Fetch()
            }

            // ─────────────────────────────────────────────────────────────
            // KEY TAKEAWAYS
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("🎯 KEY TAKEAWAYS:");
            Console.WriteLine("═══════════════════════════════════════════════════");
            Console.WriteLine("1. Use `:` to inherit from a base class");
            Console.WriteLine("2. Use `base` to call parent constructors/methods");
            Console.WriteLine("3. Use `virtual` to allow method overriding");
            Console.WriteLine("4. Use `override` to replace inherited behavior");
            Console.WriteLine("5. Use `sealed` to prevent further inheritance");
            Console.WriteLine("6. Use `abstract` for classes that can't be instantiated");
            Console.WriteLine("7. C# supports SINGLE inheritance only (one base class)");
            Console.WriteLine("8. Constructors chain from base → derived");
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
║        INHERITANCE DEMONSTRATION              ║
╚═══════════════════════════════════════════════╝

📌 DEMO 1: Basic Inheritance

Creating a Dog (inherits from Animal):
  📦 Animal constructor called for Buddy
  🐕 Dog constructor called for Buddy

Dog can use inherited methods:
💤 Buddy is sleeping...
🐕 Buddy is eating dog food eagerly!
🐕 Buddy says: WOOF WOOF!
🎾 Buddy is fetching the ball!

Dog's full info:
══════════════════════════════════════
  Name: Buddy
  Age: 3 years
  Health: Healthy
  Breed: Golden Retriever
  Trained: No
══════════════════════════════════════
...
```

---

## 🧠 Quick Quiz - Test Your Understanding

1. **What keyword is used to inherit from a class?**
   <details>
   <summary>Click for answer</summary>
   The colon `:` - Example: `class Dog : Animal`
   </details>

2. **How do you call the parent class constructor?**
   <details>
   <summary>Click for answer</summary>
   Using `base()` - Example: `public Dog(...) : base(name, age)`
   </details>

3. **What's the difference between `virtual` and `abstract`?**
   <details>
   <summary>Click for answer</summary>
   - `virtual` - Has a default implementation, CAN be overridden
   - `abstract` - Has NO implementation, MUST be overridden
   </details>

4. **Can a class inherit from multiple classes in C#?**
   <details>
   <summary>Click for answer</summary>
   No! C# only supports single inheritance. Use interfaces for multiple inheritance-like behavior.
   </details>

5. **What does `sealed` do?**
   <details>
   <summary>Click for answer</summary>
   Prevents a class from being inherited by any other class.
   </details>

---

## 🎨 When to Use Inheritance

```
USE INHERITANCE WHEN:                    DON'T USE WHEN:
────────────────────────────────────     ────────────────────────────────────
✅ "Is-a" relationship exists            ❌ "Has-a" relationship (use composition)
   Dog IS AN Animal                         Car HAS AN Engine
   
✅ Share common behavior                 ❌ Just to reuse code
   All animals eat and sleep                (use composition or utilities)
   
✅ Want polymorphism                     ❌ Deep hierarchies (>3 levels)
   Treat all animals uniformly              (becomes hard to maintain)
   
✅ Extend framework classes              ❌ Multiple inheritance needed
   Custom Exception types                   (use interfaces instead)
```

---

## 🔄 virtual vs override vs new

```csharp
// BASE CLASS
public class Animal
{
    public virtual void Speak() { }      // CAN be overridden
    public void Walk() { }               // Cannot be overridden
}

// DERIVED CLASS
public class Dog : Animal
{
    public override void Speak() { }     // REPLACES base implementation
    public new void Walk() { }           // HIDES base (not recommended)
}

// USAGE
Animal a = new Dog();
a.Speak();   // Calls Dog.Speak() - uses override (polymorphism works)
a.Walk();    // Calls Animal.Walk() - 'new' doesn't participate in polymorphism
```

---

## 🏗️ Architectural Perspective

```
┌─────────────────────────────────────────────────────────────────┐
│                    INHERITANCE BENEFITS                         │
├─────────────────────────────────────────────────────────────────┤
│  ✅ Code Reuse         - Write once, inherit everywhere         │
│  ✅ Polymorphism       - Treat derived as base type            │
│  ✅ Extensibility      - Add features without modifying base   │
│  ✅ Type Safety        - Compiler enforces relationships       │
└─────────────────────────────────────────────────────────────────┘

does in polymorphism a base be treated as a derived? No, in polymorphism, a derived class can be treated as its base class, but not the other way around. For example, you can assign a `Dog` object to an `Animal` variable (because Dog IS AN Animal), but you cannot assign an `Animal` object to a `Dog` variable without an explicit cast (and it will only work if the actual object is a Dog).

┌─────────────────────────────────────────────────────────────────┐
│                    INHERITANCE PITFALLS                         │
├─────────────────────────────────────────────────────────────────┤
│  ⚠️ Tight Coupling     - Changes to base affect all derived    │
│  ⚠️ Fragile Base Class - Hard to change base without breaking  │
│  ⚠️ Deep Hierarchies   - Hard to understand and maintain       │
│  ⚠️ Gorilla Problem    - Inherit more than you need            │
│                                                                 │
│  💡 SOLUTION: Prefer Composition Over Inheritance               │
│     (Next topic: Composition vs Inheritance)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Summary

| Concept | Keyword | Purpose |
|---------|---------|---------|
| Inherit | `:` | `class Dog : Animal` |
| Call parent | `base` | `base.MethodName()` |
| Allow override | `virtual` | Method CAN be overridden |
| Replace method | `override` | Replace inherited method |
| Force implementation | `abstract` | MUST be overridden |
| Prevent inheritance | `sealed` | Cannot be inherited |
| Access in derived | `protected` | Visible in child classes |

---

## 📚 Next Steps

Once you understand Inheritance, move on to:
- [ ] **Polymorphism** - Using base types to work with derived objects
- [ ] **Abstraction** - Hiding complexity behind interfaces
- [ ] **Composition vs Inheritance** - When to use which

---

*Happy Learning! 🚀*
