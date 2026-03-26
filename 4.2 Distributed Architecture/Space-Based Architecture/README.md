# Space-Based Architecture (SBA) in C#

This page is a "do it now" training track for becoming a senior software architect while staying friendly to attention deficits.

## How to use this README (attention-friendly)
1. Read only the next section title.
2. Execute the commands under it.
3. Stop. Then come back for the next section title.

No theory walls first. You will build intuition by running small, realistic SBA pieces.

---

## What you are learning (SBA mindset)

- **Processing Units (PU)**: Self-contained nodes that hold *both* application logic *and* in-memory data. Any PU can serve any request — there is no single database bottleneck.
- **Data Grid**: Distributed in-memory store replicated across PUs. Reads and writes happen in RAM, not disk. Think Redis at the architectural level, but owned *by the application layer*.
- **Message Grid**: Routes requests and events between PUs without them knowing each other.
- **Virtualized Middleware**: Manages PU lifecycle, failover, and load balancing transparently.
- **No central database on the hot path**: The DB is only a persistence backup. The source of truth for live traffic is the in-memory grid.
- **Scale by adding PUs**: New nodes join the grid and get a copy of the data. The system scales horizontally without redesign.

SBA solves the problem where *the database becomes the bottleneck*, not the application servers. Used in: airline seat booking, stock trading, online gaming, flash sale systems.

---

## Prerequisites

Install/use:
- [.NET SDK 8+](https://dotnet.microsoft.com/download)
- PowerShell 5+ (or pwsh)

Verify:
```powershell
dotnet --version
```

No Docker required for this exercise. Orleans runs in-process for local development.

---

## Exercise 1 (60 minutes): Flight seat booking with Microsoft Orleans

**Real-world scenario**: Thousands of users compete to book the last seats on a flight. With a traditional database, you get deadlocks, row locks, and connection pool exhaustion. With SBA (Orleans here), each flight lives as an independent in-memory Processing Unit — no shared database lock, no bottleneck.

```
[BookingApi]  --calls grain-->  FlightGrain("AA-101")  (in-memory: seat map, 200 seats)
                                      |
                              Claim seat instantly in RAM
                                      |
                              Write-behind to DB (async, non-blocking)
```

Each `FlightGrain` IS a Processing Unit: it holds its own data in memory and processes all requests for that flight. Multiple flights = multiple independent grains = horizontal scale with zero shared lock.

### Step 1) Create the solution and projects

In PowerShell, run:
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture"
mkdir sba-csharp -Force
cd sba-csharp

dotnet new sln -n sba-csharp
dotnet new classlib  -n sba-csharp.Grains
dotnet new webapi    -n sba-csharp.BookingApi

dotnet sln add .\sba-csharp.Grains\sba-csharp.Grains.csproj
dotnet sln add .\sba-csharp.BookingApi\sba-csharp.BookingApi.csproj

dotnet add .\sba-csharp.BookingApi\sba-csharp.BookingApi.csproj reference .\sba-csharp.Grains\sba-csharp.Grains.csproj
```

### Step 2) Add Orleans packages

Run:
```powershell
# Grains project: grain logic lives here
dotnet add .\sba-csharp.Grains\sba-csharp.Grains.csproj package Microsoft.Orleans.Sdk

# API project: hosts the silo + exposes HTTP endpoints
dotnet add .\sba-csharp.BookingApi\sba-csharp.BookingApi.csproj package Microsoft.Orleans.Sdk
dotnet add .\sba-csharp.BookingApi\sba-csharp.BookingApi.csproj package Microsoft.Orleans.Server
```

### Step 3) Define the grain interface (the contract)

Create this file:
`sba-csharp.Grains/IFlightGrain.cs`

Paste:
```csharp
namespace sba_csharp.Grains;

// IFlightGrain is the contract for one Processing Unit.
// One grain instance = one flight. Grain key = flight number ("AA-101").
// Orleans routes every request for "AA-101" to the same grain instance
// — no external coordination needed, no lock contention between flights.
public interface IFlightGrain : IGrainWithStringKey
{
    // Returns how many seats are still available for this flight.
    Task<int> GetAvailableSeatsAsync();

    // Tries to book `count` seats. Returns the booked seat numbers, or empty if not enough seats.
    Task<IReadOnlyList<string>> BookSeatsAsync(string passengerId, int count);

    // Returns the current seat map (seat number -> passengerId or null if free).
    Task<IReadOnlyDictionary<string, string?>> GetSeatMapAsync();
}
```

### Step 4) Implement the FlightGrain (the Processing Unit)

Create this file:
`sba-csharp.Grains/FlightGrain.cs`

Paste:
```csharp
using Orleans.Runtime;

namespace sba_csharp.Grains;

// SBA concept: FlightGrain IS a Processing Unit.
// It owns its data (seat map) in memory — no database call on the hot path.
// Orleans guarantees single-threaded execution per grain: no locks needed here.
// This is the key insight of SBA: the unit of scale IS the unit of data ownership.
public class FlightGrain : Grain, IFlightGrain
{
    // SBA Data Grid equivalent: this dictionary lives in RAM inside this grain.
    // For "AA-101", this is the authoritative seat map — no DB read on every booking.
    private readonly Dictionary<string, string?> _seatMap = new();

    private bool _initialized;

    // Called once when the grain activates (comes alive in the cluster).
    // In production: load initial state from DB here (write-behind pattern).
    public override Task OnActivateAsync(CancellationToken cancellationToken)
    {
        if (!_initialized)
        {
            // Initialize 180 economy seats for this flight.
            // In production: restore from persistent store (CosmosDB, PostgreSQL, etc.)
            for (int row = 1; row <= 30; row++)
            {
                foreach (var col in new[] { "A", "B", "C", "D", "E", "F" })
                {
                    _seatMap[$"{row}{col}"] = null; // null = free
                }
            }
            _initialized = true;
        }
        return base.OnActivateAsync(cancellationToken);
    }

    public Task<int> GetAvailableSeatsAsync()
    {
        var count = _seatMap.Values.Count(v => v is null);
        return Task.FromResult(count);
    }

    public Task<IReadOnlyList<string>> BookSeatsAsync(string passengerId, int count)
    {
        // No lock needed — Orleans guarantees one call at a time per grain.
        // This is the "single writer" guarantee of the SBA Processing Unit.
        var freeSeats = _seatMap
            .Where(kv => kv.Value is null)
            .Select(kv => kv.Key)
            .Take(count)
            .ToList();

        if (freeSeats.Count < count)
        {
            // Not enough seats — return empty list (caller decides how to handle).
            return Task.FromResult<IReadOnlyList<string>>(Array.Empty<string>());
        }

        foreach (var seat in freeSeats)
        {
            _seatMap[seat] = passengerId;
        }

        // SBA write-behind pattern: persist to DB asynchronously.
        // The HTTP response is already sent before the DB write completes.
        // In production: use a reliable outbox or Orleans reminder to retry on failure.
        _ = PersistBookingAsync(passengerId, freeSeats);

        return Task.FromResult<IReadOnlyList<string>>(freeSeats);
    }

    public Task<IReadOnlyDictionary<string, string?>> GetSeatMapAsync()
    {
        return Task.FromResult<IReadOnlyDictionary<string, string?>>(_seatMap);
    }

    private Task PersistBookingAsync(string passengerId, List<string> seats)
    {
        // Simulates writing to a database in the background.
        // In production: use IStorageProvider (Orleans built-in) or publish a domain event.
        Console.WriteLine($"[persistence] Saving booking: passenger={passengerId} seats=[{string.Join(",", seats)}] flight={this.GetPrimaryKeyString()}");
        return Task.CompletedTask;
    }
}
```

### Step 5) Wire up Orleans silo and API endpoints

Replace `sba-csharp.BookingApi/Program.cs` with:
```csharp
using sba_csharp.Grains;

var builder = WebApplication.CreateBuilder(args);

// SBA concept: the Silo IS the Virtual Middleware.
// It manages grain (Processing Unit) lifecycle, routing, and failover.
// In production: use Azure Clustering or Kubernetes to run multiple silos.
builder.Host.UseOrleans(silo =>
{
    // Local development: single-node silo, in-memory clustering.
    // Production: replace with .UseAzureStorageClustering(...) or .UseKubernetesClustering(...).
    silo.UseLocalhostClustering();

    // In production: configure grain storage to CosmosDB, PostgreSQL, Azure Table, etc.
    // This is the write-behind layer — the DB receives data after the response is sent.
    silo.AddMemoryGrainStorage("Default");
});

var app = builder.Build();

// --- Endpoint: Get available seats for a flight ---
app.MapGet("/flights/{flightNumber}/seats", async (string flightNumber, IGrainFactory grains) =>
{
    // Orleans routes this call to the FlightGrain for this specific flight.
    // SBA: no query to the database — the grain answers from RAM instantly.
    var flight = grains.GetGrain<IFlightGrain>(flightNumber);
    var available = await flight.GetAvailableSeatsAsync();

    return Results.Ok(new { flightNumber, availableSeats = available });
});

// --- Endpoint: Book seats on a flight ---
app.MapPost("/flights/{flightNumber}/bookings", async (
    string flightNumber,
    BookingRequest request,
    IGrainFactory grains) =>
{
    var flight = grains.GetGrain<IFlightGrain>(flightNumber);

    // SBA processing unit handles this atomically in memory.
    // Concurrent requests for the same flight are serialized by Orleans automatically.
    // Concurrent requests for DIFFERENT flights are fully parallel — zero contention.
    var bookedSeats = await flight.BookSeatsAsync(request.PassengerId, request.SeatCount);

    if (bookedSeats.Count == 0)
    {
        return Results.Conflict(new { error = "Not enough seats available", flightNumber });
    }

    return Results.Created($"/flights/{flightNumber}/bookings/{request.PassengerId}", new
    {
        flightNumber,
        passengerId = request.PassengerId,
        bookedSeats
    });
});

// --- Endpoint: View the full seat map ---
app.MapGet("/flights/{flightNumber}/seat-map", async (string flightNumber, IGrainFactory grains) =>
{
    var flight = grains.GetGrain<IFlightGrain>(flightNumber);
    var seatMap = await flight.GetSeatMapAsync();

    var occupied = seatMap.Where(kv => kv.Value is not null)
                          .Select(kv => new { seat = kv.Key, passenger = kv.Value });
    var free = seatMap.Where(kv => kv.Value is null).Select(kv => kv.Key);

    return Results.Ok(new { flightNumber, occupied, freeSeats = free });
});

app.Run();

record BookingRequest(string PassengerId, int SeatCount);
```

### Step 6) Delete the auto-generated placeholder class

Run:
```powershell
del ".\sba-csharp.Grains\Class1.cs"
```

### Step 7) Build the solution

Run:
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\sba-csharp"
dotnet build
```

Expected: `Build succeeded. 0 Error(s)`

### Step 8) Run the API

Run:
```powershell
dotnet run --project .\sba-csharp.BookingApi\sba-csharp.BookingApi.csproj
```

Expected output includes:
```
Orleans Silo started successfully.
```

### Step 9) Test: check available seats

Open a second PowerShell window and run:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/flights/AA-101/seats"
```

Expected:
```json
{ "flightNumber": "AA-101", "availableSeats": 180 }
```

The grain activated on first access. 180 seats initialized in RAM. No database queried.

### Step 10) Test: book seats

Run:
```powershell
$body = @{
  PassengerId = "passenger-007"
  SeatCount   = 2
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/flights/AA-101/bookings" `
  -ContentType "application/json" -Body $body
```

Expected:
```json
{
  "flightNumber": "AA-101",
  "passengerId": "passenger-007",
  "bookedSeats": ["1A", "1B"]
}
```

Run the command again with a different PassengerId and watch it pick the next free seats.

### Step 11) Test: concurrent bookings on different flights

Run both commands at nearly the same time:
```powershell
# These two grains run in parallel — completely independent in-memory state, zero contention.
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/flights/AA-101/seats"
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/flights/UA-500/seats"
```

Key insight: `AA-101` and `UA-500` are two independent Processing Units. They never share a lock, never contend on a database row. Scale to 10,000 flights with zero extra coordination.

### Step 12) Test: exhaust all seats

Run this loop to book all 180 seats:
```powershell
for ($i = 1; $i -le 90; $i++) {
    $body = @{ PassengerId = "pax-$i"; SeatCount = 2 } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "http://localhost:5000/flights/AA-101/bookings" `
      -ContentType "application/json" -Body $body | Out-Null
}

# Now try to book one more — should return 409 Conflict
$body = @{ PassengerId = "pax-overflow"; SeatCount = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:5000/flights/AA-101/bookings" `
  -ContentType "application/json" -Body $body
```

Expected: `409 Conflict` with `"Not enough seats available"`.

---

## Exercise 2 (20-30 minutes): Architecture thinking (no new code)

Write 6-10 lines in your notes for each question. These are questions you will face in a senior architect role.

- What happens to in-memory grain state when the silo (server) crashes? How do you recover it?
- If you need to query "all flights with fewer than 10 seats remaining" across 50,000 grains, how do you do it without activating every grain?
- How does Orleans prevent two concurrent requests for the same grain from corrupting data? What is the trade-off?
- When would you choose SBA over a standard microservices + database approach?
- In the booking scenario, the write-behind to the database is async. What happens if the silo crashes between the booking and the DB write? How do real systems handle this?

Hint for senior architects: your answers should cover both *the mechanism* and *the operational runbook*.

---

## Real-world production SBA examples (C#)

### 1) American Airlines / Airline Booking Systems

**The problem**: 500 simultaneous users book seats on the same flight during a flash sale. A traditional RDBMS deadlocks on the seat row.

**SBA solution**:
```
Each FlightGrain = one flight's seat map in RAM
                       |
         All requests for "AA-101" route to one grain
                       |
         Orleans single-threaded guarantee = no race conditions
                       |
         Write-behind to PostgreSQL after response sent
```

**C# production pattern**: Use Orleans with `IPersistentState<T>` for automatic write-behind:
```csharp
public class FlightGrain : Grain, IFlightGrain
{
    // Orleans reads this from storage on activation, writes back when you call WriteStateAsync().
    // You get the in-memory speed on the hot path + durability on the write-behind path.
    private readonly IPersistentState<FlightState> _state;

    public FlightGrain([PersistentState("flight", "Default")] IPersistentState<FlightState> state)
    {
        _state = state;
    }

    public async Task<IReadOnlyList<string>> BookSeatsAsync(string passengerId, int count)
    {
        var freeSeats = _state.State.SeatMap
            .Where(kv => kv.Value is null)
            .Select(kv => kv.Key)
            .Take(count)
            .ToList();

        if (freeSeats.Count < count) return Array.Empty<string>();

        foreach (var seat in freeSeats)
            _state.State.SeatMap[seat] = passengerId;

        // Persist after updating in-memory state.
        // Orleans will serialize and store this in your configured storage provider.
        await _state.WriteStateAsync();

        return freeSeats;
    }
}

public class FlightState
{
    public Dictionary<string, string?> SeatMap { get; set; } = new();
}
```

**Why SBA here**:
- 50,000 flights = 50,000 independent grains = zero cross-flight contention.
- Each grain handles its own flight serially — no distributed lock manager needed.
- Adding more silos to the cluster gives you more RAM and CPU with no schema changes.

---

### 2) High-frequency trading platform (order book)

**The problem**: Each trading symbol (AAPL, MSFT, TSLA) has an order book. Market makers send thousands of quotes per second. A shared DB cannot keep up.

**SBA solution**:
```
OrderBookGrain("AAPL")  = in-memory order book (bids + asks sorted in RAM)
                              |
      Market makers send quotes -> grain processes in RAM at microsecond speed
                              |
      Matching engine runs inside the grain (no external call)
                              |
      Matched trades published as events to downstream systems
```

**C# production pattern**:
```csharp
public interface IOrderBookGrain : IGrainWithStringKey
{
    Task<MatchResult> SubmitOrderAsync(Order order);
    Task<OrderBookSnapshot> GetSnapshotAsync();
}

public class OrderBookGrain : Grain, IOrderBookGrain
{
    // SBA Data Grid: the full order book lives in RAM — sorted collections.
    // In production: use SortedDictionary or a purpose-built price-level structure.
    private readonly SortedDictionary<decimal, Queue<Order>> _bids = new(Comparer<decimal>.Create((a, b) => b.CompareTo(a)));
    private readonly SortedDictionary<decimal, Queue<Order>> _asks = new();

    public Task<MatchResult> SubmitOrderAsync(Order order)
    {
        // Price-time priority matching, entirely in RAM.
        // No database roundtrip in the critical path — this is the SBA value proposition.
        var matched = TryMatch(order);

        if (matched.IsFilled)
        {
            // Write-behind: publish trade to event bus (Kafka/Service Bus) for downstream systems.
            // The trade confirmation returns to the caller before persistence completes.
            _ = PublishTradeAsync(matched);
        }
        else
        {
            AddToBook(order);
        }

        return Task.FromResult(matched);
    }

    private MatchResult TryMatch(Order incoming) { /* matching logic */ return new MatchResult(); }
    private void AddToBook(Order order) { /* add to bids or asks */ }
    private Task PublishTradeAsync(MatchResult match) => Task.CompletedTask; // stub
}
```

**Why SBA here**:
- Sub-millisecond response time is impossible with DB roundtrips.
- One grain per symbol = perfect data locality, no cache invalidation complexity.
- Replay from an event log reconstructs grain state after a crash.

---

### 3) Real-time gaming leaderboard (flash-scale)

**The problem**: A mobile game launches and 2 million players submit scores in the first hour. A Redis sorted set on one node becomes the bottleneck. A SQL leaderboard deadlocks.

**SBA solution**:
```
Shard leaderboard into 100 LeaderboardShardGrains (players A-Z by name bucket)
                              |
Each grain owns its shard's sorted score list in RAM
                              |
GlobalLeaderboardGrain periodically merges top-N from each shard
                              |
Players query the merged top-100 from GlobalLeaderboardGrain (read from RAM, <1ms)
```

**C# production pattern**:
```csharp
public interface ILeaderboardShardGrain : IGrainWithIntegerKey
{
    Task SubmitScoreAsync(string playerId, long score);
    Task<IReadOnlyList<LeaderboardEntry>> GetTopNAsync(int n);
}

public class LeaderboardShardGrain : Grain, ILeaderboardShardGrain
{
    // SBA Data Grid: sorted score list in RAM. No Redis, no SQL on the hot path.
    private readonly SortedDictionary<long, List<string>> _scores
        = new(Comparer<long>.Create((a, b) => b.CompareTo(a))); // descending

    public Task SubmitScoreAsync(string playerId, long score)
    {
        // Update score in RAM — O(log n), no I/O.
        if (!_scores.TryGetValue(score, out var players))
        {
            players = new List<string>();
            _scores[score] = players;
        }
        players.Add(playerId);
        return Task.CompletedTask;
    }

    public Task<IReadOnlyList<LeaderboardEntry>> GetTopNAsync(int n)
    {
        var top = _scores
            .SelectMany(kv => kv.Value.Select(p => new LeaderboardEntry(p, kv.Key)))
            .Take(n)
            .ToList();
        return Task.FromResult<IReadOnlyList<LeaderboardEntry>>(top);
    }
}

// Aggregator grain runs on a timer to merge all shards.
public class GlobalLeaderboardGrain : Grain, IGlobalLeaderboardGrain
{
    private List<LeaderboardEntry> _cachedTopN = new();

    public override Task OnActivateAsync(CancellationToken cancellationToken)
    {
        // SBA: grains can schedule work internally — no external scheduler needed.
        RegisterTimer(_ => RefreshLeaderboardAsync(), null, TimeSpan.Zero, TimeSpan.FromSeconds(5));
        return base.OnActivateAsync(cancellationToken);
    }

    private async Task RefreshLeaderboardAsync()
    {
        var tasks = Enumerable.Range(0, 100)
            .Select(i => GrainFactory.GetGrain<ILeaderboardShardGrain>(i).GetTopNAsync(100));
        var shardResults = await Task.WhenAll(tasks);

        _cachedTopN = shardResults
            .SelectMany(r => r)
            .OrderByDescending(e => e.Score)
            .Take(100)
            .ToList();
    }

    public Task<IReadOnlyList<LeaderboardEntry>> GetTopNAsync(int n)
        => Task.FromResult<IReadOnlyList<LeaderboardEntry>>(_cachedTopN.Take(n).ToList());
}

record LeaderboardEntry(string PlayerId, long Score);
```

**Why SBA here**:
- 2 million score submissions hit 100 independent shards = 20,000 per shard = trivially parallel.
- Reads from `GlobalLeaderboardGrain` are sub-millisecond (pre-merged, in RAM).
- Adding more silos distributes shards automatically. No manual rebalancing.

---

## Architecture checklist (SBA, C#)

Use this before you declare "we built Space-Based Architecture":

- **Processing Unit independence**: can each grain be activated, run, and recover without coordinating with other grains?
- **Data locality**: does each grain own its data? Are there cross-grain database queries on the hot path? (There should not be.)
- **Write-behind durability**: is there a reliable path from in-memory state to persistent storage? Is it retried on failure?
- **Activation strategy**: do you load state from DB only at activation (cold start), never on every request?
- **Single-writer guarantee**: is concurrent access to one Processing Unit serialized? (Orleans does this automatically per grain.)
- **Horizontal scale**: does adding a new silo node distribute load automatically? Or do you need manual rebalancing?
- **Crash recovery**: can a grain reconstruct its in-memory state from storage after a silo crash?
- **Read models**: for queries that span many grains (e.g., "all flights under 10 seats"), do you maintain a separate read model updated by events — rather than scanning all grains?
- **Grain size**: is each grain focused on one aggregate (one flight, one order book, one user session)? Overly large grains become single-node bottlenecks — the same problem SBA was meant to solve.

---

## EDA vs Space-Based Architecture

Both are distributed and async-friendly. The difference is in *where data lives* and *what drives the design*.

### The core difference in one line

> EDA: services **react to events** that flow between them through a broker.
> SBA: logic and data **co-locate in Processing Units**; no broker sits between you and your data.

### Data ownership

| Concern | EDA | SBA |
|---|---|---|
| Where live data lives | Each service has its own database; data is shared via events | In-memory inside Processing Units (grains); DB is a write-behind backup |
| How data is accessed on the hot path | Service reads its own DB (I/O on every request) | Grain reads its own RAM (no I/O on the hot path) |
| Consistency model | Eventual — services sync via events asynchronously | Strong within a grain (single-writer); eventual between grains |
| Source of truth | Each service's database | The in-memory grid (with write-behind to storage) |

### Communication model

| Concern | EDA | SBA |
|---|---|---|
| How components communicate | Via events published to a broker (RabbitMQ, Kafka, Azure Service Bus) | Via direct grain-to-grain calls managed by the virtual middleware (Orleans) |
| Producer knowledge | Producer does not know consumers — zero coupling | Caller knows the grain interface — explicit coupling to the grain contract |
| Temporal coupling | Absent — producer fires and forgets | Caller awaits the grain response (request/response by default) |
| Broker required | Yes — a message broker is a core infrastructure component | No external broker — Orleans handles routing internally |

### Scaling strategy

| Concern | EDA | SBA |
|---|---|---|
| How you scale | Scale consumer services independently; partition broker topics | Add silo nodes to the cluster; grains redistribute automatically |
| Bottleneck location | Broker throughput, consumer lag, or shared DB under heavy write load | Memory per silo node; grain activation time on first access |
| Data partitioning | Manual (partition keys on Kafka topics, consumer groups) | Automatic (Orleans places grains across silos by consistent hashing) |

### Failure behavior

| Concern | EDA | SBA |
|---|---|---|
| What happens when a node dies | Events stay in the broker; consumers on other nodes pick them up | Grains on that silo reactivate on surviving silos; state reloads from storage |
| Data loss risk | Low — broker persists events durably before any consumer processes them | Medium — in-memory state can be lost between writes; mitigated by write-behind frequency and event sourcing |
| Recovery complexity | Consumer replays from broker offset (Kafka) or DLQ | Grain reloads from persistent state store on reactivation |

### When to choose each

Choose **EDA** when:
- Services are owned by different teams and must evolve independently.
- You need audit trails, event replay, or the ability for new consumers to join later and catch up.
- Eventual consistency is acceptable and you do not need sub-millisecond response time.
- You are integrating heterogeneous systems (legacy, third-party, regulated).

Choose **SBA** when:
- Latency is the primary constraint (trading, gaming, booking during flash sales).
- Your bottleneck is the database under concurrent write load (seat locks, order book locks).
- Data is naturally partitioned by a key (flight number, symbol, user ID) and requests mostly touch one partition at a time.
- You need strong consistency *within* an entity without distributed transactions.

### They are not mutually exclusive

In production systems, SBA and EDA are layered:

```
[API]
  |
  v
[FlightGrain]  <-- SBA: in-memory seat map, sub-millisecond booking
  |
  | write-behind
  v
[Database]
  |
  | after persist, publish domain event
  v
[Event Broker (RabbitMQ / Kafka)]  <-- EDA: fan out to analytics, notifications, loyalty
  |             |
[Analytics]  [NotificationService]
```

Senior architect phrasing: "We use SBA at the transactional core where latency and consistency matter most — one grain owns one aggregate in RAM. We use EDA at the integration boundary where different teams and systems need to react to what happened, asynchronously, at their own pace."
