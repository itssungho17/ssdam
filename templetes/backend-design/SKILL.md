---
name: backend-design
description: Backend-specialised design skill in the SSDAM pipeline. Reads architecture-design (and optionally schema-design) to produce a DDD-structured backend specification per domain. Mandatory components per domain are domain/entity, domain/facade, api/controller, and service/store. All other sub-layers (vo, event, exception, shared, request, response, mapper, proxy, config, application service) are optional and included only when needed.
compatibility: Universal
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# backend-design Skill

## File Paths Reference

This skill reads from and writes to the SSDAM pipeline workspace:

```
task-spec.TSK-NNN.yaml (user provides path)
  + architecture-design.TSK-NNN.md (required — from .ssdam/{id}/output/design/)
  + schema-design.TSK-NNN.sql (optional — if data-modeling + schema-design were run)
  ↓
[backend-design]  ← YOU ARE HERE
  ↓
.ssdam/{id}/output/design/backend-design.TSK-NNN.md
  ↓
[backend-implementation]  (depends on this output)
```

**Skill files (read-only):**
- `/mnt/ssdam/templetes/backend-design/SKILL.md` (this file)
- `/mnt/ssdam/templetes/backend-design/references/input.template.yaml` (input schema reference)
- `/mnt/ssdam/templetes/backend-design/references/output.template.yaml` (output schema reference)
- `/mnt/ssdam/templetes/backend-design/references/rules.md` (design rules and anti-patterns)

**Runtime files (created per execution):**
- Input 1: `task-spec.TSK-NNN.yaml` (user provides path)
- Input 2: `.ssdam/{id}/output/design/architecture-design.TSK-NNN.md` (required prerequisite)
- Input 3: `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (optional — read if present)
- Output: `.ssdam/{id}/output/design/backend-design.TSK-NNN.md` (written by this skill)

---

## Overview

| | |
|---|---|
| **Trigger** | `/backend-design <task-spec-path>` |
| **Prerequisites** | `architecture-design.TSK-NNN.md` must exist; optionally `schema-design.TSK-NNN.sql` |
| **Input** | task-spec.TSK-NNN.yaml + architecture-design output + (optional) schema-design output |
| **Work** | Define API endpoints, request/response schemas, service/repository layers, error handling, test strategy |
| **Output** | `.ssdam/{id}/output/design/backend-design.TSK-NNN.md` (detailed backend specification) |
| **Required** | YES — must exist before running backend-implementation |

---

## Input Specification

### Trigger Command

```
/backend-design <task-spec-path>
```

**Example:**
```
/backend-design .ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml
```

### Fields Read from task-spec

From `task-spec.TSK-NNN.yaml`:

**From `metadata`:**
- `mission_id` — copied to output document header
- `task_id` — used to derive output filename (TSK-NNN)
- `task_name` — used as document title
- `requirement_ids` — for traceability

**From `output_contract`:**
- List of deliverables the backend must provide
- Used to verify all endpoints are designed

**From `execution_plan`:**
- `tech_stack.backend` — backend framework (FastAPI, Django, etc.)
- `tech_stack.database` — database type (PostgreSQL, MySQL, etc.)
- `tech_stack.project_root` — absolute path to project repository
- `steps[]` where `exec_type == "backend-design"`: description and acceptance_criteria

### Fields Read from architecture-design Output

From `.ssdam/{id}/output/design/architecture-design.TSK-NNN.md`:

- `api_contract_overview` — list of endpoints with method, path, purpose, request/response summaries
- `module_boundaries` — module names and responsibilities (maps to service layer)
- `domain_entities` — entity names and key fields (maps to repository layer)

### Fields Read from schema-design Output (Optional)

From `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (if it exists):

- Table definitions with column names, types, constraints, and relationships
- Used to ensure Pydantic models match database schema exactly

---

## Pre-Execution Verification

Before starting the main execution procedure, perform these checks:

**1. Validate task-spec file**
- [ ] File exists at the provided path
- [ ] File is valid YAML (no syntax errors)
- [ ] File contains all required sections: `metadata`, `output_contract`, `execution_plan`

**2. Derive workspace directory**
- From the task-spec path (e.g., `.ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml`):
  - Workspace dir = `.ssdam/{id}/` (extract from parent of parent)
  - Design output dir = `.ssdam/{id}/output/design/`

**3. Verify architecture-design output exists**
- [ ] Extract task_id from task-spec (TSK-NNN)
- [ ] Check `.ssdam/{id}/output/design/architecture-design.TSK-NNN.md` exists
- If NOT found: **STOP** and inform user: "architecture-design.TSK-NNN.md not found. Run /architecture-design first."

**4. Check for backend deliverables in output_contract**
- [ ] Examine `output_contract` entries for backend artifacts (REST API, service, middleware, etc.)
- If NO backend artifacts: **WARN** — "This task has no backend deliverables. Skipping backend-design."
- User may choose to proceed anyway; backend-design is optional if no backend work exists

**4b. Identify and exclude migration items from output_contract**
- [ ] Scan `output_contract` for any migration-related entries (keywords: Flyway, Liquibase, migration, `db/migration`, `V1__`, `.sql`)
- These items are **out of scope** for backend-design. They are handled by the schema-design step.
- In the Output Contract Traceability section of the output, mark these items as:
  `N/A — handled by schema-design`
- Do **NOT** create any migration sections, migration file paths, or Flyway/Liquibase instructions in the output document.

**5. Verify backend framework is configured**
- [ ] `execution_plan.tech_stack.backend` is set (not null or empty)
- If not: **STOP** and inform user: "Backend framework not configured in task-spec. Cannot design backend."

**6. Verify database is configured (if entities exist)**
- [ ] If architecture-design mentions domain_entities, check `execution_plan.tech_stack.database` is set
- If not: **WARN** — "Database not configured but entities are in scope. Proceeding, but schema-design may be incomplete."

**7. Check for schema-design output (optional)**
- [ ] Check if `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` exists
- [ ] If it exists, note that it will be read in Step 1 to align Pydantic models with database schema

**8. Create design output directory**
- [ ] Create `.ssdam/{id}/output/design/` if it does not exist
- [ ] Verify directory is writable

---

## Execution Procedure

Execute the following 7 steps in order. After each step, accumulate information to assemble the final output document.

### Step 1 — Load Inputs

**Action:** Parse all input files.

**Extract from task-spec.TSK-NNN.yaml and store:**
- `metadata.mission_id` → output metadata
- `metadata.task_id` → output metadata (derive NNN)
- `metadata.task_name` → output title
- `metadata.requirement_ids` → output traceability
- `output_contract` → list of deliverables (used for verification)
- `execution_plan.tech_stack.backend` → backend framework info
- `execution_plan.tech_stack.database` → database type
- `execution_plan.tech_stack.project_root` → project root path
- `execution_plan.steps[exec_type=="backend-design"]` → acceptance criteria

**Extract from architecture-design.TSK-NNN.md and store:**
- `api_contract_overview` → list of endpoints with method, path, purpose, request/response summaries
- `module_boundaries` → list of modules with responsibility and interfaces
- `domain_entities` → list of entities with key fields and relationships

**Extract from schema-design.TSK-NNN.sql (if present) and store:**
- Parse CREATE TABLE statements
- Extract table names, column names, types, constraints, relationships
- Store for alignment with Pydantic models

**Error handling:**
- If YAML parsing fails, report error and stop
- If architecture-design is missing or malformed, report which section is invalid
- If schema-design exists but is malformed SQL, warn but continue (schema-design may be incomplete)

---

### Step 2 — Define API Endpoints

**Action:** For each backend API hinted in architecture-design.api_contract_overview, produce a detailed endpoint specification.

**For each endpoint in api_contract_overview:**

Define:
- `method` — HTTP method (GET, POST, PUT, PATCH, DELETE)
- `path` — RESTful URL path (e.g., `/api/v1/media-files/{file_id}`)
- `description` — one sentence describing what the endpoint does
- `auth_required` — boolean (true if endpoint needs authentication)
- `request_schema` — Pydantic model name for request body (or "empty" if no body)
- `response_schema` — Pydantic model name for response body
- `status_codes` — HTTP status codes returned (200, 201, 400, 401, 404, 422, 500, etc.)
- `requirement_ids` — which REQ-NNN from output_contract this endpoint satisfies

**Example endpoint specification:**
```
Method: POST
Path: /api/v1/media-files
Description: Upload a new media file
Auth Required: true
Request Schema: MediaFileCreate
Response Schema: MediaFileResponse
Status Codes:
  Success: 201 Created
  Errors: 400 Bad Request, 401 Unauthorized, 422 Unprocessable Entity
Requirement IDs: REQ-001, REQ-002
```

**Validation:**
- Every endpoint must have both request and response schema defined
- If endpoint takes no request body, use a schema like `Empty` or mark "no body"
- All status codes must be sensible (don't invent codes like 218)

---

### Step 3 — Design Domain Layer

**Action:** For each domain in scope, define the pure Python domain objects. The domain layer has NO dependency on any framework (no FastAPI, no SQLModel, no SQLAlchemy imports).

Each domain (`auth`, `media`, `folder`, etc.) gets its own top-level directory containing the three layers (`domain/`, `api/`, `service/`).

#### 3a — Entities (`domain/entity/`) — **Mandatory**

For each domain entity (derived from architecture-design `domain_entities`):

Define:
- `entity_name` — PascalCase (e.g., `MediaFile`, `User`, `Folder`)
- `file` — `{domain}/domain/entity/{entity_name}.py`
- `fields` — list of fields with:
  - `name` — snake_case field name
  - `type` — Python type or Value Object type
  - `description` — one sentence

**Rules:**
- Entities are pure Python dataclasses or classes — no ORM decorators
- Identity is carried by a field (e.g., `id: UUID`)
- Use Value Objects (VOs) for fields that have domain rules (e.g., email, file size)

**Example:**
```
Entity: MediaFile
File: media/domain/entity/media_file.py
Fields:
  - id:         UUID
  - owner_id:   UUID
  - filename:   FileName (VO)
  - mime_type:  MimeType (VO)
  - size_bytes: FileSize (VO)
  - created_at: datetime
```

#### 3b — Value Objects (`domain/vo/`) — *Optional*

For each field with domain validation rules, define a Value Object:

Define:
- `vo_name` — PascalCase (e.g., `FileName`, `EmailAddress`, `FileSize`)
- `file` — `{domain}/domain/vo/{vo_name}.py`
- `wraps` — the primitive type it wraps (str, int, etc.)
- `validation_rules` — concrete rules enforced on construction
- `immutable` — always true; VOs must be frozen/immutable

**Example:**
```
VO: FileSize
File: media/domain/vo/file_size.py
Wraps: int
Validation: gt=0, le=10_485_760 (max 10 MB)
Immutable: true

VO: MimeType
File: media/domain/vo/mime_type.py
Wraps: str
Validation: pattern='^[a-z]+/[a-z0-9.+\-]+$'
Immutable: true
```

#### 3c — Domain Exceptions (`domain/exception/`) — *Optional*

Define all domain-specific exceptions. These are raised by domain logic, NOT by HTTP handlers.

- `file` — `{domain}/domain/exception/{exception_name}.py` or a single `exceptions.py`
- Map each exception to an HTTP status code (for the API mapper to use)

**Example:**
```
MediaFileNotFoundError    → 404
MediaFileForbiddenError   → 403
FileSizeLimitExceededError → 422
```

#### 3d — Domain Events (`domain/event/`) — *Optional*

For each significant state change in the domain, define a domain event:

- `event_name` — PascalCase past tense (e.g., `MediaFileUploaded`, `UserRegistered`)
- `file` — `{domain}/domain/event/{event_name}.py`
- `payload` — fields carried by the event

**Example:**
```
Event: MediaFileUploaded
File: media/domain/event/media_file_uploaded.py
Payload: { file_id: UUID, owner_id: UUID, filename: str, uploaded_at: datetime }
```

#### 3e — Domain Facade (`domain/facade/`) — **Mandatory**

Define the facade interface that the service layer uses to interact with the domain. This is the only entry point into the domain from the service layer.

- `facade_name` — `{Domain}Facade` (e.g., `MediaFacade`, `AuthFacade`)
- `file` — `{domain}/domain/facade/{domain}_facade.py`
- `methods` — list of domain operations (business logic only, no infrastructure)

**Example:**
```
Facade: MediaFacade
File: media/domain/facade/media_facade.py
Methods:
  - create_file(owner_id: UUID, filename: FileName, mime_type: MimeType, size: FileSize) → MediaFile
  - validate_ownership(file: MediaFile, user_id: UUID) → None  # raises ForbiddenError
  - mark_hidden(file: MediaFile) → MediaFile
```

#### 3f — Shared (`domain/shared/`) — *Optional*

Define base classes, mixins, or shared constants used across entities or VOs in this domain.

---

### Step 4 — Design API Layer

**Action:** For each domain, define the HTTP-facing layer. This layer translates between HTTP (FastAPI) and the domain facade. It has NO business logic.

#### 4a — Controllers (`api/controller/`) — **Mandatory**

For each group of endpoints (from Step 2), define a FastAPI router:

- `controller_name` — `{Domain}Router` (e.g., `MediaRouter`, `AuthRouter`)
- `file` — `{domain}/api/controller/{domain}_router.py`
- `prefix` — URL prefix (e.g., `/api/v1/media`)
- `endpoints` — list of handler functions, each mapping to one endpoint from Step 2
- For each handler: method, path, auth_required, request type, response type, facade method called

**Example:**
```
Controller: MediaRouter
File: media/api/controller/media_router.py
Prefix: /api/v1/media
Endpoints:
  - POST /              auth: true   request: MediaFileCreateRequest  response: MediaFileResponse  → facade.create_file()
  - GET  /{file_id}     auth: true   request: —                       response: MediaFileResponse  → facade.get_file()
  - DELETE /{file_id}   auth: true   request: —                       response: —                  → facade.delete_file()
```

#### 4b — Request DTOs (`api/request/`) — *Optional*

For each endpoint that accepts a request body, define a Pydantic request model:

- `file` — `{domain}/api/request/{name}.py`
- `fields` — name, Python type, required, validation, description

**Example:**
```
Request: MediaFileCreateRequest
File: media/api/request/media_file_create_request.py
Fields:
  - filename:   str   required=true  min_length=1, max_length=255
  - mime_type:  str   required=true  pattern='^[a-z]+/[a-z0-9.+\-]+$'
  - size_bytes: int   required=true  gt=0, le=10_485_760
  - tags:       Optional[List[str]]  max_length=5
```

#### 4c — Response DTOs (`api/response/`) — *Optional*

For each endpoint that returns data, define a Pydantic response model:

- `file` — `{domain}/api/response/{name}.py`
- `fields` — name, type, description

**Example:**
```
Response: MediaFileResponse
File: media/api/response/media_file_response.py
Fields:
  - id:         UUID
  - filename:   str
  - mime_type:  str
  - size_bytes: int
  - created_at: datetime
```

#### 4d — API Mapper (`api/mapper/`) — *Optional*

For each domain, define a mapper that converts between API DTOs and domain objects.

- `file` — `{domain}/api/mapper/{domain}_mapper.py`
- `methods`:
  - `to_domain(request_dto) → domain_object` — converts incoming request → domain input
  - `to_response(domain_object) → response_dto` — converts domain output → response DTO

**Example:**
```
Mapper: MediaMapper
File: media/api/mapper/media_mapper.py
Methods:
  - to_domain(req: MediaFileCreateRequest) → (FileName, MimeType, FileSize)
  - to_response(entity: MediaFile) → MediaFileResponse
```

---

### Step 5 — Design Service Layer

**Action:** For each domain, define the application service layer that orchestrates the domain facade, stores, and proxies. This layer is the glue between the domain and infrastructure.

#### 5a — Store (`service/store/`) — **Mandatory**

Store = the implementation class that holds data access methods. DAO (if separate) = the mapper interface it calls internally.

> **CRITICAL — Two distinct concepts:**
>
> | | `service/store/` | `service/store/dao/` |
> |---|---|---|
> | **What** | Store class — has methods with logic | DAO interface — method signatures only |
> | **How** | Implemented class (calls DAO or ORM directly) | Interface / mapper (no implementation body) |
> | **Described in design as** | Class with method list (name, params, return, description) | Interface with signature list only |
>
> **Do NOT describe the DAO interface as if it were a class with implementations.** DAO is a mapper interface — list its method signatures; the Store class is what has the logic.
>
> ```
> CORRECT package placement:
> {domain}/
> ├── domain/entity/          ← entities
> └── service/
>     └── store/              ← Store class here
>         └── dao/            ← DAO interface here (Java/MyBatis)
>
> WRONG:
> {domain}/
> ├── domain/entity/
> └── dao/                    ← ❌ NOT a sibling of domain/
> ```

For the Store class:
- `store_name` — `{Entity}Store` (e.g., `MediaFileStore`, `UserStore`)
- `file` — `{domain}/service/store/{entity}_store.py` (Python) or `{package}.service.store.{Entity}Store.java` (Java)
- `methods` — method name, params, return type, description

For the DAO interface (Java/MyBatis only, under `service/store/dao/`):
- `dao_name` — `{Entity}DAO{module}` per project naming convention
- `file` — `{package}.service.store.dao.{Entity}DAO{module}.java`
- `methods` — interface method signatures only (name + params + return type); no logic description

**Rules:**
- Store class has methods with descriptions
- DAO interface has signatures only — no implementation details belong in the design
- ORM models live inside `service/store/` — not in the domain layer
- No business logic in either layer — only data access

**Example (Java/MyBatis):**
```
Store: MediaFileStore
File: com.example.mediaasset.service.store.MediaFileStore
Methods:
  - findById(String id) → Optional<MediaFile>
  - findByUserId(String userId) → List<MediaFile>
  - save(MediaFile entity) → int

DAO Interface: MediaFileDAOmediaasset
File: com.example.mediaasset.service.store.dao.MediaFileDAOmediaasset
Signatures:
  - MediaFile selectById(String imageId)
  - List<MediaFile> selectByUserId(String userId)
  - int insert(MediaFile entity)
```

#### 5b — Proxy (`service/proxy/`) — *Optional*

Proxy = adapter for external services (file storage, email, payment gateway, etc.).

For each external integration:
- `proxy_name` — `{Service}Proxy` (e.g., `StorageProxy`, `EmailProxy`)
- `file` — `{domain}/service/proxy/{service}_proxy.py`
- `methods` — async methods that call the external service

**Example:**
```
Proxy: StorageProxy
File: media/service/proxy/storage_proxy.py
Methods:
  - upload(file_bytes: bytes, filename: str, mime_type: str) → str  (returns URL)
  - delete(file_url: str) → bool
```

#### 5c — Service Mapper (`service/mapper/`) — *Optional*

Converts between ORM objects (from store) and domain entities.

- `file` — `{domain}/service/mapper/{domain}_mapper.py`
- `methods`:
  - `to_domain(orm_obj) → domain_entity`
  - `to_orm(domain_entity) → orm_obj`

**Example:**
```
Mapper: MediaServiceMapper
File: media/service/mapper/media_mapper.py
Methods:
  - to_domain(orm: MediaFileORM) → MediaFile
  - to_orm(entity: MediaFile) → MediaFileORM
```

#### 5d — Application Service (orchestration) — *Optional*

The application service wires facade + stores + proxies together. It is called by the controller.

For each domain, define the application service:
- `service_name` — `{Domain}Service` (e.g., `MediaService`, `AuthService`)
- `file` — `{domain}/service/{domain}_service.py`
- `dependencies` — facade, stores, proxies, mappers injected
- `methods` — one method per use case (called by controller)

**Example:**
```
Service: MediaService
File: media/service/media_service.py
Dependencies: MediaFacade, MediaFileStore, StorageProxy, MediaServiceMapper

Methods:
  - create_file(session, owner_id: UUID, req: MediaFileCreateRequest) → MediaFileResponse
      1. mapper.to_domain(req) → (FileName, MimeType, FileSize)
      2. facade.create_file(owner_id, filename, mime_type, size) → MediaFile (domain)
      3. proxy.upload(file_bytes, ...) → url
      4. store.save(session, entity) → MediaFile
      5. api_mapper.to_response(entity) → MediaFileResponse

  - get_file(session, file_id: UUID, user_id: UUID) → MediaFileResponse
  - delete_file(session, file_id: UUID, user_id: UUID) → None
```

---

### Step 6 — Define Cross-Cutting Concerns

**Action:** Specify auth strategy, error handling, middleware, logging, and other system-wide concerns.

#### 6a — Authentication Strategy

Define:
- `auth_scheme` — e.g., "JWT Bearer token"
- `token_type` — e.g., "JWT"
- `token_location` — e.g., "Authorization header (Bearer token)"
- `token_payload` — what claims should the token contain (user_id, roles, etc.)
- `validation_method` — how to validate (e.g., "FastAPI Depends(get_current_user)")
- `scope` — protected vs. public endpoints

**Example:**
```
Auth Scheme: JWT Bearer Token
Token Type: JWT (JSON Web Token)
Token Location: Authorization header (Bearer token)
Token Payload: { sub: user_id, exp: timestamp, roles: [string] }
Validation Method: FastAPI Depends(get_current_user) in protected endpoints
Protected Endpoints: All endpoints with auth_required: true
Public Endpoints: e.g., POST /auth/login, GET /health
```

#### 6b — Error Handling Strategy

Define:
- `exception_classes` — custom exceptions to define:
  - Class name, HTTP status code, error message template
  - Examples: `ResourceNotFoundError` (404), `UnauthorizedError` (401), `ValidationError` (422)
- `http_mapping` — how each exception maps to HTTP status code
- `error_response_schema` — the structure of error responses returned to client

**Example:**
```
Custom Exceptions:
  - ResourceNotFoundError
    HTTP Status: 404 Not Found
    Message Template: "{entity_type} with ID {id} not found"

  - UnauthorizedError
    HTTP Status: 401 Unauthorized
    Message Template: "Invalid or missing credentials"

  - ForbiddenError
    HTTP Status: 403 Forbidden
    Message Template: "You do not have permission to access this resource"

Error Response Schema:
{
  "error_code": "RESOURCE_NOT_FOUND",
  "message": "MediaFile with ID abc123 not found",
  "status_code": 404,
  "timestamp": "2026-02-21T10:30:00Z"
}
```

#### 6c — Middleware Strategy

Define:
- `cors_enabled` — whether CORS headers are needed
- `cors_origins` — allowed origins (e.g., ["http://localhost:3000", "https://example.com"])
- `rate_limiting` — whether rate limiting is in scope (if mentioned in requirements)
- `logging_middleware` — whether to log all requests/responses

**Example:**
```
Middleware:
  - CORS: Enabled, Origins: [http://localhost:3000, https://example.com]
  - Rate Limiting: Disabled (not in scope)
  - Request Logging: Enabled (log method, path, status code, response time)
```

#### 6d — Logging Strategy

Define:
- `log_level` — what level of detail to log (DEBUG, INFO, WARNING, ERROR)
- `what_to_log` — for each endpoint:
  - Request: method, path, user_id (if auth'd), request size
  - Response: status code, response size, response time
  - Errors: full exception traceback, request context

---

### Step 7 — Test Strategy and File Structure

#### 7a — Test Strategy

Define:
- `unit_tests`:
  - What to test: service layer methods, Pydantic schema validation
  - How: mock repository, pytest fixtures
  - Location: `tests/unit/services/`, `tests/unit/schemas/`
  - Example tests: `test_create_media_file_success`, `test_create_media_file_validation_error`

- `integration_tests`:
  - What to test: API endpoints, auth flow, error handling
  - How: TestClient with test database, actual service/repository calls
  - Location: `tests/integration/api/`
  - Example tests: `test_post_media_files_success`, `test_post_media_files_unauthorized`

- `test_coverage`:
  - Aim for >80% coverage on service and repository layers
  - All error paths should be tested (not just happy path)

**Example test specifications:**
```
Unit Tests:
  - tests/unit/services/test_media_file_service.py
    - test_create_media_file_success
    - test_create_media_file_validation_error
    - test_get_media_file_not_found
    - test_delete_media_file_success

Integration Tests:
  - tests/integration/api/test_media_files.py
    - test_post_media_files_success (201 Created)
    - test_post_media_files_unauthorized (401)
    - test_get_media_file_success (200)
    - test_get_media_file_not_found (404)
    - test_delete_media_file_success (204)
```

#### 7b — File Structure

Define the expected DDD directory layout per domain. Each domain is a self-contained vertical slice.

**Example structure (auth + media domains):**
```
project_root/
├── auth/
│   ├── domain/
│   │   ├── entity/
│   │   │   └── user.py                        # User domain entity (pure Python)
│   │   ├── vo/
│   │   │   ├── email_address.py               # EmailAddress value object
│   │   │   └── password.py                    # Password value object (hashed)
│   │   ├── facade/
│   │   │   └── auth_facade.py                 # AuthFacade — domain interface for service layer
│   │   ├── event/
│   │   │   └── user_registered.py             # UserRegistered domain event
│   │   ├── exception/
│   │   │   └── exceptions.py                  # AuthDomainError, InvalidCredentialsError, ...
│   │   └── shared/
│   │       └── base_entity.py                 # Shared base classes for auth domain
│   ├── api/
│   │   ├── controller/
│   │   │   └── auth_router.py                 # FastAPI router: POST /auth/register, /auth/login
│   │   ├── dto/
│   │   │   └── auth_dto.py                    # Shared auth DTOs (if any)
│   │   ├── request/
│   │   │   ├── register_request.py            # RegisterRequest Pydantic model
│   │   │   └── login_request.py               # LoginRequest Pydantic model
│   │   ├── response/
│   │   │   ├── auth_response.py               # AuthResponse (token, user info)
│   │   │   └── user_response.py               # UserResponse
│   │   └── mapper/
│   │       └── auth_mapper.py                 # to_domain() / to_response()
│   └── service/
│       ├── store/
│       │   └── user_store.py                  # UserORM model + async DB queries
│       ├── proxy/
│       │   └── token_proxy.py                 # JWT token generation/validation
│       ├── config/
│       │   └── auth_config.py                 # Auth settings (secret, expiry, etc.)
│       ├── mapper/
│       │   └── user_mapper.py                 # to_domain(UserORM) / to_orm(User)
│       └── auth_service.py                    # AuthService — orchestrates facade + store + proxy
│
├── media/
│   ├── domain/
│   │   ├── entity/
│   │   │   └── media_file.py
│   │   ├── vo/
│   │   │   ├── file_name.py
│   │   │   ├── mime_type.py
│   │   │   └── file_size.py
│   │   ├── facade/
│   │   │   └── media_facade.py
│   │   ├── event/
│   │   │   └── media_file_uploaded.py
│   │   ├── exception/
│   │   │   └── exceptions.py
│   │   └── shared/
│   ├── api/
│   │   ├── controller/
│   │   │   └── media_router.py
│   │   ├── dto/
│   │   ├── request/
│   │   │   └── media_file_create_request.py
│   │   ├── response/
│   │   │   └── media_file_response.py
│   │   └── mapper/
│   │       └── media_mapper.py
│   └── service/
│       ├── store/
│       │   └── media_file_store.py
│       ├── proxy/
│       │   └── storage_proxy.py
│       ├── config/
│       │   └── media_config.py
│       ├── mapper/
│       │   └── media_mapper.py
│       └── media_service.py
│
├── shared/                                    # Cross-domain shared utilities
│   ├── db.py                                  # Async DB session setup
│   ├── dependencies.py                        # FastAPI Depends (get_current_user, get_session)
│   └── exceptions.py                          # HTTP exception handler registration
│
├── main.py                                    # FastAPI app init + router registration
├── tests/
│   ├── unit/
│   │   ├── auth/
│   │   └── media/
│   ├── integration/
│   │   ├── auth/
│   │   └── media/
│   └── conftest.py                            # pytest fixtures (test DB, TestClient)
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

### Step 7b — Final Verification

**Before writing the output file, verify:**

1. **Output Contract Traceability**
   - [ ] Every entry in `output_contract` is covered by at least one API endpoint OR marked `N/A — handled by schema-design`
   - [ ] Migration items (Flyway, Liquibase, `db/migration`, `.sql`) are marked N/A — NOT designed here
   - [ ] If output_contract mentions "REST API", check that all endpoints are defined in Step 2
   - [ ] If output_contract mentions "service", check that it appears in Step 4
   - [ ] If output_contract mentions "repository", check that it appears in Step 5
   - [ ] Output document contains NO migration sections, NO `db/migration/` paths, NO Flyway/Liquibase instructions

2. **Endpoint Completeness**
   - [ ] Every endpoint has both request and response schema defined
   - [ ] Every auth_required: true endpoint will use Depends(get_current_user)
   - [ ] Status codes are sensible (no invented codes)

3. **Schema Validation**
   - [ ] All field types are valid Python type hints
   - [ ] Validation rules are concrete (not vague like "valid email")
   - [ ] SQLModel fields match schema-design table columns exactly (if schema-design exists)

4. **DDD Layer Alignment**

   Mandatory (always verify):
   - [ ] Every domain has: `domain/entity/`, `domain/facade/`, `api/controller/`, `service/store/`
   - [ ] Domain layer (`domain/`) has no framework imports (no FastAPI, SQLModel, SQLAlchemy)
   - [ ] Application service (if present) only calls facade + stores + proxies; no direct ORM access

   Optional (verify only if included):
   - [ ] `domain/vo/` — VOs are immutable and self-validating
   - [ ] `domain/exception/` — domain exceptions are distinct from HTTP exceptions
   - [ ] `domain/event/` — event names are past-tense PascalCase
   - [ ] `service/mapper/` — `to_domain` / `to_orm` both defined
   - [ ] `api/mapper/` — `to_domain` / `to_response` both defined
   - [ ] `service/proxy/` — all proxy methods are `async def`

5. **Error Handling Completeness**
   - [ ] All error paths are defined (404, 401, 422, 500, etc.)
   - [ ] Custom exception classes cover all error scenarios
   - [ ] Error response schema is defined

6. **File Structure Validity**
   - [ ] All files listed exist or will be created
   - [ ] Directory structure is clear and follows Python conventions
   - [ ] No file path conflicts

**Error Handling for Verification:**
- If any verification fails, stop and fix the design before writing
- Log which verification(s) failed and what was fixed
- Example: "Verification failed: output_contract item 'MEDIA-DELETE-ENDPOINT' not covered. Added DELETE /api/v1/media-files/{file_id} endpoint."

---

## Post-Execution Summary

After successfully writing the output file, print a confirmation message:

```
✓ backend-design.TSK-NNN.md written to:
  .ssdam/{id}/output/design/backend-design.TSK-NNN.md

Summary:
  - N domains designed: [auth, media, ...]
  - N API endpoints defined
  - N domain entities + N value objects
  - N stores (data access) + N proxies (external services)
  - N application service methods
  - Error handling strategy: [brief summary]
  - Test strategy: [brief summary]

Verification:
  ✓ All output_contract entries covered
  ✓ Every domain has: entity + facade + controller + store (mandatory 4)
  ✓ Domain layer has no framework imports
  ✓ All auth_required endpoints use Depends(get_current_user)
  ✓ Optional components included only where needed

Next: run /backend-implementation <task-spec-path>
```

---

## Error Handling Reference

| Error | Condition | Action |
|-------|-----------|--------|
| **task-spec file not found** | File path does not exist | Stop execution. Report the full path attempted. |
| **Invalid YAML syntax** | YAML parser error | Stop execution. Report line number and parse error. |
| **architecture-design.TSK-NNN.md not found** | Prerequisite file missing | Stop execution. Run /architecture-design first. |
| **No backend deliverables in output_contract** | output_contract has no REST API or service entries | Warn user: "This task has no backend work. Skipping backend-design." (optional) |
| **Backend framework not configured** | `execution_plan.tech_stack.backend` is null or empty | Stop execution. Configure backend in task-spec. |
| **Endpoint defined without request schema** | API endpoint missing request_schema field | Add empty/placeholder schema and warn. |
| **Endpoint defined without response schema** | API endpoint missing response_schema field | Add empty/placeholder schema and warn. |
| **Schema references non-existent field type** | Type hint is not valid Python | Fix the type hint. Report which field. |
| **Service calls repository directly** | Service method implements DB logic instead of using repo | Refactor: move DB logic to repository. |
| **output_contract not fully traceable** | Deliverable has no corresponding endpoint/service/repository | Add missing endpoint/service/repo. Report which item. |
| **schema-design.TSK-NNN.sql exists but malformed** | SQL parsing fails | Warn but continue. Suggest user re-run schema-design. |

---

## Implementation Notes for the Agent

1. **Workspace Derivation:**
   - Input path: `.ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml`
   - Workspace: `.ssdam/media-marketplace-20260221-001/`
   - Design output dir: `.ssdam/media-marketplace-20260221-001/output/design/`
   - Output filename: `backend-design.TSK-001.md`

2. **Task ID Extraction:**
   - From filename `task-spec.TSK-NNN.yaml`, extract `NNN`
   - Use `NNN` in output filename: `backend-design.TSK-NNN.md`

3. **Validation is Strict:**
   - Pre-execution checks MUST pass before proceeding
   - Output verification MUST pass before writing
   - If any check fails, stop and report — do not work around

4. **Scope Coverage:**
   - Every output_contract entry must map to at least one endpoint
   - This is the proof that the backend design is complete

5. **Store/DAO Package Placement:**
   - Data access classes (DAO, Store, Repository) must ALWAYS live inside `service/store/` — never as a sibling of `domain/`
   - Common mistake: placing `dao/` at the same level as `domain/` — this is WRONG
   - Correct: `domain/` and `service/` are siblings; `service/store/dao/` is where DAOs go

5. **Next Steps:**
   - backend-implementation can run immediately after backend-design
