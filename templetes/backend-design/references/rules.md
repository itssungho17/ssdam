# backend-design Skill Rules and Anti-Patterns

This document defines the design rules that must be enforced when producing a backend-design output.

---

## Core Design Rules

### Rule 1: Output Contract Traceability (Mandatory)

**Every entry in `output_contract` must map to at least one API endpoint.**

- If output_contract mentions "REST API with endpoints: POST /media/upload, GET /media/{id}", then:
  - Step 2 (API Endpoints) must define both endpoints
  - Step 3 (Schemas) must define request/response schemas for both
  - Step 4 (Services) must include the service method(s) that handle these endpoints

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

### Rule 3: Service Layer Isolation (Mandatory)

**Service layer must NOT directly access the database. All DB access goes through repositories.**

- Service method implementation detail:
  ```python
  # CORRECT:
  async def create_media_file(self, data: MediaFileCreate):
    return await self.media_repo.create(self.session, data)

  # WRONG:
  async def create_media_file(self, data: MediaFileCreate):
    db.session.add(MediaFile(...))  # Direct DB access
    db.session.commit()
  ```

- Rationale: Separating business logic (service) from data access (repository) enables testing, mocking, and future database changes.

- Verification: In Step 5 verification, check that every service method calls only repository methods or external services, never direct DB queries.

- Anti-pattern: Service method contains SQLAlchemy queries, ORM session manipulation, or database locks.

---

### Rule 4: Repository Methods Must Be Async (Mandatory)

**Every repository method must be defined as `async def` (not `def`).**

- This enables concurrent request handling in FastAPI.

- Example:
  ```python
  # CORRECT:
  async def get_by_id(self, session: AsyncSession, file_id: UUID) -> Optional[MediaFile]:
    ...

  # WRONG:
  def get_by_id(self, session: Session, file_id: UUID) -> MediaFile:
    ...
  ```

- Verification: In Step 5, check that all repository method signatures include `async def`.

- Anti-pattern: Synchronous repository methods (blocking calls in async context).

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

**Follow Python and FastAPI naming standards.**

#### File Naming (snake_case)
- Router files: `src/api/v1/media_files.py` (not `MediaFiles.py`)
- Service files: `src/services/media_file_service.py` (not `MediaFileService.py`)
- Repository files: `src/repositories/media_file_repository.py` (not `MediaFileRepository.py`)

#### Class Naming (PascalCase)
- Service classes: `MediaFileService` (not `media_file_service`)
- Repository classes: `MediaFileRepository` (not `media_file_repository`)
- Pydantic schemas: `MediaFileCreate`, `MediaFileResponse` (not `media_file_create`)
- Exception classes: `ResourceNotFoundError` (not `resource_not_found_error`)

#### Method/Function Naming (snake_case)
- Service methods: `create_media_file()`, `get_by_owner()`, `delete_media_file()`
- Repository methods: `create()`, `get_by_id()`, `filter_by_owner()`
- Router endpoints: `@router.post("/upload")` def `upload_media()`

#### Field Naming (snake_case)
- Pydantic fields: `file_name`, `mime_type`, `size_bytes` (not `fileName`, `mimeType`)
- Database columns: `file_name`, `mime_type`, `size_bytes` (from schema-design)

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

#### Anti-Pattern 2: Direct DB Queries in Repository

**WRONG:**
```python
class MediaFileRepository:
    async def get_by_owner(self, user_id: UUID):
        # Mixing query logic with repository logic
        return session.query(MediaFile).filter(MediaFile.user_id == user_id).all()
```

**CORRECT:**
```python
class MediaFileRepository:
    async def get_by_owner(self, session: AsyncSession, user_id: UUID):
        result = await session.execute(
            select(MediaFile).where(MediaFile.user_id == user_id)
        )
        return result.scalars().all()
```

#### Anti-Pattern 3: Missing Error Handling

**WRONG:**
```python
async def get_media_file(file_id: UUID):
    # No error handling — what if file not found?
    media = await media_repo.get_by_id(session, file_id)
    return media
```

**CORRECT:**
```python
async def get_media_file(file_id: UUID):
    media = await media_repo.get_by_id(session, file_id)
    if not media:
        raise ResourceNotFoundError(f"MediaFile {file_id} not found")
    return media
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

---

## Design Quality Checklist

Before declaring a backend-design complete, verify:

- [ ] **Scope**: All output_contract entries are covered by endpoints
- [ ] **Schemas**: Every endpoint has request and response schemas defined
- [ ] **Services**: Service methods use repositories, not direct DB access
- [ ] **Repositories**: All methods are async
- [ ] **Auth**: Protected endpoints use Depends(get_current_user)
- [ ] **Exceptions**: Custom exception classes are defined for all error scenarios
- [ ] **Naming**: All files, classes, methods, and fields follow conventions
- [ ] **Anti-patterns**: No business logic in routers, no direct DB access outside repos
- [ ] **File Structure**: All files are planned and don't conflict
- [ ] **Tests**: Unit and integration test plans cover happy path and error cases
- [ ] **Documentation**: Each endpoint, service, and repository has a description

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

### Schema Usage Verification

After Step 3, verify:

- [ ] Every schema used in an endpoint is defined in Step 3 output
- [ ] No undefined schema references
- [ ] All fields in each schema are concrete (no "something", "data", etc.)

### Service/Repository Alignment

After Step 5, verify:

- [ ] Every service method that needs DB access calls a repository method
- [ ] Every repository method is called by at least one service method (or is a custom query)
- [ ] No service method directly manipulates ORM objects or sessions

---

## Notes for Cursor AI Agent

1. **Validation is strict** — if any rule is violated, fix it before writing the output.
2. **Traceability is mandatory** — the ability to trace from output_contract to endpoint to code is proof the design is complete.
3. **Anti-patterns are common** — watch for them during design; they are easy to miss.
4. **Naming matters** — consistent naming makes the code easier to understand and implement.
5. **Self-validation is not optional** — the output file must include a self-validation section showing all checks passed.
