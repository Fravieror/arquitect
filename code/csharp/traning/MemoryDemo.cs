using System;
using System.Drawing;

public class MemoryDemo
{
    struct PointStruct
    {
        public int X;
        public int Y;
    }

    class PointClass
    {
        public int X;
        public int Y;
    }

    public static void Run()
    {
        Console.WriteLine("=== C# Memory Management Demo ===\n");

        // Stack values types
        int a = 10;
        int b = a;
        b = 20;
        Console.WriteLine($"Value Types (Stack): a={a}, b={b}"); // a=10,b=20

        // Stack structure (value type)
        PointStruct ps1 = new PointStruct {X = 1, Y =2};
        PointStruct ps2 = ps1;
        ps2.X = 100;        
        Console.WriteLine($"Struct (Stack): ps1.X={ps1.X}, ps2.x={ps2.X}"); // 1, 100

        // heap: Class (reference type)
        PointClass pc1 = new PointClass {X = 1, Y =2};
        PointClass pc2 = pc1;
        pc2.X = 100;
        Console.WriteLine($"Class (Heap): pc1.X={pc1.X}, pc2.X={pc2.X}"); // 100,100

        // boxing: value type moved to heap
        int num = 42; // stack
        object boxed = num; // boxing: copied to heap
        int unboxed = (int)boxed; // unboxing: copied back
        Console.WriteLine($"boxing demo: num{num}, boxed={boxed}");

        // stack allocation with span<t> (high-performance)
        Span<int> stackArray = stackalloc int[3] {1,2,3}; // stackalloc allocates memory on the stack, which is faster than heap allocation
        Console.WriteLine($"stackalloc array: {stackArray[0]}, {stackArray[1]}, {stackArray[2]}");

        // force garbage collection (for demostration)
        Console.WriteLine($"\nmemory before gc: {GC.GetTotalMemory(false):N0} bytes"); 
        // N0 is a numeric format specifier that formats the number with thousand separators
        GC.Collect();
        Console.WriteLine($"memory after gc: {GC.GetTotalMemory(true):N0} bytes");
        
        Console.WriteLine("\n=== Key Takeaways ===");
        Console.WriteLine("- Value types (int, struct) live on Stack - fast, copied by value");
        Console.WriteLine("- Reference types (class) live on Heap - shared by reference");
        Console.WriteLine("- Boxing moves value types to Heap (performance cost)");
        Console.WriteLine("- Use 'stackalloc' for performance-critical stack arrays ");

    }
    
}