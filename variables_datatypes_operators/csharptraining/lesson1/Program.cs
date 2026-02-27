// See https://aka.ms/new-console-template for more information
using System;

class Program
{
    static void Main(string[] args)
    {
        string name = "John";
        int age = 30;
        double salary = 75000.50;
        bool isEmployed = true;
        char grade = 'A';

        var city = "New york";
        var count = 100;
        var price = 19.99;

        const double PI = 3.14159;
        const string COMPANY = "TechCorp";

        int? nullableAge = null;
        string? nullableName = null;

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
