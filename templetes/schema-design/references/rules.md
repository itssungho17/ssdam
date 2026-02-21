# Schema-Design DDL Rules and Conventions

This document defines the rules, conventions, and anti-patterns for the schema-design skill in the SSDAM pipeline.

---

## DDL (Data Definition Language) Basics

### CREATE TABLE Structure

**Standard PostgreSQL CREATE TABLE syntax:**

```sql
CREATE TABLE table_name (
  column_name TYPE [constraints],
  column_name TYPE [constraints],
  ...
  constraint_name constraint_definition
);
```

**Constraints (placed inline or as table constraints):**
- `PRIMARY KEY` — unique identifier for the row
- `NOT NULL` — column must have a value
- `UNIQUE` — all values must be distinct
- `DEFAULT value` — default value when not provided
- `REFERENCES target_table(id)` — foreign key constraint
- `ON DELETE [CASCADE|SET NULL|RESTRICT]` — action when referenced row deleted
- `CHECK expression` — custom constraint (e.g., `CHECK (price > 0)`)

**Example:**

```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255) NOT NULL,
  size_bytes INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Naming Conventions (Must Match data-modeling)

### Table Names (snake_case plural)

- Format: `snake_case_plural`
- Examples: `users`, `media_files`, `comments`, `upload_tasks`
- Convention: Always plural, even for singleton tables (e.g., `system_settings`, not `system_setting`)
- Derived from data-modeling `table_name` field

### Column Names (snake_case)

- Format: `snake_case`
- Examples: `id`, `owner_id`, `filename`, `created_at`, `is_public`
- Always singular
- For booleans: prefix with `is_`, `has_`, or `can_`
- For timestamps: use `_at` suffix
- Derived from data-modeling `name` field

### Primary Key Column

- Always named `id` (convention in SSDAM)
- Type: Always `UUID`
- Default: Always `DEFAULT gen_random_uuid()`
- Example: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`

### Foreign Key Columns

- Format: `{entity}_id` where entity is singular, snake_case version of referenced entity
- Examples:
  - References `User`: `user_id`
  - References `MediaFile`: `media_file_id`
  - References `UploadTask`: `upload_task_id`
- Must match the PK type of referenced table (always UUID)
- Derived from data-modeling `fk_field`

### Constraint Names (Optional)

- Can name constraints explicitly for clarity
- Format: `constraint_type_table_column`
- Examples:
  - `fk_media_files_owner_id` (foreign key)
  - `ck_media_files_size_positive` (check constraint)
  - `uq_users_email` (unique constraint)

### Index Names (Mandatory)

- Format: `idx_{table}_{column}` for single-column
- Format: `idx_{table}_{col1}_{col2}` for multi-column
- For unique: `idx_{table}_{column}_unique` or add `_uk` suffix
- Examples:
  - `idx_media_files_owner_id` (FK index)
  - `idx_media_files_filename` (search index)
  - `idx_users_email_unique` (unique constraint)
  - `idx_comments_media_author` (compound index)
- Derived from data-modeling `indexes` section

---

## Core DDL Rules

### Every Table Must Have These Three Columns

**1. Primary Key:**
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
```
- Never use SERIAL, BIGINT, or INT for PK
- Always UUID with `gen_random_uuid()` (requires pgcrypto extension)
- Always NOT NULL (implicit in PRIMARY KEY)
- Position: Always first column

**2. Created Timestamp:**
```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
```
- Always TIMESTAMPTZ, never TIMESTAMP or DATETIME
- Default is NOW() (server time at insertion)
- Always NOT NULL
- Immutable after creation
- Position: Always second-to-last column

**3. Updated Timestamp:**
```sql
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
```
- Always TIMESTAMPTZ, never TIMESTAMP or DATETIME
- Default is NOW()
- Always NOT NULL
- Updated on every UPDATE (via ORM or trigger)
- Position: Always last column

---

## Column Type Selection

### String Fields

| Type | Max Length | Use Case | Example |
|------|-----------|----------|---------|
| `VARCHAR(n)` | n characters | Known, bounded string | `VARCHAR(255)` for filename |
| `CHAR(n)` | n characters | Fixed-length string | `CHAR(2)` for country code |
| `TEXT` | Unlimited | Arbitrary-length string | Email body, description |
| `BYTEA` | Unlimited | Binary data | Image/file data (store as URL instead) |

**Rules:**
- Use `VARCHAR(n)` when max length is known and should be enforced
- Use `TEXT` for unbounded strings
- Never use `VARCHAR` without length (forces length check elsewhere)
- Never use `CHAR(36)` for UUID (use `UUID` type instead)
- For email: `VARCHAR(255)` is safe (max email length is 254)

**Example:**
```sql
filename VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE,
bio TEXT,  -- Unbounded biography
```

### Numeric Fields

| Type | Range | Use Case | Example |
|------|-------|----------|---------|
| `SMALLINT` | -32,768 to 32,767 | Small counts | Star rating (0–5) |
| `INTEGER` | -2B to +2B | General purpose | File size, count, age |
| `BIGINT` | -9B to +9B | Large numbers | Unix timestamps, very large counts |
| `DECIMAL(p,s)` | Exact | Money/currency | `DECIMAL(10,2)` for USD amounts |
| `NUMERIC(p,s)` | Exact | Money/currency | Alternative to DECIMAL |
| `REAL` | ~7 digits | Approximate | Scientific measurements |
| `DOUBLE PRECISION` | ~15 digits | Approximate | Scientific measurements |

**Rules:**
- Use `INTEGER` for most numbers
- Use `DECIMAL(10,2)` for money (always exact, never float)
- Use `BIGINT` only when `INTEGER` might overflow
- Never use `FLOAT` or `REAL` for money (rounding errors)
- Validate ranges in application if necessary (CHECK constraints)

**Example:**
```sql
size_bytes INTEGER NOT NULL,
price DECIMAL(10,2) NOT NULL,
rating SMALLINT CHECK (rating >= 0 AND rating <= 5),
```

### Boolean Fields

| Type | Use Case | Example |
|------|----------|---------|
| `BOOLEAN` | True/false flag | `BOOLEAN NOT NULL DEFAULT false` |
| `BOOLEAN` (nullable) | Tri-state (true/false/null) | Rare; use explicit field instead |

**Rules:**
- Use `BOOLEAN NOT NULL DEFAULT false` for boolean flags
- Name with `is_`, `has_`, or `can_` prefix
- Default to `false` unless domain requires otherwise
- Avoid nullable booleans (use explicit `deleted_at` column for soft deletes)

**Example:**
```sql
is_public BOOLEAN NOT NULL DEFAULT false,
is_verified BOOLEAN NOT NULL DEFAULT false,
```

### Date/Time Fields

| Type | Use Case | Example |
|------|----------|---------|
| `TIMESTAMPTZ` | Date + time + timezone | `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()` |
| `TIMESTAMP` | Date + time (no timezone) | Avoid; use TIMESTAMPTZ |
| `DATE` | Date only, no time | `birth_date DATE NOT NULL` |
| `TIME` | Time only, no date | Rare; usually refactor |
| `INTERVAL` | Duration | `session_duration INTERVAL` |

**Rules:**
- Always use `TIMESTAMPTZ` for timestamps (never `TIMESTAMP` or `DATETIME`)
- TIMESTAMPTZ is timezone-aware; stores in UTC internally, displays in connection timezone
- Use `DATE` only when time is irrelevant
- Use `INTERVAL` for durations (not for absolute times)
- Default current time with `DEFAULT NOW()` (server time)

**Example:**
```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
birth_date DATE NOT NULL,
session_duration INTERVAL,
```

### UUID Type

| Use Case | Type | Example |
|----------|------|---------|
| Primary key | `UUID PRIMARY KEY DEFAULT gen_random_uuid()` | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign key | `UUID [NOT NULL] REFERENCES target(id)` | `owner_id UUID NOT NULL REFERENCES users(id)` |

**Rules:**
- Always use `UUID` type for unique identifiers (never CHAR(36), VARCHAR(36), etc.)
- Requires `CREATE EXTENSION IF NOT EXISTS pgcrypto`
- Use `gen_random_uuid()` for default (v4 random UUID)
- Alternative: `uuid_generate_v4()` (requires uuid-ossp extension)
- Never use SERIAL or auto-increment; not portable
- UUID provides global uniqueness; SERIAL does not

**Example:**
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
```

### JSON Type

| Type | Indexable | Use Case | Example |
|------|-----------|----------|---------|
| `JSON` | No | Exact JSON matching | `metadata JSON` |
| `JSONB` | Yes | Flexible structured data | `config JSONB` |

**Rules:**
- Always use `JSONB` instead of `JSON` (better performance, indexable)
- Use for flexible, semi-structured data
- Prefer explicit columns for well-defined fields
- Index with `CREATE INDEX idx_table_field ON table USING GIN(field)`

**Example:**
```sql
metadata JSONB,  -- Flexible metadata storage
CREATE INDEX idx_media_metadata ON media_files USING GIN(metadata);
```

---

## Foreign Key Constraints

### CREATE TABLE with FOREIGN KEY

**Syntax:**
```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fk_field UUID NOT NULL REFERENCES other_table(id) [ON DELETE action],
  ...
);
```

**Components:**
- `fk_field`: Column that holds the FK value
- `REFERENCES target_table(id)`: Specifies the referenced table/column
- `ON DELETE action`: What happens when referenced row is deleted
  - `CASCADE` — delete this row too
  - `SET NULL` — set FK to NULL (only if FK is nullable)
  - `RESTRICT` (default) — prevent deletion if FK exists

**Choosing ON DELETE action:**

| Action | When to Use | Example |
|--------|------------|---------|
| `ON DELETE CASCADE` | Child data is meaningless without parent | `media_files` when `user` is deleted |
| `ON DELETE SET NULL` | Child can exist independently (but orphaned) | `employee.manager_id` when manager is deleted |
| `ON DELETE RESTRICT` | Strict data integrity; prevent deletion | `orders` when `customer` is deleted |

**Rules:**
- Every FK must reference a column with a unique constraint (usually PK)
- FK and referenced column must have compatible types (both UUID, both INT, etc.)
- FK can be nullable (optional relationship) or NOT NULL (required)
- FKs are never indexed automatically; add indexes separately
- Circular FKs are allowed if at least one FK is nullable (to break the cycle during insertion)

**Examples:**

```sql
-- One-to-many: media_files belong to users (cascade delete)
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- One-to-many: comments belong to media_files and authors (cascade delete)
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  media_id UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
  author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Optional relationship: employee's manager (set NULL on manager delete)
CREATE TABLE employees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  manager_id UUID REFERENCES employees(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Indexes

### Why Indexes Matter

**Indexes improve performance for:**
- `WHERE` clause filters: `WHERE owner_id = ...`
- `ORDER BY` sorts: `ORDER BY created_at DESC`
- `JOIN` conditions: `ON media_files.owner_id = users.id`
- `UNIQUE` constraints: enforce uniqueness + fast lookup

**Indexes slow down:**
- `INSERT` — must update index
- `UPDATE` — must update index
- `DELETE` — must update index
- Storage — indexes consume disk space

**Trade-off:** Faster reads, slower writes. Typical OLTP systems benefit greatly.

### CREATE INDEX Syntax

**Single-column index:**
```sql
CREATE INDEX idx_media_files_owner_id ON media_files(owner_id);
```

**Unique index (enforces uniqueness):**
```sql
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

**Compound index (multiple columns):**
```sql
CREATE INDEX idx_comments_media_author ON comments(media_id, author_id);
```

**Partial index (conditional; advanced):**
```sql
CREATE INDEX idx_comments_active ON comments(id) WHERE deleted_at IS NULL;
```

### Which Columns to Index

**Always index (mandatory):**
1. Foreign key columns — required for JOIN performance
2. Columns used in WHERE clauses with high selectivity
3. Columns in ORDER BY clauses
4. Columns with UNIQUE constraint

**Examples of good indexes:**
```sql
-- FK index
CREATE INDEX idx_media_files_owner_id ON media_files(owner_id);

-- Search index
CREATE INDEX idx_media_files_filename ON media_files(filename);

-- Sort index
CREATE INDEX idx_media_files_created_at ON media_files(created_at);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

**Do NOT index (avoid over-indexing):**
- Low-cardinality columns (< 5% unique values): BOOLEAN, status flags
- Nullable columns (unless supporting IS NULL queries)
- Columns that are frequently updated
- Small columns with few rows (index overhead > benefit)
- Columns never used in WHERE/ORDER BY/JOIN

### Compound Indexes (Multiple Columns)

**When to use:**
- Multiple columns frequently queried together
- First column has high selectivity

**Column order matters:**
- Place most selective column first
- Order should match common query patterns
- Leftmost columns are used for filters

**Example:**
```sql
-- Good: media_id first (more selective; typical query: find comments on specific media)
CREATE INDEX idx_comments_media_author ON comments(media_id, author_id);

-- Query this index efficiently:
SELECT * FROM comments WHERE media_id = ? AND author_id = ?;
SELECT * FROM comments WHERE media_id = ?;  -- Uses index prefix

-- This query does NOT use the index:
SELECT * FROM comments WHERE author_id = ?;  -- Misses prefix
```

---

## Table Creation Order (Dependency Resolution)

**Rule:** Create tables without foreign keys FIRST, then tables with foreign keys.

**Algorithm:**
1. Identify all tables
2. Find tables with NO incoming FK dependencies (no table references them)
3. Create those tables first
4. Remove created tables from the dependency graph
5. Repeat until all tables are created

**Example dependency order:**

```
users (no FKs)
  ↓ (referenced by)
media_files (FK: owner_id → users)
comments (FK: media_id → media_files, author_id → users)
tags (no FKs)
comment_tags (FK: comment_id → comments, tag_id → tags)
```

**Correct creation order:**
1. `users` (no FK)
2. `tags` (no FK)
3. `media_files` (FK to users)
4. `comments` (FK to media_files, users)
5. `comment_tags` (FK to comments, tags)

**SQL ordering:**
```sql
CREATE TABLE users (...);
CREATE TABLE tags (...);
CREATE TABLE media_files (...);
CREATE TABLE comments (...);
CREATE TABLE comment_tags (...);
```

---

## Anti-Patterns and What NOT to Do

### 1. SERIAL Primary Keys (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  id SERIAL PRIMARY KEY,  -- WRONG
  ...
);
```

**Problems:**
- Not globally unique (sequence scoped to database)
- Exposes internal implementation (sequential IDs leaking business logic)
- Non-portable (SERIAL is PostgreSQL-specific)
- Difficult in distributed systems (conflict resolution needed)
- Security risk (sequential IDs allow enumeration)

**Fix:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- CORRECT
  ...
);
```

### 2. CHAR(36) for UUID (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  id CHAR(36) PRIMARY KEY,  -- WRONG
  ...
);
```

**Problems:**
- Wastes storage (36 chars instead of native UUID 16 bytes)
- Requires casting for UUID operations
- Inefficient indexing and comparison

**Fix:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- CORRECT
  ...
);
```

### 3. DATETIME Instead of TIMESTAMPTZ (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  created_at DATETIME NOT NULL DEFAULT NOW(),  -- WRONG
  ...
);
```

**Problems:**
- DATETIME is not timezone-aware
- Ambiguous when data is read from different timezones
- Difficult to store/retrieve UTC properly

**Fix:**
```sql
CREATE TABLE media_files (
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- CORRECT
  ...
);
```

### 4. FLOAT for Money (Anti-pattern)

**Bad:**
```sql
CREATE TABLE orders (
  total_amount FLOAT NOT NULL,  -- WRONG
  ...
);
```

**Problems:**
- Floating-point arithmetic is approximate (rounding errors)
- Not suitable for financial calculations
- Cannot represent all decimal values exactly

**Fix:**
```sql
CREATE TABLE orders (
  total_amount DECIMAL(10,2) NOT NULL,  -- CORRECT
  ...
);
```

### 5. Missing FK Index (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id),
  ...
);
-- No index on owner_id!
```

**Problems:**
- JOINs on this FK require full table scans
- Severe performance degradation at scale
- Constraint checking becomes slow

**Fix:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id),
  ...
);
CREATE INDEX idx_media_files_owner_id ON media_files(owner_id);
```

### 6. Storing Array Types for Relationships (Anti-pattern)

**Bad:**
```sql
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tag_ids UUID[] NOT NULL,  -- WRONG: array type
  ...
);
```

**Problems:**
- Violates normalization (1NF)
- Difficult to query (must use array operators)
- Cannot enforce referential integrity
- Inefficient indexing

**Fix (junction table):**
```sql
CREATE TABLE comment_tags (
  comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
  tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (comment_id, tag_id)
);
```

### 7. Nullable Primary Key (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY,  -- Missing DEFAULT
  ...
);
INSERT INTO media_files(...) VALUES(...);  -- id is NULL!
```

**Problems:**
- PK cannot be NULL
- Breaks uniqueness guarantee

**Fix:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- CORRECT
  ...
);
```

### 8. Missing NOT NULL on Required Fields (Anti-pattern)

**Bad:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID REFERENCES users(id),  -- Missing NOT NULL
  filename VARCHAR(255),  -- Missing NOT NULL
  ...
);
```

**Problems:**
- Fields can be NULL when they shouldn't be
- Application must check for NULL everywhere
- Hard to track which fields are optional vs required

**Fix:**
```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id),  -- Required
  filename VARCHAR(255) NOT NULL,  -- Required
  description TEXT,  -- Optional (nullable)
  ...
);
```

---

## Verification Checklist

Before finalizing schema-design output, verify:

- [ ] **All tables in dependency order** — referenced tables first, no forward FK references
- [ ] **Every table has id PK** — `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- [ ] **Every table has timestamps** — `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- [ ] **Every FK has REFERENCES clause** — `REFERENCES target_table(id)`
- [ ] **Every FK has corresponding INDEX** — `CREATE INDEX idx_table_fk_column ON table(fk_column)`
- [ ] **All field types are PostgreSQL native types** — no CHAR(36), DATETIME, FLOAT for money, etc.
- [ ] **All nullable fields are declared** — `NOT NULL` for required, omit for nullable
- [ ] **All defaults are present** — PK, timestamps, boolean flags with sensible defaults
- [ ] **All constraints are valid** — UNIQUE, CHECK, FK constraints are syntactically correct
- [ ] **All table/column names are snake_case** — no CamelCase, no spaces, no special chars
- [ ] **All junction tables have compound PKs** — `PRIMARY KEY (left_id, right_id)`
- [ ] **SQL syntax is valid** — can be parsed and executed by PostgreSQL
- [ ] **Mermaid ERD matches schema** — table names, column names, relationships match

---

## Summary

**Mandatory:**
1. Every table: id (UUID PK), created_at, updated_at
2. Every FK: REFERENCES constraint + INDEX
3. Use PostgreSQL native types (UUID, TIMESTAMPTZ, VARCHAR(n), TEXT, INTEGER, BIGINT, DECIMAL, BOOLEAN)
4. Table creation order: dependency order (referenced first)
5. Name conventions: snake_case tables, snake_case columns, {entity}_id for FKs, idx_{table}_{column} for indexes

**Recommended:**
6. Use `ON DELETE CASCADE` for child tables
7. Use `DECIMAL(p,s)` for money, never FLOAT
8. Index all FK columns + search columns + sort columns
9. Use `DEFAULT false` for boolean flags
10. Document unusual constraints with SQL comments

**Forbidden:**
- SERIAL primary keys (use UUID)
- CHAR(36) for UUID (use UUID type)
- DATETIME (use TIMESTAMPTZ)
- FLOAT for money (use DECIMAL)
- FKs without indexes
- Array types for relationships (use junction tables)
- Nullable primary keys
- Fields without declared nullability
- Forward FK references (table creation order)

