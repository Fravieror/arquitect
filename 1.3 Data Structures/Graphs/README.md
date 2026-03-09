# Graphs in C#

## Overview

Graphs are one of the **most versatile data structures** in computer science. As an architect, you'll encounter graphs in social networks, routing algorithms (Dijkstra, A*, Bellman-Ford), dependency resolution, recommendation engines, network topology, workflow systems, and countless real-world applications.

---

## 1. Graph Terminology

```
    [A] -------- [B]
     |  \         |
     |   \        |
     |    \       |
    [C] ------- [D]
     |
    [E]
```

| Term | Definition |
|------|------------|
| **Vertex (Node)** | A point in the graph (A, B, C, D, E) |
| **Edge** | Connection between two vertices |
| **Adjacent** | Two vertices connected by an edge |
| **Degree** | Number of edges connected to a vertex |
| **Path** | Sequence of vertices connected by edges |
| **Cycle** | Path that starts and ends at the same vertex |
| **Connected** | Path exists between every pair of vertices |
| **Weight** | Value/cost assigned to an edge |

---

## 2. Types of Graphs

| Type | Description | Example |
|------|-------------|---------|
| **Undirected** | Edges have no direction | Social network friendships |
| **Directed (Digraph)** | Edges have direction (A→B) | Twitter followers, dependencies |
| **Weighted** | Edges have costs/weights | Road networks, flight routes |
| **Unweighted** | All edges have equal weight | Simple connections |
| **Cyclic** | Contains at least one cycle | Circular dependencies |
| **Acyclic** | No cycles (DAG = Directed Acyclic Graph) | Task scheduling, package dependencies |

can you modify the above table to be in plain english and more concise?

| Type | Description | Example |
|------|-------------|---------|
| **Undirected** | Edges go both ways | Facebook friends |
| **Directed** | Edges go one way | Twitter followers |
| **Weighted** | Edges have costs | Road distances |
| **Unweighted** | All edges are equal | Simple connections |
| **Cyclic** | Has at least one cycle | Circular dependencies |
| **Acyclic** | No cycles | Task scheduling |
---

## 3. Graph Representations

### Adjacency List (Most Common)

```
A: [B, C, D]
B: [A, D]
C: [A, D, E]
D: [A, B, C]
E: [C]
```

**Pros**: Space efficient O(V + E), fast iteration over neighbors
**Cons**: O(V) to check if edge exists

### Adjacency Matrix

```
    A  B  C  D  E
A [ 0  1  1  1  0 ]
B [ 1  0  0  1  0 ]
C [ 1  0  0  1  1 ]
D [ 1  1  1  0  0 ]
E [ 0  0  1  0  0 ]
```

**Pros**: O(1) edge lookup
**Cons**: O(V²) space, wasteful for sparse graphs

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

### Exercise 1: Graph Implementation (Adjacency List)

Create a file `Graph.cs` and type the following:

```csharp
namespace DataStructures;

/// <summary>
/// Generic Graph using Adjacency List representation
/// ARCHITECT NOTE: Adjacency list is preferred for most real-world scenarios
/// </summary>
public class Graph<T> where T : notnull
{
    private readonly Dictionary<T, HashSet<T>> _adjacencyList = new();
    // is HashSet<T> here the number of adjacent vertices? Yes, it stores the neighbors of each vertex.

    // why is not colled something like vertexList? Because it's an adjacency list, not just a list of vertices. It maps each vertex to its neighbors.
    private readonly bool _isDirected;
    // isDirected allows us to use the same class for both directed and undirected graphs, which is more flexible.

    public Graph(bool isDirected = false)
    {
        _isDirected = isDirected;
    }

    public int VertexCount => _adjacencyList.Count;

    // is this to store the number of edges(conection between vertices)? Yes, it calculates the total number of edges by summing the counts of neighbors for each vertex. For undirected graphs, it divides by 2 to avoid double counting.

    // it means this will count 1 for the two edges A-B and B-A in an undirected graph, but for a directed graph it will count both A→B and B→A as separate edges.
    public int EdgeCount
    {
        get
        {
            int count = _adjacencyList.Values.Sum(neighbors => neighbors.Count);
            return _isDirected ? count : count / 2;
        }
    }

    public IEnumerable<T> Vertices => _adjacencyList.Keys;

    // Add a vertex
    public void AddVertex(T vertex)
    {
        if (!_adjacencyList.ContainsKey(vertex))
        {
            _adjacencyList[vertex] = new HashSet<T>();
        }
    }

    // Add an edge
    public void AddEdge(T from, T to)
    {
        AddVertex(from);
        AddVertex(to);

        _adjacencyList[from].Add(to);

        if (!_isDirected)
        {
            _adjacencyList[to].Add(from);
        }
    }

    // Remove an edge
    public bool RemoveEdge(T from, T to)
    {
        bool removed = false;

        if (_adjacencyList.TryGetValue(from, out var fromNeighbors))
        {
            removed = fromNeighbors.Remove(to);
        }

        if (!_isDirected && _adjacencyList.TryGetValue(to, out var toNeighbors))
        {
            toNeighbors.Remove(from);
        }

        return removed;
    }

    // Remove a vertex and all its edges
    public bool RemoveVertex(T vertex)
    {
        if (!_adjacencyList.Remove(vertex)) // is .Remove() and out of thebox method to remove the vertex from the adjacency list? Yes, it removes the vertex and its associated edges from the graph. If the vertex doesn't exist, it returns false.
        
        // is this a default method for Dictionaries? Yes, Dictionary<TKey, TValue>.Remove(TKey key) is a built-in method that removes the element with the specified key from the dictionary and returns true if the element was successfully removed; otherwise, false.
        
        // what can cause the Remove method to return false? It can return false if the vertex does not exist in the graph, meaning there is no key in the adjacency list for that vertex to remove.
            return false;

        // Remove all edges pointing to this vertex
        foreach (var neighbors in _adjacencyList.Values)
        {
            neighbors.Remove(vertex);
        }

        return true;
    }

    // Check if edge exists
    public bool HasEdge(T from, T to)
    {
        return _adjacencyList.TryGetValue(from, out var neighbors) &&
               neighbors.Contains(to);
    }

    // Check if vertex exists
    public bool HasVertex(T vertex)
    {
        return _adjacencyList.ContainsKey(vertex);
    }

    // Get neighbors of a vertex
    public IEnumerable<T> GetNeighbors(T vertex)
    {
        return _adjacencyList.TryGetValue(vertex, out var neighbors)
            ? neighbors
            : Enumerable.Empty<T>();
    }

    // Get degree of a vertex
    public int GetDegree(T vertex)
    {
        return _adjacencyList.TryGetValue(vertex, out var neighbors)
            ? neighbors.Count
            : 0;
    }

    // Print the graph
    public void Print()
    {
        Console.WriteLine(_isDirected ? "Directed Graph:" : "Undirected Graph:");
        foreach (var (vertex, neighbors) in _adjacencyList)
        {
            string arrow = _isDirected ? " → " : " ↔ ";
            Console.WriteLine($"  {vertex}:{arrow}[{string.Join(", ", neighbors)}]");
        }
    }
}
```

---

### Exercise 2: Weighted Graph

Create `WeightedGraph.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// Weighted Graph for algorithms like Dijkstra, Prim, Kruskal
/// ARCHITECT INSIGHT: Weighted graphs are essential for modeling real-world problems where connections have costs, distances, or capacities. They enable powerful algorithms for optimization and pathfinding.
/// whay does it mean weighted in this context? It means that each edge in the graph has an associated value (weight) that represents the cost, distance, or capacity of that connection. This allows us to model more complex scenarios where not all connections are equal, such as road networks with different distances or social networks with varying strengths of relationships.
/// 
/// is a road network like a payment you have to make to travel from one city to another? Yes, in a road network, the weight of an edge could represent the distance between two cities, the time it takes to travel, or even the toll cost. This allows us to use algorithms like Dijkstra's to find the shortest path based on these weights.
/// Is it like a peaje in Colombia? Yes, a "peaje" (toll) in Colombia is an example of a weight in a graph. If you're modeling a road network, the toll cost for traveling on a particular road could be represented as the weight of the edge connecting two cities. This way, when calculating the best route, you can consider not just the distance but also the cost of tolls along the way.
/// </summary>
public class WeightedGraph<T> where T : notnull
{
    private readonly Dictionary<T, List<(T Neighbor, double Weight)>> _adjacencyList = new();
    private readonly bool _isDirected; //does it mean it is bidirectional? Yes, if _isDirected is false, the graph is undirected (bidirectional), meaning that if there is an edge from A to B, there is also an edge from B to A with the same weight. If _isDirected is true, the graph is directed, and edges only go one way (A→B does not imply B→A).

    public WeightedGraph(bool isDirected = false)
    {
        _isDirected = isDirected;
    }

    public int VertexCount => _adjacencyList.Count;
    public IEnumerable<T> Vertices => _adjacencyList.Keys;

    public void AddVertex(T vertex)
    {
        if (!_adjacencyList.ContainsKey(vertex))
        {
            _adjacencyList[vertex] = new List<(T, double)>();
        }
    }

    public void AddEdge(T from, T to, double weight)
    {
        AddVertex(from);
        AddVertex(to);

        _adjacencyList[from].Add((to, weight));

        if (!_isDirected)
        {
            _adjacencyList[to].Add((from, weight));
        }
        // how would look like this method if is directed? If the graph is directed, we only add the edge from 'from' to 'to' and not the reverse. In that case, the AddEdge method would look like this:
        /*public void AddEdge(T from, T to, double weight)
        {
            AddVertex(from);
            AddVertex(to);

            _adjacencyList[from].Add((to, weight));
        }*/
    }

    public IEnumerable<(T Neighbor, double Weight)> GetNeighbors(T vertex)
    {
        return _adjacencyList.TryGetValue(vertex, out var neighbors)
            ? neighbors
            : Enumerable.Empty<(T, double)>();
    }

    public double? GetEdgeWeight(T from, T to)
    {
        if (_adjacencyList.TryGetValue(from, out var neighbors))
        {
            var edge = neighbors.FirstOrDefault(n => n.Neighbor.Equals(to));
            if (!edge.Equals(default))
                return edge.Weight;
        }
        return null;
    }

    // Get all edges (for algorithms like Kruskal)
    public IEnumerable<(T From, T To, double Weight)> GetAllEdges()
    {
        var seen = new HashSet<(T, T)>();

        foreach (var (vertex, neighbors) in _adjacencyList)
        {
            foreach (var (neighbor, weight) in neighbors)
            {
                var edge = _isDirected
                    ? (vertex, neighbor)
                    : (vertex.GetHashCode() < neighbor.GetHashCode()
                        ? (vertex, neighbor)
                        : (neighbor, vertex));

                if (seen.Add(edge))
                {
                    yield return (vertex, neighbor, weight);
                    // help me to see how the caller process a yield return? When a method uses 'yield return', it returns an IEnumerable<T> that produces values on demand. The caller can iterate over the results using a foreach loop or LINQ queries, and each time it requests the next item, the method continues execution from where it last yielded. This allows for efficient memory usage and the ability to generate sequences of data without needing to store them all in memory at once.

                    //does it have any amount of memory limitation? The memory usage of a method that uses 'yield return' is generally more efficient than methods that return a complete collection, as it generates items one at a time. However, the actual memory usage depends on how the caller consumes the IEnumerable. If the caller iterates through all items and stores them in a list, then the memory usage will grow with the number of items. If the caller processes items one at a time without storing them, then the memory usage will remain low regardless of the number of items generated.

                    // for instance to show in a frontend table, the best thing to handle it is render it as soon as it arraives, instead of waiting for the entire collection to be generated, right? Yes, if you're rendering data in a frontend table, it's often best to process and display each item as it arrives rather than waiting for the entire collection. This allows for a more responsive user experience, especially if the dataset is large or if generating the items takes time. By using 'yield return', you can start rendering rows in the table immediately as they are produced, which can improve perceived performance and reduce memory usage.

                    // in a web application, you could use server-sent events (SSE) or WebSockets to stream the data to the frontend as it is generated, allowing for real-time updates to the table without needing to wait for the entire dataset to be ready.

                    //has it some relation with lazy or eager loading? Yes, 'yield return' is related to lazy loading because it generates items on demand rather than all at once. This allows for more efficient memory usage and can improve performance when dealing with large datasets. Eager loading, on the other hand, would involve generating and storing all items in memory before they are accessed, which can lead to higher memory usage and slower performance if the dataset is large.
                }
            }
        }
    }

    public void Print()
    {
        Console.WriteLine(_isDirected ? "Weighted Directed Graph:" : "Weighted Undirected Graph:");
        foreach (var (vertex, neighbors) in _adjacencyList)
        {
            var edges = neighbors.Select(n => $"{n.Neighbor}({n.Weight})");
            Console.WriteLine($"  {vertex} → [{string.Join(", ", edges)}]");
        }
    }
}
```

---

### Exercise 3: Graph Traversals (BFS & DFS)

Create `GraphTraversals.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: BFS and DFS are the foundation of most graph algorithms.
/// Understanding when to use each is critical.
/// BFS (Breadth-First Search) is ideal for shortest path in unweighted graphs, level-order traversal, and finding connected components. 
/// DFS (Depth-First Search) is great for pathfinding, cycle detection, topological sorting, and exploring all possibilities (backtracking).
/// </summary>
public static class GraphTraversals
{
    public static void Run()
    {
        Console.WriteLine("=== GRAPH TRAVERSALS ===\n");

        // Create sample graph
        //     A --- B
        //     |     |
        //     C --- D --- E
        //     |
        //     F

        var graph = new Graph<string>();
        graph.AddEdge("A", "B");
        graph.AddEdge("A", "C");
        graph.AddEdge("B", "D");
        graph.AddEdge("C", "D");
        graph.AddEdge("C", "F");
        graph.AddEdge("D", "E");

        graph.Print();

        Console.WriteLine($"\nVertices: {graph.VertexCount}, Edges: {graph.EdgeCount}");

        // BFS - Level by level, finds shortest path (unweighted)
        Console.WriteLine("\n--- Breadth-First Search (BFS) ---");
        Console.WriteLine("Starting from A:");
        var bfsResult = BFS(graph, "A");
        Console.WriteLine($"  Order: {string.Join(" → ", bfsResult)}");

        // DFS - Goes deep first, good for paths and cycles
        Console.WriteLine("\n--- Depth-First Search (DFS) ---");
        Console.WriteLine("Starting from A (Recursive):");
        var dfsResult = DFSRecursive(graph, "A");
        Console.WriteLine($"  Order: {string.Join(" → ", dfsResult)}");

        Console.WriteLine("\nStarting from A (Iterative):");
        var dfsIterResult = DFSIterative(graph, "A");
        Console.WriteLine($"  Order: {string.Join(" → ", dfsIterResult)}");
    }

    // BFS - Uses Queue (FIFO)
    // what relation has BFS with Queue? BFS uses a Queue data structure to keep track of the vertices to visit next. The Queue ensures that vertices are processed in the order they were added, which allows BFS to explore the graph level by level. When a vertex is visited, all of its unvisited neighbors are added to the Queue, and the process continues until the Queue is empty.
    // Use case: Shortest path (unweighted), level-order traversal
    public static List<T> BFS<T>(Graph<T> graph, T start) where T : notnull
    {
        var visited = new HashSet<T>();
        // can this visited be replaced by peeking at the queue? No, the visited set is necessary to keep track of which vertices have already been processed. Peeking at the queue only shows the next vertex to be processed, but it does not provide information about all the vertices that have been visited so far. The visited set ensures that we do not process the same vertex multiple times, which is crucial for preventing infinite loops and ensuring correct traversal.
        var result = new List<T>();
        var queue = new Queue<T>();

        queue.Enqueue(start);
        visited.Add(start);

        while (queue.Count > 0)
        {
            var vertex = queue.Dequeue();
            result.Add(vertex);

            foreach (var neighbor in graph.GetNeighbors(vertex)) // is neighbor here another vertex adjacent to the current vertex? Yes, 'neighbor' refers to another vertex that is directly connected to the current vertex by an edge. In the context of BFS, we explore these neighboring vertices to continue traversing the graph.
            {
                if (visited.Add(neighbor)) // Add returns false if already present
                {
                    queue.Enqueue(neighbor);
                }
            }
        }

        return result;
    }
    // is not relation between BFS and recursion? BFS is typically implemented using an iterative approach with a Queue, while DFS is more naturally implemented using recursion. However, it is possible to implement BFS recursively, but it is less common and can be less efficient due to the overhead of recursive calls and the need to manage the queue manually. In general, BFS is best suited for an iterative implementation, while DFS lends itself well to recursion.

    // DFS Recursive - Uses call stack
    public static List<T> DFSRecursive<T>(Graph<T> graph, T start) where T : notnull
    {
        var visited = new HashSet<T>();
        var result = new List<T>();
        DFSHelper(graph, start, visited, result);
        return result;
    }

    private static void DFSHelper<T>(Graph<T> graph, T vertex, HashSet<T> visited, List<T> result)
        where T : notnull
    {
        visited.Add(vertex);
        result.Add(vertex);

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (!visited.Contains(neighbor))
            {
                DFSHelper(graph, neighbor, visited, result);
            }
        }
    }
    // is there any particular relation between depth traversal and recursion? Yes, depth-first traversal naturally lends itself to a recursive implementation because it explores as far down a branch as possible before backtracking. Each recursive call processes a vertex and then calls itself for one of its neighbors, effectively diving deeper into the graph. When it reaches a vertex with no unvisited neighbors, it backtracks to the previous vertex and continues exploring other branches. This recursive structure mirrors the depth-first nature of the traversal.

    // DFS Iterative - Uses explicit Stack (avoids stack overflow for deep graphs)
    public static List<T> DFSIterative<T>(Graph<T> graph, T start) where T : notnull
    {
        var visited = new HashSet<T>();
        var result = new List<T>();
        var stack = new Stack<T>();

        stack.Push(start);

        while (stack.Count > 0)
        {
            var vertex = stack.Pop();

            if (visited.Add(vertex))
            {
                result.Add(vertex);

                // Push neighbors in reverse order for consistent ordering
                foreach (var neighbor in graph.GetNeighbors(vertex).Reverse())
                {
                    if (!visited.Contains(neighbor))
                    {
                        stack.Push(neighbor);
                    }
                }
            }
        }

        return result;
    }
}
```

---

### Exercise 4: Shortest Path Algorithms

Create `ShortestPath.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Shortest path algorithms are essential for
/// routing, navigation, network optimization, and resource allocation.
/// </summary>
public static class ShortestPath
{
    public static void Run()
    {
        Console.WriteLine("\n=== SHORTEST PATH ALGORITHMS ===\n");

        // Unweighted graph - BFS shortest path
        Console.WriteLine("--- BFS Shortest Path (Unweighted) ---");
        var unweighted = new Graph<string>();
        unweighted.AddEdge("A", "B");
        unweighted.AddEdge("A", "C");
        unweighted.AddEdge("B", "D");
        unweighted.AddEdge("C", "D");
        unweighted.AddEdge("D", "E");
        unweighted.AddEdge("B", "E");

        var (path, distance) = BFSShortestPath(unweighted, "A", "E");
        Console.WriteLine($"Path from A to E: {string.Join(" → ", path)}");
        Console.WriteLine($"Distance: {distance} edges");

        // Weighted graph - Dijkstra
        Console.WriteLine("\n--- Dijkstra's Algorithm (Weighted) ---");

        //       B --- 1 --- D
        //      /|           |\
        //     4 |           | 3
        //    /  2           1  \
        //   A   |           |   F
        //    \  |           |  /
        //     2 |           | 1
        //      \|           |/
        //       C --- 3 --- E

        var weighted = new WeightedGraph<string>();
        weighted.AddEdge("A", "B", 4);
        weighted.AddEdge("A", "C", 2);
        weighted.AddEdge("B", "C", 2);
        weighted.AddEdge("B", "D", 1);
        weighted.AddEdge("C", "E", 3);
        weighted.AddEdge("D", "E", 1);
        weighted.AddEdge("D", "F", 3);
        weighted.AddEdge("E", "F", 1);

        weighted.Print();

        var dijkstraResult = Dijkstra(weighted, "A");
        Console.WriteLine($"\nShortest distances from A:");
        foreach (var (vertex, dist) in dijkstraResult.Distances.OrderBy(x => x.Key))
        {
            var pathStr = ReconstructPath(dijkstraResult.Previous, "A", vertex);
            Console.WriteLine($"  {vertex}: distance={dist}, path={pathStr}");
        }
    }

    // BFS finds shortest path in UNWEIGHTED graphs
    public static (List<T> Path, int Distance) BFSShortestPath<T>(
        Graph<T> graph, T start, T end) where T : notnull
    {
        var visited = new HashSet<T> { start };
        var queue = new Queue<T>();
        var parent = new Dictionary<T, T>();

        queue.Enqueue(start);

        while (queue.Count > 0)
        {
            var vertex = queue.Dequeue();

            if (vertex.Equals(end))
            {
                // Reconstruct path
                var path = new List<T>();
                var current = end;
                while (!current.Equals(start))
                {
                    path.Add(current);
                    current = parent[current];
                }
                path.Add(start);
                path.Reverse();
                return (path, path.Count - 1);
            }

            foreach (var neighbor in graph.GetNeighbors(vertex))
            {
                if (visited.Add(neighbor))
                {
                    parent[neighbor] = vertex;
                    queue.Enqueue(neighbor);
                }
            }
        }

        return (new List<T>(), -1); // No path found
    }

    // Dijkstra's Algorithm for WEIGHTED graphs (non-negative weights)
    public static (Dictionary<T, double> Distances, Dictionary<T, T> Previous) Dijkstra<T>(
        WeightedGraph<T> graph, T start) where T : notnull
    {
        var distances = new Dictionary<T, double>();
        var previous = new Dictionary<T, T>();
        var visited = new HashSet<T>();

        // Initialize distances
        foreach (var vertex in graph.Vertices)
        {
            distances[vertex] = double.MaxValue;
        }
        distances[start] = 0;

        // Priority queue (min-heap by distance)
        var pq = new PriorityQueue<T, double>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0)
        {
            var current = pq.Dequeue();

            if (!visited.Add(current))
                continue;

            foreach (var (neighbor, weight) in graph.GetNeighbors(current))
            {
                if (visited.Contains(neighbor))
                    continue;

                double newDist = distances[current] + weight;

                if (newDist < distances[neighbor])
                {
                    distances[neighbor] = newDist;
                    previous[neighbor] = current;
                    pq.Enqueue(neighbor, newDist);
                }
            }
        }

        return (distances, previous);
    }

    private static string ReconstructPath<T>(Dictionary<T, T> previous, T start, T end)
        where T : notnull
    {
        var path = new List<T>();
        var current = end;

        while (!current.Equals(start))
        {
            path.Add(current);
            if (!previous.TryGetValue(current, out current!))
            {
                return "No path";
            }
        }
        path.Add(start);
        path.Reverse();
        return string.Join(" → ", path);
    }
}
```

---

### Exercise 5: Cycle Detection

Create `CycleDetection.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Cycle detection is critical for:
/// - Dependency resolution (deadlock detection)
/// - Task scheduling (detecting circular dependencies)
/// - Resource allocation (detecting deadlocks)
/// </summary>
public static class CycleDetection
{
    public static void Run()
    {
        Console.WriteLine("\n=== CYCLE DETECTION ===\n");

        // Undirected graph with cycle
        Console.WriteLine("--- Undirected Graph ---");
        var undirected = new Graph<string>();
        undirected.AddEdge("A", "B");
        undirected.AddEdge("B", "C");
        undirected.AddEdge("C", "A"); // Creates cycle A-B-C-A

        Console.WriteLine($"Has cycle: {HasCycleUndirected(undirected)}");

        // Undirected graph without cycle
        var noCycle = new Graph<string>();
        noCycle.AddEdge("A", "B");
        noCycle.AddEdge("B", "C");
        noCycle.AddEdge("C", "D");

        Console.WriteLine($"Tree (no cycle): {HasCycleUndirected(noCycle)}");

        // Directed graph with cycle
        Console.WriteLine("\n--- Directed Graph ---");
        var directed = new Graph<string>(isDirected: true);
        directed.AddEdge("A", "B");
        directed.AddEdge("B", "C");
        directed.AddEdge("C", "D");
        directed.AddEdge("D", "B"); // Creates cycle B→C→D→B

        Console.WriteLine($"Has cycle: {HasCycleDirected(directed)}");

        // DAG (Directed Acyclic Graph)
        var dag = new Graph<string>(isDirected: true);
        dag.AddEdge("A", "B");
        dag.AddEdge("A", "C");
        dag.AddEdge("B", "D");
        dag.AddEdge("C", "D");

        Console.WriteLine($"DAG (no cycle): {HasCycleDirected(dag)}");
    }

    // Cycle detection in UNDIRECTED graph using DFS
    public static bool HasCycleUndirected<T>(Graph<T> graph) where T : notnull
    {
        var visited = new HashSet<T>();

        foreach (var vertex in graph.Vertices)
        {
            if (!visited.Contains(vertex))
            {
                if (HasCycleUndirectedDFS(graph, vertex, visited, default!))
                    return true;
            }
        }

        return false;
    }

    private static bool HasCycleUndirectedDFS<T>(
        Graph<T> graph, T vertex, HashSet<T> visited, T parent) where T : notnull
    {
        visited.Add(vertex);

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (!visited.Contains(neighbor))
            {
                if (HasCycleUndirectedDFS(graph, neighbor, visited, vertex))
                    return true;
            }
            else if (!neighbor.Equals(parent))
            {
                // Found visited vertex that's not parent = cycle!
                return true;
            }
        }

        return false;
    }

    // Cycle detection in DIRECTED graph using DFS with coloring
    // White (0) = unvisited, Gray (1) = in current path, Black (2) = done
    public static bool HasCycleDirected<T>(Graph<T> graph) where T : notnull
    {
        var color = new Dictionary<T, int>(); // 0=white, 1=gray, 2=black

        foreach (var vertex in graph.Vertices)
        {
            color[vertex] = 0; // Initialize all as white
        }

        foreach (var vertex in graph.Vertices)
        {
            if (color[vertex] == 0) // White
            {
                if (HasCycleDirectedDFS(graph, vertex, color))
                    return true;
            }
        }

        return false;
    }

    private static bool HasCycleDirectedDFS<T>(
        Graph<T> graph, T vertex, Dictionary<T, int> color) where T : notnull
    {
        color[vertex] = 1; // Gray - currently being processed

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (color[neighbor] == 1) // Gray = back edge = cycle!
                return true;

            if (color[neighbor] == 0) // White = unvisited
            {
                if (HasCycleDirectedDFS(graph, neighbor, color))
                    return true;
            }
        }

        color[vertex] = 2; // Black - done processing
        return false;
    }
}
```

---

### Exercise 6: Topological Sort

Create `TopologicalSort.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Topological Sort is essential for:
/// - Build systems (compiling dependencies in order)
/// - Task scheduling (prerequisites before dependent tasks)
/// - Package managers (dependency resolution)
/// - Course prerequisites (academic planning)
/// </summary>
public static class TopologicalSort
{
    public static void Run()
    {
        Console.WriteLine("\n=== TOPOLOGICAL SORT ===\n");

        // Course prerequisites example
        // To take D, you need B and C
        // To take B, you need A
        // To take C, you need A

        var courses = new Graph<string>(isDirected: true);
        courses.AddEdge("A", "B");  // A must come before B
        courses.AddEdge("A", "C");  // A must come before C
        courses.AddEdge("B", "D");  // B must come before D
        courses.AddEdge("C", "D");  // C must come before D
        courses.AddEdge("D", "E");  // D must come before E
        courses.AddEdge("C", "E");  // C must come before E

        Console.WriteLine("Course Dependencies:");
        courses.Print();

        // DFS-based topological sort
        Console.WriteLine("\n--- DFS-based Topological Sort ---");
        var dfsSorted = TopologicalSortDFS(courses);
        Console.WriteLine($"Order: {string.Join(" → ", dfsSorted)}");

        // Kahn's Algorithm (BFS-based)
        Console.WriteLine("\n--- Kahn's Algorithm (BFS-based) ---");
        var kahnResult = TopologicalSortKahn(courses);
        if (kahnResult.HasCycle)
        {
            Console.WriteLine("Graph has a cycle! Cannot sort.");
        }
        else
        {
            Console.WriteLine($"Order: {string.Join(" → ", kahnResult.Sorted)}");
        }

        // Build system example
        Console.WriteLine("\n--- Build System Example ---");
        var buildDeps = new Graph<string>(isDirected: true);
        buildDeps.AddEdge("utils", "core");
        buildDeps.AddEdge("core", "api");
        buildDeps.AddEdge("core", "web");
        buildDeps.AddEdge("api", "app");
        buildDeps.AddEdge("web", "app");
        buildDeps.AddEdge("database", "api");

        var buildOrder = TopologicalSortDFS(buildDeps);
        Console.WriteLine($"Build order: {string.Join(" → ", buildOrder)}");
    }

    // DFS-based Topological Sort
    public static List<T> TopologicalSortDFS<T>(Graph<T> graph) where T : notnull
    {
        var visited = new HashSet<T>();
        var result = new Stack<T>(); // Use stack to reverse order

        foreach (var vertex in graph.Vertices)
        {
            if (!visited.Contains(vertex))
            {
                TopSortDFSHelper(graph, vertex, visited, result);
            }
        }

        return result.ToList();
    }

    private static void TopSortDFSHelper<T>(
        Graph<T> graph, T vertex, HashSet<T> visited, Stack<T> result) where T : notnull
    {
        visited.Add(vertex);

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (!visited.Contains(neighbor))
            {
                TopSortDFSHelper(graph, neighbor, visited, result);
            }
        }

        result.Push(vertex); // Add after processing all descendants
    }

    // Kahn's Algorithm (BFS-based) - Also detects cycles
    public static (List<T> Sorted, bool HasCycle) TopologicalSortKahn<T>(Graph<T> graph)
        where T : notnull
    {
        // Calculate in-degrees
        var inDegree = new Dictionary<T, int>();
        foreach (var vertex in graph.Vertices)
        {
            inDegree[vertex] = 0;
        }

        foreach (var vertex in graph.Vertices)
        {
            foreach (var neighbor in graph.GetNeighbors(vertex))
            {
                inDegree[neighbor]++;
            }
        }

        // Start with vertices that have no prerequisites
        var queue = new Queue<T>();
        foreach (var (vertex, degree) in inDegree)
        {
            if (degree == 0)
            {
                queue.Enqueue(vertex);
            }
        }

        var result = new List<T>();

        while (queue.Count > 0)
        {
            var vertex = queue.Dequeue();
            result.Add(vertex);

            foreach (var neighbor in graph.GetNeighbors(vertex))
            {
                inDegree[neighbor]--;

                if (inDegree[neighbor] == 0)
                {
                    queue.Enqueue(neighbor);
                }
            }
        }

        // If we couldn't process all vertices, there's a cycle
        bool hasCycle = result.Count != graph.VertexCount;
        return (result, hasCycle);
    }
}
```

---

### Exercise 7: Connected Components

Create `ConnectedComponents.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: Finding connected components helps identify:
/// - Clusters in social networks
/// - Independent subsystems
/// - Network partitions
/// - Island counting problems
/// </summary>
public static class ConnectedComponents
{
    public static void Run()
    {
        Console.WriteLine("\n=== CONNECTED COMPONENTS ===\n");

        // Graph with multiple components
        //   Component 1: A-B-C
        //   Component 2: D-E
        //   Component 3: F

        var graph = new Graph<string>();
        graph.AddEdge("A", "B");
        graph.AddEdge("B", "C");
        graph.AddEdge("D", "E");
        graph.AddVertex("F"); // Isolated vertex

        Console.WriteLine("Graph structure:");
        graph.Print();

        var components = FindConnectedComponents(graph);
        Console.WriteLine($"\nNumber of connected components: {components.Count}");

        for (int i = 0; i < components.Count; i++)
        {
            Console.WriteLine($"Component {i + 1}: {{{string.Join(", ", components[i])}}}");
        }

        // Strongly Connected Components (for directed graphs)
        Console.WriteLine("\n--- Strongly Connected Components (Directed) ---");
        var directed = new Graph<string>(isDirected: true);
        directed.AddEdge("A", "B");
        directed.AddEdge("B", "C");
        directed.AddEdge("C", "A"); // Cycle A→B→C→A
        directed.AddEdge("C", "D");
        directed.AddEdge("D", "E");
        directed.AddEdge("E", "D"); // Cycle D→E→D

        directed.Print();

        var sccs = FindSCCKosaraju(directed);
        Console.WriteLine($"\nNumber of SCCs: {sccs.Count}");
        for (int i = 0; i < sccs.Count; i++)
        {
            Console.WriteLine($"SCC {i + 1}: {{{string.Join(", ", sccs[i])}}}");
        }
    }

    // Find connected components in UNDIRECTED graph
    public static List<List<T>> FindConnectedComponents<T>(Graph<T> graph) where T : notnull
    {
        var visited = new HashSet<T>();
        var components = new List<List<T>>();

        foreach (var vertex in graph.Vertices)
        {
            if (!visited.Contains(vertex))
            {
                var component = new List<T>();
                DFS(graph, vertex, visited, component);
                components.Add(component);
            }
        }

        return components;
    }

    private static void DFS<T>(Graph<T> graph, T vertex, HashSet<T> visited, List<T> component)
        where T : notnull
    {
        visited.Add(vertex);
        component.Add(vertex);

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (!visited.Contains(neighbor))
            {
                DFS(graph, neighbor, visited, component);
            }
        }
    }

    // Kosaraju's Algorithm for Strongly Connected Components (directed graphs)
    public static List<List<T>> FindSCCKosaraju<T>(Graph<T> graph) where T : notnull
    {
        // Step 1: Get finish times using DFS
        var visited = new HashSet<T>();
        var finishOrder = new Stack<T>();

        foreach (var vertex in graph.Vertices)
        {
            if (!visited.Contains(vertex))
            {
                FillOrder(graph, vertex, visited, finishOrder);
            }
        }

        // Step 2: Create transpose graph (reverse all edges)
        var transpose = CreateTranspose(graph);

        // Step 3: DFS on transpose in finish order
        visited.Clear();
        var sccs = new List<List<T>>();

        while (finishOrder.Count > 0)
        {
            var vertex = finishOrder.Pop();

            if (!visited.Contains(vertex))
            {
                var scc = new List<T>();
                DFS(transpose, vertex, visited, scc);
                sccs.Add(scc);
            }
        }

        return sccs;
    }

    private static void FillOrder<T>(Graph<T> graph, T vertex, HashSet<T> visited, Stack<T> stack)
        where T : notnull
    {
        visited.Add(vertex);

        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (!visited.Contains(neighbor))
            {
                FillOrder(graph, neighbor, visited, stack);
            }
        }

        stack.Push(vertex);
    }

    private static Graph<T> CreateTranspose<T>(Graph<T> graph) where T : notnull
    {
        var transpose = new Graph<T>(isDirected: true);

        foreach (var vertex in graph.Vertices)
        {
            transpose.AddVertex(vertex);
        }

        foreach (var vertex in graph.Vertices)
        {
            foreach (var neighbor in graph.GetNeighbors(vertex))
            {
                transpose.AddEdge(neighbor, vertex); // Reverse the edge
            }
        }

        return transpose;
    }
}
```

---

### Exercise 8: Minimum Spanning Tree (MST)

Create `MinimumSpanningTree.cs`:

```csharp
namespace DataStructures;

/// <summary>
/// ARCHITECT INSIGHT: MST algorithms are used for:
/// - Network design (minimum cable to connect all nodes)
/// - Cluster analysis
/// - Image segmentation
/// - Approximation algorithms for NP-hard problems
/// </summary>
public static class MinimumSpanningTree
{
    public static void Run()
    {
        Console.WriteLine("\n=== MINIMUM SPANNING TREE ===\n");

        //       B --- 4 --- D
        //      /|           |\
        //     2 |           | 5
        //    /  3           1  \
        //   A   |           |   F
        //    \  |           |  /
        //     3 |           | 2
        //      \|           |/
        //       C --- 2 --- E

        var graph = new WeightedGraph<string>();
        graph.AddEdge("A", "B", 2);
        graph.AddEdge("A", "C", 3);
        graph.AddEdge("B", "C", 3);
        graph.AddEdge("B", "D", 4);
        graph.AddEdge("C", "E", 2);
        graph.AddEdge("D", "E", 1);
        graph.AddEdge("D", "F", 5);
        graph.AddEdge("E", "F", 2);

        Console.WriteLine("Original Graph:");
        graph.Print();

        // Prim's Algorithm
        Console.WriteLine("\n--- Prim's Algorithm ---");
        var primMST = PrimMST(graph, "A");
        Console.WriteLine($"MST Edges:");
        double primTotal = 0;
        foreach (var (from, to, weight) in primMST)
        {
            Console.WriteLine($"  {from} -- {to} : {weight}");
            primTotal += weight;
        }
        Console.WriteLine($"Total weight: {primTotal}");

        // Kruskal's Algorithm
        Console.WriteLine("\n--- Kruskal's Algorithm ---");
        var kruskalMST = KruskalMST(graph);
        Console.WriteLine($"MST Edges:");
        double kruskalTotal = 0;
        foreach (var (from, to, weight) in kruskalMST)
        {
            Console.WriteLine($"  {from} -- {to} : {weight}");
            kruskalTotal += weight;
        }
        Console.WriteLine($"Total weight: {kruskalTotal}");
    }

    // Prim's Algorithm - Greedy, grows MST from starting vertex
    public static List<(T From, T To, double Weight)> PrimMST<T>(
        WeightedGraph<T> graph, T start) where T : notnull
    {
        var mst = new List<(T, T, double)>();
        var visited = new HashSet<T> { start };
        var pq = new PriorityQueue<(T From, T To), double>();

        // Add all edges from start
        foreach (var (neighbor, weight) in graph.GetNeighbors(start))
        {
            pq.Enqueue((start, neighbor), weight);
        }

        while (pq.Count > 0 && visited.Count < graph.VertexCount)
        {
            var (from, to) = pq.Dequeue();

            if (visited.Contains(to))
                continue;

            // Add edge to MST
            double edgeWeight = graph.GetEdgeWeight(from, to) ?? 0;
            mst.Add((from, to, edgeWeight));
            visited.Add(to);

            // Add all edges from new vertex
            foreach (var (neighbor, weight) in graph.GetNeighbors(to))
            {
                if (!visited.Contains(neighbor))
                {
                    pq.Enqueue((to, neighbor), weight);
                }
            }
        }

        return mst;
    }

    // Kruskal's Algorithm - Sort edges, use Union-Find
    public static List<(T From, T To, double Weight)> KruskalMST<T>(
        WeightedGraph<T> graph) where T : notnull
    {
        var mst = new List<(T, T, double)>();
        var unionFind = new UnionFind<T>(graph.Vertices);

        // Get all edges sorted by weight
        var edges = graph.GetAllEdges()
            .OrderBy(e => e.Weight)
            .ToList();

        foreach (var (from, to, weight) in edges)
        {
            // Only add edge if it doesn't create a cycle
            if (unionFind.Find(from).Equals(unionFind.Find(to)))
                continue;

            mst.Add((from, to, weight));
            unionFind.Union(from, to);

            // MST complete when we have V-1 edges
            if (mst.Count == graph.VertexCount - 1)
                break;
        }

        return mst;
    }
}

// Union-Find (Disjoint Set) data structure for Kruskal's
public class UnionFind<T> where T : notnull
{
    private readonly Dictionary<T, T> _parent = new();
    private readonly Dictionary<T, int> _rank = new();

    public UnionFind(IEnumerable<T> elements)
    {
        foreach (var element in elements)
        {
            _parent[element] = element;
            _rank[element] = 0;
        }
    }

    // Find with path compression
    public T Find(T x)
    {
        if (!_parent[x].Equals(x))
        {
            _parent[x] = Find(_parent[x]); // Path compression
        }
        return _parent[x];
    }

    // Union by rank
    public void Union(T x, T y)
    {
        var rootX = Find(x);
        var rootY = Find(y);

        if (rootX.Equals(rootY))
            return;

        // Union by rank
        if (_rank[rootX] < _rank[rootY])
        {
            _parent[rootX] = rootY;
        }
        else if (_rank[rootX] > _rank[rootY])
        {
            _parent[rootY] = rootX;
        }
        else
        {
            _parent[rootY] = rootX;
            _rank[rootX]++;
        }
    }
}
```

---

## 4. Update Program.cs

Replace the contents of `Program.cs`:

```csharp
using DataStructures;

Console.WriteLine("╔═══════════════════════════════════════════════════════╗");
Console.WriteLine("║         GRAPHS - ARCHITECT TRAINING                   ║");
Console.WriteLine("╚═══════════════════════════════════════════════════════╝");

GraphTraversals.Run();
ShortestPath.Run();
CycleDetection.Run();
TopologicalSort.Run();
ConnectedComponents.Run();
MinimumSpanningTree.Run();

Console.WriteLine("\n\n=== ARCHITECT DECISION GUIDE ===");
Console.WriteLine("┌─────────────────────────────────────────────────────────────┐");
Console.WriteLine("│ Use BFS when:                                               │");
Console.WriteLine("│   • Finding shortest path (unweighted)                      │");
Console.WriteLine("│   • Level-order traversal needed                            │");
Console.WriteLine("│   • Finding nearest neighbors                               │");
Console.WriteLine("├─────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use DFS when:                                               │");
Console.WriteLine("│   • Finding any path (not necessarily shortest)             │");
Console.WriteLine("│   • Cycle detection                                         │");
Console.WriteLine("│   • Topological sorting                                     │");
Console.WriteLine("│   • Connected components                                    │");
Console.WriteLine("├─────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use Dijkstra when:                                          │");
Console.WriteLine("│   • Shortest path in weighted graph                         │");
Console.WriteLine("│   • All edge weights are non-negative                       │");
Console.WriteLine("│   • Single-source shortest path                             │");
Console.WriteLine("├─────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use Bellman-Ford when:                                      │");
Console.WriteLine("│   • Graph may have negative edge weights                    │");
Console.WriteLine("│   • Need to detect negative cycles                          │");
Console.WriteLine("├─────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use Topological Sort when:                                  │");
Console.WriteLine("│   • Task scheduling with dependencies                       │");
Console.WriteLine("│   • Build systems (compile order)                           │");
Console.WriteLine("│   • Course prerequisites                                    │");
Console.WriteLine("├─────────────────────────────────────────────────────────────┤");
Console.WriteLine("│ Use MST (Prim/Kruskal) when:                                │");
Console.WriteLine("│   • Connecting all nodes with minimum cost                  │");
Console.WriteLine("│   • Network design, cluster analysis                        │");
Console.WriteLine("└─────────────────────────────────────────────────────────────┘");
```

---

## 5. Run the Project

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\DataStructures"
dotnet run
```

---

## 6. Architect's Cheat Sheet

### Time Complexity

| Algorithm | Time Complexity | Space |
|-----------|-----------------|-------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra (PQ) | O((V + E) log V) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| Prim (PQ) | O((V + E) log V) | O(V) |
| Kruskal | O(E log E) | O(V) |
| Connected Components | O(V + E) | O(V) |

### Representation Comparison

| | Adjacency List | Adjacency Matrix |
|---|----------------|------------------|
| Space | O(V + E) | O(V²) |
| Add Edge | O(1) | O(1) |
| Remove Edge | O(E) | O(1) |
| Check Edge | O(degree) | O(1) |
| Iterate Neighbors | O(degree) | O(V) |
| Best for | Sparse graphs | Dense graphs |

### Algorithm Selection

```
                    SHORTEST PATH
                         │
           ┌─────────────┴─────────────┐
           │                           │
      Unweighted                   Weighted
           │                           │
          BFS              ┌───────────┴───────────┐
                           │                       │
                   Non-negative              May be negative
                    weights                    weights
                       │                           │
                   Dijkstra                  Bellman-Ford
```

---

## 7. Real-World Applications

| Domain | Graph Application |
|--------|-------------------|
| **Social Networks** | Friend recommendations, influence propagation |
| **Maps/Navigation** | Route finding, traffic optimization |
| **Dependency Management** | Package managers, build systems |
| **Network Routing** | Internet routing protocols, load balancing |
| **Recommendation Systems** | Product recommendations, content discovery |
| **Fraud Detection** | Transaction network analysis |
| **Knowledge Graphs** | Semantic search, question answering |
| **Compilers** | Control flow graphs, data flow analysis |

---

## 8. Common Interview Questions

### Q1: Find if path exists between two nodes

```csharp
bool HasPath<T>(Graph<T> graph, T start, T end) where T : notnull
{
    if (start.Equals(end)) return true;

    var visited = new HashSet<T>();
    var queue = new Queue<T>();
    queue.Enqueue(start);
    visited.Add(start);

    while (queue.Count > 0)
    {
        var vertex = queue.Dequeue();
        foreach (var neighbor in graph.GetNeighbors(vertex))
        {
            if (neighbor.Equals(end)) return true;
            if (visited.Add(neighbor))
                queue.Enqueue(neighbor);
        }
    }
    return false;
}
```

### Q2: Clone a graph

```csharp
Dictionary<Node, Node> CloneGraph(Node node)
{
    var clones = new Dictionary<Node, Node>();
    var queue = new Queue<Node>();
    
    clones[node] = new Node(node.Value);
    queue.Enqueue(node);
    
    while (queue.Count > 0)
    {
        var original = queue.Dequeue();
        foreach (var neighbor in original.Neighbors)
        {
            if (!clones.ContainsKey(neighbor))
            {
                clones[neighbor] = new Node(neighbor.Value);
                queue.Enqueue(neighbor);
            }
            clones[original].Neighbors.Add(clones[neighbor]);
        }
    }
    return clones;
}
```

### Q3: Number of islands (2D grid)

```csharp
int NumIslands(char[][] grid)
{
    int count = 0;
    for (int i = 0; i < grid.Length; i++)
    {
        for (int j = 0; j < grid[0].Length; j++)
        {
            if (grid[i][j] == '1')
            {
                SinkIsland(grid, i, j);
                count++;
            }
        }
    }
    return count;
}

void SinkIsland(char[][] grid, int i, int j)
{
    if (i < 0 || i >= grid.Length || j < 0 || j >= grid[0].Length)
        return;
    if (grid[i][j] == '0') return;
    
    grid[i][j] = '0'; // Mark as visited
    SinkIsland(grid, i + 1, j);
    SinkIsland(grid, i - 1, j);
    SinkIsland(grid, i, j + 1);
    SinkIsland(grid, i, j - 1);
}
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **Adjacency List** | Preferred for most applications, O(V+E) space |
| **BFS** | Level-order, shortest path (unweighted) |
| **DFS** | Depth-first, cycles, topological sort |
| **Dijkstra** | Shortest path (weighted, non-negative) |
| **Topological Sort** | DAG ordering, dependency resolution |
| **Union-Find** | Efficient connected components, MST |
| **Prim/Kruskal** | Minimum spanning tree |
| **SCC** | Strongly connected components (directed) |

---

**Next Step**: Move to **Heaps** when ready!
