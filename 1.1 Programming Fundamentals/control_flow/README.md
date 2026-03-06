# Control Flow (if/else, switch, loops)

Master control flow structures across C#, Go, Python, and JavaScript (React).

---

## 📖 Theory

Control flow determines the order in which code executes. The three main structures are:

| Structure | Purpose |
|-----------|---------|
| **Conditional** | Execute code based on conditions (if/else, switch) |
| **Loops** | Repeat code (for, while, foreach) |
| **Branching** | Jump to another part (break, continue, return) |

---

## 🔷 C# Control Flow

### Setup
```powershell
cd code/csharp/traning
```

### If/Else

Create `ControlFlow.cs`:
```csharp
namespace traning;

public class ControlFlow
{
    public static void IfElseDemo()
    {
        int score = 85;

        // Basic if/else
        if (score >= 90)
        {
            Console.WriteLine("Grade: A");
        }
        else if (score >= 80)
        {
            Console.WriteLine("Grade: B");
        }
        else if (score >= 70)
        {
            Console.WriteLine("Grade: C");
        }
        else
        {
            Console.WriteLine("Grade: F");
        }

        // Ternary operator (concise if/else)
        string result = score >= 60 ? "Pass" : "Fail";
        Console.WriteLine($"Result: {result}");

        // Null-conditional and null-coalescing
        string? name = null;
        string displayName = name ?? "Anonymous";
        Console.WriteLine($"User: {displayName}");

        // Pattern matching with if (C# 9+)
        object obj = 42;
        if (obj is int number && number > 0)
        {
            Console.WriteLine($"Positive integer: {number}");
        }
    }
}
```

### Switch Statement

Add to `ControlFlow.cs`:
```csharp
public static void SwitchDemo()
{
    // Classic switch
    int dayOfWeek = 3;
    switch (dayOfWeek)
    {
        case 1:
            Console.WriteLine("Monday");
            break;
        case 2:
            Console.WriteLine("Tuesday");
            break;
        case 3:
            Console.WriteLine("Wednesday");
            break;
        case 4:
        case 5:
            Console.WriteLine("Thursday or Friday");
            break;
        default:
            Console.WriteLine("Weekend");
            break;
    }

    // Switch expression (C# 8+) - more concise
    string dayName = dayOfWeek switch
    {
        1 => "Monday",
        2 => "Tuesday",
        3 => "Wednesday",
        4 => "Thursday",
        5 => "Friday",
        6 or 7 => "Weekend",
        _ => "Invalid day"
    };
    Console.WriteLine($"Today is: {dayName}");

    // Pattern matching switch
    object value = 3.14;
    string typeDescription = value switch
    {
        int i => $"Integer: {i}",
        double d => $"Double: {d:F2}",
        string s => $"String: {s}",
        null => "Null value",
        _ => "Unknown type"
    };
    Console.WriteLine(typeDescription);
}
```

### Loops

Add to `ControlFlow.cs`:
```csharp
public static void LoopsDemo()
{
    // For loop
    Console.WriteLine("For loop:");
    for (int i = 0; i < 5; i++)
    {
        Console.WriteLine($"  Iteration {i}");
    }

    // While loop
    Console.WriteLine("\nWhile loop:");
    int count = 0;
    while (count < 3)
    {
        Console.WriteLine($"  Count: {count}");
        count++;
    }

    // Do-while loop (executes at least once)
    Console.WriteLine("\nDo-while loop:");
    int num = 0;
    do
    {
        Console.WriteLine($"  Number: {num}");
        num++;
    } while (num < 3);

    // Foreach loop
    Console.WriteLine("\nForeach loop:");
    string[] languages = { "C#", "Go", "Python", "JavaScript" };
    foreach (string lang in languages)
    {
        Console.WriteLine($"  Language: {lang}");
    }

    // LINQ ForEach (requires System.Linq)
    Console.WriteLine("\nLINQ operations:");
    var filtered = languages.Where(l => l.Length > 2)
                           .Select(l => l.ToUpper());
    foreach (var item in filtered)
    {
        Console.WriteLine($"  {item}");
    }
}
```

### Break, Continue, Return

Add to `ControlFlow.cs`:
```csharp
public static void BranchingDemo()
{
    // Break - exits the loop entirely
    Console.WriteLine("Break example:");
    for (int i = 0; i < 10; i++)
    {
        if (i == 5) break;
        Console.WriteLine($"  {i}");
    }

    // Continue - skips current iteration
    Console.WriteLine("\nContinue example (skip even numbers):");
    for (int i = 0; i < 10; i++)
    {
        if (i % 2 == 0) continue;
        Console.WriteLine($"  {i}");
    }

    // Labeled break with goto (use sparingly!)
    Console.WriteLine("\nNested loop break:");
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (i == 1 && j == 1) goto exitLoops;
            Console.WriteLine($"  i={i}, j={j}");
        }
    }
    exitLoops:
    Console.WriteLine("  Exited nested loops");
}
```

### Run C# Examples

Update `Program.cs`:
```csharp
using traning;

Console.WriteLine("=== IF/ELSE DEMO ===");
ControlFlow.IfElseDemo();

Console.WriteLine("\n=== SWITCH DEMO ===");
ControlFlow.SwitchDemo();

Console.WriteLine("\n=== LOOPS DEMO ===");
ControlFlow.LoopsDemo();

Console.WriteLine("\n=== BRANCHING DEMO ===");
ControlFlow.BranchingDemo();
```

```powershell
dotnet run
```

---

## 🔷 Go Control Flow

### Setup
```powershell
cd code/go
```

### If/Else

Create `control_flow.go`:
```go
package main

import "fmt"

func ifElseDemo() {
	score := 85

	// Basic if/else
	if score >= 90 {
		fmt.Println("Grade: A")
	} else if score >= 80 {
		fmt.Println("Grade: B")
	} else if score >= 70 {
		fmt.Println("Grade: C")
	} else {
		fmt.Println("Grade: F")
	}

	// If with initialization statement (scoped variable)
	if result := score >= 60; result {
		fmt.Println("Pass")
	} else {
		fmt.Println("Fail")
	}
	// 'result' is not accessible here

	// Multiple conditions
	age := 25
	hasLicense := true
	if age >= 18 && hasLicense {
		fmt.Println("Can drive")
	}
}
```

### Switch Statement

Add to `control_flow.go`:
```go
func switchDemo() {
	dayOfWeek := 3

	// Basic switch (no break needed - implicit)
	switch dayOfWeek {
	case 1:
		fmt.Println("Monday")
	case 2:
		fmt.Println("Tuesday")
	case 3:
		fmt.Println("Wednesday")
	case 4, 5: // Multiple values
		fmt.Println("Thursday or Friday")
	default:
		fmt.Println("Weekend")
	}

	// Switch with initialization
	switch day := dayOfWeek; day {
	case 1, 2, 3, 4, 5:
		fmt.Println("Weekday")
	default:
		fmt.Println("Weekend")
	}

	// Switch without expression (like if-else chain)
	score := 85
	switch {
	case score >= 90:
		fmt.Println("Excellent")
	case score >= 80:
		fmt.Println("Good")
	case score >= 70:
		fmt.Println("Average")
	default:
		fmt.Println("Poor")
	}

	// Type switch
	var value interface{} = 3.14
	switch v := value.(type) {
	case int:
		fmt.Printf("Integer: %d\n", v)
	case float64:
		fmt.Printf("Float: %.2f\n", v)
	case string:
		fmt.Printf("String: %s\n", v)
	default:
		fmt.Printf("Unknown type: %T\n", v)
	}

	// Fallthrough (explicit - rarely used)
	num := 1
	switch num {
	case 1:
		fmt.Println("One")
		fallthrough
	case 2:
		fmt.Println("Two (fallthrough)")
	}
}
```

### Loops

Add to `control_flow.go`:
```go
func loopsDemo() {
	// Go only has 'for' - but it covers all loop types

	// Classic for loop
	fmt.Println("Classic for:")
	for i := 0; i < 5; i++ {
		fmt.Printf("  Iteration %d\n", i)
	}

	// While-style loop
	fmt.Println("\nWhile-style:")
	count := 0
	for count < 3 {
		fmt.Printf("  Count: %d\n", count)
		count++
	}

	// Infinite loop (use break to exit)
	fmt.Println("\nInfinite loop with break:")
	counter := 0
	for {
		fmt.Printf("  Counter: %d\n", counter)
		counter++
		if counter >= 3 {
			break
		}
	}

	// Range loop (foreach equivalent)
	fmt.Println("\nRange over slice:")
	languages := []string{"C#", "Go", "Python", "JavaScript"}
	for index, lang := range languages {
		fmt.Printf("  [%d] %s\n", index, lang)
	}

	// Range - value only (ignore index with _)
	fmt.Println("\nRange value only:")
	for _, lang := range languages {
		fmt.Printf("  %s\n", lang)
	}

	// Range over map
	fmt.Println("\nRange over map:")
	scores := map[string]int{"Alice": 95, "Bob": 87, "Carol": 92}
	for name, score := range scores {
		fmt.Printf("  %s: %d\n", name, score)
	}

	// Range over string (iterates runes)
	fmt.Println("\nRange over string:")
	for i, char := range "Go!" {
		fmt.Printf("  [%d] %c\n", i, char)
	}

	// Range over channel
	fmt.Println("\nRange over channel:")
	ch := make(chan int, 3)
	ch <- 1
	ch <- 2
	ch <- 3
	close(ch)
	for num := range ch {
		fmt.Printf("  %d\n", num)
	}
}
```

### Break, Continue, Labels

Add to `control_flow.go`:
```go
func branchingDemo() {
	// Break
	fmt.Println("Break example:")
	for i := 0; i < 10; i++ {
		if i == 5 {
			break
		}
		fmt.Printf("  %d\n", i)
	}

	// Continue
	fmt.Println("\nContinue example (skip even):")
	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			continue
		}
		fmt.Printf("  %d\n", i)
	}

	// Labeled break (exit outer loop)
	fmt.Println("\nLabeled break:")
OuterLoop:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if i == 1 && j == 1 {
				break OuterLoop
			}
			fmt.Printf("  i=%d, j=%d\n", i, j)
		}
	}

	// Labeled continue
	fmt.Println("\nLabeled continue:")
Outer:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if j == 1 {
				continue Outer
			}
			fmt.Printf("  i=%d, j=%d\n", i, j)
		}
	}
}
```

### Run Go Examples

Update `main.go`:
```go
package main

import "fmt"

func main() {
	fmt.Println("=== IF/ELSE DEMO ===")
	ifElseDemo()

	fmt.Println("\n=== SWITCH DEMO ===")
	switchDemo()

	fmt.Println("\n=== LOOPS DEMO ===")
	loopsDemo()

	fmt.Println("\n=== BRANCHING DEMO ===")
	branchingDemo()
}
```

```powershell
go run .
```

---

## 🔷 Python Control Flow

### Setup
```powershell
cd code/py
```

### If/Else

Create `control_flow.py`:
```python
def if_else_demo():
    score = 85

    # Basic if/else
    if score >= 90:
        print("Grade: A")
    elif score >= 80:
        print("Grade: B")
    elif score >= 70:
        print("Grade: C")
    else:
        print("Grade: F")

    # Ternary operator (conditional expression)
    result = "Pass" if score >= 60 else "Fail"
    print(f"Result: {result}")

    # Multiple conditions
    age = 25
    has_license = True
    if age >= 18 and has_license:
        print("Can drive")

    # Truthy/Falsy values
    name = ""
    if name:
        print(f"Hello, {name}")
    else:
        print("Hello, Anonymous")

    # Walrus operator (Python 3.8+) - assignment expression
    numbers = [1, 2, 3, 4, 5]
    if (n := len(numbers)) > 3:
        print(f"List has {n} elements (more than 3)")

    # Chained comparisons
    x = 5
    if 0 < x < 10:
        print("x is between 0 and 10")
```

### Match Statement (Python 3.10+)

Add to `control_flow.py`:
```python
def match_demo():
    """Match statement - Python's structural pattern matching (3.10+)"""
    
    day_of_week = 3

    # Basic match (like switch)
    match day_of_week:
        case 1:
            print("Monday")
        case 2:
            print("Tuesday")
        case 3:
            print("Wednesday")
        case 4 | 5:  # Multiple patterns with OR
            print("Thursday or Friday")
        case _:  # Wildcard (default)
            print("Weekend")

    # Match with guards
    score = 85
    match score:
        case s if s >= 90:
            print("Excellent")
        case s if s >= 80:
            print("Good")
        case s if s >= 70:
            print("Average")
        case _:
            print("Poor")

    # Match with destructuring
    point = (3, 4)
    match point:
        case (0, 0):
            print("Origin")
        case (x, 0):
            print(f"On X-axis at {x}")
        case (0, y):
            print(f"On Y-axis at {y}")
        case (x, y):
            print(f"Point at ({x}, {y})")

    # Match with class patterns
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Point(3, 4)
    match p:
        case Point(x=0, y=0):
            print("At origin")
        case Point(x=x, y=y):
            print(f"Point at ({x}, {y})")

    # Match with dictionary patterns
    command = {"action": "move", "direction": "north", "distance": 10}
    match command:
        case {"action": "move", "direction": dir, "distance": dist}:
            print(f"Moving {dir} by {dist}")
        case {"action": "stop"}:
            print("Stopping")
        case _:
            print("Unknown command")
```

### Loops

Add to `control_flow.py`:
```python
def loops_demo():
    # For loop (iterates over sequences)
    print("For loop over list:")
    languages = ["C#", "Go", "Python", "JavaScript"]
    for lang in languages:
        print(f"  {lang}")

    # For with index (enumerate)
    print("\nFor with enumerate:")
    for index, lang in enumerate(languages):
        print(f"  [{index}] {lang}")

    # For with range
    print("\nFor with range:")
    for i in range(5):
        print(f"  Iteration {i}")

    # Range with start, stop, step
    print("\nRange with step:")
    for i in range(0, 10, 2):
        print(f"  {i}")

    # While loop
    print("\nWhile loop:")
    count = 0
    while count < 3:
        print(f"  Count: {count}")
        count += 1

    # While with else (executes if no break)
    print("\nWhile with else:")
    n = 0
    while n < 3:
        print(f"  {n}")
        n += 1
    else:
        print("  Loop completed without break")

    # For with else
    print("\nFor with else (search example):")
    target = 7
    for num in [1, 3, 5, 7, 9]:
        if num == target:
            print(f"  Found {target}")
            break
    else:
        print("  Not found")

    # Iterate over dictionary
    print("\nIterate over dict:")
    scores = {"Alice": 95, "Bob": 87, "Carol": 92}
    for name, score in scores.items():
        print(f"  {name}: {score}")

    # List comprehension (compact loop)
    print("\nList comprehension:")
    squares = [x**2 for x in range(5)]
    print(f"  Squares: {squares}")

    # Filtered comprehension
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"  Evens: {evens}")

    # Dictionary comprehension
    squared_dict = {x: x**2 for x in range(5)}
    print(f"  Squared dict: {squared_dict}")

    # Generator expression (memory efficient)
    print("\nGenerator expression:")
    gen = (x**2 for x in range(5))
    for val in gen:
        print(f"  {val}")

    # Zip multiple iterables
    print("\nZip example:")
    names = ["Alice", "Bob", "Carol"]
    ages = [25, 30, 28]
    for name, age in zip(names, ages):
        print(f"  {name} is {age}")
```

### Break, Continue, Pass

Add to `control_flow.py`:
```python
def branching_demo():
    # Break
    print("Break example:")
    for i in range(10):
        if i == 5:
            break
        print(f"  {i}")

    # Continue
    print("\nContinue example (skip even):")
    for i in range(10):
        if i % 2 == 0:
            continue
        print(f"  {i}")

    # Pass (placeholder - does nothing)
    print("\nPass example:")
    for i in range(3):
        if i == 1:
            pass  # TODO: implement later
        print(f"  {i}")

    # Nested loop with break
    print("\nNested loop break (inner only):")
    for i in range(3):
        for j in range(3):
            if j == 2:
                break  # Only breaks inner loop
            print(f"  i={i}, j={j}")

    # Breaking outer loop (use flag or function)
    print("\nBreaking outer loop with flag:")
    should_break = False
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                should_break = True
                break
            print(f"  i={i}, j={j}")
        if should_break:
            break


if __name__ == "__main__":
    print("=== IF/ELSE DEMO ===")
    if_else_demo()

    print("\n=== MATCH DEMO ===")
    match_demo()

    print("\n=== LOOPS DEMO ===")
    loops_demo()

    print("\n=== BRANCHING DEMO ===")
    branching_demo()
```

### Run Python Examples
```powershell
python control_flow.py
```

---

## 🔷 React (JavaScript) Control Flow

### Setup
```powershell
cd code/react
npm install
```

### Conditional Rendering

Create `src/ControlFlow.js`:
```jsx
import React, { useState } from 'react';

// Conditional Rendering Examples
function ConditionalRendering() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [score, setScore] = useState(85);
  const [items, setItems] = useState(['Apple', 'Banana', 'Orange']);

  // 1. If/else in JSX (using immediately invoked function)
  const renderGrade = () => {
    if (score >= 90) return <span className="grade-a">Grade: A</span>;
    else if (score >= 80) return <span className="grade-b">Grade: B</span>;
    else if (score >= 70) return <span className="grade-c">Grade: C</span>;
    else return <span className="grade-f">Grade: F</span>;
  };

  // 2. Ternary operator (most common in JSX)
  const greeting = isLoggedIn ? (
    <h2>Welcome back!</h2>
  ) : (
    <h2>Please log in</h2>
  );

  // 3. Logical AND (&&) - render only if true
  const notification = items.length > 0 && (
    <p>You have {items.length} items</p>
  );

  // 4. Logical OR (||) - fallback value
  const username = null;
  const displayName = username || 'Anonymous';

  // 5. Nullish coalescing (??) - only null/undefined fallback
  const count = 0;
  const displayCount = count ?? 'No count'; // Shows 0, not "No count"

  return (
    <div>
      <h1>Conditional Rendering</h1>
      
      {/* Ternary */}
      {greeting}
      <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
        {isLoggedIn ? 'Logout' : 'Login'}
      </button>

      {/* Function-based rendering */}
      <div>Score: {score} - {renderGrade()}</div>
      <input 
        type="range" 
        min="0" 
        max="100" 
        value={score}
        onChange={(e) => setScore(Number(e.target.value))}
      />

      {/* Logical AND */}
      {notification}

      {/* Short-circuit evaluation warning */}
      {/* BAD: {count && <p>Count: {count}</p>} - renders 0 */}
      {/* GOOD: */}
      {count > 0 && <p>Count: {count}</p>}

      {/* Display name with fallback */}
      <p>User: {displayName}</p>
    </div>
  );
}

export default ConditionalRendering;
```

### Switch-like Patterns

Create `src/SwitchPatterns.js`:
```jsx
import React, { useState } from 'react';

// Switch-like patterns in React
function SwitchPatterns() {
  const [status, setStatus] = useState('loading');
  const [tab, setTab] = useState('home');

  // 1. Object lookup (preferred over switch)
  const statusMessages = {
    loading: <p>⏳ Loading...</p>,
    success: <p>✅ Data loaded successfully!</p>,
    error: <p>❌ Error loading data</p>,
    idle: <p>💤 Waiting to start</p>,
  };

  // 2. Function with switch (when you need logic)
  const renderStatusIcon = (currentStatus) => {
    switch (currentStatus) {
      case 'loading':
        return '⏳';
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '❓';
    }
  };

  // 3. Component mapping
  const TabContent = {
    home: () => <div><h2>Home</h2><p>Welcome to the home page</p></div>,
    about: () => <div><h2>About</h2><p>Learn about us</p></div>,
    contact: () => <div><h2>Contact</h2><p>Get in touch</p></div>,
  };

  const CurrentTab = TabContent[tab] || (() => <div>Not found</div>);

  return (
    <div>
      <h1>Switch Patterns</h1>

      {/* Object lookup */}
      <section>
        <h3>Status: {renderStatusIcon(status)} {status}</h3>
        {statusMessages[status] || <p>Unknown status</p>}
        <div>
          <button onClick={() => setStatus('loading')}>Loading</button>
          <button onClick={() => setStatus('success')}>Success</button>
          <button onClick={() => setStatus('error')}>Error</button>
        </div>
      </section>

      {/* Tab component mapping */}
      <section>
        <nav>
          <button onClick={() => setTab('home')}>Home</button>
          <button onClick={() => setTab('about')}>About</button>
          <button onClick={() => setTab('contact')}>Contact</button>
        </nav>
        <CurrentTab />
      </section>
    </div>
  );
}

export default SwitchPatterns;
```

### Loops and Lists

Create `src/LoopsAndLists.js`:
```jsx
import React, { useState } from 'react';

function LoopsAndLists() {
  const [items, setItems] = useState([
    { id: 1, name: 'Learn React', completed: true },
    { id: 2, name: 'Build a project', completed: false },
    { id: 3, name: 'Deploy to production', completed: false },
  ]);

  const [newItem, setNewItem] = useState('');

  // 1. Basic map (most common loop in React)
  const renderBasicList = () => (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );

  // 2. Map with index (use when no unique id)
  const numbers = [10, 20, 30, 40, 50];
  const renderNumbersWithIndex = () => (
    <ul>
      {numbers.map((num, index) => (
        <li key={index}>Index {index}: {num}</li>
      ))}
    </ul>
  );

  // 3. Filter + Map (chaining)
  const completedItems = items
    .filter((item) => item.completed)
    .map((item) => <li key={item.id}>✅ {item.name}</li>);

  // 4. Reduce for complex transformations
  const groupedByStatus = items.reduce((acc, item) => {
    const key = item.completed ? 'completed' : 'pending';
    return { ...acc, [key]: [...(acc[key] || []), item] };
  }, {});

  // 5. Nested loops
  const matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
  ];

  // 6. Object iteration
  const user = { name: 'John', age: 30, city: 'NYC' };

  // Add item handler
  const addItem = () => {
    if (newItem.trim()) {
      setItems([
        ...items,
        { id: Date.now(), name: newItem, completed: false },
      ]);
      setNewItem('');
    }
  };

  // Toggle item
  const toggleItem = (id) => {
    setItems(items.map((item) =>
      item.id === id ? { ...item, completed: !item.completed } : item
    ));
  };

  // Remove item
  const removeItem = (id) => {
    setItems(items.filter((item) => item.id !== id));
  };

  return (
    <div>
      <h1>Loops and Lists</h1>

      {/* Basic list */}
      <section>
        <h3>Basic Map</h3>
        {renderBasicList()}
      </section>

      {/* Numbers with index */}
      <section>
        <h3>Map with Index</h3>
        {renderNumbersWithIndex()}
      </section>

      {/* Filtered list */}
      <section>
        <h3>Completed Items (Filter + Map)</h3>
        <ul>{completedItems.length > 0 ? completedItems : <li>None</li>}</ul>
      </section>

      {/* Interactive todo */}
      <section>
        <h3>Interactive Todo</h3>
        <input
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="New item"
          onKeyPress={(e) => e.key === 'Enter' && addItem()}
        />
        <button onClick={addItem}>Add</button>
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <input
                type="checkbox"
                checked={item.completed}
                onChange={() => toggleItem(item.id)}
              />
              <span style={{
                textDecoration: item.completed ? 'line-through' : 'none'
              }}>
                {item.name}
              </span>
              <button onClick={() => removeItem(item.id)}>🗑️</button>
            </li>
          ))}
        </ul>
      </section>

      {/* Nested loops (matrix) */}
      <section>
        <h3>Nested Loops (Matrix)</h3>
        <table style={{ borderCollapse: 'collapse' }}>
          <tbody>
            {matrix.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((cell, colIndex) => (
                  <td key={colIndex} style={{ border: '1px solid black', padding: '10px' }}>
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Object iteration */}
      <section>
        <h3>Object Iteration</h3>
        <ul>
          {Object.entries(user).map(([key, value]) => (
            <li key={key}><strong>{key}:</strong> {value}</li>
          ))}
        </ul>
      </section>

      {/* Grouped data */}
      <section>
        <h3>Grouped Items</h3>
        {Object.entries(groupedByStatus).map(([status, statusItems]) => (
          <div key={status}>
            <h4>{status.toUpperCase()} ({statusItems.length})</h4>
            <ul>
              {statusItems.map((item) => (
                <li key={item.id}>{item.name}</li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    </div>
  );
}

export default LoopsAndLists;
```

### Update App.js

Update `src/App.js`:
```jsx
import React from 'react';
import ConditionalRendering from './ControlFlow';
import SwitchPatterns from './SwitchPatterns';
import LoopsAndLists from './LoopsAndLists';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>React Control Flow Examples</h1>
      <hr />
      <ConditionalRendering />
      <hr />
      <SwitchPatterns />
      <hr />
      <LoopsAndLists />
    </div>
  );
}

export default App;
```

### Run React Examples
```powershell
npm start
```

---

## 🎯 Key Differences Summary

| Feature | C# | Go | Python | JavaScript |
|---------|----|----|--------|------------|
| **If/Else** | Parentheses required | No parentheses | Colons, indentation | Parentheses required |
| **Switch** | `switch/case/break` | `switch/case` (no break) | `match/case` (3.10+) | `switch/case/break` |
| **Ternary** | `? :` | No ternary | `if else` expression | `? :` |
| **For** | `for(;;)` | `for {}` | `for in` / `range()` | `for(;;)` / `for of` |
| **Foreach** | `foreach` | `for range` | `for in` | `for of` / `.map()` |
| **While** | `while` / `do-while` | `for` (condition only) | `while` | `while` / `do-while` |
| **Labels** | `goto` (discouraged) | Labeled `break/continue` | None (use flag) | Labeled `break/continue` |

---

## ✅ Exercises

### Exercise 1: FizzBuzz
Implement FizzBuzz (1-100) in all four languages:
- Print "Fizz" for multiples of 3
- Print "Buzz" for multiples of 5
- Print "FizzBuzz" for multiples of both
- Print the number otherwise

### Exercise 2: Grade Calculator
Create a grade calculator that:
- Takes a score (0-100)
- Returns letter grade with +/- modifiers
- Handles invalid input gracefully

### Exercise 3: Menu System
Build an interactive menu system using switch/match that:
- Displays options
- Handles user selection
- Loops until user exits

### Exercise 4: Search in Array
Implement a search that:
- Finds an item in an array/list
- Uses break when found
- Reports if not found (use else clause where available)

---

## 📚 Best Practices

1. **Prefer early returns** - Reduces nesting
2. **Use guard clauses** - Handle edge cases first
3. **Avoid deep nesting** - Extract to functions
4. **Use meaningful conditions** - `isValid` vs `flag == true`
5. **Consider switch/match for 3+ conditions**
6. **Always use `key` prop in React loops**
7. **Prefer `for range` in Go over classic for**
8. **Use list comprehensions in Python for simple transforms**
9. **Avoid `goto` in C# unless absolutely necessary**
10. **Use object lookup instead of switch in JavaScript**
