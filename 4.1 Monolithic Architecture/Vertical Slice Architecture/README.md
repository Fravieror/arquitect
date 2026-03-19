# Vertical Slice Architecture for C# – Senior Software Architect Training

Welcome! This guide is designed for learners with attention deficits:
- short steps
- clear “done when” checkpoints
- production-minded examples (idempotency, persistence boundaries, failure modes)

You will type and run the code yourself. The goal is understanding, not copy/paste perfection.

---

## How to use this guide (ADHD-friendly)

1. Do one step at a time. When a step says “Done when…”, stop there.
2. After each step, run the app and test the endpoint once.
3. If you get stuck: copy the exact error message and retry only the last step.

---

## 1) What Vertical Slice Architecture is

Vertical Slice Architecture organizes your code by **use case / feature**, not by **technical layers** (Controllers vs Services vs Repositories).

Instead of splitting everything horizontally into layers, you create **slices** that are vertical “end-to-end stacks” for a single request:
- endpoint contract (HTTP route + input)
- request/command/query DTOs
- handler/business rules
- persistence/external adapters needed by that use case

**Key outcome:** opening one folder for a slice helps you understand the whole flow for that feature.

---

## 2) The core rules (what makes it actually “vertical slice”)

### Cohesion per use case
- Keep everything needed to fulfill one request inside the slice folder (input -> handler -> output).

### Thin endpoints, real logic in handlers
- Endpoint/controller should mostly map inputs, call the handler, and translate results to HTTP.
- Business rules live in handlers.

### Minimize cross-slice coupling
- Prefer sharing domain concepts, not handler internals.
- If two slices share a rule, extract it to a shared domain/application component (carefully).

### Production boundaries live in slices too
- If a use case needs idempotency, retries, error mapping, transactional writes, or outbox patterns, put those concerns in/near the slice (not scattered across generic controllers).

---

## 3) When Vertical Slice is a good fit (architect view)

### Great fit
- Product teams shipping features frequently (e-commerce, SaaS workflows, internal tooling)
- You want feature ownership to map directly to code ownership

### Watch-outs
- If your product has heavy, shared “workflow engines”, naive slicing can cause duplication. Extract shared domain/application abstractions.
- If you put too much logic into endpoints, you lose testability (handlers must own the rules).

---

## 4) Production-grade examples to keep in mind

When you design slices for real systems, these questions matter:

- **Idempotency:** How do you prevent duplicate charges/orders when clients retry? (common for payments, form submissions, message consumers)
- **Transactional consistency:** When a slice writes to DB and triggers side effects, how do you avoid partial failure? (often outbox/inbox patterns)
- **Error mapping:** How do you translate domain/infrastructure errors into consistent HTTP errors?
- **Resilience:** What retry strategy applies, and where do timeouts and circuit breakers live?
- **Observability:** Where are structured logs, correlation ids, metrics, and traces for each slice?

This guide includes idempotency in the write slice.

---

## 5) Build a small Vertical Slice API in C# (step-by-step)

We’ll build a Web API with two slices:
- `GET /api/products/{id}` (read slice)
- `POST /api/orders` (write slice with payment + idempotency)

We will not create code files for you automatically. You will create them by typing/pasting exactly what is below.

---

### Step 1: Create the solution

Run PowerShell:

```sh
mkdir VerticalSliceDemo
cd VerticalSliceDemo

dotnet new sln -n VerticalSliceDemo
dotnet new webapi -n Api

dotnet sln add Api/Api.csproj
```

Done when:
- the solution compiles and `dotnet run` starts.

Run it once to verify:

```sh
cd Api
dotnet run
```

Stop with `Ctrl+C`.

---

### Step 2: Add packages

```sh
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection

dotnet add package FluentValidation
dotnet add package FluentValidation.AspNetCore
```

Done when:
- `dotnet restore` succeeds (it usually runs implicitly).

---

## 6) Create the folder structure (the slices)

Inside `Api`, create these folders:

```txt
Features
  Products
    GetById
  Orders
    CreateOrder
Shared
  Abstractions
  Adapters
```

You can create folders using your IDE or with PowerShell `mkdir`.

---

## 7) Slice #1: Get product by id (read)

### Step 3: Persistence contract + DTO

Create `Shared/Abstractions/ProductDto.cs`:

```csharp
namespace Api.Shared.Abstractions;

public sealed record ProductDto(Guid Id, string Name, decimal Price);
```

Create `Shared/Abstractions/IProductRepository.cs`:

```csharp
namespace Api.Shared.Abstractions;

public interface IProductRepository
{
    Task<ProductDto?> GetByIdAsync(Guid id, CancellationToken ct);
}
```

### Step 4: In-memory adapter (training stand-in)

Create `Shared/Adapters/InMemoryProductRepository.cs`:

```csharp
using Api.Shared.Abstractions;

namespace Api.Shared.Adapters;

public sealed class InMemoryProductRepository : IProductRepository
{
    private readonly Dictionary<Guid, ProductDto> _data = new()
    {
        [Guid.Parse("11111111-1111-1111-1111-111111111111")] =
            new ProductDto(Guid.Parse("11111111-1111-1111-1111-111111111111"), "Keyboard", 49.99m),
        [Guid.Parse("22222222-2222-2222-2222-222222222222")] =
            new ProductDto(Guid.Parse("22222222-2222-2222-2222-222222222222"), "Mouse", 19.99m)
    };

    public Task<ProductDto?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        _data.TryGetValue(id, out var dto);
        return Task.FromResult(dto);
    }
}
```

### Step 5: Request + handler (the slice core)

Create `Features/Products/GetById/GetProductByIdQuery.cs`:

```csharp
using Api.Shared.Abstractions;
using MediatR;

namespace Api.Features.Products.GetById;

public sealed record GetProductByIdQuery(Guid Id) : IRequest<ProductDto?>;
```

Create `Features/Products/GetById/GetProductByIdHandler.cs`:

```csharp
using Api.Shared.Abstractions;
using MediatR;

namespace Api.Features.Products.GetById;

public sealed class GetProductByIdHandler : IRequestHandler<GetProductByIdQuery, ProductDto?>
{
    private readonly IProductRepository _products;

    public GetProductByIdHandler(IProductRepository products)
    {
        _products = products;
    }

    public Task<ProductDto?> Handle(GetProductByIdQuery request, CancellationToken cancellationToken)
        => _products.GetByIdAsync(request.Id, cancellationToken);
}
```

### Step 6: Validator (real-world habit)

Create `Features/Products/GetById/GetProductByIdValidator.cs`:

```csharp
using FluentValidation;

namespace Api.Features.Products.GetById;

public sealed class GetProductByIdValidator : AbstractValidator<GetProductByIdQuery>
{
    public GetProductByIdValidator()
    {
        RuleFor(x => x.Id).NotEqual(Guid.Empty);
    }
}
```

### Step 7: Endpoint/controller (thin wrapper)

Create `Features/Products/GetById/GetProductByIdEndpoint.cs`:

```csharp
using Api.Features.Products.GetById;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Api.Features.Products.GetById;

[ApiController]
public sealed class GetProductByIdEndpoint : ControllerBase
{
    private readonly IMediator _mediator;

    public GetProductByIdEndpoint(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet("api/products/{id:guid}")]
    public async Task<ActionResult<object>> Handle([FromRoute] Guid id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetProductByIdQuery(id), ct);
        if (result is null) return NotFound();
        return Ok(result);
    }
}
```

---

## 8) Slice #2: Create order (write) with payment + idempotency

This slice demonstrates a production behavior: **clients retry**, so the slice must not double-charge.

### Step 8: Contracts (request DTOs + interfaces)

Create `Shared/Abstractions/IPaymentGateway.cs`:

```csharp
namespace Api.Shared.Abstractions;

public interface IPaymentGateway
{
    Task ChargeAsync(decimal amount, string currency, string paymentMethod, CancellationToken ct);
}
```

Create `Shared/Abstractions/IIdempotencyStore.cs`:

```csharp
namespace Api.Shared.Abstractions;

public interface IIdempotencyStore
{
    Task<Guid?> GetOrderIdAsync(string idempotencyKey, CancellationToken ct);
    Task StoreOrderIdAsync(string idempotencyKey, Guid orderId, CancellationToken ct);
}
```

Create `Shared/Abstractions/IOrderRepository.cs`:

```csharp
namespace Api.Shared.Abstractions;

public interface IOrderRepository
{
    Task<Guid> CreateAsync(Guid customerId, Guid productId, int quantity, decimal total, string currency, CancellationToken ct);
}
```

Create `Features/Orders/CreateOrder/CreateOrderRequest.cs`:

```csharp
using MediatR;

namespace Api.Features.Orders.CreateOrder;

public sealed record CreateOrderRequest(
    Guid CustomerId,
    Guid ProductId,
    int Quantity,
    decimal Total,
    string Currency,
    string PaymentMethod,
    string IdempotencyKey
) : IRequest<CreateOrderResponse>;
```

Create `Features/Orders/CreateOrder/CreateOrderResponse.cs`:

```csharp
namespace Api.Features.Orders.CreateOrder;

public sealed record CreateOrderResponse(Guid OrderId);
```

### Step 9: In-memory adapters for training

Create `Shared/Adapters/FakePaymentGateway.cs`:

```csharp
using Api.Shared.Abstractions;

namespace Api.Shared.Adapters;

public sealed class FakePaymentGateway : IPaymentGateway
{
    public Task ChargeAsync(decimal amount, string currency, string paymentMethod, CancellationToken ct)
    {
        // Training stand-in:
        // In production, you'd set timeouts, use retries where safe, and map gateway errors.
        return Task.CompletedTask;
    }
}
```

Create `Shared/Adapters/InMemoryIdempotencyStore.cs`:

```csharp
using Api.Shared.Abstractions;

namespace Api.Shared.Adapters;

public sealed class InMemoryIdempotencyStore : IIdempotencyStore
{
    private readonly Dictionary<string, Guid> _store = new(StringComparer.OrdinalIgnoreCase);

    public Task<Guid?> GetOrderIdAsync(string idempotencyKey, CancellationToken ct)
    {
        if (_store.TryGetValue(idempotencyKey, out var id))
            return Task.FromResult<Guid?>(id);

        return Task.FromResult<Guid?>(null);
    }

    public Task StoreOrderIdAsync(string idempotencyKey, Guid orderId, CancellationToken ct)
    {
        _store[idempotencyKey] = orderId;
        return Task.CompletedTask;
    }
}
```

Create `Shared/Adapters/InMemoryOrderRepository.cs`:

```csharp
using Api.Shared.Abstractions;

namespace Api.Shared.Adapters;

public sealed class InMemoryOrderRepository : IOrderRepository
{
    public Task<Guid> CreateAsync(Guid customerId, Guid productId, int quantity, decimal total, string currency, CancellationToken ct)
        => Task.FromResult(Guid.NewGuid());
}
```

### Step 10: Handler with idempotency (the slice’s production logic)

Create `Features/Orders/CreateOrder/CreateOrderHandler.cs`:

```csharp
using Api.Features.Orders.CreateOrder;
using Api.Shared.Abstractions;
using MediatR;

namespace Api.Features.Orders.CreateOrder;

public sealed class CreateOrderHandler : IRequestHandler<CreateOrderRequest, CreateOrderResponse>
{
    private readonly IOrderRepository _orders;
    private readonly IPaymentGateway _payments;
    private readonly IIdempotencyStore _idempotency;

    public CreateOrderHandler(
        IOrderRepository orders,
        IPaymentGateway payments,
        IIdempotencyStore idempotency)
    {
        _orders = orders;
        _payments = payments;
        _idempotency = idempotency;
    }

    public async Task<CreateOrderResponse> Handle(CreateOrderRequest request, CancellationToken cancellationToken)
    {
        // Idempotency: if we've already processed this request, return the same result.
        var existingOrderId = await _idempotency.GetOrderIdAsync(request.IdempotencyKey, cancellationToken);
        if (existingOrderId is not null)
            return new CreateOrderResponse(existingOrderId.Value);

        // Production note:
        // A real system would also ensure consistency between:
        // 1) payment side effects
        // 2) database writes
        // Often via outbox/inbox or provider-specific idempotency.
        await _payments.ChargeAsync(request.Total, request.Currency, request.PaymentMethod, cancellationToken);

        var orderId = await _orders.CreateAsync(
            request.CustomerId,
            request.ProductId,
            request.Quantity,
            request.Total,
            request.Currency,
            cancellationToken);

        await _idempotency.StoreOrderIdAsync(request.IdempotencyKey, orderId, cancellationToken);
        return new CreateOrderResponse(orderId);
    }
}
```

### Step 11: Validator

Create `Features/Orders/CreateOrder/CreateOrderValidator.cs`:

```csharp
using FluentValidation;

namespace Api.Features.Orders.CreateOrder;

public sealed class CreateOrderValidator : AbstractValidator<CreateOrderRequest>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.CustomerId).NotEqual(Guid.Empty);
        RuleFor(x => x.ProductId).NotEqual(Guid.Empty);
        RuleFor(x => x.Quantity).GreaterThan(0);
        RuleFor(x => x.Total).GreaterThan(0m);
        RuleFor(x => x.Currency).NotEmpty().Length(3);
        RuleFor(x => x.PaymentMethod).NotEmpty();
        RuleFor(x => x.IdempotencyKey).NotEmpty();
    }
}
```

### Step 12: Endpoint/controller for the slice

Create `Features/Orders/CreateOrder/CreateOrderEndpoint.cs`:

```csharp
using Api.Features.Orders.CreateOrder;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Api.Features.Orders.CreateOrder;

[ApiController]
public sealed class CreateOrderEndpoint : ControllerBase
{
    private readonly IMediator _mediator;

    public CreateOrderEndpoint(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpPost("api/orders")]
    public async Task<ActionResult<CreateOrderResponse>> Handle([FromBody] CreateOrderRequest request, CancellationToken ct)
    {
        var result = await _mediator.Send(request, ct);
        return Created(string.Empty, result);
    }
}
```

---

## 9) Wire MediatR, FluentValidation, and DI (Program.cs)

Open `Api/Program.cs` and ensure you have the following registrations.

### Step 13: Add DI + MediatR + validators

In `Api/Program.cs`, add/update registrations like:

```csharp
using Api.Features.Orders.CreateOrder;
using Api.Features.Products.GetById;
using Api.Shared.Abstractions;
using Api.Shared.Adapters;
using FluentValidation;
using FluentValidation.AspNetCore;
using MediatR;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssemblyContaining<GetProductByIdHandler>();
    cfg.RegisterServicesFromAssemblyContaining<CreateOrderHandler>();
});

builder.Services.AddValidatorsFromAssemblyContaining<GetProductByIdValidator>();
builder.Services.AddValidatorsFromAssemblyContaining<CreateOrderValidator>();
builder.Services.AddFluentValidationAutoValidation();

builder.Services.AddScoped<IProductRepository, InMemoryProductRepository>();
builder.Services.AddScoped<IOrderRepository, InMemoryOrderRepository>();
builder.Services.AddScoped<IPaymentGateway, FakePaymentGateway>();
builder.Services.AddScoped<IIdempotencyStore, InMemoryIdempotencyStore>();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();
```

Done when:
- the app starts and Swagger shows both endpoints.

---

## 10) Run and test

### Step 14: Run

```sh
cd Api
dotnet run
```

### Step 15: Test GET /products

```sh
curl -v http://localhost:5000/api/products/11111111-1111-1111-1111-111111111111
```

Expected:
- `200 OK` with JSON product
- unknown id => `404`

### Step 16: Test POST /orders (includes idempotency)

```sh
curl -v -X POST http://localhost:5000/api/orders ^
  -H "Content-Type: application/json" ^
  -d '{
    "customerId":"33333333-3333-3333-3333-333333333333",
    "productId":"11111111-1111-1111-1111-111111111111",
    "quantity":2,
    "total":99.98,
    "currency":"USD",
    "paymentMethod":"card_123",
    "idempotencyKey":"req_0001"
  }'
```

Expected:
- `201 Created`
- response body includes `orderId`

Repeat the same POST with the same `idempotencyKey`.
Expected:
- you should get the same `orderId` again.

---

## 11) Senior-architect checklist (Vertical Slice review)

Use this when you review your own slices:

- Each slice folder answers: “What request does this feature serve and how does it behave?”
- Endpoints are thin; handlers contain rules.
- External systems (DB, payments) are abstracted behind slice-adjacent interfaces.
- Write slices implement idempotency (at least in the design, even if initially in-memory).
- Error handling is consistent (same shape + status codes for similar failures).
- Observability hooks exist per slice (log context includes correlation/idempotency keys).

---

## 12) Vertical Slice Architecture vs Onion Architecture

Both aim to isolate complexity and keep business logic maintainable, but they optimize for different organizing principles.

### Vertical Slice Architecture
- Organizes code by **use case / feature**.
- A slice is “vertical”: endpoint + request/handler + adapters for that specific behavior.
- Developer experience: open one slice folder and understand the feature end-to-end.

### Onion Architecture
- Organizes code by **dependency direction** and rings around the domain.
- The domain/application core sits at the center; dependencies point inward.
- Developer experience: you can reason about safety and framework leakage by looking at layers/rings.

### Practical difference (the mental model)
- With Vertical Slice, the unit of organization is the request/feature.
- With Onion, the unit of organization is dependency safety around the domain.

### Can you combine them?
Yes. Many teams use Vertical Slice for feature organization, while still applying Onion-like dependency rules inside each slice (domain stays framework-agnostic; infrastructure depends inward via interfaces).

