# AGENTS.md — Django Ninja Guidelines

Project context and strict constraints for AI agents. Adhere to these conventions to maintain codebase consistency and prevent regressions.

---

## 1. Project Overview & Quick Reference
Tenir is a backend API for flutter app tenir. So this project functions purely as a headless REST API. Tenir is an app that allows people to book travel for hiking a mountain in Indonesia.
* **Framework:** Django + Django Ninja (`ninja`)
* **Validation/Serialization:** Pydantic (via `ninja.Schema`)
* **Database:** Django ORM

### Common Commands

* **Run Development Server:** `python manage.py runserver`
* **Create Migrations:** `python manage.py makemigrations`
* **Apply Migrations:** `python manage.py migrate`
* **Run Tests:** `python manage.py test`
* **Check Formatting & Linting:** `ruff check .`
* **Format Code:** `ruff format .`

---

## 2. Core Architecture Rules

### API Routes & Structure
* Place API definitions inside `api.py` or `apis/` modules within each Django app.
* Main API instance lives in `config/api.py` (or project root settings package). Register sub-routers using `api.add_router("/prefix/", router)`.
* **DO NOT** use standard Django Views, Class-Based Views (CBVs), or Django REST Framework (DRF) serializers. Everything goes through Django Ninja.

### Schemas (`ninja.Schema`)
* Always use `ninja.Schema` for request/response models (never raw Pydantic `BaseModel` unless doing non-field pure validation).
* **Separate Input and Output schemas explicitly**:
  * `UserIn(Schema)` for incoming payload (`POST`/`PUT`).
  * `UserOut(Schema)` for outgoing responses.
  * `ModelSchema` is permitted when mapping directly to ORM fields, but explicitly set `model_fields`.

#### Example Schema Definition

```python
from ninja import Schema, ModelSchema
from .models import Article

class ArticleIn(Schema):
    title: str
    content: str

class ArticleOut(ModelSchema):
    class Config:
        model = Article
        model_fields = ['id', 'title', 'content', 'created_at']
```

---

## 3. Async vs Sync Execution

Django Ninja supports both `def` and `async def`. **Do not mix these up.**

1. **Default to Synchronous (`def`)** unless the operation is explicitly I/O bound on non-Django calls (e.g., external API requests via `httpx`).
2. **Async Rules (`async def`):** ALL Django ORM calls MUST use async ORM methods:
   * `await Article.objects.aget(id=pk)` instead of `.get(id=pk)`
   * `async for obj in Article.objects.all():` instead of standard loops
   * Or wrap sync operations in `sync_to_async`.
3. Never issue synchronous ORM calls inside an `async def` route (it will cause blockages or throw `SynchronousOnlyOperation`).

---

## 4. Error Handling & HTTP Status Codes

* Use Django Ninja's builtin exception handling or raise HTTP exceptions directly using `ninja.errors.HttpError`.
* Define response schemas for status codes explicitly in route decorators when applicable.

#### Example Error Handling

```python
from ninja.errors import HttpError

@router.get("/items/{item_id}", response={200: ItemOut, 404: ErrorOut})
def get_item(request, item_id: int):
    try:
        return Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise HttpError(404, "Item not found")
```

---

## 5. Security & Authentication

* Place authenticators in `apps/core/auth.py` or app-level `auth.py`.
* Pass authentication via route options: `@router.get("/me", auth=GlobalAuth())`.
* Never bypass authentication decorators on protected endpoints.
* Keep in mind the app is using JWT for authentication between API and the flutter app.
* Always filter ORM queries by the logged-in user (`request.auth` or `request.user`) to prevent IDOR vulnerabilities.

---

## 6. Strict "Do Not Do" Constraints

* ❌ **DO NOT** use Django Forms, `django.forms`, or DRF `serializers.Serializer`.
* ❌ **DO NOT** create raw SQL queries; use Django ORM or `.select_related()` / `.prefetch_related()` to avoid N+1 queries.
* ❌ **DO NOT** return raw ORM QuerySets directly without declaring a `response` schema on the router decorator.
* ❌ **DO NOT** place heavy business logic directly inside route handlers; delegate to domain functions or service files (`services.py`).