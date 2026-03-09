# Trees (Binary, BST, AVL) in C#

## Overview

Trees are **hierarchical data structures** that model relationships and enable efficient searching, sorting, and hierarchical data representation. As an architect, you'll encounter trees in databases (B-trees), file systems, DOM structures, decision engines, and countless algorithms.

what does it mean B-trees? B-trees are a type of self-balancing tree data structure that maintains sorted data and allows for efficient insertion, deletion, and search operations. They are commonly used in databases and file systems to manage large amounts of data that cannot fit into memory.

what does it mean the B in B-trees? The "B" in B-trees does not have a specific meaning; it is simply a name given to this type of tree. Some sources suggest that it stands for "balanced" or "broad," but there is no official consensus on its origin.

---

## 1. Tree Terminology

```
                    [50]           ← Root (Level 0)
                   /    \
                [30]    [70]       ← Internal Nodes (Level 1)
               /    \      \
            [20]   [40]   [80]     ← Level 2
            /                \
         [10]               [90]   ← Leaf Nodes (Level 3)
```

| Term | Definition |
|------|------------|
| **Root** | Top node (no parent) |
| **Node** | Element containing data + references to children |
| **Edge** | Connection between nodes |
| **Leaf** | Node with no children |
| **Parent** | Node with children below it |
| **Child** | Node directly below another |
| **Sibling** | Nodes sharing the same parent |
| **Height** | Longest path from node to leaf |
| **Depth** | Distance from root to node |
| **Subtree** | Tree formed by a node and all descendants |

where are used trees? Trees are used in various applications such as:
- File systems (directories and files)
- Databases (B-trees for indexing)
- Compilers (abstract syntax trees)
- Decision trees in machine learning
- Hierarchical data representation (e.g., organizational charts, XML/JSON parsing)
- Network routing algorithms (e.g., spanning trees)
- Game development (scene graphs, AI decision trees)
- Expression evaluation (binary expression trees) like in calculators or programming languages.
- Version control systems (e.g., Git uses a tree structure to manage commits and branches)
- GUI frameworks (e.g., DOM trees in web development) Angular, React, etc.
- Data compression algorithms (e.g., Huffman coding trees) Huffman coding is a lossless data compression algorithm that uses a binary tree to represent the frequency of characters in a given input. The characters with higher frequencies are represented with shorter codes, while less frequent characters are represented with longer codes, resulting in efficient compression of data.

---

## 2. Types of Trees Covered

| Tree Type | Description | Use Case |
|-----------|-------------|----------|
| **Binary Tree** | Each node has at most 2 children | Expression parsing, Huffman coding |
| **Binary Search Tree (BST)** | Left < Parent < Right | Sorted data, searching |
| **AVL Tree** | Self-balancing BST | Guaranteed O(log n) operations |

---

### Hands-On: Project Setup

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

## 3. Binary Tree

### Exercise 1: Binary Tree Node & Structure

Create a file `BinaryTree.cs` and type the following:

```csharp
namespace DataStructures;

/// <summary>
/// Generic Binary Tree Node
/// </summary>
public class TreeNode<T>
{
    public T Value { get; set; }
    public TreeNode<T>? Left { get; set; }
    public TreeNode<T>? Right { get; set; }

    public TreeNode(T value)
    {
        Value = value;
    }

    public bool IsLeaf => Left is null && Right is null;

    public override string ToString() => Value?.ToString() ?? "null";
}

/// <summary>
/// Basic Binary Tree with traversal methods
/// </summary>
public class BinaryTree<T>
{
    public TreeNode<T>? Root { get; set; }

    public BinaryTree() { }

    public BinaryTree(T rootValue)
    {
        Root = new TreeNode<T>(rootValue);
    }

    // Calculate tree height
    public int Height => CalculateHeight(Root);

    private int CalculateHeight(TreeNode<T>? node)
    {
        if (node is null) return -1; // Empty tree has height -1
        return 1 + Math.Max(CalculateHeight(node.Left), CalculateHeight(node.Right));
    }

    // Count total nodes
    public int Count => CountNodes(Root);

    private int CountNodes(TreeNode<T>? node)
    {
        if (node is null) return 0;
        return 1 + CountNodes(node.Left) + CountNodes(node.Right);
    }

    // Count leaf nodes
    public int LeafCount => CountLeaves(Root);

    private int CountLeaves(TreeNode<T>? node)
    {
        if (node is null) return 0;
        if (node.IsLeaf) return 1;
        return CountLeaves(node.Left) + CountLeaves(node.Right);
    }

    // graphical representation (for small trees) in comment
     /*
        Example Tree:
                A
               / \
              B   C
             /   / \
            D   E   F

        Height: 2
        Count: 6
        Leaf Count: 3 (D, E, F)
     */

}
```

---

### Exercise 2: Tree Traversals (DFS)

Create `TreeTraversals.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Understanding traversals is fundamental.
/// Each traversal order has specific use cases.
/// </summary>
public static class TreeTraversals
{
    public static void Run()
    {
        Console.WriteLine("=== TREE TRAVERSALS ===\n");

        // Build sample tree:
        //        1
        //       / \
        //      2   3
        //     / \   \
        //    4   5   6

        var tree = new BinaryTree<int>(1);
        tree.Root!.Left = new TreeNode<int>(2); // what is ! in C#? The "!" operator in C# is called the null-forgiving operator. It is used to suppress compiler warnings about potential null reference exceptions. When you use "!" after a variable, you are telling the compiler that you are confident that the variable will not be null at runtime, even if it is declared as nullable. In this case, we are asserting that tree.Root will not be null when we access its Left property.

        // what happen if we try to access tree.Root.Left without the null-forgiving operator? If we try to access tree.Root.Left without the null-forgiving operator, the compiler will generate a warning about a potential null reference exception. This is because tree.Root is declared as nullable (TreeNode<int>?), and the compiler cannot guarantee that it will not be null at runtime. To avoid this warning, we can use the null-forgiving operator "!" to assert that tree.Root will not be null when we access its Left property.

        // what happen if we try to access tree.Root.Left when tree.Root is actually null? If we try to access tree.Root.Left when tree.Root is actually null, it will result in a NullReferenceException at runtime. This is because we are trying to access a property (Left) on a null object (Root). To prevent this, we should ensure that tree.Root is properly initialized before accessing its properties, or we can use null checks to handle the case where tree.Root might be null.
        tree.Root.Right = new TreeNode<int>(3);
        // what will happen if we pass a diferent data type to this TreeNode like a string? If we try to pass a different data type, such as a string, to the TreeNode<int> constructor, it will result in a compile-time error. This is because TreeNode<int> is a generic class that is specifically designed to hold values of type int. If we want to use a different data type, we would need to create a new instance of TreeNode with the appropriate type parameter, such as TreeNode<string> for strings.

        // do you mean if I pass TreeNode<string> instead of TreeNode<int>? Yes, if you want to use a TreeNode that holds string values instead of int values, you would create an instance of TreeNode<string>. 

        // Can this cause a problem if I create a node with string? No, creating a node with string values using TreeNode<string> will not cause a problem as long as you are consistent with the type parameter throughout your code. The generic type system in C# ensures that you can only use the specified type (in this case, string) for that instance of TreeNode. However, if you try to mix types (e.g., using TreeNode<int> and TreeNode<string> together without proper handling), it could lead to confusion or errors in your code. Always ensure that you are using the correct type parameter for your TreeNode instances to avoid any issues.
        tree.Root.Left.Left = new TreeNode<int>(4);
        tree.Root.Left.Right = new TreeNode<int>(5);
        tree.Root.Right.Right = new TreeNode<int>(6);

        Console.WriteLine($"Tree Height: {tree.Height}");
        Console.WriteLine($"Node Count: {tree.Count}");
        Console.WriteLine($"Leaf Count: {tree.LeafCount}");

        // 1. Pre-Order: Root → Left → Right (NLR)
        // Use case: Copy tree, prefix expression
        Console.WriteLine("\nPre-Order (Root→Left→Right):");
        PreOrder(tree.Root, v => Console.Write($"{v} "));
        Console.WriteLine();

        // 2. In-Order: Left → Root → Right (LNR)
        // Use case: BST sorted output
        Console.WriteLine("\nIn-Order (Left→Root→Right):");
        InOrder(tree.Root, v => Console.Write($"{v} "));
        Console.WriteLine();

        // 3. Post-Order: Left → Right → Root (LRN)
        // Use case: Delete tree, postfix expression
        Console.WriteLine("\nPost-Order (Left→Right→Root):");
        PostOrder(tree.Root, v => Console.Write($"{v} "));
        Console.WriteLine();

        // 4. Level-Order (BFS): Level by level
        // Use case: Find shortest path, serialize tree
        Console.WriteLine("\nLevel-Order (BFS):");
        LevelOrder(tree.Root, v => Console.Write($"{v} "));
        Console.WriteLine();
    }

    // Recursive Pre-Order
    // What does this method do? This method performs a pre-order traversal of a binary tree. It processes the current node (root) first, then recursively traverses the left subtree, followed by the right subtree. The action parameter is a delegate that defines what to do with the value of each node during the traversal (e.g., print it, store it in a list, etc.).

    // what is a pre-order traversal? A pre-order traversal is a depth(spanish: profundidad)-first traversal method for binary trees where the nodes are processed in the following order: Root → Left → Right. This means that the current node (root) is processed first, then the left subtree is traversed recursively, followed by the right subtree. Pre-order traversal is often used for tasks such as copying a tree or generating a prefix expression from an expression tree.

    // I don't understand the order of the traversal. Can you explain it with an example? Sure! Let's take the following binary tree as an example:

        1
       / \
      2   3
     / \   \
    4   5   6

    // Pre-Order traversal of the above tree would visit nodes in the following order: 1, 2, 4, 5, 3, 6
    
    // what does it mean the parameter action? The parameter "action" is a delegate of type Action<T> that represents a method that takes a single parameter of type T and returns void. In the context of the PreOrder method, it is used to define what operation should be performed on the value of each node during the traversal. For example, if you want to print the value of each node, you can pass in an action like "v => Console.Write($"{v} ")". This allows you to customize the behavior of the traversal without changing the traversal logic itself.

    // what does in this case action delegate? In this case, the action delegate is a way to specify what you want to do with the value of each node as you traverse the tree. It allows you to pass in a method or lambda expression that will be called for each node's value during the traversal. For example, if you want to print the value of each node, you can pass in an action like "v => Console.Write($"{v} ")". This means that for every node visited during the pre-order traversal, its value will be printed to the console followed by a space. The use of an action delegate provides flexibility, allowing you to perform different operations on the node values without modifying the traversal logic.
    public static void PreOrder<T>(TreeNode<T>? node, Action<T> action)
    {
        if (node is null) return;
        action(node.Value);           // Process root
        PreOrder(node.Left, action);  // Process left subtree
        PreOrder(node.Right, action); // Process right subtree
    }

    // Recursive In-Order
    // what is an in-order traversal? An in-order traversal is a depth(spanish: profundidad)-first traversal method for binary trees where the nodes are processed in the following order: Left → Root → Right. This means that the left subtree is traversed recursively first, then the current node (root) is processed, followed by the right subtree. In-order traversal is commonly used for binary search trees (BSTs) because it processes the nodes in sorted order.

     // I don't understand the order of the traversal. Can you explain it with an example? Sure! Let's take the same binary tree as an example:

        1
       / \
      2   3
     / \   \
    4   5   6

    // In-Order traversal of the above tree would visit nodes in the following order: 4, 2, 5, 1, 3, 6
    public static void InOrder<T>(TreeNode<T>? node, Action<T> action)
    {
        if (node is null) return;
        InOrder(node.Left, action);   // Process left subtree
        action(node.Value);           // Process root
        InOrder(node.Right, action);  // Process right subtree
    }

    // Recursive Post-Order
    // what is a post-order traversal? A post-order traversal is a depth(spanish: profundidad)-first traversal method for binary trees where the nodes are processed in the following order: Left → Right → Root. This means that the left subtree is traversed recursively first, then the right subtree, and finally the current node (root) is processed. Post-order traversal is often used for tasks such as deleting a tree or generating a postfix expression from an expression tree.

    // an example of when to use post-order traversal? One common example of when to use post-order traversal is when you want to delete a binary tree. In post-order traversal, you process the left and right subtrees before processing the root node. This means that you will delete the leaf nodes first, then the internal nodes, and finally the root node. This order ensures that you do not attempt to access or delete a node that has already been deleted, which can lead to errors. Another example is when evaluating an expression tree, where post-order traversal allows you to evaluate the operands before applying the operator at the root node.

    // I don't understand the order of the traversal. Can you explain it with an example? Sure! Let's take the same binary tree as an example:

        1
       / \
      2   3
     / \   \
    4   5   6

    // Post-Order traversal of the above tree would visit nodes in the following order: 4, 5, 2, 6, 3, 1
    public static void PostOrder<T>(TreeNode<T>? node, Action<T> action)
    {
        if (node is null) return;
        PostOrder(node.Left, action);  // Process left subtree
        PostOrder(node.Right, action); // Process right subtree
        action(node.Value);            // Process root
    }

    // Iterative Level-Order (BFS) using Queue
    // what is level-order traversal? Level-order traversal, also known as breadth(spanish: amplitud)-first traversal, is a method of traversing a binary tree where the nodes are processed level by level from top to bottom and from left to right. This means that all nodes at the same depth (level) are processed before moving on to the next level. Level-order traversal is often implemented using a queue data structure to keep track of the nodes at each level.

     // an example of when to use level-order traversal? One common example of when to use level-order traversal is when you want to serialize a binary tree (convert it into a format that can be easily stored or transmitted). Level-order traversal allows you to capture the structure of the tree, including null nodes, which is essential for accurate serialization and deserialization. Another example is when you want to find the shortest path from the root node to a specific target node in an unweighted binary tree. Level-order traversal ensures that you explore all nodes at the current depth before moving deeper into the tree, which helps in finding the shortest path efficiently.

    // I don't understand the order of the traversal. Can you explain it with an example? Sure! Let's take the same binary tree as an example:

        1
       / \
      2   3
     / \   \
    4   5   6
    // Level-Order traversal of the above tree would visit nodes in the following order: 1, 2, 3, 4, 5, 6
    public static void LevelOrder<T>(TreeNode<T>? root, Action<T> action)
    {
        if (root is null) return;

        Queue<TreeNode<T>> queue = new();
        queue.Enqueue(root);

        while (queue.Count > 0)
        {
            var node = queue.Dequeue();
            action(node.Value);

            if (node.Left is not null) queue.Enqueue(node.Left);
            if (node.Right is not null) queue.Enqueue(node.Right);
        }
    }
}
```

---

### Exercise 3: Iterative Traversals (Without Recursion)

Create `IterativeTraversals.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Iterative traversals avoid stack overflow
/// for very deep trees. Essential for production systems.
/// </summary>
public static class IterativeTraversals
{
    public static void Run()
    {
        Console.WriteLine("\n=== ITERATIVE TRAVERSALS ===\n");

        //        10
        //       /  \
        //      5    15
        //     / \     \
        //    3   7    20

        var root = new TreeNode<int>(10)
        {
            Left = new TreeNode<int>(5)
            {
                Left = new TreeNode<int>(3),
                Right = new TreeNode<int>(7)
            },
            Right = new TreeNode<int>(15)
            {
                Right = new TreeNode<int>(20)
            }
        };

        Console.WriteLine("Iterative Pre-Order:");
        foreach (var val in PreOrderIterative(root))
        {
            Console.Write($"{val} ");
        }

        Console.WriteLine("\n\nIterative In-Order:");
        foreach (var val in InOrderIterative(root))
        {
            Console.Write($"{val} ");
        }

        Console.WriteLine("\n\nIterative Post-Order:");
        foreach (var val in PostOrderIterative(root))
        {
            Console.Write($"{val} ");
        }

        Console.WriteLine("\n\nLevel-Order with Levels:");
        var levels = LevelOrderWithLevels(root);
        for (int i = 0; i < levels.Count; i++)
        {
            Console.WriteLine($"  Level {i}: [{string.Join(", ", levels[i])}]");
        }
    }

    // Iterative Pre-Order using Stack
    public static IEnumerable<T> PreOrderIterative<T>(TreeNode<T>? root)
    {
        if (root is null) yield break; // what does yield break do? The "yield break" statement is used in an iterator method to indicate that the iteration should stop and no more values will be returned. When the "yield break" statement is executed, it exits the iterator method and signals to the caller that there are no more items to iterate over. In this case, if the root of the tree is null, we use "yield break" to immediately end the iteration since there are no nodes to traverse.

        Stack<TreeNode<T>> stack = new(); // what is a stack? A stack is a data structure that follows the Last In, First Out (LIFO) principle. It allows you to add (push) and remove (pop) elements in a specific order. The last element added to the stack will be the first one to be removed. In the context of tree traversal, we use a stack to keep track of the nodes we need to visit next, allowing us to traverse the tree iteratively without using recursion.
        stack.Push(root);

        while (stack.Count > 0)
        {
            var node = stack.Pop();
            yield return node.Value; // what does yeild return do? The "yield return" statement is used in an iterator method to return a value to the caller while maintaining the state of the method. When "yield return" is executed, it returns the specified value to the caller and pauses the execution of the method. The next time the caller requests the next item in the iteration, the method resumes execution right after the "yield return" statement, allowing it to continue generating values one at a time. In this case, we use "yield return node.Value" to return the value of each node during the pre-order traversal.

            // Push right first so left is processed first
            if (node.Right is not null) stack.Push(node.Right);
            if (node.Left is not null) stack.Push(node.Left);
        }
    }

    // Iterative In-Order using Stack
    public static IEnumerable<T> InOrderIterative<T>(TreeNode<T>? root)
    {        
        Stack<TreeNode<T>> stack = new();
        // what is the purpose of having a Stack in this method? The stack is used to keep track of the nodes that we need to visit as we traverse the tree iteratively. In an in-order traversal, we need to process the left subtree first, then the current node (root), and finally the right subtree. The stack allows us to remember the nodes we have visited and the order in which we need to process them. As we go down the left side of the tree, we push nodes onto the stack until we reach a leaf node. Then, we pop nodes from the stack to process them and move to their right subtrees as needed.
        var current = root;

        while (current is not null || stack.Count > 0)
        {
            // Go to leftmost node
            while (current is not null)
            {
                stack.Push(current);
                current = current.Left;
            }

            // Process current node
            current = stack.Pop();
            yield return current.Value;

            // Move to right subtree
            current = current.Right;
        }         
    }

    // Iterative Post-Order using Two Stacks
    public static IEnumerable<T> PostOrderIterative<T>(TreeNode<T>? root)
    {
        if (root is null) yield break;

        Stack<TreeNode<T>> stack1 = new();
        Stack<TreeNode<T>> stack2 = new();

        // why two stacks? The two-stack approach is used to achieve post-order traversal iteratively. The first stack (stack1) is used to traverse the tree in a modified pre-order manner (Root → Right → Left), while the second stack (stack2) is used to reverse the order of the nodes so that they are processed in the correct post-order sequence (Left → Right → Root). By pushing nodes onto stack2 as we pop them from stack1, we effectively reverse the order of processing, allowing us to yield the values in post-order without recursion.
        stack1.Push(root);

        while (stack1.Count > 0)
        {
            var node = stack1.Pop();
            stack2.Push(node);

            if (node.Left is not null) stack1.Push(node.Left);
            if (node.Right is not null) stack1.Push(node.Right);
        }

        while (stack2.Count > 0)
        {
            yield return stack2.Pop().Value;
        }
    }

    // Level-Order returning list of levels
    public static List<List<T>> LevelOrderWithLevels<T>(TreeNode<T>? root)
    {
        List<List<T>> result = new();
        if (root is null) return result;

        Queue<TreeNode<T>> queue = new();
        //why to use a Queue in this method? A queue is used in level-order traversal to keep track of the nodes at each level of the tree. In level-order traversal, we want to process all nodes at the current depth before moving on to the next level. The queue allows us to enqueue nodes as we visit them and ensures that we process them in the order they were added (first-in, first-out). As we dequeue nodes, we can enqueue their children, which helps us maintain the correct order of processing for each level of the tree.
        queue.Enqueue(root);

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            List<T> currentLevel = new();

            for (int i = 0; i < levelSize; i++)
            {
                var node = queue.Dequeue();
                currentLevel.Add(node.Value);

                if (node.Left is not null) queue.Enqueue(node.Left);
                if (node.Right is not null) queue.Enqueue(node.Right);
            }

            result.Add(currentLevel);
        }

        return result;
    }
}
```

---

## 4. Binary Search Tree (BST)

### Key Property

For every node:
- All values in **left subtree** are **less than** the node
- All values in **right subtree** are **greater than** the node

```
         50
        /  \
      30    70      30 < 50 < 70
     /  \     \
   20   40    80    20 < 30 < 40    70 < 80
```

### Time Complexity

| Operation | Average | Worst (Unbalanced) |
|-----------|---------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

---

### Exercise 4: Binary Search Tree Implementation

Create `BinarySearchTree.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// Binary Search Tree implementation
/// ARCHITECT NOTE: BST is the foundation for many database indexes
/// </summary>
public class BinarySearchTree<T> where T : IComparable<T>
{
    public TreeNode<T>? Root { get; private set; }
    public int Count { get; private set; } // what is this count for? The "Count" property is used to keep track of the number of nodes currently in the binary search tree. It is incremented each time a new node is inserted and decremented when a node is deleted. This allows us to quickly retrieve the total number of nodes in the tree without having to traverse it, which can be useful for various operations and for understanding the size of the tree at any given time.

    // INSERT - O(log n) average, O(n) worst
    public void Insert(T value)
    {
        Root = InsertRecursive(Root, value);
        Count++;
    }

    private TreeNode<T> InsertRecursive(TreeNode<T>? node, T value)
    {
        // What does it mean insert recursively? Inserting recursively means that the method calls itself to navigate through the tree structure until it finds the correct position for the new value. The method starts at the root and compares the value to be inserted with the current node's value. If the value is less than the current node's value, it goes to the left subtree; if it's greater, it goes to the right subtree. This process continues until it reaches a null position where the new node can be inserted. The recursive approach simplifies the code and makes it easier to read, as it naturally follows the structure of the tree.
        if (node is null)
            return new TreeNode<T>(value);

        int comparison = value.CompareTo(node.Value);

        // where is declared CompareTo? The CompareTo method is declared in the IComparable<T> interface, which is a generic interface in C#. When a type implements IComparable<T>, it must provide an implementation for the CompareTo method, which compares the current instance with another object of the same type and returns an integer that indicates their relative order. In this case, since our BinarySearchTree class has a type constraint "where T : IComparable<T>", we can call the CompareTo method on instances of T to compare their values and determine whether to navigate left or right in the tree during insertion.

        // is compareTo return a negative number if value is less than node.Value, zero if they are equal, and a positive number if value is greater than node.Value? Yes, that's correct. The CompareTo method returns:
        // - A negative number if the current instance (value) is less than the object being compared to (node.Value).
        // - Zero if the current instance (value) is equal to the object being compared to (node.Value).
        // - A positive number if the current instance (value) is greater than the object being compared to (node.Value). This allows us to determine the correct position for the new value in the binary search tree based on its relationship to the existing node values.

        // what happen if we try to insert a duplicate value? In this implementation of the binary search tree, if we try to insert a duplicate value (a value that is equal to an existing node's value), the method will simply ignore the insertion and return the existing node without creating a new one. This means that duplicate values will not be added to the tree, and the structure of the tree will remain unchanged. If you want to allow duplicates, you could modify the insertion logic to decide whether to go left or right when values are equal, or you could choose to store duplicates in a list at each node.

        if (comparison < 0)
            node.Left = InsertRecursive(node.Left, value);
        else if (comparison > 0)
            node.Right = InsertRecursive(node.Right, value);
        // If equal, we don't insert duplicates (or could go left/right)

        return node;
    }

    // SEARCH - O(log n) average, O(n) worst
    public bool Contains(T value)
    {
        return Search(Root, value) is not null;
    }

    public TreeNode<T>? Search(TreeNode<T>? node, T value)
    {
        if (node is null)
            return null;

        int comparison = value.CompareTo(node.Value);

        if (comparison == 0)
            return node;
        else if (comparison < 0)
            return Search(node.Left, value);
        else
            return Search(node.Right, value);
    }

    // Iterative Search (more efficient)
    public TreeNode<T>? SearchIterative(T value)
    {
        var current = Root;

        while (current is not null)
        {
            int comparison = value.CompareTo(current.Value);

            if (comparison == 0)
                return current;
            else if (comparison < 0)
                current = current.Left;
            else
                current = current.Right;
        }

        return null;
    }

    // MINIMUM - Leftmost node
    public T? Min()
    {
        var node = FindMin(Root);
        return node is not null ? node.Value : default;
    }

    private TreeNode<T>? FindMin(TreeNode<T>? node)
    {
        if (node is null) return null;
        while (node.Left is not null)
            node = node.Left;
        return node;
    }

    // MAXIMUM - Rightmost node
    public T? Max()
    {
        var node = FindMax(Root);
        return node is not null ? node.Value : default;
    }

    private TreeNode<T>? FindMax(TreeNode<T>? node)
    {
        if (node is null) return null;
        while (node.Right is not null)
            node = node.Right;
        return node;
    }

    // DELETE - O(log n) average, O(n) worst
    public bool Delete(T value)
    {
        int originalCount = Count;
        Root = DeleteRecursive(Root, value);
        return Count < originalCount;
    }

    private TreeNode<T>? DeleteRecursive(TreeNode<T>? node, T value)
    {
        if (node is null)
            return null;

        int comparison = value.CompareTo(node.Value);

        if (comparison < 0)
        {
            node.Left = DeleteRecursive(node.Left, value);
        }
        else if (comparison > 0)
        {
            node.Right = DeleteRecursive(node.Right, value);
        }
        else
        {
            // Found node to delete
            Count--;

            // Case 1: Leaf node
            if (node.IsLeaf)
                return null;

            // Case 2: One child
            if (node.Left is null)
                return node.Right;
            if (node.Right is null)
                return node.Left;

            // Case 3: Two children
            // Replace with in-order successor (smallest in right subtree)
            var successor = FindMin(node.Right)!;
            node.Value = successor.Value;
            node.Right = DeleteRecursive(node.Right, successor.Value);
            Count++; // Compensate for the recursive delete
        }

        return node;
    }

    // IN-ORDER TRAVERSAL - Returns sorted sequence
    public IEnumerable<T> InOrder()
    {
        return InOrderTraversal(Root);
    }

    private IEnumerable<T> InOrderTraversal(TreeNode<T>? node)
    {
        if (node is null) yield break;

        foreach (var val in InOrderTraversal(node.Left))
            yield return val;

        yield return node.Value;

        foreach (var val in InOrderTraversal(node.Right))
            yield return val;
    }

    // VALIDATE BST
    public bool IsValidBST()
    {
        return IsValidBST(Root, default, default, false, false);
    }

    private bool IsValidBST(TreeNode<T>? node, T? min, T? max, bool hasMin, bool hasMax)
    {
        if (node is null) return true;

        if (hasMin && node.Value.CompareTo(min) <= 0) return false;
        if (hasMax && node.Value.CompareTo(max) >= 0) return false;

        return IsValidBST(node.Left, min, node.Value, hasMin, true) &&
               IsValidBST(node.Right, node.Value, max, true, hasMax);
    }

    // Height
    public int Height => CalculateHeight(Root);

    private int CalculateHeight(TreeNode<T>? node)
    {
        if (node is null) return -1;
        return 1 + Math.Max(CalculateHeight(node.Left), CalculateHeight(node.Right));
    }
}
```

---

### Exercise 5: BST Demo

Create `BSTDemo.cs`:

```csharp
namespace DataStructures;

public static class BSTDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== BINARY SEARCH TREE ===\n");

        var bst = new BinarySearchTree<int>();

        // Insert values
        int[] values = { 50, 30, 70, 20, 40, 60, 80, 15, 25, 35, 45 };
        Console.WriteLine($"Inserting: {string.Join(", ", values)}");

        foreach (var val in values)
        {
            bst.Insert(val);
        }

        //           50
        //         /    \
        //       30      70
        //      /  \    /  \
        //    20   40  60  80
        //   /  \  / \
        //  15 25 35 45

        Console.WriteLine($"\nTree Height: {bst.Height}");
        Console.WriteLine($"Node Count: {bst.Count}");
        Console.WriteLine($"Is Valid BST: {bst.IsValidBST()}");

        // In-order traversal (sorted!)
        Console.WriteLine($"\nIn-Order (Sorted): {string.Join(", ", bst.InOrder())}");

        // Min and Max
        Console.WriteLine($"\nMin: {bst.Min()}");
        Console.WriteLine($"Max: {bst.Max()}");

        // Search
        Console.WriteLine($"\nContains 40: {bst.Contains(40)}");
        Console.WriteLine($"Contains 99: {bst.Contains(99)}");

        // Delete
        Console.WriteLine("\n--- Deletion ---");
        Console.WriteLine($"Delete 20 (leaf): {bst.Delete(20)}");
        Console.WriteLine($"In-Order: {string.Join(", ", bst.InOrder())}");

        Console.WriteLine($"Delete 30 (two children): {bst.Delete(30)}");
        Console.WriteLine($"In-Order: {string.Join(", ", bst.InOrder())}");

        Console.WriteLine($"Delete 50 (root): {bst.Delete(50)}");
        Console.WriteLine($"In-Order: {string.Join(", ", bst.InOrder())}");

        // Problem with unbalanced insertion
        Console.WriteLine("\n--- Unbalanced BST Problem ---");
        var unbalanced = new BinarySearchTree<int>();
        foreach (var val in new[] { 1, 2, 3, 4, 5, 6, 7 })
        {
            unbalanced.Insert(val);
        }
        Console.WriteLine($"Sorted insert [1-7]:");
        Console.WriteLine($"  Height: {unbalanced.Height} (should be ~2 for balanced)");
        Console.WriteLine($"  This degrades to O(n) operations!");
        Console.WriteLine("  → Solution: Self-balancing trees (AVL, Red-Black)");
    }
}
```

---

## 5. AVL Tree (Self-Balancing BST)

### What is an AVL Tree?

An AVL tree is a **self-balancing BST** where the heights of left and right subtrees differ by at most 1 (balance factor: -1, 0, or +1).

### Balance Factor

```
Balance Factor = Height(Left Subtree) - Height(Right Subtree)

Valid: -1, 0, +1
Invalid: < -1 or > +1 (requires rotation)
```

### Rotations

```
RIGHT ROTATION (LL Case):        LEFT ROTATION (RR Case):
     y                               x
    / \                             / \
   x   T3   →    x                T1   y
  / \           / \                   / \
 T1  T2       T1   y                T2  T3
                  / \
                T2  T3

LEFT-RIGHT (LR Case):            RIGHT-LEFT (RL Case):
     z                               z
    /                                 \
   x      →  Left then Right          x   →  Right then Left
    \                                /
     y                              y
```

---

### Exercise 6: AVL Tree Implementation

Create `AVLTree.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// AVL Tree Node with height tracking
/// </summary>
public class AVLNode<T>
{
    public T Value { get; set; }
    public AVLNode<T>? Left { get; set; }
    public AVLNode<T>? Right { get; set; }
    public int Height { get; set; }

    public AVLNode(T value)
    {
        Value = value;
        Height = 1; // New node has height 1
    }

    public override string ToString() => $"{Value}(h={Height})";
}

/// <summary>
/// Self-balancing AVL Tree
/// ARCHITECT INSIGHT: Guarantees O(log n) for all operations
/// </summary>
public class AVLTree<T> where T : IComparable<T>
{
    public AVLNode<T>? Root { get; private set; }
    public int Count { get; private set; }

    // Get height of node (null-safe)
    private int GetHeight(AVLNode<T>? node) => node?.Height ?? 0;

    // Calculate balance factor
    private int GetBalanceFactor(AVLNode<T>? node)
    {
        if (node is null) return 0;
        return GetHeight(node.Left) - GetHeight(node.Right);
    }

    // Update height after rotation
    private void UpdateHeight(AVLNode<T> node)
    {
        node.Height = 1 + Math.Max(GetHeight(node.Left), GetHeight(node.Right));
    }

    // RIGHT ROTATION (for Left-Left case)
    //     y                x
    //    / \              / \
    //   x   T3    →     T1   y
    //  / \                  / \
    // T1  T2              T2  T3
    private AVLNode<T> RotateRight(AVLNode<T> y)
    {
        var x = y.Left!;
        var T2 = x.Right;

        // Perform rotation
        x.Right = y;
        y.Left = T2;

        // Update heights (y first, then x)
        UpdateHeight(y);
        UpdateHeight(x);

        return x; // New root
    }

    // LEFT ROTATION (for Right-Right case)
    //   x                    y
    //  / \                  / \
    // T1  y        →      x   T3
    //    / \             / \
    //   T2  T3         T1  T2
    private AVLNode<T> RotateLeft(AVLNode<T> x)
    {
        var y = x.Right!;
        var T2 = y.Left;

        // Perform rotation
        y.Left = x;
        x.Right = T2;

        // Update heights (x first, then y)
        UpdateHeight(x);
        UpdateHeight(y);

        return y; // New root
    }

    // INSERT with auto-balancing
    public void Insert(T value)
    {
        Root = InsertRecursive(Root, value);
        Count++;
    }

    private AVLNode<T> InsertRecursive(AVLNode<T>? node, T value)
    {
        // 1. Standard BST insert
        if (node is null)
            return new AVLNode<T>(value);

        int comparison = value.CompareTo(node.Value);

        if (comparison < 0)
            node.Left = InsertRecursive(node.Left, value);
        else if (comparison > 0)
            node.Right = InsertRecursive(node.Right, value);
        else
            return node; // Duplicate, don't insert

        // 2. Update height
        UpdateHeight(node);

        // 3. Get balance factor
        int balance = GetBalanceFactor(node);

        // 4. Balance if needed (4 cases)

        // Left Left Case
        if (balance > 1 && value.CompareTo(node.Left!.Value) < 0)
            return RotateRight(node);

        // Right Right Case
        if (balance < -1 && value.CompareTo(node.Right!.Value) > 0)
            return RotateLeft(node);

        // Left Right Case
        if (balance > 1 && value.CompareTo(node.Left!.Value) > 0)
        {
            node.Left = RotateLeft(node.Left);
            return RotateRight(node);
        }

        // Right Left Case
        if (balance < -1 && value.CompareTo(node.Right!.Value) < 0)
        {
            node.Right = RotateRight(node.Right);
            return RotateLeft(node);
        }

        return node; // No imbalance
    }

    // DELETE with auto-balancing
    public bool Delete(T value)
    {
        int originalCount = Count;
        Root = DeleteRecursive(Root, value);
        return Count < originalCount;
    }

    private AVLNode<T>? DeleteRecursive(AVLNode<T>? node, T value)
    {
        // 1. Standard BST delete
        if (node is null)
            return null;

        int comparison = value.CompareTo(node.Value);

        if (comparison < 0)
            node.Left = DeleteRecursive(node.Left, value);
        else if (comparison > 0)
            node.Right = DeleteRecursive(node.Right, value);
        else
        {
            // Found node to delete
            Count--;

            // Node with one or no child
            if (node.Left is null)
                return node.Right;
            if (node.Right is null)
                return node.Left;

            // Node with two children
            var successor = FindMin(node.Right);
            node.Value = successor.Value;
            node.Right = DeleteRecursive(node.Right, successor.Value);
            Count++; // Compensate
        }

        // 2. Update height
        UpdateHeight(node);

        // 3. Get balance factor
        int balance = GetBalanceFactor(node);

        // 4. Balance if needed

        // Left Left Case
        if (balance > 1 && GetBalanceFactor(node.Left) >= 0)
            return RotateRight(node);

        // Left Right Case
        if (balance > 1 && GetBalanceFactor(node.Left) < 0)
        {
            node.Left = RotateLeft(node.Left!);
            return RotateRight(node);
        }

        // Right Right Case
        if (balance < -1 && GetBalanceFactor(node.Right) <= 0)
            return RotateLeft(node);

        // Right Left Case
        if (balance < -1 && GetBalanceFactor(node.Right) > 0)
        {
            node.Right = RotateRight(node.Right!);
            return RotateLeft(node);
        }

        return node;
    }

    private AVLNode<T> FindMin(AVLNode<T> node)
    {
        while (node.Left is not null)
            node = node.Left;
        return node;
    }

    // Search - O(log n) guaranteed
    public bool Contains(T value)
    {
        var current = Root;
        while (current is not null)
        {
            int comparison = value.CompareTo(current.Value);
            if (comparison == 0) return true;
            current = comparison < 0 ? current.Left : current.Right;
        }
        return false;
    }

    // In-Order Traversal
    public IEnumerable<T> InOrder()
    {
        return InOrderTraversal(Root);
    }

    private IEnumerable<T> InOrderTraversal(AVLNode<T>? node)
    {
        if (node is null) yield break;
        foreach (var v in InOrderTraversal(node.Left)) yield return v;
        yield return node.Value;
        foreach (var v in InOrderTraversal(node.Right)) yield return v;
    }

    // Tree height
    public int Height => GetHeight(Root);

    // Is balanced check
    public bool IsBalanced => CheckBalance(Root);

    private bool CheckBalance(AVLNode<T>? node)
    {
        if (node is null) return true;
        int balance = GetBalanceFactor(node);
        return Math.Abs(balance) <= 1 &&
               CheckBalance(node.Left) &&
               CheckBalance(node.Right);
    }
}
```

---

### Exercise 7: AVL Tree Demo

Create `AVLDemo.cs`:

```csharp
namespace DataStructures;

public static class AVLDemo
{
    public static void Run()
    {
        Console.WriteLine("\n=== AVL TREE (Self-Balancing) ===\n");

        var avl = new AVLTree<int>();

        // Insert in sorted order (worst case for regular BST)
        Console.WriteLine("Inserting 1-15 in sorted order:");
        for (int i = 1; i <= 15; i++)
        {
            avl.Insert(i);
        }

        Console.WriteLine($"AVL Height: {avl.Height}");
        Console.WriteLine($"Expected balanced height: ~{Math.Ceiling(Math.Log2(16))}");
        Console.WriteLine($"Is Balanced: {avl.IsBalanced}");
        Console.WriteLine($"In-Order: {string.Join(", ", avl.InOrder())}");

        // Compare with BST
        var bst = new BinarySearchTree<int>();
        for (int i = 1; i <= 15; i++)
        {
            bst.Insert(i);
        }
        Console.WriteLine($"\nBST Height (same data): {bst.Height}");
        Console.WriteLine("BST degrades to linked list!");

        // Demonstrate rotations
        Console.WriteLine("\n--- Rotation Demonstration ---");
        var demo = new AVLTree<int>();

        Console.WriteLine("Insert 30, 20, 10 (triggers Right Rotation):");
        demo.Insert(30);
        demo.Insert(20);
        demo.Insert(10);
        Console.WriteLine($"  Height: {demo.Height}, Balanced: {demo.IsBalanced}");
        Console.WriteLine($"  In-Order: {string.Join(", ", demo.InOrder())}");

        Console.WriteLine("\nInsert 40, 50 (triggers Left Rotation):");
        demo.Insert(40);
        demo.Insert(50);
        Console.WriteLine($"  Height: {demo.Height}, Balanced: {demo.IsBalanced}");
        Console.WriteLine($"  In-Order: {string.Join(", ", demo.InOrder())}");

        // Delete operations
        Console.WriteLine("\n--- Deletion with Rebalancing ---");
        Console.WriteLine($"Before delete: {string.Join(", ", demo.InOrder())}");
        demo.Delete(10);
        Console.WriteLine($"After delete 10: {string.Join(", ", demo.InOrder())}");
        Console.WriteLine($"Still balanced: {demo.IsBalanced}");

        // Performance comparison
        Console.WriteLine("\n--- Performance Comparison ---");
        PerformanceComparison();
    }

    private static void PerformanceComparison()
    {
        const int N = 10000;
        var sw = System.Diagnostics.Stopwatch.StartNew();

        // AVL Tree
        var avl = new AVLTree<int>();
        for (int i = 0; i < N; i++)
            avl.Insert(i);
        sw.Stop();
        Console.WriteLine($"AVL Insert {N} sorted items: {sw.ElapsedMilliseconds}ms, Height: {avl.Height}");

        // BST
        sw.Restart();
        var bst = new BinarySearchTree<int>();
        for (int i = 0; i < N; i++)
            bst.Insert(i);
        sw.Stop();
        Console.WriteLine($"BST Insert {N} sorted items: {sw.ElapsedMilliseconds}ms, Height: {bst.Height}");

        // Search performance
        sw.Restart();
        for (int i = 0; i < 1000; i++)
            avl.Contains(N / 2);
        sw.Stop();
        Console.WriteLine($"\nAVL 1000 searches: {sw.ElapsedMilliseconds}ms");

        sw.Restart();
        for (int i = 0; i < 1000; i++)
            bst.Contains(N / 2);
        sw.Stop();
        Console.WriteLine($"BST 1000 searches: {sw.ElapsedMilliseconds}ms");
    }
}
```

---

### Exercise 8: Tree Visualization

Create `TreeVisualizer.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// Utility to visualize trees in console
/// </summary>
public static class TreeVisualizer
{
    public static void Run()
    {
        Console.WriteLine("\n=== TREE VISUALIZATION ===\n");

        var avl = new AVLTree<int>();
        foreach (var val in new[] { 50, 30, 70, 20, 40, 60, 80, 10, 25 })
        {
            avl.Insert(val);
        }

        Console.WriteLine("AVL Tree Structure:");
        PrintTree(avl.Root);

        Console.WriteLine("\n\nLevel-by-Level View:");
        PrintLevels(avl.Root);
    }

    public static void PrintTree<T>(AVLNode<T>? root, string indent = "", bool isLast = true)
    {
        if (root is null) return;

        Console.Write(indent);
        Console.Write(isLast ? "└── " : "├── ");
        Console.WriteLine(root.Value);

        indent += isLast ? "    " : "│   ";

        var children = new List<AVLNode<T>?> { root.Left, root.Right }
            .Where(c => c != null)
            .ToList();

        for (int i = 0; i < children.Count; i++)
        {
            PrintTree(children[i], indent, i == children.Count - 1);
        }
    }

    public static void PrintLevels<T>(AVLNode<T>? root)
    {
        if (root is null) return;

        Queue<AVLNode<T>?> queue = new();
        queue.Enqueue(root);

        int level = 0;
        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            Console.Write($"Level {level}: ");

            for (int i = 0; i < levelSize; i++)
            {
                var node = queue.Dequeue();
                if (node is not null)
                {
                    Console.Write($"{node.Value} ");
                    queue.Enqueue(node.Left);
                    queue.Enqueue(node.Right);
                }
            }
            Console.WriteLine();
            level++;

            // Stop if all remaining are null
            if (queue.All(n => n is null)) break;
        }
    }
}
```

---

## 6. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DataStructures;

Console.WriteLine("╔═══════════════════════════════════════════════════════╗");
Console.WriteLine("║   TREES (Binary, BST, AVL) - ARCHITECT TRAINING       ║");
Console.WriteLine("╚═══════════════════════════════════════════════════════╝");

TreeTraversals.Run();
IterativeTraversals.Run();
BSTDemo.Run();
AVLDemo.Run();
TreeVisualizer.Run();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ Use BINARY TREE when:                                      │");
Console.WriteLine("│   • Representing hierarchical data (file systems, DOM)     │");
Console.WriteLine("│   • Expression parsing (syntax trees)                      │");
Console.WriteLine("│   • Huffman encoding                                       │");
Console.WriteLine("├────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use BST when:                                              │");
Console.WriteLine("│   • Need sorted data with fast search                      │");
Console.WriteLine("│   • Data mostly random (not pre-sorted)                    │");
Console.WriteLine("│   • Simple implementation preferred                        │");
Console.WriteLine("├────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use AVL TREE when:                                         │");
Console.WriteLine("│   • Data may arrive sorted or nearly sorted                │");
Console.WriteLine("│   • Need guaranteed O(log n) operations                    │");
Console.WriteLine("│   • Read-heavy workloads (more rotations on write)         │");
Console.WriteLine("├────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use RED-BLACK TREE when:                                   │");
Console.WriteLine("│   • Write-heavy workloads (fewer rotations)                │");
Console.WriteLine("│   • Used in SortedSet<T>, SortedDictionary<K,V>            │");
Console.WriteLine("├────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use B-TREE / B+ TREE when:                                 │");
Console.WriteLine("│   • Database indexes (minimizes disk I/O)                  │");
Console.WriteLine("│   • File system directories                                │");
Console.WriteLine("│   • Large datasets on disk                                 │");
Console.WriteLine("└────────────────────────────────────────────────────────────┘");
```

---

## 7. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DataStructures"
dotnet run
```

---

## 8. Architect's Cheat Sheet

### Time Complexity Comparison

| Operation | BST Average | BST Worst | AVL | Red-Black |
|-----------|-------------|-----------|-----|-----------|
| Search | O(log n) | O(n) | O(log n) | O(log n) |
| Insert | O(log n) | O(n) | O(log n) | O(log n) |
| Delete | O(log n) | O(n) | O(log n) | O(log n) |
| Space | O(n) | O(n) | O(n) | O(n) |

### Traversal Order Summary

```
Tree:      1
          / \
         2   3
        / \
       4   5

Pre-Order  (NLR): 1, 2, 4, 5, 3  → Copy tree, serialize
In-Order   (LNR): 4, 2, 5, 1, 3  → Sorted order (BST)
Post-Order (LRN): 4, 5, 2, 3, 1  → Delete tree, postfix
Level-Order:      1, 2, 3, 4, 5  → BFS, shortest path
```

### When to Use C# Built-in Collections

```csharp
// SortedSet<T> - Uses Red-Black Tree internally
SortedSet<int> sortedSet = new() { 5, 2, 8, 1, 9 };
// Automatically sorted: 1, 2, 5, 8, 9

// SortedDictionary<K,V> - Uses Red-Black Tree
SortedDictionary<string, int> sortedDict = new()
{
    ["Charlie"] = 3,
    ["Alice"] = 1,
    ["Bob"] = 2
};
// Keys sorted: Alice, Bob, Charlie

// SortedList<K,V> - Uses sorted array (not tree)
// Better for small collections, binary search
```

---

## 9. Common Interview Questions

### Q1: Validate if a tree is a BST

```csharp
// Pass min/max bounds down recursively
bool IsValidBST(TreeNode<int>? node, int? min, int? max)
{
    if (node is null) return true;
    if (min.HasValue && node.Value <= min.Value) return false;
    if (max.HasValue && node.Value >= max.Value) return false;
    return IsValidBST(node.Left, min, node.Value) &&
           IsValidBST(node.Right, node.Value, max);
}
```

### Q2: Find Lowest Common Ancestor (LCA)

```csharp
TreeNode<int>? LCA(TreeNode<int>? root, int p, int q)
{
    if (root is null) return null;
    
    // Both on left
    if (p < root.Value && q < root.Value)
        return LCA(root.Left, p, q);
    
    // Both on right
    if (p > root.Value && q > root.Value)
        return LCA(root.Right, p, q);
    
    // Split point = LCA
    return root;
}
```

### Q3: Convert Sorted Array to Balanced BST

```csharp
TreeNode<int>? SortedArrayToBST(int[] nums, int left, int right)
{
    if (left > right) return null;
    
    int mid = left + (right - left) / 2;
    var node = new TreeNode<int>(nums[mid]);
    node.Left = SortedArrayToBST(nums, left, mid - 1);
    node.Right = SortedArrayToBST(nums, mid + 1, right);
    return node;
}
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Binary Tree** | Hierarchical structure, max 2 children per node |
| **Traversals** | Pre/In/Post-Order (DFS), Level-Order (BFS) |
| **BST** | Left < Root < Right, O(log n) average |
| **BST Weakness** | Degrades to O(n) with sorted input |
| **AVL Tree** | Self-balancing, guaranteed O(log n) |
| **Rotations** | LL→Right, RR→Left, LR→Left-Right, RL→Right-Left |
| **C# Built-ins** | SortedSet, SortedDictionary use Red-Black trees |

---

**Next Step**: Move to **Graphs** when ready!
