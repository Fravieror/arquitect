# Classes and Objects in C#

## 📖 Overview

Understanding the difference and relationship between **Classes** and **Objects** is fundamental to Object-Oriented Programming (OOP).

---

## 🎯 Key Concepts

### What is a Class?

A **Class** is a **blueprint** or **template** that defines:
- **Data** (fields/properties) - what data the object holds
- **Behavior** (methods) - what actions the object can perform

Think of a class as an **architectural plan** for a house - it describes what the house will look like, but it's not a house itself.

### What is an Object?

An **Object** is a **concrete instance** of a class. It's the actual "thing" created from the blueprint.

Using the house analogy: the object is the **actual house** built from the architectural plan.

---

## 🔄 Class vs Object: The Difference

| Aspect | Class | Object |
|--------|-------|--------|
| **Definition** | Blueprint/Template | Instance of a class |
| **Memory** | No memory allocated | Memory allocated on heap |
| **Creation** | Defined using `class` keyword | Created using `new` keyword |
| **Quantity** | Only one definition | Multiple objects from same class |
| **Nature** | Logical entity | Physical entity (exists in memory) |
| **Example** | `Car` (the concept) | `myCar` (a specific car) |

---

## 🔗 The Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                         CLASS                               │
│                    (Blueprint/Template)                     │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Fields:    string Brand, string Model, int Year    │   │
│   │  Methods:   Start(), Stop(), Accelerate()           │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ new Car()
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │  OBJECT 1   │     │  OBJECT 2   │     │  OBJECT 3   │
   │  (myCar)    │     │  (yourCar)  │     │  (herCar)   │
   │             │     │             │     │             │
   │ Brand:"BMW" │     │ Brand:"Audi"│     │ Brand:"Ford"│
   │ Model:"X5"  │     │ Model:"A4"  │     │ Model:"F150"│
   │ Year: 2024  │     │ Year: 2023  │     │ Year: 2022  │
   └─────────────┘     └─────────────┘     └─────────────┘
```

**Relationship Summary:**
- A **Class** defines the structure
- An **Object** is an instantiation of that structure
- One class → Many objects
- Objects are independent (changing one doesn't affect others)

---

## 💻 Hands-On Practice

### Step 1: Create a New Console Project

Open your terminal and run:

```powershell
cd c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp
dotnet new console -n ClassesAndObjects
cd ClassesAndObjects
```

### Step 2: Type the Following Code

Open `Program.cs` and replace all content with:

```csharp
using System;

namespace ClassesAndObjects
{
    // ═══════════════════════════════════════════════════════════════
    // THIS IS A CLASS - The Blueprint
    // ═══════════════════════════════════════════════════════════════
    public class Car
    {
        // FIELDS (Data the object holds)
        public string Brand;
        public string Model;
        public int Year;
        private bool _isRunning;  // Private - only accessible inside the class

        // CONSTRUCTOR (Special method to initialize objects)
        public Car(string brand, string model, int year)
        {
            Brand = brand;
            Model = model;
            Year = year;
            _isRunning = false;
        }

        // METHODS (Behavior/Actions)
        public void Start()
        {
            if (!_isRunning)
            {
                _isRunning = true;
                Console.WriteLine($"🚗 {Brand} {Model} engine started!");
            }
            else
            {
                Console.WriteLine($"⚠️ {Brand} {Model} is already running.");
            }
        }

        public void Stop()
        {
            if (_isRunning)
            {
                _isRunning = false;
                Console.WriteLine($"🛑 {Brand} {Model} engine stopped.");
            }
            else
            {
                Console.WriteLine($"⚠️ {Brand} {Model} is not running.");
            }
        }

        public void DisplayInfo()
        {
            Console.WriteLine($"══════════════════════════════════════");
            Console.WriteLine($"Brand: {Brand}");
            Console.WriteLine($"Model: {Model}");
            Console.WriteLine($"Year:  {Year}");
            Console.WriteLine($"Running: {(_isRunning ? "Yes" : "No")}");
            Console.WriteLine($"══════════════════════════════════════");
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // MAIN PROGRAM - Where we create OBJECTS from the CLASS
    // ═══════════════════════════════════════════════════════════════
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("╔═══════════════════════════════════════════════╗");
            Console.WriteLine("║     CLASSES AND OBJECTS DEMONSTRATION         ║");
            Console.WriteLine("╚═══════════════════════════════════════════════╝\n");

            // ─────────────────────────────────────────────────────────────
            // CREATING OBJECTS (Instances of the Car class)
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("📌 Creating objects from the Car class...\n");
            
            // Object 1: myCar is an INSTANCE (object) of the Car CLASS
            Car myCar = new Car("BMW", "X5", 2024);
            
            // Object 2: yourCar is ANOTHER INSTANCE of the same Car CLASS
            Car yourCar = new Car("Audi", "A4", 2023);
            
            // Object 3: herCar is YET ANOTHER INSTANCE
            Car herCar = new Car("Ford", "F-150", 2022);

            // ─────────────────────────────────────────────────────────────
            // DEMONSTRATING THAT OBJECTS ARE INDEPENDENT
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("📌 Each object has its own data:\n");
            
            myCar.DisplayInfo();
            yourCar.DisplayInfo();
            herCar.DisplayInfo();

            // ─────────────────────────────────────────────────────────────
            // USING OBJECT METHODS
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("\n📌 Using methods on individual objects:\n");
            
            myCar.Start();       // Only myCar starts
            yourCar.Start();     // yourCar starts independently
            
            myCar.Start();       // Try to start again (already running)
            
            myCar.Stop();        // Stop myCar
            
            Console.WriteLine();
            herCar.DisplayInfo(); // herCar was never started

            // ─────────────────────────────────────────────────────────────
            // KEY INSIGHT: SAME CLASS, DIFFERENT DATA
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("\n📌 Key Insight:");
            Console.WriteLine("   - Car is the CLASS (blueprint)");
            Console.WriteLine("   - myCar, yourCar, herCar are OBJECTS (instances)");
            Console.WriteLine("   - Each object holds its own data");
            Console.WriteLine("   - Changing one object does NOT affect others");

            // ─────────────────────────────────────────────────────────────
            // PROVING OBJECTS ARE SEPARATE IN MEMORY
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("\n📌 Proving objects are independent:\n");
            
            // Modify myCar
            myCar.Brand = "Tesla";
            myCar.Model = "Model S";
            myCar.Year = 2025;
            
            Console.WriteLine("After changing myCar to Tesla Model S 2025:\n");
            
            Console.WriteLine("myCar:");
            myCar.DisplayInfo();
            
            Console.WriteLine("yourCar (unchanged):");
            yourCar.DisplayInfo();

            // ─────────────────────────────────────────────────────────────
            // REFERENCE VS VALUE
            // ─────────────────────────────────────────────────────────────
            
            Console.WriteLine("\n📌 Reference Behavior:\n");
            
            Car anotherReference = myCar;  // anotherReference points to SAME object as myCar
            anotherReference.Brand = "Modified";
            
            Console.WriteLine("After changing brand through anotherReference:");
            Console.WriteLine($"myCar.Brand = {myCar.Brand}");         // Also shows "Modified"!
            Console.WriteLine($"anotherReference.Brand = {anotherReference.Brand}");
            Console.WriteLine("\n⚡ Both variables reference the SAME object in memory!");

            Console.WriteLine("\n═══════════════════════════════════════════════════");
            Console.WriteLine("End of demonstration. Press any key to exit...");
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
║     CLASSES AND OBJECTS DEMONSTRATION         ║
╚═══════════════════════════════════════════════╝

📌 Creating objects from the Car class...

══════════════════════════════════════
Brand: BMW
Model: X5
Year:  2024
Running: No
══════════════════════════════════════
══════════════════════════════════════
Brand: Audi
Model: A4
Year:  2023
Running: No
══════════════════════════════════════
══════════════════════════════════════
Brand: Ford
Model: F-150
Year:  2022
Running: No
══════════════════════════════════════

📌 Using methods on individual objects:

🚗 BMW X5 engine started!
🚗 Audi A4 engine started!
⚠️ BMW X5 is already running.
🛑 BMW X5 engine stopped.
...
```

---

## 🧠 Quick Quiz - Test Your Understanding

After running the code, answer these questions:

1. **How many classes are defined in the code?**
   <details>
   <summary>Click for answer</summary>
   One: the `Car` class (Program is also a class but it's the entry point)
   </details>

2. **How many objects are created?**
   <details>
   <summary>Click for answer</summary>
   Three: `myCar`, `yourCar`, `herCar`
   </details>

3. **What keyword creates an object from a class?**
   <details>
   <summary>Click for answer</summary>
   The `new` keyword: `Car myCar = new Car(...)`
   </details>

4. **If you change `myCar.Brand`, does `yourCar.Brand` change?**
   <details>
   <summary>Click for answer</summary>
   No! Each object has its own copy of data.
   </details>

5. **Why did `anotherReference.Brand = "Modified"` also change `myCar.Brand`?**
   <details>
   <summary>Click for answer</summary>
   Because `anotherReference` and `myCar` reference the SAME object in memory. No new object was created.
   </details>

---

## 🎯 Memory Visualization

```
STACK                          HEAP
┌─────────────────┐            ┌──────────────────────────────┐
│ myCar           │ ────────►  │ Car Object                   │
│ (reference)     │            │ Brand: "BMW"                 │
├─────────────────┤            │ Model: "X5"                  │
│ yourCar         │ ────────►  │ Year: 2024                   │
│ (reference)     │ ──┐        └──────────────────────────────┘
├─────────────────┤   │        ┌──────────────────────────────┐
│ herCar          │ ──│─────►  │ Car Object                   │
│ (reference)     │   │        │ Brand: "Audi"                │
└─────────────────┘   │        │ Model: "A4"                  │
                      │        │ Year: 2023                   │
                      │        └──────────────────────────────┘
                      │        ┌──────────────────────────────┐
                      └─────►  │ Car Object                   │
                               │ Brand: "Ford"                │
                               │ Model: "F-150"               │
                               │ Year: 2022                   │
                               └──────────────────────────────┘
```

**Key Points:**
- Variables on the **Stack** hold **references** (memory addresses)
- Actual objects live on the **Heap** what is the heap? The heap is a region of memory used for dynamic allocation. When you create an object using `new`, it is allocated on the heap, and the variable holds a reference to that memory location.
- Multiple variables can reference the same object

when the garbage collector runs, it will free memory for objects that are no longer referenced by any variable.
it means GC goes first to the stack to check which variables are still in scope and then checks the heap for objects that are still referenced. If an object on the heap is not referenced by any variable on the stack, it becomes eligible for garbage collection.

**Q&A?**
are the variables on the stack garbage collected? No, variables on the stack are automatically managed and are not garbage collected. They are created when a method is called and destroyed when the method exits. The garbage collector only manages memory on the heap where objects are stored.

so the first generation of GC is for the heap, not the stack. The stack is managed by the runtime and does not require garbage collection. the second generation of GC is for the heap, not the stack. The stack is managed by the runtime and does not require garbage collection. the third generation of GC is for the heap, not the stack. The stack is managed by the runtime and does not require garbage collection.

---

## ✅ Summary

| Concept | Class | Object |
|---------|-------|--------|
| **What it is** | Template/Blueprint | Instance of template |
| **Keyword** | `class` | `new` |
| **Lives in** | Code (definition) | Memory (runtime) |
| **Count** | One definition | Many instances |
| **Analogy** | Cookie cutter | Cookies made from it |

---

## 📚 Next Steps

Once you understand Classes and Objects, move on to:
- [ ] **Encapsulation** - Hiding internal data
- [ ] **Inheritance** - Creating class hierarchies
- [ ] **Polymorphism** - Same interface, different behaviors

---

*Happy Learning! 🚀*
