


# Repository Guidelines

> **For AI Agents**: This is the single source of truth for coding preferences and project context.
> Agent-specific files (CLAUDE.md, GEMINI.md, CODEX.md) reference this document.

---

## Context Priority

1. **Read this file first** for repository conventions
2. Review existing code patterns before implementing new features
3. **Search for existing utilities before writing new code**
---
## Key Principles
You are an expert in Python, Django, and scalable web application development. # emprove
  - Write clear, technical responses with precise Django examples.
  - Use Django's built-in features and tools wherever possible to leverage its full capabilities.
  - Prioritize readability and maintainability; follow Django's coding style guide (PEP 8 compliance).
  - Use descriptive variable and function names; adhere to naming conventions (e.g., lowercase with underscores for functions and variables).
  - Structure your project in a modular way using Django apps to promote reusability and separation of concerns.

  ## Django/Python
  - Use Django’s class-based views (CBVs) for more complex views; prefer function-based views (FBVs) for simpler logic.
  - Leverage Django’s ORM for database interactions; avoid raw SQL queries unless necessary for performance.
  - Use Django’s built-in user model and authentication framework for user management.
  - Utilize Django's form and model form classes for form handling and validation.
  - Follow the MVT (Model-View-Template) pattern strictly for clear separation of concerns.
  - Use middleware judiciously to handle cross-cutting concerns like authentication, logging, and caching.

## Django Specific Rules
  ### Error Handling
  - NEVER swallow errors silently
  - Always show user feedback for errors (Django messages, HTMX response headers)
  - Log errors with proper context for debugging

  ### Views
  - Prefer Function-Based Views
  - Always validate request.method explicitly
  - Return proper HTTP status codes
  - Use `select_related()` / `prefetch_related()` to avoid N+1 queries

  ### Templates & HTMX
  - Use template inheritance (`{% extends %}`, `{% block %}`)
  - Create partial templates for HTMX responses (`_partial.html` naming)
  - Always include `hx-indicator` for loading states
  - Handle `HX-Request` header for partial vs full page responses using django.htmx from django-htmx package

  ### Forms
  - Use ModelForm for model-backed forms
  - Validate in `clean()` and `clean_<field>()` methods
  - Always handle form errors in templates
  - Disable submit buttons during HTMX requests

  ### Celery Tasks
  - Tasks must be idempotent
  - Use proper retry strategies with exponential backoff
  - Always log task start/completion/failure
  - Pass serializable arguments only (no model instances)

  ## Testing

  - Write failing test first (TDD)
  - Use Factory Boy: `UserFactory.create(is_admin=True)`
  - Use pytest fixtures in `conftest.py`
  - Test behavior, not implementation
  - Run tests before committing

## Error Handling and Validation
  - Implement error handling at the view level and use Django's built-in error handling mechanisms.
  - Use Django's validation framework to validate form and model data.
  - Prefer try-except blocks for handling exceptions in business logic and views.
  - Customize error pages (e.g., 404, 500) to improve user experience and provide helpful information.
  - Use Django signals to decouple error handling and logging from core business logic.

    1. Follow Django's "Convention Over Configuration" principle for reducing boilerplate code.
    2. Prioritize security and performance optimization in every stage of development.
    3. Maintain a clear and logical project structure to enhance readability and maintainability.
    
    Refer to Django documentation for best practices in views, models, forms, and security considerations.

**NEVER reinvent the wheel. ALWAYS search for existing utilities first.**

## ⚠️ CRITICAL: Reuse Existing Code (DRY)

**Tech Stack:**
- **Backend**: Django 5.x with Python 3.13+
- **Frontend**: React/TypeScript, TailwindCSS, AlpineJS, HTMX
- **Database**: PostgreSQL with pgvector extension
- **Task Queue**: Celery with Redis
- **AI/ML**: LangChain, OpenAI, Anthropic, Google Gemini
- **Package Management**: uv (Python), npm (Node.js)
## Architecture

- This is a Django project built on Python 3.14.
- User authentication uses `django-allauth`.
- The front end is mostly standard Django views and templates.
- HTMX and Alpine.js are used to provide single-page-app user experience with Django templates.
  HTMX is used for interactions which require accessing the backend, and Alpine.js is used for
  browser-only interactions.
- JavaScript files are kept in the `/assets/` folder and built by vite.
  JavaScript code is typically loaded via the static files framework inside Django templates using `django-vite`.
- APIs use Django Rest Framework, and JavaScript code that interacts with APIs uses an
  auto-generated OpenAPI-schema-baesd client.
- The front end uses Tailwind (Version 4) and DaisyUI.
- The main database is Postgres.
- Celery is used for background jobs and scheduled tasks.
- Redis is used as the default cache, and the message broker for Celery.

## Project Structure & Module Organization


## Python Best Practices


## Django Guidelines



## Dependencies
  ### Backend
  - Django
  - Django Ninja (for API development)
  - Celery (for background tasks)
  - Redis (for caching and task queues)
  - PostgreSQL (preferred database for production)

  ### Frontend
  - TailwindCSS
  - DaisyUI
  - AlpineJS
  - HTMX
  ### Mobile App
  - React Native
  - Expo
  ### Package Management
  - uv (Python)
  - npm (Node.js)


**NEVER reinvent the wheel. ALWAYS search for existing utilities first.**

## ⚠️ CRITICAL: Reuse Existing Code (DRY)

## Performance Optimization
  - Optimize query performance using Django ORM's select_related and prefetch_related for related object fetching.
  - Use Django’s cache framework with backend support (e.g., Redis or Memcached) to reduce database load.
  - Implement database indexing and query optimization techniques for better performance.
  - Use asynchronous views and background tasks (via Celery) for I/O-bound or long-running operations.
  - Optimize static file handling with Django’s static file management system (e.g., WhiteNoise or CDN integration).

## Key Conventions




### Quick Reference Commands
