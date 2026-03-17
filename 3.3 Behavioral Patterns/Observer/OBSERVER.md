# Observer (C#) — from “I know it” to “I can design it”

The **Observer pattern** is about **one-to-many dependency**: when one object changes state (**Subject / Publisher**), it **notifies** many dependents (**Observers / Subscribers**) so they can react.

Plain English: **“Tell me when this changes.”**  
Technical English: **publish-subscribe with a stable contract and decoupled listeners**.

---

## Why architects care (the real point)

Observer is less about “events exist” and more about **how you design change propagation** without turning the system into a tangled graph of direct calls.

- **Decoupling**: publishers don’t need to know who’s listening.
- **Extensibility**: new behaviors can subscribe without changing publisher code.
- **Boundaries**: in-process observer is cheap; cross-process needs a bus (Kafka/RabbitMQ/Azure Service Bus/etc.).

If you can explain **when not to use it**, you’re thinking like a senior.

---

## C# “Observer” in the real world

In .NET, the pattern most commonly appears as:

- **Events / delegates** (`event EventHandler<T>`) — simplest in-process Observer.
- **`IObservable<T>` / `IObserver<T>`** — formal push-based stream contract.
- **Reactive Extensions (Rx)** — `IObservable<T>` with operators (filter, throttle, retry, combine…).

Also related (bigger scope): **Domain events**, **Event bus**, **Message broker**, **Event sourcing** (not the same thing, but adjacent).

---

## Production scenarios (what it looks like in real systems)

- **Cache invalidation inside a service**
  - Inventory changes → cache entries for that SKU are invalidated.
  - Subscribers: cache layer, metrics, audit log.

- **Config hot-reload**
  - Config provider watches source → notifies subscribers.
  - Subscribers: HTTP clients (timeouts), feature flags, circuit breakers.

- **Business workflows**
  - Order shipped → notify email sender, loyalty points, analytics.
  - Architect decision: in-process event vs reliable message to a broker (exactly-once is hard; aim for at-least-once + idempotency).

- **UI / desktop apps**
  - ViewModel property changes → UI updates (Observer-like via bindings / `INotifyPropertyChanged`).

- **Monitoring / health**
  - Health state changes → notify dashboards and alerting logic.

---

## The hard parts (senior-level pitfalls and how to reason about them)

- **Memory leaks (the #1 practical issue)**
  - In C#, events keep strong references to subscribers. If a long-lived publisher holds an event, and a short-lived subscriber subscribes and forgets to unsubscribe → subscriber never gets GC’d.
  - Fix options:
    - Unsubscribe (`-=`) deterministically (e.g., `IDisposable` pattern).
    - Use **weak event** patterns (more advanced; sometimes needed in UI).

- **Synchronous notification can become an outage**
  - Events are typically **invoked synchronously**. One slow subscriber can block the publisher, increasing latency or causing timeouts.
  - Mitigation:
    - Keep handlers fast; offload work.
    - Consider async pipelines (channels, queues) or message bus for heavy work.

- **Error handling semantics**
  - If one subscriber throws, do you:
    - Stop notifying others (default if you don’t catch)?
    - Catch-and-continue (more resilient)?
    - Aggregate exceptions (more observable)?
  - Decide intentionally. Document it as part of the contract.

- **Ordering & reentrancy**
  - Subscribers might assume ordering; publishers often shouldn’t promise it.
  - Subscribers might cause changes that trigger the same event again (reentrancy). Guard against loops.

- **Threading**
  - Raising events from multiple threads needs care; subscribers may not be thread-safe.
  - In UI, you must marshal back to the UI thread.

- **Backpressure / overload**
  - High-frequency updates (prices, telemetry) can overwhelm subscribers.
  - Use throttling/debouncing/buffering (Rx is great here) or switch to pull-based polling when appropriate.

---

## What to type and run (C# console demo)

This demo shows:
1) classic **events** (most common “Observer in C#”)  
2) disciplined **unsubscribe** to avoid leaks  
3) a simple **contract** for change notification

### Step 1: Create a console app

In PowerShell:

```powershell
dotnet new console -n ObserverDemo
cd .\ObserverDemo
```

### Step 2: Replace `Program.cs` with this

```csharp
using System;
using System.Collections.Generic;

// SUBJECT (Publisher)
public sealed class PriceFeed
{
    private readonly Dictionary<string, decimal> _prices = new();

    // Observer contract: "a price changed"
    public event EventHandler<PriceChanged>? PriceChanged;

    public decimal? TryGet(string sku) => _prices.TryGetValue(sku, out var p) ? p : null;

    public void Upsert(string sku, decimal newPrice)
    {
        _prices.TryGetValue(sku, out var oldPrice);
        if (oldPrice == newPrice) return;

        _prices[sku] = newPrice;

        // Raise synchronously; subscribers must be fast.
        PriceChanged?.Invoke(this, new PriceChanged(sku, oldPrice, newPrice, DateTimeOffset.UtcNow));
    }
}

public sealed record PriceChanged(
    string Sku,
    decimal OldPrice,
    decimal NewPrice,
    DateTimeOffset AtUtc
);

// OBSERVER 1: Logging
public sealed class PriceLogger : IDisposable
{
    private readonly PriceFeed _feed;
    private bool _disposed;

    public PriceLogger(PriceFeed feed)
    {
        _feed = feed;
        _feed.PriceChanged += OnPriceChanged;
    }

    private void OnPriceChanged(object? sender, PriceChanged e)
        => Console.WriteLine($"[LOG] {e.AtUtc:O} SKU={e.Sku} {e.OldPrice} -> {e.NewPrice}");

    public void Dispose()
    {
        if (_disposed) return;
        _feed.PriceChanged -= OnPriceChanged; // critical to avoid leaks in long-lived publishers
        _disposed = true;
    }
}

// OBSERVER 2: Cache invalidation (toy example)
public sealed class PriceCache : IDisposable
{
    private readonly PriceFeed _feed;
    private readonly Dictionary<string, decimal> _cache = new();
    private bool _disposed;

    public PriceCache(PriceFeed feed)
    {
        _feed = feed;
        _feed.PriceChanged += OnPriceChanged;
    }

    public decimal? Get(string sku) => _cache.TryGetValue(sku, out var v) ? v : null;

    private void OnPriceChanged(object? sender, PriceChanged e)
    {
        // In real systems you might invalidate, refresh asynchronously, or mark stale.
        _cache[e.Sku] = e.NewPrice;
        Console.WriteLine($"[CACHE] Updated SKU={e.Sku} to {e.NewPrice}");
    }

    public void Dispose()
    {
        if (_disposed) return;
        _feed.PriceChanged -= OnPriceChanged;
        _disposed = true;
    }
}

public static class Program
{
    public static void Main()
    {
        var feed = new PriceFeed();

        using var logger = new PriceLogger(feed);
        using var cache = new PriceCache(feed);

        feed.Upsert("SKU-123", 10.00m);
        feed.Upsert("SKU-123", 12.50m);
        feed.Upsert("SKU-123", 12.50m); // no-op, avoids noisy notifications

        Console.WriteLine($"[READ] Cache says SKU-123 = {cache.Get("SKU-123")}");

        // Show unsubscribe works: after disposal, observers stop receiving notifications.
        Console.WriteLine("Disposing observers...");
    }
}
```

### Step 3: Run it

```powershell
dotnet run
```

---

## How to talk about Observer like a senior (quick mental checklist)

- **Contract**: What exactly is the event? What’s the payload? Is it immutable? Does it include timestamps/correlation IDs?
  - **Answer**: Define the event as a stable **business fact** (not “what my code happens to do”), with a **versionable schema**.
  - **Answer**: Payload should be **minimal but sufficient**: identifiers, new value (and optionally old), and metadata you’ll need for debugging and ordering.
  - **Answer**: Prefer **immutable** event args/records. In C#, use `record`/`readonly` data and avoid passing mutable domain objects.
  - **Answer**: Include **`OccurredAt` (UTC)** and a **correlation/trace id** when the event crosses boundaries or is used for observability. In-process you can omit correlation, but it’s still helpful in logs.
  - **Example**: `PriceChanged { Sku, OldPrice, NewPrice, OccurredAtUtc, CorrelationId }` (even if only two subscribers exist today).
- **Delivery semantics**: Best-effort in-process? Reliable across processes? At-least-once vs at-most-once?
  - **Answer**: Decide whether you need **reliability**. In-process events are typically **best-effort** (lost on crash, not persisted).
  - **Answer**: If it must survive restarts / guarantee eventual processing, you’re in **messaging** territory (outbox + broker), not just Observer.
  - **Answer**: Across processes, default to **at-least-once** delivery and make consumers **idempotent**. At-most-once is simpler but risks loss; exactly-once is expensive and usually illusory end-to-end.
  - **Example**: “Send customer email” should usually be brokered (durable) + idempotent; “update in-memory cache” can be best-effort.
- **Failure policy**: What happens if a subscriber fails or is slow?
  - **Answer**: Choose and document one:
    - **Fail-fast**: propagate exception; publisher operation fails (useful when subscribers are part of the same transaction).
    - **Isolate**: catch/log per subscriber and continue (common for “side effects” like metrics, auditing).
  - **Answer**: Avoid making a hot-path synchronous event handler do slow I/O. If a handler can block, offload (queue/channel/background worker) or go async with a defined policy.
  - **Example**: Request pipeline raises `OrderPlaced`; metrics handler failure should not fail checkout → catch/log. Fraud-check handler might be required → fail-fast or make it part of the core flow, not a “subscriber”.
- **Lifecycle**: Who owns unsubscribe? Is publisher long-lived? Could subscribers leak?
  - **Answer**: Treat subscription as a **resource** with an owner. Default rule: **whoever subscribes must unsubscribe**.
  - **Answer**: In C#, `event` subscriptions create strong references; if publisher outlives subscriber, you can leak memory. Use `IDisposable` subscriptions (`using`) or explicit teardown hooks.
  - **Example**: A singleton `PriceFeed` + per-request subscriber is a leak unless you unsubscribe at end of request.
- **Performance**: Notification frequency, hot paths, and whether you need batching/throttling.
  - **Answer**: Ask “is this a **hot path**?” If yes, keep notification payload small, avoid allocations, and avoid sync I/O in handlers.
  - **Answer**: If updates are frequent (telemetry, prices), add **coalescing** (latest wins), **throttling/debouncing**, or **batching**. Rx or `Channel<T>` patterns help.
  - **Example**: A price feed at 1k updates/sec should not cause 1k cache refresh HTTP calls/sec; throttle to 10/sec or batch per 100ms window.
- **Boundaries**: Inside a process → events/IObservable. Across services → message broker + idempotent consumers.
  - **Answer**: Pick the mechanism based on the boundary:
    - **Same process**: events / `IObservable<T>` (fast, simple, not durable).
    - **Cross-service**: broker (durable, retry, backpressure), with **idempotent** consumers and often an **outbox** to avoid “DB committed but message lost”.
  - **Answer**: Don’t “fake reliability” with in-process observers. If the business requires durability, use the right tool.
  - **Example**: “Inventory reserved” should publish a durable integration event; “update in-memory read model” can stay in-process.

---

## When NOT to use Observer

- When there is exactly one consumer and it’s part of the same abstraction → a direct method call is clearer.
- When consumers must be reliable and durable across restarts → use a **message broker** (Observer alone won’t persist).
- When the change rate is huge and consumers can’t keep up → you need backpressure/buffering (Rx/Channels) or redesign.

