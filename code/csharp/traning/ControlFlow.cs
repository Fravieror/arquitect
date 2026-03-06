public class ControlFlow
{
    public static void IfElseDemo()
    {
        object obj = 42;
        if(obj is int number && number > 0)
        {
            Console.WriteLine($"Positive integer: {number}");
        }
    }
}