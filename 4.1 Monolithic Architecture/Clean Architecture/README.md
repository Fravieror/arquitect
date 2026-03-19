# Clean Architecture for C# – Senior Software Architect Training

Welcome! This guide is designed for learners with attention deficit, focusing on clarity, actionable steps, and real-world production examples. You’ll learn Clean Architecture in C# by following hands-on instructions. **No code files are created for you – you’ll type and run everything yourself.**

---

## What is Clean Architecture?

Clean Architecture is a way to organize code so that:
- Business logic is independent of frameworks, UI, and databases.
- Code is easy to test, maintain, and extend.
- Dependencies point inwards (from outer layers to inner core).

**Layers:**
- **Domain/Core:** Business rules (Entities, Use Cases)
- **Application:** Application logic (Use Case orchestration)
- **Infrastructure:** External concerns (DB, APIs, File I/O)
- **Presentation:** UI, Web API, etc.

---

## 1. Folder Structure (Create this yourself)

```
/YourProject
  /Core
    - Entities/
    - Interfaces/
    - UseCases/
  /Application
    - Services/
  /Infrastructure
    - Data/
    - ExternalServices/
  /WebApi
    - Controllers/
```

---

## 2. Step-by-Step: Build a Real-World Example

We’ll build a simple **Order Management** system.

### 2.1. Create the Solution and Projects

Open a terminal and type:

```sh
# Create a solution and projects
mkdir CleanArchDemo
cd CleanArchDemo

dotnet new sln -n CleanArchDemo

dotnet new classlib -n Core

dotnet new classlib -n Application

dotnet new classlib -n Infrastructure

dotnet new webapi -n WebApi

# Add projects to solution

dotnet sln add Core/Application/Infrastructure/WebApi

# Add references

dotnet add Application reference Core

dotnet add Infrastructure reference Application Core

dotnet add WebApi reference Application Infrastructure Core
```

---

### 2.2. Define the Domain (Core)

**File:** Core/Entities/Order.cs

```csharp
namespace Core.Entities
{
    public class Order
    {
        public int Id { get; set; }
        public string Customer { get; set; }
        public decimal Total { get; set; }
    }
}
```

---

### 2.3. Define Repository Interface (Core)

**File:** Core/Interfaces/IOrderRepository.cs

```csharp
using System.Collections.Generic;
using Core.Entities;

namespace Core.Interfaces
{
    public interface IOrderRepository
    {
        IEnumerable<Order> GetAll();
        Order GetById(int id);
        void Add(Order order);
    }
}
```

---

### 2.4. Implement Use Case (Application)

**File:** Application/UseCases/GetOrdersUseCase.cs

```csharp
using Core.Entities;
using Core.Interfaces;
using System.Collections.Generic;

namespace Application.UseCases
{
    public class GetOrdersUseCase
    {
        private readonly IOrderRepository _repo;
        public GetOrdersUseCase(IOrderRepository repo)
        {
            _repo = repo;
        }
        public IEnumerable<Order> Execute() => _repo.GetAll();
    }
}
```

---

### 2.5. Implement Repository (Infrastructure)

**File:** Infrastructure/Data/InMemoryOrderRepository.cs

```csharp
using Core.Entities;
using Core.Interfaces;
using System.Collections.Generic;
using System.Linq;

namespace Infrastructure.Data
{
    public class InMemoryOrderRepository : IOrderRepository
    {
        private readonly List<Order> _orders = new();
        public IEnumerable<Order> GetAll() => _orders;
        public Order GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);
        public void Add(Order order) => _orders.Add(order);
    }
}
```

---

### 2.6. Wire Up in Web API (Presentation)

**File:** WebApi/Controllers/OrdersController.cs

```csharp
using Application.UseCases;
using Core.Entities;
using Core.Interfaces;
using Infrastructure.Data;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly GetOrdersUseCase _getOrders;
    private readonly IOrderRepository _repo;

    public OrdersController()
    {
        _repo = new InMemoryOrderRepository();
        _getOrders = new GetOrdersUseCase(_repo);
    }

    [HttpGet]
    public IEnumerable<Order> Get() => _getOrders.Execute();

    [HttpPost]
    public IActionResult Post(Order order)
    {
        _repo.Add(order);
        return Ok();
    }
}
```

---

## 3. Run the Example

```sh
cd WebApi

dotnet run
```

- Visit: http://localhost:5000/api/orders
- Use Postman or curl to POST new orders.

---

## 4. Real-World Production Tips

- Use Dependency Injection (built-in in ASP.NET Core)
- Replace InMemoryOrderRepository with a real DB (e.g., EF Core)
- Add validation, error handling, logging
- Write unit tests for Use Cases and Repositories
- Keep controllers thin – all logic in Use Cases

---

## 5. Further Reading
- "Clean Architecture" by Robert C. Martin
- Microsoft Docs: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures

---

**Stay focused:**
- Do one step at a time
- Type out the code yourself
- Run and test after each step
- Take breaks as needed

You’re on your way to mastering Clean Architecture in C#!

---

## Clean Architecture vs. Layered Architecture (N-Tier)

**Layered Architecture (N-Tier):**
- Organizes code into horizontal layers: Presentation, Business Logic, Data Access, etc.
- Each layer depends on the one below it (e.g., UI → Business Logic → Data Access).
- Common in traditional enterprise apps.
- **Drawback:** Business logic can become dependent on frameworks or data access details, making changes and testing harder.

**Clean Architecture:**
- Organizes code in concentric circles (core in the center, frameworks on the outside).
- Core business logic (Entities, Use Cases) has no dependencies on outer layers.
- Outer layers (UI, DB, frameworks) depend on the core, not vice versa.
- **Benefits:**
    - Business rules are isolated and testable.
    - Easy to swap out frameworks, databases, or UI without changing core logic.
    - Promotes long-term maintainability and flexibility.

**Summary Table:**

| Aspect                | Layered (N-Tier)                | Clean Architecture           |
|-----------------------|----------------------------------|------------------------------|
| Dependency Direction  | Outward (UI → DB)                | Inward (Frameworks → Core)   |
| Testability           | Harder (logic tied to layers)    | Easier (core is isolated)    |
| Flexibility           | Lower                            | Higher                       |
| Typical Use           | Legacy/Enterprise apps           | Modern, maintainable apps    |

**In Practice:**
- Clean Architecture is an evolution of Layered/N-Tier, solving its main pain points for large, long-lived systems.