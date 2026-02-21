# Data-Modeling Design Rules and Conventions

This document defines the rules, naming conventions, and anti-patterns for the data-modeling skill in the SSDAM pipeline.

---

## Naming Conventions

### Entity Names (PascalCase)

- Format: `PascalCase` (capitalize each word, no underscores)
- Examples: `MediaFile`, `UploadTask`, `UserAccount`, `CommentThread`
- Always singular, never plural
- Use descriptive, domain-specific terms
- Avoid generic names like `Data`, `Info`, `Object`

### Table Names (snake_case plural)

- Format: `snake_case_plural` (lowercase, underscores between words, plural form)
- Examples: `media_files`, `upload_tasks`, `user_accounts`, `comment_threads`
- Always plural, never singular (convention in SQL)
- Direct mapping: `MediaFile` → `media_files`, `UploadTask` → `upload_tasks`
- Multi-word entities: `BlogPostComment` → `blog_post_comments`

### Column Names (snake_case)

- Format: `snake_case` (lowercase, underscores between words)
- Examples: `filename`, `user_id`, `created_at`, `mime_type`, `is_public`
- Always singular
- For booleans: prefix with `is_`, `has_`, or `can_` (e.g., `is_public`, `has_comments`, `can_edit`)
- For timestamps: use `_at` suffix (e.g., `created_at`, `updated_at`, `deleted_at`, `published_at`)
- For counts: use `_count` suffix (e.g., `comment_count`, `view_count`)

### Foreign Key Fields

- Format: `{entity}_id` where entity is singular, snake_case version of referenced entity
- Examples:
  - References `User` entity: `user_id`
  - References `MediaFile` entity: `media_file_id`
  - References `UploadTask` entity: `upload_task_id`
- Never abbreviate: `uid`, `mid`, `utid` are NOT acceptable
- Always store the same type as the referenced PK (usually UUID)

### Index Names

- Format: `idx_{table}_{column}` for single-column indexes
- Format: `idx_{table}_{col1}_{col2}` for multi-column indexes
- For unique indexes: `idx_{table}_{column}_unique` or add `_uk` suffix
- Examples:
  - `idx_media_files_owner_id` (FK index)
  - `idx_users_email_unique` (unique constraint index)
  - `idx_media_files_created_at` (sort/filter index)

---

## Mandatory Fields

Every entity MUST have these three fields:

### 1. Primary Key

```yaml
- name: id
  type: UUID
  nullable: false
  default: gen_random_uuid()
  unique: true
```

- **Type:** Always `UUID` (not `SERIAL`, not `BIGINT`, not `INT`)
- **Default:** Always `gen_random_uuid()` or `uuid_generate_v4()` (depends on PostgreSQL version)
- **Nullable:** Always `false`
- **Unique:** Always `true` (implied by PRIMARY KEY)
- **Rationale:** UUIDs provide global uniqueness, better security, and support distributed systems

### 2. Created Timestamp

```yaml
- name: created_at
  type: TIMESTAMPTZ
  nullable: false
  default: NOW()
  unique: false
```

- **Type:** Always `TIMESTAMPTZ` (timezone-aware), never `TIMESTAMP` or `DATETIME`
- **Default:** Always `NOW()` (server time at insertion)
- **Nullable:** Always `false`
- **Purpose:** Record when the entity was created; immutable after creation
- **Rationale:** Essential for audit trails, sorting, and temporal queries

### 3. Updated Timestamp

```yaml
- name: updated_at
  type: TIMESTAMPTZ
  nullable: false
  default: NOW()
  unique: false
```

- **Type:** Always `TIMESTAMPTZ`
- **Default:** Always `NOW()` (server time)
- **Nullable:** Always `false`
- **Purpose:** Record when the entity was last modified; updated on every write
- **Trigger/ORM requirement:** Application or database trigger must update this on every UPDATE
- **Rationale:** Essential for concurrency control, change tracking, and last-modified queries

---

## Field Type Mapping (PostgreSQL)

Use these PostgreSQL native types. Never use generic or legacy types.

### String Fields

| Use Case | PostgreSQL Type | Example | Notes |
|----------|-----------------|---------|-------|
| String with known max length | `VARCHAR(n)` | `VARCHAR(255)` for filename | Use when max length is known and enforced |
| Unbounded string | `TEXT` | Email content, descriptions | Use for arbitrary-length strings |
| Single character | `CHAR(1)` | Status flag | Rare; usually prefer ENUM or BOOLEAN |
| Email (unique) | `VARCHAR(255)` + UNIQUE INDEX | user.email | Email max length is 254; use 255 for safety |
| URL (unbounded) | `TEXT` | storage_url | URLs can exceed VARCHAR limits |
| Enum-like string | `VARCHAR(50)` or custom ENUM | status (pending, active, archived) | Consider PostgreSQL ENUM type for better validation |

### Numeric Fields

| Use Case | PostgreSQL Type | Example | Notes |
|----------|-----------------|---------|-------|
| Small integers (0–32,767) | `SMALLINT` | Version number | Use for bounded ranges |
| Medium integers (-2B to +2B) | `INTEGER` | File size in bytes, count | Standard choice for most numbers |
| Large integers (−9B to +9B) | `BIGINT` | Very large counts, Unix timestamps | Use when INTEGER might overflow |
| Decimal/currency | `DECIMAL(precision, scale)` | DECIMAL(10,2) for USD | Always use for money; never float |
| Floating-point (approximate) | `REAL` or `DOUBLE PRECISION` | Scientific data | Never use for money; use DECIMAL |

### Date/Time Fields

| Use Case | PostgreSQL Type | Example | Notes |
|----------|-----------------|---------|-------|
| Date + time with timezone | `TIMESTAMPTZ` | created_at, published_at | Always use timezone-aware; never TIMESTAMP |
| Date only (no time) | `DATE` | birth_date, event_date | Use when time is irrelevant |
| Time only (no date) | `TIME` or `TIMETZ` | Rare | Avoid; usually refactor to store as string or interval |
| Duration/interval | `INTERVAL` | session_duration | Use for time differences |

### Boolean Fields

| Use Case | PostgreSQL Type | Example | Notes |
|----------|-----------------|---------|-------|
| Boolean flag | `BOOLEAN` | is_public, is_verified, has_payment | Standard choice; true/false only |
| Tri-state (true/false/null) | `BOOLEAN` (nullable) | is_deleted (null = not deleted, true = deleted) | Nullable booleans are rare; prefer explicit fields |

### Binary / Complex Data

| Use Case | PostgreSQL Type | Example | Notes |
|----------|-----------------|---------|-------|
| JSON (typed) | `JSONB` | metadata, config | Always JSONB (not JSON); supports indexing and operators |
| Binary data | `BYTEA` | File content | Store binary data in external file storage (S3); use for metadata only |
| UUID/identifier | `UUID` | id, owner_id, parent_id | Always UUID for PKs and FKs |

### Anti-Pattern Types (NEVER USE)

| Bad Type | Why Not | Use Instead |
|----------|---------|-------------|
| `CHAR(36)` for UUID | Wasteful space; inconsistent with UUID operators | `UUID` |
| `DATETIME` | Non-standard; not timezone-aware | `TIMESTAMPTZ` |
| `TIMESTAMP` | Ambiguous timezone handling | `TIMESTAMPTZ` |
| `INT` for file sizes | May overflow; use BIGINT | `INTEGER` or `BIGINT` |
| `FLOAT` for money | Rounding errors; precision loss | `DECIMAL(precision, scale)` |
| `VARCHAR` without length | Forces length on every use | `VARCHAR(n)` or `TEXT` |
| `SERIAL` | Non-portable; problematic in distributed systems | Use `UUID` with `gen_random_uuid()` |

---

## Foreign Key Rules

### Every FK Must Have an Index

**Rule:** Every column that serves as a foreign key MUST have a database index.

**Why:**
- FKs are frequently used in JOIN operations
- Without indexes, joins become full table scans
- PostgreSQL does NOT automatically index FK columns (unlike MySQL)

**Example:**
```yaml
# Entity: Comment
fields:
  - name: media_id
    type: UUID
    nullable: false

# Relationship: Comment.media_id → MediaFile.id
relationships:
  - from_entity: Comment
    to_entity: MediaFile
    fk_field: media_id

# Index is REQUIRED
indexes:
  - name: idx_comments_media_id
    columns: [media_id]
    unique: false
```

### Many-to-Many: Always Use Junction Table

**Rule:** Never use composite FK or array fields for many-to-many relationships. Always create a dedicated junction table.

**Bad (anti-pattern):**
```yaml
# WRONG: Comment with array of tag_ids
Comment:
  fields:
    - name: tag_ids
      type: UUID[]  # WRONG: array type
```

**Good (correct):**
```yaml
# RIGHT: Junction table
junction_tables:
  - junction_table_name: comment_tags
    left_entity: Comment
    left_fk_column: comment_id
    right_entity: Tag
    right_fk_column: tag_id
    fields:
      - name: comment_id
        type: UUID
        nullable: false
      - name: tag_id
        type: UUID
        nullable: false
      - name: created_at
        type: TIMESTAMPTZ
        nullable: false
    primary_key: [comment_id, tag_id]  # Compound PK
```

**Why:**
- Junction tables are normalized (1NF, 2NF, 3NF)
- Array types complicate queries and indexing
- Composite PKs are standard in relational databases
- Easy to add metadata (created_at, added_by) to the relationship

### Optional vs. Required FK

**Nullable FK (optional relationship):**
```yaml
- name: parent_comment_id
  type: UUID
  nullable: true  # Can be null (comment has no parent = root comment)
  default: null
```

**Non-null FK (required relationship):**
```yaml
- name: media_id
  type: UUID
  nullable: false  # Every comment must belong to media
  default: null
```

---

## Relationship Cardinality

### One-to-Many (||--o{)

- **Definition:** One instance of A can have many instances of B; each B belongs to exactly one A
- **Example:** One User has many MediaFiles; each MediaFile belongs to exactly one User
- **Implementation:** FK field on the "many" side points to the "one" side
  ```yaml
  relationships:
    - from_entity: MediaFile
      to_entity: User
      relationship_type: one_to_many
      fk_field: owner_id  # on media_files table
  ```
- **Index:** Always add index on FK column (`idx_media_files_owner_id`)
- **Mermaid notation:** `USER ||--o{ MEDIA_FILE : owns`

### One-to-One (||--||)

- **Definition:** One instance of A is related to exactly one instance of B, and vice versa
- **Example:** One User has one UserProfile; one UserProfile belongs to exactly one User
- **Implementation:** FK field on either side (conventionally on the "child" side), marked UNIQUE
  ```yaml
  relationships:
    - from_entity: UserProfile
      to_entity: User
      relationship_type: one_to_one
      fk_field: user_id  # Must be UNIQUE to enforce cardinality
  ```
- **Index:** Index on FK column; index must be UNIQUE
  ```yaml
  indexes:
    - name: idx_user_profiles_user_id_unique
      columns: [user_id]
      unique: true
  ```
- **Mermaid notation:** `USER ||--|| USER_PROFILE : has`

### Many-to-Many (}o--o{)

- **Definition:** Multiple A can relate to multiple B, and vice versa
- **Example:** Comments have many Tags; Tags have many Comments
- **Implementation:** Junction table with compound PK
  ```yaml
  junction_tables:
    - junction_table_name: comment_tags
      left_entity: Comment
      left_fk_column: comment_id
      right_entity: Tag
      right_fk_column: tag_id
      primary_key: [comment_id, tag_id]
  ```
- **Indexes:** One index per FK column
  ```yaml
  indexes:
    - name: idx_comment_tags_comment_id
      columns: [comment_id]
      unique: false
    - name: idx_comment_tags_tag_id
      columns: [tag_id]
      unique: false
  ```
- **Mermaid notation:** `COMMENT }o--o{ TAG : is_tagged_with`

---

## Index Strategy

### What to Index

**Mandatory indexes (always):**
1. Primary key: Implicit, created by PK constraint
2. Foreign key columns: Required for JOIN performance

**Required indexes (usually):**
3. Columns used in WHERE clauses (filters)
4. Columns used in ORDER BY (sorting)
5. Unique constraint columns (enforce uniqueness)

**Optional indexes (sometimes):**
6. Columns in compound filters (if high cardinality)
7. Columns used in subqueries or aggregations

### What NOT to Index

- Low-cardinality columns (< 5% unique values) — usually not worth it
- Nullable columns (unless supporting IS NULL queries)
- Boolean columns (too low cardinality)
- Columns that are frequently updated (maintenance cost high)
- Columns in tables that are write-heavy and rarely queried

### Compound Indexes

**Use compound indexes when:**
- Multiple columns are frequently queried together
- The first column has high selectivity

**Example:**
```yaml
# Bad: two separate indexes
indexes:
  - name: idx_comments_media_id
    columns: [media_id]
    unique: false
  - name: idx_comments_author_id
    columns: [author_id]
    unique: false

# Better: compound index (if media_id is often queried with author_id)
indexes:
  - name: idx_comments_media_author
    columns: [media_id, author_id]
    unique: false
```

**Index column order matters:**
- Place most selective (high cardinality) column first
- Column order should match common query patterns

---

## Anti-Patterns and What NOT to Do

### 1. Entity Without Primary Key

**Bad:**
```yaml
- entity_name: TempData
  table_name: temp_data
  fields:
    - name: user_id
      type: UUID
    - name: value
      type: TEXT
  # NO PRIMARY KEY!
```

**Problem:**
- Every row is identical to another row with same data
- Cannot uniquely identify a row
- UPDATE and DELETE become ambiguous
- Breaks referential integrity

**Fix:**
```yaml
- entity_name: TempData
  table_name: temp_data
  fields:
    - name: id
      type: UUID
      nullable: false
      default: gen_random_uuid()
      unique: true
    - name: user_id
      type: UUID
    - name: value
      type: TEXT
  primary_key: id
```

### 2. Foreign Key Without Index

**Bad:**
```yaml
fields:
  - name: owner_id
    type: UUID
    nullable: false
# No index on owner_id!
```

**Problem:**
- JOINs on this column require full table scans
- Poor query performance at scale
- Constraint checking becomes slow

**Fix:**
```yaml
fields:
  - name: owner_id
    type: UUID
    nullable: false

indexes:
  - name: idx_media_files_owner_id
    columns: [owner_id]
    unique: false
```

### 3. TEXT for All Strings

**Bad:**
```yaml
fields:
  - name: username
    type: TEXT  # Why TEXT for max 50 chars?
  - name: email
    type: TEXT  # Why TEXT for max 254 chars?
  - name: country_code
    type: TEXT  # Why TEXT for max 2 chars?
```

**Problem:**
- Wastes storage (every cell allocates full page)
- No validation (could store 1GB string)
- Indexes less efficient
- Database cannot enforce length

**Fix:**
```yaml
fields:
  - name: username
    type: VARCHAR(50)
  - name: email
    type: VARCHAR(255)
  - name: country_code
    type: CHAR(2)
```

### 4. Composite Primary Key (anti-pattern)

**Bad:**
```yaml
- entity_name: OrderItem
  table_name: order_items
  primary_key: [order_id, item_id]  # Composite PK
  fields:
    - name: order_id
      type: UUID
    - name: item_id
      type: UUID
    - name: quantity
      type: INTEGER
  # No surrogate id!
```

**Problem:**
- Composite PKs are hard to reference (FKs become multi-column)
- Difficult to use in APIs (can't pass single ID)
- Inefficient in database (wider index)
- Violates normalization principles

**Fix:**
```yaml
- entity_name: OrderItem
  table_name: order_items
  primary_key: id
  fields:
    - name: id
      type: UUID
      nullable: false
      default: gen_random_uuid()
    - name: order_id
      type: UUID
      nullable: false
    - name: item_id
      type: UUID
      nullable: false
    - name: quantity
      type: INTEGER
  # Junction table (many-to-many) can use composite PK
```

### 5. Columns Without Nullability Declared

**Bad:**
```yaml
fields:
  - name: email
    type: VARCHAR(255)
    # nullable: ??? (not declared)
```

**Problem:**
- Ambiguous whether field is optional or required
- SQL defaults to nullable (usually not intended)
- API/ORM doesn't know if field must be sent

**Fix:**
```yaml
fields:
  - name: email
    type: VARCHAR(255)
    nullable: false  # Required field
```

### 6. Relationship Without Type

**Bad:**
```yaml
relationships:
  - from_entity: Comment
    to_entity: Media
    # relationship_type: ??? (not declared)
```

**Problem:**
- Unclear what cardinality is intended
- Mermaid ERD cannot be drawn
- Schema design has ambiguity

**Fix:**
```yaml
relationships:
  - from_entity: Comment
    to_entity: Media
    relationship_type: one_to_many
    fk_field: media_id
```

### 7. Self-Referential Foreign Key Without Purpose

**Bad:**
```yaml
- entity_name: Comment
  fields:
    - name: parent_comment_id
      type: UUID
      nullable: true
  relationships:
    - from_entity: Comment
      to_entity: Comment
      relationship_type: one_to_many
      fk_field: parent_comment_id
  # What is the domain pattern here? Unclear.
```

**Problem:**
- Valid pattern, but unusual; must document intent
- May cause circular update/delete logic

**Good (documented):**
```yaml
# Comments can be nested (replies to replies)
relationships:
  - from_entity: Comment
    to_entity: Comment
    relationship_type: one_to_many
    fk_field: parent_comment_id
    # Pattern: Hierarchical tree structure
    # parent_comment_id is null for root comments
```

---

## Verification Checklist

Before finalizing data-modeling output, verify:

- [ ] **Every entity has a PK** — exactly one `primary_key: id` of type UUID
- [ ] **Every entity has timestamps** — `created_at` and `updated_at`, both TIMESTAMPTZ
- [ ] **Every FK has an index** — for each relationship, corresponding index exists
- [ ] **All types are PostgreSQL native** — no CHAR(36), DATETIME, FLOAT for money, etc.
- [ ] **Many-to-many has junction table** — no array types, no composite FKs
- [ ] **Naming is consistent**:
  - Entity names: PascalCase
  - Table names: snake_case plural
  - Column names: snake_case
  - FK names: `{entity}_id`
  - Index names: `idx_{table}_{column}`
- [ ] **Nullable is declared** — every field has explicit `nullable: true|false`
- [ ] **Relationships match cardinality** — correct `relationship_type` chosen
- [ ] **No circular self-references** — unless intentional (hierarchical pattern)
- [ ] **Mermaid ERD syntax is valid** — all entities and relationships represented

---

## Summary

**Mandatory:**
1. Every entity must have: id (UUID, PK), created_at, updated_at
2. Every FK must have an index
3. Many-to-many relationships must use junction tables (compound PK)
4. Use PostgreSQL native types (UUID, TIMESTAMPTZ, VARCHAR(n), TEXT, INTEGER, BIGINT, DECIMAL, BOOLEAN, JSONB)
5. Name conventions: PascalCase entities, snake_case tables, snake_case columns, {entity}_id for FKs

**Recommended:**
6. Document relationship patterns (especially hierarchical or unusual)
7. Index columns used in WHERE, ORDER BY, and JOINs
8. Use VARCHAR(n) for bounded strings, TEXT for unbounded
9. Use BOOLEAN for flags (not CHAR(1) or INT)
10. Use DECIMAL for money, never FLOAT

**Forbidden:**
- Entities without PK
- FKs without indexes
- Composite PKs (use surrogate UUID PKs instead)
- Non-TZAWARE timestamps
- CHAR(36) for UUID, DATETIME, FLOAT for money
- Array types for relationships (use junction tables)
- Fields without declared nullability

