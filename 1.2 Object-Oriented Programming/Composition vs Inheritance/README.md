# Composition vs Inheritance in C#

## 📖 Overview

**Composition** and **Inheritance** are two fundamental ways to reuse code and build relationships between classes. Understanding when to use each is a crucial skill for software architects.

> **"Favor composition over inheritance"** - Gang of Four, Design Patterns (1994)

---

## 🎯 The Core Difference

| Aspect | Inheritance | Composition |
|--------|-------------|-------------|
| **Relationship** | "Is-a" | "Has-a" |
| **Coupling** | Tight (compile-time) | Loose (runtime) |
| **Flexibility** | Static | Dynamic |
| **Reuse** | Through class hierarchy | Through object references |
| **Example** | Dog IS AN Animal | Car HAS AN Engine |

---

## 🔄 Visual Comparison

```
═══════════════════════════════════════════════════════════════════
                         INHERITANCE
                         (IS-A relationship)
═══════════════════════════════════════════════════════════════════

                    ┌─────────────┐
                    │   Vehicle   │
                    │─────────────│
                    │ +Start()    │
                    │ +Stop()     │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │     Car     │ │    Boat     │ │   Plane     │
    │─────────────│ │─────────────│ │─────────────│
    │  Car IS A   │ │  Boat IS A  │ │ Plane IS A  │
    │  Vehicle    │ │  Vehicle    │ │ Vehicle     │
    └─────────────┘ └─────────────┘ └─────────────┘


═══════════════════════════════════════════════════════════════════
                         COMPOSITION
                         (HAS-A relationship)
═══════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────┐
    │                          Car                            │
    │─────────────────────────────────────────────────────────│
    │                                                         │
    │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
    │   │ Engine  │  │ Trans-  │  │ Wheels  │  │  GPS    │   │
    │   │         │  │ mission │  │  [4]    │  │ System  │   │
    │   └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
    │                                                         │
    │   Car HAS AN Engine                                     │
    │   Car HAS A Transmission                                │
    │   Car HAS Wheels                                        │
    │   Car HAS A GPS (optional, can be swapped)             │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
```

---

## ⚠️ The Problems with Inheritance

### 1. The Fragile Base Class Problem

```
┌─────────────────────────────────────────────────────────────────┐
│  When you change the base class, ALL derived classes break!    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   class Animal { public virtual void Eat() { ... } }           │
│                  ↓                                              │
│   class Dog : Animal { ... }                                    │
│   class Cat : Animal { ... }                                    │
│   class Bird : Animal { ... }                                   │
│   class Fish : Animal { ... }                                   │
│                                                                 │
│   😱 Change Animal.Eat() → Potentially breaks 100+ classes!    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. The Gorilla-Banana Problem

> "The problem with object-oriented languages is they've got all this implicit environment that they carry around with them. You wanted a banana but what you got was a gorilla holding the banana and the entire jungle." - Joe Armstrong

```
class BananaHolder : Gorilla : Primate : Mammal : Animal : LivingThing
{
    // You just wanted to hold a banana...
    // Now you've inherited 200 methods you don't need!
}
```

### 3. The Diamond Problem (Multiple Inheritance)

```
          ┌─────────┐
          │    A    │
          │ +Fly()  │
          └────┬────┘
        ┌──────┴──────┐
        ▼             ▼
   ┌─────────┐   ┌─────────┐
   │    B    │   │    C    │
   │ +Fly()  │   │ +Fly()  │
   └────┬────┘   └────┬────┘
        └──────┬──────┘
               ▼
          ┌─────────┐
          │    D    │       ❓ Which Fly() does D inherit?
          │ +Fly()?│        C# prevents this with single inheritance
          └─────────┘
```

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n CompositionVsInheritance
cd CompositionVsInheritance
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;
using System.Collections.Generic;

namespace CompositionVsInheritanceDemo
{
    // ═══════════════════════════════════════════════════════════════
    // PART 1: THE PROBLEM WITH INHERITANCE
    // ═══════════════════════════════════════════════════════════════
    
    // Inheritance approach - seems fine at first...
    public class Bird_Inheritance
    {
        public virtual void Eat() => Console.WriteLine("  🐦 Bird is eating");
        public virtual void Fly() => Console.WriteLine("  🐦 Bird is flying");
    }
    
    public class Duck_Inheritance : Bird_Inheritance
    {
        public void Quack() => Console.WriteLine("  🦆 Quack!");
        // Inherits Eat() and Fly() - works fine!
    }
    
    public class Penguin_Inheritance : Bird_Inheritance
    {
        // ❌ PROBLEM: Penguins CAN'T fly, but they inherit Fly()!
        public override void Fly()
        {
            throw new NotSupportedException("Penguins can't fly! 🐧");
        }
        // This violates the Liskov Substitution Principle!
    }
    
    // What if we want a RobotDuck that flies but doesn't eat?
    // Inheritance fails us here - we can't mix and match behaviors!

    // ═══════════════════════════════════════════════════════════════
    // PART 2: COMPOSITION SOLUTION - Behavior Interfaces
    // ═══════════════════════════════════════════════════════════════
    
    // Define BEHAVIORS as interfaces (capabilities)
    public interface IFlyBehavior
    {
        void Fly();
    }
    
    public interface ISwimBehavior
    {
        void Swim();
    }
    
    public interface IQuackBehavior
    {
        void Quack();
    }
    
    // Concrete behavior implementations
    public class FlyWithWings : IFlyBehavior
    {
        public void Fly() => Console.WriteLine("  ✈️ Flying with wings!");
    }
    
    public class FlyNoWay : IFlyBehavior
    {
        public void Fly() => Console.WriteLine("  ❌ Can't fly!");
    }
    
    public class FlyWithRocket : IFlyBehavior
    {
        public void Fly() => Console.WriteLine("  🚀 Flying with rocket boosters!");
    }
    
    public class SwimLikeAFish : ISwimBehavior
    {
        public void Swim() => Console.WriteLine("  🏊 Swimming gracefully!");
    }
    
    public class SwimNoWay : ISwimBehavior
    {
        public void Swim() => Console.WriteLine("  ❌ Can't swim!");
    }
    
    public class QuackLoud : IQuackBehavior
    {
        public void Quack() => Console.WriteLine("  🔊 QUACK QUACK!");
    }
    
    public class QuackSilent : IQuackBehavior
    {
        public void Quack() => Console.WriteLine("  🔇 << silence >>");
    }
    
    public class QuackRobot : IQuackBehavior
    {
        public void Quack() => Console.WriteLine("  🤖 Beep boop quack!");
    }
    
    // Duck with COMPOSITION - behaviors are composed, not inherited
    public class Duck
    {
        public string Name { get; }
        
        // HAS-A relationships (composition)
        private IFlyBehavior _flyBehavior;
        private ISwimBehavior _swimBehavior;
        private IQuackBehavior _quackBehavior;
        
        public Duck(string name, IFlyBehavior fly, ISwimBehavior swim, IQuackBehavior quack)
        {
            Name = name;
            _flyBehavior = fly;
            _swimBehavior = swim;
            _quackBehavior = quack;
        }
        
        // Delegate to composed behaviors
        public void Fly() => _flyBehavior.Fly();
        public void Swim() => _swimBehavior.Swim();
        public void Quack() => _quackBehavior.Quack();
        
        // ✨ KEY BENEFIT: Can change behavior at RUNTIME!
        public void SetFlyBehavior(IFlyBehavior behavior) => _flyBehavior = behavior;
        public void SetQuackBehavior(IQuackBehavior behavior) => _quackBehavior = behavior;
        
        public void Display()
        {
            Console.WriteLine($"\n  🦆 {Name}:");
            Fly();
            Swim();
            Quack();
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 3: REAL-WORLD EXAMPLE - Game Characters
    // ═══════════════════════════════════════════════════════════════
    
    // INHERITANCE APPROACH (Problematic)
    namespace InheritanceApproach
    {
        public class GameCharacter
        {
            public virtual void Attack() => Console.WriteLine("Basic attack");
            public virtual void Move() => Console.WriteLine("Walking");
            public virtual void Speak() => Console.WriteLine("Hello");
        }
        
        public class Warrior : GameCharacter
        {
            public override void Attack() => Console.WriteLine("Sword slash!");
        }
        
        public class Mage : GameCharacter
        {
            public override void Attack() => Console.WriteLine("Fireball!");
        }
        
        // What about a WarriorMage? Can't inherit from both!
        // What about a mute character? Still has Speak()
        // What about a character that can fly later in the game?
    }
    
    // COMPOSITION APPROACH (Flexible)
    namespace CompositionApproach
    {
        // Behavior interfaces
        public interface IAttackStrategy
        {
            void Attack();
            int GetDamage();
        }
        
        public interface IMovementStrategy
        {
            void Move();
            int GetSpeed();
        }
        
        public interface ISpecialAbility
        {
            void UseAbility();
            string GetAbilityName();
        }
        
        // Concrete strategies
        public class SwordAttack : IAttackStrategy
        {
            public void Attack() => Console.WriteLine("  ⚔️ Sword slash!");
            public int GetDamage() => 25;
        }
        
        public class MagicAttack : IAttackStrategy
        {
            public void Attack() => Console.WriteLine("  🔮 Casting spell!");
            public int GetDamage() => 30;
        }
        
        public class BowAttack : IAttackStrategy
        {
            public void Attack() => Console.WriteLine("  🏹 Arrow shot!");
            public int GetDamage() => 20;
        }
        
        public class WalkMovement : IMovementStrategy
        {
            public void Move() => Console.WriteLine("  🚶 Walking...");
            public int GetSpeed() => 5;
        }
        
        public class FlyMovement : IMovementStrategy
        {
            public void Move() => Console.WriteLine("  🦅 Flying!");
            public int GetSpeed() => 15;
        }
        
        public class TeleportMovement : IMovementStrategy
        {
            public void Move() => Console.WriteLine("  ✨ Teleporting!");
            public int GetSpeed() => 100;
        }
        
        public class Fireball : ISpecialAbility
        {
            public void UseAbility() => Console.WriteLine("  🔥 FIREBALL!");
            public string GetAbilityName() => "Fireball";
        }
        
        public class Healing : ISpecialAbility
        {
            public void UseAbility() => Console.WriteLine("  💚 Healing...");
            public string GetAbilityName() => "Heal";
        }
        
        public class Stealth : ISpecialAbility
        {
            public void UseAbility() => Console.WriteLine("  👻 Going invisible...");
            public string GetAbilityName() => "Stealth";
        }
        
        // Character composed of behaviors
        public class Character
        {
            public string Name { get; }
            
            // Composed behaviors (can have multiple abilities!)
            private IAttackStrategy _attackStrategy;
            private IMovementStrategy _movementStrategy;
            private readonly List<ISpecialAbility> _abilities = new();
            
            public Character(string name, IAttackStrategy attack, IMovementStrategy movement)
            {
                Name = name;
                _attackStrategy = attack;
                _movementStrategy = movement;
            }
            
            // Add abilities dynamically
            public void AddAbility(ISpecialAbility ability)
            {
                _abilities.Add(ability);
                Console.WriteLine($"  📚 {Name} learned {ability.GetAbilityName()}!");
            }
            
            // Change strategies at runtime (power-ups, equipment changes)
            public void EquipWeapon(IAttackStrategy newAttack)
            {
                _attackStrategy = newAttack;
                Console.WriteLine($"  🔄 {Name} changed weapon!");
            }
            
            public void LearnMovement(IMovementStrategy newMovement)
            {
                _movementStrategy = newMovement;
                Console.WriteLine($"  🔄 {Name} learned new movement!");
            }
            
            public void Attack() => _attackStrategy.Attack();
            public void Move() => _movementStrategy.Move();
            
            public void UseAllAbilities()
            {
                foreach (var ability in _abilities)
                {
                    ability.UseAbility();
                }
            }
            
            public void ShowStats()
            {
                Console.WriteLine($"\n  ═══════════════════════════════════");
                Console.WriteLine($"  Character: {Name}");
                Console.WriteLine($"  Damage: {_attackStrategy.GetDamage()}");
                Console.WriteLine($"  Speed: {_movementStrategy.GetSpeed()}");
                Console.WriteLine($"  Abilities: {string.Join(", ", _abilities.ConvertAll(a => a.GetAbilityName()))}");
                Console.WriteLine($"  ═══════════════════════════════════");
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 4: AGGREGATION vs COMPOSITION
    // ═══════════════════════════════════════════════════════════════
    
    // Engine - exists independently
    public class Engine
    {
        public int Horsepower { get; }
        public string Type { get; }
        
        public Engine(int hp, string type)
        {
            Horsepower = hp;
            Type = type;
        }
        
        public void Start() => Console.WriteLine($"  🔧 {Type} engine ({Horsepower}hp) started!");
        public void Stop() => Console.WriteLine($"  🔧 {Type} engine stopped.");
    }
    
    // GPS - exists independently
    public class GpsSystem
    {
        public string Provider { get; }
        
        public GpsSystem(string provider)
        {
            Provider = provider;
        }
        
        public void Navigate(string destination)
        {
            Console.WriteLine($"  📍 {Provider} GPS: Navigating to {destination}...");
        }
    }
    
    // Car AGGREGATES Engine and GPS (they can exist independently)
    // Car COMPOSES Wheels (wheels are created with car, destroyed with car)
    public class Car
    {
        public string Model { get; }
        
        // Aggregation - Engine and GPS can exist without Car
        private readonly Engine _engine;
        private GpsSystem _gps;  // Can be null, added later
        
        // Composition - Wheels are part of Car (created/destroyed together)
        private readonly List<Wheel> _wheels;
        
        public Car(string model, Engine engine)
        {
            Model = model;
            _engine = engine;
            
            // Wheels are composed - created with the car
            _wheels = new List<Wheel>
            {
                new Wheel("Front-Left"),
                new Wheel("Front-Right"),
                new Wheel("Rear-Left"),
                new Wheel("Rear-Right")
            };
        }
        
        // GPS is aggregated - can be added/removed anytime
        public void InstallGps(GpsSystem gps)
        {
            _gps = gps;
            Console.WriteLine($"  ✅ GPS installed in {Model}");
        }
        
        public void RemoveGps()
        {
            _gps = null;
            Console.WriteLine($"  ❌ GPS removed from {Model}");
        }
        
        public void Start()
        {
            Console.WriteLine($"\n  🚗 Starting {Model}...");
            _engine.Start();
        }
        
        public void Drive(string destination)
        {
            if (_gps != null)
            {
                _gps.Navigate(destination);
            }
            else
            {
                Console.WriteLine("  ⚠️ No GPS - driving by memory!");
            }
            
            foreach (var wheel in _wheels)
            {
                wheel.Rotate();
            }
            Console.WriteLine($"  🚗 {Model} is moving!");
        }
        
        // Nested class - Wheel only makes sense in context of Car
        private class Wheel
        {
            public string Position { get; }
            public Wheel(string position) => Position = position;
            public void Rotate() => Console.WriteLine($"    🔘 {Position} wheel rotating");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // PART 5: WHEN INHERITANCE IS STILL APPROPRIATE
    // ═══════════════════════════════════════════════════════════════
    
    // Template Method Pattern - inheritance makes sense here
    public abstract class DataProcessor
    {
        // Template method - defines the algorithm skeleton
        public void Process()
        {
            Console.WriteLine("\n  📊 Starting data processing...");
            LoadData();
            TransformData();
            ValidateData();
            SaveData();
            Console.WriteLine("  ✅ Processing complete!");
        }
        
        // Steps that vary - subclasses implement these
        protected abstract void LoadData();
        protected abstract void TransformData();
        protected abstract void SaveData();
        
        // Common step - shared by all
        protected virtual void ValidateData()
        {
            Console.WriteLine("  ✓ Validating data...");
        }
    }
    
    public class CsvProcessor : DataProcessor
    {
        protected override void LoadData() => Console.WriteLine("  📄 Loading CSV file...");
        protected override void TransformData() => Console.WriteLine("  🔄 Parsing CSV rows...");
        protected override void SaveData() => Console.WriteLine("  💾 Saving to database...");
    }
    
    public class JsonProcessor : DataProcessor
    {
        protected override void LoadData() => Console.WriteLine("  📄 Loading JSON file...");
        protected override void TransformData() => Console.WriteLine("  🔄 Parsing JSON objects...");
        protected override void SaveData() => Console.WriteLine("  💾 Saving to NoSQL...");
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN PROGRAM
    // ═══════════════════════════════════════════════════════════════
    
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("╔═══════════════════════════════════════════════╗");
            Console.WriteLine("║    COMPOSITION vs INHERITANCE DEMO            ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // DEMO 1: The Problem with Inheritance
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("📌 DEMO 1: Inheritance Problems\n");
            
            var duck = new Duck_Inheritance();
            duck.Fly();  // Works fine
            
            var penguin = new Penguin_Inheritance();
            try
            {
                penguin.Fly();  // ❌ Throws exception!
            }
            catch (NotSupportedException ex)
            {
                Console.WriteLine($"  ❌ ERROR: {ex.Message}");
            }
            
            Console.WriteLine("\n  ⚠️ Penguin inherits Fly() but can't fly!");
            Console.WriteLine("  ⚠️ This violates Liskov Substitution Principle!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 2: Composition Solution
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 2: Composition Solution\n");
            
            // Different ducks with different behaviors
            var mallard = new Duck("Mallard", new FlyWithWings(), new SwimLikeAFish(), new QuackLoud());
            var penguinDuck = new Duck("Penguin", new FlyNoWay(), new SwimLikeAFish(), new QuackSilent());
            var robotDuck = new Duck("RoboDuck", new FlyWithRocket(), new SwimNoWay(), new QuackRobot());
            
            mallard.Display();
            penguinDuck.Display();
            robotDuck.Display();
            
            // ✨ Change behavior at runtime!
            Console.WriteLine("\n  🔄 Upgrading Mallard with rocket boosters...");
            mallard.SetFlyBehavior(new FlyWithRocket());
            mallard.Display();
            
            Console.WriteLine("\n  ⚡ Composition lets us mix and match behaviors!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 3: Game Character Example
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 3: Game Character (Composition)\n");
            
            using CompositionApproach;
            
            // Create a warrior
            var warrior = new CompositionApproach.Character("Thor", new SwordAttack(), new WalkMovement());
            warrior.AddAbility(new Healing());
            warrior.ShowStats();
            
            warrior.Attack();
            warrior.Move();
            warrior.UseAllAbilities();
            
            // Character evolves during game!
            Console.WriteLine("\n  🎮 Thor levels up and gains new abilities!\n");
            warrior.EquipWeapon(new MagicAttack());    // Found magic sword!
            warrior.LearnMovement(new FlyMovement());   // Learned to fly!
            warrior.AddAbility(new Fireball());         // New spell!
            
            warrior.ShowStats();
            warrior.Attack();
            warrior.Move();
            warrior.UseAllAbilities();
            
            Console.WriteLine("\n  ⚡ Same character, completely different abilities!");
            Console.WriteLine("  ⚡ Impossible with pure inheritance!");

            // ─────────────────────────────────────────────────────────────
            // DEMO 4: Aggregation vs Composition
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 4: Aggregation vs Composition\n");
            
            // Engine exists independently
            var v8Engine = new Engine(450, "V8");
            
            // GPS exists independently  
            var garminGps = new GpsSystem("Garmin");
            
            // Car AGGREGATES engine (engine can exist without car)
            var mustang = new Car("Ford Mustang", v8Engine);
            mustang.Start();
            mustang.Drive("Beach");  // No GPS yet
            
            // Add GPS later (aggregation - loose relationship)
            mustang.InstallGps(garminGps);
            mustang.Drive("Mountains");
            
            // GPS can be moved to another car
            mustang.RemoveGps();
            var camaro = new Car("Chevy Camaro", new Engine(400, "LT1"));
            camaro.InstallGps(garminGps);  // Same GPS in different car!
            camaro.Start();
            camaro.Drive("City");
            
            Console.WriteLine("\n  📝 AGGREGATION: Objects can exist independently");
            Console.WriteLine("  📝 COMPOSITION: Objects live and die together (wheels)");

            // ─────────────────────────────────────────────────────────────
            // DEMO 5: When Inheritance IS Appropriate
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n─".PadRight(50, '─'));
            Console.WriteLine("📌 DEMO 5: When Inheritance Works\n");
            
            Console.WriteLine("Template Method Pattern - algorithm skeleton with variable steps:\n");
            
            DataProcessor csvProcessor = new CsvProcessor();
            csvProcessor.Process();
            
            DataProcessor jsonProcessor = new JsonProcessor();
            jsonProcessor.Process();
            
            Console.WriteLine("\n  ✅ Inheritance works well for:");
            Console.WriteLine("     - Shared algorithm structures");
            Console.WriteLine("     - True 'is-a' relationships");
            Console.WriteLine("     - Framework extension points");

            // ─────────────────────────────────────────────────────────────
            // KEY TAKEAWAYS
            // ─────────────────────────────────────────────────────────────
            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("🎯 KEY TAKEAWAYS:");
            Console.WriteLine("═══════════════════════════════════════════════════");
            Console.WriteLine("1. INHERITANCE: 'Is-a' relationships (Dog is an Animal)");
            Console.WriteLine("2. COMPOSITION: 'Has-a' relationships (Car has an Engine)");
            Console.WriteLine("3. FAVOR COMPOSITION: More flexible, less coupling");
            Console.WriteLine("4. COMPOSITION: Change behavior at runtime");
            Console.WriteLine("5. INHERITANCE: Okay for true hierarchies, templates");
            Console.WriteLine("6. THINK: Would I want to change this at runtime? → Composition");
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
║    COMPOSITION vs INHERITANCE DEMO            ║
╚═══════════════════════════════════════════════╝

📌 DEMO 1: Inheritance Problems

  🐦 Bird is flying
  ❌ ERROR: Penguins can't fly! 🐧

  ⚠️ Penguin inherits Fly() but can't fly!
  ⚠️ This violates Liskov Substitution Principle!

──────────────────────────────────────────────────
📌 DEMO 2: Composition Solution

  🦆 Mallard:
  ✈️ Flying with wings!
  🏊 Swimming gracefully!
  🔊 QUACK QUACK!

  🦆 Penguin:
  ❌ Can't fly!
  🏊 Swimming gracefully!
  🔇 << silence >>
...
```

---

## 🧠 Quick Quiz - Test Your Understanding

1. **When should you use inheritance?**
   <details>
   <summary>Click for answer</summary>
   - True "is-a" relationships (Dog IS AN Animal)
   - Shared algorithm structures (Template Method Pattern)
   - When behavior WON'T change at runtime
   - Framework extension points
   </details>

2. **When should you use composition?**
   <details>
   <summary>Click for answer</summary>
   - "Has-a" relationships (Car HAS AN Engine)
   - When you need to change behavior at runtime
   - When you want to combine multiple behaviors
   - When you want loose coupling
   </details>

3. **What's the Gorilla-Banana problem?**
   <details>
   <summary>Click for answer</summary>
   You inherit more than you need. You wanted a simple behavior but got an entire class hierarchy with hundreds of methods and dependencies you don't want.
   </details>

4. **What's the difference between Aggregation and Composition?**
   <details>
   <summary>Click for answer</summary>
   - **Aggregation**: Parts can exist independently (Engine can exist without Car)
   - **Composition**: Parts live and die with the whole (Wheels destroyed when Car is destroyed)
   </details>

---

## 🎨 Decision Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHEN TO USE WHAT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ASK: "Is this truly a IS-A relationship?"                     │
│  └─► Is a Square truly a Rectangle? (Debatable!)               │
│  └─► Is a Penguin truly a Bird? (Yes, but can't fly!)         │
│                                                                 │
│  ASK: "Will behavior change at runtime?"                       │
│  └─► Yes → COMPOSITION                                         │
│  └─► No  → Either works, but composition is still safer        │
│                                                                 │
│  ASK: "Do I need to combine multiple behaviors?"               │
│  └─► Yes → COMPOSITION (with interfaces)                       │
│  └─► No  → Could use inheritance                               │
│                                                                 │
│  ASK: "Am I building a framework extension point?"             │
│  └─► Yes → Inheritance might be appropriate                    │
│                                                                 │
│  WHEN IN DOUBT: Default to Composition!                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architectural Principle

```
┌─────────────────────────────────────────────────────────────────┐
│              STRATEGY PATTERN (Composition)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐         ┌───────────────────────┐            │
│   │   Context   │────────►│   IStrategy           │            │
│   │             │         │   + Execute()         │            │
│   │ + DoWork()  │         └───────────┬───────────┘            │
│   └─────────────┘                     │                        │
│                          ┌────────────┼────────────┐           │
│                          ▼            ▼            ▼           │
│                    ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│                    │ StratA   │ │ StratB   │ │ StratC   │     │
│                    └──────────┘ └──────────┘ └──────────┘     │
│                                                                 │
│   Context COMPOSES strategy - can swap at runtime!             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Summary

| Aspect | Inheritance | Composition |
|--------|-------------|-------------|
| **Keyword** | `: base class` | `private IComponent` |
| **Relationship** | Is-a | Has-a |
| **Coupling** | Tight | Loose |
| **Flexibility** | Static | Dynamic (runtime) |
| **Reuse** | Forced (all or nothing) | Selective |
| **Testing** | Harder (need whole hierarchy) | Easier (mock components) |
| **Prefer When** | True hierarchies, templates | Most other cases |

---

## 📚 Next Steps

Once you understand Composition vs Inheritance, move on to:
- [ ] **SOLID Principles** - Especially Liskov Substitution & Dependency Inversion
- [ ] **Strategy Pattern** - Composition in action
- [ ] **Decorator Pattern** - Dynamic behavior extension

---

*Happy Learning! 🚀*
