# backend-implementation Skill Rules and Patterns

This document defines the implementation rules that must be enforced when producing backend code.

---

## Core Implementation Rules

### Rule 1: Never Overwrite User Code (Mandatory)

**Do not overwrite existing files unless they were created by a previous backend-implementation run.**

- Before writing each file: check if it exists
- If the file exists and is NOT in backend-design.file_structure: **WARN** user and ask for confirmation
- If the file is a test file: allow overwriting (tests can be regenerated)
- If the file is a code file (src/): do NOT overwrite without explicit user permission

- Anti-pattern: Blindly overwriting project_root files, causing data loss

---

### Rule 2: All Repository Methods Must Be Async (Mandatory)

**Every repository method must be defined as `async def`, not `def`.**

```python
# CORRECT:
async def get_by_id(self, session: AsyncSession, file_id: UUID) -> Optional[MediaFile]:
    statement = select(MediaFile).where(MediaFile.id == file_id)
    result = await session.execute(statement)
    return result.scalars().first()

# WRONG:
def get_by_id(self, session: Session, file_id: UUID) -> MediaFile:
    return session.query(MediaFile).filter(...).first()
```

**Rationale:** Enables concurrent request handling in FastAPI. Synchronous code would block the event loop.

---

### Rule 3: Service Layer Isolation (Mandatory)

**Service methods MUST call repositories, never access database directly.**

```python
# CORRECT (service calls repository):
async def get_media_file(self, session, file_id, user_id):
    media = await self.repository.get_by_id(session, file_id)
    if not media:
        raise ResourceNotFoundError(...)
    if media.user_id != user_id:
        raise UnauthorizedError(...)
    return MediaFileResponse.from_orm(media)

# WRONG (direct DB access):
async def get_media_file(self, session, file_id, user_id):
    result = await session.execute(select(MediaFile).where(...))
    media = result.scalars().first()
    ...
```

**Rationale:** Business logic is separate from data access. Enables testing and mocking.

---

### Rule 4: Router Layer Calls Only Services (Mandatory)

**API routers MUST call services, never repositories or database directly.**

```python
# CORRECT (router calls service):
@router.post("/media/upload")
async def upload(file: UploadFile, current_user = Depends(get_current_user)):
    try:
        media = await service.create_media_file(session, data, current_user.user_id)
        return MediaFileResponse.from_orm(media)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

# WRONG (direct service/repo access):
@router.post("/media/upload")
async def upload(file: UploadFile):
    repo = MediaFileRepository()
    media = await repo.create(session, data)  # No service layer!
    return media
```

**Rationale:** Clean separation of concerns. Router handles HTTP, service handles business logic.

---

### Rule 5: Authentication Dependency Injection (Mandatory)

**All endpoints with auth_required: true MUST use `Depends(get_current_user)`.**

```python
# CORRECT:
@router.delete("/{file_id}")
async def delete_media(
    file_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),  # ← Required
    session: AsyncSession = Depends(get_session),
):
    await service.delete_media_file(session, file_id, current_user.user_id)

# WRONG:
@router.delete("/{file_id}")
async def delete_media(file_id: UUID, session: AsyncSession = Depends(get_session)):
    # No authentication!
    await service.delete_media_file(session, file_id, "hardcoded_user_id")
```

**Rationale:** Ensures consistent authentication on all protected endpoints. FastAPI manages token extraction and validation.

---

### Rule 6: Custom Exceptions, Not HTTPException (Mandatory)

**Raise custom exceptions in services and repositories, convert to HTTPException in routers.**

```python
# CORRECT (service raises custom exception):
class MediaFileService:
    async def get_media_file(self, session, file_id, user_id):
        media = await self.repository.get_by_id(session, file_id)
        if not media:
            raise ResourceNotFoundError(f"MediaFile {file_id} not found")  # Custom exception
        ...

# CORRECT (router catches and converts):
@router.get("/{file_id}")
async def get_media(file_id: UUID, current_user = Depends(get_current_user)):
    try:
        return await service.get_media_file(session, file_id, current_user.user_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)  # HTTP exception

# WRONG (direct HTTPException in service):
class MediaFileService:
    async def get_media_file(self, session, file_id, user_id):
        media = await self.repository.get_by_id(session, file_id)
        if not media:
            raise HTTPException(status_code=404, detail="Not found")  # Wrong layer!
```

**Rationale:** Services are framework-agnostic. HTTP is an implementation detail. Custom exceptions enable testing without HTTP.

---

### Rule 7: Pydantic Schemas for Request/Response (Mandatory)

**Never expose ORM models directly. Always use Pydantic schemas.**

```python
# CORRECT:
@router.get("/{file_id}")
async def get_media(...) -> MediaFileResponse:  # Pydantic schema as response
    media = await service.get_media_file(...)
    return MediaFileResponse.from_orm(media)  # Convert ORM to schema

# WRONG:
@router.get("/{file_id}")
async def get_media(...) -> MediaFile:  # Returning ORM model directly
    return await service.get_media_file(...)
```

**Rationale:** Pydantic validates response data. ORM models may expose internal fields (passwords, IDs, etc.).

---

### Rule 8: Async/Await Consistency (Mandatory)

**All I/O operations (DB, HTTP, file) must be async. Use await on async functions.**

```python
# CORRECT:
async def create_media_file(self, session: AsyncSession, data: MediaFileCreate):
    media = MediaFile(**data.dict())
    session.add(media)
    await session.commit()  # Await async operation
    await session.refresh(media)
    return media

# WRONG:
async def create_media_file(self, session: AsyncSession, data: MediaFileCreate):
    media = MediaFile(**data.dict())
    session.add(media)
    session.commit()  # No await! Blocking call
    session.refresh(media)
    return media
```

**Rationale:** Blocks the event loop and kills concurrency. AsyncSession requires await.

---

### Rule 9: Naming Conventions (Mandatory)

#### File Names (snake_case)
- `src/services/media_file_service.py` (not `MediaFileService.py`)
- `src/repositories/user_repository.py` (not `UserRepository.py`)
- `src/api/v1/media_files.py` (not `MediaFiles.py`)
- `tests/unit/services/test_media_file_service.py`

#### Class Names (PascalCase)
- `class MediaFileService:` (not `class media_file_service:`)
- `class MediaFileRepository:` (not `class media_file_repository:`)
- `class MediaFileCreate(BaseModel):` (Pydantic schema)
- `class ResourceNotFoundError(AppException):` (custom exception)

#### Method/Function Names (snake_case)
- `async def create_media_file(self, ...)`
- `async def get_by_owner(self, ...)`
- `async def delete_media_file(self, ...)`
- `def upload_media(...)` (FastAPI route handler)

#### Field Names (snake_case)
- `filename: str` (not `fileName`)
- `mime_type: str` (not `mimeType`)
- `size_bytes: int` (not `sizeBytes`)

---

### Rule 10: Documentation (Mandatory)

**All classes, methods, and functions must have docstrings.**

```python
class MediaFileService:
    """Service for media file operations."""

    async def create_media_file(
        self,
        session: AsyncSession,
        data: MediaFileCreate,
        user_id: UUID
    ) -> MediaFileResponse:
        """Create a new media file (upload).

        Args:
            session: Database session
            data: Media file create schema
            user_id: Owner user ID

        Returns:
            MediaFileResponse with created file metadata

        Raises:
            ValidationError: If file data is invalid
        """
        ...
```

**Rationale:** Code documentation enables understanding and maintenance. Docstrings are extracted by tools like Sphinx.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Synchronous Operations in Async Context

**WRONG:**
```python
async def get_media_file(self, session: AsyncSession, file_id: UUID):
    # session.execute() is synchronous — blocks event loop!
    result = session.execute(select(MediaFile).where(...))
    return result.scalars().first()
```

**CORRECT:**
```python
async def get_media_file(self, session: AsyncSession, file_id: UUID):
    result = await session.execute(select(MediaFile).where(...))
    return result.scalars().first()
```

---

### Anti-Pattern 2: Bare HTTPException

**WRONG:**
```python
class MediaFileService:
    async def get_media_file(self, file_id):
        media = await self.repo.get_by_id(file_id)
        if not media:
            raise HTTPException(status_code=404, detail="Not found")
```

**CORRECT:**
```python
class MediaFileService:
    async def get_media_file(self, file_id):
        media = await self.repo.get_by_id(file_id)
        if not media:
            raise ResourceNotFoundError(f"MediaFile {file_id} not found")
```

---

### Anti-Pattern 3: Exposing ORM Models in Responses

**WRONG:**
```python
@router.get("/{file_id}")
async def get_media(...) -> MediaFile:  # ORM model
    return await service.get_media_file(file_id)
```

**CORRECT:**
```python
@router.get("/{file_id}")
async def get_media(...) -> MediaFileResponse:  # Pydantic schema
    media = await service.get_media_file(file_id)
    return MediaFileResponse.from_orm(media)
```

---

### Anti-Pattern 4: Hardcoded Configuration

**WRONG:**
```python
DATABASE_URL = "postgresql://localhost/mydb"
SECRET_KEY = "my-secret-key"
```

**CORRECT:**
```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/mydb")
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

### Anti-Pattern 5: Missing Pagination on List Endpoints

**WRONG:**
```python
@router.get("/media")
async def list_media() -> List[MediaFileResponse]:
    return await service.get_all_media()  # Could return millions!
```

**CORRECT:**
```python
@router.get("/media")
async def list_media(
    skip: int = 0,
    limit: int = 20
) -> PaginatedResponse[MediaFileResponse]:
    items = await service.get_all_media(skip=skip, limit=limit)
    return PaginatedResponse(items=items, skip=skip, limit=limit)
```

---

### Anti-Pattern 6: No Error Handling in Tests

**WRONG:**
```python
@pytest.mark.asyncio
async def test_get_media(test_session):
    result = await service.get_media_file(test_session, uuid4(), user_id)
    # What if file not found? Test fails without clear error message
```

**CORRECT:**
```python
@pytest.mark.asyncio
async def test_get_media_not_found(test_session):
    with pytest.raises(ResourceNotFoundError):
        await service.get_media_file(test_session, uuid4(), user_id)
```

---

## Testing Requirements

### Unit Test Coverage (Mandatory)

- **Target:** >80% coverage on service and repository layers
- **Scope:** Test business logic, not HTTP layer
- **Mocking:** Mock repository to isolate service layer
- **Scenarios:** Happy path + error cases

**Example unit test:**
```python
@pytest.mark.asyncio
async def test_delete_media_file_unauthorized(test_session, media_service):
    """Test deleting media file owned by another user."""
    owner_id = uuid4()
    user_id = uuid4()

    # Create file for owner_id
    file = await media_service.create_media_file(
        test_session,
        MediaFileCreate(filename="test.png", mime_type="image/png", size_bytes=1024),
        owner_id
    )

    # Try to delete with different user_id
    with pytest.raises(UnauthorizedError):
        await media_service.delete_media_file(test_session, file.id, user_id)
```

### Integration Test Coverage (Mandatory)

- **Target:** All endpoints covered
- **Scope:** Test HTTP layer (status codes, request/response validation)
- **Database:** Use test database (fixtures from conftest.py)
- **Scenarios:** Success + common error cases (401, 404, 422)

**Example integration test:**
```python
def test_delete_media_file_success(auth_token, test_file_id):
    """Test successful media file deletion."""
    response = client.delete(
        f"/api/v1/media/{test_file_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204
```

---

## Code Quality Standards

### Documentation

- [ ] All classes have docstrings
- [ ] All methods have docstrings with Args, Returns, Raises
- [ ] All public functions have docstrings
- [ ] TODO comments mark unfinished work (with context)

### Naming

- [ ] File names are snake_case
- [ ] Class names are PascalCase
- [ ] Method names are snake_case
- [ ] Variable names are snake_case
- [ ] Constants are UPPERCASE_WITH_UNDERSCORES

### Error Handling

- [ ] No bare `except Exception:`
- [ ] Custom exceptions for domain errors
- [ ] HTTPException converted from custom exceptions in routers
- [ ] All error paths tested

### Testing

- [ ] All services have unit tests
- [ ] All endpoints have integration tests
- [ ] All error scenarios are tested
- [ ] Tests use pytest fixtures for setup
- [ ] Tests are named descriptively (test_method_scenario)

### Async/Await

- [ ] All I/O operations are async
- [ ] No blocking calls in async functions
- [ ] AsyncSession used in repositories
- [ ] All calls to async functions use await

---

## Implementation Checklist

Before considering implementation complete:

- [ ] All files from backend-design.file_structure are created
- [ ] All endpoints are implemented with correct method, path, auth
- [ ] All request/response schemas are defined with validation
- [ ] All services use repositories (no direct DB access)
- [ ] All repositories use AsyncSession and async methods
- [ ] All error scenarios raise custom exceptions
- [ ] All auth_required endpoints use Depends(get_current_user)
- [ ] All tests pass (unit + integration)
- [ ] Code follows naming conventions
- [ ] All classes/methods have docstrings
- [ ] No hardcoded secrets or configuration
- [ ] All acceptance criteria from task-spec are satisfied

---

## Notes for Cursor AI Agent

1. **Autonomous execution** — you are writing real code, not a design document.

2. **Dependency order matters** — follow the implementation order in SKILL.md:
   - Schemas → Exceptions → ORM models → Repositories → Services → Middleware → Routes → Main app

3. **Testing is non-negotiable** — all tests must pass before considering implementation complete.

4. **Verify acceptance criteria** — check every criterion from task-spec.execution_plan.steps[exec_type=="backend-implementation"].acceptance_criteria

5. **TODOs are expected** — mark incomplete functionality with TODO comments and continue. Examples:
   - "TODO: Upload file to S3"
   - "TODO: Implement email notifications"
   - "TODO: Add caching layer"

6. **Configuration is external** — use .env files for all sensitive data. Never hardcode:
   - Database URLs
   - API keys
   - Secret keys
   - CORS origins
   - Any credentials

7. **Documentation is code** — docstrings are part of the specification. Maintain clarity.

8. **Error handling must be tested** — test not just success cases, but all error scenarios:
   - 401 Unauthorized (missing/invalid token)
   - 403 Forbidden (user lacks permission)
   - 404 Not Found (resource doesn't exist)
   - 422 Unprocessable Entity (validation error)

9. **Keep code simple** — follow the patterns in this document. Don't over-engineer.

10. **Ask for confirmation on conflicts** — if a file exists and might be user code, ask before overwriting.
