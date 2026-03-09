# Architecture Decision Flow Diagram

Use this diagram to help decide which architectural pattern best fits your project requirements.

```mermaid
graph TD
    A[Start New Project] --> B{Team Size}
    
    B --> |Small 1-5| C{Project Complexity}
    B --> |Medium 5-20| D{Scalability Needs}
    B --> |Large 20+| E{Independent Deployments}
    
    C --> |Simple/MVP| F{Time to Market}
    C --> |Moderate| G{Maintainability Priority}
    C --> |Complex| H{Domain Complexity}
    
    F --> |Fast| Layered[Layered Architecture]
    F --> |Flexible| Clean[Clean Architecture]
    
    G --> |High| Clean
    G --> |Moderate| Layered
    
    H --> |High| Hexagonal[Hexagonal Architecture]
    H --> |Moderate| Onion[Onion Architecture]
    
    D --> |Low| I{Testability Priority}
    D --> |High| J{Real-time Events}
    
    I --> |High| Hexagonal
    I --> |Moderate| VerticalSlice[Vertical Slice]
    
    J --> |Yes| K{Event Volume}
    J --> |No| Microservices[Microservices]
    
    K --> |High| EDA[Event-Driven Architecture]
    K --> |Moderate| Microservices
    
    E --> |Yes| L{Service Boundaries Clear}
    E --> |No| M{Legacy Integration}
    
    L --> |Yes| Microservices
    L --> |No| SOA[SOA]
    
    M --> |Heavy| SOA
    M --> |Light| N{Compute Model}
    
    N --> |On-Demand| Serverless[Serverless]
    N --> |Always-On| SpaceBased[Space-Based]
```

---

## Quick Reference Guide

| Architecture | Best For | Trade-offs |
|-------------|----------|------------|
| **Layered (N-Tier)** | Simple apps, MVPs, small teams | Fast start, but can become rigid |
| **Clean Architecture** | Domain-centric apps, testability | Learning curve, more boilerplate |
| **Hexagonal** | High testability, external integrations | Complexity increases with ports |
| **Onion** | Domain isolation, dependency control | Similar to Clean, steeper curve |
| **Vertical Slice** | Feature-focused teams, rapid iteration | Can lead to duplication |
| **Microservices** | Large teams, independent scaling | Operational complexity |
| **SOA** | Enterprise integration, legacy systems | Can be heavyweight |
| **Event-Driven** | Real-time, high throughput, decoupling | Debugging complexity |
| **Serverless** | Variable workloads, cost optimization | Cold starts, vendor lock-in |
| **Space-Based** | Extreme scalability, high availability | Infrastructure complexity |
