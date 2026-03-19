# Onion Architecture for C# – Senior Software Architect Training

Welcome! This guide is designed for learners with attention deficit, focusing on clarity, actionable steps, and real-world production examples. You’ll learn Onion Architecture in C# by following hands-on instructions. **No code files are created for you – you’ll type and run everything yourself.**

---

## How to use this guide (ADHD-friendly)

1. Do one step at a time. When a step says “Done when…”, stop there.
2. After each step, run the app (or at least build) and test the endpoint once.
3. If you get stuck, copy the exact error message and retry only the last step you changed.

## What is Onion Architecture?

Onion Architecture is a way to structure your application so that:
- The core business logic is at the center and has no dependencies on anything else.
- All dependencies point inwards, toward the core.
- Infrastructure and frameworks are at the outermost layer.
- The application is easy to test, maintain, and extend.

**Key Concepts:**
- **Core (Domain):** Business rules, entities, value objects.
- **Application Services:** Orchestrate use cases, interact with domain.
- **Interfaces:** Contracts for external dependencies (e.g., repositories, services).
- **Infrastructure:** Implementations of interfaces (e.g., DB, APIs, UI).

---

## 1. Folder Structure (Create this yourself)

```
/YourProject
  /Domain
    - Entities/
    - ValueObjects/
  /Application
    - Services/
    - Interfaces/
  /Infrastructure
    - Data/
    - ExternalServices/
  /UI
    - Controllers/
```

---

## 2. Step-by-Step: Build a Real-World Example

We’ll build a simple **Library Management** system.

### 2.1. Create the Solution and Projects

Open a terminal and type:

```sh
# Create a solution and projects
mkdir OnionArchDemo
cd OnionArchDemo

dotnet new sln -n OnionArchDemo

dotnet new classlib -n Domain

dotnet new classlib -n Application

dotnet new classlib -n Infrastructure

dotnet new webapi -n UI

# Add projects to solution

dotnet sln add Domain/Application/Infrastructure/UI

# Add references

dotnet add Application reference Domain

dotnet add Infrastructure reference Application Domain

dotnet add UI reference Application Infrastructure Domain
```

---

### 2.2. Define the Domain (Core)

**File:** Domain/Entities/Book.cs

```csharp
namespace Domain.Entities
{
    public class Book
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Author { get; set; }
    }
}
```

---

### 2.3. Define Repository Interface (Application)

**File:** Application/Interfaces/IBookRepository.cs

```csharp
using Domain.Entities;
using System.Collections.Generic;

namespace Application.Interfaces
{
    public interface IBookRepository
    {
        IEnumerable<Book> GetAll();
        Book? GetById(int id);
        void Add(Book book);
    }
}
```

---

### 2.4. Implement Service (Application)

**File:** Application/Services/BookService.cs

```csharp
using Application.Interfaces;
using Domain.Entities;
using System.Collections.Generic;

namespace Application.Services
{
    public class BookService
    {
        private readonly IBookRepository _repo;
        public BookService(IBookRepository repo)
        {
            _repo = repo;
        }
        public IEnumerable<Book> GetAllBooks() => _repo.GetAll();
        public void AddBook(Book book) => _repo.Add(book);
        public Book? GetBookById(int id) => _repo.GetById(id);
    }
}
```

---

### 2.5. Implement Repository (Infrastructure)

**File:** Infrastructure/Data/InMemoryBookRepository.cs

```csharp
using Application.Interfaces;
using Domain.Entities;
using System.Collections.Generic;
using System.Linq;

namespace Infrastructure.Data
{
    public class InMemoryBookRepository : IBookRepository
    {
        private readonly List<Book> _books = new();
        public IEnumerable<Book> GetAll() => _books;
        public Book? GetById(int id) => _books.FirstOrDefault(b => b.Id == id);
        public void Add(Book book) => _books.Add(book);
    }
}
```

---

### 2.6. Wire Up in UI (Web API)

**File:** UI/Controllers/BooksController.cs

```csharp
using Application.Services;
using Domain.Entities;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly BookService _service;

    public BooksController(BookService service)
    {
        _service = service;
    }

    [HttpGet]
    public IEnumerable<Book> Get() => _service.GetAllBooks();

    [HttpGet("{id:int}")]
    public ActionResult<Book> GetById(int id)
    {
        var book = _service.GetBookById(id);
        if (book is null) return NotFound();
        return Ok(book);
    }

    [HttpPost]
    public IActionResult Post([FromBody] Book book)
    {
        _service.AddBook(book);
        return CreatedAtAction(nameof(GetById), new { id = book.Id }, book);
    }
}
```

---

### 2.7. Wire Up Dependency Injection (Program.cs)

Onion Architecture relies on outer layers depending on interfaces. With ASP.NET Core, that typically means using DI to connect:
- `Application.Interfaces.IBookRepository` (abstraction)
- `Infrastructure.Data.InMemoryBookRepository` (implementation)
- `Application.Services.BookService` (use case/service)

**File:** `UI/Program.cs`

Add registrations like this (exact location depends on your template, but they must be before `var app = builder.Build();`):

```csharp
using Application.Interfaces;
using Application.Services;
using Infrastructure.Data;

builder.Services.AddScoped<IBookRepository, InMemoryBookRepository>();
builder.Services.AddScoped<BookService>();
```

## 3. Run the Example

```sh
cd UI

dotnet run
```

- Visit: http://localhost:5000/api/books
- `GET /api/books` to list books
- `GET /api/books/{id}` to fetch one book
- `POST /api/books` to add a book (send JSON body)

---

## 4. Real-World Production Tips

- Use Dependency Injection (built-in in ASP.NET Core)
- Replace `InMemoryBookRepository` with a real DB (e.g., EF Core) inside `Infrastructure/Data/`
- Keep your `Domain` (Entities/ValueObjects) free of EF/Core attributes and framework types
- Add validation in the Application layer (use cases should reject invalid input early)
- Map domain/application errors to consistent HTTP responses (e.g., 404, 409, 400)
- Write unit tests for `Application.Services` (use the repository interface with fakes/mocks)
- When you later add “side effects” (emails, payments, message publishing), push those to Infrastructure adapters and keep the domain rules in the center

---

## 5. Further Reading
- "Onion Architecture" by Jeffrey Palermo
- Microsoft Docs: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures

---

**Stay focused:**
- Do one step at a time
- Type out the code yourself
- Run and test after each step
- Take breaks as needed

You’re on your way to mastering Onion Architecture in C#!

---

## Onion Architecture vs. Hexagonal Architecture (Ports & Adapters)

Both architectures try to protect business logic from framework/infrastructure churn, but they emphasize different organizing concepts.

| Aspect                | Onion Architecture | Hexagonal Architecture (Ports & Adapters) |
|-----------------------|-------------------|--------------------------------------------|
| Primary organizing axis | Dependency direction (outer -> inner) around the domain | Explicit ports/adapters for each interaction |
| Mental model          | “Keep the core safe” | “Route everything through ports” |
| What becomes explicit | Interfaces/boundaries through dependency rules (often implicit) | Ports are first-class concepts; adapters implement them |
| Structure             | Concentric rings (domain in the center) | Core + Ports + Adapters |
| Developer navigation  | Find the safest core path by layers/rings | Find the use case path by port/adapters |
| Typical sweet spot   | Business-logic-heavy apps where domain safety matters | Integration-heavy apps where you swap adapters frequently |

### Production check: what should you be able to prove?

- **Onion:** framework-specific code (MVC/EF annotations, etc.) does not “leak” into Domain, and dependencies still point inward even as the app grows.
- **Hex:** every external interaction has a port, so you can test the application core with alternative adapters (in-memory, mocks, test doubles).

**In practice:** they overlap heavily. A good C# implementation often uses *feature/use-case boundaries* (vertical-ish structure) while still enforcing *onion-style dependency direction* and *hex-style ports for external systems*.

---

## Onion Architecture vs. Vertical Slice Architecture

**Vertical Slice Architecture** organizes code by **use case / feature** (each “slice” is end-to-end for one request).

**Onion Architecture** organizes code by **dependency direction and rings around the domain** (the center contains core logic; outer rings depend inward).

Quick mental model:
- Vertical Slice: “Where is the logic for this feature end-to-end?”
- Onion: “Is my domain core safe from framework/infrastructure dependencies?”

How to combine them in real systems:
- Use Vertical Slices to organize feature folders.
- Apply Onion-style dependency rules *inside each slice* so business/domain rules stay framework-free.
