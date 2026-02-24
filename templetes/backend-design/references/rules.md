# backend-design Skill Rules and Anti-Patterns

This document defines the design rules that must be enforced when producing a backend-design output.

---

## Core Design Rules

### Rule 1: Output Contract Traceability (Mandatory)

**Every entry in `output_contract` must map to at least one API endpoint.**

- If output_contract mentions "REST API with endpoints: POST /media/upload, GET /media/{id}", then:
  - Step 2 (API Endpoints) must define both endpoints
  - Step 4 (API Layer: Request/Response DTOs) must define request/response schemas for both
  - Step 5 (Service Layer: Application Service) must include the service method(s) that handle these endpoints

- Verification: After Step 7b, the design document must include a traceability matrix showing which endpoint(s) satisfy each output_contract entry.

- Anti-pattern: Designing endpoints that are not mentioned in output_contract (scope creep).

---

### Rule 2: Endpoint Schema Completeness (Mandatory)

**Every API endpoint must have both a request schema and a response schema defined.**

- GET endpoints with no request body: define `request_schema: "empty"` or `"NoContent"`
- POST/PATCH endpoints: define a request schema (e.g., `MediaFileCreate`, `MediaFileUpdate`)
- All endpoints: define a response schema (even if error-only, e.g., `ErrorResponse`)

- Validation: Before writing, verify no endpoint has a null or empty request_schema or response_schema field.

- Anti-pattern: "POST /api/media { }" — endpoint with no schema detail.

---

### Rule 3: Domain Layer Isolation (Mandatory)

**The domain layer (`{domain}/domain/`) must have zero dependencies on any framework.**

No imports of FastAPI, SQLModel, SQLAlchemy, Pydantic, or any HTTP/ORM library are allowed inside `domain/`.
Domain entities and value objects are pure Python classes.

```python
# CORRECT — pure Python domain entity
@dataclass
class MediaFile:
    id: UUID
    owner_id: UUID
    filename: FileName     # VO
    mime_type: MimeType    # VO
    size_bytes: FileSize   # VO

# WRONG — ORM decorator leaking into domain
class MediaFile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
```

- Rationale: Keeping the domain pure means it can be tested without any infrastructure, swapped without changing business rules, and read without understanding any framework.

- Verification: In Step 3 review, confirm no `import fastapi`, `import sqlmodel`, or `import sqlalchemy` appears in any `domain/` file.

- Anti-pattern: Mixing ORM models with domain entities in the same class.

---

### Rule 3b: Service Layer Isolation (Mandatory)

**The application service layer must NOT directly access the database. All DB access goes through stores.**

```python
# CORRECT
class MediaService:
    async def create_file(self, session, owner_id, req):
        entity = self.facade.create_file(...)   # domain logic
        await self.store.save(session, entity)  # DB via store

# WRONG
class MediaService:
    async def create_file(self, session, owner_id, req):
        orm = MediaFileORM(...)                 # ORM directly in service
        session.add(orm)
        await session.commit()
```

- Verification: Every application service method calls only facade methods, store methods, proxy methods, and mappers. Never direct ORM operations.

---

### Rule 4: Store Methods Must Be Async (Mandatory)

**Every store (`service/store/`) method must be defined as `async def` (not `def`).**

- This enables concurrent request handling in FastAPI.

- Example:
  ```python
  # CORRECT:
  async def find_by_id(self, session: AsyncSession, file_id: UUID) -> Optional[MediaFile]:
    ...

  # WRONG:
  def find_by_id(self, session: Session, file_id: UUID) -> MediaFile:
    ...
  ```

- Verification: In Step 5a, check that all store method signatures include `async def`.

- Anti-pattern: Synchronous store methods (blocking calls in async context).

---

### Rule 5: Custom Exception Classes (Mandatory)

**Error handling must use custom exception classes, not bare `HTTPException`.**

- Define custom exceptions for domain-specific errors:
  ```
  - ResourceNotFoundError(404) — entity not found
  - UnauthorizedError(401) — user not authenticated
  - ForbiddenError(403) — user lacks permission
  - ValidationError(422) — request data invalid
  ```

- Each custom exception:
  - Has a class name (PascalCase)
  - Maps to an HTTP status code
  - Includes a message template for context

- Rationale: Custom exceptions are more testable, self-documenting, and enable consistent error handling across the codebase.

- Verification: In Step 6b, verify all error scenarios are covered by custom exception classes.

- Anti-pattern: `raise HTTPException(status_code=404, detail="Not found")` scattered throughout code.

---

### Rule 6: Authentication Dependency Injection (Mandatory)

**All endpoints with `auth_required: true` must use `FastAPI Depends(get_current_user)` pattern.**

- Design step output must explicitly list which endpoints are protected.

- Example:
  ```
  POST /api/v1/media/upload
    Auth Required: true
    Implementation: async def upload_media(file: UploadFile, current_user = Depends(get_current_user))
  ```

- The `get_current_user` dependency:
  - Validates JWT token in Authorization header
  - Extracts user_id from token claims
  - Raises UnauthorizedError if token is missing or invalid
  - Returns the authenticated user object

- Verification: In Step 6a, verify all protected endpoints include auth_required: true AND will use Depends(get_current_user) in implementation.

- Anti-pattern: Checking authentication inside the endpoint handler (manual auth checks instead of Depends).

---

### Rule 7: Naming Conventions (Mandatory)

**Follow Python, FastAPI, and DDD naming standards.**

#### Directory Naming (domain-first, snake_case)
- Domain directories: `auth/`, `media/`, `folder/` (one directory per domain)
- Sub-layers: `domain/`, `api/`, `service/` (always lowercase, fixed names)

#### File Naming (snake_case)
- Controller: `{domain}/api/controller/{domain}_router.py`
- Request DTO: `{domain}/api/request/{entity}_{action}_request.py`
- Response DTO: `{domain}/api/response/{entity}_response.py`
- API Mapper: `{domain}/api/mapper/{domain}_mapper.py`
- Entity: `{domain}/domain/entity/{entity}.py`
- Value Object: `{domain}/domain/vo/{vo_name}.py`
- Facade: `{domain}/domain/facade/{domain}_facade.py`
- Store: `{domain}/service/store/{entity}_store.py`
- Proxy: `{domain}/service/proxy/{service}_proxy.py`
- Service Mapper: `{domain}/service/mapper/{domain}_mapper.py`
- App Service: `{domain}/service/{domain}_service.py`

#### Class Naming (PascalCase)
- Domain entities: `User`, `MediaFile`, `Folder`
- Value Objects: `EmailAddress`, `FileName`, `FileSize`, `MimeType`
- Domain Facade: `AuthFacade`, `MediaFacade`
- Application Service: `AuthService`, `MediaService`
- Store: `UserStore`, `MediaFileStore`
- Proxy: `StorageProxy`, `EmailProxy`, `TokenProxy`
- Request DTOs: `RegisterRequest`, `MediaFileCreateRequest`
- Response DTOs: `UserResponse`, `MediaFileResponse`, `AuthResponse`
- Domain Exceptions: `MediaFileNotFoundError`, `InvalidCredentialsError`

#### Method/Function Naming (snake_case)
- Application service: `create_file()`, `get_file()`, `delete_file()`
- Store methods: `save()`, `find_by_id()`, `find_by_owner()`, `delete()`
- Proxy methods: `upload()`, `delete()`, `send_email()`
- Facade methods: `create_file()`, `validate_ownership()`, `mark_hidden()`
- Mapper methods: `to_domain()`, `to_response()`, `to_orm()`

#### Field Naming (snake_case)
- Entity fields: `owner_id`, `created_at`, `mime_type`
- Request/Response DTO fields: `file_name`, `mime_type`, `size_bytes` (not `fileName`)
- Database columns: match entity field names exactly (from schema-design)

---

### Rule 8: Anti-Patterns (Do NOT Do)

#### Anti-Pattern 1: Business Logic in Router

**WRONG:**
```python
@router.post("/api/v1/media/upload")
async def upload(file: UploadFile, current_user = Depends(get_current_user)):
    # Business logic here
    if file.size > 10_485_760:
        raise HTTPException(status_code=422, detail="File too large")

    # Direct DB access
    media = MediaFile(filename=file.filename, user_id=current_user.id)
    session.add(media)
    session.commit()

    return {"id": media.id}
```

**CORRECT:**
```python
@router.post("/api/v1/media/upload")
async def upload(file: UploadFile, current_user = Depends(get_current_user)):
    # Call service layer (business logic + DB access via service)
    try:
        media = await media_service.create_media_file(file, current_user.id)
        return MediaFileResponse.from_orm(media)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
```

#### Anti-Pattern 2: Direct DB Queries in Store (Session Not Injected)

**WRONG:**
```python
class MediaFileStore:
    async def get_by_owner(self, user_id: UUID):
        # Session not injected — hidden state, untestable
        return session.query(MediaFileORM).filter(MediaFileORM.user_id == user_id).all()
```

**CORRECT:**
```python
class MediaFileStore:
    async def find_by_owner(self, session: AsyncSession, user_id: UUID) -> list[MediaFile]:
        result = await session.execute(
            select(MediaFileORM).where(MediaFileORM.user_id == user_id)
        )
        orm_list = result.scalars().all()
        return [self.mapper.to_domain(orm) for orm in orm_list]
```

#### Anti-Pattern 3: Missing Error Handling

**WRONG:**
```python
async def get_media_file(self, session: AsyncSession, file_id: UUID):
    # No error handling — what if file not found?
    media = await self.store.find_by_id(session, file_id)
    return media
```

**CORRECT:**
```python
async def get_media_file(self, session: AsyncSession, file_id: UUID) -> MediaFileResponse:
    media = await self.store.find_by_id(session, file_id)
    if not media:
        raise MediaFileNotFoundError(f"MediaFile {file_id} not found")
    return self.mapper.to_response(media)
```

#### Anti-Pattern 4: Missing Auth on Protected Endpoints

**WRONG:**
```python
@router.delete("/api/v1/media/{file_id}")
async def delete_media_file(file_id: UUID):
    # No authentication — anyone can delete!
    return await media_service.delete(file_id)
```

**CORRECT:**
```python
@router.delete("/api/v1/media/{file_id}")
async def delete_media_file(file_id: UUID, current_user = Depends(get_current_user)):
    # Verify ownership
    return await media_service.delete(file_id, current_user.id)
```

#### Anti-Pattern 5: Inconsistent Schema Naming

**WRONG:**
```
MediaFile (base)
MediaFileCreate (request for POST)
media_file_response (response — inconsistent casing)
CreateMediaFile (request for PATCH — confusing name)
```

**CORRECT:**
```
MediaFileBase (base schema with common fields)
MediaFileCreate (request for POST /media)
MediaFileUpdate (request for PATCH /media/{id})
MediaFileResponse (response for GET endpoints)
MediaFileDetailResponse (response for GET /media/{id})
```

#### Anti-Pattern 6: Overly Broad Service Methods

**WRONG:**
```python
class MediaFileService:
    async def process_request(self, request: dict):
        # Handles upload, delete, list — too many responsibilities
        if request["action"] == "upload":
            ...
        elif request["action"] == "delete":
            ...
```

**CORRECT:**
```python
class MediaFileService:
    async def create_media_file(self, file_data: MediaFileCreate) -> MediaFileResponse:
        # One method, one responsibility
        ...

    async def delete_media_file(self, file_id: UUID, user_id: UUID) -> bool:
        # One method, one responsibility
        ...
```

#### Anti-Pattern 7: Vague Validation Rules

**WRONG:**
```
- name: email
  type: str
  validation: "valid email format"
```

**CORRECT:**
```
- name: email
  type: str
  validation: "regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'"
```

#### Anti-Pattern 8: Missing Pagination/Filtering for List Endpoints

**WRONG:**
```
GET /api/v1/media
  Response: List[MediaFileResponse]  # Could return 1M items!
```

**CORRECT:**
```
GET /api/v1/media?skip=0&limit=20&sort=created_at&order=desc
  Request Schema: MediaFileListQuery
  Response: { items: List[MediaFileResponse], total: int, skip: int, limit: int }
```

#### Anti-Pattern 9: Framework Imports in the Domain Layer

**WRONG:**
```python
# media/domain/entity/media_file.py
from sqlmodel import SQLModel, Field    # ← ORM in domain — FORBIDDEN
from fastapi import UploadFile           # ← HTTP framework in domain — FORBIDDEN

class MediaFile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
```

**CORRECT:**
```python
# media/domain/entity/media_file.py
from dataclasses import dataclass
from uuid import UUID
from media.domain.vo.file_name import FileName    # ← only domain VOs
from media.domain.vo.mime_type import MimeType

@dataclass
class MediaFile:
    id: UUID
    owner_id: UUID
    filename: FileName
    mime_type: MimeType
```

- Rule: `{domain}/domain/` files must contain **zero** imports from `fastapi`, `sqlmodel`, `sqlalchemy`, `pydantic`, or any HTTP/ORM library.

#### Anti-Pattern 10: Mapper Confusion — API Mapper vs Service Mapper

Two separate mapper classes exist per domain and must not be mixed.

**WRONG:**
```python
# Using the service mapper (ORM ↔ domain) inside the API layer
@router.post("/media")
async def upload(req: MediaFileCreateRequest):
    entity = service_mapper.to_domain(req)   # ← service mapper in API layer
    ...
```

**CORRECT:**
```python
# media/api/mapper/media_mapper.py  — converts API DTOs ↔ domain objects
class MediaApiMapper:
    def to_domain(self, req: MediaFileCreateRequest) -> MediaFileCreateCommand: ...
    def to_response(self, entity: MediaFile) -> MediaFileResponse: ...

# media/service/mapper/media_mapper.py  — converts ORM models ↔ domain objects
class MediaServiceMapper:
    def to_domain(self, orm: MediaFileORM) -> MediaFile: ...
    def to_orm(self, entity: MediaFile) -> MediaFileORM: ...
```

- API mapper lives in `{domain}/api/mapper/` and touches only Pydantic DTOs + domain objects.
- Service mapper lives in `{domain}/service/mapper/` and touches only ORM models + domain objects.

---

## Design Quality Checklist

Before declaring a backend-design complete, verify:

**Mandatory (every domain must have these four):**
- [ ] **Entity** (`domain/entity/`): At least one domain entity defined as pure Python
- [ ] **Facade** (`domain/facade/`): Facade interface defined; service layer calls only facade for domain logic
- [ ] **Controller** (`api/controller/`): FastAPI router defined; no business logic inside handlers
- [ ] **Store** (`service/store/`): Store class defined; all methods are `async def` with `AsyncSession` as first arg

**Always verify:**
- [ ] **Scope**: All output_contract entries are covered by at least one endpoint
- [ ] **Domain Layer**: `{domain}/domain/` files contain zero imports from fastapi / sqlmodel / sqlalchemy / pydantic
- [ ] **Auth**: All protected endpoints have `auth_required: true` and use `Depends(get_current_user)`
- [ ] **Naming**: All included files, classes, methods, and fields follow DDD + snake_case / PascalCase conventions (Rule 7)
- [ ] **Anti-patterns**: No business logic in routers; no ORM in domain layer; no direct DB access outside stores

**Optional — verify only if included:**
- [ ] **Value Objects** (`domain/vo/`): VOs are immutable and enforce validation on construction
- [ ] **Domain Exceptions** (`domain/exception/`): Domain exceptions are distinct from HTTP exceptions
- [ ] **Request DTOs** (`api/request/`): Each request DTO has concrete field types and validation rules
- [ ] **Response DTOs** (`api/response/`): Each response DTO covers all fields returned by the endpoint
- [ ] **API Mapper** (`api/mapper/`): `to_domain()` and `to_response()` both defined
- [ ] **Service Mapper** (`service/mapper/`): `to_domain()` and `to_orm()` both defined
- [ ] **Proxy** (`service/proxy/`): All proxy methods are `async def`
- [ ] **Application Service**: Methods call only facade / store / proxy / mapper — no direct ORM operations

---

## Traceability and Verification

### Output Contract → Endpoint Mapping

After Step 2, create a matrix:

| Output Contract Item | Endpoint(s) | Status |
|---|---|---|
| REST API: POST /api/v1/media/upload | POST /api/v1/media/upload | ✓ |
| REST API: GET /api/v1/media/{file_id} | GET /api/v1/media/{file_id} | ✓ |
| Service: Media validation | (handled in POST endpoint) | ✓ |

Every row must have a checkmark before writing.

### DTO/Schema Usage Verification

After Step 4 (API Layer), verify:

- [ ] Every request DTO used in an endpoint is defined in `{domain}/api/request/`
- [ ] Every response DTO used in an endpoint is defined in `{domain}/api/response/`
- [ ] No undefined schema references
- [ ] All fields in each DTO are concrete (no "something", "data", etc.)
- [ ] API mapper methods (`to_domain`, `to_response`) are defined for every DTO pair

### Service/Store Alignment

After Step 5 (Service Layer), verify:

- [ ] Every store has at least one async CRUD method defined
- [ ] If an application service is present: all DB access goes through the store, never direct ORM
- [ ] If `service/mapper/` is present: `to_domain` and `to_orm` both defined for each entity
- [ ] No service method calls `session.add()` / `session.commit()` directly

---

## Notes for Cursor AI Agent

1. **Validation is strict** — if any rule is violated, fix it before writing the output.
2. **Traceability is mandatory** — the ability to trace from output_contract to endpoint to code is proof the design is complete.
3. **Anti-patterns are common** — watch for them during design; they are easy to miss.
4. **Naming matters** — consistent naming makes the code easier to understand and implement.
5. **Self-validation is not optional** — the output file must include a self-validation section showing all checks passed.
