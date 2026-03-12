# Object Pool Pattern in C#

## 🎯 TL;DR (30 seconds)

**Object Pool** = Reuse expensive objects instead of creating new ones.

```csharp
// ❌ SLOW: Create new connection every time
var conn = new DatabaseConnection(); // 50ms each!

// ✅ FAST: Borrow from pool, return when done
var conn = pool.Get();    // instant!
// ... use it ...
pool.Return(conn);        // back to pool
```

**Real-world uses**: Database connections, HTTP clients, threads, game objects.

---

## 📦 What You'll Build

| Exercise | What | Time |
|----------|------|------|
| 1 | Basic Pool | 5 min |
| 2 | .NET's ArrayPool | 3 min |
| 3 | .NET's ObjectPool | 5 min |
| 4 | Database Connection Pool | 7 min |
| 5 | HTTP Client Pool | 5 min |
| 6 | Game Object Pool | 5 min |

---

## 🚀 Quick Setup

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp"
dotnet new console -n ObjectPoolDemo
cd ObjectPoolDemo
dotnet add package Microsoft.Extensions.ObjectPool
```

---

## Exercise 1: Basic Object Pool (5 min)

> **Goal**: Understand the core concept

Create `BasicPool.cs`:

```csharp
namespace ObjectPoolDemo;

// ═══════════════════════════════════════════════════════════
// THE PROBLEM: Creating objects is expensive
// ═══════════════════════════════════════════════════════════

public class ExpensiveObject
{
    public Guid Id { get; } = Guid.NewGuid();
    
    public ExpensiveObject()
    {
        // Simulate expensive initialization
        Thread.Sleep(100); // 100ms to create!
        Console.WriteLine($"  💰 Created expensive object {Id}");
    }
    
    public void DoWork() => Console.WriteLine($"  ⚙️ Working with {Id}");
    
    public void Reset() => Console.WriteLine($"  🔄 Reset {Id}");
}

// ═══════════════════════════════════════════════════════════
// THE SOLUTION: Object Pool
// ═══════════════════════════════════════════════════════════

public class SimpleObjectPool<T> where T : new()
{
    private readonly Stack<T> _pool = new();
    private readonly int _maxSize;
    
    public SimpleObjectPool(int maxSize = 10)
    {
        _maxSize = maxSize;
    }
    
    public T Get()
    {
        lock (_pool)
        {
            if (_pool.Count > 0)
            {
                Console.WriteLine("  ♻️ Reusing from pool");
                return _pool.Pop();
            }
        }
        Console.WriteLine("  🆕 Pool empty, creating new");
        return new T();
    }
    
    public void Return(T item)
    {
        lock (_pool)
        {
            if (_pool.Count < _maxSize)
            {
                _pool.Push(item);
                Console.WriteLine("  📥 Returned to pool");
            }
            else
            {
                Console.WriteLine("  🗑️ Pool full, discarding");
            }
        }
    }
    
    public int Count => _pool.Count;
}

// ═══════════════════════════════════════════════════════════
// DEMO: See the difference
// ═══════════════════════════════════════════════════════════

public static class BasicPoolDemo
{
    public static void Run()
    {
        Console.WriteLine("╔════════════════════════════════════╗");
        Console.WriteLine("║   BASIC OBJECT POOL DEMO           ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        // ❌ WITHOUT POOL
        Console.WriteLine("WITHOUT POOL (3 objects):");
        var sw = System.Diagnostics.Stopwatch.StartNew();
        for (int i = 0; i < 3; i++)
        {
            var obj = new ExpensiveObject();
            obj.DoWork();
            // obj is garbage collected
        }
        Console.WriteLine($"⏱️ Time: {sw.ElapsedMilliseconds}ms\n");
        
        // ✅ WITH POOL
        Console.WriteLine("WITH POOL (3 uses, same object):");
        var pool = new SimpleObjectPool<ExpensiveObject>(5);
        sw.Restart();
        
        for (int i = 0; i < 3; i++)
        {
            var obj = pool.Get();
            obj.DoWork();
            pool.Return(obj);
        }
        Console.WriteLine($"⏱️ Time: {sw.ElapsedMilliseconds}ms");
        Console.WriteLine($"📊 Pool size: {pool.Count}");
    }
}
```

---

## Exercise 2: .NET's ArrayPool (3 min)

> **Production Use**: High-performance array operations, image processing, serialization

Create `ArrayPoolDemo.cs`:

```csharp
using System.Buffers;

namespace ObjectPoolDemo;

public static class ArrayPoolDemo
{
    public static void Run()
    {
        Console.WriteLine("\n╔════════════════════════════════════╗");
        Console.WriteLine("║   ARRAYPOOL - BUILT INTO .NET      ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        // Get the shared pool (no setup needed!)
        var pool = ArrayPool<byte>.Shared;
        
        // ═══════════════════════════════════════════
        // SCENARIO: Process multiple data chunks
        // Like reading files, network packets, etc.
        // ═══════════════════════════════════════════
        
        Console.WriteLine("Processing 5 data chunks...\n");
        
        for (int i = 0; i < 5; i++)
        {
            // Rent an array (might be larger than requested!)
            byte[] buffer = pool.Rent(1024);
            
            try
            {
                Console.WriteLine($"Chunk {i + 1}:");
                Console.WriteLine($"  Requested: 1024 bytes");
                Console.WriteLine($"  Got: {buffer.Length} bytes");
                
                // Simulate work
                Array.Fill(buffer, (byte)(i + 1));
                Console.WriteLine($"  Processed ✓");
            }
            finally
            {
                // ALWAYS return! Use try/finally
                pool.Return(buffer, clearArray: true);
                Console.WriteLine($"  Returned to pool ♻️\n");
            }
        }
        
        // ═══════════════════════════════════════════
        // WHY THIS MATTERS
        // ═══════════════════════════════════════════
        
        Console.WriteLine("💡 WHY ARRAYPOOL MATTERS:");
        Console.WriteLine("┌─────────────────────────────────────┐");
        Console.WriteLine("│ Without Pool:                       │");
        Console.WriteLine("│   5 × new byte[1024] = 5 allocations│");
        Console.WriteLine("│   5 arrays for GC to collect        │");
        Console.WriteLine("├─────────────────────────────────────┤");
        Console.WriteLine("│ With Pool:                          │");
        Console.WriteLine("│   1 allocation, reused 5 times      │");
        Console.WriteLine("│   Zero GC pressure                  │");
        Console.WriteLine("└─────────────────────────────────────┘");
    }
}
```

---

## Exercise 3: .NET's ObjectPool (5 min)

> **Production Use**: ASP.NET Core's StringBuilderPool, JSON serialization

```powershell
# Already added, but just in case:
dotnet add package Microsoft.Extensions.ObjectPool
```

Create `DotNetObjectPoolDemo.cs`:

```csharp
using Microsoft.Extensions.ObjectPool;

namespace ObjectPoolDemo;

public static class DotNetObjectPoolDemo
{
    public static void Run()
    {
        Console.WriteLine("\n╔════════════════════════════════════╗");
        Console.WriteLine("║   MICROSOFT.EXTENSIONS.OBJECTPOOL  ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        // ═══════════════════════════════════════════
        // OPTION 1: Default pool (for simple types)
        // ═══════════════════════════════════════════
        
        Console.WriteLine("1️⃣ StringBuilder Pool (built-in):\n");
        
        var sbPool = new DefaultObjectPool<StringBuilder>(
            new StringBuilderPooledObjectPolicy());
        
        // Use it 3 times
        for (int i = 0; i < 3; i++)
        {
            var sb = sbPool.Get();
            try
            {
                sb.Append($"Request #{i + 1}: ");
                sb.Append("Processing data...");
                Console.WriteLine($"  {sb}");
            }
            finally
            {
                sbPool.Return(sb); // Auto-cleared!
            }
        }
        
        // ═══════════════════════════════════════════
        // OPTION 2: Custom objects with policy
        // ═══════════════════════════════════════════
        
        Console.WriteLine("\n2️⃣ Custom Object Pool:\n");
        
        var workerPool = new DefaultObjectPool<Worker>(
            new WorkerPolicy(), 
            maximumRetained: 5);
        
        // Simulate parallel work
        var tasks = Enumerable.Range(1, 10).Select(i => Task.Run(() =>
        {
            var worker = workerPool.Get();
            try
            {
                worker.Process($"Job-{i}");
            }
            finally
            {
                workerPool.Return(worker);
            }
        }));
        
        Task.WaitAll(tasks.ToArray());
        
        Console.WriteLine("\n✅ 10 jobs processed with pooled workers!");
    }
}

// ═══════════════════════════════════════════
// CUSTOM POOLABLE OBJECT
// ═══════════════════════════════════════════

public class Worker
{
    public int Id { get; set; }
    public bool IsInitialized { get; set; }
    
    public void Initialize()
    {
        Thread.Sleep(50); // Expensive!
        IsInitialized = true;
        Console.WriteLine($"  Worker {Id} initialized");
    }
    
    public void Process(string job)
    {
        Console.WriteLine($"  Worker {Id} processing {job}");
    }
    
    public void Reset()
    {
        // Clear state for reuse
    }
}

// ═══════════════════════════════════════════
// POOL POLICY - Controls create/return behavior
// ═══════════════════════════════════════════

public class WorkerPolicy : IPooledObjectPolicy<Worker>
{
    private int _nextId = 1;
    
    public Worker Create()
    {
        var worker = new Worker { Id = _nextId++ };
        worker.Initialize();
        return worker;
    }
    
    public bool Return(Worker worker)
    {
        // Return true to keep in pool, false to discard
        if (!worker.IsInitialized) return false;
        
        worker.Reset();
        return true;
    }
}

// For StringBuilder
public class StringBuilderPooledObjectPolicy : IPooledObjectPolicy<StringBuilder>
{
    public StringBuilder Create() => new StringBuilder();
    
    public bool Return(StringBuilder sb)
    {
        sb.Clear();
        return sb.Capacity <= 4096; // Don't keep huge builders
    }
}
```

---

## Exercise 4: Database Connection Pool (7 min)

> **Production Use**: Entity Framework, Dapper, ADO.NET - ALL use connection pooling!

Create `DatabasePoolDemo.cs`:

```csharp
namespace ObjectPoolDemo;

// ═══════════════════════════════════════════════════════════
// REAL-WORLD: Database Connection Pooling
// This is what SQL Server, PostgreSQL, etc. do internally
// ═══════════════════════════════════════════════════════════

public static class DatabasePoolDemo
{
    public static async Task RunAsync()
    {
        Console.WriteLine("\n╔════════════════════════════════════╗");
        Console.WriteLine("║   DATABASE CONNECTION POOL         ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        var pool = new ConnectionPool(
            connectionString: "Server=localhost;Database=Test",
            minSize: 2,
            maxSize: 5);
        
        Console.WriteLine("📊 Initial pool state:");
        pool.PrintStatus();
        
        // Simulate 10 concurrent database requests
        Console.WriteLine("\n🚀 Simulating 10 concurrent requests...\n");
        
        var tasks = Enumerable.Range(1, 10).Select(async i =>
        {
            var conn = await pool.GetConnectionAsync();
            try
            {
                Console.WriteLine($"Request {i}: Got connection {conn.Id}");
                await Task.Delay(100); // Simulate query
                Console.WriteLine($"Request {i}: Query complete");
            }
            finally
            {
                pool.ReleaseConnection(conn);
            }
        });
        
        await Task.WhenAll(tasks);
        
        Console.WriteLine("\n📊 Final pool state:");
        pool.PrintStatus();
    }
}

// ═══════════════════════════════════════════
// SIMULATED DATABASE CONNECTION
// ═══════════════════════════════════════════

public class DbConnection
{
    public int Id { get; }
    public string ConnectionString { get; }
    public bool IsOpen { get; private set; }
    public DateTime LastUsed { get; set; }
    
    public DbConnection(int id, string connectionString)
    {
        Id = id;
        ConnectionString = connectionString;
    }
    
    public async Task OpenAsync()
    {
        // Real connection takes time!
        await Task.Delay(50);
        IsOpen = true;
        Console.WriteLine($"  🔌 Connection {Id} opened");
    }
    
    public void Close()
    {
        IsOpen = false;
    }
}

// ═══════════════════════════════════════════
// CONNECTION POOL (simplified version of real pools)
// ═══════════════════════════════════════════

public class ConnectionPool
{
    private readonly string _connectionString;
    private readonly int _minSize;
    private readonly int _maxSize;
    
    private readonly Stack<DbConnection> _available = new();
    private readonly HashSet<DbConnection> _inUse = new();
    private readonly SemaphoreSlim _semaphore;
    private int _nextId = 1;
    
    public ConnectionPool(string connectionString, int minSize, int maxSize)
    {
        _connectionString = connectionString;
        _minSize = minSize;
        _maxSize = maxSize;
        _semaphore = new SemaphoreSlim(maxSize, maxSize);
        
        // Pre-create minimum connections
        Console.WriteLine($"🏗️ Pre-creating {minSize} connections...");
        for (int i = 0; i < minSize; i++)
        {
            var conn = CreateConnection();
            conn.OpenAsync().Wait();
            _available.Push(conn);
        }
    }
    
    public async Task<DbConnection> GetConnectionAsync()
    {
        // Wait if pool is exhausted
        await _semaphore.WaitAsync();
        
        lock (_available)
        {
            DbConnection conn;
            
            if (_available.Count > 0)
            {
                conn = _available.Pop();
            }
            else
            {
                conn = CreateConnection();
                conn.OpenAsync().Wait();
            }
            
            conn.LastUsed = DateTime.UtcNow;
            _inUse.Add(conn);
            return conn;
        }
    }
    
    public void ReleaseConnection(DbConnection conn)
    {
        lock (_available)
        {
            _inUse.Remove(conn);
            _available.Push(conn);
        }
        _semaphore.Release();
    }
    
    private DbConnection CreateConnection()
    {
        return new DbConnection(_nextId++, _connectionString);
    }
    
    public void PrintStatus()
    {
        Console.WriteLine($"  Available: {_available.Count}");
        Console.WriteLine($"  In Use: {_inUse.Count}");
        Console.WriteLine($"  Total: {_available.Count + _inUse.Count}/{_maxSize}");
    }
}
```

---

## Exercise 5: HttpClient Pool (5 min)

> **Production Use**: IHttpClientFactory in ASP.NET Core!

Create `HttpClientPoolDemo.cs`:

```csharp
namespace ObjectPoolDemo;

// ═══════════════════════════════════════════════════════════
// REAL-WORLD: HttpClient Pooling
// This is what IHttpClientFactory does in ASP.NET Core
// ═══════════════════════════════════════════════════════════

public static class HttpClientPoolDemo
{
    public static async Task RunAsync()
    {
        Console.WriteLine("\n╔════════════════════════════════════╗");
        Console.WriteLine("║   HTTPCLIENT POOLING               ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        // ═══════════════════════════════════════════
        // ❌ THE WRONG WAY (Socket Exhaustion!)
        // ═══════════════════════════════════════════
        
        Console.WriteLine("❌ WRONG: Creating new HttpClient each time\n");
        Console.WriteLine("// DON'T DO THIS!");
        Console.WriteLine("for (int i = 0; i < 100; i++)");
        Console.WriteLine("{");
        Console.WriteLine("    using var client = new HttpClient(); // BAD!");
        Console.WriteLine("    await client.GetAsync(url);");
        Console.WriteLine("}");
        Console.WriteLine("// Causes socket exhaustion!\n");
        
        // ═══════════════════════════════════════════
        // ✅ THE RIGHT WAY (Pooled handlers)
        // ═══════════════════════════════════════════
        
        Console.WriteLine("✅ RIGHT: Use pooled HttpClient\n");
        
        var factory = new SimpleHttpClientFactory();
        
        // Simulate 10 API calls
        var tasks = Enumerable.Range(1, 10).Select(async i =>
        {
            var client = factory.CreateClient("github-api");
            Console.WriteLine($"  Request {i}: Using handler {client.GetHashCode() % 1000}");
            
            // Real API call would go here
            await Task.Delay(10);
        });
        
        await Task.WhenAll(tasks);
        
        factory.PrintStatus();
        
        // ═══════════════════════════════════════════
        // REAL ASP.NET CORE USAGE
        // ═══════════════════════════════════════════
        
        Console.WriteLine("\n📘 In ASP.NET Core, use IHttpClientFactory:\n");
        Console.WriteLine(@"// In Startup.cs / Program.cs
services.AddHttpClient(""github"", client =>
{
    client.BaseAddress = new Uri(""https://api.github.com"");
    client.DefaultRequestHeaders.Add(""User-Agent"", ""MyApp"");
});

// In your service
public class GitHubService
{
    private readonly IHttpClientFactory _factory;
    
    public GitHubService(IHttpClientFactory factory)
    {
        _factory = factory;
    }
    
    public async Task<string> GetRepoAsync(string repo)
    {
        var client = _factory.CreateClient(""github""); // Pooled!
        return await client.GetStringAsync($""/repos/{repo}"");
    }
}");
    }
}

// Simplified version of what ASP.NET Core does
public class SimpleHttpClientFactory
{
    private readonly Dictionary<string, HttpMessageHandler> _handlers = new();
    private readonly object _lock = new();
    
    public HttpClient CreateClient(string name)
    {
        lock (_lock)
        {
            if (!_handlers.TryGetValue(name, out var handler))
            {
                handler = new SocketsHttpHandler
                {
                    PooledConnectionLifetime = TimeSpan.FromMinutes(2),
                    MaxConnectionsPerServer = 10
                };
                _handlers[name] = handler;
                Console.WriteLine($"  🆕 Created new handler for '{name}'");
            }
            
            return new HttpClient(handler, disposeHandler: false);
        }
    }
    
    public void PrintStatus()
    {
        Console.WriteLine($"\n📊 Handler pool: {_handlers.Count} handlers");
    }
}
```

---

## Exercise 6: Game Object Pool (5 min)

> **Production Use**: Unity, Unreal Engine, any game with particles/bullets

Create `GameObjectPoolDemo.cs`:

```csharp
namespace ObjectPoolDemo;

// ═══════════════════════════════════════════════════════════
// REAL-WORLD: Game Object Pooling (Bullets, Particles, etc.)
// Every game engine uses this pattern!
// ═══════════════════════════════════════════════════════════

public static class GameObjectPoolDemo
{
    public static void Run()
    {
        Console.WriteLine("\n╔════════════════════════════════════╗");
        Console.WriteLine("║   GAME OBJECT POOL (Bullet Hell!)  ║");
        Console.WriteLine("╚════════════════════════════════════╝\n");
        
        var bulletPool = new GameObjectPool<Bullet>(
            factory: () => new Bullet(),
            reset: b => b.Reset(),
            initialSize: 20);
        
        Console.WriteLine($"🎮 Pool created with {bulletPool.AvailableCount} bullets\n");
        
        // Simulate shooting
        Console.WriteLine("💥 Player fires 5 bullets:\n");
        var activeBullets = new List<Bullet>();
        
        for (int i = 0; i < 5; i++)
        {
            var bullet = bulletPool.Get();
            bullet.Fire(x: i * 10, y: 0, velocityY: 100);
            activeBullets.Add(bullet);
        }
        
        bulletPool.PrintStatus();
        
        // Simulate bullets going off-screen
        Console.WriteLine("\n🌟 3 bullets hit targets (returned to pool):\n");
        
        for (int i = 0; i < 3; i++)
        {
            var bullet = activeBullets[i];
            bullet.OnHit();
            bulletPool.Return(bullet);
        }
        
        bulletPool.PrintStatus();
        
        // ═══════════════════════════════════════════
        // BULLET HELL: Spawn 100 bullets rapidly
        // ═══════════════════════════════════════════
        
        Console.WriteLine("\n🔥 BULLET HELL MODE: 100 bullets!\n");
        
        var sw = System.Diagnostics.Stopwatch.StartNew();
        var hellBullets = new List<Bullet>();
        
        for (int i = 0; i < 100; i++)
        {
            var bullet = bulletPool.Get();
            bullet.Fire(x: i % 50, y: 0, velocityY: 50 + i);
            hellBullets.Add(bullet);
        }
        
        Console.WriteLine($"⏱️ Spawned 100 bullets in {sw.ElapsedMilliseconds}ms");
        bulletPool.PrintStatus();
        
        // Return all
        foreach (var b in hellBullets)
        {
            bulletPool.Return(b);
        }
        
        Console.WriteLine("\n♻️ All bullets returned:");
        bulletPool.PrintStatus();
    }
}

// ═══════════════════════════════════════════
// GAME OBJECT
// ═══════════════════════════════════════════

public class Bullet
{
    public int Id { get; }
    public bool IsActive { get; private set; }
    public float X { get; private set; }
    public float Y { get; private set; }
    public float VelocityY { get; private set; }
    
    private static int _nextId = 1;
    
    public Bullet()
    {
        Id = _nextId++;
        // Expensive: Load sprite, set up collision, etc.
    }
    
    public void Fire(float x, float y, float velocityY)
    {
        X = x;
        Y = y;
        VelocityY = velocityY;
        IsActive = true;
    }
    
    public void OnHit()
    {
        Console.WriteLine($"  💥 Bullet {Id} hit something!");
        IsActive = false;
    }
    
    public void Reset()
    {
        IsActive = false;
        X = Y = VelocityY = 0;
    }
}

// ═══════════════════════════════════════════
// GENERIC GAME OBJECT POOL
// ═══════════════════════════════════════════

public class GameObjectPool<T> where T : class
{
    private readonly Stack<T> _pool = new();
    private readonly Func<T> _factory;
    private readonly Action<T> _reset;
    private int _totalCreated;
    private int _inUse;
    
    public int AvailableCount => _pool.Count;
    public int InUseCount => _inUse;
    public int TotalCreated => _totalCreated;
    
    public GameObjectPool(Func<T> factory, Action<T> reset, int initialSize = 10)
    {
        _factory = factory;
        _reset = reset;
        
        // Pre-warm the pool
        for (int i = 0; i < initialSize; i++)
        {
            _pool.Push(CreateNew());
        }
    }
    
    public T Get()
    {
        T item;
        
        lock (_pool)
        {
            item = _pool.Count > 0 ? _pool.Pop() : CreateNew();
            _inUse++;
        }
        
        return item;
    }
    
    public void Return(T item)
    {
        _reset(item);
        
        lock (_pool)
        {
            _pool.Push(item);
            _inUse--;
        }
    }
    
    private T CreateNew()
    {
        _totalCreated++;
        return _factory();
    }
    
    public void PrintStatus()
    {
        Console.WriteLine($"  📊 Pool Status:");
        Console.WriteLine($"     Available: {AvailableCount}");
        Console.WriteLine($"     In Use: {InUseCount}");
        Console.WriteLine($"     Total Created: {TotalCreated}");
    }
}
```

---

## Update Program.cs

```csharp
using ObjectPoolDemo;

Console.WriteLine("╔══════════════════════════════════════════════════════════════╗");
Console.WriteLine("║         OBJECT POOL PATTERN - ARCHITECT TRAINING             ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════════╝");

BasicPoolDemo.Run();
ArrayPoolDemo.Run();
DotNetObjectPoolDemo.Run();
await DatabasePoolDemo.RunAsync();
await HttpClientPoolDemo.RunAsync();
GameObjectPoolDemo.Run();

Console.WriteLine("\n\n");
Console.WriteLine("╔══════════════════════════════════════════════════════════════╗");
Console.WriteLine("║                    QUICK REFERENCE                           ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════════╝");
Console.WriteLine(@"
┌─────────────────────────────────────────────────────────────────┐
│  WHEN TO USE OBJECT POOL:                                       │
├─────────────────────────────────────────────────────────────────┤
│  ✅ Object creation is expensive (>1ms)                        │
│  ✅ Objects are created/destroyed frequently                   │
│  ✅ Objects are similar/reusable                               │
│  ✅ You need to limit resource usage                           │
├─────────────────────────────────────────────────────────────────┤
│  WHEN NOT TO USE:                                               │
├─────────────────────────────────────────────────────────────────┤
│  ❌ Cheap object creation (new DTO(), new List<T>())           │
│  ❌ Objects have unique state that can't be reset              │
│  ❌ Low-frequency creation                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  BUILT-IN .NET POOLS (use these first!):                        │
├─────────────────────────────────────────────────────────────────┤
│  ArrayPool<T>.Shared     → Reuse arrays (Rent/Return)          │
│  MemoryPool<T>.Shared    → Reuse Memory<T>                     │
│  DefaultObjectPool<T>    → Microsoft.Extensions.ObjectPool     │
│  IHttpClientFactory      → HttpClient with pooled handlers     │
│  DbConnection pooling    → Built into ADO.NET connection string│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  CONNECTION STRING POOLING:                                      │
├─────────────────────────────────────────────────────────────────┤
│  SQL Server: ""...;Pooling=true;Min Pool Size=5;Max Pool Size=100""
│  PostgreSQL: ""...;Pooling=true;Minimum Pool Size=5;Maximum Pool Size=100""
│  MySQL:      ""...;Pooling=true;MinimumPoolSize=5;MaximumPoolSize=100""
└─────────────────────────────────────────────────────────────────┘
");
```

---

## 🏃 Run It

```powershell
cd "c:\Users\lFJl\source\repos\senior_arquitecture\code\csharp\ObjectPoolDemo"
dotnet run
```

---

## 🧠 Key Takeaways (Remember These!)

| Concept | One-Liner |
|---------|-----------|
| **Object Pool** | Reuse expensive objects instead of creating new |
| **ArrayPool** | `ArrayPool<T>.Shared.Rent()` / `Return()` |
| **ObjectPool** | `Microsoft.Extensions.ObjectPool` for custom objects |
| **HttpClient** | ALWAYS use `IHttpClientFactory`, never `new HttpClient()` in loops |
| **DB Connections** | Already pooled! Just use connection strings correctly |
| **Game Objects** | Pre-create bullets/particles, activate/deactivate |

---

## 🎯 Interview Quick Answers

**Q: What is Object Pool?**
> "Reusable cache of pre-initialized objects to avoid expensive creation."

**Q: When to use it?**
> "Expensive creation + frequent use + similar objects."

**Q: Real-world examples?**
> "Database connections, HTTP clients, thread pools, game bullets."

**Q: .NET built-in pools?**
> "ArrayPool, MemoryPool, IHttpClientFactory, connection string pooling."

---

**Next Step**: Move to **Dependency Injection** when ready!
