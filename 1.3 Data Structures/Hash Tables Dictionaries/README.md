# Hash Tables / Dictionaries in C#

## Overview

Hash tables are one of the **most important data structures** in software engineering. As an architect, you'll use them constantly for caching, lookups, indexing, and configuration management. Understanding their internals helps you make informed decisions about performance and memory trade-offs.

---

## 1. What is a Hash Table?

A hash table is a data structure that maps **keys to values** using a **hash function**. The hash function converts keys into array indices, enabling near-constant time lookups.

### How Hashing Works

```
Key: "John"
    ↓
Hash Function: GetHashCode()
    ↓
Hash Code: 2314539 (integer)
    ↓
Index: hashCode % bucketCount = 2314539 % 8 = 3
    ↓
Store at bucket[3]
```

### Key Characteristics

| Property | Dictionary<TKey,TValue> |
|----------|------------------------|
| Lookup | O(1) average, O(n) worst |
| Insert | O(1) average, O(n) worst |
| Delete | O(1) average, O(n) worst |
| Memory | Extra overhead for buckets |
| Order | Not guaranteed |
| Namespace | `System.Collections.Generic` |

---

## 2. Hash Collision Strategies

When two keys hash to the same index, we have a **collision**. C# uses **separate chaining** (linked lists at each bucket).

what does it mean separate chaining? Separate chaining is a collision resolution technique where each bucket in the hash table contains a list (or chain) of entries that hash to the same index. When a collision occurs, the new key-value pair is added to the list at that bucket, allowing multiple entries to coexist at the same index without overwriting each other.

what is the difference with a golang map? The main difference between C#'s Dictionary<TKey,TValue> and Go's map is that C# uses separate chaining to handle hash collisions, while Go uses open addressing with linear probing. In C#, when a collision occurs, the new key-value pair is added to a linked list at the corresponding bucket, allowing multiple entries to exist at the same index. In contrast, Go's map resolves collisions by probing for the next available slot in the array, which can lead to clustering and performance degradation if many collisions occur. Additionally, C#'s Dictionary<TKey,TValue> provides more features like custom equality comparers and thread-safe variants, while Go's map is simpler and built into the language with less overhead.

for me this is wrong is better to throw and exception when trying to add a key that already exists, instead of adding it to the list, because it can lead to performance issues if there are many collisions. In C#, the Dictionary<TKey,TValue> class does throw an exception if you try to add a key that already exists using the Add method, which helps prevent performance degradation due to collisions. However, if you use the indexer (e.g., dict[key] = value), it will overwrite the existing value without throwing an exception, which can be useful in some scenarios but requires careful handling to avoid unintended consequences.

```
Bucket 0: → [Key1, Value1] → [Key5, Value5]
Bucket 1: → [Key2, Value2]
Bucket 2: → null
Bucket 3: → [Key3, Value3] → [Key4, Value4] → [Key7, Value7]
```

---

### Hands-On: Project Setup

If you haven't created the project yet:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n DataStructures
cd DataStructures
```

Or if you already have it:

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DataStructures"
```

---

### Exercise 1: Dictionary Fundamentals

Create a file `DictionaryBasics.cs` and type the following:

```csharp
namespace DataStructures;

public class DictionaryBasics
{
    public static void Run()
    {
        Console.WriteLine("=== DICTIONARY FUNDAMENTALS ===\n");

        // 1. Creating Dictionaries
        Dictionary<string, int> ages = new();
        Dictionary<int, string> idToName = new(capacity: 100); // Pre-allocate

        // Collection initializer
        Dictionary<string, string> capitals = new()
        {
            ["USA"] = "Washington D.C.",
            ["UK"] = "London",
            ["France"] = "Paris"
        };

        // Alternative syntax
        Dictionary<string, int> scores = new()
        {
            { "Alice", 95 },
            { "Bob", 87 },
            { "Charlie", 92 }
        };

        // 2. Adding Elements - O(1) average
        ages["John"] = 30;
        ages["Jane"] = 25;
        ages.Add("Bob", 35); // Throws if key exists!

        Console.WriteLine($"Ages: {DictToString(ages)}");

        // 3. Accessing Elements - O(1) average
        int johnsAge = ages["John"];
        Console.WriteLine($"John's age: {johnsAge}");

        // 4. Safe Access with TryGetValue (PREFERRED!)
        if (ages.TryGetValue("Jane", out int janesAge))
        {
            Console.WriteLine($"Jane's age: {janesAge}");
        }

        if (!ages.TryGetValue("Unknown", out int unknownAge))
        {
            Console.WriteLine("Unknown person not found");
        }

        // 5. ContainsKey and ContainsValue
        bool hasJohn = ages.ContainsKey("John");      // O(1)
        bool hasAge30 = ages.ContainsValue(30);        // O(n)!
        Console.WriteLine($"\nHas John: {hasJohn}");
        Console.WriteLine($"Has age 30: {hasAge30}");

        // 6. Updating Values
        ages["John"] = 31; // Update existing
        Console.WriteLine($"John's new age: {ages["John"]}");

        // 7. Removing Elements - O(1)
        bool removed = ages.Remove("Bob");
        Console.WriteLine($"\nRemoved Bob: {removed}");

        // Remove and get value (C# 7+)
        if (ages.Remove("Jane", out int removedAge))
        {
            Console.WriteLine($"Removed Jane with age: {removedAge}");
        }

        // 8. Count and Clear
        Console.WriteLine($"\nCount: {ages.Count}");
        ages.Clear();
        Console.WriteLine($"After Clear: {ages.Count}");
    }

    private static string DictToString<TKey, TValue>(Dictionary<TKey, TValue> dict) 
        where TKey : notnull
    {
        return string.Join(", ", dict.Select(kv => $"{kv.Key}={kv.Value}"));
    }
}
```
Are the dictionaries more performant than lists for lookups? Yes, dictionaries are generally more performant than lists for lookups because they use a hash-based structure that allows for average-case O(1) time complexity for lookups, while lists require O(n) time complexity as they may need to iterate through the entire list to find an element. However, the actual performance can depend on factors such as the size of the collection and the quality of the hash function used in the dictionary.

what size make a dictionary less performant than a list? The performance of a dictionary can degrade when there are many collisions, which can happen if the hash function is poor or if the number of entries exceeds the capacity of the dictionary, leading to increased time complexity for lookups. In general, if a dictionary has a large number of entries (e.g., tens of thousands or more) and experiences many collisions, it may become less performant than a list for lookups. However, this threshold can vary based on the specific use case and the quality of the hash function. In practice, dictionaries are still often more efficient than lists for lookups even with a large number of entries, as long as the hash function distributes keys well and the dictionary is properly sized.

let's suppose the keys are handle properly, how many entries make a dictionary less performant than a list? If the keys are handled properly and the hash function distributes them well, a dictionary can still be more performant than a list for lookups even with a large number of entries. However, as the number of entries grows into the hundreds of thousands or millions, the overhead of managing the hash table and potential collisions can start to impact performance. In general, dictionaries are designed to handle large datasets efficiently, so it's unlikely that you would encounter a scenario where a dictionary becomes less performant than a list solely due to size, as long as it is used appropriately and the keys are well-distributed.

it sounds the dictionary will always be better than a list for lookups, is that correct? Yes, in general, a dictionary will always be better than a list for lookups when you need to retrieve values based on keys, as dictionaries are designed for fast key-based access with average-case O(1) time complexity. Lists, on the other hand, require O(n) time complexity for lookups since they may need to iterate through the entire list to find an element. However, if you only need to access elements by their index or if the dataset is very small, a list might be more appropriate due to its lower overhead. But for key-based lookups, dictionaries are typically the superior choice regardless of size.

---

### Exercise 2: Iterating Dictionaries

Create `DictionaryIteration.cs`:

```csharp
namespace DataStructures;

public class DictionaryIteration
{
    public static void Run()
    {
        Console.WriteLine("\n=== DICTIONARY ITERATION ===\n");

        Dictionary<string, decimal> products = new()
        {
            ["Laptop"] = 999.99m,
            ["Mouse"] = 29.99m,
            ["Keyboard"] = 79.99m,
            ["Monitor"] = 299.99m
        };

        // 1. Iterate Key-Value Pairs (most common)
        Console.WriteLine("Using KeyValuePair:");
        foreach (KeyValuePair<string, decimal> kvp in products)
        {
            Console.WriteLine($"  {kvp.Key}: ${kvp.Value}");
        }

        // 2. Using var (cleaner)
        Console.WriteLine("\nUsing var:");
        foreach (var kvp in products)
        {
            Console.WriteLine($"  {kvp.Key}: ${kvp.Value}");
        }

        // 3. Deconstruction (C# 7+)
        Console.WriteLine("\nUsing deconstruction:");
        foreach (var (product, price) in products)
        {
            Console.WriteLine($"  {product}: ${price}");
        }

        // 4. Iterate Keys only
        Console.WriteLine("\nKeys only:");
        foreach (string key in products.Keys)
        {
            Console.Write($"{key}, ");
        }

        // 5. Iterate Values only
        Console.WriteLine("\n\nValues only:");
        foreach (decimal value in products.Values)
        {
            Console.Write($"${value}, ");
        }

        // 6. LINQ operations
        Console.WriteLine("\n\nLINQ - Products over $50:");
        var expensive = products
            .Where(p => p.Value > 50)
            .OrderByDescending(p => p.Value);

        // when using linq the performance is worse than using a foreach? Yes, using LINQ can introduce additional overhead compared to a simple foreach loop, especially if the collection is large or if the LINQ query is complex. LINQ queries often involve creating intermediate objects and may require multiple iterations over the collection, which can lead to increased memory usage and slower performance. In contrast, a foreach loop allows you to iterate directly over the collection without the overhead of creating additional objects or performing multiple passes. However, for small collections or simple queries, the performance difference may be negligible, and LINQ can provide more readable and expressive code.

        foreach (var (name, price) in expensive)
        {
            Console.WriteLine($"  {name}: ${price}");
        }

        // 7. Convert to arrays
        string[] keys = products.Keys.ToArray();
        decimal[] values = products.Values.ToArray();
        Console.WriteLine($"\nKeys array: [{string.Join(", ", keys)}]");
    }
}
```

---

### Exercise 3: GetValueOrDefault and TryAdd

Create `DictionaryModernPatterns.cs`:

```csharp
namespace DataStructures;

public class DictionaryModernPatterns
{
    public static void Run()
    {
        Console.WriteLine("\n=== MODERN DICTIONARY PATTERNS ===\n");

        Dictionary<string, int> inventory = new()
        {
            ["Apples"] = 50,
            ["Oranges"] = 30
        };

        // 1. GetValueOrDefault - Returns default if key not found
        int apples = inventory.GetValueOrDefault("Apples");       // 50
        int bananas = inventory.GetValueOrDefault("Bananas");     // 0 (default int)
        int grapes = inventory.GetValueOrDefault("Grapes", -1);   // -1 (custom default)

        Console.WriteLine($"Apples: {apples}");
        Console.WriteLine($"Bananas: {bananas}");
        Console.WriteLine($"Grapes: {grapes}");

        // 2. TryAdd - Only adds if key doesn't exist (returns bool)
        bool added1 = inventory.TryAdd("Bananas", 25);  // true, added
        bool added2 = inventory.TryAdd("Apples", 100);  // false, already exists

        Console.WriteLine($"\nTryAdd Bananas: {added1}");
        Console.WriteLine($"TryAdd Apples: {added2}");
        Console.WriteLine($"Apples count: {inventory["Apples"]}"); // Still 50

        // 3. Pattern: Add or Update (common pattern)
        Console.WriteLine("\n--- Add or Update Pattern ---");
        AddOrIncrement(inventory, "Apples", 10);   // 50 + 10 = 60
        AddOrIncrement(inventory, "Mangoes", 15);  // New with 15

        foreach (var (fruit, count) in inventory)
        {
            Console.WriteLine($"  {fruit}: {count}");
        }

        // 4. CollectionsMarshal.GetValueRefOrAddDefault (high-perf, .NET 6+)
        Console.WriteLine("\n--- High-Performance Update ---");
        HighPerfIncrement(inventory, "Apples", 5);
        Console.WriteLine($"Apples after high-perf increment: {inventory["Apples"]}");
    }

    // Standard pattern
    private static void AddOrIncrement(Dictionary<string, int> dict, string key, int amount)
    {
        if (dict.TryGetValue(key, out int existing))
        {
            dict[key] = existing + amount;
        }
        else
        {
            dict[key] = amount;
        }
    }

    // High-performance pattern (avoids double lookup)
    private static void HighPerfIncrement(Dictionary<string, int> dict, string key, int amount)
    {
        ref int valueRef = ref System.Runtime.InteropServices.CollectionsMarshal
            .GetValueRefOrAddDefault(dict, key, out bool exists);
        valueRef += amount;
    }
}
```

---

### Exercise 4: Custom Equality Comparers

Create `CustomEqualityDemo.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Understanding equality is crucial.
/// Bad GetHashCode/Equals implementations cause severe performance issues.
/// </summary>
public class CustomEqualityDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== CUSTOM EQUALITY COMPARERS ===\n");

        // 1. Case-insensitive dictionary
        var caseInsensitive = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
        {
            ["Apple"] = 1
        };

        Console.WriteLine($"caseInsensitive[\"APPLE\"]: {caseInsensitive["APPLE"]}");
        Console.WriteLine($"caseInsensitive[\"apple\"]: {caseInsensitive["apple"]}");

        // 2. Custom object as key
        var employeeData = new Dictionary<Employee, string>();
        var emp1 = new Employee(1, "John");
        var emp2 = new Employee(1, "John"); // Same ID

        employeeData[emp1] = "Engineering";

        // Without proper Equals/GetHashCode, this would NOT find emp1!
        Console.WriteLine($"\nFound emp2 in dict: {employeeData.ContainsKey(emp2)}");
        Console.WriteLine($"emp1.Equals(emp2): {emp1.Equals(emp2)}");
        Console.WriteLine($"emp1 hash: {emp1.GetHashCode()}, emp2 hash: {emp2.GetHashCode()}");

        // 3. Using custom IEqualityComparer
        var byNameOnly = new Dictionary<Employee, string>(new EmployeeNameComparer())
        {
            [new Employee(1, "John")] = "Engineering"
        };

        var johnWithDifferentId = new Employee(999, "John");
        Console.WriteLine($"\nFound John (different ID): {byNameOnly.ContainsKey(johnWithDifferentId)}");

        // 4. Common comparers
        Console.WriteLine("\n--- Built-in Comparers ---");
        var ordinal = new Dictionary<string, int>(StringComparer.Ordinal);
        var invariant = new Dictionary<string, int>(StringComparer.InvariantCulture);
        var currentCulture = new Dictionary<string, int>(StringComparer.CurrentCulture);

        Console.WriteLine("StringComparer.Ordinal - Fast, binary comparison");
        Console.WriteLine("StringComparer.OrdinalIgnoreCase - Fast, case-insensitive");
        Console.WriteLine("StringComparer.InvariantCulture - Culture-aware, consistent");
    }
}

// IMPORTANT: When using objects as dictionary keys, implement GetHashCode and Equals
public class Employee : IEquatable<Employee>
{
    public int Id { get; }
    public string Name { get; }

    public Employee(int id, string name)
    {
        Id = id;
        Name = name;
    }

    public bool Equals(Employee? other)
    {
        if (other is null) return false;
        return Id == other.Id && Name == other.Name;
    }

    public override bool Equals(object? obj) => Equals(obj as Employee);

    public override int GetHashCode() => HashCode.Combine(Id, Name);
}

public class EmployeeNameComparer : IEqualityComparer<Employee>
{
    public bool Equals(Employee? x, Employee? y)
    {
        if (x is null || y is null) return x is null && y is null;
        return string.Equals(x.Name, y.Name, StringComparison.OrdinalIgnoreCase);
    }

    public int GetHashCode(Employee obj)
    {
        return StringComparer.OrdinalIgnoreCase.GetHashCode(obj.Name);
    }
}
```

---

### Exercise 5: HashSet<T> - Unique Collections

Create `HashSetDemo.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: HashSet is essentially a Dictionary without values.
/// Use for membership testing and eliminating duplicates.
/// </summary>
public class HashSetDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== HASHSET<T> ===\n");

        // 1. Creating HashSets
        HashSet<int> numbers = new() { 1, 2, 3, 4, 5 };
        HashSet<string> names = new(StringComparer.OrdinalIgnoreCase);
        

        // 2. Adding Elements
        bool added1 = numbers.Add(6);  // true
        bool added2 = numbers.Add(3);  // false (already exists)
        Console.WriteLine($"Add 6: {added1}, Add 3: {added2}");
        Console.WriteLine($"Numbers: {string.Join(", ", numbers)}");

        // 3. Checking Membership - O(1)
        bool contains = numbers.Contains(3);
        Console.WriteLine($"\nContains 3: {contains}");

        // 4. Set Operations
        HashSet<int> setA = new() { 1, 2, 3, 4, 5 };
        HashSet<int> setB = new() { 4, 5, 6, 7, 8 };

        // Union (A ∪ B)
        var union = new HashSet<int>(setA);
        union.UnionWith(setB);
        Console.WriteLine($"\nUnion: {string.Join(", ", union)}");

        // Intersection (A ∩ B)
        var intersection = new HashSet<int>(setA);
        intersection.IntersectWith(setB);
        Console.WriteLine($"Intersection: {string.Join(", ", intersection)}");

        // Difference (A - B)
        var difference = new HashSet<int>(setA);
        difference.ExceptWith(setB);
        Console.WriteLine($"Difference (A-B): {string.Join(", ", difference)}");

        // Symmetric Difference (A △ B) - elements in either but not both
        var symmetricDiff = new HashSet<int>(setA);
        symmetricDiff.SymmetricExceptWith(setB);
        Console.WriteLine($"Symmetric Diff: {string.Join(", ", symmetricDiff)}");

        // 5. Subset/Superset checks
        HashSet<int> small = new() { 1, 2 };
        HashSet<int> large = new() { 1, 2, 3, 4, 5 };

        Console.WriteLine($"\n{{1,2}} is subset of {{1,2,3,4,5}}: {small.IsSubsetOf(large)}");
        Console.WriteLine($"{{1,2,3,4,5}} is superset of {{1,2}}: {large.IsSupersetOf(small)}");
        Console.WriteLine($"Sets overlap: {small.Overlaps(large)}");

        // 6. Removing duplicates from list (common pattern)
        List<string> withDupes = new() { "A", "B", "A", "C", "B", "D", "A" };
        List<string> unique = new HashSet<string>(withDupes).ToList();
        Console.WriteLine($"\nOriginal: [{string.Join(", ", withDupes)}]");
        Console.WriteLine($"Unique: [{string.Join(", ", unique)}]");
    }
}
```

---

### Exercise 6: Concurrent Dictionaries

Create `ConcurrentDictionaryDemo.cs`:

```csharp
using System.Collections.Concurrent;

namespace DataStructures;

/// <summary>
/// ARCHITECT PATTERN: Thread-safe dictionary for multi-threaded scenarios.
/// Essential for caching, memoization, and shared state.
/// </summary>
public class ConcurrentDictionaryDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== CONCURRENT DICTIONARY ===\n");

        ConcurrentDictionary<string, int> cache = new();

        // 1. TryAdd - Thread-safe add
        cache.TryAdd("item1", 100);
        cache.TryAdd("item2", 200);

        // 2. GetOrAdd - Get existing or add new (atomic)
        int value1 = cache.GetOrAdd("item1", 999);    // Returns 100 (existing)
        int value2 = cache.GetOrAdd("item3", 300);    // Adds and returns 300

        Console.WriteLine($"GetOrAdd item1: {value1}");
        Console.WriteLine($"GetOrAdd item3: {value2}");

        // 3. GetOrAdd with factory (lazy initialization)
        var expensiveCache = new ConcurrentDictionary<string, ExpensiveObject>();

        var obj = expensiveCache.GetOrAdd("key1", key =>
        {
            Console.WriteLine($"  Creating expensive object for {key}...");
            return new ExpensiveObject(key);
        });

        var objAgain = expensiveCache.GetOrAdd("key1", key =>
        {
            Console.WriteLine("  This won't print - object already exists");
            return new ExpensiveObject(key);
        });

        Console.WriteLine($"Same object: {ReferenceEquals(obj, objAgain)}");

        // 4. AddOrUpdate - Add if not exists, update if exists
        var counters = new ConcurrentDictionary<string, int>();

        counters.AddOrUpdate("pageViews",
            addValue: 1,
            updateValueFactory: (key, oldValue) => oldValue + 1);

        counters.AddOrUpdate("pageViews",
            addValue: 1,
            updateValueFactory: (key, oldValue) => oldValue + 1);

        Console.WriteLine($"\nPage views: {counters["pageViews"]}");

        // 5. Multi-threaded example
        Console.WriteLine("\n--- Multi-threaded Counter ---");
        var threadSafeCounter = new ConcurrentDictionary<string, int>();

        var tasks = new List<Task>();
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(Task.Run(() =>
            {
                for (int j = 0; j < 100; j++)
                {
                    threadSafeCounter.AddOrUpdate("counter", 1, (k, v) => v + 1);
                }
            }));
        }

        Task.WaitAll(tasks.ToArray());
        Console.WriteLine($"Final counter value: {threadSafeCounter["counter"]}");
        // Should always be 1000 (10 tasks × 100 increments)

        // 6. TryUpdate - Conditional update
        cache["item1"] = 100;
        bool updated = cache.TryUpdate("item1",
            newValue: 150,
            comparisonValue: 100);  // Only update if current value is 100

        Console.WriteLine($"\nTryUpdate succeeded: {updated}");
        Console.WriteLine($"New value: {cache["item1"]}");
    }
}

public class ExpensiveObject
{
    public string Key { get; }
    public DateTime Created { get; } = DateTime.Now;

    public ExpensiveObject(string key)
    {
        Key = key;
        Thread.Sleep(10); // Simulate expensive creation
    }
}
```

---

### Exercise 7: Immutable and Frozen Dictionaries

Create `ImmutableDictionaryDemo.cs`:

```csharp
using System.Collections.Frozen;
using System.Collections.Immutable;

namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Immutable collections for thread safety.
/// Frozen collections (.NET 8+) for read-heavy scenarios with maximum perf.
/// </summary>
public class ImmutableDictionaryDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== IMMUTABLE & FROZEN DICTIONARIES ===\n");

        // 1. ImmutableDictionary - Thread-safe, functional style
        var immutable = ImmutableDictionary<string, int>.Empty;

        // Each operation returns a NEW dictionary
        immutable = immutable.Add("A", 1);
        var immutable2 = immutable.Add("B", 2);
        var immutable3 = immutable2.SetItem("A", 10);

        Console.WriteLine($"Original: A={immutable["A"]}");
        Console.WriteLine($"After adding B: A={immutable2["A"]}, B={immutable2["B"]}");
        Console.WriteLine($"After updating A: A={immutable3["A"]}");

        // 2. Builder pattern (more efficient for bulk operations)
        var builder = ImmutableDictionary.CreateBuilder<string, int>();
        builder.Add("X", 100);
        builder.Add("Y", 200);
        builder.Add("Z", 300);
        var builtDict = builder.ToImmutable();

        Console.WriteLine($"\nBuilt dictionary: {string.Join(", ", builtDict.Select(kv => $"{kv.Key}={kv.Value}"))}");

        // 3. FrozenDictionary (.NET 8+) - Optimized for read-heavy scenarios
        var regularDict = new Dictionary<string, int>
        {
            ["Config1"] = 100,
            ["Config2"] = 200,
            ["Config3"] = 300
        };

        // Create frozen dictionary (one-time cost)
        FrozenDictionary<string, int> frozen = regularDict.ToFrozenDictionary();

        // Lookups are FASTER than regular Dictionary
        Console.WriteLine($"\nFrozen lookup: Config2 = {frozen["Config2"]}");

        // 4. FrozenSet
        var items = new[] { "apple", "banana", "cherry" };
        FrozenSet<string> frozenSet = items.ToFrozenSet(StringComparer.OrdinalIgnoreCase);

        Console.WriteLine($"FrozenSet contains 'APPLE': {frozenSet.Contains("APPLE")}");

        // ARCHITECT NOTE:
        Console.WriteLine("\n--- When to use each ---");
        Console.WriteLine("Dictionary<K,V>: General purpose, mutable");
        Console.WriteLine("ConcurrentDictionary<K,V>: Multi-threaded reads/writes");
        Console.WriteLine("ImmutableDictionary<K,V>: Thread-safe, functional updates");
        Console.WriteLine("FrozenDictionary<K,V>: Read-only config, max lookup speed");
    }
}
```

---

### Exercise 8: Practical Patterns - Caching & Memoization

Create `CachingPatterns.cs`:

```csharp
using System.Collections.Concurrent;

namespace DataStructures;

/// <summary>
/// ARCHITECT PATTERNS: Common dictionary-based patterns in production systems.
/// </summary>
public class CachingPatterns
{
    public static void Run()
    {
        Console.WriteLine("\n=== CACHING PATTERNS ===\n");

        // 1. Simple Memoization
        Console.WriteLine("--- Memoization ---");
        var fibonacci = new MemoizedFibonacci();

        var sw = System.Diagnostics.Stopwatch.StartNew();
        long fib40 = fibonacci.Calculate(40);
        sw.Stop();
        Console.WriteLine($"Fib(40) = {fib40}, Time: {sw.ElapsedMilliseconds}ms");

        sw.Restart();
        long fib40Again = fibonacci.Calculate(40);
        sw.Stop();
        Console.WriteLine($"Fib(40) cached = {fib40Again}, Time: {sw.ElapsedMilliseconds}ms");

        // 2. LRU Cache (Least Recently Used)
        Console.WriteLine("\n--- LRU Cache ---");
        var lruCache = new SimpleLRUCache<string, string>(capacity: 3);

        lruCache.Put("A", "Value A");
        lruCache.Put("B", "Value B");
        lruCache.Put("C", "Value C");
        Console.WriteLine(lruCache);

        lruCache.Get("A"); // Access A (moves to most recent)
        lruCache.Put("D", "Value D"); // Evicts B (least recently used)
        Console.WriteLine($"After adding D: {lruCache}");

        // 3. Two-way lookup
        Console.WriteLine("\n--- Bidirectional Map ---");
        var biMap = new BiMap<int, string>();
        biMap.Add(1, "One");
        biMap.Add(2, "Two");
        biMap.Add(3, "Three");

        Console.WriteLine($"Forward lookup [1]: {biMap.GetByKey(1)}");
        Console.WriteLine($"Reverse lookup [\"Two\"]: {biMap.GetByValue("Two")}");

        // 4. MultiValueDictionary pattern
        Console.WriteLine("\n--- MultiValue Dictionary ---");
        var multiDict = new Dictionary<string, List<string>>();

        AddToMultiDict(multiDict, "Fruits", "Apple");
        AddToMultiDict(multiDict, "Fruits", "Banana");
        AddToMultiDict(multiDict, "Fruits", "Cherry");
        AddToMultiDict(multiDict, "Vegetables", "Carrot");

        foreach (var (category, items) in multiDict)
        {
            Console.WriteLine($"{category}: [{string.Join(", ", items)}]");
        }
    }

    private static void AddToMultiDict<TKey, TValue>(
        Dictionary<TKey, List<TValue>> dict, TKey key, TValue value) where TKey : notnull
    {
        if (!dict.TryGetValue(key, out var list))
        {
            list = new List<TValue>();
            dict[key] = list;
        }
        list.Add(value);
    }
}

// Memoization pattern
public class MemoizedFibonacci
{
    private readonly Dictionary<int, long> _cache = new();

    public long Calculate(int n)
    {
        if (n <= 1) return n;

        if (_cache.TryGetValue(n, out long cached))
            return cached;

        long result = Calculate(n - 1) + Calculate(n - 2);
        _cache[n] = result;
        return result;
    }
}

// Simple LRU Cache using LinkedList + Dictionary
public class SimpleLRUCache<TKey, TValue> where TKey : notnull
{
    private readonly int _capacity;
    private readonly Dictionary<TKey, LinkedListNode<(TKey Key, TValue Value)>> _cache;
    private readonly LinkedList<(TKey Key, TValue Value)> _order;

    public SimpleLRUCache(int capacity)
    {
        _capacity = capacity;
        _cache = new Dictionary<TKey, LinkedListNode<(TKey, TValue)>>(capacity);
        _order = new LinkedList<(TKey, TValue)>();
    }

    public TValue? Get(TKey key)
    {
        if (_cache.TryGetValue(key, out var node))
        {
            _order.Remove(node);
            _order.AddLast(node);
            return node.Value.Value;
        }
        return default;
    }

    public void Put(TKey key, TValue value)
    {
        if (_cache.TryGetValue(key, out var existing))
        {
            _order.Remove(existing);
            _cache.Remove(key);
        }
        else if (_cache.Count >= _capacity)
        {
            var lru = _order.First!;
            _cache.Remove(lru.Value.Key);
            _order.RemoveFirst();
        }

        var newNode = _order.AddLast((key, value));
        _cache[key] = newNode;
    }

    public override string ToString() =>
        $"[{string.Join(", ", _order.Select(x => $"{x.Key}={x.Value}"))}]";
}

// Bidirectional map
public class BiMap<TKey, TValue>
    where TKey : notnull
    where TValue : notnull
{
    private readonly Dictionary<TKey, TValue> _forward = new();
    private readonly Dictionary<TValue, TKey> _reverse = new();

    public void Add(TKey key, TValue value)
    {
        _forward[key] = value;
        _reverse[value] = key;
    }

    public TValue GetByKey(TKey key) => _forward[key];
    public TKey GetByValue(TValue value) => _reverse[value];
}
```

---

## 3. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DataStructures;

Console.WriteLine("╔═══════════════════════════════════════════════════════╗");
Console.WriteLine("║   HASH TABLES / DICTIONARIES - ARCHITECT TRAINING     ║");
Console.WriteLine("╚═══════════════════════════════════════════════════════╝");

DictionaryBasics.Run();
DictionaryIteration.Run();
DictionaryModernPatterns.Run();
CustomEqualityDemo.Run();
HashSetDemo.Run();
ConcurrentDictionaryDemo.Run();
ImmutableDictionaryDemo.Run();
CachingPatterns.Run();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌───────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ Use Dictionary<K,V> when:                                     │");
Console.WriteLine("│   • Single-threaded key-value storage                         │");
Console.WriteLine("│   • Need fast O(1) lookups by key                             │");
Console.WriteLine("│   • General-purpose mapping                                   │");
Console.WriteLine("├───────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use HashSet<T> when:                                          │");
Console.WriteLine("│   • Only need to track membership (no values)                 │");
Console.WriteLine("│   • Removing duplicates                                       │");
Console.WriteLine("│   • Set operations (union, intersection, etc.)                │");
Console.WriteLine("├───────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use ConcurrentDictionary<K,V> when:                           │");
Console.WriteLine("│   • Multiple threads read/write simultaneously                │");
Console.WriteLine("│   • Shared caches or memoization                              │");
Console.WriteLine("│   • Need atomic GetOrAdd/AddOrUpdate operations               │");
Console.WriteLine("├───────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use ImmutableDictionary<K,V> when:                            │");
Console.WriteLine("│   • Need thread-safe immutability                             │");
Console.WriteLine("│   • Functional programming patterns                           │");
Console.WriteLine("│   • Want to preserve previous versions                        │");
Console.WriteLine("├───────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use FrozenDictionary<K,V> when:                               │");
Console.WriteLine("│   • Data is set once, read many times                         │");
Console.WriteLine("│   • Configuration/lookup tables                               │");
Console.WriteLine("│   • Maximum read performance is critical                      │");
Console.WriteLine("└───────────────────────────────────────────────────────────────┘");
```

---

## 4. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DataStructures"
dotnet run
```

---

## 5. Architect's Cheat Sheet

### Time Complexity

| Operation | Dictionary | HashSet | ConcurrentDict |
|-----------|-----------|---------|----------------|
| Add | O(1)* | O(1)* | O(1)* |
| Lookup | O(1)* | O(1)* | O(1)* |
| Remove | O(1)* | O(1)* | O(1)* |
| ContainsValue | O(n) | N/A | O(n) |

*Average case. Worst case O(n) with hash collisions.

### Hash Function Rules

```csharp
// GOLDEN RULES for GetHashCode():
// 1. Equal objects MUST have equal hash codes
// 2. Hash code should be consistent during object lifetime (in dictionary)
// 3. Combine multiple fields with HashCode.Combine()

public override int GetHashCode()
{
    return HashCode.Combine(Field1, Field2, Field3);
}

// Bad example (don't do this!):
// return new Random().Next(); // Different every time!
```

### Memory Layout

```
Dictionary Internal Structure:
┌─────────────────────────────────────────┐
│ Buckets Array (int[])                   │
│ [0] → -1 (empty)                        │
│ [1] → 2 (index into entries)            │
│ [2] → 0 (index into entries)            │
│ [3] → -1 (empty)                        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ Entries Array (Entry[])                 │
│ [0] Key="Alice" Value=95  Next=-1       │
│ [1] Key="Bob"   Value=87  Next=0        │ ← Collision chain
│ [2] Key="Charlie" Value=92 Next=-1      │
└─────────────────────────────────────────┘
```

---

## 6. Common Interview Questions

### Q1: When does O(1) become O(n)?

**Answer**: When too many collisions occur (bad hash function or load factor too high). The dictionary degrades to a linked list.

### Q2: Why use HashSet over List for Contains?

```csharp
// List.Contains() = O(n) - linear search
// HashSet.Contains() = O(1) - hash lookup

List<int> list = Enumerable.Range(0, 1_000_000).ToList();
HashSet<int> set = list.ToHashSet();

// set.Contains(999_999) is ~1,000,000x faster than list.Contains()
```

### Q3: Dictionary vs SortedDictionary?

```csharp
Dictionary<K,V>       // Hash-based, O(1), unordered
SortedDictionary<K,V> // Tree-based, O(log n), sorted by key
SortedList<K,V>       // Array-based, O(log n) lookup, O(n) insert
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Dictionary<K,V>** | O(1) lookups, general-purpose key-value store |
| **HashSet<T>** | Unique elements only, set operations |
| **GetHashCode/Equals** | Critical for custom keys, immutable preferred |
| **ConcurrentDictionary** | Thread-safe with atomic operations |
| **FrozenDictionary** | Maximum read performance, immutable |
| **ImmutableDictionary** | Functional updates, preserves history |
| **StringComparer** | Use OrdinalIgnoreCase for case-insensitive keys |

---

**Next Step**: Move to **Trees (Binary, BST, AVL)** when ready!
