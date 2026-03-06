# Layered Architecture (N-Tier)

A foundational architectural pattern that organizes code into horizontal layers, each with a specific responsibility. Essential knowledge for any senior software architect.

---

## Core Concepts

### What is Layered Architecture?

Layered Architecture separates an application into **distinct horizontal layers**, where each layer:
- Has a **single responsibility**
- **Only depends on layers below it** (never above)
- **Communicates through well-defined interfaces**

### The Classic 3-Tier/4-Tier Model

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │  ← UI, Controllers, Views
│         (User Interface)                │
├─────────────────────────────────────────┤
│         APPLICATION LAYER               │  ← Use Cases, Orchestration
│         (Business Logic / Services)     │     (Optional in 3-tier)
├─────────────────────────────────────────┤
│         DOMAIN LAYER                    │  ← Business Rules, Entities
│         (Business Rules)                │
├─────────────────────────────────────────┤
│         DATA ACCESS LAYER               │  ← Repositories, Database
│         (Persistence)                   │
└─────────────────────────────────────────┘
```

### Key Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Each layer handles one aspect of the application |
| **Dependency Rule** | Layers only depend on layers below them |
| **Abstraction** | Upper layers don't know implementation details of lower layers |
| **Testability** | Each layer can be tested in isolation |
| **Replaceability** | Layers can be swapped without affecting others |

### When to Use

✅ **Good for:**
- Traditional business applications
- CRUD-heavy systems
- Teams new to architecture patterns
- Applications with clear functional boundaries
- Monolithic applications

❌ **Avoid when:**
- Building microservices (use other patterns)
- High-performance, low-latency requirements
- Very simple applications (overkill)

---

## C# Implementation (.NET)

### Project Structure

```
LayeredArchitecture/
├── LayeredArchitecture.sln
├── src/
│   ├── Presentation/
│   │   └── LayeredArchitecture.API/
│   │       ├── Controllers/
│   │       │   └── ProductController.cs
│   │       ├── DTOs/
│   │       │   └── ProductDto.cs
│   │       └── Program.cs
│   ├── Application/
│   │   └── LayeredArchitecture.Application/
│   │       ├── Interfaces/
│   │       │   └── IProductService.cs
│   │       └── Services/
│   │           └── ProductService.cs
│   ├── Domain/
│   │   └── LayeredArchitecture.Domain/
│   │       ├── Entities/
│   │       │   └── Product.cs
│   │       └── Interfaces/
│   │           └── IProductRepository.cs
│   └── Infrastructure/
│       └── LayeredArchitecture.Infrastructure/
│           └── Repositories/
│               └── ProductRepository.cs
```

### Commands to Run

```powershell
# Create solution and projects
mkdir csharp
cd csharp

dotnet new sln -n LayeredArchitecture

# Create projects for each layer
dotnet new webapi -n LayeredArchitecture.API -o src/Presentation/LayeredArchitecture.API
dotnet new classlib -n LayeredArchitecture.Application -o src/Application/LayeredArchitecture.Application
dotnet new classlib -n LayeredArchitecture.Domain -o src/Domain/LayeredArchitecture.Domain
dotnet new classlib -n LayeredArchitecture.Infrastructure -o src/Infrastructure/LayeredArchitecture.Infrastructure

# Add projects to solution
dotnet sln add src/Presentation/LayeredArchitecture.API
dotnet sln add src/Application/LayeredArchitecture.Application
dotnet sln add src/Domain/LayeredArchitecture.Domain
dotnet sln add src/Infrastructure/LayeredArchitecture.Infrastructure

# Set up layer dependencies (respecting dependency rule)
cd src/Presentation/LayeredArchitecture.API
dotnet add reference ../../Application/LayeredArchitecture.Application
dotnet add reference ../../Infrastructure/LayeredArchitecture.Infrastructure

cd ../../Application/LayeredArchitecture.Application
dotnet add reference ../../Domain/LayeredArchitecture.Domain

cd ../../Infrastructure/LayeredArchitecture.Infrastructure
dotnet add reference ../../Domain/LayeredArchitecture.Domain

cd ../../../../
```

### Code to Type

**1. Domain Layer - `src/Domain/LayeredArchitecture.Domain/Entities/Product.cs`**

```csharp
namespace LayeredArchitecture.Domain.Entities;

// Domain Entity - Pure business object, no dependencies
public class Product
{
    public Guid Id { get; private set; }
    public string Name { get; private set; }
    public decimal Price { get; private set; }
    public int StockQuantity { get; private set; }
    public DateTime CreatedAt { get; private set; }

    // Private constructor for EF Core
    private Product() { }

    public Product(string name, decimal price, int stockQuantity)
    {
        Id = Guid.NewGuid();
        SetName(name);
        SetPrice(price);
        StockQuantity = stockQuantity;
        CreatedAt = DateTime.UtcNow;
    }

    // Business rules encapsulated in the entity
    public void SetName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Product name cannot be empty", nameof(name));
        
        if (name.Length > 100)
            throw new ArgumentException("Product name cannot exceed 100 characters", nameof(name));
        
        Name = name;
    }

    public void SetPrice(decimal price)
    {
        if (price < 0)
            throw new ArgumentException("Price cannot be negative", nameof(price));
        
        Price = price;
    }

    public void AddStock(int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Quantity must be positive", nameof(quantity));
        
        StockQuantity += quantity;
    }

    public void RemoveStock(int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Quantity must be positive", nameof(quantity));
        
        if (quantity > StockQuantity)
            throw new InvalidOperationException("Insufficient stock");
        
        StockQuantity -= quantity;
    }

    public bool IsInStock() => StockQuantity > 0;
}
```

**2. Domain Layer - `src/Domain/LayeredArchitecture.Domain/Interfaces/IProductRepository.cs`**

```csharp
namespace LayeredArchitecture.Domain.Interfaces;

using LayeredArchitecture.Domain.Entities;

// Repository interface defined in Domain layer
// Implementation will be in Infrastructure layer
public interface IProductRepository
{
    Task<Product?> GetByIdAsync(Guid id);
    Task<IEnumerable<Product>> GetAllAsync();
    Task<Product> AddAsync(Product product);
    Task UpdateAsync(Product product);
    Task DeleteAsync(Guid id);
    Task<IEnumerable<Product>> GetInStockAsync();
}
```

**3. Application Layer - `src/Application/LayeredArchitecture.Application/Interfaces/IProductService.cs`**

```csharp
namespace LayeredArchitecture.Application.Interfaces;

using LayeredArchitecture.Domain.Entities;

// Application service interface - orchestrates use cases
public interface IProductService
{
    Task<Product?> GetProductByIdAsync(Guid id);
    Task<IEnumerable<Product>> GetAllProductsAsync();
    Task<Product> CreateProductAsync(string name, decimal price, int stockQuantity);
    Task UpdateProductAsync(Guid id, string name, decimal price);
    Task DeleteProductAsync(Guid id);
    Task AddStockAsync(Guid id, int quantity);
    Task<bool> PurchaseProductAsync(Guid id, int quantity);
}
```

**4. Application Layer - `src/Application/LayeredArchitecture.Application/Services/ProductService.cs`**

```csharp
namespace LayeredArchitecture.Application.Services;

using LayeredArchitecture.Application.Interfaces;
using LayeredArchitecture.Domain.Entities;
using LayeredArchitecture.Domain.Interfaces;

// Application Service - Orchestrates use cases
// Contains NO business logic, only coordination
public class ProductService : IProductService
{
    private readonly IProductRepository _repository;

    public ProductService(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<Product?> GetProductByIdAsync(Guid id)
    {
        return await _repository.GetByIdAsync(id);
    }

    public async Task<IEnumerable<Product>> GetAllProductsAsync()
    {
        return await _repository.GetAllAsync();
    }

    public async Task<Product> CreateProductAsync(string name, decimal price, int stockQuantity)
    {
        // Business validation happens in Product constructor
        var product = new Product(name, price, stockQuantity);
        return await _repository.AddAsync(product);
    }

    public async Task UpdateProductAsync(Guid id, string name, decimal price)
    {
        var product = await _repository.GetByIdAsync(id)
            ?? throw new KeyNotFoundException($"Product {id} not found");

        // Business rules are in the entity
        product.SetName(name);
        product.SetPrice(price);

        await _repository.UpdateAsync(product);
    }

    public async Task DeleteProductAsync(Guid id)
    {
        var product = await _repository.GetByIdAsync(id)
            ?? throw new KeyNotFoundException($"Product {id} not found");

        await _repository.DeleteAsync(id);
    }

    public async Task AddStockAsync(Guid id, int quantity)
    {
        var product = await _repository.GetByIdAsync(id)
            ?? throw new KeyNotFoundException($"Product {id} not found");

        product.AddStock(quantity);
        await _repository.UpdateAsync(product);
    }

    public async Task<bool> PurchaseProductAsync(Guid id, int quantity)
    {
        var product = await _repository.GetByIdAsync(id)
            ?? throw new KeyNotFoundException($"Product {id} not found");

        if (!product.IsInStock())
            return false;

        try
        {
            product.RemoveStock(quantity);
            await _repository.UpdateAsync(product);
            return true;
        }
        catch (InvalidOperationException)
        {
            return false; // Insufficient stock
        }
    }
}
```

**5. Infrastructure Layer - `src/Infrastructure/LayeredArchitecture.Infrastructure/Repositories/ProductRepository.cs`**

```csharp
namespace LayeredArchitecture.Infrastructure.Repositories;

using LayeredArchitecture.Domain.Entities;
using LayeredArchitecture.Domain.Interfaces;

// Infrastructure implementation of repository
// In production, this would use EF Core or another ORM
public class ProductRepository : IProductRepository
{
    // In-memory storage for demo (use DbContext in production)
    private static readonly Dictionary<Guid, Product> _products = new();

    public Task<Product?> GetByIdAsync(Guid id)
    {
        _products.TryGetValue(id, out var product);
        return Task.FromResult(product);
    }

    public Task<IEnumerable<Product>> GetAllAsync()
    {
        return Task.FromResult<IEnumerable<Product>>(_products.Values.ToList());
    }

    public Task<Product> AddAsync(Product product)
    {
        _products[product.Id] = product;
        return Task.FromResult(product);
    }

    public Task UpdateAsync(Product product)
    {
        _products[product.Id] = product;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Guid id)
    {
        _products.Remove(id);
        return Task.CompletedTask;
    }

    public Task<IEnumerable<Product>> GetInStockAsync()
    {
        var inStock = _products.Values.Where(p => p.IsInStock()).ToList();
        return Task.FromResult<IEnumerable<Product>>(inStock);
    }
}
```

**6. Presentation Layer - `src/Presentation/LayeredArchitecture.API/DTOs/ProductDto.cs`**

```csharp
namespace LayeredArchitecture.API.DTOs;

// DTOs for API - separate from domain entities
public record ProductDto(
    Guid Id,
    string Name,
    decimal Price,
    int StockQuantity,
    bool IsInStock
);

public record CreateProductRequest(
    string Name,
    decimal Price,
    int StockQuantity
);

public record UpdateProductRequest(
    string Name,
    decimal Price
);

public record AddStockRequest(int Quantity);

public record PurchaseRequest(int Quantity);
```

**7. Presentation Layer - `src/Presentation/LayeredArchitecture.API/Controllers/ProductController.cs`**

```csharp
namespace LayeredArchitecture.API.Controllers;

using Microsoft.AspNetCore.Mvc;
using LayeredArchitecture.API.DTOs;
using LayeredArchitecture.Application.Interfaces;

[ApiController]
[Route("api/[controller]")]
public class ProductController : ControllerBase
{
    private readonly IProductService _productService;

    public ProductController(IProductService productService)
    {
        _productService = productService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll()
    {
        var products = await _productService.GetAllProductsAsync();
        var dtos = products.Select(p => new ProductDto(
            p.Id, p.Name, p.Price, p.StockQuantity, p.IsInStock()
        ));
        return Ok(dtos);
    }

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ProductDto>> GetById(Guid id)
    {
        var product = await _productService.GetProductByIdAsync(id);
        if (product == null)
            return NotFound();

        return Ok(new ProductDto(
            product.Id, product.Name, product.Price,
            product.StockQuantity, product.IsInStock()
        ));
    }

    [HttpPost]
    public async Task<ActionResult<ProductDto>> Create([FromBody] CreateProductRequest request)
    {
        try
        {
            var product = await _productService.CreateProductAsync(
                request.Name, request.Price, request.StockQuantity
            );

            var dto = new ProductDto(
                product.Id, product.Name, product.Price,
                product.StockQuantity, product.IsInStock()
            );

            return CreatedAtAction(nameof(GetById), new { id = product.Id }, dto);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPut("{id:guid}")]
    public async Task<ActionResult> Update(Guid id, [FromBody] UpdateProductRequest request)
    {
        try
        {
            await _productService.UpdateProductAsync(id, request.Name, request.Price);
            return NoContent();
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpDelete("{id:guid}")]
    public async Task<ActionResult> Delete(Guid id)
    {
        try
        {
            await _productService.DeleteProductAsync(id);
            return NoContent();
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
    }

    [HttpPost("{id:guid}/stock")]
    public async Task<ActionResult> AddStock(Guid id, [FromBody] AddStockRequest request)
    {
        try
        {
            await _productService.AddStockAsync(id, request.Quantity);
            return Ok();
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPost("{id:guid}/purchase")]
    public async Task<ActionResult> Purchase(Guid id, [FromBody] PurchaseRequest request)
    {
        try
        {
            var success = await _productService.PurchaseProductAsync(id, request.Quantity);
            if (!success)
                return BadRequest("Insufficient stock");

            return Ok();
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
    }
}
```

**8. Presentation Layer - `src/Presentation/LayeredArchitecture.API/Program.cs`**

```csharp
using LayeredArchitecture.Application.Interfaces;
using LayeredArchitecture.Application.Services;
using LayeredArchitecture.Domain.Interfaces;
using LayeredArchitecture.Infrastructure.Repositories;

var builder = WebApplication.CreateBuilder(args);

// Register dependencies (Dependency Injection)
// Notice: We register interfaces with their implementations
// This is where we "wire up" the layers
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<IProductService, ProductService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

### Run the Application

```powershell
cd src/Presentation/LayeredArchitecture.API
dotnet run

# Open browser: https://localhost:5001/swagger
# Or test with curl:
# curl -X POST https://localhost:5001/api/product -H "Content-Type: application/json" -d '{"name":"Laptop","price":999.99,"stockQuantity":10}'
```

---

## Go Implementation

### Project Structure

```
go_layered/
├── go.mod
├── main.go
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── product.go          # Entity
│   │   └── repository.go       # Repository interface
│   ├── application/
│   │   └── product_service.go  # Application service
│   ├── infrastructure/
│   │   └── memory_repository.go # Repository implementation
│   └── presentation/
│       ├── handlers.go         # HTTP handlers
│       └── dto.go              # Data transfer objects
```

### Commands to Run

```powershell
mkdir go_layered
cd go_layered
go mod init layered-architecture
```

### Code to Type

**1. Domain Layer - `internal/domain/product.go`**

```go
package domain

import (
	"errors"
	"time"

	"github.com/google/uuid"
)

// Product is the domain entity with business rules
type Product struct {
	ID            string
	Name          string
	Price         float64
	StockQuantity int
	CreatedAt     time.Time
}

// Domain errors
var (
	ErrEmptyName        = errors.New("product name cannot be empty")
	ErrNameTooLong      = errors.New("product name cannot exceed 100 characters")
	ErrNegativePrice    = errors.New("price cannot be negative")
	ErrNegativeQuantity = errors.New("quantity must be positive")
	ErrInsufficientStock = errors.New("insufficient stock")
)

// NewProduct creates a new product with validation
func NewProduct(name string, price float64, stockQuantity int) (*Product, error) {
	p := &Product{
		ID:            uuid.New().String(),
		StockQuantity: stockQuantity,
		CreatedAt:     time.Now().UTC(),
	}

	if err := p.SetName(name); err != nil {
		return nil, err
	}

	if err := p.SetPrice(price); err != nil {
		return nil, err
	}

	return p, nil
}

// SetName validates and sets the product name
func (p *Product) SetName(name string) error {
	if name == "" {
		return ErrEmptyName
	}
	if len(name) > 100 {
		return ErrNameTooLong
	}
	p.Name = name
	return nil
}

// SetPrice validates and sets the product price
func (p *Product) SetPrice(price float64) error {
	if price < 0 {
		return ErrNegativePrice
	}
	p.Price = price
	return nil
}

// AddStock adds to the stock quantity
func (p *Product) AddStock(quantity int) error {
	if quantity <= 0 {
		return ErrNegativeQuantity
	}
	p.StockQuantity += quantity
	return nil
}

// RemoveStock removes from stock with validation
func (p *Product) RemoveStock(quantity int) error {
	if quantity <= 0 {
		return ErrNegativeQuantity
	}
	if quantity > p.StockQuantity {
		return ErrInsufficientStock
	}
	p.StockQuantity -= quantity
	return nil
}

// IsInStock checks if product has stock
func (p *Product) IsInStock() bool {
	return p.StockQuantity > 0
}
```

**2. Domain Layer - `internal/domain/repository.go`**

```go
package domain

import "context"

// ProductRepository defines the contract for product persistence
// Defined in domain, implemented in infrastructure
type ProductRepository interface {
	GetByID(ctx context.Context, id string) (*Product, error)
	GetAll(ctx context.Context) ([]*Product, error)
	Add(ctx context.Context, product *Product) error
	Update(ctx context.Context, product *Product) error
	Delete(ctx context.Context, id string) error
}
```

**3. Application Layer - `internal/application/product_service.go`**

```go
package application

import (
	"context"
	"errors"

	"layered-architecture/internal/domain"
)

var ErrProductNotFound = errors.New("product not found")

// ProductService orchestrates product use cases
type ProductService struct {
	repo domain.ProductRepository
}

// NewProductService creates a new product service
func NewProductService(repo domain.ProductRepository) *ProductService {
	return &ProductService{repo: repo}
}

// GetProduct retrieves a product by ID
func (s *ProductService) GetProduct(ctx context.Context, id string) (*domain.Product, error) {
	return s.repo.GetByID(ctx, id)
}

// GetAllProducts retrieves all products
func (s *ProductService) GetAllProducts(ctx context.Context) ([]*domain.Product, error) {
	return s.repo.GetAll(ctx)
}

// CreateProduct creates a new product
func (s *ProductService) CreateProduct(ctx context.Context, name string, price float64, stock int) (*domain.Product, error) {
	product, err := domain.NewProduct(name, price, stock)
	if err != nil {
		return nil, err
	}

	if err := s.repo.Add(ctx, product); err != nil {
		return nil, err
	}

	return product, nil
}

// UpdateProduct updates an existing product
func (s *ProductService) UpdateProduct(ctx context.Context, id, name string, price float64) error {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if product == nil {
		return ErrProductNotFound
	}

	if err := product.SetName(name); err != nil {
		return err
	}
	if err := product.SetPrice(price); err != nil {
		return err
	}

	return s.repo.Update(ctx, product)
}

// DeleteProduct removes a product
func (s *ProductService) DeleteProduct(ctx context.Context, id string) error {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if product == nil {
		return ErrProductNotFound
	}

	return s.repo.Delete(ctx, id)
}

// AddStock adds stock to a product
func (s *ProductService) AddStock(ctx context.Context, id string, quantity int) error {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if product == nil {
		return ErrProductNotFound
	}

	if err := product.AddStock(quantity); err != nil {
		return err
	}

	return s.repo.Update(ctx, product)
}

// PurchaseProduct attempts to purchase a quantity
func (s *ProductService) PurchaseProduct(ctx context.Context, id string, quantity int) error {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if product == nil {
		return ErrProductNotFound
	}

	if err := product.RemoveStock(quantity); err != nil {
		return err
	}

	return s.repo.Update(ctx, product)
}
```

**4. Infrastructure Layer - `internal/infrastructure/memory_repository.go`**

```go
package infrastructure

import (
	"context"
	"sync"

	"layered-architecture/internal/domain"
)

// MemoryProductRepository is an in-memory implementation
type MemoryProductRepository struct {
	mu       sync.RWMutex
	products map[string]*domain.Product
}

// NewMemoryProductRepository creates a new in-memory repository
func NewMemoryProductRepository() *MemoryProductRepository {
	return &MemoryProductRepository{
		products: make(map[string]*domain.Product),
	}
}

func (r *MemoryProductRepository) GetByID(ctx context.Context, id string) (*domain.Product, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return r.products[id], nil
}

func (r *MemoryProductRepository) GetAll(ctx context.Context) ([]*domain.Product, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	products := make([]*domain.Product, 0, len(r.products))
	for _, p := range r.products {
		products = append(products, p)
	}
	return products, nil
}

func (r *MemoryProductRepository) Add(ctx context.Context, product *domain.Product) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.products[product.ID] = product
	return nil
}

func (r *MemoryProductRepository) Update(ctx context.Context, product *domain.Product) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.products[product.ID] = product
	return nil
}

func (r *MemoryProductRepository) Delete(ctx context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	delete(r.products, id)
	return nil
}
```

**5. Presentation Layer - `internal/presentation/dto.go`**

```go
package presentation

// ProductDTO is the API response model
type ProductDTO struct {
	ID            string  `json:"id"`
	Name          string  `json:"name"`
	Price         float64 `json:"price"`
	StockQuantity int     `json:"stockQuantity"`
	IsInStock     bool    `json:"isInStock"`
}

// CreateProductRequest is the request body for creating a product
type CreateProductRequest struct {
	Name          string  `json:"name"`
	Price         float64 `json:"price"`
	StockQuantity int     `json:"stockQuantity"`
}

// UpdateProductRequest is the request body for updating a product
type UpdateProductRequest struct {
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

// StockRequest is the request body for stock operations
type StockRequest struct {
	Quantity int `json:"quantity"`
}
```

**6. Presentation Layer - `internal/presentation/handlers.go`**

```go
package presentation

import (
	"encoding/json"
	"net/http"

	"layered-architecture/internal/application"
	"layered-architecture/internal/domain"
)

// ProductHandler handles HTTP requests for products
type ProductHandler struct {
	service *application.ProductService
}

// NewProductHandler creates a new product handler
func NewProductHandler(service *application.ProductService) *ProductHandler {
	return &ProductHandler{service: service}
}

// RegisterRoutes registers all product routes
func (h *ProductHandler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("GET /api/products", h.GetAll)
	mux.HandleFunc("GET /api/products/{id}", h.GetByID)
	mux.HandleFunc("POST /api/products", h.Create)
	mux.HandleFunc("PUT /api/products/{id}", h.Update)
	mux.HandleFunc("DELETE /api/products/{id}", h.Delete)
	mux.HandleFunc("POST /api/products/{id}/stock", h.AddStock)
	mux.HandleFunc("POST /api/products/{id}/purchase", h.Purchase)
}

func (h *ProductHandler) GetAll(w http.ResponseWriter, r *http.Request) {
	products, err := h.service.GetAllProducts(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	dtos := make([]ProductDTO, len(products))
	for i, p := range products {
		dtos[i] = toDTO(p)
	}

	respondJSON(w, http.StatusOK, dtos)
}

func (h *ProductHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	product, err := h.service.GetProduct(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if product == nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}

	respondJSON(w, http.StatusOK, toDTO(product))
}

func (h *ProductHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateProductRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	product, err := h.service.CreateProduct(r.Context(), req.Name, req.Price, req.StockQuantity)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	respondJSON(w, http.StatusCreated, toDTO(product))
}

func (h *ProductHandler) Update(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	var req UpdateProductRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := h.service.UpdateProduct(r.Context(), id, req.Name, req.Price); err != nil {
		if err == application.ErrProductNotFound {
			http.Error(w, "not found", http.StatusNotFound)
			return
		}
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func (h *ProductHandler) Delete(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	if err := h.service.DeleteProduct(r.Context(), id); err != nil {
		if err == application.ErrProductNotFound {
			http.Error(w, "not found", http.StatusNotFound)
			return
		}
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func (h *ProductHandler) AddStock(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	var req StockRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := h.service.AddStock(r.Context(), id, req.Quantity); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func (h *ProductHandler) Purchase(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	var req StockRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := h.service.PurchaseProduct(r.Context(), id, req.Quantity); err != nil {
		if err == domain.ErrInsufficientStock {
			http.Error(w, "insufficient stock", http.StatusBadRequest)
			return
		}
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func toDTO(p *domain.Product) ProductDTO {
	return ProductDTO{
		ID:            p.ID,
		Name:          p.Name,
		Price:         p.Price,
		StockQuantity: p.StockQuantity,
		IsInStock:     p.IsInStock(),
	}
}

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
```

**7. Main - `main.go`**

```go
package main

import (
	"fmt"
	"log"
	"net/http"

	"layered-architecture/internal/application"
	"layered-architecture/internal/infrastructure"
	"layered-architecture/internal/presentation"
)

func main() {
	// Wire up dependencies (Dependency Injection)
	// Infrastructure layer
	repo := infrastructure.NewMemoryProductRepository()

	// Application layer
	productService := application.NewProductService(repo)

	// Presentation layer
	handler := presentation.NewProductHandler(productService)

	// HTTP Server
	mux := http.NewServeMux()
	handler.RegisterRoutes(mux)

	fmt.Println("Server starting on :8080")
	fmt.Println("Endpoints:")
	fmt.Println("  GET    /api/products")
	fmt.Println("  GET    /api/products/{id}")
	fmt.Println("  POST   /api/products")
	fmt.Println("  PUT    /api/products/{id}")
	fmt.Println("  DELETE /api/products/{id}")
	fmt.Println("  POST   /api/products/{id}/stock")
	fmt.Println("  POST   /api/products/{id}/purchase")

	log.Fatal(http.ListenAndServe(":8080", mux))
}
```

### Run the Application

```powershell
# Get dependencies
go get github.com/google/uuid

# Run
go run main.go

# Test with curl:
# curl -X POST http://localhost:8080/api/products -H "Content-Type: application/json" -d '{"name":"Laptop","price":999.99,"stockQuantity":10}'
```

---

## Python Implementation

### Project Structure

```
python_layered/
├── main.py
├── requirements.txt
├── domain/
│   ├── __init__.py
│   ├── product.py              # Entity
│   └── repository.py           # Repository interface
├── application/
│   ├── __init__.py
│   └── product_service.py      # Application service
├── infrastructure/
│   ├── __init__.py
│   └── memory_repository.py    # Repository implementation
└── presentation/
    ├── __init__.py
    ├── dto.py                  # Data transfer objects
    └── routes.py               # API routes
```

### Commands to Run

```powershell
mkdir python_layered
cd python_layered
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic
```

### Code to Type

**1. Domain Layer - `domain/product.py`**

```python
"""Domain Entity - Product with business rules."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


class DomainError(Exception):
    """Base class for domain errors."""
    pass


class ValidationError(DomainError):
    """Raised when validation fails."""
    pass


class InsufficientStockError(DomainError):
    """Raised when there's not enough stock."""
    pass


@dataclass
class Product:
    """
    Product entity with encapsulated business rules.
    
    Domain entities should:
    - Contain business logic and validation
    - Be independent of frameworks
    - Not depend on infrastructure
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    price: float = 0.0
    stock_quantity: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate on creation."""
        if self.name:
            self._validate_name(self.name)
        if self.price:
            self._validate_price(self.price)
    
    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Product name cannot be empty")
        if len(name) > 100:
            raise ValidationError("Product name cannot exceed 100 characters")
    
    @staticmethod
    def _validate_price(price: float) -> None:
        if price < 0:
            raise ValidationError("Price cannot be negative")
    
    def set_name(self, name: str) -> None:
        """Set name with validation."""
        self._validate_name(name)
        self.name = name
    
    def set_price(self, price: float) -> None:
        """Set price with validation."""
        self._validate_price(price)
        self.price = price
    
    def add_stock(self, quantity: int) -> None:
        """Add stock with validation."""
        if quantity <= 0:
            raise ValidationError("Quantity must be positive")
        self.stock_quantity += quantity
    
    def remove_stock(self, quantity: int) -> None:
        """Remove stock with validation."""
        if quantity <= 0:
            raise ValidationError("Quantity must be positive")
        if quantity > self.stock_quantity:
            raise InsufficientStockError("Insufficient stock")
        self.stock_quantity -= quantity
    
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock_quantity > 0


def create_product(name: str, price: float, stock_quantity: int) -> Product:
    """Factory function to create a valid product."""
    product = Product()
    product.set_name(name)
    product.set_price(price)
    product.stock_quantity = stock_quantity
    return product
```

**2. Domain Layer - `domain/repository.py`**

```python
"""Repository interface - defined in domain, implemented in infrastructure."""
from abc import ABC, abstractmethod
from typing import List, Optional

from .product import Product


class ProductRepository(ABC):
    """
    Abstract repository for products.
    
    This is a PORT in hexagonal architecture terms.
    The interface is defined in the domain layer,
    but implementations live in infrastructure.
    """
    
    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        """Get a product by its ID."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Product]:
        """Get all products."""
        pass
    
    @abstractmethod
    async def add(self, product: Product) -> Product:
        """Add a new product."""
        pass
    
    @abstractmethod
    async def update(self, product: Product) -> None:
        """Update an existing product."""
        pass
    
    @abstractmethod
    async def delete(self, product_id: str) -> None:
        """Delete a product."""
        pass
```

**3. Domain Layer - `domain/__init__.py`**

```python
from .product import (
    Product,
    create_product,
    DomainError,
    ValidationError,
    InsufficientStockError,
)
from .repository import ProductRepository

__all__ = [
    "Product",
    "create_product",
    "ProductRepository",
    "DomainError",
    "ValidationError",
    "InsufficientStockError",
]
```

**4. Application Layer - `application/product_service.py`**

```python
"""Application Service - orchestrates use cases."""
from typing import List, Optional

from domain import Product, ProductRepository, create_product


class ProductNotFoundError(Exception):
    """Raised when a product is not found."""
    pass


class ProductService:
    """
    Application service for product operations.
    
    Application services:
    - Orchestrate use cases
    - Coordinate between domain and infrastructure
    - Contain NO business logic (that's in the domain)
    - Handle transactions (if needed)
    """
    
    def __init__(self, repository: ProductRepository):
        self._repository = repository
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID."""
        return await self._repository.get_by_id(product_id)
    
    async def get_all_products(self) -> List[Product]:
        """Get all products."""
        return await self._repository.get_all()
    
    async def create_product(
        self, name: str, price: float, stock_quantity: int
    ) -> Product:
        """Create a new product."""
        # Business validation happens in domain factory
        product = create_product(name, price, stock_quantity)
        return await self._repository.add(product)
    
    async def update_product(
        self, product_id: str, name: str, price: float
    ) -> None:
        """Update a product."""
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        # Business rules in the entity
        product.set_name(name)
        product.set_price(price)
        
        await self._repository.update(product)
    
    async def delete_product(self, product_id: str) -> None:
        """Delete a product."""
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        await self._repository.delete(product_id)
    
    async def add_stock(self, product_id: str, quantity: int) -> None:
        """Add stock to a product."""
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        product.add_stock(quantity)
        await self._repository.update(product)
    
    async def purchase_product(self, product_id: str, quantity: int) -> bool:
        """
        Attempt to purchase a product.
        Returns True if successful, False otherwise.
        """
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        # Business rule is in the entity
        product.remove_stock(quantity)
        await self._repository.update(product)
        return True
```

**5. Application Layer - `application/__init__.py`**

```python
from .product_service import ProductService, ProductNotFoundError

__all__ = ["ProductService", "ProductNotFoundError"]
```

**6. Infrastructure Layer - `infrastructure/memory_repository.py`**

```python
"""In-memory repository implementation."""
from typing import Dict, List, Optional

from domain import Product, ProductRepository


class MemoryProductRepository(ProductRepository):
    """
    In-memory implementation of ProductRepository.
    
    In production, you would have:
    - SQLAlchemyProductRepository
    - MongoProductRepository
    - etc.
    
    The application layer doesn't care which one is used.
    """
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
    
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)
    
    async def get_all(self) -> List[Product]:
        return list(self._products.values())
    
    async def add(self, product: Product) -> Product:
        self._products[product.id] = product
        return product
    
    async def update(self, product: Product) -> None:
        self._products[product.id] = product
    
    async def delete(self, product_id: str) -> None:
        self._products.pop(product_id, None)
```

**7. Infrastructure Layer - `infrastructure/__init__.py`**

```python
from .memory_repository import MemoryProductRepository

__all__ = ["MemoryProductRepository"]
```

**8. Presentation Layer - `presentation/dto.py`**

```python
"""Data Transfer Objects for the API."""
from pydantic import BaseModel, Field


class ProductDTO(BaseModel):
    """Product response model."""
    id: str
    name: str
    price: float
    stock_quantity: int
    is_in_stock: bool

    class Config:
        from_attributes = True


class CreateProductRequest(BaseModel):
    """Request model for creating a product."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)


class UpdateProductRequest(BaseModel):
    """Request model for updating a product."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)


class StockRequest(BaseModel):
    """Request model for stock operations."""
    quantity: int = Field(..., gt=0)
```

**9. Presentation Layer - `presentation/routes.py`**

```python
"""API Routes - Presentation layer."""
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from domain import ValidationError, InsufficientStockError, Product
from application import ProductService, ProductNotFoundError
from .dto import ProductDTO, CreateProductRequest, UpdateProductRequest, StockRequest


router = APIRouter(prefix="/api/products", tags=["products"])

# Dependency injection will be set up in main.py
_service: ProductService = None


def get_service() -> ProductService:
    if _service is None:
        raise RuntimeError("Service not initialized")
    return _service


def set_service(service: ProductService):
    global _service
    _service = service


def to_dto(product: Product) -> ProductDTO:
    return ProductDTO(
        id=product.id,
        name=product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
        is_in_stock=product.is_in_stock(),
    )


@router.get("", response_model=List[ProductDTO])
async def get_all_products(service: ProductService = Depends(get_service)):
    """Get all products."""
    products = await service.get_all_products()
    return [to_dto(p) for p in products]


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product(
    product_id: str, service: ProductService = Depends(get_service)
):
    """Get a product by ID."""
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return to_dto(product)


@router.post("", response_model=ProductDTO, status_code=201)
async def create_product(
    request: CreateProductRequest, service: ProductService = Depends(get_service)
):
    """Create a new product."""
    try:
        product = await service.create_product(
            request.name, request.price, request.stock_quantity
        )
        return to_dto(product)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", status_code=204)
async def update_product(
    product_id: str,
    request: UpdateProductRequest,
    service: ProductService = Depends(get_service),
):
    """Update a product."""
    try:
        await service.update_product(product_id, request.name, request.price)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str, service: ProductService = Depends(get_service)
):
    """Delete a product."""
    try:
        await service.delete_product(product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/{product_id}/stock", status_code=200)
async def add_stock(
    product_id: str,
    request: StockRequest,
    service: ProductService = Depends(get_service),
):
    """Add stock to a product."""
    try:
        await service.add_stock(product_id, request.quantity)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{product_id}/purchase", status_code=200)
async def purchase_product(
    product_id: str,
    request: StockRequest,
    service: ProductService = Depends(get_service),
):
    """Purchase a product."""
    try:
        await service.purchase_product(product_id, request.quantity)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    except InsufficientStockError:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**10. Presentation Layer - `presentation/__init__.py`**

```python
from .routes import router, set_service
from .dto import ProductDTO, CreateProductRequest, UpdateProductRequest, StockRequest

__all__ = [
    "router",
    "set_service",
    "ProductDTO",
    "CreateProductRequest",
    "UpdateProductRequest",
    "StockRequest",
]
```

**11. Main - `main.py`**

```python
"""
Main application entry point.

This is where we wire up all the layers using Dependency Injection.
"""
from fastapi import FastAPI

from application import ProductService
from infrastructure import MemoryProductRepository
from presentation import router, set_service


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Layered Architecture Demo",
        description="Product API demonstrating layered architecture in Python",
        version="1.0.0",
    )
    
    # Wire up dependencies (Dependency Injection)
    # 1. Infrastructure layer
    repository = MemoryProductRepository()
    
    # 2. Application layer (depends on infrastructure)
    service = ProductService(repository)
    
    # 3. Presentation layer (depends on application)
    set_service(service)
    app.include_router(router)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    print("Starting server on http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**12. Requirements - `requirements.txt`**

```
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
```

### Run the Application

```powershell
# Install dependencies
pip install -r requirements.txt

# Run
python main.py

# Or with uvicorn directly:
uvicorn main:app --reload

# Open browser: http://localhost:8000/docs (Swagger UI)
```

---

## React Implementation

### Project Structure

```
react_layered/
├── package.json
├── src/
│   ├── index.tsx
│   ├── App.tsx
│   ├── domain/
│   │   ├── product.ts          # Entity
│   │   └── repository.ts       # Repository interface
│   ├── application/
│   │   └── productService.ts   # Application service
│   ├── infrastructure/
│   │   └── apiRepository.ts    # Repository implementation
│   └── presentation/
│       ├── components/
│       │   ├── ProductList.tsx
│       │   ├── ProductForm.tsx
│       │   └── ProductCard.tsx
│       └── hooks/
│           └── useProducts.ts
```

### Commands to Run

```powershell
npx create-react-app react_layered --template typescript
cd react_layered
```

### Code to Type

**1. Domain Layer - `src/domain/product.ts`**

```typescript
/**
 * Domain Entity - Product with business rules
 * 
 * Domain entities should:
 * - Contain business logic and validation
 * - Be independent of frameworks (no React imports!)
 * - Not depend on infrastructure
 */

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class InsufficientStockError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'InsufficientStockError';
  }
}

export interface ProductData {
  id: string;
  name: string;
  price: number;
  stockQuantity: number;
  createdAt: Date;
}

export class Product {
  readonly id: string;
  private _name: string;
  private _price: number;
  private _stockQuantity: number;
  readonly createdAt: Date;

  constructor(data: ProductData) {
    this.id = data.id;
    this._name = data.name;
    this._price = data.price;
    this._stockQuantity = data.stockQuantity;
    this.createdAt = data.createdAt;
  }

  // Getters
  get name(): string { return this._name; }
  get price(): number { return this._price; }
  get stockQuantity(): number { return this._stockQuantity; }

  // Business rules
  setName(name: string): void {
    if (!name || name.trim() === '') {
      throw new ValidationError('Product name cannot be empty');
    }
    if (name.length > 100) {
      throw new ValidationError('Product name cannot exceed 100 characters');
    }
    this._name = name;
  }

  setPrice(price: number): void {
    if (price < 0) {
      throw new ValidationError('Price cannot be negative');
    }
    this._price = price;
  }

  addStock(quantity: number): void {
    if (quantity <= 0) {
      throw new ValidationError('Quantity must be positive');
    }
    this._stockQuantity += quantity;
  }

  removeStock(quantity: number): void {
    if (quantity <= 0) {
      throw new ValidationError('Quantity must be positive');
    }
    if (quantity > this._stockQuantity) {
      throw new InsufficientStockError('Insufficient stock');
    }
    this._stockQuantity -= quantity;
  }

  isInStock(): boolean {
    return this._stockQuantity > 0;
  }

  // Immutable update - returns new Product
  withUpdates(updates: Partial<{ name: string; price: number }>): Product {
    const newProduct = new Product({
      id: this.id,
      name: this._name,
      price: this._price,
      stockQuantity: this._stockQuantity,
      createdAt: this.createdAt,
    });

    if (updates.name !== undefined) {
      newProduct.setName(updates.name);
    }
    if (updates.price !== undefined) {
      newProduct.setPrice(updates.price);
    }

    return newProduct;
  }

  toJSON(): ProductData {
    return {
      id: this.id,
      name: this._name,
      price: this._price,
      stockQuantity: this._stockQuantity,
      createdAt: this.createdAt,
    };
  }
}

// Factory function
export function createProduct(
  name: string,
  price: number,
  stockQuantity: number
): Product {
  // Validate before creating
  if (!name || name.trim() === '') {
    throw new ValidationError('Product name cannot be empty');
  }
  if (price < 0) {
    throw new ValidationError('Price cannot be negative');
  }

  return new Product({
    id: crypto.randomUUID(),
    name,
    price,
    stockQuantity,
    createdAt: new Date(),
  });
}
```

**2. Domain Layer - `src/domain/repository.ts`**

```typescript
/**
 * Repository Interface - defined in domain, implemented in infrastructure
 */
import { Product } from './product';

export interface CreateProductInput {
  name: string;
  price: number;
  stockQuantity: number;
}

export interface UpdateProductInput {
  name: string;
  price: number;
}

export interface ProductRepository {
  getById(id: string): Promise<Product | null>;
  getAll(): Promise<Product[]>;
  add(input: CreateProductInput): Promise<Product>;
  update(id: string, input: UpdateProductInput): Promise<Product>;
  delete(id: string): Promise<void>;
  addStock(id: string, quantity: number): Promise<Product>;
  removeStock(id: string, quantity: number): Promise<Product>;
}
```

**3. Application Layer - `src/application/productService.ts`**

```typescript
/**
 * Application Service - orchestrates use cases
 * 
 * In React, this service acts as the bridge between
 * domain logic and the UI components.
 */
import { Product, createProduct, ValidationError, InsufficientStockError } from '../domain/product';
import { ProductRepository, CreateProductInput, UpdateProductInput } from '../domain/repository';

export class ProductNotFoundError extends Error {
  constructor(id: string) {
    super(`Product ${id} not found`);
    this.name = 'ProductNotFoundError';
  }
}

export class ProductService {
  constructor(private readonly repository: ProductRepository) {}

  async getProduct(id: string): Promise<Product | null> {
    return this.repository.getById(id);
  }

  async getAllProducts(): Promise<Product[]> {
    return this.repository.getAll();
  }

  async createProduct(input: CreateProductInput): Promise<Product> {
    // Validate using domain logic
    createProduct(input.name, input.price, input.stockQuantity);
    
    // Persist via repository
    return this.repository.add(input);
  }

  async updateProduct(id: string, input: UpdateProductInput): Promise<Product> {
    const product = await this.repository.getById(id);
    if (!product) {
      throw new ProductNotFoundError(id);
    }

    // Validate using domain logic
    product.setName(input.name);
    product.setPrice(input.price);

    return this.repository.update(id, input);
  }

  async deleteProduct(id: string): Promise<void> {
    const product = await this.repository.getById(id);
    if (!product) {
      throw new ProductNotFoundError(id);
    }

    return this.repository.delete(id);
  }

  async addStock(id: string, quantity: number): Promise<Product> {
    const product = await this.repository.getById(id);
    if (!product) {
      throw new ProductNotFoundError(id);
    }

    // Business validation in domain
    product.addStock(quantity);

    return this.repository.addStock(id, quantity);
  }

  async purchaseProduct(id: string, quantity: number): Promise<Product> {
    const product = await this.repository.getById(id);
    if (!product) {
      throw new ProductNotFoundError(id);
    }

    // Business validation in domain
    product.removeStock(quantity);

    return this.repository.removeStock(id, quantity);
  }
}

// Export types for convenience
export { ValidationError, InsufficientStockError };
```

**4. Infrastructure Layer - `src/infrastructure/apiRepository.ts`**

```typescript
/**
 * API Repository Implementation
 * 
 * In production, this would make real API calls.
 * For demo, we use localStorage.
 */
import { Product, ProductData } from '../domain/product';
import { ProductRepository, CreateProductInput, UpdateProductInput } from '../domain/repository';

export class LocalStorageProductRepository implements ProductRepository {
  private readonly STORAGE_KEY = 'products';

  private getProducts(): Map<string, ProductData> {
    const data = localStorage.getItem(this.STORAGE_KEY);
    if (!data) return new Map();
    
    const parsed = JSON.parse(data);
    return new Map(Object.entries(parsed).map(([id, p]: [string, any]) => [
      id,
      { ...p, createdAt: new Date(p.createdAt) }
    ]));
  }

  private saveProducts(products: Map<string, ProductData>): void {
    const obj = Object.fromEntries(products);
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(obj));
  }

  async getById(id: string): Promise<Product | null> {
    const products = this.getProducts();
    const data = products.get(id);
    return data ? new Product(data) : null;
  }

  async getAll(): Promise<Product[]> {
    const products = this.getProducts();
    return Array.from(products.values()).map(data => new Product(data));
  }

  async add(input: CreateProductInput): Promise<Product> {
    const products = this.getProducts();
    
    const data: ProductData = {
      id: crypto.randomUUID(),
      name: input.name,
      price: input.price,
      stockQuantity: input.stockQuantity,
      createdAt: new Date(),
    };

    products.set(data.id, data);
    this.saveProducts(products);

    return new Product(data);
  }

  async update(id: string, input: UpdateProductInput): Promise<Product> {
    const products = this.getProducts();
    const existing = products.get(id);
    
    if (!existing) {
      throw new Error(`Product ${id} not found`);
    }

    const updated: ProductData = {
      ...existing,
      name: input.name,
      price: input.price,
    };

    products.set(id, updated);
    this.saveProducts(products);

    return new Product(updated);
  }

  async delete(id: string): Promise<void> {
    const products = this.getProducts();
    products.delete(id);
    this.saveProducts(products);
  }

  async addStock(id: string, quantity: number): Promise<Product> {
    const products = this.getProducts();
    const existing = products.get(id);
    
    if (!existing) {
      throw new Error(`Product ${id} not found`);
    }

    const updated: ProductData = {
      ...existing,
      stockQuantity: existing.stockQuantity + quantity,
    };

    products.set(id, updated);
    this.saveProducts(products);

    return new Product(updated);
  }

  async removeStock(id: string, quantity: number): Promise<Product> {
    const products = this.getProducts();
    const existing = products.get(id);
    
    if (!existing) {
      throw new Error(`Product ${id} not found`);
    }

    const updated: ProductData = {
      ...existing,
      stockQuantity: existing.stockQuantity - quantity,
    };

    products.set(id, updated);
    this.saveProducts(products);

    return new Product(updated);
  }
}

// For API calls in production:
export class ApiProductRepository implements ProductRepository {
  constructor(private readonly baseUrl: string = '/api/products') {}

  async getById(id: string): Promise<Product | null> {
    const response = await fetch(`${this.baseUrl}/${id}`);
    if (response.status === 404) return null;
    const data = await response.json();
    return new Product({ ...data, createdAt: new Date(data.createdAt) });
  }

  async getAll(): Promise<Product[]> {
    const response = await fetch(this.baseUrl);
    const data = await response.json();
    return data.map((d: any) => new Product({ ...d, createdAt: new Date(d.createdAt) }));
  }

  async add(input: CreateProductInput): Promise<Product> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    const data = await response.json();
    return new Product({ ...data, createdAt: new Date(data.createdAt) });
  }

  async update(id: string, input: UpdateProductInput): Promise<Product> {
    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    const data = await response.json();
    return new Product({ ...data, createdAt: new Date(data.createdAt) });
  }

  async delete(id: string): Promise<void> {
    await fetch(`${this.baseUrl}/${id}`, { method: 'DELETE' });
  }

  async addStock(id: string, quantity: number): Promise<Product> {
    const response = await fetch(`${this.baseUrl}/${id}/stock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity }),
    });
    const data = await response.json();
    return new Product({ ...data, createdAt: new Date(data.createdAt) });
  }

  async removeStock(id: string, quantity: number): Promise<Product> {
    const response = await fetch(`${this.baseUrl}/${id}/purchase`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity }),
    });
    const data = await response.json();
    return new Product({ ...data, createdAt: new Date(data.createdAt) });
  }
}
```

**5. Presentation Layer - `src/presentation/hooks/useProducts.ts`**

```typescript
/**
 * Custom Hook - Presentation layer
 * 
 * Hooks are the React way to connect to services.
 * This abstracts away the service implementation from components.
 */
import { useState, useEffect, useCallback, useMemo } from 'react';
import { Product } from '../../domain/product';
import { ProductService, ValidationError, InsufficientStockError } from '../../application/productService';
import { LocalStorageProductRepository } from '../../infrastructure/apiRepository';

// Create service instance (in production, use Context/DI)
const repository = new LocalStorageProductRepository();
const productService = new ProductService(repository);

export interface UseProductsResult {
  products: Product[];
  loading: boolean;
  error: string | null;
  createProduct: (name: string, price: number, stockQuantity: number) => Promise<void>;
  updateProduct: (id: string, name: string, price: number) => Promise<void>;
  deleteProduct: (id: string) => Promise<void>;
  addStock: (id: string, quantity: number) => Promise<void>;
  purchaseProduct: (id: string, quantity: number) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useProducts(): UseProductsResult {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productService.getAllProducts();
      setProducts(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createProduct = useCallback(async (
    name: string,
    price: number,
    stockQuantity: number
  ) => {
    try {
      setError(null);
      await productService.createProduct({ name, price, stockQuantity });
      await refresh();
    } catch (e) {
      if (e instanceof ValidationError) {
        setError(e.message);
      } else {
        setError('Failed to create product');
      }
      throw e;
    }
  }, [refresh]);

  const updateProduct = useCallback(async (
    id: string,
    name: string,
    price: number
  ) => {
    try {
      setError(null);
      await productService.updateProduct(id, { name, price });
      await refresh();
    } catch (e) {
      if (e instanceof ValidationError) {
        setError(e.message);
      } else {
        setError('Failed to update product');
      }
      throw e;
    }
  }, [refresh]);

  const deleteProduct = useCallback(async (id: string) => {
    try {
      setError(null);
      await productService.deleteProduct(id);
      await refresh();
    } catch (e) {
      setError('Failed to delete product');
      throw e;
    }
  }, [refresh]);

  const addStock = useCallback(async (id: string, quantity: number) => {
    try {
      setError(null);
      await productService.addStock(id, quantity);
      await refresh();
    } catch (e) {
      if (e instanceof ValidationError) {
        setError(e.message);
      } else {
        setError('Failed to add stock');
      }
      throw e;
    }
  }, [refresh]);

  const purchaseProduct = useCallback(async (id: string, quantity: number) => {
    try {
      setError(null);
      await productService.purchaseProduct(id, quantity);
      await refresh();
    } catch (e) {
      if (e instanceof InsufficientStockError) {
        setError('Insufficient stock');
      } else if (e instanceof ValidationError) {
        setError(e.message);
      } else {
        setError('Failed to purchase');
      }
      throw e;
    }
  }, [refresh]);

  return useMemo(() => ({
    products,
    loading,
    error,
    createProduct,
    updateProduct,
    deleteProduct,
    addStock,
    purchaseProduct,
    refresh,
  }), [products, loading, error, createProduct, updateProduct, deleteProduct, addStock, purchaseProduct, refresh]);
}
```

**6. Presentation Layer - `src/presentation/components/ProductCard.tsx`**

```tsx
/**
 * ProductCard Component - Pure presentation
 */
import React, { useState } from 'react';
import { Product } from '../../domain/product';

interface ProductCardProps {
  product: Product;
  onUpdate: (id: string, name: string, price: number) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onAddStock: (id: string, quantity: number) => Promise<void>;
  onPurchase: (id: string, quantity: number) => Promise<void>;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onUpdate,
  onDelete,
  onAddStock,
  onPurchase,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(product.name);
  const [price, setPrice] = useState(product.price);
  const [quantity, setQuantity] = useState(1);

  const handleSave = async () => {
    try {
      await onUpdate(product.id, name, price);
      setIsEditing(false);
    } catch (e) {
      // Error handled by hook
    }
  };

  const handleAddStock = async () => {
    try {
      await onAddStock(product.id, quantity);
    } catch (e) {
      // Error handled by hook
    }
  };

  const handlePurchase = async () => {
    try {
      await onPurchase(product.id, quantity);
    } catch (e) {
      // Error handled by hook
    }
  };

  return (
    <div style={styles.card}>
      {isEditing ? (
        <div style={styles.editForm}>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={styles.input}
            placeholder="Name"
          />
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(Number(e.target.value))}
            style={styles.input}
            placeholder="Price"
          />
          <div style={styles.buttonGroup}>
            <button onClick={handleSave} style={styles.saveButton}>Save</button>
            <button onClick={() => setIsEditing(false)} style={styles.cancelButton}>Cancel</button>
          </div>
        </div>
      ) : (
        <>
          <h3 style={styles.title}>{product.name}</h3>
          <p style={styles.price}>${product.price.toFixed(2)}</p>
          <p style={{
            ...styles.stock,
            color: product.isInStock() ? 'green' : 'red'
          }}>
            Stock: {product.stockQuantity} {product.isInStock() ? '✓' : '✗'}
          </p>
          
          <div style={styles.actions}>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(Math.max(1, Number(e.target.value)))}
              min="1"
              style={styles.quantityInput}
            />
            <button onClick={handleAddStock} style={styles.stockButton}>+ Stock</button>
            <button 
              onClick={handlePurchase} 
              style={styles.purchaseButton}
              disabled={!product.isInStock()}
            >
              Buy
            </button>
          </div>
          
          <div style={styles.buttonGroup}>
            <button onClick={() => setIsEditing(true)} style={styles.editButton}>Edit</button>
            <button onClick={() => onDelete(product.id)} style={styles.deleteButton}>Delete</button>
          </div>
        </>
      )}
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '16px',
    margin: '8px',
    width: '250px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: { margin: '0 0 8px 0' },
  price: { fontSize: '1.25rem', fontWeight: 'bold', color: '#333' },
  stock: { margin: '8px 0' },
  actions: { display: 'flex', gap: '8px', marginBottom: '8px' },
  quantityInput: { width: '50px', padding: '4px' },
  stockButton: { padding: '4px 8px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  purchaseButton: { padding: '4px 8px', backgroundColor: '#2196F3', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  buttonGroup: { display: 'flex', gap: '8px' },
  editButton: { padding: '4px 8px', backgroundColor: '#FF9800', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  deleteButton: { padding: '4px 8px', backgroundColor: '#f44336', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  editForm: { display: 'flex', flexDirection: 'column', gap: '8px' },
  input: { padding: '8px', border: '1px solid #ddd', borderRadius: '4px' },
  saveButton: { padding: '8px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  cancelButton: { padding: '8px', backgroundColor: '#9e9e9e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
```

**7. Presentation Layer - `src/presentation/components/ProductForm.tsx`**

```tsx
/**
 * ProductForm Component - Create new products
 */
import React, { useState } from 'react';

interface ProductFormProps {
  onSubmit: (name: string, price: number, stockQuantity: number) => Promise<void>;
}

export const ProductForm: React.FC<ProductFormProps> = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState(0);
  const [stockQuantity, setStockQuantity] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      await onSubmit(name, price, stockQuantity);
      setName('');
      setPrice(0);
      setStockQuantity(0);
    } catch (e) {
      // Error handled by hook
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h3>Add New Product</h3>
      <input
        type="text"
        placeholder="Product Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
        style={styles.input}
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(Number(e.target.value))}
        min="0"
        step="0.01"
        required
        style={styles.input}
      />
      <input
        type="number"
        placeholder="Stock Quantity"
        value={stockQuantity}
        onChange={(e) => setStockQuantity(Number(e.target.value))}
        min="0"
        required
        style={styles.input}
      />
      <button type="submit" disabled={submitting} style={styles.button}>
        {submitting ? 'Adding...' : 'Add Product'}
      </button>
    </form>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    padding: '16px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    maxWidth: '300px',
    margin: '16px',
  },
  input: {
    padding: '8px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
  },
  button: {
    padding: '10px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};
```

**8. Presentation Layer - `src/presentation/components/ProductList.tsx`**

```tsx
/**
 * ProductList Component - Main product display
 */
import React from 'react';
import { useProducts } from '../hooks/useProducts';
import { ProductCard } from './ProductCard';
import { ProductForm } from './ProductForm';

export const ProductList: React.FC = () => {
  const {
    products,
    loading,
    error,
    createProduct,
    updateProduct,
    deleteProduct,
    addStock,
    purchaseProduct,
  } = useProducts();

  if (loading) {
    return <div style={styles.loading}>Loading products...</div>;
  }

  return (
    <div style={styles.container}>
      <h1>Layered Architecture Demo</h1>
      <p style={styles.subtitle}>Product Management with Clean Layers</p>
      
      {error && (
        <div style={styles.error}>
          Error: {error}
        </div>
      )}

      <div style={styles.layout}>
        <ProductForm onSubmit={createProduct} />
        
        <div style={styles.products}>
          {products.length === 0 ? (
            <p style={styles.empty}>No products yet. Add one!</p>
          ) : (
            products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onUpdate={updateProduct}
                onDelete={deleteProduct}
                onAddStock={addStock}
                onPurchase={purchaseProduct}
              />
            ))
          )}
        </div>
      </div>

      <div style={styles.architecture}>
        <h3>Architecture Layers:</h3>
        <ul>
          <li><strong>Domain:</strong> Product entity, business rules, repository interface</li>
          <li><strong>Application:</strong> ProductService orchestrating use cases</li>
          <li><strong>Infrastructure:</strong> LocalStorageRepository / ApiRepository</li>
          <li><strong>Presentation:</strong> React components, hooks</li>
        </ul>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: { padding: '20px', fontFamily: 'Arial, sans-serif' },
  subtitle: { color: '#666', marginTop: 0 },
  loading: { padding: '20px', textAlign: 'center' },
  error: { padding: '12px', backgroundColor: '#ffebee', color: '#c62828', borderRadius: '4px', marginBottom: '16px' },
  layout: { display: 'flex', flexWrap: 'wrap', gap: '20px' },
  products: { display: 'flex', flexWrap: 'wrap', flex: 1 },
  empty: { color: '#666', fontStyle: 'italic' },
  architecture: { marginTop: '40px', padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px' },
};
```

**9. Update `src/App.tsx`**

```tsx
import React from 'react';
import { ProductList } from './presentation/components/ProductList';

function App() {
  return <ProductList />;
}

export default App;
```

### Run the Application

```powershell
npm start

# Opens browser at http://localhost:3000
```

---

## Summary: Layer Responsibilities

| Layer | Responsibility | Depends On |
|-------|---------------|------------|
| **Presentation** | UI, Controllers, DTOs, Input validation | Application |
| **Application** | Use case orchestration, transactions | Domain |
| **Domain** | Business rules, entities, interfaces | Nothing |
| **Infrastructure** | Database, external APIs, frameworks | Domain |

## Common Anti-Patterns to Avoid

❌ **Anemic Domain Model** - Entities with only getters/setters, no business logic
❌ **God Service** - One service class doing everything
❌ **Leaky Abstractions** - Infrastructure details in domain layer
❌ **Circular Dependencies** - Higher layers depending on lower and vice versa
❌ **DTOs in Domain** - Using API models as domain entities

## Architect-Level Considerations

1. **When to break layers**: Cross-cutting concerns (logging, caching) may span layers
2. **Performance**: Layer overhead is negligible; optimize queries, not architecture
3. **Testing**: Each layer should be testable in isolation
4. **Migration**: Can swap infrastructure without touching domain/application
5. **Evolution**: Start with layers, evolve to Clean/Hexagonal as complexity grows
