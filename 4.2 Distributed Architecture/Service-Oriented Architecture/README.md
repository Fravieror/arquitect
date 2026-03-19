# Service-Oriented Architecture (SOA) in C#

This page is a “do it now” training track for becoming a senior software architect while staying friendly to attention deficits.

## How to use this README (attention-friendly)
1. Read only the next section title.
2. Execute the commands under it.
3. Stop. Then come back for the next section title.

No long theory blocks first; you’ll build intuition by running small, realistic SOA-style pieces.

---

## What you are learning (SOA mindset)
- Services expose *contracts* (schemas + semantics), not just endpoints.
- Integration is *independent* from the caller (usually async): queues/broker, orchestration, and/or adapters.
- You plan for *versioning*, *reliability*, and *governance* (policies, monitoring, error handling).
- You treat “enterprise integration” as a first-class architecture topic.

---

## Prerequisites
Install/use:
- [.NET SDK 8+](https://dotnet.microsoft.com/download)
- PowerShell 5+ (or pwsh)
- (Optional for local testing) Docker Desktop to run RabbitMQ

Verify:
```powershell
dotnet --info
```

---

## Exercise 1 (45 minutes): SOA-style async integration with C# + MassTransit
You will build:
- `soa-csharp.Contracts`: message contracts (the SOA contract surface)
- `soa-csharp.OrderApi`: a service facade (HTTP) that publishes a command to the bus
- `soa-csharp.OrderWorker`: a service that consumes the command and performs work asynchronously

### 1) Create the solution and projects
In PowerShell, run:
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture"
mkdir soa-csharp -Force
cd soa-csharp

dotnet new sln -n soa-csharp
dotnet new classlib -n soa-csharp.Contracts
dotnet new webapi -n soa-csharp.OrderApi
dotnet new worker -n soa-csharp.OrderWorker

dotnet sln add .\soa-csharp.Contracts\soa-csharp.Contracts.csproj
dotnet sln add .\soa-csharp.OrderApi\soa-csharp.OrderApi.csproj
dotnet sln add .\soa-csharp.OrderWorker\soa-csharp.OrderWorker.csproj
```

### 2) Add project references
Run:
```powershell
dotnet add .\soa-csharp.OrderApi\soa-csharp.OrderApi.csproj reference .\soa-csharp.Contracts\soa-csharp.Contracts.csproj
dotnet add .\soa-csharp.OrderWorker\soa-csharp.OrderWorker.csproj reference .\soa-csharp.Contracts\soa-csharp.Contracts.csproj
```

### 3) Add messaging packages
Run:
```powershell
dotnet add .\soa-csharp.OrderApi\soa-csharp.OrderApi.csproj package MassTransit
dotnet add .\soa-csharp.OrderApi\soa-csharp.OrderApi.csproj package MassTransit.RabbitMQ

dotnet add .\soa-csharp.OrderWorker\soa-csharp.OrderWorker.csproj package MassTransit
dotnet add .\soa-csharp.OrderWorker\soa-csharp.OrderWorker.csproj package MassTransit.RabbitMQ
```

### 4) (Optional) Start RabbitMQ locally
If you have Docker Desktop:
```powershell
docker run -d --rm --name rabbitmq-soa -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

If you do not have Docker, you can still read the architecture patterns below; executing the run commands will require a broker.

### 5) Define the SOA contract (message)
Create this file:
`soa-csharp.Contracts/OrderMessages.cs`

Paste:
```csharp
namespace soa_csharp.Contracts;

// SOA contract: stable message schema used across service boundaries.
public record PlaceOrder(
    Guid MessageId,
    string CustomerId,
    decimal TotalAmount,
    DateTimeOffset OccurredAtUtc
);
```

### 6) Implement the consumer (worker)
Replace the worker Program and create a consumer.

Create this file:
`soa-csharp.OrderWorker/Consumers/PlaceOrderConsumer.cs`

Paste:
```csharp
using MassTransit;
using soa_csharp.Contracts;

namespace soa_csharp.OrderWorker.Consumers;

public class PlaceOrderConsumer : IConsumer<PlaceOrder>
{
    // For real production: use a durable idempotency store keyed by MessageId.
    private static readonly HashSet<Guid> Seen = new();

    public async Task Consume(ConsumeContext<PlaceOrder> context)
    {
        var msg = context.Message;

        // Demonstrates a key SOA concern: reliability + duplicate handling.
        lock (Seen)
        {
            if (Seen.Contains(msg.MessageId))
                return;
            Seen.Add(msg.MessageId);
        }

        // Simulate work (e.g., persist order, call downstream services via adapters).
        Console.WriteLine($"[worker] Processing order for customer={msg.CustomerId} total={msg.TotalAmount} id={msg.MessageId}");

        await Task.Delay(TimeSpan.FromMilliseconds(300));
    }
}
```

Replace `soa-csharp.OrderWorker/Program.cs` with:
```csharp
using MassTransit;
using soa_csharp.Contracts;
using soa_csharp.OrderWorker.Consumers;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<PlaceOrderConsumer>();

    cfg.UsingRabbitMq((context, rabbit) =>
    {
        // Default local broker. In production: use configuration + secrets.
        rabbit.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });

        rabbit.ReceiveEndpoint("place-order", e =>
        {
            e.ConfigureConsumer<PlaceOrderConsumer>(context);
        });
    });
});

var app = builder.Build();
app.Run();
```

If your build fails, tell me the exact error and I will adjust the `Program.cs` for your template.

### 7) Implement the facade (HTTP publishes to bus)
Create this controller:
`soa-csharp.OrderApi/Controllers/OrdersController.cs`

Paste:
```csharp
using MassTransit;
using Microsoft.AspNetCore.Mvc;
using soa_csharp.Contracts;

namespace soa_csharp.OrderApi.Controllers;

[ApiController]
[Route("orders")]
public class OrdersController : ControllerBase
{
    private readonly IPublishEndpoint _publish;

    public OrdersController(IPublishEndpoint publish)
    {
        _publish = publish;
    }

    public record PlaceOrderRequest(string CustomerId, decimal TotalAmount);

    [HttpPost]
    public async Task<IActionResult> PlaceOrder([FromBody] PlaceOrderRequest request)
    {
        var msg = new PlaceOrder(
            MessageId: Guid.NewGuid(),
            CustomerId: request.CustomerId,
            TotalAmount: request.TotalAmount,
            OccurredAtUtc: DateTimeOffset.UtcNow
        );

        await _publish.Publish(msg);
        return Accepted(new { messageId = msg.MessageId });
    }
}
```

Replace `soa-csharp.OrderApi/Program.cs` with:
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

### 8) Run it
In three terminal windows:

#### Window A: RabbitMQ (if using Docker)
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
```

#### Window B: Start the worker
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\soa-csharp"
dotnet run --project .\soa-csharp.OrderWorker\soa-csharp.OrderWorker.csproj
```

#### Window C: Start the API
```powershell
cd "C:\Users\lFJl\source\repos\senior_arquitecture\soa-csharp"
dotnet run --project .\soa-csharp.OrderApi\soa-csharp.OrderApi.csproj
```

### 9) Call the service facade (so you see SOA behavior)
Find the API URL in the output. If it is `https://localhost:####`, use the matching one.

PowerShell call:
```powershell
$body = @{
  CustomerId = "cust-001"
  TotalAmount = 42.50
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5000/orders" -ContentType "application/json" -Body $body
```

Expected:
- API returns `202 Accepted` with a `messageId`
- Worker prints a line like: `[worker] Processing order ...`

---

## Exercise 2 (20-30 minutes): Add SOA governance thinking (no new code)
In a real organization, architecture quality is measured by how you handle non-happy-path behavior.

Answer (write 6-10 lines) in your notes:
- What is your SOA *contract versioning* strategy? (e.g., additive fields + semantic versioning)
- How do you implement idempotency for `MessageId` across deployments?
- What is your *retry policy* (immediate retry vs delayed) and why?
- Where do you put *policy enforcement*: API gateway, consumer, or transport layer?
- How do you monitor: end-to-end trace correlation IDs and failure rates?

Hint for senior architects: your answer should mention both *technology* and *operating model*.

---

## Real-world production SOA examples (what they look like in C#)
Use these as mental templates for architecture interviews and design reviews.

### 1) Enterprise integration with an ESB (SOAP + orchestration)
Scenario: Legacy systems speak SOAP/WSDL; your C# services must integrate without rewriting everything.
- Pattern: “Adapter services” wrap legacy interfaces and translate to modern internal contracts.
- Operational concern: schema governance, backward compatibility, and WSDL publishing/versioning.
- C# angle: WCF (classic .NET Framework) or CoreWCF (where applicable) for SOAP endpoints; use consistent DTO mapping.

What to say as a senior: “We isolate legacy volatility behind stable contracts and control versioning centrally.”

### 2) Async business workflows over a message broker (queues + saga/orchestration)
Scenario: Order placement triggers payments, inventory reservation, shipping booking, and notifications.
- Pattern: async commands/events + orchestration (saga) to handle multi-step failures.
- C# angle: message consumers validate commands, update state, and publish next steps; use outbox/inbox patterns for reliability.

Production-level must-haves:
- durable idempotency keys (like our `MessageId`)
- correlation IDs (so support teams can trace one order end-to-end)
- DLQ (dead-letter queue) handling and re-drive procedures

### 3) Cloud SOA integration (service-to-service contracts + Azure Service Bus)
Scenario: You want SOA without maintaining infrastructure.
- Pattern: publish/consume contracts on `Azure Service Bus` topics/subscriptions.
- C# angle: use Azure SDK clients or MassTransit integration, with proper retry and dead-lettering.

What to say:
- “Contracts are versioned; consumers are tolerant.”
- “Retry is policy-driven; poison messages are routed and triaged.”

---

## Architecture checklist (SOA, C#)
Use this before you declare “we built SOA”:
- Contracts: are they explicit, stable, versioned, and tested?
- Integration style: do you have a clear choice between sync (request/response) and async (messaging)?
- Reliability: idempotency, retries, DLQ, and poison message strategy are defined.
- Observability: correlation IDs, structured logging, metrics, and traceability.
- Governance: who owns contract changes? what is the release/process?
- Security: authn/authz at boundaries; message-level security where needed.

---

## Microservices vs Service-Oriented Architecture (SOA)
Both are “service” approaches, but they differ in emphasis and governance.

### What SOA emphasizes
- Business-aligned services with explicit contracts.
- Integration often includes an enterprise layer (ESB, gateway, orchestration engines, adapters).
- Governance: strong focus on contract lifecycle, versioning, policies, and enterprise-wide standards.
- Integration style is commonly hybrid (sync + async) and may involve SOAP/WS-* in regulated/legacy contexts.

### What Microservices emphasizes
- A decentralized style: services are independently deployable, owned by teams, and optimized for autonomous scaling and release.
- Contracts still matter, but the emphasis is on bounded contexts and independent evolution (often via event-driven communication).
- Platform and deployment automation are core to making the architecture work.

### A useful simplification
- SOA is often “enterprise integration first.”
- Microservices is often “team autonomy and independent delivery first.”

In practice, many real systems blend both ideas; the difference is usually *what drives design decisions* and *how governance vs autonomy is balanced*.

