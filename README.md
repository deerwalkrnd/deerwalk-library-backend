# Library Management System (Deerwalk Schools)

A modular, scalable backend built with **FastAPI**, designed using **Clean Architecture** and **Domain-Driven Design (DDD)** principles.  
The system is divided into distinct layers and feature-based modules to ensure maintainability, testability, and clear separation of concerns.

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

## Directory Structure

Below is the standardized project structure:

```
.
├── background/                   # Background processing (Celery)
│   ├── celery_app.py
│   ├── __init__.py
│   └── tasks/
│       └── email_task.py

├── cli/
│   └── seed_admin.py             # Command-line scripts (seeding, maintenance)

├── core/                         # Shared infrastructure and global domain
│   ├── config.py
│   ├── dependencies/
│   │   ├── database.py
│   │   ├── get_settings.py
│   │   ├── get_smtp.py
│   │   └── middleware/
│   │       ├── get_available_user.py
│   │       ├── get_current_librarian.py
│   │       └── get_current_user.py
│   ├── domain/
│   │   ├── entities/
│   │   │   └── base_entity.py
│   │   ├── repositories/
│   │   │   └── repository_interface.py
│   │   └── services/
│   │       ├── email_service_interface.py
│   │       ├── file_service_interface.py
│   │       └── s3_file_service_interface.py
│   ├── exc/
│   │   ├── error_code.py
│   │   └── library_exception.py
│   ├── infra/
│   │   ├── repositories/
│   │   │   └── repository.py
│   │   └── services/
│   │       ├── email_notification_service.py
│   │       └── s3_file_service.py
│   ├── models/                   # ORM models (SQLAlchemy)
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── book_copy.py
│   │   ├── genre.py
│   │   ├── ...
│   └── utils/
│       ├── csv_metadata_parser.py
│       ├── csv_password_hasher.py
│       ├── csv_validator.py
│       └── make_email.py

├── main.py                       # Application entrypoint

├── modules/                      # Feature-based bounded contexts
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── password_reset_token.py
│   │   │   ├── repositories/
│   │   │   │   └── password_reset_token_repository_interface.py
│   │   │   ├── requests/
│   │   │   │   ├── login_request.py
│   │   │   │   ├── password_reset_token_request.py
│   │   │   │   ├── reset_password_request.py
│   │   │   │   └── sso_url_request.py
│   │   │   ├── responses/
│   │   │   │   ├── token_response.py
│   │   │   │   └── forgot_password_response.py
│   │   │   ├── services/
│   │   │   │   ├── password_hasher_interface.py
│   │   │   │   └── token_service_interface.py
│   │   │   └── usecases/
│   │   │       ├── login_use_case.py
│   │   │       ├── create_password_reset_token_use_case.py
│   │   │       └── generate_jwt_token_use_case.py
│   │   ├── infra/
│   │   │   ├── repositories/
│   │   │   │   └── password_reset_token_repository.py
│   │   │   └── services/
│   │   │       ├── jwt_service.py
│   │   │       └── argon2_hasher.py
│   │   └── presentation/
│   │       └── v1/
│   │           ├── controllers/
│   │           │   ├── auth_controller.py
│   │           │   └── password_reset_token_controller.py
│   │           └── routers/
│   │               └── auth_router.py
│   ├── books/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   ├── requests/
│   │   │   ├── responses/
│   │   │   └── usecases/
│   │   ├── infra/
│   │   │   └── repositories/
│   │   └── presentation/
│   │       └── v1/
│   │           ├── controllers/
│   │           └── routers/
│   ├── users/
│   │   ├── domain/
│   │   │   ├── requests/
│   │   │   ├── responses/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       └── v1/
│   │           ├── controllers/
│   │           └── routers/
│   └── ... other modules (book_borrows, reviews, quotes, genres, feedbacks, etc.)

└── routers/
    └── v1/
        └── router.py             # Central router aggregator
```

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

## 🧾 License

MIT License © 2025 — Built with ❤️ by dmt guys.
