# Memory Management: Stack vs Heap

Understanding memory management is critical for a senior software architect. This guide covers how Stack and Heap memory work in C#, Go, Python, and JavaScript (React).

---

## Core Concepts

| Aspect | Stack | Heap |
|--------|-------|------|
| **Allocation** | Automatic, fast (LIFO) | Dynamic, slower |
| **Size** | Limited (typically 1-8 MB) | Large (limited by system RAM) |
| **Lifetime** | Scoped to function/block | Until garbage collected or freed |
| **Access** | Direct, very fast | Indirect (via pointer/reference) |
| **Stores** | Value types, local variables, function calls | Objects, reference types, dynamic data |

---

## C# Memory Management

### Key Concepts
- **Value Types** (int, float, struct, bool) → Stored on **Stack**
- **Reference Types** (class, string, arrays) → Object on **Heap**, reference on **Stack**
- **Boxing** → Value type wrapped in object (moves to Heap)
- **Garbage Collection** → Automatic, generational (Gen 0, 1, 2)

### Code to Type

Create a file `MemoryDemo.cs`:

```csharp
using System;

class MemoryDemo
{
    // Struct = Value Type (Stack)
    struct PointStruct
    {
        public int X;
        public int Y;
    }

    // Class = Reference Type (Heap)
    class PointClass
    {
        public int X;
        public int Y;
    }

    static void Main()
    {
        Console.WriteLine("=== C# Memory Management Demo ===\n");

        // STACK: Value types
        int a = 10;           // Stack
        int b = a;            // Copy on Stack (independent)
        b = 20;
        Console.WriteLine($"Value Types (Stack): a={a}, b={b}"); // a=10, b=20

        // STACK: Struct (value type)
        PointStruct ps1 = new PointStruct { X = 1, Y = 2 };
        PointStruct ps2 = ps1;  // Full copy on Stack
        ps2.X = 100;
        Console.WriteLine($"Struct (Stack): ps1.X={ps1.X}, ps2.X={ps2.X}"); // 1, 100

        // HEAP: Class (reference type)
        PointClass pc1 = new PointClass { X = 1, Y = 2 };
        PointClass pc2 = pc1;   // Both point to same Heap object
        pc2.X = 100;
        Console.WriteLine($"Class (Heap): pc1.X={pc1.X}, pc2.X={pc2.X}"); // 100, 100

        // BOXING: Value type moved to Heap
        int num = 42;           // Stack
        object boxed = num;     // Boxing: copied to Heap
        int unboxed = (int)boxed; // Unboxing: copied back
        Console.WriteLine($"Boxing Demo: num={num}, boxed={boxed}");

        // Stack allocation with Span<T> (high-performance)
        Span<int> stackArray = stackalloc int[3] { 1, 2, 3 };
        Console.WriteLine($"stackalloc array: {stackArray[0]}, {stackArray[1]}, {stackArray[2]}");

        // Force Garbage Collection (for demonstration)
        Console.WriteLine($"\nMemory before GC: {GC.GetTotalMemory(false):N0} bytes");
        GC.Collect();
        Console.WriteLine($"Memory after GC: {GC.GetTotalMemory(true):N0} bytes");

        Console.WriteLine("\n=== Key Takeaways ===");
        Console.WriteLine("- Value types (int, struct) live on Stack - fast, copied by value");
        Console.WriteLine("- Reference types (class) live on Heap - shared by reference");
        Console.WriteLine("- Boxing moves value types to Heap (performance cost)");
        Console.WriteLine("- Use 'stackalloc' for performance-critical stack arrays ");
    }
}
```

### Commands to Run

```powershell
# Navigate to memory_management folder
cd memory_management

# Create a new console project
dotnet new console -n CSharpMemory -o csharp

# Copy your code to csharp/Program.cs, then run:
cd csharp
dotnet run
```

---

## Go Memory Management

### Key Concepts
- **Stack** → Local variables, small objects, function parameters
- **Heap** → Escaped variables, large objects, pointers shared across goroutines
- **Escape Analysis** → Compiler decides Stack vs Heap automatically
- **Garbage Collection** → Concurrent, low-latency GC

### Code to Type

Create a file `main.go`:

```go
package main

import (
	"fmt"
	"runtime"
)

// Struct - where it lives depends on escape analysis
type Point struct {
	X, Y int
}

// Returns pointer - Point ESCAPES to Heap
func createOnHeap() *Point {
	p := Point{X: 10, Y: 20} // Escapes to Heap (returned as pointer)
	return &p
}

// Returns value - stays on Stack
func createOnStack() Point {
	p := Point{X: 10, Y: 20} // Stays on Stack (copied on return)
	return p
}

// Modifies via pointer (Heap or Stack, depends on caller)
func modifyPoint(p *Point) {
	p.X = 999
}

func main() {
	fmt.Println("=== Go Memory Management Demo ===\n")

	// STACK: Value types stay on stack
	a := 10
	b := a // Copy
	b = 20
	fmt.Printf("Value copy (Stack): a=%d, b=%d\n", a, b) // 10, 20

	// STACK: Struct by value
	p1 := Point{X: 1, Y: 2}
	p2 := p1 // Full copy
	p2.X = 100
	fmt.Printf("Struct copy (Stack): p1.X=%d, p2.X=%d\n", p1.X, p2.X) // 1, 100

	// HEAP: Pointer returned (escape analysis)
	heapPoint := createOnHeap()
	fmt.Printf("Heap pointer: X=%d, Y=%d\n", heapPoint.X, heapPoint.Y)

	// STACK: Value returned
	stackPoint := createOnStack()
	fmt.Printf("Stack value: X=%d, Y=%d\n", stackPoint.X, stackPoint.Y)

	// Pointer modification
	p3 := Point{X: 5, Y: 5}
	modifyPoint(&p3)
	fmt.Printf("After pointer modify: p3.X=%d\n", p3.X) // 999

	// Slices - backing array on Heap
	slice1 := make([]int, 3) // Heap allocation
	slice1[0] = 1
	slice2 := slice1 // Same backing array (Heap)
	slice2[0] = 999
	fmt.Printf("Slices share Heap: slice1[0]=%d, slice2[0]=%d\n", slice1[0], slice2[0]) // 999, 999

	// Memory stats
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("\nHeap Allocated: %d KB\n", m.HeapAlloc/1024)
	fmt.Printf("Stack In Use: %d KB\n", m.StackInuse/1024)
	fmt.Printf("Num GC cycles: %d\n", m.NumGC)

	fmt.Println("\n=== Key Takeaways ===")
	fmt.Println("- Go uses escape analysis to decide Stack vs Heap")
	fmt.Println("- Returning a pointer forces Heap allocation")
	fmt.Println("- Slices/maps always have backing data on Heap")
	fmt.Println("- Use 'go build -gcflags=-m' to see escape analysis")
}
```

### Commands to Run

```powershell
# Navigate to memory_management folder
cd memory_management

# Create Go module
mkdir go_memory
cd go_memory
go mod init memory_demo

# Create main.go with the code above, then run:
go run main.go

# See escape analysis decisions:
go build -gcflags="-m" main.go
```

---

## Python Memory Management

### Key Concepts
- **Everything is an object** → All stored on Heap (including integers!)
- **Names are references** → Variables are pointers to Heap objects
- **Immutable types** (int, str, tuple) → New object created on modification
- **Reference Counting + Garbage Collection** → Cyclic GC for complex references
- **Interning** → Small integers (-5 to 256) and some strings are cached

### Code to Type

Create a file `memory_demo.py`:

```python
import sys
import gc

print("=== Python Memory Management Demo ===\n")

# Everything is on the Heap - variables are references
a = 10
b = a  # Both point to same object on Heap
print(f"Same object? a is b: {a is b}")  # True (interned integer)
print(f"id(a)={id(a)}, id(b)={id(b)}")

# Integers are immutable - new object created
b = 20
print(f"After b=20: a is b: {a is b}")  # False (different objects)

# Integer interning (-5 to 256)
x = 256
y = 256
print(f"\n256 interned? x is y: {x is y}")  # True

x = 257
y = 257
print(f"257 interned? x is y: {x is y}")  # False (may vary by context)

# Lists are mutable - same Heap object modified
list1 = [1, 2, 3]
list2 = list1  # Same reference
list2.append(4)
print(f"\nLists (same ref): list1={list1}, list2={list2}")  # Both show [1,2,3,4]

# Copy to get independent object
list3 = list1.copy()  # New Heap object
list3.append(5)
print(f"After copy: list1={list1}, list3={list3}")

# Reference counting
class MyClass:
    def __init__(self, name):
        self.name = name
        print(f"  Created: {name}")
    def __del__(self):
        print(f"  Destroyed: {self.name}")

print("\n--- Reference Counting Demo ---")
obj = MyClass("Object1")
print(f"Reference count: {sys.getrefcount(obj) - 1}")  # -1 for getrefcount's ref

ref2 = obj
print(f"After ref2=obj: {sys.getrefcount(obj) - 1}")

del ref2
print(f"After del ref2: {sys.getrefcount(obj) - 1}")

del obj  # Reference count = 0, object destroyed

# Circular reference (needs GC)
print("\n--- Circular Reference Demo ---")
class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

a = Node("NodeA")
b = Node("NodeB")
a.ref = b
b.ref = a  # Circular!

del a
del b
print(f"Unreachable objects before GC: {gc.collect()}")  # GC cleans circular refs

# Memory usage
print("\n--- Memory Sizes ---")
print(f"int: {sys.getsizeof(1)} bytes")
print(f"float: {sys.getsizeof(1.0)} bytes")
print(f"empty list: {sys.getsizeof([])} bytes")
print(f"list [1,2,3]: {sys.getsizeof([1,2,3])} bytes")
print(f"empty dict: {sys.getsizeof({})} bytes")
print(f"string 'hello': {sys.getsizeof('hello')} bytes")

# Slots for memory optimization
print("\n--- __slots__ Optimization ---")
class WithoutSlots:
    def __init__(self):
        self.x = 1
        self.y = 2

class WithSlots:
    __slots__ = ['x', 'y']
    def __init__(self):
        self.x = 1
        self.y = 2

print(f"Without __slots__: {sys.getsizeof(WithoutSlots().__dict__) + sys.getsizeof(WithoutSlots())} bytes")
print(f"With __slots__: {sys.getsizeof(WithSlots())} bytes")

print("\n=== Key Takeaways ===")
print("- Python stores EVERYTHING on the Heap")
print("- Variables are just references (pointers)")
print("- Immutable types create new objects on 'change'")
print("- Reference counting + cyclic GC for cleanup")
print("- Use __slots__ to reduce class memory footprint")
```

### Commands to Run

```powershell
# Navigate to memory_management folder
cd memory_management

# Create Python folder
mkdir python_memory
cd python_memory

# Create memory_demo.py with the code above, then run:
python memory_demo.py
```

---

## JavaScript/React Memory Management

### Key Concepts
- **Primitives** (number, string, boolean, null, undefined, symbol, bigint) → Stack
- **Objects** (arrays, functions, objects) → Heap, reference on Stack
- **Closures** → Capture variables, can cause memory leaks
- **Garbage Collection** → Mark-and-sweep algorithm
- **React Specifics** → useRef, useMemo, useCallback to control allocations

### Code to Type

Create a file `memory_demo.js` (Node.js):

```javascript
console.log("=== JavaScript Memory Management Demo ===\n");

// STACK: Primitives
let a = 10;
let b = a;  // Copy of value
b = 20;
console.log(`Primitives (Stack): a=${a}, b=${b}`);  // 10, 20

// HEAP: Objects (reference copied, not value)
const obj1 = { x: 1, y: 2 };
const obj2 = obj1;  // Same reference
obj2.x = 100;
console.log(`Objects (Heap): obj1.x=${obj1.x}, obj2.x=${obj2.x}`);  // 100, 100

// Clone to get independent copy
const obj3 = { ...obj1 };  // Shallow copy
obj3.x = 999;
console.log(`After spread clone: obj1.x=${obj1.x}, obj3.x=${obj3.x}`);  // 100, 999

// Arrays (Heap)
const arr1 = [1, 2, 3];
const arr2 = arr1;
arr2.push(4);
console.log(`Arrays share reference: arr1=${arr1}, arr2=${arr2}`);

// Strings are immutable (but primitives)
let str1 = "hello";
let str2 = str1;
str2 = "world";
console.log(`Strings (immutable): str1="${str1}", str2="${str2}"`);

// Closure - captures variable (can cause leaks)
function createCounter() {
    let count = 0;  // Captured in closure (stays in memory)
    return function() {
        return ++count;
    };
}

const counter = createCounter();
console.log(`\nClosure counter: ${counter()}, ${counter()}, ${counter()}`);

// Memory leak example (closure holding reference)
function potentialLeak() {
    const largeData = new Array(1000000).fill("data");
    
    // This closure captures largeData even if unused!
    return function() {
        console.log("I exist");
        // largeData still in memory because closure captures it
    };
}

// Proper cleanup
function noLeak() {
    let largeData = new Array(1000000).fill("data");
    const result = largeData.length;
    largeData = null;  // Clear reference
    
    return function() {
        return result;  // Only captures primitive
    };
}

// WeakMap/WeakSet for weak references
console.log("\n--- WeakMap Demo ---");
const weakMap = new WeakMap();
let keyObj = { id: 1 };
weakMap.set(keyObj, "associated data");
console.log(`WeakMap get: ${weakMap.get(keyObj)}`);
keyObj = null;  // Object can now be garbage collected
// weakMap entry will be automatically cleaned up

// Memory usage (Node.js)
const used = process.memoryUsage();
console.log("\n--- Memory Usage (Node.js) ---");
console.log(`Heap Used: ${Math.round(used.heapUsed / 1024)} KB`);
console.log(`Heap Total: ${Math.round(used.heapTotal / 1024)} KB`);
console.log(`External: ${Math.round(used.external / 1024)} KB`);

console.log("\n=== Key Takeaways ===");
console.log("- Primitives on Stack, Objects on Heap");
console.log("- Object assignment copies reference, not value");
console.log("- Closures can cause memory leaks if they capture large objects");
console.log("- Use WeakMap/WeakSet for cache that shouldn't prevent GC");
console.log("- Set references to null when done with large objects");
```

Create a React component `MemoryDemo.jsx`:

```jsx
import React, { useState, useRef, useMemo, useCallback, useEffect } from 'react';

// Memory-optimized React component
function MemoryDemo() {
    const [count, setCount] = useState(0);
    const [items, setItems] = useState([1, 2, 3]);

    // useRef - persists across renders without causing re-render
    // Value stored in .current, object reference stable
    const renderCount = useRef(0);
    renderCount.current += 1;

    // useMemo - memoizes computed value (prevents recalculation)
    // Only recalculates when items changes
    const expensiveSum = useMemo(() => {
        console.log('Computing sum...');
        return items.reduce((a, b) => a + b, 0);
    }, [items]);

    // useCallback - memoizes function reference
    // Prevents new function allocation on every render
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []);  // Empty deps = same function reference always

    // Bad: Creates new function every render
    const badHandleClick = () => {
        setCount(c => c + 1);
    };

    // Bad: Creates new object every render (causes child re-renders)
    const badStyle = { color: 'red' };

    // Good: Memoize objects too
    const goodStyle = useMemo(() => ({ color: 'red' }), []);

    // Cleanup to prevent memory leaks
    useEffect(() => {
        const intervalId = setInterval(() => {
            console.log('tick');
        }, 1000);

        // CRITICAL: Cleanup function prevents memory leak
        return () => {
            clearInterval(intervalId);
        };
    }, []);

    // Cleanup event listeners
    useEffect(() => {
        const handleResize = () => console.log('resize');
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <div>
            <h2>Memory Management in React</h2>
            <p>Render count: {renderCount.current}</p>
            <p>Count: {count}</p>
            <p>Sum (memoized): {expensiveSum}</p>
            
            {/* Good: Stable callback reference */}
            <button onClick={handleClick}>
                Increment (useCallback)
            </button>

            {/* Bad: New function every render */}
            <button onClick={badHandleClick}>
                Increment (bad)
            </button>

            <button onClick={() => setItems([...items, items.length + 1])}>
                Add Item
            </button>

            <h3>Key Takeaways:</h3>
            <ul>
                <li>useRef: Stable reference, doesn't trigger re-render</li>
                <li>useMemo: Cache expensive computations</li>
                <li>useCallback: Stable function references for child props</li>
                <li>Always cleanup intervals/listeners in useEffect return</li>
                <li>Avoid inline objects/functions in JSX when possible</li>
            </ul>
        </div>
    );
}

export default MemoryDemo;
```

### Commands to Run

```powershell
# Navigate to memory_management folder
cd memory_management

# For Node.js demo
mkdir js_memory
cd js_memory
# Create memory_demo.js with the code above
node memory_demo.js

# For React demo (from existing react-training or new project)
cd ../react_memory
npx create-react-app . --template minimal
# Or use existing: cd ../../variables_datatypes_operators/react-training
# Copy MemoryDemo.jsx to src/ and import in App.js
npm start
```

---

## Summary Table

| Language | Stack | Heap | GC Type |
|----------|-------|------|---------|
| **C#** | Value types, struct | Class, arrays, boxed | Generational (Gen 0,1,2) |
| **Go** | Non-escaped locals | Escaped, slices, maps | Concurrent, tri-color |
| **Python** | Nothing* | Everything | Reference counting + Cyclic |
| **JavaScript** | Primitives | Objects, arrays, functions | Mark-and-sweep |

*Python uses a private heap; the "stack" only holds references

---

## Architect-Level Considerations

1. **Performance**: Stack allocation is ~100x faster than Heap
2. **Memory Leaks**: Watch for closures, event listeners, circular references
3. **GC Pauses**: Large heaps = longer GC pauses (affects latency)
4. **Struct vs Class (C#/Go)**: Use value types for small, immutable data
5. **Escape Analysis (Go)**: Profile with `-gcflags=-m` to understand allocations
6. **React Optimization**: useMemo/useCallback prevent unnecessary re-renders
7. **Python**: Use `__slots__` and generators to reduce memory footprint
