# Stacks and Queues in C#

## Overview

Stacks and Queues are fundamental **linear data structures** that control the order of element access. As an architect, understanding when to use each is critical for designing efficient systems—from undo mechanisms to task schedulers.

---

## 1. Stack (LIFO - Last In, First Out)

### What is a Stack?

A stack is a collection where the **last element added is the first removed**. Think of a stack of plates—you add to the top and remove from the top.

### Key Characteristics

| Property | Value |
|----------|-------|
| Order | LIFO (Last In, First Out) |
| Push | O(1) - Add to top |
| Pop | O(1) - Remove from top |
| Peek | O(1) - View top without removing |
| Search | O(n) - Linear |
| Namespace | `System.Collections.Generic` |

### Real-World Use Cases

- **Undo/Redo functionality** (text editors, design tools)
- **Call stack** (function execution tracking)
- **Expression parsing** (compilers, calculators)
- **Backtracking algorithms** (maze solving, DFS)
- **Browser history** (back button)

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

### Exercise 1: Stack Fundamentals

Create a file `StackBasics.cs` and type the following:

```csharp
namespace DataStructures;

public class StackBasics
{
    public static void Run()
    {
        Console.WriteLine("=== STACK FUNDAMENTALS ===\n");

        // 1. Creating a Stack
        Stack<int> numbers = new();
        Stack<string> names = new(capacity: 100); // With initial capacity

        // 2. Push - Add elements to top - O(1)
        numbers.Push(10);
        numbers.Push(20);
        numbers.Push(30);
        numbers.Push(40);

        Console.WriteLine($"After pushing: {string.Join(" → ", numbers)}");
        Console.WriteLine($"Count: {numbers.Count}");

        // 3. Peek - View top element without removing - O(1)
        int top = numbers.Peek(); // what will return Peek? It will return 40, which is the last element pushed onto the stack and currently at the top.
        Console.WriteLine($"\nPeek (top element): {top}");
        Console.WriteLine($"Count after Peek: {numbers.Count}"); // Still 4

        // 4. Pop - Remove and return top element - O(1)
        int popped = numbers.Pop();
        Console.WriteLine($"\nPopped: {popped}");
        Console.WriteLine($"After Pop: {string.Join(" → ", numbers)}");
        Console.WriteLine($"Count after Pop: {numbers.Count}"); // Now 3

        // 5. TryPeek and TryPop - Safe operations (no exception if empty)
        if (numbers.TryPeek(out int peeked))
        {
            Console.WriteLine($"\nTryPeek succeeded: {peeked}");
        }

        if (numbers.TryPop(out int tryPopped))
        {
            Console.WriteLine($"TryPop succeeded: {tryPopped}");
        }

        // 6. Contains - Check if element exists - O(n)
        bool hasElement = numbers.Contains(10);
        Console.WriteLine($"\nContains 10: {hasElement}");

        // 7. Clear - Remove all elements
        numbers.Clear();
        Console.WriteLine($"After Clear - Count: {numbers.Count}");

        // 8. Iterating (doesn't remove elements)
        Stack<string> colors = new();
        colors.Push("Red");
        colors.Push("Green");
        colors.Push("Blue");

        Console.WriteLine("\nIterating through stack:");
        foreach (var color in colors)
        {
            Console.WriteLine($"  {color}");
        }
        Console.WriteLine($"Count after iteration: {colors.Count}"); // Still 3
    }
    // ARCHITECT INSIGHT: Stack<T> is implemented as a resizable array internally, providing O(1) push and pop operations. It's ideal for scenarios where you need LIFO behavior and fast access to the most recently added elements.

    // is this more efficient than using a List<T> as a stack? Yes, Stack<T> is optimized for LIFO operations and provides better performance for push and pop compared to using a List<T> as a stack, which may require additional overhead for managing the list's internal structure and resizing.

    // when was incorporated stack in .NET? Stack<T> was introduced in .NET Framework 2.0 as part of the System.Collections.Generic namespace, providing a strongly-typed collection for LIFO operations. which year was .NET Framework 2.0 released? .NET Framework 2.0 was released in November 2005.
}
```

---

### Exercise 2: Practical Stack - Undo/Redo System

Create `UndoRedoSystem.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT PATTERN: Command Pattern with Stack for Undo/Redo
/// This is a common pattern in text editors, design tools, and IDEs.
/// </summary>
public class UndoRedoSystem
{
    public static void Run()
    {
        Console.WriteLine("\n=== UNDO/REDO SYSTEM ===\n");

        var editor = new TextEditor();

        // Perform actions
        editor.Type("Hello");
        editor.Type(" World");
        editor.Type("!");
        Console.WriteLine($"Current text: \"{editor.Text}\"");

        // Undo operations
        editor.Undo();
        Console.WriteLine($"After Undo: \"{editor.Text}\"");

        editor.Undo();
        Console.WriteLine($"After Undo: \"{editor.Text}\"");

        // Redo operations
        editor.Redo();
        Console.WriteLine($"After Redo: \"{editor.Text}\"");

        // New action clears redo stack
        editor.Type("?");
        Console.WriteLine($"After new action: \"{editor.Text}\"");

        editor.Redo(); // Nothing happens
        Console.WriteLine($"After attempted Redo: \"{editor.Text}\"");
    }
}

public class TextEditor
{
    private readonly Stack<ICommand> _undoStack = new();
    private readonly Stack<ICommand> _redoStack = new();

    public string Text { get; private set; } = "";

    public void Type(string text)
    {
        var command = new TypeCommand(this, text); // is this performed each time the user types a new word? Yes, each time the user types a new word, a new TypeCommand is created and executed, allowing for individual undo/redo actions for each typed word.
        command.Execute();
        _undoStack.Push(command);
        _redoStack.Clear(); // New action clears redo history, why clear redo stack? Because once you perform a new action after undoing, the previous redo history becomes invalid, as it would not reflect the current state of the text editor. Clearing the redo stack ensures that you cannot redo actions that are no longer relevant to the current state of the editor.
    }

    public void Undo()
    {
        if (_undoStack.TryPop(out var command))
        {
            command.Undo();
            _redoStack.Push(command);
        }
    }

    public void Redo()
    {
        if (_redoStack.TryPop(out var command))
        {
            command.Execute();
            _undoStack.Push(command);
        }
    }

    internal void AppendText(string text) => Text += text;
    internal void RemoveText(int length) => Text = Text[..^length];
}

public interface ICommand
{
    void Execute();
    void Undo();
}

public class TypeCommand : ICommand
{
    private readonly TextEditor _editor;
    private readonly string _text;

    public TypeCommand(TextEditor editor, string text)
    {
        _editor = editor;
        _text = text;
    }

    public void Execute() => _editor.AppendText(_text);
    public void Undo() => _editor.RemoveText(_text.Length);
}
```

---

### Exercise 3: Expression Evaluation with Stack

Create `ExpressionEvaluator.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Stacks are fundamental to compilers and interpreters.
/// This demonstrates postfix (Reverse Polish Notation) evaluation.
/// </summary>
public class ExpressionEvaluator
{
    public static void Run()
    {
        Console.WriteLine("\n=== EXPRESSION EVALUATION ===\n");

        // Postfix notation: operands first, then operator
        // "3 4 +" means 3 + 4 = 7
        // "3 4 + 2 *" means (3 + 4) * 2 = 14

        string[] expressions = {
            "3 4 +",           // 7
            "3 4 + 2 *",       // 14
            "5 1 2 + 4 * + 3 -", // 14
            "10 2 / 3 *"       // 15
        };

        foreach (var expr in expressions)
        {
            int result = EvaluatePostfix(expr);
            Console.WriteLine($"{expr} = {result}");
        }

        // Bracket matching
        Console.WriteLine("\n--- Bracket Matching ---");
        string[] testStrings = {
            "(a + b) * (c + d)",
            "((a + b)",
            "{[()]}",
            "{[(])}",
            "function() { return array[0]; }"
        };

        foreach (var test in testStrings)
        {
            bool isValid = IsBalanced(test);
            Console.WriteLine($"\"{test}\" → {(isValid ? "Valid" : "Invalid")}");
        }
    }

    public static int EvaluatePostfix(string expression)
    {
        Stack<int> stack = new();
        string[] tokens = expression.Split(' ');

        foreach (string token in tokens)
        {
            if (int.TryParse(token, out int number))
            {
                stack.Push(number);
            }
            else
            {
                // Operator - pop two operands
                int b = stack.Pop();
                int a = stack.Pop();

                int result = token switch
                {
                    "+" => a + b,
                    "-" => a - b,
                    "*" => a * b,
                    "/" => a / b,
                    _ => throw new ArgumentException($"Unknown operator: {token}")
                };

                stack.Push(result);
            }
        }

        return stack.Pop();
    }

    public static bool IsBalanced(string expression)
    {
        Stack<char> stack = new();
        Dictionary<char, char> brackets = new()
        {
            { ')', '(' },
            { ']', '[' },
            { '}', '{' }
        };

        foreach (char c in expression)
        {
            if (c is '(' or '[' or '{')
            {
                stack.Push(c);
            }
            else if (brackets.ContainsKey(c))
            {
                if (stack.Count == 0 || stack.Pop() != brackets[c])
                {
                    return false;
                }
            }
        }

        return stack.Count == 0;
    }
}
```

---

## 2. Queue (FIFO - First In, First Out)

### What is a Queue?

A queue is a collection where the **first element added is the first removed**. Think of a line at a store—first come, first served.

### Key Characteristics

| Property | Value |
|----------|-------|
| Order | FIFO (First In, First Out) |
| Enqueue | O(1) - Add to back |
| Dequeue | O(1) - Remove from front |
| Peek | O(1) - View front without removing |
| Search | O(n) - Linear |
| Namespace | `System.Collections.Generic` |

### Real-World Use Cases

- **Task scheduling** (job queues, print queues)
- **Message queues** (RabbitMQ, Azure Service Bus)
- **BFS traversal** (graph algorithms)
- **Rate limiting** (request throttling)
- **Event handling** (event loops, UI events)

---

### Exercise 4: Queue Fundamentals

Create `QueueBasics.cs`:

```csharp
namespace DataStructures;

public class QueueBasics
{
    public static void Run()
    {
        Console.WriteLine("\n=== QUEUE FUNDAMENTALS ===\n");

        // 1. Creating a Queue
        Queue<int> numbers = new();
        Queue<string> messages = new(capacity: 100);

        // 2. Enqueue - Add elements to back - O(1)
        numbers.Enqueue(10);
        numbers.Enqueue(20);
        numbers.Enqueue(30);
        numbers.Enqueue(40);

        Console.WriteLine($"After enqueuing: {string.Join(" → ", numbers)}");
        Console.WriteLine($"Count: {numbers.Count}");

        // 3. Peek - View front element without removing - O(1)
        int front = numbers.Peek();
        Console.WriteLine($"\nPeek (front element): {front}");
        Console.WriteLine($"Count after Peek: {numbers.Count}"); // Still 4

        // 4. Dequeue - Remove and return front element - O(1)
        int dequeued = numbers.Dequeue();
        Console.WriteLine($"\nDequeued: {dequeued}");
        Console.WriteLine($"After Dequeue: {string.Join(" → ", numbers)}");
        Console.WriteLine($"Count after Dequeue: {numbers.Count}"); // Now 3

        // 5. TryPeek and TryDequeue - Safe operations
        if (numbers.TryPeek(out int peeked))
        {
            Console.WriteLine($"\nTryPeek succeeded: {peeked}");
        }

        if (numbers.TryDequeue(out int tryDequeued))
        {
            Console.WriteLine($"TryDequeue succeeded: {tryDequeued}");
        }

        // 6. Contains - Check if element exists - O(n)
        bool hasElement = numbers.Contains(40);
        Console.WriteLine($"\nContains 40: {hasElement}");

        // 7. ToArray and iteration
        Queue<string> tasks = new();
        tasks.Enqueue("Task A");
        tasks.Enqueue("Task B");
        tasks.Enqueue("Task C");

        Console.WriteLine("\nIterating through queue:");
        foreach (var task in tasks)
        {
            Console.WriteLine($"  {task}");
        }
        Console.WriteLine($"Count after iteration: {tasks.Count}"); // Still 3

        // 8. Processing queue until empty
        Console.WriteLine("\nProcessing queue:");
        while (tasks.TryDequeue(out string? task))
        {
            Console.WriteLine($"  Processing: {task}");
        }
        Console.WriteLine($"Count after processing: {tasks.Count}"); // Now 0

        // is a queue more efficient than a list for FIFO operations? Yes, Queue<T> is optimized for FIFO operations and provides O(1) complexity for enqueue and dequeue, while using a List<T> for similar operations would typically involve O(n) complexity due to the need to shift elements when removing from the front.

        // is a queue a list or array internally? Queue<T> is implemented as a circular array internally, which allows it to efficiently manage the front and back of the queue without needing to shift elements, providing O(1) time complexity for both enqueue and dequeue operations.
    }
}
```

---

### Exercise 5: Task Scheduler with Queue

Create `TaskScheduler.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT PATTERN: Producer-Consumer with Queue
/// Common in microservices, background job processors, and message-driven architectures.
/// </summary>
public class TaskScheduler
{
    public static void Run()
    {
        Console.WriteLine("\n=== TASK SCHEDULER ===\n");

        var scheduler = new SimpleTaskScheduler();

        // Enqueue tasks (producer)
        scheduler.EnqueueTask(new WorkItem("Send email notification", Priority.High));
        scheduler.EnqueueTask(new WorkItem("Generate report", Priority.Normal));
        scheduler.EnqueueTask(new WorkItem("Cleanup temp files", Priority.Low));
        scheduler.EnqueueTask(new WorkItem("Process payment", Priority.High));
        scheduler.EnqueueTask(new WorkItem("Update cache", Priority.Normal));

        Console.WriteLine($"Tasks in queue: {scheduler.PendingCount}\n");

        // Process tasks (consumer)
        scheduler.ProcessAll();
    }
}

public enum Priority { Low, Normal, High }

public record WorkItem(string Description, Priority Priority)
{
    public DateTime CreatedAt { get; } = DateTime.Now;
}

public class SimpleTaskScheduler
{
    private readonly Queue<WorkItem> _taskQueue = new();

    public int PendingCount => _taskQueue.Count;

    public void EnqueueTask(WorkItem task)
    {
        _taskQueue.Enqueue(task);
        Console.WriteLine($"[ENQUEUED] {task.Description} (Priority: {task.Priority})");
    }

    public void ProcessAll()
    {
        Console.WriteLine("--- Processing Tasks (FIFO Order) ---");
        int processed = 0;

        while (_taskQueue.TryDequeue(out var task)) // does the queue dequeue the object in priority order? No, the queue processes tasks in the order they were enqueued (FIFO), regardless of their priority. To process tasks based on priority, you would need to use a PriorityQueue instead of a regular Queue.
        {
            processed++;
            Console.WriteLine($"[{processed}] Processing: {task.Description}");
            Thread.Sleep(100); // Simulate work
        }

        Console.WriteLine($"\nCompleted {processed} tasks.");
    }
}
```

---

### Exercise 6: Priority Queue (C# 10+)

Create `PriorityQueueDemo.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: PriorityQueue was added in .NET 6.
/// Essential for job scheduling, pathfinding (Dijkstra), and event processing.
/// </summary>
public class PriorityQueueDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== PRIORITY QUEUE ===\n");

        // PriorityQueue<TElement, TPriority>
        // Lower priority value = higher priority (dequeued first)
        PriorityQueue<string, int> taskQueue = new();

        // Enqueue with priorities
        taskQueue.Enqueue("Regular backup", priority: 5);
        taskQueue.Enqueue("Critical security patch", priority: 1);
        taskQueue.Enqueue("Update documentation", priority: 10);
        taskQueue.Enqueue("Fix production bug", priority: 2);
        taskQueue.Enqueue("Refactor code", priority: 7);

        Console.WriteLine($"Tasks in priority queue: {taskQueue.Count}\n");

        // Dequeue in priority order
        Console.WriteLine("Processing by priority:");
        while (taskQueue.TryDequeue(out string? task, out int priority)) // does the queue dequeue the object in priority order? Yes, the PriorityQueue<TElement, TPriority> dequeues elements based on their priority, with lower priority values being dequeued first. In this example, "Critical security patch" (priority 1) will be processed before "Fix production bug" (priority 2), and so on.
        {
            Console.WriteLine($"  Priority {priority}: {task}");
        }

        // Using with custom objects
        Console.WriteLine("\n--- Emergency Room Simulation ---");
        PriorityQueue<Patient, int> emergencyRoom = new();

        emergencyRoom.Enqueue(new Patient("John", "Broken arm"), 3);
        emergencyRoom.Enqueue(new Patient("Jane", "Heart attack"), 1);
        emergencyRoom.Enqueue(new Patient("Bob", "Headache"), 5);
        emergencyRoom.Enqueue(new Patient("Alice", "Severe bleeding"), 2);

        Console.WriteLine("Patients seen in order:");
        while (emergencyRoom.TryDequeue(out var patient, out int severity)) // does the queue dequeue the object in priority order? Yes, the PriorityQueue<TElement, TPriority> dequeues elements based on their priority, with lower priority values being dequeued first. In this example, "Jane" (priority 1) will be seen before "Alice" (priority 2), and so on.
        {
            Console.WriteLine($"  [{severity}] {patient.Name}: {patient.Condition}");
        }
    }
}

public record Patient(string Name, string Condition);
```

---

### Exercise 7: Concurrent Queue (Thread-Safe)

Create `ConcurrentQueueDemo.cs`:

```csharp
using System.Collections.Concurrent;

namespace DataStructures;

/// <summary>
/// ARCHITECT PATTERN: Thread-safe queue for producer-consumer scenarios.
/// Essential for multi-threaded applications and parallel processing.
/// </summary>
public class ConcurrentQueueDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== CONCURRENT QUEUE (Thread-Safe) ===\n");

        ConcurrentQueue<string> messageQueue = new();
        bool producerDone = false;

        // Producer thread
        var producer = Task.Run(() =>
        {
            for (int i = 1; i <= 10; i++)
            {
                string message = $"Message-{i}";
                messageQueue.Enqueue(message);
                Console.WriteLine($"[Producer] Enqueued: {message}");
                Thread.Sleep(50);
                // does this producer has to wait for the consumer to process the message before enqueuing the next one? No, the producer does not have to wait for the consumer to process the message before enqueuing the next one. The ConcurrentQueue allows multiple producers and consumers to operate concurrently without blocking each other, so the producer can continue enqueuing messages while the consumer is processing them.
            }

            // if the producer doen't wait for the consumer to process the message before enqueuing the next one, how does the consumer know when the producer is done? The consumer can check the `producerDone` flag to determine when the producer has finished enqueuing messages. In this example, once the producer has enqueued all messages, it sets `producerDone` to true. The consumer threads can periodically check this flag to know when no more messages will be added to the queue, allowing them to exit gracefully once all messages have been processed.
            // but is it not going to cause the consumer to miss processing some messages if it checks the producerDone flag before the producer has enqueued all messages? No, the consumer will not miss processing any messages as long as it continues to check the `producerDone` flag and the queue is not empty. The consumer threads will keep trying to dequeue messages until the producer signals that it is done and the queue is empty. This means that even if the producer is still enqueuing messages, the consumer will continue to process them until there are no more messages left in the queue after the producer has finished.

            // ok so the important validation is that the queue is not empty, and the producerDone flag is just to know when to stop trying to dequeue messages, is not really relavant? Yes, that's correct. The `producerDone` flag is primarily used to signal to the consumer threads that no more messages will be added to the queue, allowing them to stop trying to dequeue messages once the queue is empty. The critical validation for the consumer is to check if the queue is not empty before attempting to dequeue a message. The `producerDone` flag helps ensure that the consumer threads can exit gracefully once all messages have been processed, but it does not affect the actual processing of messages as long as there are still messages in the queue.
            producerDone = true;
            Console.WriteLine("[Producer] Done producing.");
        });

        // Consumer threads
        var consumer1 = Task.Run(() => ConsumeMessages(messageQueue, "Consumer-1", () => producerDone)); // what function performs producerDone? The producerDone variable is a boolean flag that indicates whether the producer has finished enqueuing messages. The lambda function `() => producerDone` is passed to the consumer threads as a way for them to check if the producer has completed its work. The consumer threads will continue to attempt to dequeue messages from the ConcurrentQueue until the producerDone flag is set to true, indicating that no more messages will be added to the queue.

        //
        var consumer2 = Task.Run(() => ConsumeMessages(messageQueue, "Consumer-2", () => producerDone));

        Task.WaitAll(producer, consumer1, consumer2); // does it process the 10 messages sent by the producer, or just the 2 first messages? The consumer threads will process all 10 messages sent by the producer. The ConcurrentQueue allows multiple consumers to safely dequeue messages as they are produced, and the producerDone flag ensures that the consumers continue processing until all messages have been handled, even if they arrive at different times.

        // I see just 2 consumers, where is stored the other 8 messages? The other 8 messages are stored in the ConcurrentQueue until they are dequeued by the consumer threads. The producer thread enqueues all 10 messages into the queue, and the consumer threads will dequeue and process them one by one. The ConcurrentQueue is designed to handle multiple producers and consumers safely, so all messages will be processed as long as the producer continues to enqueue them and the consumers continue to dequeue until the producer is done.

        //where is delared the funcion is ProducerDone? The function `isProducerDone` is declared as a parameter in the `ConsumeMessages` method. It is a `Func<bool>` delegate that allows the consumer threads to check if the producer has finished enqueuing messages. The actual implementation of this function is provided as a lambda expression `() => producerDone` when the consumer tasks are created in the `Run` method of the `ConcurrentQueueDemo` class.

        Console.WriteLine($"\nFinal queue count: {messageQueue.Count}");
    }

    private static void ConsumeMessages(ConcurrentQueue<string> queue, string consumerName, Func<bool> isProducerDone)
    {
        while (!isProducerDone() || !queue.IsEmpty)
        {
            if (queue.TryDequeue(out string? message))
            {
                Console.WriteLine($"  [{consumerName}] Processed: {message}");
                Thread.Sleep(100); // Simulate processing
            }
            else
            {
                Thread.Sleep(10); // Wait for more items
            }
        }
        Console.WriteLine($"  [{consumerName}] Done consuming.");
    }
}
```

---

### Exercise 8: Channel (Modern Async Queue)

Create `ChannelDemo.cs`:

```csharp
using System.Threading.Channels;

namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Channel<T> is the modern async-await friendly queue.
/// Preferred for async producer-consumer patterns in modern .NET applications.
/// </summary>
public class ChannelDemo
{
    public static async Task RunAsync()
    {
        Console.WriteLine("\n=== CHANNEL (Async Queue) ===\n");

        // Bounded channel - blocks producer when full
        var options = new BoundedChannelOptions(capacity: 5)
        {
            FullMode = BoundedChannelFullMode.Wait
        };
        Channel<WorkOrder> channel = Channel.CreateBounded<WorkOrder>(options);

        // Start consumers first
        var consumer1 = ConsumeAsync(channel.Reader, "Worker-1");
        var consumer2 = ConsumeAsync(channel.Reader, "Worker-2");
        // Can I add more consumers? Yes, you can add more consumers by starting additional tasks that call the ConsumeAsync method with the channel's reader. Each consumer will independently read from the channel and process messages as they become available, allowing for scalable processing of work items.

        //what is return by ConsumeAsync? The `ConsumeAsync` method is an asynchronous method that returns a `Task`. It represents the ongoing operation of consuming messages from the channel. When you call `ConsumeAsync`, it will run in the background and process messages as they are read from the channel until the channel is completed and all messages have been processed. The method itself does not return any specific value; instead, it allows you to await its completion to ensure that all consuming operations have finished before proceeding with any further actions in your program.

        // is await Task.WhenAll(producer, consumer1, consumer2); the line that validates the consumers have processed all the messages? Yes, `await Task.WhenAll(producer, consumer1, consumer2);` is the line that ensures that the main thread waits for all the producer and consumer tasks to complete before proceeding. This means that it will wait until the producer has finished enqueuing messages and both consumers have finished processing all messages from the channel. By awaiting this line, you can be confident that all work has been completed before moving on to any subsequent code or finalizing the program.

        // if I want to add more consumers, must I add in the await Task.WhenAll(producer, consumer1, consumer2, consumer3, consumer4);? Yes, if you want to add more consumers, you would need to include them in the `await Task.WhenAll(...)` call to ensure that the main thread waits for all of the producer and consumer tasks to complete. For example, if you add `consumer3` and `consumer4`, you would update the line to `await Task.WhenAll(producer, consumer1, consumer2, consumer3, consumer4);` to ensure that the program waits for all tasks to finish before proceeding.

        // what happens if I don't await Task.WhenAll(producer, consumer1, consumer2);? If you don't await `Task.WhenAll(producer, consumer1, consumer2);`, the main thread will not wait for the producer and consumer tasks to complete before moving on to the next lines of code. This can lead to several issues.

        // if just one consumer is missed it will let the main thread continue and print "All work completed!" before the consumers have finished processing all messages. This can give a false impression that all work is done when in reality, some tasks may still be running in the background.

        // Producer
        var producer = Task.Run(async () =>
        {
            for (int i = 1; i <= 10; i++)
            {
                var order = new WorkOrder(i, $"Task-{i}");
                await channel.Writer.WriteAsync(order);
                Console.WriteLine($"[Producer] Wrote: {order.Description}");
                await Task.Delay(30);
            }
            channel.Writer.Complete();
            Console.WriteLine("[Producer] Completed writing.");
        });

        await Task.WhenAll(producer, consumer1, consumer2);
        Console.WriteLine("\nAll work completed!");
    }

    private static async Task ConsumeAsync(ChannelReader<WorkOrder> reader, string workerName)
    {
        await foreach (var order in reader.ReadAllAsync())
        {
            Console.WriteLine($"  [{workerName}] Processing: {order.Description}");
            await Task.Delay(100); // Simulate async work
        }
        Console.WriteLine($"  [{workerName}] Done.");
    }
}

public record WorkOrder(int Id, string Description);
```

the difference between Channel and ConcurrentQueue is that Channel<T> is designed for asynchronous producer-consumer scenarios and provides built-in support for async/await patterns, while ConcurrentQueue<T> is a thread-safe collection for synchronous producer-consumer scenarios. Channel<T> allows producers and consumers to operate asynchronously without blocking threads, making it ideal for modern .NET applications that heavily utilize async programming, whereas ConcurrentQueue<T> is better suited for scenarios where producers and consumers are running on separate threads but do not require asynchronous processing.

---

## 3. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DataStructures;

Console.WriteLine("╔═══════════════════════════════════════════════════╗");
Console.WriteLine("║     STACKS AND QUEUES - ARCHITECT TRAINING        ║");
Console.WriteLine("╚═══════════════════════════════════════════════════╝");

StackBasics.Run();
UndoRedoSystem.Run();
ExpressionEvaluator.Run();
QueueBasics.Run();
TaskScheduler.Run();
PriorityQueueDemo.Run();
ConcurrentQueueDemo.Run();

// Run async demo
await ChannelDemo.RunAsync();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌─────────────────────────────────────────────────────────┐");
Console.WriteLine("│ Use STACK when:                                         │");
Console.WriteLine("│   • Need LIFO order (last in, first out)                │");
Console.WriteLine("│   • Implementing undo/redo functionality                │");
Console.WriteLine("│   • Parsing expressions or syntax                       │");
Console.WriteLine("│   • Backtracking algorithms (DFS, maze solving)         │");
Console.WriteLine("│   • Managing function calls / recursion                 │");
Console.WriteLine("├─────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use QUEUE when:                                         │");
Console.WriteLine("│   • Need FIFO order (first in, first out)               │");
Console.WriteLine("│   • Task scheduling and job processing                  │");
Console.WriteLine("│   • BFS graph traversal                                 │");
Console.WriteLine("│   • Request buffering and rate limiting                 │");
Console.WriteLine("│   • Event handling and message passing                  │");
Console.WriteLine("├─────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use PRIORITY QUEUE when:                                │");
Console.WriteLine("│   • Elements have different importance levels           │");
Console.WriteLine("│   • Implementing Dijkstra's algorithm                   │");
Console.WriteLine("│   • Job scheduling with priorities                      │");
Console.WriteLine("│   • Event simulation systems                            │");
Console.WriteLine("├─────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use CONCURRENT QUEUE when:                              │");
Console.WriteLine("│   • Multiple threads produce/consume                    │");
Console.WriteLine("│   • Thread-safe operations required                     │");
Console.WriteLine("│   • Simple synchronous producer-consumer                │");
Console.WriteLine("├─────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use CHANNEL when:                                       │");
Console.WriteLine("│   • Async/await producer-consumer pattern               │");
Console.WriteLine("│   • Modern .NET async applications                      │");
Console.WriteLine("│   • Need backpressure (bounded channels)                │");
Console.WriteLine("│   • Streaming data processing                           │");
Console.WriteLine("└─────────────────────────────────────────────────────────┘");
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

| Operation | Stack | Queue | PriorityQueue |
|-----------|-------|-------|---------------|
| Add | O(1) Push | O(1) Enqueue | O(log n) Enqueue |
| Remove | O(1) Pop | O(1) Dequeue | O(log n) Dequeue |
| Peek | O(1) | O(1) | O(1) |
| Search | O(n) | O(n) | O(n) |

### When to Use Each Type

```
┌──────────────────────────────────────────────────────────────┐
│                     DECISION FLOWCHART                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Need ordered access?                                        │
│       │                                                      │
│       ├── Last added first? ──────────► Stack<T>             │
│       │                                                      │
│       ├── First added first?                                 │
│       │       │                                              │
│       │       ├── With priorities? ──► PriorityQueue<T,P>    │
│       │       │                                              │
│       │       ├── Multi-threaded?                            │
│       │       │       │                                      │
│       │       │       ├── Async? ────► Channel<T>            │
│       │       │       │                                      │
│       │       │       └── Sync? ─────► ConcurrentQueue<T>    │
│       │       │                                              │
│       │       └── Single-threaded? ──► Queue<T>              │
│       │                                                      │
│       └── Both ends? ────────────────► LinkedList<T>         │
│                                         (as Deque)           │
└──────────────────────────────────────────────────────────────┘
```

### Memory Layout

```
Stack:  [Header | Count | Array →]
                          ↓
        Array: [A][B][C][D][_][_]  ← Top at index 3
                         ↑
                       Top

Queue:  [Header | Head | Tail | Array →]
                                 ↓
        Array: [_][B][C][D][E][_]
                 ↑           ↑
               Head        Tail
        (Circular buffer implementation)
```

---

## 6. Advanced Topics for Architects

### Implementing a Deque (Double-Ended Queue)

```csharp
// C# doesn't have a built-in Deque, use LinkedList<T>
LinkedList<int> deque = new();

// Add to front and back
deque.AddFirst(1);  // Push front
deque.AddLast(2);   // Push back

// Remove from front and back
int front = deque.First!.Value;
deque.RemoveFirst(); // Pop front

int back = deque.Last!.Value;
deque.RemoveLast();  // Pop back
```

### Stack-Based DFS vs Queue-Based BFS

```csharp
// DFS with Stack (goes deep first)
void DFS(Node start)
{
    Stack<Node> stack = new();
    HashSet<Node> visited = new();
    stack.Push(start);

    while (stack.Count > 0)
    {
        var node = stack.Pop();
        if (visited.Add(node))
        {
            Process(node);
            foreach (var neighbor in node.Neighbors)
                stack.Push(neighbor);
        }
    }
}

// BFS with Queue (goes wide first)
void BFS(Node start)
{
    Queue<Node> queue = new();
    HashSet<Node> visited = new();
    queue.Enqueue(start);
    visited.Add(start);

    while (queue.Count > 0)
    {
        var node = queue.Dequeue();
        Process(node);
        foreach (var neighbor in node.Neighbors)
        {
            if (visited.Add(neighbor))
                queue.Enqueue(neighbor);
        }
    }
}
```

### ImmutableStack and ImmutableQueue

```csharp
using System.Collections.Immutable;

// Thread-safe, immutable collections
ImmutableStack<int> stack = ImmutableStack<int>.Empty;
stack = stack.Push(1).Push(2).Push(3);
var (top, newStack) = (stack.Peek(), stack.Pop());
// Can I add a item to this inmutable stack? Yes, you can add an item to an ImmutableStack by using the Push method, which returns a new instance of the stack with the new item added. For example, `stack = stack.Push(4);` would create a new stack with the value 4 on top of the existing items.

// so what is the difference between stack and immutable stack? The main difference between a regular Stack<T> and an ImmutableStack<T> is that the ImmutableStack<T> is designed to be thread-safe and cannot be modified after it is created. When you perform operations like Push or Pop on an ImmutableStack, it returns a new instance of the stack with the changes applied, while the original stack remains unchanged. In contrast, a regular Stack<T> allows you to modify the existing instance directly, which can lead to issues in multi-threaded scenarios if not handled properly.

// is the main difference in memory usage? Yes, the main difference in memory usage between Stack<T> and ImmutableStack<T> is that ImmutableStack<T> creates a new instance of the stack for each modification (like Push or Pop), which can lead to increased memory usage if you perform many operations. In contrast, Stack<T> modifies the existing instance in place, which can be more memory-efficient but requires careful handling to avoid issues in multi-threaded environments.

// is it the same with queues and immutable queues? Yes, the same principles apply to Queue<T> and ImmutableQueue<T>. The ImmutableQueue<T> is designed to be thread-safe and immutable, meaning that any operation that modifies the queue (like Enqueue or Dequeue) will return a new instance of the queue with the changes applied, while the original queue remains unchanged. In contrast, a regular Queue<T> allows you to modify the existing instance directly, which can lead to issues in multi-threaded scenarios if not handled properly and can be more memory-efficient for single-threaded use cases.

```csharp


ImmutableQueue<int> queue = ImmutableQueue<int>.Empty;
queue = queue.Enqueue(1).Enqueue(2).Enqueue(3);
var (front, newQueue) = (queue.Peek(), queue.Dequeue());
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Stack<T>** | LIFO, O(1) push/pop, use for undo/redo, parsing, DFS |
| **Queue<T>** | FIFO, O(1) enqueue/dequeue, use for scheduling, BFS |
| **PriorityQueue** | Priority-based ordering, O(log n) operations |
| **ConcurrentQueue** | Thread-safe for multi-threaded sync scenarios |
| **Channel<T>** | Modern async producer-consumer pattern |
| **ImmutableStack/Queue** | Thread-safe immutable versions |

---

**Next Step**: Move to **Hash Tables / Dictionaries** when ready!
