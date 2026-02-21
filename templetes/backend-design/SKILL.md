---
name: backend-design
description: Backend-specialised design skill in the SSDAM pipeline. Reads architecture-design (and optionally schema-design) to produce a detailed backend specification: API endpoints, request/response schemas, service/repo layers, error handling, and test plan. Its output drives backend-implementation.
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

### Step 3 — Define Pydantic Request/Response Schemas

**Action:** For each unique schema referenced in Step 2, produce a detailed Pydantic model specification.

**For each schema (request or response):**

Define:
- `schema_name` — PascalCase name (e.g., `MediaFileCreate`, `MediaFileResponse`, `ErrorResponse`)
- `schema_type` — "request", "response", or "base" (base = reusable in multiple contexts)
- `fields` — list of fields with:
  - `name` — snake_case field name
  - `type` — Python type hint (str, int, UUID, Optional[str], List[str], etc.)
  - `required` — boolean (true if field has no default)
  - `validation` — optional validation rules (min_length, max_length, regex, pattern, etc.)
  - `description` — one sentence describing the field

**Example schema specification:**
```
Schema Name: MediaFileCreate
Schema Type: request
Fields:
  - name: filename
    type: str
    required: true
    validation: "min_length=1, max_length=255"
    description: "Name of the uploaded file"

  - name: mime_type
    type: str
    required: true
    validation: "pattern='^[a-z]+/[a-z0-9\\.\\+\\-]+$'"
    description: "MIME type of the file (e.g., image/png)"

  - name: size_bytes
    type: int
    required: true
    validation: "gt=0, le=10485760"
    description: "File size in bytes (max 10MB)"

  - name: tags
    type: Optional[List[str]]
    required: false
    validation: "max_length=5"
    description: "Optional list of tags (max 5)"
```

**Naming conventions:**
- Request schemas: `<Entity>Create`, `<Entity>Update`, `<Entity>Search`
- Response schemas: `<Entity>Response`, `<Entity>DetailResponse`
- Base schemas (reusable): `<Entity>Base`
- Error schema: `ErrorResponse`

**SQLModel alignment:**
- If schema-design exists and table definition matches this entity, create SQLModel ORM model
- Example: `MediaFile` (base schema) → `media_files` table → Pydantic schema + SQLModel ORM model
- Ensure field names and types match the schema-design table definition exactly

---

### Step 4 — Design Service Layer

**Action:** For each logical service (corresponding to a module from architecture-design), define the service class and methods.

**For each service (derived from architecture-design.module_boundaries):**

Define:
- `service_name` — PascalCase, e.g., `MediaFileService`
- `file` — where it will be implemented, e.g., `src/services/media_file_service.py`
- `responsibility` — one sentence (from architecture-design module responsibility)
- `methods` — list of public methods with:
  - `name` — snake_case method name
  - `params` — list of parameter names and types (e.g., `file_id: UUID, user_id: UUID`)
  - `return_type` — what the method returns (e.g., `MediaFileResponse`, `List[MediaFileResponse]`)
  - `description` — one sentence describing what the method does
- `dependencies` — list of injected dependencies (repositories, other services, etc.)

**Example service specification:**
```
Service Name: MediaFileService
File: src/services/media_file_service.py
Responsibility: Manage media file operations (create, retrieve, update, delete)

Methods:
  - name: create_media_file
    params: file_id: UUID, user_id: UUID, data: MediaFileCreate
    return_type: MediaFileResponse
    description: "Create a new media file entry in the database"

  - name: get_media_file
    params: file_id: UUID, user_id: UUID
    return_type: MediaFileResponse
    description: "Retrieve a media file by ID (verify user ownership)"

  - name: delete_media_file
    params: file_id: UUID, user_id: UUID
    return_type: bool
    description: "Delete a media file (verify user ownership)"

Dependencies:
  - MediaFileRepository (for DB access)
  - StorageService (for file deletion from S3/local storage)
```

**Design rules:**
- Service layer MUST NOT directly access database (only via repository)
- Service layer SHOULD NOT raise HTTPException (only business exceptions)
- Every service method should validate inputs and business logic
- Service methods are async (async def)

---

### Step 5 — Design Repository Layer

**Action:** For each DB entity this task works with, define the repository class and methods.

**For each repository (one per domain entity):**

Define:
- `repo_name` — PascalCase, e.g., `MediaFileRepository`
- `entity` — the ORM model this repo manages (e.g., `MediaFile`)
- `file` — where it will be implemented, e.g., `src/repositories/media_file_repository.py`
- `methods` — list of data access methods with:
  - `name` — snake_case method name
  - `params` — list of parameter names and types
  - `return_type` — what the method returns (ORM model, list, or scalar)
  - `query_type` — "select", "insert", "update", "delete", or "custom"
  - `description` — one sentence

**Example repository specification:**
```
Repository Name: MediaFileRepository
Entity: MediaFile (ORM model)
File: src/repositories/media_file_repository.py

Methods:
  - name: create
    params: session: AsyncSession, data: MediaFileCreate
    return_type: MediaFile
    query_type: insert
    description: "Create a new media file record"

  - name: get_by_id
    params: session: AsyncSession, file_id: UUID
    return_type: Optional[MediaFile]
    query_type: select
    description: "Retrieve a media file by ID"

  - name: get_by_owner
    params: session: AsyncSession, user_id: UUID
    return_type: List[MediaFile]
    query_type: select
    description: "Retrieve all media files owned by a user"

  - name: delete
    params: session: AsyncSession, file_id: UUID
    return_type: bool
    query_type: delete
    description: "Delete a media file by ID"
```

**Design rules:**
- Repository is the ONLY place where DB queries occur
- All repository methods are async (async def)
- Use SQLAlchemy AsyncSession for async operations
- No business logic in repository (just CRUD and queries)
- Custom methods (beyond CRUD) are common for domain-specific queries

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

Define the expected directory layout for this task's backend code:

**Example structure:**
```
project_root/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── media_files.py        # FastAPI router for media endpoints
│   │       └── auth.py               # FastAPI router for auth endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── media_file_service.py    # Business logic
│   │   └── auth_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── media_file_repository.py # DB access
│   │   └── user_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py               # Pydantic request/response schemas
│   │   ├── db.py                    # SQLModel ORM models
│   │   └── exceptions.py            # Custom exception classes
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py                  # Auth middleware (get_current_user)
│   ├── main.py                      # FastAPI app initialization
│   └── config.py                    # Config and settings
├── migrations/
│   └── versions/                    # Alembic migration files
├── tests/
│   ├── unit/
│   │   ├── services/
│   │   └── schemas/
│   ├── integration/
│   │   └── api/
│   ├── fixtures/
│   │   └── conftest.py              # pytest fixtures (test DB, TestClient, etc.)
│   └── __init__.py
├── requirements.txt
├── pytest.ini
└── .env.example
```

**Per-file descriptions:**
- `src/api/v1/media_files.py` — FastAPI routers for `/api/v1/media-files` endpoints
- `src/services/media_file_service.py` — Service class with business logic
- `src/repositories/media_file_repository.py` — Repository class with DB queries
- `src/models/schemas.py` — Pydantic request/response schemas
- `src/models/db.py` — SQLModel ORM models
- `src/models/exceptions.py` — Custom exception classes
- `src/middleware/auth.py` — get_current_user dependency function
- `tests/unit/services/test_media_file_service.py` — Unit tests (mocked repo)
- `tests/integration/api/test_media_files.py` — Integration tests (real endpoints)

---

### Step 7b — Final Verification

**Before writing the output file, verify:**

1. **Output Contract Traceability**
   - [ ] Every entry in `output_contract` is covered by at least one API endpoint
   - [ ] If output_contract mentions "REST API", check that all endpoints in output_contract are defined in Step 2
   - [ ] If output_contract mentions "service", check that it appears in Step 4
   - [ ] If output_contract mentions "repository", check that it appears in Step 5

2. **Endpoint Completeness**
   - [ ] Every endpoint has both request and response schema defined
   - [ ] Every auth_required: true endpoint will use Depends(get_current_user)
   - [ ] Status codes are sensible (no invented codes)

3. **Schema Validation**
   - [ ] All field types are valid Python type hints
   - [ ] Validation rules are concrete (not vague like "valid email")
   - [ ] SQLModel fields match schema-design table columns exactly (if schema-design exists)

4. **Service/Repository Alignment**
   - [ ] Every service method that needs DB access calls a repository method
   - [ ] Every entity from architecture-design has a corresponding repository
   - [ ] Repository methods don't contain business logic (only CRUD)

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
  - N API endpoints defined
  - N Pydantic schemas defined
  - N service methods defined
  - N repository methods defined
  - Error handling strategy: [brief summary]
  - Test strategy: [brief summary]

Verification:
  ✓ All output_contract entries covered
  ✓ All endpoints have request/response schemas
  ✓ All services have corresponding repositories
  ✓ All auth_required endpoints use Depends(get_current_user)

Next: run /backend-implementation <task-spec-path>
  (or verify schema-design.TSK-NNN.sql if database changes are needed)
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

5. **Next Steps:**
   - backend-implementation can run immediately after backend-design
   - If schema-design was run, backend implementation can use those migrations
   - If schema-design was not run, backend-implementation may create basic SQLModel models
