# Event-Driven Architecture (EDA) in C#

This page is a "do it now" training track for becoming a senior software architect while staying friendly to attention deficits.

## How to use this README (attention-friendly)
1. Read only the next section title.
2. Execute the commands under it.
3. Stop. Then come back for the next section title.

No long theory blocks first; you'll build intuition by running small, realistic EDA pieces.

---

## What you are learning (EDA mindset)
- Events are *facts that already happened* (past tense: `OrderPlaced`, `PaymentFailed`), not commands.
- Producers **do not know** who listens. That is the whole point — loose coupling.
- Consumers react *independently*, at their own pace (async by default).
- Coordination happens via *choreography* (each service reacts) not via a central orchestrator calling everyone.
- You plan for *eventual consistency*, *idempotency*, and *at-least-once delivery*.

---

## Prerequisites
Install/use:
- [.NET SDK 8+](https://dotnet.microsoft.com/download)
- PowerShell 5+ (or pwsh)
- Docker Desktop (to run RabbitMQ as event broker)

Verify:
```powershell
dotnet --info
docker --version
```

---

## Exercise 1 (60 minutes): EDA choreography with C# + MassTransit + RabbitMQ

You will build three independent services that talk only through events — no service calls another service directly.

```
[OrderApi]  --publishes--> OrderPlaced event
                                  |
              RabbitMQ (event broker / fanout exchange)
                    |                        |
        [InventoryWorker]          [NotificationWorker]
    (reserves stock)             (sends confirmation email)
```

This is real-world EDA choreography: the API publishes one event and two consumers react independently.

### Step 1) Create the solution and projects

In PowerShell, run:
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture"
mkdir eda-csharp -Force
cd eda-csharp

dotnet new sln -n eda-csharp
dotnet new classlib -n eda-csharp.Events
dotnet new webapi -n eda-csharp.OrderApi
dotnet new worker -n eda-csharp.InventoryWorker
dotnet new worker -n eda-csharp.NotificationWorker

dotnet sln add .\eda-csharp.Events\eda-csharp.Events.csproj
dotnet sln add .\eda-csharp.OrderApi\eda-csharp.OrderApi.csproj
dotnet sln add .\eda-csharp.InventoryWorker\eda-csharp.InventoryWorker.csproj
dotnet sln add .\eda-csharp.NotificationWorker\eda-csharp.NotificationWorker.csproj
```

### Step 2) Add project references

Run:
```powershell
dotnet add .\eda-csharp.OrderApi\eda-csharp.OrderApi.csproj reference .\eda-csharp.Events\eda-csharp.Events.csproj
dotnet add .\eda-csharp.InventoryWorker\eda-csharp.InventoryWorker.csproj reference .\eda-csharp.Events\eda-csharp.Events.csproj
dotnet add .\eda-csharp.NotificationWorker\eda-csharp.NotificationWorker.csproj reference .\eda-csharp.Events\eda-csharp.Events.csproj
```

### Step 3) Add messaging packages

Run:
```powershell
dotnet add .\eda-csharp.OrderApi\eda-csharp.OrderApi.csproj package MassTransit
dotnet add .\eda-csharp.OrderApi\eda-csharp.OrderApi.csproj package MassTransit.RabbitMQ

dotnet add .\eda-csharp.InventoryWorker\eda-csharp.InventoryWorker.csproj package MassTransit
dotnet add .\eda-csharp.InventoryWorker\eda-csharp.InventoryWorker.csproj package MassTransit.RabbitMQ

dotnet add .\eda-csharp.NotificationWorker\eda-csharp.NotificationWorker.csproj package MassTransit
dotnet add .\eda-csharp.NotificationWorker\eda-csharp.NotificationWorker.csproj package MassTransit.RabbitMQ
```

### Step 4) Start RabbitMQ locally

Run:
```powershell
docker run -d --rm --name rabbitmq-eda -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

RabbitMQ dashboard (optional, to watch events flow): open http://localhost:15672 in your browser.
Login: `guest` / `guest`

### Step 5) Define the event (the shared fact)

Create this file:
`eda-csharp.Events/OrderPlaced.cs`

Paste:
```csharp
namespace eda_csharp.Events;

// EDA rule: event names are past tense (something already happened).
// Event is a fact — it carries what happened, not what to do next.
public record OrderPlaced(
    Guid EventId,          // For idempotency: consumers deduplicate by this.
    string OrderId,
    string CustomerId,
    decimal TotalAmount,
    string[] ProductIds,
    DateTimeOffset OccurredAtUtc
);
```

### Step 6) Implement the Inventory consumer

Create this file:
`eda-csharp.InventoryWorker/Consumers/OrderPlacedConsumer.cs`

Paste:
```csharp
using MassTransit;
using eda_csharp.Events;

namespace eda_csharp.InventoryWorker.Consumers;

public class OrderPlacedConsumer : IConsumer<OrderPlaced>
{
    // In production: use a database-backed idempotency table keyed by EventId.
    private static readonly HashSet<Guid> Processed = new();

    public async Task Consume(ConsumeContext<OrderPlaced> context)
    {
        var ev = context.Message;

        lock (Processed)
        {
            if (Processed.Contains(ev.EventId)) return;
            Processed.Add(ev.EventId);
        }

        // Simulate stock reservation (in production: call inventory DB).
        Console.WriteLine($"[inventory] Reserving stock for order={ev.OrderId} products=[{string.Join(",", ev.ProductIds)}]");
        await Task.Delay(200);
        Console.WriteLine($"[inventory] Stock reserved for order={ev.OrderId}");
    }
}
```

Replace `eda-csharp.InventoryWorker/Program.cs` with:
```csharp
using MassTransit;
using eda_csharp.InventoryWorker.Consumers;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<OrderPlacedConsumer>();

    cfg.UsingRabbitMq((context, rabbit) =>
    {
        rabbit.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });

        // Each consumer gets its own queue — this is what allows fanout (multiple consumers
        // independently receiving the same event).
        rabbit.ReceiveEndpoint("inventory-order-placed", e =>
        {
            e.ConfigureConsumer<OrderPlacedConsumer>(context);
        });
    });
});

var app = builder.Build();
app.Run();
```

### Step 7) Implement the Notification consumer

Create this file:
`eda-csharp.NotificationWorker/Consumers/OrderPlacedConsumer.cs`

Paste:
```csharp
using MassTransit;
using eda_csharp.Events;

namespace eda_csharp.NotificationWorker.Consumers;

public class OrderPlacedConsumer : IConsumer<OrderPlaced>
{
    private static readonly HashSet<Guid> Processed = new();

    public async Task Consume(ConsumeContext<OrderPlaced> context)
    {
        var ev = context.Message;

        lock (Processed)
        {
            if (Processed.Contains(ev.EventId)) return;
            Processed.Add(ev.EventId);
        }

        // Simulate sending a confirmation email (in production: call email/SMS provider).
        Console.WriteLine($"[notifications] Sending confirmation to customer={ev.CustomerId} for order={ev.OrderId} total={ev.TotalAmount:C}");
        await Task.Delay(150);
        Console.WriteLine($"[notifications] Email sent for order={ev.OrderId}");
    }
}
```

Replace `eda-csharp.NotificationWorker/Program.cs` with:
```csharp
using MassTransit;
using eda_csharp.NotificationWorker.Consumers;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<OrderPlacedConsumer>();

    cfg.UsingRabbitMq((context, rabbit) =>
    {
        rabbit.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });

        // Different queue name = independent consumer = same event reaches both workers.
        rabbit.ReceiveEndpoint("notification-order-placed", e =>
        {
            e.ConfigureConsumer<OrderPlacedConsumer>(context);
        });
    });
});

var app = builder.Build();
app.Run();
```

### Step 8) Implement the Order API (event publisher)

Create this file:
`eda-csharp.OrderApi/Controllers/OrdersController.cs`

Paste:
```csharp
using MassTransit;
using Microsoft.AspNetCore.Mvc;
using eda_csharp.Events;

namespace eda_csharp.OrderApi.Controllers;

[ApiController]
[Route("orders")]
public class OrdersController : ControllerBase
{
    private readonly IPublishEndpoint _publish;

    public OrdersController(IPublishEndpoint publish)
    {
        _publish = publish;
    }

    public record PlaceOrderRequest(string CustomerId, decimal TotalAmount, string[] ProductIds);

    [HttpPost]
    public async Task<IActionResult> PlaceOrder([FromBody] PlaceOrderRequest request)
    {
        var orderId = $"ORD-{Guid.NewGuid():N}"[..12];

        // EDA: publish the fact. The API does NOT call inventory or notifications directly.
        // It has zero knowledge of who listens — that is the core of EDA loose coupling.
        var ev = new OrderPlaced(
            EventId: Guid.NewGuid(),
            OrderId: orderId,
            CustomerId: request.CustomerId,
            TotalAmount: request.TotalAmount,
            ProductIds: request.ProductIds,
            OccurredAtUtc: DateTimeOffset.UtcNow
        );

        await _publish.Publish(ev);

        return Accepted(new { orderId, eventId = ev.EventId });
    }
}
```

Replace `eda-csharp.OrderApi/Program.cs` with:
```csharp
using MassTransit;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddMassTransit(cfg =>
{
    cfg.UsingRabbitMq((context, rabbit) =>
    {
        rabbit.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });
    });
});

var app = builder.Build();
app.MapControllers();
app.Run();
```

### Step 9) Run all three services

Open three terminal windows:

#### Window A: Start Inventory worker
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\eda-csharp"
dotnet run --project .\eda-csharp.InventoryWorker\eda-csharp.InventoryWorker.csproj
```

#### Window B: Start Notification worker
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\eda-csharp"
dotnet run --project .\eda-csharp.NotificationWorker\eda-csharp.NotificationWorker.csproj
```

#### Window C: Start Order API
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\eda-csharp"
dotnet run --project .\eda-csharp.OrderApi\eda-csharp.OrderApi.csproj
```

### Step 10) Publish an event (place an order)

Run in PowerShell:
```powershell
$body = @{
  CustomerId = "cust-007"
  TotalAmount = 129.99
  ProductIds = @("SKU-001", "SKU-042")
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/orders" -ContentType "application/json" -Body $body
```

Expected output:
- API returns `202 Accepted` with `orderId` and `eventId`
- **Window A** prints: `[inventory] Reserving stock...` then `[inventory] Stock reserved...`
- **Window B** prints: `[notifications] Sending confirmation...` then `[notifications] Email sent...`

The key insight: both consumers reacted to one event, independently, without knowing each other.

---

## Exercise 2 (20-30 minutes): Architecture thinking (no new code)

Write 6-10 lines in your notes for each question. These are the questions you will face in a senior architect role.

- What happens if `NotificationWorker` is down when the event is published? Does the event get lost?
- How do you guarantee a consumer processes each event *exactly once* in production?
- If the `OrderPlaced` event schema changes (add a field), how do you avoid breaking existing consumers?
- When would you use *choreography* (like this exercise) vs *orchestration* (a saga/process manager)?
- How would you trace a single order end-to-end across three services in production logs?

Hint for senior architects: your answers should cover both *technical mechanism* and *team/operational process*.

---

## Real-world production EDA examples (C#)

Use these as mental templates for architecture interviews and design reviews.

### 1) E-commerce order processing (choreography across microservices)

Real system: Amazon-style order pipeline.

```
OrderService  -->  OrderPlaced event
                        |
        ┌───────────────┼────────────────┐
        |               |                |
InventoryService  PaymentService  NotificationService
 (reserve stock)  (charge card)   (email + push)
        |               |
  StockReserved    PaymentProcessed
        |               |
        └─────> ShippingService (creates shipment)
```

Why EDA here:
- Each team owns their service independently. No team needs to change when a new consumer is added.
- The `OrderService` does not need to be updated when a `LoyaltyService` is added later.
- Services scale independently (payment queue can scale without affecting inventory).

C# production patterns used:
- MassTransit + Azure Service Bus (managed broker, no infra to operate).
- Outbox pattern on the `OrderService` side: write to DB + outbox in the same transaction, then relay to bus. This prevents the "event published but DB write failed" split-brain problem.
- Dead-letter queue (DLQ) for all consumers: failed messages are routed to DLQ for human triage, never silently dropped.

### 2) Payment gateway webhook → internal events

Real scenario: Stripe sends a `payment_intent.succeeded` webhook to your API.

```
Stripe webhook  -->  [WebhookController]  -->  PaymentConfirmed (internal event)
                                                        |
                                           ┌────────────┼────────────┐
                                    OrderService   InvoiceService  AnalyticsService
                                  (mark paid)     (generate PDF)  (record revenue)
```

Why EDA here:
- External events (Stripe, PayPal, Adyen) are translated into your domain's language at the boundary.
- Downstream services react without knowing the payment provider.
- When you switch from Stripe to Adyen, only the webhook adapter changes — all consumers stay the same.

C# production code pattern:
```csharp
// WebhookController translates external → internal event
[HttpPost("stripe/webhook")]
public async Task<IActionResult> StripeWebhook()
{
    // Validate Stripe signature first (security boundary)
    var stripeEvent = ConstructStripeEvent(Request);

    if (stripeEvent.Type == "payment_intent.succeeded")
    {
        var intent = stripeEvent.Data.Object as PaymentIntent;

        // Publish your domain event — NOT Stripe's raw object
        await _publish.Publish(new PaymentConfirmed(
            EventId: Guid.NewGuid(),
            OrderId: intent.Metadata["orderId"],
            Amount: intent.AmountReceived / 100m,
            Currency: intent.Currency.ToUpper(),
            OccurredAtUtc: DateTimeOffset.UtcNow
        ));
    }

    return Ok();
}
```

Senior insight: always translate external events into your domain's language at the boundary. Never let Stripe's schema leak into your OrderService.

### 3) Real-time inventory updates (Kafka event streaming)

Real scenario: A retailer needs every warehouse, store app, and analytics dashboard to see stock changes in real time.

```
WarehouseScanner  -->  StockAdjusted event  -->  Kafka topic: "inventory.stock-adjusted"
                                                           |
                              ┌────────────────────────────┼───────────────────────────┐
                         StoreAppService          AnalyticsPipeline         AlertingService
                       (update local UI)        (update dashboards)     (notify if low stock)
```

Why Kafka instead of RabbitMQ here:
- Kafka retains events for days/weeks — a new consumer can replay from the beginning and rebuild state.
- High throughput: millions of stock events per minute across thousands of SKUs.
- Event log is the source of truth (event sourcing style).

C# production pattern (MassTransit + Kafka):
```csharp
// In any consumer: replay from day 0 by specifying an offset
cfg.UsingKafka((context, kafka) =>
{
    kafka.TopicEndpoint<StockAdjusted>("inventory.stock-adjusted", "analytics-group", e =>
    {
        e.AutoOffsetReset = AutoOffsetReset.Earliest; // replay from start if new consumer
        e.ConfigureConsumer<StockAdjustedConsumer>(context);
    });
});
```

Senior insight: use Kafka when you need event replay, high throughput, or consumers that can join late and catch up. Use RabbitMQ/Service Bus when you need simple queue semantics and lower operational complexity.

---

## Architecture checklist (EDA, C#)

Use this before you declare "we built EDA":
- Events: are names past tense? Do they carry facts, not instructions?
- Loose coupling: does the publisher have zero knowledge of consumers? If yes to the producer knowing the consumer — it's not EDA, it's just async RPC.
- Idempotency: does every consumer handle duplicate delivery without side effects?
- Delivery guarantee: at-least-once confirmed? Dead-letter queue defined for all consumers?
- Schema evolution: do you use additive-only changes? Do consumers use tolerant reader pattern?
- Observability: correlation ID on every event? Structured logging with `EventId`, `OrderId`, consumer name?
- Replay capability: can a new consumer replay past events to rebuild state?
- Backpressure: can consumers signal they are overwhelmed, or do events pile up silently?

---

## SOA vs EDA: the real difference senior architects care about

Both SOA and EDA deal with distributed systems and async communication. The difference is in *what drives the design* and *how services are coupled*.

### The core difference in one line

> SOA: services expose **contracts** for others to call.
> EDA: services emit **facts** and react to facts from others.

### Coupling style

| Concern | SOA | EDA |
|---|---|---|
| What producers know | Producer knows the contract it exposes and the consumer it calls (often) | Producer knows nothing about consumers — it only publishes a fact |
| What consumers know | Consumer knows the service contract it calls | Consumer knows the event schema it subscribes to |
| Temporal coupling | Often present (request/response waits) | Absent by default (async, fire-and-forget) |
| Schema coupling | Strong (both sides must agree on request/response schema) | Weaker (consumers use tolerant reader; events evolve additively) |

### Coordination style

| Concern | SOA | EDA |
|---|---|---|
| How workflows are coordinated | Often **orchestration**: a central service calls each participant in order | Often **choreography**: each service reacts to events independently |
| Who knows the business process | Usually one service (the orchestrator) | Distributed — no single service has the full picture |
| Adding a new participant | Requires changing the orchestrator | Requires only the new consumer subscribing to the event |

### Governance vs autonomy

| Concern | SOA | EDA |
|---|---|---|
| Design focus | Contract governance, service reuse, enterprise standards | Team autonomy, independent deployability, loose coupling |
| Change impact | Changing a service contract requires coordinating all callers | Changing an event requires updating consumers (but they can evolve independently) |
| Who this suits | Large enterprises with many integration points, legacy systems, regulatory environments | Product teams that need to move fast and add capabilities without cross-team coordination |

### When to choose which

Choose **SOA** when:
- You have many heterogeneous systems (legacy, third-party, regulated) that must integrate with stable contracts.
- You need central governance over who calls what.
- Request/response semantics are required (the caller needs an immediate answer).

Choose **EDA** when:
- You want teams to add new capabilities without modifying existing services.
- You need to scale consumers independently.
- Eventual consistency is acceptable.
- You need event replay (audit, rebuilding read models, new consumers catching up).

### They are not mutually exclusive

In production systems, you will use both:
- SOA-style contracts for synchronous boundaries (API gateway, client-facing HTTP).
- EDA-style events for internal domain communication and cross-service reactions.

Senior architect phrasing: "We use request/response at the edges where the caller needs an immediate answer, and events internally where eventual consistency is acceptable and we want teams to evolve independently."
