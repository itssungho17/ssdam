---
name: backend-implementation
description: Final backend step in the SSDAM execution chain. Reads backend-design and directly implements the backend code (FastAPI routes, services, repositories, migrations, tests) in the project root. This skill is for Cursor AI agent autonomous execution.
compatibility: Cursor AI agent (autonomous code execution)
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# backend-implementation Skill

## File Paths Reference

This skill reads from the design outputs and writes code directly to the project root:

```
task-spec.TSK-NNN.yaml (user provides path)
  + backend-design.TSK-NNN.md (required — from .ssdam/{id}/output/design/)
  + schema-design.TSK-NNN.sql (optional — if data-modeling was run)
  ↓
[backend-implementation]  ← YOU ARE HERE
  ↓
Code written directly to project_root/:
  src/api/       ← FastAPI routes (routers)
  src/services/  ← service layer (business logic)
  src/repositories/ ← repository layer (data access)
  src/models/    ← Pydantic schemas + SQLModel ORM models
  migrations/    ← Alembic database migrations
  tests/         ← unit and integration tests
```

**Skill files (read-only):**
- `/mnt/ssdam/templetes/backend-implementation/SKILL.md` (this file)
- `/mnt/ssdam/templetes/backend-implementation/references/input.template.yaml` (input schema reference)
- `/mnt/ssdam/templetes/backend-implementation/references/output.template.yaml` (output schema reference)
- `/mnt/ssdam/templetes/backend-implementation/references/rules.md` (implementation rules and patterns)

**Runtime files (inputs):**
- Input 1: `task-spec.TSK-NNN.yaml` (user provides path)
- Input 2: `.ssdam/{id}/output/design/backend-design.TSK-NNN.md` (required — detailed specification)
- Input 3: `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (optional — schema migrations)

**Output files (created in project_root):**
- Code files as specified in backend-design.file_structure
- No design document output — the implementation IS the output

---

## Overview

| | |
|---|---|
| **Trigger** | `/backend-implementation <task-spec-path>` |
| **Prerequisites** | `backend-design.TSK-NNN.md` must exist; optionally `schema-design.TSK-NNN.sql` |
| **Input** | task-spec.TSK-NNN.yaml + backend-design output + (optional) schema-design output |
| **Work** | Read backend-design specification and implement all code (routes, services, repositories, models, migrations, tests) |
| **Output** | Code files written directly to project_root (no design document) |
| **Scope** | This is an autonomous code execution skill for Cursor AI agents |

---

## Input Specification

### Trigger Command

```
/backend-implementation <task-spec-path>
```

**Example:**
```
/backend-implementation .ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml
```

### Fields Read from task-spec

From `task-spec.TSK-NNN.yaml`:

**From `metadata`:**
- `task_id` — for logging and traceability
- `task_name` — for logging and documentation
- `requirement_ids` — for code comments and test names

**From `execution_plan`:**
- `tech_stack.backend` — what framework and libraries to use
- `tech_stack.database` — database type (PostgreSQL, MySQL, etc.)
- `tech_stack.project_root` — where to write code
- `steps[]` where `exec_type == "backend-implementation"`: acceptance_criteria (defines success)

### Fields Read from backend-design Output

From `.ssdam/{id}/output/design/backend-design.TSK-NNN.md`:

- `api_endpoints` — all endpoints to implement (method, path, auth, schemas, status codes)
- `schemas` — all Pydantic request/response schemas
- `services` — all service classes with methods
- `repositories` — all repository classes with DB methods
- `error_handling` — custom exception classes and HTTP mapping
- `authentication` — JWT validation strategy
- `middleware` — CORS, rate limiting, logging
- `file_structure` — where each file should be created
- `test_strategy` — what unit and integration tests to write

### Fields Read from schema-design Output (Optional)

From `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (if it exists):

- CREATE TABLE statements
- Used to generate Alembic migrations (if database schema changes are needed)

---

## Pre-Execution Verification

Before starting implementation, perform these checks:

**1. Validate task-spec file**
- [ ] File exists at the provided path
- [ ] File is valid YAML (no syntax errors)
- [ ] File contains all required sections: `metadata`, `execution_plan`

**2. Derive workspace and project directories**
- From the task-spec path: extract workspace directory and project_root
- Example: task-spec at `.ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml`
  - Workspace: `.ssdam/media-marketplace-20260221-001/`
  - Project root: from `execution_plan.tech_stack.project_root`

**3. Verify backend-design output exists**
- [ ] Extract task_id from task-spec (TSK-NNN)
- [ ] Check `.ssdam/{id}/output/design/backend-design.TSK-NNN.md` exists
- If NOT found: **STOP** and inform user: "backend-design.TSK-NNN.md not found. Run /backend-design first."

**4. Parse backend-design thoroughly**
- [ ] Load all sections: api_endpoints, schemas, services, repositories, error_handling, file_structure, test_strategy
- If any critical section is empty or malformed: **STOP** and report which section is invalid

**5. Verify project_root is writable**
- [ ] Check that project_root directory exists or can be created
- [ ] Verify write permissions on project_root
- [ ] Create required directories (src/, tests/, migrations/) if they don't exist
- If project_root is not writable: **STOP** and report permission error

**6. Scan existing files and build UPDATE / CREATE plan**

For every file listed in backend-design.file_structure, check whether it already exists at the target path.

| File exists? | Same role / class name inside? | Action |
|---|---|---|
| No | — | **CREATE** — write the new file |
| Yes | No matching class/function found | **APPEND** — add the new class/function to the existing file |
| Yes | Matching class/function found | **UPDATE** — modify only the relevant class/function inside the existing file |

**Rules:**
- **NEVER create a new file with a different name if a file with the same role already exists at the target path.**
- **NEVER leave the old class unchanged and add a duplicate alongside it.**
- If a class named `UserService` already exists at `service/user_service.py`, modify that class — do NOT create `service/user_service_v2.py` or `service/user_service_new.py`.
- If a method inside an existing class needs to change, edit only that method — leave all other methods intact.

**How to detect "same role":**
- Same file path as specified in backend-design.file_structure → it is the same file
- Inside the file, look for a class/function whose name matches what backend-design expects → it is the same class/function

**Log the plan before starting:**
```
File scan complete:
  CREATE  src/domain/entity/Tag.java          (new file)
  UPDATE  src/domain/entity/User.java         (file exists — will modify class User)
  APPEND  src/service/store/dao/UserDAO.java  (file exists — will add method selectByEmail)
```

**7. Check for schema-design output (optional)**
- [ ] Check if `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` exists
- [ ] If it exists, parse CREATE TABLE statements to generate migrations
- If not present: proceed without database migrations (assume schema already exists or is not needed)

---

## Execution Procedure

Execute the following 8 steps in order. Steps 1-7 implement code; Step 8 verifies and tests.

### Step 1 — Load Inputs and Create Implementation Plan

**Action:** Parse all input files and create an ordered implementation plan.

**Extract from task-spec.TSK-NNN.yaml:**
- `metadata.task_id` → for logging and file naming
- `metadata.task_name` → for logging and documentation
- `execution_plan.tech_stack.backend` → framework (FastAPI), ORM (SQLModel), auth (JWT)
- `execution_plan.tech_stack.database` → database type (PostgreSQL)
- `execution_plan.tech_stack.project_root` → where to write code
- `execution_plan.steps[exec_type=="backend-implementation"].acceptance_criteria` → success criteria

**Load backend-design.TSK-NNN.md fully:**
- Parse all sections: api_endpoints, schemas, services, repositories, error_handling, authentication, middleware, file_structure, test_strategy
- Build in-memory data structures (dicts/objects) for each component

**Create implementation plan:**

For each file in backend-design.file_structure, apply the scan result from Pre-Execution Step 6 to tag each item as CREATE, UPDATE, or APPEND. Build the ordered plan:

```
Implementation plan for TSK-NNN:
  [CREATE] src/domain/entity/Tag.java                 — new entity class
  [UPDATE] src/domain/entity/User.java                — add field `profileImageUrl`
  [APPEND] src/service/store/dao/UserDAO.java         — add method `selectByEmail()`
  [CREATE] src/service/store/UserStore.java           — new store class
  [UPDATE] src/service/UserService.java               — update `createUser()` method
  ...
```

**Dependency order (always follow regardless of CREATE/UPDATE):**
1. Domain entities (`domain/entity/`)
2. Domain facades (`domain/facade/`) — if present
3. Request/Response DTOs (`api/request/`, `api/response/`) — if present
4. DAO interfaces (`service/store/dao/`) — signatures only
5. Store classes (`service/store/`)
6. Application service (`service/`) — if present
7. Controllers (`api/controller/`)

**Critical rule — log before executing:**
Print the full CREATE/UPDATE/APPEND plan and confirm there are no duplicate-role files before writing a single line of code.

---

### Step 2 — Set Up File Structure

**Action:** Create all directories and __init__.py files as defined in backend-design.file_structure.

**For each directory in file_structure:**
- Create the directory if it does not exist
- Create an empty `__init__.py` file to make it a Python package

**Example directories to create:**
```
project_root/src/
project_root/src/api/
project_root/src/api/v1/
project_root/src/models/
project_root/src/services/
project_root/src/repositories/
project_root/src/middleware/
project_root/migrations/
project_root/migrations/versions/
project_root/tests/
project_root/tests/unit/
project_root/tests/unit/services/
project_root/tests/integration/
project_root/tests/integration/api/
project_root/tests/fixtures/
```

**Error handling:**
- If directory creation fails (permission denied, disk full, etc.): **STOP** and report the error.
- Do NOT delete existing directories.

**Log output:**
```
✓ Directory structure created:
  ✓ src/api/v1/
  ✓ src/services/
  ✓ src/repositories/
  ✓ src/models/
  ✓ tests/unit/
  ✓ tests/integration/
  ... (other directories)
```

---

### Universal Rule — Check Before Every Write

> **This rule applies to Steps 3–15 (every step that writes code).**
>
> Before writing any file in each step:
>
> 1. **Check if the target file already exists.**
> 2. If it **does not exist** → proceed with CREATE as described in the step.
> 3. If it **exists** → read the file completely, then:
>    - Find every class/function that the step intends to add or modify.
>    - For each one:
>      - **Already exists in the file** → edit only the changed lines; preserve everything else.
>      - **Not yet in the file** → append it at the end of the file.
>    - Do NOT rewrite the entire file. Do NOT rename the file.
>
> Violating this rule (e.g., creating `MediaService2.java` alongside `MediaService.java`) is a critical error and must be avoided.

---

### Step 3 — Implement Pydantic Schemas

**Action:** Create src/models/schemas.py with all request/response Pydantic schemas.

**For each schema in backend-design.schemas:**

Generate Python code:
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class MediaFileBase(BaseModel):
    """Base schema for MediaFile — shared fields."""
    filename: str = Field(..., min_length=1, max_length=255, description="Name of the uploaded file")
    mime_type: str = Field(..., description="MIME type (e.g., image/png)")
    size_bytes: int = Field(..., gt=0, le=10485760, description="File size in bytes (max 10MB)")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility

class MediaFileCreate(MediaFileBase):
    """Request schema for POST /api/v1/media/upload."""
    tags: Optional[List[str]] = Field(None, max_length=5, description="Optional tags")

class MediaFileResponse(MediaFileBase):
    """Response schema for GET endpoints."""
    id: UUID = Field(..., description="Unique identifier")
    user_id: UUID = Field(..., description="Owner user ID")
    storage_url: str = Field(..., description="URL to access the file")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class MediaFileDetailResponse(MediaFileResponse):
    """Detailed response schema for GET /api/v1/media/{file_id}."""
    download_count: int = Field(0, description="Number of times downloaded")
    last_accessed_at: Optional[datetime] = Field(None, description="Last access timestamp")

class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error_code: str = Field(..., description="Error code (e.g., RESOURCE_NOT_FOUND)")
    message: str = Field(..., description="Human-readable error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(..., description="When the error occurred")
```

**Requirements:**
- All schemas inherit from `BaseModel` (unless they inherit from another schema)
- Request schemas should be used only for request bodies (POST, PATCH)
- Response schemas should be used only for responses (GET, POST success, PATCH)
- Base schemas are reusable building blocks (inherit in request/response schemas)
- Use `Field(...)` with constraints (min_length, max_length, gt, le, regex, etc.)
- Add class `Config` with `from_attributes = True` for SQLModel compatibility
- Add docstrings to all classes and fields
- All validation rules should be concrete (from backend-design.schemas.validation)

**Log output:**
```
✓ src/models/schemas.py created:
  - MediaFileBase
  - MediaFileCreate
  - MediaFileResponse
  - MediaFileDetailResponse
  - ErrorResponse
  (5 schemas total)
```

---

### Step 4 — Implement Custom Exception Classes

**Action:** Create src/models/exceptions.py with all custom exception classes.

**For each exception in backend-design.error_handling.exception_classes:**

Generate Python code:
```python
from typing import Optional

class AppException(Exception):
    """Base exception class for application errors."""
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class ResourceNotFoundError(AppException):
    """Raised when a requested resource is not found (404)."""
    def __init__(self, message: str, error_code: str = "RESOURCE_NOT_FOUND"):
        super().__init__(message, status_code=404, error_code=error_code)

class UnauthorizedError(AppException):
    """Raised when authentication fails (401)."""
    def __init__(self, message: str = "Invalid or missing credentials", error_code: str = "UNAUTHORIZED"):
        super().__init__(message, status_code=401, error_code=error_code)

class ForbiddenError(AppException):
    """Raised when user lacks permission (403)."""
    def __init__(self, message: str = "You do not have permission", error_code: str = "FORBIDDEN"):
        super().__init__(message, status_code=403, error_code=error_code)

class ValidationError(AppException):
    """Raised when request validation fails (422)."""
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, status_code=422, error_code=error_code)
```

**Requirements:**
- All custom exceptions inherit from AppException
- Each exception class includes: message, status_code, error_code
- Status codes must match backend-design.error_handling.http_mapping
- Error codes are UPPERCASE_WITH_UNDERSCORES (used in error responses)
- Include docstrings

**Log output:**
```
✓ src/models/exceptions.py created:
  - AppException (base)
  - ResourceNotFoundError (404)
  - UnauthorizedError (401)
  - ForbiddenError (403)
  - ValidationError (422)
  (5 exception classes total)
```

---

### Step 5 — Implement SQLModel ORM Models

**Action:** Create src/models/db.py with all SQLModel ORM models.

**Requirements:**
- Models inherit from SQLModel (which is both Pydantic + SQLAlchemy)
- Each model corresponds to a domain entity from architecture-design
- Fields must exactly match the schema-design SQL table definition (if schema-design exists)
- Use PostgreSQL types (UUID, VARCHAR, INTEGER, TIMESTAMP, etc.)

**For each domain entity:**

Generate Python code:
```python
from sqlmodel import SQLModel, Field, Column
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class MediaFile(SQLModel, table=True):
    """Database model for media files."""
    __tablename__ = "media_files"

    # Primary key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier"
    )

    # Fields from schema-design
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        description="Owner user ID"
    )
    filename: str = Field(
        max_length=255,
        nullable=False,
        description="Name of the uploaded file"
    )
    mime_type: str = Field(
        max_length=100,
        nullable=False,
        description="MIME type (e.g., image/png)"
    )
    size_bytes: int = Field(
        nullable=False,
        description="File size in bytes"
    )
    storage_url: str = Field(
        nullable=False,
        description="URL to access the file"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp"
    )

    class Config:
        from_attributes = True
```

**Alignment with schema-design:**
- If schema-design.TSK-NNN.sql exists, ensure:
  - All columns from CREATE TABLE are in the model
  - Column types match (VARCHAR → str, INTEGER → int, UUID → UUID, TIMESTAMP → datetime)
  - Constraints match (nullable, unique, foreign_key)
  - Primary key and default values are correct

**If schema-design does NOT exist:**
- Infer types from Pydantic schemas in Step 3
- Use sensible defaults (UUID for id, TIMESTAMP for created_at/updated_at)

**Log output:**
```
✓ src/models/db.py created:
  - MediaFile (table: media_files)
  (1 ORM model total)
```

---

### Step 6 — Implement Repository Layer

**Action:** Create src/repositories/ with one repository class per domain entity.

**For each repository in backend-design.repositories:**

Create file: `src/repositories/{snake_case_entity}_repository.py`

Generate Python code:
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, List
from src.models.db import MediaFile
from src.models.schemas import MediaFileCreate, MediaFileUpdate

class MediaFileRepository:
    """Repository for MediaFile database operations."""

    async def create(
        self,
        session: AsyncSession,
        data: MediaFileCreate
    ) -> MediaFile:
        """Create a new media file record."""
        media_file = MediaFile(**data.dict())
        session.add(media_file)
        await session.commit()
        await session.refresh(media_file)
        return media_file

    async def get_by_id(
        self,
        session: AsyncSession,
        file_id: UUID
    ) -> Optional[MediaFile]:
        """Retrieve a media file by ID."""
        statement = select(MediaFile).where(MediaFile.id == file_id)
        result = await session.execute(statement)
        return result.scalars().first()

    async def get_by_owner(
        self,
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[MediaFile]:
        """Retrieve all media files owned by a user (with pagination)."""
        statement = (
            select(MediaFile)
            .where(MediaFile.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(statement)
        return result.scalars().all()

    async def update(
        self,
        session: AsyncSession,
        file_id: UUID,
        data: MediaFileUpdate
    ) -> Optional[MediaFile]:
        """Update a media file."""
        media_file = await self.get_by_id(session, file_id)
        if not media_file:
            return None

        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(media_file, field, value)

        session.add(media_file)
        await session.commit()
        await session.refresh(media_file)
        return media_file

    async def delete(
        self,
        session: AsyncSession,
        file_id: UUID
    ) -> bool:
        """Delete a media file by ID."""
        media_file = await self.get_by_id(session, file_id)
        if not media_file:
            return False

        await session.delete(media_file)
        await session.commit()
        return True
```

**Requirements:**
- All methods are async
- Use `AsyncSession` from SQLAlchemy (not synchronous Session)
- Use SQLAlchemy select() for queries (not raw SQL)
- Include pagination (skip, limit) for list methods
- All methods handle errors gracefully (return None instead of raising exceptions)
- Include docstrings for all methods
- CRUD methods (create, read, update, delete) are standard
- Custom query methods are specific to the domain (get_by_owner, search_by_name, etc.)

**Create src/repositories/__init__.py:**
```python
from src.repositories.media_file_repository import MediaFileRepository

__all__ = [
    "MediaFileRepository",
]
```

**Log output:**
```
✓ src/repositories/ created:
  - MediaFileRepository (src/repositories/media_file_repository.py)
  (1 repository class total)
```

---

### Step 7 — Implement Service Layer

**Action:** Create src/services/ with one service class per module from architecture-design.

**For each service in backend-design.services:**

Create file: `src/services/{snake_case_module}_service.py`

Generate Python code:
```python
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.schemas import MediaFileCreate, MediaFileResponse, MediaFileDetailResponse
from src.models.exceptions import ResourceNotFoundError, UnauthorizedError
from src.repositories.media_file_repository import MediaFileRepository

class MediaFileService:
    """Service for media file operations."""

    def __init__(self, repository: MediaFileRepository):
        """Initialize service with dependency injection."""
        self.repository = repository

    async def create_media_file(
        self,
        session: AsyncSession,
        data: MediaFileCreate,
        user_id: UUID
    ) -> MediaFileResponse:
        """Create a new media file (upload)."""
        # Add user_id to data
        file_data = {**data.dict(), "user_id": user_id}

        # Call repository
        media_file = await self.repository.create(session, MediaFileCreate(**file_data))

        # Return response schema
        return MediaFileResponse.from_orm(media_file)

    async def get_media_file(
        self,
        session: AsyncSession,
        file_id: UUID,
        user_id: UUID
    ) -> MediaFileDetailResponse:
        """Get a media file (with ownership verification)."""
        media_file = await self.repository.get_by_id(session, file_id)

        if not media_file:
            raise ResourceNotFoundError(f"MediaFile {file_id} not found")

        if media_file.user_id != user_id:
            raise UnauthorizedError("You do not have access to this file")

        return MediaFileDetailResponse.from_orm(media_file)

    async def delete_media_file(
        self,
        session: AsyncSession,
        file_id: UUID,
        user_id: UUID
    ) -> bool:
        """Delete a media file (with ownership verification)."""
        media_file = await self.repository.get_by_id(session, file_id)

        if not media_file:
            raise ResourceNotFoundError(f"MediaFile {file_id} not found")

        if media_file.user_id != user_id:
            raise UnauthorizedError("You do not have permission to delete this file")

        # TODO: Delete file from storage (S3 or local) before DB delete

        return await self.repository.delete(session, file_id)
```

**Requirements:**
- Service class takes repository/dependencies via constructor (dependency injection)
- All service methods call repository methods (not direct DB access)
- Business logic lives in service layer (validation, authorization, etc.)
- Raise custom exceptions (not HTTPException) on error conditions
- Return Pydantic response schemas (not ORM models)
- All methods are async
- Include docstrings

**Create src/services/__init__.py:**
```python
from src.services.media_file_service import MediaFileService

__all__ = [
    "MediaFileService",
]
```

**Log output:**
```
✓ src/services/ created:
  - MediaFileService (src/services/media_file_service.py)
  (1 service class total)
```

---

### Step 8 — Implement Authentication Middleware

**Action:** Create src/middleware/auth.py with get_current_user dependency.

Generate Python code:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

# Configuration (should be in env vars in production)
SECRET_KEY = "your-secret-key"  # TODO: Load from .env
ALGORITHM = "HS256"

security = HTTPBearer()

class CurrentUser:
    """Currently authenticated user."""
    def __init__(self, user_id: UUID, email: str, roles: list):
        self.user_id = user_id
        self.email = email
        self.roles = roles

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> CurrentUser:
    """Extract and validate JWT token, return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        roles: list = payload.get("roles", [])

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(user_id=UUID(user_id), email=email, roles=roles)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(user_id: UUID, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

**Requirements:**
- get_current_user is a FastAPI dependency
- Uses HTTPBearer for Authorization header
- Validates JWT token using PyJWT library
- Returns a CurrentUser object with user_id, email, roles
- Raises HTTPException(401) on invalid/missing token
- TODO comments indicate values that should be loaded from .env

**Create src/middleware/__init__.py:**
```python
from src.middleware.auth import get_current_user, create_access_token, CurrentUser

__all__ = [
    "get_current_user",
    "create_access_token",
    "CurrentUser",
]
```

**Log output:**
```
✓ src/middleware/auth.py created:
  - CurrentUser (class)
  - get_current_user (dependency)
  - create_access_token (function)
```

---

### Step 9 — Implement FastAPI Routers

**Action:** Create src/api/v1/ routers for all endpoints.

**For each endpoint in backend-design.api_endpoints:**

Create file: `src/api/v1/{resource_name}.py`

Generate Python code:
```python
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.schemas import (
    MediaFileCreate,
    MediaFileResponse,
    MediaFileDetailResponse,
    ErrorResponse,
)
from src.models.exceptions import (
    AppException,
    ResourceNotFoundError,
    UnauthorizedError,
)
from src.services.media_file_service import MediaFileService
from src.middleware.auth import get_current_user, CurrentUser
from src.db import get_session  # Database session dependency

router = APIRouter(prefix="/api/v1/media", tags=["media"])

# Dependency injection
async def get_media_service(session: AsyncSession = Depends(get_session)):
    """Provide media file service with session."""
    from src.repositories.media_file_repository import MediaFileRepository
    repo = MediaFileRepository()
    return MediaFileService(repo)

@router.post(
    "/upload",
    response_model=MediaFileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def upload_media(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    service: MediaFileService = Depends(get_media_service),
):
    """Upload a new media file."""
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > 10_485_760:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File too large (max 10MB)"
            )

        # Create upload data
        upload_data = MediaFileCreate(
            filename=file.filename,
            mime_type=file.content_type,
            size_bytes=len(file_content),
        )

        # Call service
        media_file = await service.create_media_file(session, upload_data, current_user.user_id)

        # TODO: Upload file content to storage (S3 or local)

        return media_file

    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get(
    "/{file_id}",
    response_model=MediaFileDetailResponse,
    responses={
        404: {"model": ErrorResponse, "description": "File not found"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def get_media(
    file_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    service: MediaFileService = Depends(get_media_service),
):
    """Retrieve a media file by ID."""
    try:
        return await service.get_media_file(session, file_id, current_user.user_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "File not found"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def delete_media(
    file_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    service: MediaFileService = Depends(get_media_service),
):
    """Delete a media file."""
    try:
        await service.delete_media_file(session, file_id, current_user.user_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

**Requirements:**
- Each router is for one resource (media_files, users, etc.)
- Routers are created in src/api/v1/{resource_name}.py
- Routers use APIRouter with prefix (e.g., "/api/v1/media")
- All endpoint functions are async
- Protected endpoints use Depends(get_current_user)
- Error handling wraps AppException and converts to HTTPException
- Dependency injection for service layer (not created in endpoint)
- Response models are Pydantic schemas
- Status codes match backend-design specification

**Create src/api/__init__.py and src/api/v1/__init__.py:**
```python
# src/api/__init__.py
from src.api.v1 import router as v1_router

__all__ = ["v1_router"]

# src/api/v1/__init__.py
from src.api.v1.media_files import router as media_router

__all__ = ["media_router"]
```

**Log output:**
```
✓ src/api/v1/ created:
  - media_files.py (router with POST /upload, GET /{id}, DELETE /{id})
  (1 router file, 3 endpoints)
```

---

### Step 10 — Create Main FastAPI Application

**Action:** Create src/main.py that initializes and configures the FastAPI app.

Generate Python code:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from src.api.v1 import media_router
from src.models.exceptions import AppException
from src.models.schemas import ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Media Marketplace API",
    description="API for uploading and managing media files",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],  # TODO: Load from env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for custom AppException
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    logger.warning(f"AppException: {exc.error_code} - {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

# Register routers
app.include_router(media_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Requirements:**
- App title, description, version from task metadata
- CORS middleware configured with allowed origins (from backend-design)
- Global exception handler for AppException (converts to JSON error response)
- All routers registered (include_router)
- Health check endpoint for monitoring
- Logging configured

**Log output:**
```
✓ src/main.py created:
  - FastAPI app initialized
  - CORS configured
  - Exception handlers registered
  - Routers included
```

---

### Step 11 — Create Database Session Dependency

**Action:** Create src/db.py with database configuration and session dependency.

Generate Python code:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session as dependency."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database (create tables)."""
    async with engine.begin() as conn:
        from src.models.db import SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)

async def close_db():
    """Close database connection."""
    await engine.dispose()
```

**Requirements:**
- DATABASE_URL from environment variable (with default for testing)
- Async SQLAlchemy engine and session factory
- get_session dependency for use in routes
- init_db function to create tables
- close_db function for cleanup

**Log output:**
```
✓ src/db.py created:
  - Database engine configured
  - AsyncSession factory created
  - get_session dependency defined
```

---

### Step 12 — Create Alembic Migrations (if schema-design exists)

**Action:** Create migrations/ directory with Alembic setup and migration files.

**If schema-design.TSK-NNN.sql exists:**

1. Create `migrations/env.py` (Alembic environment configuration)
2. Create `migrations/alembic.ini` (Alembic config file)
3. Parse schema-design SQL and create initial migration: `migrations/versions/001_initial_schema.py`

**Example migration file:**
```python
"""Initial schema creation.

Revision ID: 001
Revises:
Create Date: 2026-02-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create media_files table
    op.create_table(
        'media_files',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.VARCHAR(length=255), nullable=False),
        sa.Column('mime_type', sa.VARCHAR(length=100), nullable=False),
        sa.Column('size_bytes', sa.INTEGER(), nullable=False),
        sa.Column('storage_url', sa.VARCHAR(length=2048), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('media_files')
```

**Requirements:**
- Migrations are created from schema-design CREATE TABLE statements
- Each migration has revision ID and comments
- upgrade() function creates tables
- downgrade() function drops tables
- Naming: 001_initial_schema.py, 002_add_column.py, etc.

**If schema-design does NOT exist:**
- Skip migration creation (tables will be created by SQLModel on app startup via init_db)
- Warn user: "schema-design not found — skipping migrations. Tables will be created via SQLModel.metadata.create_all()"

**Log output:**
```
✓ migrations/ created:
  - alembic.ini (configuration)
  - env.py (Alembic environment)
  - versions/001_initial_schema.py (create media_files table)
```

---

### Step 13 — Create Unit Tests

**Action:** Create tests/unit/ with unit tests for services and schemas.

**Create tests/fixtures/conftest.py:**
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from src.models.db import SQLModel
from src.repositories.media_file_repository import MediaFileRepository
from src.services.media_file_service import MediaFileService

# Test database (in-memory SQLite)
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def test_db():
    """Create test database and tables."""
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture
async def test_session(test_db):
    """Provide test database session."""
    async_session_maker = sessionmaker(
        test_db,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.close()

@pytest.fixture
def media_file_repo():
    """Provide MediaFileRepository for testing."""
    return MediaFileRepository()

@pytest.fixture
def media_file_service(media_file_repo):
    """Provide MediaFileService for testing."""
    return MediaFileService(media_file_repo)

@pytest.fixture
def test_user_id():
    """Provide a test user ID."""
    return uuid4()
```

**Create tests/unit/services/test_media_file_service.py:**
```python
import pytest
from uuid import uuid4

from src.models.schemas import MediaFileCreate
from src.models.exceptions import ResourceNotFoundError, UnauthorizedError

@pytest.mark.asyncio
async def test_create_media_file_success(test_session, media_file_service, test_user_id):
    """Test successful media file creation."""
    data = MediaFileCreate(
        filename="test.png",
        mime_type="image/png",
        size_bytes=1024,
    )

    result = await media_file_service.create_media_file(test_session, data, test_user_id)

    assert result.filename == "test.png"
    assert result.mime_type == "image/png"
    assert result.size_bytes == 1024
    assert result.user_id == test_user_id

@pytest.mark.asyncio
async def test_get_media_file_not_found(test_session, media_file_service, test_user_id):
    """Test getting non-existent media file."""
    with pytest.raises(ResourceNotFoundError):
        await media_file_service.get_media_file(test_session, uuid4(), test_user_id)

@pytest.mark.asyncio
async def test_get_media_file_unauthorized(test_session, media_file_service, test_user_id):
    """Test getting media file owned by another user."""
    # Create file for different user
    owner_id = uuid4()
    data = MediaFileCreate(
        filename="test.png",
        mime_type="image/png",
        size_bytes=1024,
    )
    file = await media_file_service.create_media_file(test_session, data, owner_id)

    # Try to access with different user
    with pytest.raises(UnauthorizedError):
        await media_file_service.get_media_file(test_session, file.id, test_user_id)

@pytest.mark.asyncio
async def test_delete_media_file_success(test_session, media_file_service, test_user_id):
    """Test successful media file deletion."""
    data = MediaFileCreate(
        filename="test.png",
        mime_type="image/png",
        size_bytes=1024,
    )
    file = await media_file_service.create_media_file(test_session, data, test_user_id)

    result = await media_file_service.delete_media_file(test_session, file.id, test_user_id)

    assert result is True
```

**Requirements:**
- Test files in tests/unit/services/test_{service_name}.py
- Each test function starts with test_ and describes the scenario
- Use pytest.mark.asyncio for async tests
- Test both happy path (success) and error cases
- Mock repository if needed (for pure unit tests)
- Include docstrings

**Log output:**
```
✓ tests/unit/ created:
  - fixtures/conftest.py (test database, fixtures)
  - services/test_media_file_service.py (4 unit tests)
```

---

### Step 14 — Create Integration Tests

**Action:** Create tests/integration/api/ with integration tests for endpoints.

**Create tests/integration/api/test_media_files.py:**
```python
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from src.main import app
from src.middleware.auth import create_access_token

client = TestClient(app)

@pytest.fixture
def auth_token(test_user_id):
    """Create JWT token for testing."""
    return create_access_token(test_user_id, "test@example.com")

def test_upload_media_success(auth_token):
    """Test successful media upload."""
    response = client.post(
        "/api/v1/media/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"file": ("test.png", b"fake image content", "image/png")},
    )

    assert response.status_code == 201
    assert response.json()["filename"] == "test.png"

def test_upload_media_unauthorized():
    """Test upload without authentication."""
    response = client.post(
        "/api/v1/media/upload",
        files={"file": ("test.png", b"fake image content", "image/png")},
    )

    assert response.status_code == 403  # or 401 depending on auth handling

def test_upload_media_file_too_large(auth_token):
    """Test upload with file exceeding size limit."""
    response = client.post(
        "/api/v1/media/upload",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"file": ("large.bin", b"x" * (10_485_761), "application/octet-stream")},
    )

    assert response.status_code == 422

def test_get_media_success(auth_token, test_file_id):
    """Test successful media file retrieval."""
    response = client.get(
        f"/api/v1/media/{test_file_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

def test_get_media_not_found(auth_token):
    """Test getting non-existent media file."""
    response = client.get(
        f"/api/v1/media/{uuid4()}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 404

def test_delete_media_success(auth_token, test_file_id):
    """Test successful media file deletion."""
    response = client.delete(
        f"/api/v1/media/{test_file_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 204

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Requirements:**
- Use TestClient from FastAPI for endpoint testing
- Test both success and error cases
- Test auth flow (with and without token)
- Test HTTP status codes
- Include docstrings

**Log output:**
```
✓ tests/integration/api/ created:
  - test_media_files.py (6 integration tests)
```

---

### Step 15 — Create Configuration Files

**Action:** Create root-level config files (.env.example, requirements.txt, pytest.ini).

**Create .env.example:**
```
# Database configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/media_marketplace

# JWT configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# CORS configuration
ALLOWED_ORIGINS=http://localhost:3000,https://example.com

# Logging
LOG_LEVEL=INFO

# File storage
STORAGE_TYPE=local  # or s3
STORAGE_PATH=/tmp/media  # for local storage
S3_BUCKET=my-bucket  # for S3
```

**Create requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.20
sqlmodel==0.0.14
pydantic==2.4.2
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
aiosqlite==0.19.0  # for testing
pytest==7.4.2
pytest-asyncio==0.21.1
httpx==0.25.0  # for TestClient
alembic==1.13.0
psycopg2-binary==2.9.9
asyncpg==0.29.0
```

**Create pytest.ini:**
```
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Log output:**
```
✓ Configuration files created:
  - .env.example
  - requirements.txt
  - pytest.ini
```

---

### Step 16 — Run Tests and Verify Implementation

**Action:** Run all tests to ensure implementation is correct.

**Commands to run:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run type checking (if using mypy)
mypy src/
```

**Verification:**
- All unit tests pass (>80% coverage target)
- All integration tests pass
- No import errors
- No type errors (if using type hints)

**Log output:**
```
Running tests...
pytest tests/ -v

tests/unit/services/test_media_file_service.py::test_create_media_file_success PASSED
tests/unit/services/test_media_file_service.py::test_get_media_file_not_found PASSED
tests/unit/services/test_media_file_service.py::test_get_media_file_unauthorized PASSED
tests/unit/services/test_media_file_service.py::test_delete_media_file_success PASSED
tests/integration/api/test_media_files.py::test_upload_media_success PASSED
tests/integration/api/test_media_files.py::test_upload_media_unauthorized PASSED
tests/integration/api/test_media_files.py::test_upload_media_file_too_large PASSED
tests/integration/api/test_media_files.py::test_get_media_success PASSED
tests/integration/api/test_media_files.py::test_get_media_not_found PASSED
tests/integration/api/test_media_files.py::test_delete_media_success PASSED
tests/integration/api/test_media_files.py::test_health_check PASSED

========================= 11 passed in 2.34s =========================

✓ All tests passed!
```

---

### Step 17 — Verify Acceptance Criteria

**Action:** Check that implementation satisfies all acceptance_criteria from task-spec.

**From task-spec.execution_plan.steps[exec_type=="backend-implementation"].acceptance_criteria:**

Example criteria:
```
- All endpoints from backend-design.api_endpoints are implemented
- All Pydantic schemas are defined and validated
- All services use repositories (no direct DB access)
- All repositories use AsyncSession
- All auth_required endpoints use Depends(get_current_user)
- Unit tests cover >80% of service layer
- Integration tests cover all endpoints
- All tests pass
```

**Verification checklist:**
- [ ] All N endpoints implemented with correct HTTP method, path, auth
- [ ] All M schemas defined with validation
- [ ] All K services implemented with repository injection
- [ ] All R repositories implement async CRUD methods
- [ ] All error scenarios handled with custom exceptions
- [ ] All tests pass (unit + integration)
- [ ] Code follows naming conventions (snake_case files, PascalCase classes)
- [ ] Project structure matches backend-design.file_structure
- [ ] Documentation (docstrings) complete

**Log output:**
```
Verifying acceptance criteria...

✓ Endpoints:
  ✓ POST /api/v1/media/upload (auth required)
  ✓ GET /api/v1/media/{file_id} (auth required)
  ✓ DELETE /api/v1/media/{file_id} (auth required)
  (3/3 endpoints implemented)

✓ Schemas:
  ✓ MediaFileCreate
  ✓ MediaFileResponse
  ✓ MediaFileDetailResponse
  ✓ ErrorResponse
  (4/4 schemas defined)

✓ Services:
  ✓ MediaFileService (3 methods)
  (1/1 service implemented)

✓ Repositories:
  ✓ MediaFileRepository (5 async methods)
  (1/1 repository implemented)

✓ Tests:
  ✓ 4 unit tests (100% service coverage)
  ✓ 7 integration tests (all endpoints + error cases)
  (11/11 tests passed)

Acceptance criteria: ALL PASSED
```

---

## Post-Execution Summary

After successfully implementing all code, print a comprehensive summary:

```
✓ Backend implementation complete for TSK-NNN.

Task: [task_name]
Framework: [backend] / [database]
Project Root: [project_root]

Files Created:
  Models & Schemas:
    ✓ src/models/schemas.py (5 Pydantic schemas)
    ✓ src/models/exceptions.py (5 custom exception classes)
    ✓ src/models/db.py (1 SQLModel ORM model)

  Data Layer:
    ✓ src/repositories/media_file_repository.py (MediaFileRepository with 5 methods)

  Business Logic:
    ✓ src/services/media_file_service.py (MediaFileService with 3 methods)

  API Layer:
    ✓ src/api/v1/media_files.py (3 endpoints: POST upload, GET detail, DELETE)
    ✓ src/main.py (FastAPI app with CORS, exception handlers, health check)

  Infrastructure:
    ✓ src/middleware/auth.py (JWT validation, get_current_user dependency)
    ✓ src/db.py (AsyncSession factory, database configuration)

  Database:
    ✓ migrations/alembic.ini
    ✓ migrations/env.py
    ✓ migrations/versions/001_initial_schema.py

  Tests:
    ✓ tests/fixtures/conftest.py (test database, fixtures)
    ✓ tests/unit/services/test_media_file_service.py (4 unit tests)
    ✓ tests/integration/api/test_media_files.py (7 integration tests)

  Configuration:
    ✓ .env.example
    ✓ requirements.txt
    ✓ pytest.ini

Summary:
  - 3 API endpoints implemented
  - 5 Pydantic schemas defined
  - 1 service layer class (3 methods)
  - 1 repository layer class (5 methods)
  - 5 custom exception classes
  - 11 tests written (4 unit, 7 integration)
  - 100% test pass rate

Verification:
  ✓ All output_contract entries covered
  ✓ All endpoints have request/response schemas
  ✓ All services use repositories
  ✓ All repository methods are async
  ✓ All auth_required endpoints use Depends(get_current_user)
  ✓ All tests pass
  ✓ Code follows naming conventions
  ✓ Acceptance criteria satisfied

Next Steps:
  1. Review generated code
  2. Configure environment variables (.env file from .env.example)
  3. Run migrations: alembic upgrade head
  4. Start server: uvicorn src.main:app --reload
  5. Test endpoints: curl -H "Authorization: Bearer {token}" http://localhost:8000/api/v1/media/{file_id}
  6. Run full test suite: pytest tests/ -v

Code is ready for review and deployment.
```

---

## Error Handling Reference

| Error | Condition | Action |
|-------|-----------|--------|
| **task-spec file not found** | File path does not exist | Stop execution. Report the full path attempted. |
| **Invalid YAML syntax** | YAML parser error | Stop execution. Report line number and parse error. |
| **backend-design.TSK-NNN.md not found** | Prerequisite file missing | Stop execution. Run /backend-design first. |
| **Project root not writable** | Permission denied on project_root | Stop execution. Report permission error. |
| **File already exists** | Target file path exists | READ the file first. UPDATE the existing class/function in place. NEVER create a duplicate file with a different name. |
| **Class already exists in file** | Class with same name found in existing file | Edit only the changed methods/fields. Do NOT add a second class with a different name. |
| **Malformed backend-design** | Missing sections or invalid structure | Stop execution. Report which section is invalid. |
| **Database connection failed** | Cannot connect to database | Report error. Suggest checking DATABASE_URL in .env. |
| **Test failures** | pytest returned non-zero exit code | Report which tests failed. Do not consider implementation complete. |
| **schema-design.TSK-NNN.sql malformed** | SQL parsing fails | Warn but continue. Skip migrations. Suggest user re-run schema-design. |

---

## Implementation Notes for Cursor AI Agent

1. **This is autonomous code execution** — the agent writes code directly to project_root, not to a design document.

2. **ALWAYS scan before writing** — before creating or editing any file, check whether it already exists at the exact target path. This is mandatory, not optional.

   ```
   Target path exists?
   ├── NO  → CREATE the file from scratch
   └── YES → Read the file first, then:
             ├── Class/function already exists → UPDATE it in place (edit only what changed)
             └── Class/function not found      → APPEND it to the existing file
   ```

   **What "UPDATE in place" means:**
   - Open the existing file
   - Find the specific class or function by name
   - Edit only the fields, methods, or lines that need to change
   - Leave all other classes, methods, imports, and comments untouched

   **What NOT to do:**
   - ❌ Create `UserService_new.java` because `UserService.java` already exists
   - ❌ Create `User_v2.java` because `User.java` already exists
   - ❌ Add a duplicate class `UserDAO` to a new file when `UserDAO` already exists
   - ❌ Overwrite an entire file when only one method needs to change

3. **Dependency order matters** — implement files in this order:
   - Schemas and exceptions first (no dependencies)
   - ORM models next (depend on schemas)
   - Repositories next (depend on ORM models)
   - Services next (depend on repositories)
   - Routes last (depend on services)

3. **All repository methods must be async** — use `async def` and `AsyncSession`.

4. **Service layer never accesses DB directly** — always use repository.

5. **Router layer never calls repository directly** — always use service.

6. **Testing is mandatory** — write both unit and integration tests. All tests must pass before considering the implementation complete.

7. **Acceptance criteria are strict** — verify every criterion from task-spec before declaring success.

8. **TODOs are expected** — some functionality like file upload to S3 may not be fully implementable without additional context. Mark with TODO comments and continue.

9. **Configuration is external** — use .env for database URLs, API keys, secret keys. Never hardcode credentials.

10. **Documentation is code** — write docstrings for all classes, methods, and functions. They are part of the specification.
