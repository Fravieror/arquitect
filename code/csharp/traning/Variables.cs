public class Variables
{
    public static void Run()
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
        Console.WriteLine($"Nullable Age: {nullableAge ?? 0} \n");
    }
}