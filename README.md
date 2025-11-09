# Library Management System (Deerwalk Schools)

A modular, scalable backend built with **FastAPI**, designed using **Clean Architecture** and **Domain-Driven Design (DDD)** principles.The system is divided into distinct layers and feature-based modules to ensure maintainability, testability, and clear separation of concerns.

---

## Project Overview

This application manages library operations such as:
- Book management and borrowing
- User authentication and roles
- Reviews, recommendations, and events
- Feedback, genres, and quotes

Each **module** encapsulates its own domain logic, persistence layer, and presentation (API).  
Shared infrastructure, configuration, and utilities are handled by the `core` and `background` packages.


---

## Architecture Overview

This project follows **Clean Architecture**, where dependencies point **inward**:

```
Presentation → Use Cases → Domain → Infrastructure
```

| Layer | Purpose |
|-------|----------|
| **Presentation** | FastAPI controllers and routers handling HTTP requests |
| **Use Cases** | Application-specific business logic |
| **Domain** | Entities, value objects, interfaces (pure business rules) |
| **Infra** | External implementations (DB, S3, SMTP, etc.) |
| **Core** | Shared global components like database setup, settings, and reusable interfaces |

---

## Creating a New Module

To add a new feature (e.g., `notifications`):

1. **Create the module folder:**
   ```bash
   mkdir -p modules/notifications/{domain/{entities,repositories,requests,responses,usecases},infra/{repositories,services},presentation/v1/{controllers,routers}}
   ```

2. **Define repository interfaces and use cases** following the domain patterns.

3. **Add controllers and routers** under `presentation/v1`.

4. **Include your router** in `routers/v1/router.py`.

---

## Creating a New Use Case

1. Create a new file in the module’s `domain/usecases/` directory.
2. Implement the logic as a class with an `execute()` method.
3. Inject dependencies via the constructor.
4. Call the use case from your controller.

---

## Running the Application

```bash
# 1. Install dependencies
uv sync

# 2. Run database migrations
alembic upgrade head

# 3. Start Celery worker (for background tasks)
celery -A background.celery_app worker --loglevel=info

# 4. Start the API server
uv run fastapi dev main.py
```

---

## Design Philosophy

- **Feature-first modularization** — each domain (books, users, events, etc.) lives in isolation.  
- **Dependency Inversion** — business logic doesn’t depend on frameworks or databases.  
- **Replaceable Infrastructure** — repositories and services are easily swappable.  
- **High Testability** — interfaces and dependency injection make unit tests trivial.

---


MIT License © 2025 — Built with ❤️ by dmt guys.
