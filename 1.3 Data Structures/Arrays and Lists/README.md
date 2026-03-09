# Arrays and Lists in C#

## Overview

As a software architect, understanding the fundamental differences between arrays and lists is critical for making informed decisions about memory allocation, performance, and API design.

---

## 1. Arrays

### What is an Array?

An array is a **fixed-size**, **contiguous block of memory** that stores elements of the same type. Once created, its size cannot change.

### Key Characteristics

| Property | Value |
|----------|-------|
| Size | Fixed at creation |
| Memory | Contiguous allocation |
| Access Time | O(1) - constant |
| Insert/Delete | O(n) - requires new array |
| Namespace | `System` |

---

### Hands-On: Create a Console Project

Open your terminal and run:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n DataStructures
cd DataStructures
```

---

### Exercise 1: Array Fundamentals

Create a file `ArrayBasics.cs` and type the following:

```csharp
namespace DataStructures;

public class ArrayBasics
{
    public static void Run()
    {
        Console.WriteLine("=== ARRAY FUNDAMENTALS ===\n");

        // 1. Declaration and Initialization
        int[] numbers = new int[5];           // Default values (0)
        int[] primes = { 2, 3, 5, 7, 11 };    // Inline initialization
        int[] squares = new int[] { 1, 4, 9, 16, 25 };

        // 2. Accessing Elements - O(1) time complexity
        Console.WriteLine($"First prime: {primes[0]}");
        Console.WriteLine($"Last prime: {primes[^1]}");  // Index from end (C# 8+)

        // 3. Modifying Elements
        numbers[0] = 10;
        numbers[1] = 20;
        Console.WriteLine($"Modified: {string.Join(", ", numbers)}");

        // 4. Array Length (fixed!)
        Console.WriteLine($"Array length: {primes.Length}");

        // 5. Iterating
        Console.WriteLine("\nIterating with foreach:");
        foreach (var prime in primes)
        {
            Console.Write($"{prime} ");
        }

        // 6. Iterating with index
        Console.WriteLine("\n\nIterating with for loop:");
        for (int i = 0; i < primes.Length; i++)
        {
            Console.WriteLine($"Index {i}: {primes[i]}");
        }
    }
}
```

---

### Exercise 2: Multi-Dimensional Arrays

Add a new file `MultiDimensionalArrays.cs`:

```csharp
namespace DataStructures;

public class MultiDimensionalArrays
{
    public static void Run()
    {
        Console.WriteLine("\n=== MULTI-DIMENSIONAL ARRAYS ===\n");

        // 1. 2D Array (Matrix) - Rectangular
        int[,] matrix = new int[3, 3]
        {
            { 1, 2, 3 },
            { 4, 5, 6 },
            { 7, 8, 9 }
        };

        Console.WriteLine("2D Matrix:");
        for (int row = 0; row < matrix.GetLength(0); row++)
        {
            for (int col = 0; col < matrix.GetLength(1); col++)
            {
                Console.Write($"{matrix[row, col]} ");
            }
            Console.WriteLine();
        }

        // 2. Jagged Array (Array of Arrays) - Can have different lengths
        int[][] jaggedArray = new int[3][];
        jaggedArray[0] = new int[] { 1, 2 };
        jaggedArray[1] = new int[] { 3, 4, 5, 6 };
        jaggedArray[2] = new int[] { 7 };

        Console.WriteLine("\nJagged Array:"); // what does it mean jagged array? A jagged array is an array of arrays, where each inner array can have a different length, allowing for more flexible data structures compared to multi-dimensional arrays which require a rectangular shape.
        for (int i = 0; i < jaggedArray.Length; i++)
        {
            Console.WriteLine($"Row {i}: [{string.Join(", ", jaggedArray[i])}]");
        }

        // ARCHITECT TIP: Jagged arrays are more flexible and often
        // perform better due to better cache locality in certain scenarios
    }
}
```

---

### Exercise 3: Array Methods & LINQ

Add `ArrayOperations.cs`:

```csharp
namespace DataStructures;

public class ArrayOperations
{
    public static void Run()
    {
        Console.WriteLine("\n=== ARRAY OPERATIONS ===\n");

        int[] numbers = { 64, 34, 25, 12, 22, 11, 90 };

        // 1. Array.Sort - In-place sorting O(n log n)
        int[] sortedCopy = (int[])numbers.Clone();
        Array.Sort(sortedCopy);
        // which algorithm does Array.Sort use? It uses a hybrid of QuickSort, HeapSort, and InsertionSort called Introspective Sort (Introsort).
        // is it more efficient than a simple QuickSort? Yes, because it avoids worst-case scenarios of QuickSort by switching to HeapSort when recursion depth exceeds a certain level, and it uses InsertionSort for small partitions, which is more efficient for small arrays.
        Console.WriteLine($"Sorted: {string.Join(", ", sortedCopy)}");

        // 2. Array.Reverse
        Array.Reverse(sortedCopy);
        // which algorithm does Array.Reverse use? It uses a simple two-pointer approach to swap elements from the start and end of the array until they meet in the middle.
        // is it more efficient than a simple for loop? No, it is essentially the same algorithm as a for loop that swaps elements, but it is optimized and implemented in native code, so it may perform better than a naive implementation in C#.
        Console.WriteLine($"Reversed: {string.Join(", ", sortedCopy)}");

        // 3. Array.Find - Returns first match
        int[] original = { 64, 34, 25, 12, 22, 11, 90 };
        int firstEven = Array.Find(original, x => x % 2 == 0);
        // is this more efficient than a simple for loop? No, it is essentially the same algorithm as a for loop that checks each element against the condition, but it is optimized and implemented in native code, so it may perform better than a naive implementation in C#.
        Console.WriteLine($"First even: {firstEven}");

        // 4. Array.FindAll - Returns all matches
        int[] allEvens = Array.FindAll(original, x => x % 2 == 0);
        // is this more efficient than a simple for loop? No, it is essentially the same algorithm as a for loop that checks each element against the condition, but it is optimized and implemented in native code, so it may perform better than a naive implementation in C#.
        Console.WriteLine($"All evens: {string.Join(", ", allEvens)}");

        // 5. Array.IndexOf
        int index = Array.IndexOf(original, 25);
        Console.WriteLine($"Index of 25: {index}");

        // 6. Array.BinarySearch (requires sorted array!)
        Array.Sort(original);
        int binaryIndex = Array.BinarySearch(original, 25);
        Console.WriteLine($"Binary search for 25: index {binaryIndex}");

        // 7. Array.Resize - Creates NEW array (expensive!)
        int[] resizable = { 1, 2, 3 };
        Console.WriteLine($"\nBefore resize: Length = {resizable.Length}");
        Array.Resize(ref resizable, 5);
        Console.WriteLine($"After resize: Length = {resizable.Length}");
        Console.WriteLine($"Contents: {string.Join(", ", resizable)}");

        // ARCHITECT WARNING: Array.Resize creates a new array and copies
        // all elements. This is O(n) and should be avoided in hot paths.
    }
}
```

---

## 2. Lists (List<T>)

### What is a List?

`List<T>` is a **dynamic array** that automatically resizes. It's the most commonly used collection in C#.

### Key Characteristics

| Property | Value |
|----------|-------|
| Size | Dynamic (auto-resizes) |
| Memory | Contiguous (with capacity buffer) |
| Access Time | O(1) - constant |
| Add at End | O(1) amortized |
| Insert/Delete | O(n) - shifts elements |
| Namespace | `System.Collections.Generic` |

---

### Exercise 4: List Fundamentals

Create `ListBasics.cs`:

```csharp
namespace DataStructures;

public class ListBasics
{
    public static void Run()
    {
        Console.WriteLine("\n=== LIST FUNDAMENTALS ===\n");

        // 1. Creating Lists
        List<int> emptyList = new();                    // Empty list
        List<int> numbers = new() { 1, 2, 3, 4, 5 };   // Collection initializer
        List<string> names = new(100);                  // With initial capacity

        // 2. Adding Elements
        numbers.Add(6);                    // Add at end - O(1) amortized
        numbers.AddRange(new[] { 7, 8 }); // Add multiple, how look like numbers after this? [1, 2, 3, 4, 5, 6, 7, 8]   
        numbers.Insert(0, 0);             // Insert at index - O(n), how look like numbers after this? [0, 1, 2, 3, 4, 5, 6, 7, 8]

        Console.WriteLine($"After adding: {string.Join(", ", numbers)}");

        // 3. Accessing Elements - O(1)
        Console.WriteLine($"First: {numbers[0]}");
        Console.WriteLine($"Last: {numbers[^1]}");

        // 4. Count vs Capacity
        Console.WriteLine($"\nCount: {numbers.Count}");
        Console.WriteLine($"Capacity: {numbers.Capacity}");

        // 5. Removing Elements
        numbers.Remove(5);           // Remove first occurrence - O(n), how look like numbers after this? [0, 1, 2, 3, 4, 6, 7, 8]
        numbers.RemoveAt(0);         // Remove at index - O(n), how look like numbers after this? [1, 2, 3, 4, 6, 7, 8]
        numbers.RemoveAll(x => x > 7); // Remove all matching - O(n), how look like numbers after this? [1, 2, 3, 4, 6, 7]

        Console.WriteLine($"After removing: {string.Join(", ", numbers)}");

        // 6. Checking Elements
        bool contains = numbers.Contains(3);  // O(n) which is the value of contains? true
        int index = numbers.IndexOf(4);       // O(n) which is the value of index? 3
        bool exists = numbers.Exists(x => x > 5); // O(n) which is the value of exists? true

        Console.WriteLine($"\nContains 3: {contains}");
        Console.WriteLine($"Index of 4: {index}");
        Console.WriteLine($"Exists > 5: {exists}");
    }
}
```

---

### Exercise 5: List Performance & Capacity

Create `ListPerformance.cs`:

```csharp
using System.Diagnostics;

namespace DataStructures;

public class ListPerformance
{
    public static void Run()
    {
        Console.WriteLine("\n=== LIST PERFORMANCE ===\n");

        // ARCHITECT INSIGHT: Understanding capacity prevents unnecessary allocations

        // 1. Without initial capacity (multiple reallocations)
        var sw = Stopwatch.StartNew();
        List<int> listWithoutCapacity = new();
        for (int i = 0; i < 1_000_000; i++)
        {
            listWithoutCapacity.Add(i);
        }
        // is not an error of sintax 1_000_000? No, it is a valid numeric literal in C# that uses underscores for readability. It represents the integer value 1000000.
        sw.Stop();
        Console.WriteLine($"Without capacity: {sw.ElapsedMilliseconds}ms");
        // is this more efficient than pre-allocating? No, because it causes multiple reallocations and copying of elements as the list grows, which can significantly degrade performance, especially for large lists.

        // 2. With initial capacity (single allocation)
        sw.Restart();
        List<int> listWithCapacity = new(1_000_000);
        for (int i = 0; i < 1_000_000; i++)
        {
            listWithCapacity.Add(i);
        }
        sw.Stop();
        Console.WriteLine($"With capacity: {sw.ElapsedMilliseconds}ms");
        // is this more efficient than not pre-allocating? Yes, because it allocates the necessary memory upfront, avoiding the overhead of multiple reallocations and copying as the list grows, resulting in significantly better performance for large lists.

        // 3. Demonstrating capacity growth
        Console.WriteLine("\n--- Capacity Growth Pattern ---");
        List<int> demo = new();
        int lastCapacity = 0;
        for (int i = 0; i < 100; i++)
        {
            demo.Add(i);
            if (demo.Capacity != lastCapacity)
            {
                Console.WriteLine($"Count: {demo.Count}, Capacity: {demo.Capacity}");
                lastCapacity = demo.Capacity;
            }
        }

        // 4. TrimExcess to free memory
        demo.TrimExcess(); // what does TrimExcess do? It reduces the capacity of the list to match its current count, effectively freeing any unused memory that was allocated for future growth. a simple examplo of an array with capacity 16 and count 10, after calling TrimExcess, the capacity would be reduced to 10, which is the current count of elements in the list.

        // [ARCHITECT TIP] Use TrimExcess when you know the list won't grow anymore to free up memory.
        Console.WriteLine($"\nAfter TrimExcess - Count: {demo.Count}, Capacity: {demo.Capacity}");
    }
}
```

---

### Exercise 6: List vs Array Performance Comparison

Create `PerformanceComparison.cs`:

```csharp
using System.Diagnostics;

namespace DataStructures;

public class PerformanceComparison
{
    private const int Size = 10_000_000;
    private const int Iterations = 100;

    public static void Run()
    {
        Console.WriteLine("\n=== ARRAY vs LIST PERFORMANCE ===\n");

        // Test 1: Sequential Access
        int[] array = new int[Size];
        List<int> list = new(Size);
        for (int i = 0; i < Size; i++)
        {
            array[i] = i;
            list.Add(i);
        }

        // Array sequential read
        var sw = Stopwatch.StartNew();
        long sum = 0;
        for (int iter = 0; iter < Iterations; iter++)
        {
            for (int i = 0; i < array.Length; i++)
            {
                sum += array[i];
            }
        }
        sw.Stop();
        Console.WriteLine($"Array sequential read: {sw.ElapsedMilliseconds}ms");

        // List sequential read
        sw.Restart();
        sum = 0;
        for (int iter = 0; iter < Iterations; iter++)
        {
            for (int i = 0; i < list.Count; i++)
            {
                sum += list[i];
            }
        }
        sw.Stop();
        Console.WriteLine($"List sequential read: {sw.ElapsedMilliseconds}ms");

        // which is more efficient for sequential access? The array is generally more efficient for sequential access due to better cache locality and less overhead compared to the list, which has additional metadata and potential for resizing.

        // what does it mean overhead in this context? Overhead refers to the additional memory and processing time required by the list to manage its dynamic resizing, capacity, and other features compared to the fixed-size array, which has a simpler structure and direct memory access.

        // Test 2: Random Access
        Random rnd = new(42);
        int[] indices = new int[1000];
        for (int i = 0; i < indices.Length; i++)
        {
            indices[i] = rnd.Next(Size);
        }

        sw.Restart();
        for (int iter = 0; iter < 10000; iter++)
        {
            foreach (var idx in indices)
            {
                sum += array[idx];
            }
        }
        sw.Stop();
        Console.WriteLine($"\nArray random access: {sw.ElapsedMilliseconds}ms");

        sw.Restart();
        for (int iter = 0; iter < 10000; iter++)
        {
            foreach (var idx in indices)
            {
                sum += list[idx];
            }
        }
        sw.Stop();
        Console.WriteLine($"List random access: {sw.ElapsedMilliseconds}ms");

        Console.WriteLine("\n[ARCHITECT TAKEAWAY]");
        Console.WriteLine("Arrays have slight edge in performance due to less indirection.");
        // what does indirection mean in this context? Indirection refers to the additional level of abstraction and memory access required by the list to manage its internal structure, such as maintaining a reference to the underlying array and handling dynamic resizing, whereas arrays provide direct access to their elements without this extra layer.
        Console.WriteLine("Lists provide flexibility. Choose based on your requirements.");
    }
}
```

---

### Exercise 7: Span<T> - Modern High-Performance Alternative

Create `SpanDemo.cs`:

```csharp
namespace DataStructures;

public class SpanDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== SPAN<T> - MODERN APPROACH ===\n");

        // ARCHITECT INSIGHT: Span<T> provides memory-safe, high-performance
        // access to contiguous memory without allocations

        // what does it mean contiguous memory? Contiguous memory refers to a block of memory where all elements are stored sequentially without any gaps, allowing for efficient access and better cache performance.

        // 1. Span from array
        int[] array = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
        Span<int> span = array;

        Console.WriteLine($"Original: {string.Join(", ", array)}");

        // 2. Slicing without allocation
        Span<int> slice = span.Slice(2, 5); // Start at index 2, take 5 elements
        Console.WriteLine($"Slice [2..5]: {SpanToString(slice)}");

        // 3. Modifications affect original array!
        slice[0] = 100;
        Console.WriteLine($"After modifying slice: {string.Join(", ", array)}");
        // how look like array after modifying slice? [1, 2, 100, 4, 5, 6, 7, 8, 9, 10]
        // how look like slice after modifying slice? [100, 4, 5, 6, 7]

        // 4. Range syntax (C# 8+)
        Span<int> rangeSlice = span[3..7]; // Start at index 3, up to but not including index 7
        Console.WriteLine($"Range [3..7]: {SpanToString(rangeSlice)}");
        // how look like rangeSlice? [4, 5, 6, 7]

        // 5. ReadOnlySpan for immutable access
        ReadOnlySpan<int> readOnly = array;
        // readOnly[0] = 1; // Compile error!

        // 6. Span on stack-allocated memory
        Span<int> stackSpan = stackalloc int[5]; // what does stackalloc do? It allocates a block of memory on the stack for the specified number of elements, which is automatically freed when the method returns, providing a high-performance way to work with temporary data without heap allocations.
        for (int i = 0; i < stackSpan.Length; i++)
        {
            stackSpan[i] = i * 10;
        }
        Console.WriteLine($"\nStack-allocated span: {SpanToString(stackSpan)}");
        // how look like stackSpan? [0, 10, 20, 30, 40]

        // 7. Parsing without allocations
        ReadOnlySpan<char> text = "Hello, World!";
        ReadOnlySpan<char> hello = text[..5]; // Start at index 0, up to but not including index 5
        ReadOnlySpan<char> world = text[7..12]; // Start at index 7, up to but not including index 12
        Console.WriteLine($"\nParsed: '{hello.ToString()}' and '{world.ToString()}'");
        // how look like hello? "Hello"
        // how look like world? "World"
    }

    private static string SpanToString<T>(Span<T> span)
    {
        return string.Join(", ", span.ToArray());
    }
}
```

---

## 3. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DataStructures;

Console.WriteLine("╔═══════════════════════════════════════════════════╗");
Console.WriteLine("║     ARRAYS AND LISTS - ARCHITECT TRAINING         ║");
Console.WriteLine("╚═══════════════════════════════════════════════════╝");

ArrayBasics.Run();
MultiDimensionalArrays.Run();
ArrayOperations.Run();
ListBasics.Run();
ListPerformance.Run();
PerformanceComparison.Run();
SpanDemo.Run();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌─────────────────────────────────────────────────────┐");
Console.WriteLine("│ Use ARRAY when:                                     │");
Console.WriteLine("│   • Size is fixed and known at compile time         │");
Console.WriteLine("│   • Maximum performance is critical                 │");
Console.WriteLine("│   • Working with interop/P-Invoke                   │");
Console.WriteLine("│   • Multi-dimensional data (matrices)               │");
Console.WriteLine("├─────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use LIST when:                                      │");
Console.WriteLine("│   • Size may change during runtime                  │");
Console.WriteLine("│   • Need Add/Remove operations                      │");
Console.WriteLine("│   • Convenience over raw performance                │");
Console.WriteLine("│   • Building collections dynamically                │");
Console.WriteLine("├─────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use SPAN when:                                      │");
Console.WriteLine("│   • Need high-performance slicing                   │");
Console.WriteLine("│   • Want to avoid allocations                       │");
Console.WriteLine("│   • Working with subsets of arrays/memory           │");
Console.WriteLine("│   • Parsing strings without allocation              │");
Console.WriteLine("└─────────────────────────────────────────────────────┘");
```

---

## 4. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DataStructures"
dotnet run
```

---

## 5. Architect's Cheat Sheet

### Time Complexity Comparison

| Operation | Array | List<T> | Notes |
|-----------|-------|---------|-------|
| Access by index | O(1) | O(1) | Both excellent |
| Search | O(n) | O(n) | Linear scan |
| Binary Search | O(log n) | O(log n) | Must be sorted |
| Add at end | N/A | O(1)* | *Amortized |
| Insert | O(n) | O(n) | Requires shifting |
| Remove | O(n) | O(n) | Requires shifting |
| Memory | Compact | +Overhead | List has capacity buffer |

### Memory Layout

```
Array:  [0][1][2][3][4]  ← Fixed, contiguous
         ↑ Direct memory access

List:   [Header | Count | Capacity | → Array pointer]
                                      ↓
                              [0][1][2][3][_][_][_][_]
                                          ↑ Unused capacity
```

---

## 6. Advanced Topics for Architects

### ImmutableArray<T>

```csharp
using System.Collections.Immutable;

// Thread-safe, immutable collection
ImmutableArray<int> immutable = ImmutableArray.Create(1, 2, 3);
ImmutableArray<int> newArray = immutable.Add(4); // Returns NEW array
```

### ArrayPool<T> - Reduce GC Pressure

```csharp
using System.Buffers;

// Rent from pool instead of allocating
int[] rented = ArrayPool<int>.Shared.Rent(1000);
try
{
    // Use the array
}
finally
{
    ArrayPool<int>.Shared.Return(rented);
}
```

### CollectionsMarshal - Internal Access

```csharp
using System.Runtime.InteropServices;

List<int> list = new() { 1, 2, 3 };
Span<int> span = CollectionsMarshal.AsSpan(list);
// Direct span access to List's internal array!
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Arrays** | Fixed-size, best performance, use when size is known |
| **List<T>** | Dynamic, flexible, slight overhead, most common choice |
| **Span<T>** | Zero-allocation slicing, modern high-perf scenarios |
| **Capacity** | Pre-allocate when size is predictable to avoid resizing |
| **ImmutableArray** | Thread-safe scenarios requiring immutability |
| **ArrayPool** | High-throughput scenarios to reduce GC |

---

**Next Step**: Move to **Stacks and Queues** when ready!
