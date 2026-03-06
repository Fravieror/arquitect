# 📘 Lesson 1: Variables, Data Types, and Operators

## 🎯 Learning Objectives
By the end of this lesson, you will understand:
- How to declare and initialize variables
- Primitive and complex data types
- Type inference and type safety
- Arithmetic, comparison, logical, and assignment operators
- Type conversion and casting

---

## 🛠️ Environment Setup

### Prerequisites - Run these commands:

**C# (.NET SDK)**
```powershell
# Check if .NET is installed
dotnet --version

# If not installed, download from https://dotnet.microsoft.com/download
# Create a new console project
mkdir CSharpTraining
cd CSharpTraining
dotnet new console -n Lesson1
cd Lesson1
```

**Go**
```powershell
# Check if Go is installed
go version

# If not installed, download from https://go.dev/dl/
# Create project folder
mkdir GoTraining
cd GoTraining
go mod init lesson1
```

**Python**
```powershell
# Check if Python is installed
python --version

# If not installed, download from https://python.org
# Create project folder
mkdir PythonTraining
cd PythonTraining
```

**React (Node.js)**
```powershell
# Check if Node.js is installed
node --version

# If not installed, download from https://nodejs.org
# Create React app
npx create-react-app react-training
cd react-training
```

---

## 📚 PART 1: VARIABLES

### 🔷 What is a Variable?
A variable is a named storage location in memory that holds a value. Think of it as a labeled box where you can store data.

### 🔷 Variable Declaration & Initialization

---

### C# Variables

Open `Program.cs` and type:

```csharp
// C# - Strongly typed, requires type declaration or 'var' for inference

using System;

class Program
{
    static void Main()
    {
        // Explicit type declaration
        string name = "John";
        int age = 30;
        double salary = 75000.50;
        bool isEmployed = true;
        char grade = 'A';

        // Type inference with 'var' (compiler determines type)
        var city = "New York";      // Inferred as string
        var count = 100;            // Inferred as int
        var price = 19.99;          // Inferred as double

        // Constants (immutable)
        const double PI = 3.14159;
        const string COMPANY = "TechCorp";

        // Nullable types (can hold null)
        int? nullableAge = null;
        string? nullableName = null;

        // Print all variables
        Console.WriteLine($"Name: {name}");
        Console.WriteLine($"Age: {age}");
        Console.WriteLine($"Salary: {salary}");
        Console.WriteLine($"Employed: {isEmployed}");
        Console.WriteLine($"Grade: {grade}");
        Console.WriteLine($"City: {city}");
        Console.WriteLine($"PI: {PI}");
        Console.WriteLine($"Nullable Age: {nullableAge ?? 0}");
    }
}
```

**Run:**
```powershell
dotnet run
```

---

### Go Variables

Create `main.go` and type:

```go
// Go - Statically typed with type inference

package main

import "fmt"

func main() {
    // Explicit type declaration
    var name string = "John"
    var age int = 30
    var salary float64 = 75000.50
    var isEmployed bool = true

    // Short declaration with := (type inference)
    city := "New York"      // Inferred as string
    count := 100            // Inferred as int
    price := 19.99          // Inferred as float64

    // Constants
    const PI float64 = 3.14159
    const COMPANY = "TechCorp"

    // Multiple variable declaration
    var (
        firstName = "Jane"
        lastName  = "Doe"
        score     = 95
    )

    // Zero values (Go initializes unassigned variables)
    var uninitializedInt int     // 0
    var uninitializedString string // "" (empty string)
    var uninitializedBool bool   // false

    // Print all variables
    fmt.Printf("Name: %s\n", name)
    fmt.Printf("Age: %d\n", age)
    fmt.Printf("Salary: %.2f\n", salary)
    fmt.Printf("Employed: %t\n", isEmployed)
    fmt.Printf("City: %s\n", city)
    fmt.Printf("PI: %f\n", PI)
    fmt.Printf("Full Name: %s %s, Score: %d\n", firstName, lastName, score)
    fmt.Printf("Uninitialized: int=%d, string='%s', bool=%t\n", 
        uninitializedInt, uninitializedString, uninitializedBool)
}
```

**Run:**
```powershell
go run main.go
```

---

### Python Variables

Create `lesson1.py` and type:

```python
# Python - Dynamically typed, no type declaration required

# Basic variable assignment (type is inferred at runtime)
name = "John"
age = 30
salary = 75000.50
is_employed = True
grade = 'A'

# Python doesn't have constants, but convention uses UPPERCASE
PI = 3.14159
COMPANY = "TechCorp"

# Type hints (Python 3.5+) - Optional but recommended for clarity
name_typed: str = "Jane"
age_typed: int = 25
salary_typed: float = 65000.00
is_active: bool = False

# Multiple assignment
x, y, z = 1, 2, 3
a = b = c = 0  # All equal to 0

# None (Python's null)
nullable_value = None

# Dynamic typing - variable can change type
dynamic_var = 10          # int
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")

dynamic_var = "Hello"     # now it's a string
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")

dynamic_var = [1, 2, 3]   # now it's a list
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")

# Print all variables
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Salary: {salary}")
print(f"Employed: {is_employed}")
print(f"PI: {PI}")
print(f"x, y, z: {x}, {y}, {z}")
print(f"Nullable: {nullable_value}")

# Check types
print(f"\nType checking:")
print(f"name type: {type(name)}")
print(f"age type: {type(age)}")
print(f"salary type: {type(salary)}")
print(f"is_employed type: {type(is_employed)}")
```

**Run:**
```powershell
python lesson1.py
```

---

### React/JavaScript Variables

Open `src/App.js` and replace with:

```jsx
// React/JavaScript - Dynamically typed

import React from 'react';

function App() {
  // var - function scoped, hoisted (avoid in modern JS)
  var oldStyleVar = "I'm using var";

  // let - block scoped, can be reassigned
  let name = "John";
  let age = 30;
  let salary = 75000.50;
  let isEmployed = true;

  // const - block scoped, cannot be reassigned (use for constants)
  const PI = 3.14159;
  const COMPANY = "TechCorp";

  // const with objects/arrays (reference is constant, content can change)
  const person = { firstName: "Jane", lastName: "Doe" };
  const numbers = [1, 2, 3, 4, 5];

  // Template literals
  const greeting = `Hello, ${name}! You are ${age} years old.`;

  // null and undefined
  let nullValue = null;           // Intentionally empty
  let undefinedValue;             // Not assigned = undefined
  
  // Destructuring assignment
  const { firstName, lastName } = person;
  const [first, second, ...rest] = numbers;

  // TypeScript-style (if using TypeScript)
  // let typedName: string = "John";
  // let typedAge: number = 30;

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>JavaScript Variables Demo</h1>
      
      <h2>Basic Variables</h2>
      <p>Name: {name}</p>
      <p>Age: {age}</p>
      <p>Salary: ${salary.toFixed(2)}</p>
      <p>Employed: {isEmployed.toString()}</p>
      
      <h2>Constants</h2>
      <p>PI: {PI}</p>
      <p>Company: {COMPANY}</p>
      
      <h2>Template Literal</h2>
      <p>{greeting}</p>
      
      <h2>Object & Array</h2>
      <p>Person: {firstName} {lastName}</p>
      <p>Numbers: {numbers.join(', ')}</p>
      
      <h2>Destructuring</h2>
      <p>First: {first}, Second: {second}</p>
      <p>Rest: {rest.join(', ')}</p>
      
      <h2>Null & Undefined</h2>
      <p>Null value: {String(nullValue)}</p>
      <p>Undefined value: {String(undefinedValue)}</p>
      
      <h2>Type Checking</h2>
      <p>typeof name: {typeof name}</p>
      <p>typeof age: {typeof age}</p>
      <p>typeof isEmployed: {typeof isEmployed}</p>
      <p>typeof person: {typeof person}</p>
      <p>typeof numbers: {typeof numbers} (Array.isArray: {Array.isArray(numbers).toString()})</p>
    </div>
  );
}

export default App;
```

**Run:**
```powershell
npm start
```

---

## 📚 PART 2: DATA TYPES

### 🔷 Primitive vs Reference Types

| Language | Primitive Types | Reference Types |
|----------|-----------------|-----------------|
| **C#** | int, double, bool, char, byte, short, long, float, decimal | string, object, arrays, classes |
| **Go** | int, float64, bool, string, byte, rune | slices, maps, structs, pointers, channels |
| **Python** | int, float, bool, str, None | list, dict, tuple, set, objects |
| **JavaScript** | number, string, boolean, null, undefined, symbol, bigint | object, array, function |

---

### C# Data Types

Add to `Program.cs`:

```csharp
using System;
using System.Collections.Generic;

class DataTypesDemo
{
    static void Main()
    {
        Console.WriteLine("=== C# DATA TYPES ===\n");

        // INTEGER TYPES
        Console.WriteLine("-- Integer Types --");
        sbyte signedByte = -128;              // -128 to 127
        byte unsignedByte = 255;              // 0 to 255
        short shortNum = -32768;              // -32,768 to 32,767
        ushort ushortNum = 65535;             // 0 to 65,535
        int intNum = -2147483648;             // -2.1B to 2.1B
        uint uintNum = 4294967295;            // 0 to 4.2B
        long longNum = -9223372036854775808;  // -9.2 quintillion to 9.2 quintillion
        ulong ulongNum = 18446744073709551615;// 0 to 18.4 quintillion

        Console.WriteLine($"sbyte: {signedByte}, Range: {sbyte.MinValue} to {sbyte.MaxValue}");
        Console.WriteLine($"int: {intNum}, Range: {int.MinValue} to {int.MaxValue}");
        Console.WriteLine($"long: {longNum}");

        // FLOATING-POINT TYPES
        Console.WriteLine("\n-- Floating-Point Types --");
        float floatNum = 3.14159f;            // 7 digits precision
        double doubleNum = 3.141592653589793; // 15-17 digits precision
        decimal decimalNum = 3.14159265358979323846m; // 28-29 digits (financial)

        Console.WriteLine($"float: {floatNum} (Precision: ~7 digits)");
        Console.WriteLine($"double: {doubleNum} (Precision: ~15 digits)");
        Console.WriteLine($"decimal: {decimalNum} (Precision: ~28 digits)");

        // CHARACTER & STRING
        Console.WriteLine("\n-- Character & String Types --");
        char singleChar = 'A';
        char unicodeChar = '\u0041';  // Unicode for 'A'
        string text = "Hello, World!";
        string verbatim = @"C:\Users\Path\File.txt";  // Verbatim string
        string interpolated = $"The answer is {40 + 2}";
        string multiline = """
            This is a
            multiline string
            in C# 11+
            """;

        Console.WriteLine($"char: {singleChar}");
        Console.WriteLine($"unicode: {unicodeChar}");
        Console.WriteLine($"string: {text}");
        Console.WriteLine($"verbatim: {verbatim}");
        Console.WriteLine($"interpolated: {interpolated}");

        // BOOLEAN
        Console.WriteLine("\n-- Boolean Type --");
        bool isTrue = true;
        bool isFalse = false;
        Console.WriteLine($"bool: {isTrue}, {isFalse}");

        // ARRAYS
        Console.WriteLine("\n-- Arrays --");
        int[] numbers = { 1, 2, 3, 4, 5 };
        string[] names = new string[3] { "Alice", "Bob", "Charlie" };
        int[,] matrix = { { 1, 2 }, { 3, 4 }, { 5, 6 } };

        Console.WriteLine($"Array: [{string.Join(", ", numbers)}]");
        Console.WriteLine($"2D Array: {matrix[0, 0]}, {matrix[1, 1]}");

        // COLLECTIONS
        Console.WriteLine("\n-- Collections --");
        List<int> list = new List<int> { 1, 2, 3 };
        Dictionary<string, int> dict = new Dictionary<string, int>
        {
            { "one", 1 },
            { "two", 2 }
        };
        HashSet<int> set = new HashSet<int> { 1, 2, 2, 3 }; // Duplicates removed

        Console.WriteLine($"List: [{string.Join(", ", list)}]");
        Console.WriteLine($"Dict: one={dict["one"]}, two={dict["two"]}");
        Console.WriteLine($"Set: [{string.Join(", ", set)}]");

        // NULLABLE TYPES
        Console.WriteLine("\n-- Nullable Types --");
        int? nullableInt = null;
        int valueOrDefault = nullableInt ?? 0;  // Null coalescing
        Console.WriteLine($"Nullable: {nullableInt}, Default: {valueOrDefault}");

        // TUPLES
        Console.WriteLine("\n-- Tuples --");
        var tuple = (Name: "John", Age: 30, Salary: 50000.0);
        Console.WriteLine($"Tuple: {tuple.Name}, {tuple.Age}, {tuple.Salary}");

        // ENUMS
        Console.WriteLine("\n-- Enums --");
        DayOfWeek today = DayOfWeek.Wednesday;
        Console.WriteLine($"Enum: {today} = {(int)today}");

        // TYPE CHECKING
        Console.WriteLine("\n-- Type Checking --");
        object obj = "Hello";
        Console.WriteLine($"obj is string: {obj is string}");
        Console.WriteLine($"Type: {obj.GetType()}");
    }
}

enum DayOfWeek { Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday }
```

**Run:**
```powershell
dotnet run
```

---

### Go Data Types

Replace `main.go` with:

```go
package main

import (
    "fmt"
    "math"
    "reflect"
)

func main() {
    fmt.Println("=== GO DATA TYPES ===\n")

    // INTEGER TYPES
    fmt.Println("-- Integer Types --")
    var i8 int8 = -128                   // -128 to 127
    var ui8 uint8 = 255                  // 0 to 255 (alias: byte)
    var i16 int16 = -32768               // -32,768 to 32,767
    var ui16 uint16 = 65535              // 0 to 65,535
    var i32 int32 = -2147483648          // -2.1B to 2.1B (alias: rune)
    var ui32 uint32 = 4294967295         // 0 to 4.2B
    var i64 int64 = -9223372036854775808 // -9.2 quintillion to 9.2 quintillion
    var ui64 uint64 = 18446744073709551615
    var platformInt int = 42             // Platform dependent (32 or 64 bit)

    fmt.Printf("int8: %d, Range: %d to %d\n", i8, math.MinInt8, math.MaxInt8)
    fmt.Printf("int32: %d\n", i32)
    fmt.Printf("int64: %d\n", i64)
    fmt.Printf("uint64: %d\n", ui64)
    fmt.Printf("int (platform): %d\n", platformInt)
    _ = ui8
    _ = i16
    _ = ui16
    _ = ui32

    // FLOATING-POINT TYPES
    fmt.Println("\n-- Floating-Point Types --")
    var f32 float32 = 3.14159            // 32-bit
    var f64 float64 = 3.141592653589793  // 64-bit (default for floats)

    fmt.Printf("float32: %f (Precision: ~7 digits)\n", f32)
    fmt.Printf("float64: %.15f (Precision: ~15 digits)\n", f64)

    // COMPLEX NUMBERS
    fmt.Println("\n-- Complex Numbers --")
    var c64 complex64 = 3 + 4i
    var c128 complex128 = 3.5 + 4.5i

    fmt.Printf("complex64: %v\n", c64)
    fmt.Printf("complex128: %v, Real: %f, Imag: %f\n", c128, real(c128), imag(c128))

    // BOOLEAN
    fmt.Println("\n-- Boolean Type --")
    var isTrue bool = true
    var isFalse bool = false
    fmt.Printf("bool: %t, %t\n", isTrue, isFalse)

    // STRING & RUNE
    fmt.Println("\n-- String & Rune Types --")
    var str string = "Hello, World!"
    var rawStr string = `C:\Users\Path\File.txt`  // Raw string
    var char rune = 'A'                            // Unicode code point (alias for int32)
    var byteVal byte = 65                          // ASCII value (alias for uint8)

    fmt.Printf("string: %s\n", str)
    fmt.Printf("raw string: %s\n", rawStr)
    fmt.Printf("rune: %c (value: %d)\n", char, char)
    fmt.Printf("byte: %c (value: %d)\n", byteVal, byteVal)
    fmt.Printf("string length: %d bytes, %d runes\n", len(str), len([]rune(str)))

    // ARRAYS (Fixed size)
    fmt.Println("\n-- Arrays (Fixed Size) --")
    var arr [5]int = [5]int{1, 2, 3, 4, 5}
    shortArr := [...]int{10, 20, 30}  // Size inferred

    fmt.Printf("Array: %v, Length: %d\n", arr, len(arr))
    fmt.Printf("Short Array: %v\n", shortArr)

    // SLICES (Dynamic size)
    fmt.Println("\n-- Slices (Dynamic) --")
    slice := []int{1, 2, 3, 4, 5}
    slice = append(slice, 6, 7)           // Append elements
    subSlice := slice[1:4]                // Slicing [start:end)

    fmt.Printf("Slice: %v, Len: %d, Cap: %d\n", slice, len(slice), cap(slice))
    fmt.Printf("SubSlice [1:4]: %v\n", subSlice)

    // MAPS
    fmt.Println("\n-- Maps --")
    ages := map[string]int{
        "Alice": 30,
        "Bob":   25,
    }
    ages["Charlie"] = 35  // Add new entry

    fmt.Printf("Map: %v\n", ages)
    fmt.Printf("Alice's age: %d\n", ages["Alice"])

    // Check if key exists
    if age, exists := ages["David"]; exists {
        fmt.Printf("David's age: %d\n", age)
    } else {
        fmt.Println("David not found")
    }

    // STRUCTS
    fmt.Println("\n-- Structs --")
    type Person struct {
        Name string
        Age  int
        City string
    }

    person := Person{Name: "John", Age: 30, City: "NYC"}
    fmt.Printf("Struct: %+v\n", person)
    fmt.Printf("Name: %s, Age: %d\n", person.Name, person.Age)

    // POINTERS
    fmt.Println("\n-- Pointers --")
    value := 42
    pointer := &value        // Get address
    fmt.Printf("Value: %d, Pointer: %p, Dereferenced: %d\n", value, pointer, *pointer)

    *pointer = 100           // Modify via pointer
    fmt.Printf("Modified value: %d\n", value)

    // TYPE CHECKING
    fmt.Println("\n-- Type Checking --")
    var x interface{} = "Hello"
    fmt.Printf("Type of x: %T\n", x)
    fmt.Printf("Reflect type: %s\n", reflect.TypeOf(x))

    // Type assertion
    if s, ok := x.(string); ok {
        fmt.Printf("x is string: %s\n", s)
    }
}
```

**Run:**
```powershell
go run main.go
```

---

### Python Data Types

Replace `lesson1.py` with:

```python
# Python Data Types Demo
import sys
from decimal import Decimal
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional

print("=== PYTHON DATA TYPES ===\n")

# INTEGER (unlimited precision in Python 3)
print("-- Integer Type --")
small_int = 42
big_int = 99999999999999999999999999999999  # No overflow!
negative = -100
binary = 0b1010      # Binary: 10
octal = 0o17         # Octal: 15
hexadecimal = 0xFF   # Hex: 255

print(f"small_int: {small_int}")
print(f"big_int: {big_int}")
print(f"binary 0b1010: {binary}")
print(f"hex 0xFF: {hexadecimal}")
print(f"sys.maxsize: {sys.maxsize}")

# FLOAT (64-bit double precision)
print("\n-- Float Type --")
float_num = 3.14159
scientific = 2.5e-3   # 0.0025
infinity = float('inf')
neg_infinity = float('-inf')
not_a_number = float('nan')

print(f"float: {float_num}")
print(f"scientific 2.5e-3: {scientific}")
print(f"infinity: {infinity}")
print(f"nan: {not_a_number}")

# DECIMAL (precise decimal arithmetic)
print("\n-- Decimal Type (for financial calculations) --")
decimal_num = Decimal('3.14159265358979323846')
print(f"Decimal: {decimal_num}")
print(f"0.1 + 0.2 (float): {0.1 + 0.2}")  # Floating point error!
print(f"0.1 + 0.2 (Decimal): {Decimal('0.1') + Decimal('0.2')}")

# FRACTION
print("\n-- Fraction Type --")
frac = Fraction(1, 3)
print(f"Fraction 1/3: {frac}")
print(f"Fraction as float: {float(frac)}")

# COMPLEX
print("\n-- Complex Type --")
complex_num = 3 + 4j
print(f"Complex: {complex_num}")
print(f"Real: {complex_num.real}, Imaginary: {complex_num.imag}")
print(f"Conjugate: {complex_num.conjugate()}")

# BOOLEAN
print("\n-- Boolean Type --")
is_true = True
is_false = False
print(f"Boolean: {is_true}, {is_false}")
print(f"True as int: {int(True)}")   # 1
print(f"False as int: {int(False)}") # 0

# Truthy/Falsy values
print(f"bool(''): {bool('')}")       # False
print(f"bool('text'): {bool('text')}")  # True
print(f"bool(0): {bool(0)}")         # False
print(f"bool(42): {bool(42)}")       # True
print(f"bool([]): {bool([])}")       # False
print(f"bool([1]): {bool([1])}")     # True

# STRING
print("\n-- String Type --")
single = 'Hello'
double = "World"
multiline = """This is a
multiline string"""
raw = r"C:\Users\Path\File.txt"  # Raw string (no escape)
formatted = f"Sum: {2 + 2}"

print(f"String: {single} {double}")
print(f"Raw: {raw}")
print(f"Formatted: {formatted}")
print(f"Length: {len(single)}")
print(f"Slicing [1:4]: {single[1:4]}")
print(f"Uppercase: {single.upper()}")

# NONE
print("\n-- None Type --")
nothing = None
print(f"None: {nothing}")
print(f"None is None: {nothing is None}")

# LIST (mutable, ordered)
print("\n-- List Type --")
numbers: List[int] = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True]
nested = [[1, 2], [3, 4], [5, 6]]

numbers.append(6)
numbers.extend([7, 8])
print(f"List: {numbers}")
print(f"Mixed: {mixed}")
print(f"Nested[0][1]: {nested[0][1]}")
print(f"List comprehension: {[x**2 for x in range(5)]}")

# TUPLE (immutable, ordered)
print("\n-- Tuple Type --")
coordinates: Tuple[int, int, int] = (10, 20, 30)
single_tuple = (42,)  # Single element needs comma
x, y, z = coordinates  # Unpacking

print(f"Tuple: {coordinates}")
print(f"Unpacked: x={x}, y={y}, z={z}")

# DICTIONARY (mutable, key-value pairs)
print("\n-- Dictionary Type --")
person: Dict[str, any] = {
    "name": "John",
    "age": 30,
    "city": "NYC"
}
person["country"] = "USA"  # Add new key

print(f"Dict: {person}")
print(f"Name: {person['name']}")
print(f"Get with default: {person.get('salary', 0)}")
print(f"Keys: {list(person.keys())}")
print(f"Values: {list(person.values())}")

# SET (mutable, unique elements, unordered)
print("\n-- Set Type --")
unique: Set[int] = {1, 2, 3, 2, 1}  # Duplicates removed
set_a = {1, 2, 3}
set_b = {3, 4, 5}

print(f"Set (duplicates removed): {unique}")
print(f"Union: {set_a | set_b}")
print(f"Intersection: {set_a & set_b}")
print(f"Difference: {set_a - set_b}")

# FROZENSET (immutable set)
print("\n-- FrozenSet Type --")
frozen = frozenset([1, 2, 3])
print(f"FrozenSet: {frozen}")

# BYTES & BYTEARRAY
print("\n-- Bytes Type --")
byte_str = b"Hello"
byte_array = bytearray(b"World")
print(f"Bytes: {byte_str}")
print(f"ByteArray: {byte_array}")

# TYPE CHECKING
print("\n-- Type Checking --")
print(f"type(42): {type(42)}")
print(f"type('hello'): {type('hello')}")
print(f"isinstance(42, int): {isinstance(42, int)}")
print(f"isinstance('hello', (str, int)): {isinstance('hello', (str, int))}")

# OPTIONAL (Type Hints)
def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, Guest!"
    return f"Hello, {name}!"

print(f"\nOptional: {greet()}")
print(f"Optional: {greet('Alice')}")
```

**Run:**
```powershell
python lesson1.py
```

---

### React/JavaScript Data Types

Replace `src/App.js` with:

```jsx
import React from 'react';

function App() {
  // NUMBER (64-bit floating point)
  const integer = 42;
  const float = 3.14159;
  const negative = -100;
  const binary = 0b1010;      // Binary: 10
  const octal = 0o17;         // Octal: 15
  const hex = 0xFF;           // Hex: 255
  const scientific = 2.5e-3;  // 0.0025
  const maxSafe = Number.MAX_SAFE_INTEGER;
  const infinity = Infinity;
  const notANumber = NaN;

  // BIGINT (arbitrary precision integers)
  const bigInt = 9007199254740991n;
  const bigIntFromString = BigInt("99999999999999999999");

  // STRING
  const singleQuote = 'Hello';
  const doubleQuote = "World";
  const template = `Sum: ${2 + 2}`;
  const multiline = `Line 1
Line 2
Line 3`;

  // BOOLEAN
  const isTrue = true;
  const isFalse = false;

  // NULL & UNDEFINED
  const nullValue = null;
  let undefinedValue;       // Implicitly undefined
  const explicitUndefined = undefined;

  // SYMBOL (unique identifier)
  const sym1 = Symbol('description');
  const sym2 = Symbol('description');
  const symbolsEqual = sym1 === sym2;  // false - always unique

  // OBJECT
  const person = {
    name: 'John',
    age: 30,
    city: 'NYC',
    greet() {
      return `Hello, I'm ${this.name}`;
    }
  };

  // ARRAY
  const numbers = [1, 2, 3, 4, 5];
  const mixed = [1, 'two', true, null, { key: 'value' }];
  const nested = [[1, 2], [3, 4]];

  // Array methods
  const doubled = numbers.map(n => n * 2);
  const evens = numbers.filter(n => n % 2 === 0);
  const sum = numbers.reduce((a, b) => a + b, 0);

  // FUNCTION (first-class citizen)
  const add = (a, b) => a + b;
  const multiply = function(a, b) { return a * b; };

  // MAP (key-value pairs, any type as key)
  const map = new Map();
  map.set('name', 'John');
  map.set(42, 'answer');
  map.set({ id: 1 }, 'object key');

  // SET (unique values)
  const set = new Set([1, 2, 2, 3, 3, 3]);

  // DATE
  const now = new Date();
  const specificDate = new Date('2026-02-27');

  // REGEXP
  const regex = /hello/gi;
  const regexMatch = 'Hello World'.match(regex);

  // TYPE COERCION (implicit)
  const coercion1 = '5' + 3;      // '53' (string)
  const coercion2 = '5' - 3;      // 2 (number)
  const coercion3 = '5' * '2';    // 10 (number)
  const coercion4 = true + true;  // 2 (number)

  // TYPE CHECKING
  const typeChecks = {
    number: typeof 42,
    string: typeof 'hello',
    boolean: typeof true,
    undefined: typeof undefined,
    null: typeof null,              // 'object' (JS quirk!)
    object: typeof {},
    array: typeof [],               // 'object'
    function: typeof (() => {}),
    symbol: typeof Symbol(),
  };

  // TRUTHY & FALSY
  const falsyValues = [false, 0, -0, 0n, '', null, undefined, NaN];
  const truthyExamples = [true, 1, -1, 'text', [], {}, () => {}];

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', maxWidth: '900px' }}>
      <h1>JavaScript Data Types Demo</h1>

      <h2>Number</h2>
      <pre>
{`integer: ${integer}
float: ${float}
binary 0b1010: ${binary}
hex 0xFF: ${hex}
scientific 2.5e-3: ${scientific}
MAX_SAFE_INTEGER: ${maxSafe}
Infinity: ${infinity}
NaN: ${notANumber}
isNaN(NaN): ${isNaN(notANumber)}`}
      </pre>

      <h2>BigInt</h2>
      <pre>
{`bigInt: ${bigInt.toString()}
bigIntFromString: ${bigIntFromString.toString()}`}
      </pre>

      <h2>String</h2>
      <pre>
{`single: ${singleQuote}
double: ${doubleQuote}
template: ${template}
length: ${singleQuote.length}
slice(1,4): ${singleQuote.slice(1, 4)}
uppercase: ${singleQuote.toUpperCase()}`}
      </pre>

      <h2>Boolean</h2>
      <pre>
{`true: ${isTrue}
false: ${isFalse}
Boolean(''): ${Boolean('')}
Boolean('text'): ${Boolean('text')}
Boolean(0): ${Boolean(0)}
Boolean(42): ${Boolean(42)}`}
      </pre>

      <h2>Null & Undefined</h2>
      <pre>
{`null: ${String(nullValue)}
undefined: ${String(undefinedValue)}
null === undefined: ${nullValue === undefinedValue}
null == undefined: ${nullValue == undefinedValue}`}
      </pre>

      <h2>Symbol</h2>
      <pre>
{`Symbol('desc') === Symbol('desc'): ${symbolsEqual}`}
      </pre>

      <h2>Object</h2>
      <pre>
{`person: ${JSON.stringify(person, null, 2)}
person.name: ${person.name}
person.greet(): ${person.greet()}`}
      </pre>

      <h2>Array</h2>
      <pre>
{`numbers: [${numbers.join(', ')}]
doubled (map): [${doubled.join(', ')}]
evens (filter): [${evens.join(', ')}]
sum (reduce): ${sum}
Array.isArray(numbers): ${Array.isArray(numbers)}`}
      </pre>

      <h2>Map & Set</h2>
      <pre>
{`Map size: ${map.size}
Map.get('name'): ${map.get('name')}
Set (unique): [${[...set].join(', ')}]`}
      </pre>

      <h2>Date</h2>
      <pre>
{`now: ${now.toISOString()}
specific: ${specificDate.toDateString()}`}
      </pre>

      <h2>Type Coercion</h2>
      <pre>
{`'5' + 3: '${coercion1}'
'5' - 3: ${coercion2}
'5' * '2': ${coercion3}
true + true: ${coercion4}`}
      </pre>

      <h2>typeof Results</h2>
      <pre>
{Object.entries(typeChecks).map(([k, v]) => `typeof ${k}: '${v}'`).join('\n')}
      </pre>

      <h2>Falsy Values</h2>
      <pre>
{`Falsy: ${falsyValues.map(v => String(v)).join(', ')}
All false: ${falsyValues.every(v => !v)}`}
      </pre>
    </div>
  );
}

export default App;
```

**Run:**
```powershell
npm start
```

---

## 📚 PART 3: OPERATORS

### 🔷 Operator Categories

1. **Arithmetic Operators**: `+ - * / % ++ --`
2. **Comparison Operators**: `== != > < >= <=`
3. **Logical Operators**: `&& || !`
4. **Assignment Operators**: `= += -= *= /= %= &= |= ^=`
5. **Bitwise Operators**: `& | ^ ~ << >>`
6. **Ternary Operator**: `condition ? true : false`
7. **Null Operators**: `?? ?.` (null coalescing, optional chaining)

---

### C# Operators

Create a new file or update `Program.cs`:

```csharp
using System;

class OperatorsDemo
{
    static void Main()
    {
        Console.WriteLine("=== C# OPERATORS ===\n");

        // ARITHMETIC OPERATORS
        Console.WriteLine("-- Arithmetic Operators --");
        int a = 10, b = 3;
        Console.WriteLine($"a = {a}, b = {b}");
        Console.WriteLine($"a + b = {a + b}");      // Addition: 13
        Console.WriteLine($"a - b = {a - b}");      // Subtraction: 7
        Console.WriteLine($"a * b = {a * b}");      // Multiplication: 30
        Console.WriteLine($"a / b = {a / b}");      // Division: 3 (integer)
        Console.WriteLine($"a % b = {a % b}");      // Modulus: 1
        Console.WriteLine($"10.0 / 3.0 = {10.0 / 3.0}"); // Float division

        // Increment/Decrement
        int x = 5;
        Console.WriteLine($"\nx = {x}");
        Console.WriteLine($"x++ (post): {x++}");    // Returns 5, then increments
        Console.WriteLine($"x now: {x}");           // 6
        Console.WriteLine($"++x (pre): {++x}");     // Increments, then returns 7
        Console.WriteLine($"--x (pre): {--x}");     // Decrements, then returns 6

        // COMPARISON OPERATORS
        Console.WriteLine("\n-- Comparison Operators --");
        int m = 10, n = 20;
        Console.WriteLine($"m = {m}, n = {n}");
        Console.WriteLine($"m == n: {m == n}");     // Equal: false
        Console.WriteLine($"m != n: {m != n}");     // Not equal: true
        Console.WriteLine($"m > n: {m > n}");       // Greater: false
        Console.WriteLine($"m < n: {m < n}");       // Less: true
        Console.WriteLine($"m >= n: {m >= n}");     // Greater or equal: false
        Console.WriteLine($"m <= n: {m <= n}");     // Less or equal: true

        // LOGICAL OPERATORS
        Console.WriteLine("\n-- Logical Operators --");
        bool p = true, q = false;
        Console.WriteLine($"p = {p}, q = {q}");
        Console.WriteLine($"p && q: {p && q}");     // AND: false
        Console.WriteLine($"p || q: {p || q}");     // OR: true
        Console.WriteLine($"!p: {!p}");             // NOT: false
        Console.WriteLine($"!q: {!q}");             // NOT: true

        // Short-circuit evaluation
        Console.WriteLine($"false && Method(): {false && AlwaysTrue()}"); // Method not called
        Console.WriteLine($"true || Method(): {true || AlwaysFalse()}");  // Method not called

        // ASSIGNMENT OPERATORS
        Console.WriteLine("\n-- Assignment Operators --");
        int v = 10;
        Console.WriteLine($"v = {v}");
        v += 5;  Console.WriteLine($"v += 5: {v}");   // 15
        v -= 3;  Console.WriteLine($"v -= 3: {v}");   // 12
        v *= 2;  Console.WriteLine($"v *= 2: {v}");   // 24
        v /= 4;  Console.WriteLine($"v /= 4: {v}");   // 6
        v %= 4;  Console.WriteLine($"v %= 4: {v}");   // 2

        // BITWISE OPERATORS
        Console.WriteLine("\n-- Bitwise Operators --");
        int bits1 = 0b1100;  // 12
        int bits2 = 0b1010;  // 10
        Console.WriteLine($"bits1 = {bits1} (0b{Convert.ToString(bits1, 2).PadLeft(4, '0')})");
        Console.WriteLine($"bits2 = {bits2} (0b{Convert.ToString(bits2, 2).PadLeft(4, '0')})");
        Console.WriteLine($"AND (&): {bits1 & bits2} (0b{Convert.ToString(bits1 & bits2, 2).PadLeft(4, '0')})");  // 8
        Console.WriteLine($"OR (|): {bits1 | bits2} (0b{Convert.ToString(bits1 | bits2, 2).PadLeft(4, '0')})");   // 14
        Console.WriteLine($"XOR (^): {bits1 ^ bits2} (0b{Convert.ToString(bits1 ^ bits2, 2).PadLeft(4, '0')})");  // 6
        Console.WriteLine($"NOT (~bits1): {~bits1}");
        Console.WriteLine($"Left Shift (bits1 << 2): {bits1 << 2}");  // 48
        Console.WriteLine($"Right Shift (bits1 >> 2): {bits1 >> 2}"); // 3

        // TERNARY OPERATOR
        Console.WriteLine("\n-- Ternary Operator --");
        int age = 18;
        string status = age >= 18 ? "Adult" : "Minor";
        Console.WriteLine($"Age {age}: {status}");

        // Nested ternary
        int score = 85;
        string grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
        Console.WriteLine($"Score {score}: Grade {grade}");

        // NULL OPERATORS
        Console.WriteLine("\n-- Null Operators --");
        string? nullableString = null;
        string result = nullableString ?? "Default Value";  // Null coalescing
        Console.WriteLine($"nullableString ?? 'Default': {result}");

        // Null-conditional operator
        string? name = null;
        int? length = name?.Length;  // Returns null if name is null
        Console.WriteLine($"name?.Length: {length?.ToString() ?? "null"}");

        // Null-coalescing assignment
        string? text = null;
        text ??= "Assigned because null";  // Only assigns if null
        Console.WriteLine($"text ??= '...': {text}");

        // TYPE OPERATORS
        Console.WriteLine("\n-- Type Operators --");
        object obj = "Hello";
        Console.WriteLine($"obj is string: {obj is string}");
        
        if (obj is string str)
        {
            Console.WriteLine($"Pattern matched: {str.ToUpper()}");
        }

        string? castResult = obj as string;  // Safe cast (returns null if fails)
        Console.WriteLine($"obj as string: {castResult}");

        // RANGE & INDEX OPERATORS (C# 8+)
        Console.WriteLine("\n-- Range & Index Operators --");
        int[] arr = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        Console.WriteLine($"arr[^1] (last): {arr[^1]}");           // 9
        Console.WriteLine($"arr[^2] (second last): {arr[^2]}");    // 8
        Console.WriteLine($"arr[2..5]: [{string.Join(", ", arr[2..5])}]");  // 2, 3, 4
        Console.WriteLine($"arr[..3]: [{string.Join(", ", arr[..3])}]");    // 0, 1, 2
        Console.WriteLine($"arr[7..]: [{string.Join(", ", arr[7..])}]");    // 7, 8, 9

        // OPERATOR PRECEDENCE
        Console.WriteLine("\n-- Operator Precedence --");
        int result1 = 2 + 3 * 4;        // 14 (multiplication first)
        int result2 = (2 + 3) * 4;      // 20 (parentheses first)
        Console.WriteLine($"2 + 3 * 4 = {result1}");
        Console.WriteLine($"(2 + 3) * 4 = {result2}");
    }

    static bool AlwaysTrue() { Console.WriteLine("AlwaysTrue called"); return true; }
    static bool AlwaysFalse() { Console.WriteLine("AlwaysFalse called"); return false; }
}
```

**Run:**
```powershell
dotnet run
```

---

### Go Operators

Replace `main.go` with:

```go
package main

import (
    "fmt"
)

func main() {
    fmt.Println("=== GO OPERATORS ===\n")

    // ARITHMETIC OPERATORS
    fmt.Println("-- Arithmetic Operators --")
    a, b := 10, 3
    fmt.Printf("a = %d, b = %d\n", a, b)
    fmt.Printf("a + b = %d\n", a+b)     // Addition: 13
    fmt.Printf("a - b = %d\n", a-b)     // Subtraction: 7
    fmt.Printf("a * b = %d\n", a*b)     // Multiplication: 30
    fmt.Printf("a / b = %d\n", a/b)     // Division: 3 (integer)
    fmt.Printf("a %% b = %d\n", a%b)    // Modulus: 1
    fmt.Printf("10.0 / 3.0 = %f\n", 10.0/3.0) // Float division

    // Increment/Decrement (Go only has post-increment)
    x := 5
    fmt.Printf("\nx = %d\n", x)
    x++
    fmt.Printf("x++ (post): %d\n", x) // 6
    x--
    fmt.Printf("x-- (post): %d\n", x) // 5
    // NOTE: Go doesn't have pre-increment (++x) or use in expressions

    // COMPARISON OPERATORS
    fmt.Println("\n-- Comparison Operators --")
    m, n := 10, 20
    fmt.Printf("m = %d, n = %d\n", m, n)
    fmt.Printf("m == n: %t\n", m == n) // Equal: false
    fmt.Printf("m != n: %t\n", m != n) // Not equal: true
    fmt.Printf("m > n: %t\n", m > n)   // Greater: false
    fmt.Printf("m < n: %t\n", m < n)   // Less: true
    fmt.Printf("m >= n: %t\n", m >= n) // Greater or equal: false
    fmt.Printf("m <= n: %t\n", m <= n) // Less or equal: true

    // LOGICAL OPERATORS
    fmt.Println("\n-- Logical Operators --")
    p, q := true, false
    fmt.Printf("p = %t, q = %t\n", p, q)
    fmt.Printf("p && q: %t\n", p && q) // AND: false
    fmt.Printf("p || q: %t\n", p || q) // OR: true
    fmt.Printf("!p: %t\n", !p)         // NOT: false
    fmt.Printf("!q: %t\n", !q)         // NOT: true

    // Short-circuit evaluation
    fmt.Printf("false && func(): %t\n", false && alwaysTrue()) // func not called
    fmt.Printf("true || func(): %t\n", true || alwaysFalse())  // func not called

    // ASSIGNMENT OPERATORS
    fmt.Println("\n-- Assignment Operators --")
    v := 10
    fmt.Printf("v = %d\n", v)
    v += 5
    fmt.Printf("v += 5: %d\n", v) // 15
    v -= 3
    fmt.Printf("v -= 3: %d\n", v) // 12
    v *= 2
    fmt.Printf("v *= 2: %d\n", v) // 24
    v /= 4
    fmt.Printf("v /= 4: %d\n", v) // 6
    v %= 4
    fmt.Printf("v %%= 4: %d\n", v) // 2

    // BITWISE OPERATORS
    fmt.Println("\n-- Bitwise Operators --")
    bits1 := 0b1100 // 12
    bits2 := 0b1010 // 10
    fmt.Printf("bits1 = %d (%04b)\n", bits1, bits1)
    fmt.Printf("bits2 = %d (%04b)\n", bits2, bits2)
    fmt.Printf("AND (&): %d (%04b)\n", bits1&bits2, bits1&bits2)       // 8
    fmt.Printf("OR (|): %d (%04b)\n", bits1|bits2, bits1|bits2)        // 14
    fmt.Printf("XOR (^): %d (%04b)\n", bits1^bits2, bits1^bits2)       // 6
    fmt.Printf("AND NOT (&^): %d (%04b)\n", bits1&^bits2, bits1&^bits2) // Go-specific: bit clear
    fmt.Printf("Left Shift (<<2): %d\n", bits1<<2)                      // 48
    fmt.Printf("Right Shift (>>2): %d\n", bits1>>2)                     // 3

    // CONDITIONAL EXPRESSION (Go doesn't have ternary operator)
    fmt.Println("\n-- Conditional Expression --")
    age := 18
    var status string
    if age >= 18 {
        status = "Adult"
    } else {
        status = "Minor"
    }
    fmt.Printf("Age %d: %s\n", age, status)

    // Using a function for ternary-like behavior
    score := 85
    grade := ternaryString(score >= 90, "A",
        ternaryString(score >= 80, "B",
            ternaryString(score >= 70, "C", "F")))
    fmt.Printf("Score %d: Grade %s\n", score, grade)

    // POINTER OPERATORS
    fmt.Println("\n-- Pointer Operators --")
    value := 42
    ptr := &value       // Address-of operator
    fmt.Printf("value: %d\n", value)
    fmt.Printf("ptr (address): %p\n", ptr)
    fmt.Printf("*ptr (dereference): %d\n", *ptr)
    *ptr = 100
    fmt.Printf("After *ptr = 100, value: %d\n", value)

    // TYPE ASSERTION
    fmt.Println("\n-- Type Assertion --")
    var i interface{} = "hello"
    
    // Type assertion with ok check
    if s, ok := i.(string); ok {
        fmt.Printf("i is string: %s\n", s)
    }
    
    // Type switch
    switch v := i.(type) {
    case string:
        fmt.Printf("String: %s\n", v)
    case int:
        fmt.Printf("Int: %d\n", v)
    default:
        fmt.Printf("Unknown type: %T\n", v)
    }

    // CHANNEL OPERATORS
    fmt.Println("\n-- Channel Operators --")
    ch := make(chan int, 1)
    ch <- 42           // Send to channel
    received := <-ch   // Receive from channel
    fmt.Printf("Received from channel: %d\n", received)

    // SLICE OPERATORS
    fmt.Println("\n-- Slice Operators --")
    arr := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    fmt.Printf("arr[2:5]: %v\n", arr[2:5])   // [2 3 4]
    fmt.Printf("arr[:3]: %v\n", arr[:3])     // [0 1 2]
    fmt.Printf("arr[7:]: %v\n", arr[7:])     // [7 8 9]
    fmt.Printf("arr[:]: %v\n", arr[:])       // Full copy

    // OPERATOR PRECEDENCE
    fmt.Println("\n-- Operator Precedence --")
    result1 := 2 + 3*4     // 14 (multiplication first)
    result2 := (2 + 3) * 4 // 20 (parentheses first)
    fmt.Printf("2 + 3 * 4 = %d\n", result1)
    fmt.Printf("(2 + 3) * 4 = %d\n", result2)
}

func alwaysTrue() bool {
    fmt.Println("alwaysTrue called")
    return true
}

func alwaysFalse() bool {
    fmt.Println("alwaysFalse called")
    return false
}

// Helper function for ternary-like expressions
func ternaryString(condition bool, trueVal, falseVal string) string {
    if condition {
        return trueVal
    }
    return falseVal
}
```

**Run:**
```powershell
go run main.go
```

---

### Python Operators

Replace `lesson1.py` with:

```python
# Python Operators Demo
print("=== PYTHON OPERATORS ===\n")

# ARITHMETIC OPERATORS
print("-- Arithmetic Operators --")
a, b = 10, 3
print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")       # Addition: 13
print(f"a - b = {a - b}")       # Subtraction: 7
print(f"a * b = {a * b}")       # Multiplication: 30
print(f"a / b = {a / b}")       # Division: 3.333... (always float)
print(f"a // b = {a // b}")     # Floor division: 3
print(f"a % b = {a % b}")       # Modulus: 1
print(f"a ** b = {a ** b}")     # Exponentiation: 1000
print(f"divmod(a, b) = {divmod(a, b)}")  # (quotient, remainder)

# No ++ or -- in Python
x = 5
x += 1  # Use this instead
print(f"\nx += 1: {x}")

# COMPARISON OPERATORS
print("\n-- Comparison Operators --")
m, n = 10, 20
print(f"m = {m}, n = {n}")
print(f"m == n: {m == n}")    # Equal: False
print(f"m != n: {m != n}")    # Not equal: True
print(f"m > n: {m > n}")      # Greater: False
print(f"m < n: {m < n}")      # Less: True
print(f"m >= n: {m >= n}")    # Greater or equal: False
print(f"m <= n: {m <= n}")    # Less or equal: True

# Chained comparisons (Python-specific)
x = 15
print(f"\nx = {x}")
print(f"10 < x < 20: {10 < x < 20}")     # True
print(f"10 < x < 20 < 30: {10 < x < 20 < 30}")  # True

# LOGICAL OPERATORS
print("\n-- Logical Operators --")
p, q = True, False
print(f"p = {p}, q = {q}")
print(f"p and q: {p and q}")   # AND: False
print(f"p or q: {p or q}")     # OR: True
print(f"not p: {not p}")       # NOT: False

# Short-circuit evaluation
def always_true():
    print("always_true called")
    return True

def always_false():
    print("always_false called")
    return False

print(f"False and always_true(): {False and always_true()}")  # func not called
print(f"True or always_false(): {True or always_false()}")    # func not called

# Logical operators with non-booleans (returns actual value)
print(f"\n0 or 'default': {'default' if not 0 else 0}")  # Using actual behavior
print(f"0 or 'default' = {0 or 'default'}")   # 'default'
print(f"'hello' or 'world' = {'hello' or 'world'}")  # 'hello'
print(f"'' or 'fallback' = {'' or 'fallback'}")  # 'fallback'
print(f"None or 42 = {None or 42}")  # 42

# ASSIGNMENT OPERATORS
print("\n-- Assignment Operators --")
v = 10
print(f"v = {v}")
v += 5; print(f"v += 5: {v}")     # 15
v -= 3; print(f"v -= 3: {v}")     # 12
v *= 2; print(f"v *= 2: {v}")     # 24
v //= 4; print(f"v //= 4: {v}")   # 6
v %= 4; print(f"v %= 4: {v}")     # 2
v **= 3; print(f"v **= 3: {v}")   # 8

# Walrus operator (Python 3.8+)
print("\n-- Walrus Operator := --")
if (n := len("hello")) > 3:
    print(f"String length {n} is greater than 3")

# Use in list comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
results = [y for x in numbers if (y := x ** 2) > 25]
print(f"Squares > 25: {results}")

# BITWISE OPERATORS
print("\n-- Bitwise Operators --")
bits1 = 0b1100  # 12
bits2 = 0b1010  # 10
print(f"bits1 = {bits1} ({bin(bits1)})")
print(f"bits2 = {bits2} ({bin(bits2)})")
print(f"AND (&): {bits1 & bits2} ({bin(bits1 & bits2)})")     # 8
print(f"OR (|): {bits1 | bits2} ({bin(bits1 | bits2)})")      # 14
print(f"XOR (^): {bits1 ^ bits2} ({bin(bits1 ^ bits2)})")     # 6
print(f"NOT (~bits1): {~bits1}")                               # -13 (two's complement)
print(f"Left Shift (<<2): {bits1 << 2}")                       # 48
print(f"Right Shift (>>2): {bits1 >> 2}")                      # 3

# TERNARY OPERATOR
print("\n-- Ternary Operator --")
age = 18
status = "Adult" if age >= 18 else "Minor"
print(f"Age {age}: {status}")

# Nested ternary
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"Score {score}: Grade {grade}")

# IDENTITY OPERATORS
print("\n-- Identity Operators (is, is not) --")
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print(f"list1 == list2: {list1 == list2}")     # True (same value)
print(f"list1 is list2: {list1 is list2}")     # False (different objects)
print(f"list1 is list3: {list1 is list3}")     # True (same object)

# None comparison
value = None
print(f"value is None: {value is None}")       # Preferred
print(f"value == None: {value == None}")       # Works but not recommended

# MEMBERSHIP OPERATORS
print("\n-- Membership Operators (in, not in) --")
fruits = ["apple", "banana", "orange"]
print(f"'apple' in fruits: {'apple' in fruits}")           # True
print(f"'grape' not in fruits: {'grape' not in fruits}") # True

# Works with strings, dicts, sets
text = "Hello, World!"
print(f"'World' in text: {'World' in text}")   # True

person = {"name": "John", "age": 30}
print(f"'name' in person: {'name' in person}")  # True (checks keys)

# UNPACKING OPERATORS
print("\n-- Unpacking Operators (* and **) --")
# List unpacking
nums = [1, 2, 3]
print(f"*nums in list: {[0, *nums, 4]}")  # [0, 1, 2, 3, 4]

# Function argument unpacking
def greet(name, age, city):
    return f"{name}, {age}, {city}"

args = ["John", 30, "NYC"]
kwargs = {"name": "Jane", "age": 25, "city": "LA"}
print(f"*args: {greet(*args)}")
print(f"**kwargs: {greet(**kwargs)}")

# Dict merging (Python 3.9+)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = {**dict1, **dict2}
print(f"Merged dict: {merged}")

# OPERATOR PRECEDENCE
print("\n-- Operator Precedence --")
result1 = 2 + 3 * 4       # 14 (multiplication first)
result2 = (2 + 3) * 4     # 20 (parentheses first)
print(f"2 + 3 * 4 = {result1}")
print(f"(2 + 3) * 4 = {result2}")

# Complex precedence
result3 = 2 ** 3 ** 2     # 512 (right-to-left for **)
result4 = (2 ** 3) ** 2   # 64
print(f"2 ** 3 ** 2 = {result3} (right-to-left)")
print(f"(2 ** 3) ** 2 = {result4}")
```

**Run:**
```powershell
python lesson1.py
```

---

### React/JavaScript Operators

Replace `src/App.js` with:

```jsx
import React from 'react';

function App() {
  // ARITHMETIC OPERATORS
  const a = 10, b = 3;
  const arithmetic = {
    addition: a + b,           // 13
    subtraction: a - b,        // 7
    multiplication: a * b,     // 30
    division: a / b,           // 3.333...
    modulus: a % b,            // 1
    exponentiation: a ** b,    // 1000
  };

  // Increment/Decrement
  let x = 5;
  const postIncrement = x++;   // Returns 5, x becomes 6
  const preIncrement = ++x;    // x becomes 7, returns 7

  // COMPARISON OPERATORS
  const comparison = {
    equal: 10 == '10',         // true (type coercion)
    strictEqual: 10 === '10',  // false (no coercion)
    notEqual: 10 != '10',      // false
    strictNotEqual: 10 !== '10', // true
    greater: 10 > 5,           // true
    less: 10 < 5,              // false
    greaterOrEqual: 10 >= 10,  // true
    lessOrEqual: 10 <= 5,      // false
  };

  // LOGICAL OPERATORS
  const p = true, q = false;
  const logical = {
    and: p && q,               // false
    or: p || q,                // true
    not: !p,                   // false
    doubleNot: !!0,            // false (convert to boolean)
    doubleNotTruthy: !!'hello', // true
  };

  // Short-circuit evaluation
  const shortCircuit = {
    andShort: false && 'never reached',  // false
    orShort: 'value' || 'default',       // 'value'
    orDefault: '' || 'default',          // 'default' (empty is falsy)
    nullishCoalescing: null ?? 'default', // 'default'
    nullishZero: 0 ?? 'default',          // 0 (only null/undefined)
  };

  // ASSIGNMENT OPERATORS
  let v = 10;
  const assignments = [];
  assignments.push(`v = ${v}`);
  v += 5; assignments.push(`v += 5: ${v}`);
  v -= 3; assignments.push(`v -= 3: ${v}`);
  v *= 2; assignments.push(`v *= 2: ${v}`);
  v /= 4; assignments.push(`v /= 4: ${v}`);
  v %= 4; assignments.push(`v %= 4: ${v}`);
  v **= 2; assignments.push(`v **= 2: ${v}`);

  // Logical assignment operators (ES2021)
  let logicalAssign = null;
  logicalAssign ??= 'default';  // Assign if null/undefined
  let orAssign = '';
  orAssign ||= 'fallback';      // Assign if falsy
  let andAssign = 'value';
  andAssign &&= 'replaced';     // Assign if truthy

  // BITWISE OPERATORS
  const bits1 = 0b1100; // 12
  const bits2 = 0b1010; // 10
  const bitwise = {
    and: (bits1 & bits2).toString(2).padStart(4, '0'),   // 1000 (8)
    or: (bits1 | bits2).toString(2).padStart(4, '0'),    // 1110 (14)
    xor: (bits1 ^ bits2).toString(2).padStart(4, '0'),   // 0110 (6)
    not: (~bits1).toString(2),                            // -1101 (two's complement)
    leftShift: bits1 << 2,                                // 48
    rightShift: bits1 >> 2,                               // 3
    unsignedRightShift: (-8) >>> 2,                       // Large positive number
  };

  // TERNARY OPERATOR
  const age = 18;
  const status = age >= 18 ? 'Adult' : 'Minor';

  // Nested ternary
  const score = 85;
  const grade = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : 'F';

  // OPTIONAL CHAINING & NULLISH COALESCING
  const user = {
    name: 'John',
    address: {
      city: 'NYC'
    }
  };
  
  const optionalChaining = {
    existing: user?.address?.city,           // 'NYC'
    nonExisting: user?.contact?.email,       // undefined (no error)
    withDefault: user?.contact?.email ?? 'N/A', // 'N/A'
    methodCall: user.toString?.(),           // '[object Object]'
    arrayAccess: [1, 2, 3]?.[1],             // 2
  };

  // TYPEOF OPERATOR
  const typeofResults = {
    number: typeof 42,
    string: typeof 'hello',
    boolean: typeof true,
    undefined: typeof undefined,
    null: typeof null,           // 'object' (JS quirk!)
    object: typeof {},
    array: typeof [],            // 'object'
    function: typeof (() => {}),
    symbol: typeof Symbol(),
  };

  // INSTANCEOF OPERATOR
  const arr = [1, 2, 3];
  const date = new Date();
  const instanceofResults = {
    arrIsArray: arr instanceof Array,     // true
    dateIsDate: date instanceof Date,     // true
    arrIsObject: arr instanceof Object,   // true
  };

  // SPREAD OPERATOR
  const nums = [1, 2, 3];
  const spread = {
    arrayCopy: [...nums],
    arrayMerge: [...nums, 4, 5],
    objectCopy: { ...user },
    objectMerge: { ...user, age: 30 },
  };

  // REST OPERATOR (in function)
  const sum = (...numbers) => numbers.reduce((a, b) => a + b, 0);
  const [first, ...rest] = [1, 2, 3, 4, 5];

  // COMMA OPERATOR
  let comma = (1, 2, 3);  // Returns last value: 3

  // VOID OPERATOR
  const voidResult = void 0;  // undefined

  // DELETE OPERATOR
  const obj = { a: 1, b: 2 };
  const deleteResult = delete obj.a;  // true, obj is now { b: 2 }

  // IN OPERATOR
  const inResults = {
    keyInObject: 'name' in user,     // true
    indexInArray: 0 in [1, 2, 3],    // true
  };

  // OPERATOR PRECEDENCE
  const precedence = {
    noParens: 2 + 3 * 4,     // 14
    withParens: (2 + 3) * 4, // 20
    rightToLeft: 2 ** 3 ** 2, // 512 (right-to-left)
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', maxWidth: '900px' }}>
      <h1>JavaScript Operators Demo</h1>

      <h2>Arithmetic Operators</h2>
      <pre>
{`a = ${a}, b = ${b}
${Object.entries(arithmetic).map(([k, v]) => `${k}: ${v}`).join('\n')}`}
      </pre>

      <h2>Comparison Operators</h2>
      <pre>
{Object.entries(comparison).map(([k, v]) => `${k}: ${v}`).join('\n')}
      </pre>

      <h2>Logical Operators</h2>
      <pre>
{`p = ${p}, q = ${q}
${Object.entries(logical).map(([k, v]) => `${k}: ${v}`).join('\n')}`}
      </pre>

      <h2>Short-Circuit Evaluation</h2>
      <pre>
{Object.entries(shortCircuit).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n')}
      </pre>

      <h2>Assignment Operators</h2>
      <pre>{assignments.join('\n')}</pre>

      <h2>Logical Assignment (ES2021)</h2>
      <pre>
{`logicalAssign ??= 'default': ${logicalAssign}
orAssign ||= 'fallback': ${orAssign}
andAssign &&= 'replaced': ${andAssign}`}
      </pre>

      <h2>Bitwise Operators</h2>
      <pre>
{`bits1 = ${bits1} (${bits1.toString(2).padStart(4, '0')})
bits2 = ${bits2} (${bits2.toString(2).padStart(4, '0')})
${Object.entries(bitwise).map(([k, v]) => `${k}: ${v}`).join('\n')}`}
      </pre>

      <h2>Ternary Operator</h2>
      <pre>
{`age ${age}: ${status}
score ${score}: Grade ${grade}`}
      </pre>

      <h2>Optional Chaining & Nullish Coalescing</h2>
      <pre>
{Object.entries(optionalChaining).map(([k, v]) => `${k}: ${v}`).join('\n')}
      </pre>

      <h2>typeof Operator</h2>
      <pre>
{Object.entries(typeofResults).map(([k, v]) => `typeof ${k}: '${v}'`).join('\n')}
      </pre>

      <h2>instanceof Operator</h2>
      <pre>
{Object.entries(instanceofResults).map(([k, v]) => `${k}: ${v}`).join('\n')}
      </pre>

      <h2>Spread & Rest Operators</h2>
      <pre>
{`[...nums] = [${spread.arrayCopy.join(', ')}]
[...nums, 4, 5] = [${spread.arrayMerge.join(', ')}]
sum(1,2,3,4,5) = ${sum(1, 2, 3, 4, 5)}
[first, ...rest] = first: ${first}, rest: [${rest.join(', ')}]`}
      </pre>

      <h2>in Operator</h2>
      <pre>
{Object.entries(inResults).map(([k, v]) => `${k}: ${v}`).join('\n')}
      </pre>

      <h2>Operator Precedence</h2>
      <pre>
{Object.entries(precedence).map(([k, v]) => `${k}: ${v}`).join('\n')}
      </pre>
    </div>
  );
}

export default App;
```

**Run:**
```powershell
npm start
```

---

## 📝 EXERCISES

### Exercise 1: Variable Swap
Swap two variables without using a third variable.

**C#:**
```csharp
int a = 5, b = 10;
// Your code here - swap a and b
Console.WriteLine($"a = {a}, b = {b}"); // Should print: a = 10, b = 5
```

**Go:**
```go
a, b := 5, 10
// Your code here
fmt.Printf("a = %d, b = %d\n", a, b)
```

**Python:**
```python
a, b = 5, 10
# Your code here
print(f"a = {a}, b = {b}")
```

**JavaScript:**
```javascript
let a = 5, b = 10;
// Your code here
console.log(`a = ${a}, b = ${b}`);
```

<details>
<summary>Solution</summary>

```csharp
// C#
(a, b) = (b, a);
// or: a = a + b; b = a - b; a = a - b;
```

```go
// Go
a, b = b, a
```

```python
# Python
a, b = b, a
```

```javascript
// JavaScript
[a, b] = [b, a];
```
</details>

---

### Exercise 2: Check Even/Odd
Determine if a number is even or odd using bitwise operators.

<details>
<summary>Solution</summary>

```csharp
// C# - Using bitwise AND
int num = 7;
string result = (num & 1) == 0 ? "Even" : "Odd";
```

```go
// Go
num := 7
if num&1 == 0 {
    fmt.Println("Even")
} else {
    fmt.Println("Odd")
}
```

```python
# Python
num = 7
result = "Even" if num & 1 == 0 else "Odd"
```

```javascript
// JavaScript
const num = 7;
const result = (num & 1) === 0 ? 'Even' : 'Odd';
```
</details>

---

### Exercise 3: Null-Safe Property Access
Safely access nested properties that might be null.

<details>
<summary>Solution</summary>

```csharp
// C#
var user = new { Address = (object?)null };
var city = user?.Address?.ToString() ?? "Unknown";
```

```go
// Go (no optional chaining, must check manually)
type Address struct { City string }
type User struct { Address *Address }

user := User{Address: nil}
var city string
if user.Address != nil {
    city = user.Address.City
} else {
    city = "Unknown"
}
```

```python
# Python
user = {"address": None}
city = user.get("address", {}).get("city", "Unknown") if user.get("address") else "Unknown"
```

```javascript
// JavaScript
const user = { address: null };
const city = user?.address?.city ?? 'Unknown';
```
</details>

---

## 🎯 KEY TAKEAWAYS

| Concept | C# | Go | Python | JavaScript |
|---------|----|----|--------|------------|
| **Typing** | Static | Static | Dynamic | Dynamic |
| **Type Inference** | `var` | `:=` | Always | `let`/`const` |
| **Constants** | `const` | `const` | Convention (UPPER) | `const` |
| **Null/None** | `null`, `?` | `nil` | `None` | `null`, `undefined` |
| **Increment** | `++x`, `x++` | `x++` only | `x += 1` | `++x`, `x++` |
| **Ternary** | `? :` | None (use if) | `if else` | `? :` |
| **Null Coalescing** | `??` | None | `or` | `??` |
| **Optional Chaining** | `?.` | None | None (3.10+ match) | `?.` |

---

## 📚 NEXT LESSON

**Control Flow (if/else, switch, loops)** - We'll cover:
- Conditional statements
- Switch/match expressions
- For/while/do-while loops
- Iterators and ranges
- Break, continue, and return

---

*Type "next" to proceed to the next lesson!*
