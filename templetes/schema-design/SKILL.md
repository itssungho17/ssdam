---
name: schema-design
description: Third step in the SSDAM data chain. Reads data-modeling output and produces DDL SQL (CREATE TABLE, INDEX, constraints). Its output is consumed by backend-design as the authoritative schema reference.
compatibility: Universal
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# schema-design Skill

## File Paths Reference

This skill reads from and writes to the SSDAM pipeline workspace:

```
task-spec.TSK-NNN.yaml (user provides path)
  + data-modeling.TSK-NNN.md (from .ssdam/{id}/output/design/)
  ↓
[schema-design]  ← YOU ARE HERE
  ↓
.ssdam/{id}/output/design/schema-design.TSK-NNN.sql
  ↓
[backend-design]  (reads schema as authoritative DB contract)
```

**Skill files (read-only):**
- `/mnt/ssdam/templetes/schema-design/SKILL.md` (this file)
- `/mnt/ssdam/templetes/schema-design/references/input.template.yaml` (input schema reference)
- `/mnt/ssdam/templetes/schema-design/references/output.template.yaml` (output schema reference)
- `/mnt/ssdam/templetes/schema-design/references/rules.md` (DDL rules and anti-patterns)

**Runtime files (created per execution):**
- Input 1: `task-spec.TSK-NNN.yaml` (user provides path)
- Input 2: `.ssdam/{id}/output/design/data-modeling.TSK-NNN.md` (prerequisite)
- Output: `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (written by this skill)

---

## Overview

| | |
|---|---|
| **Trigger** | `/schema-design <task-spec-path>` |
| **Prerequisites** | `data-modeling.TSK-NNN.md` must exist at `.ssdam/{id}/output/design/` |
| **Input** | task-spec.TSK-NNN.yaml + data-modeling output |
| **Work** | Parse data-modeling → generate CREATE TABLE statements → generate indexes → verify DDL |
| **Output** | `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` (SQL file with DDL statements) |
| **Optional** | Only run if task includes database schema changes; skip if using existing schema |

---

## Input Specification

### Trigger Command

```
/schema-design <task-spec-path>
```

**Example:**
```
/schema-design .ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml
```

### Fields Read from task-spec

From `task-spec.TSK-NNN.yaml`:

**From `metadata`:**
- `mission_id` — copied to SQL file header comment
- `task_id` — used to derive output filename (TSK-NNN)
- `task_name` — used as document title in SQL header

**From `execution_plan`:**
- `tech_stack.database` — confirms database type (PostgreSQL, MySQL, etc.; this skill assumes PostgreSQL)
- `steps[]` where `exec_type == "schema-design"`: read acceptance_criteria for DDL validation

### Fields Read from data-modeling Output

From `.ssdam/{id}/output/design/data-modeling.TSK-NNN.md`:

**From YAML frontmatter:**
- `task_id`, `mission_id`, `document_type: "data-modeling"`

**From `entities` section:**
- For each entity: `entity_name`, `table_name`, `fields` (with types, nullability, defaults), `primary_key`, `indexes`

**From `relationships` section:**
- For each relationship: `from_entity`, `to_entity`, `relationship_type`, `fk_field`

**From `junction_tables` section (if present):**
- For each many-to-many: `junction_table_name`, `left_entity`, `left_fk_column`, `right_entity`, `right_fk_column`

---

## Pre-Execution Verification

Before starting the main execution procedure, perform these checks:

**1. Validate task-spec file**
- [ ] File exists at the provided path
- [ ] File is valid YAML (no syntax errors)
- [ ] File contains required sections: `metadata`, `execution_plan`

**2. Derive workspace directory**
- From the task-spec path (e.g., `.ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml`):
  - Workspace dir = `.ssdam/{id}/` (extract from parent of parent)
  - Design output dir = `.ssdam/{id}/output/design/`

**3. Verify data-modeling output exists**
- [ ] Extract task_id from task-spec (TSK-NNN)
- [ ] Check `.ssdam/{id}/output/design/data-modeling.TSK-NNN.md` exists
- If NOT found: **STOP** and inform user: "data-modeling.TSK-NNN.md not found. Run /data-modeling first."

**4. Parse data-modeling output**
- [ ] Read the markdown file
- [ ] Extract YAML frontmatter
- [ ] Locate `entities:` section
- [ ] Confirm at least one entity exists

**5. Verify database is PostgreSQL**
- [ ] `execution_plan.tech_stack.database` is set to PostgreSQL (or compatible)
- If not: **WARN** (this skill assumes PostgreSQL; may need adjustment for MySQL, etc.)

**6. Create design output directory**
- [ ] Create `.ssdam/{id}/output/design/` if it does not exist
- [ ] Verify directory is writable
- If creation or write permission fails, **STOP** and report the error

---

## Execution Procedure

Execute the following 5 steps in order. After each step, accumulate SQL statements to assemble the final DDL file.

### Step 1 — Load Inputs

**Action:** Parse both input files.

**Extract from task-spec.TSK-NNN.yaml and store:**
- `metadata.mission_id` → SQL file header comment
- `metadata.task_id` → output filename (schema-design.TSK-NNN.sql)
- `metadata.task_name` → SQL file header title
- `execution_plan.tech_stack.database` → confirm database type (expect PostgreSQL)

**Extract from data-modeling.TSK-NNN.md and store:**
- `entities[]` → list of all tables to create
- `relationships[]` → list of foreign keys to add
- `junction_tables[]` → list of junction tables to create
- For each entity: `fields[]`, `indexes[]`

**Error handling:**
- If YAML parsing fails, report error and stop
- If data-modeling is malformed, report which section is invalid

---

### Step 2 — Generate CREATE TABLE Statements

**Action:** For each entity in the data-modeling output, generate a CREATE TABLE statement.

**Table creation order:**
- Create tables without foreign keys FIRST (tables that are referenced by others)
- Create tables with foreign keys SECOND (tables that reference others)
- Example dependency order:
  1. `users` (no FK)
  2. `media_files` (FK to users)
  3. `comments` (FK to media_files and users)

**For each entity, generate SQL:**

```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  field_name TYPE [NOT NULL] [DEFAULT value] [UNIQUE],
  fk_field UUID NOT NULL REFERENCES other_table(id) [ON DELETE CASCADE|SET NULL],
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Rules for each field:**

1. **Primary key (always first):**
   ```sql
   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
   ```

2. **Foreign key fields:**
   ```sql
   owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
   ```
   - Type: Always UUID (match the referenced PK type)
   - Constraint: `REFERENCES target_table(id)`
   - ON DELETE clause:
     - `ON DELETE CASCADE` — delete this row if referenced row is deleted (e.g., media_files when user is deleted)
     - `ON DELETE SET NULL` — set FK to NULL if referenced row is deleted (only if FK is nullable)
     - `ON DELETE RESTRICT` — prevent deletion of referenced row if FK exists (default; most restrictive)
   - **Choose based on domain logic:**
     - Cascading deletes: parent deletion removes children (e.g., user → media files)
     - Set NULL: parent deletion orphans children (e.g., employee → manager)
     - Restrict: prevent deletion if children exist (strict integrity)

3. **Domain-specific fields (in order they appear in data-modeling):**
   ```sql
   filename VARCHAR(255) NOT NULL,
   mime_type VARCHAR(100) NOT NULL,
   size_bytes INTEGER NOT NULL,
   storage_url TEXT NOT NULL,
   is_public BOOLEAN NOT NULL DEFAULT false,
   ```
   - Type: From data-modeling (e.g., VARCHAR(255), TEXT, INTEGER, BOOLEAN)
   - Nullable: `NOT NULL` if `nullable: false` in data-modeling; omit if `nullable: true`
   - Default: `DEFAULT value` if specified in data-modeling
   - Unique: Add `UNIQUE` constraint if `unique: true` in data-modeling

4. **Timestamps (always last two):**
   ```sql
   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
   updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   ```

**Complete example:**

```sql
CREATE TABLE media_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255) NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  size_bytes INTEGER NOT NULL,
  storage_url TEXT NOT NULL,
  is_public BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  media_id UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
  author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Error handling:**
- If entity in data-modeling has no PK: Add `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` and warn
- If field type is invalid: Report error; use only PostgreSQL native types
- If relationship references non-existent entity: Report error; skip FK constraint and flag for manual review

---

### Step 3 — Generate CREATE INDEX Statements

**Action:** For each index defined in data-modeling, generate a CREATE INDEX statement.

**For each index in data-modeling output:**

```sql
CREATE [UNIQUE] INDEX idx_name ON table_name(column_name);
```

**Rules:**

1. **Single-column index:**
   ```sql
   CREATE INDEX idx_media_files_owner_id ON media_files(owner_id);
   CREATE INDEX idx_media_files_created_at ON media_files(created_at);
   ```

2. **Unique index (for unique constraints):**
   ```sql
   CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
   ```

3. **Compound index (multiple columns):**
   ```sql
   CREATE INDEX idx_comments_media_author ON comments(media_id, author_id);
   ```

4. **Partial index (advanced; optional):**
   ```sql
   -- Only index deleted comments (for soft deletes)
   CREATE INDEX idx_comments_deleted ON comments(created_at) WHERE deleted_at IS NULL;
   ```

**Example index generation:**

```sql
-- Indexes for media_files
CREATE INDEX idx_media_files_owner_id ON media_files(owner_id);
CREATE INDEX idx_media_files_filename ON media_files(filename);
CREATE INDEX idx_media_files_created_at ON media_files(created_at);

-- Indexes for comments
CREATE INDEX idx_comments_media_id ON comments(media_id);
CREATE INDEX idx_comments_author_id ON comments(author_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

-- Unique indexes
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
CREATE UNIQUE INDEX idx_tags_name_unique ON tags(name);
```

---

### Step 4 — Generate Junction Tables for Many-to-Many Relationships

**Action:** For each many-to-many relationship, generate a CREATE TABLE statement for the junction table.

**For each junction table in data-modeling output:**

```sql
CREATE TABLE junction_table_name (
  left_entity_id UUID NOT NULL REFERENCES left_table(id) ON DELETE CASCADE,
  right_entity_id UUID NOT NULL REFERENCES right_table(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (left_entity_id, right_entity_id)
);
```

**Rules:**

1. **Junction table structure:**
   - Two FK columns pointing to the related entities
   - Compound primary key on the two FK columns
   - Always include `created_at` timestamp
   - Do NOT include `updated_at` (junction tables are immutable)
   - Column naming: `{entity}_id` (singular, snake_case)

2. **Primary key is the compound key:**
   ```sql
   PRIMARY KEY (comment_id, tag_id)
   ```
   - This prevents duplicate relationships

3. **ON DELETE CASCADE is standard:**
   - When a related entity is deleted, remove the junction table row
   - This is the typical pattern for many-to-many

**Example junction table:**

```sql
CREATE TABLE comment_tags (
  comment_id UUID NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
  tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (comment_id, tag_id)
);

-- Always add indexes on both FK columns for query performance
CREATE INDEX idx_comment_tags_comment_id ON comment_tags(comment_id);
CREATE INDEX idx_comment_tags_tag_id ON comment_tags(tag_id);
```

---

### Step 5 — Verify and Write SQL

**Action:** Validate all SQL and assemble into final DDL file.

**Verification checklist:**

- [ ] Every entity from data-modeling has a CREATE TABLE statement
- [ ] Every table has:
  - `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- [ ] Every FK field has a `REFERENCES` clause
- [ ] Every FK column is indexed (or part of compound index)
- [ ] Every junction table exists (for many-to-many relationships)
- [ ] All field types are valid PostgreSQL types
- [ ] All table/column names follow snake_case convention
- [ ] SQL syntax is valid (can be parsed and executed)
- [ ] Tables are in dependency order (no forward references)
- [ ] Primary keys use `DEFAULT gen_random_uuid()` (not `SERIAL`)

**SQL Syntax Validation:**
- No missing semicolons at end of statements
- No unclosed parentheses or quotes
- All keywords properly capitalized (CREATE TABLE, NOT NULL, DEFAULT, etc.)
- All type names are recognized PostgreSQL types

**Error handling:**
- If table has no PK: Add default UUID PK and warn
- If FK references non-existent table: Flag as error; note which task owns the table
- If type name is invalid: Report error; use only PostgreSQL native types
- If circular dependencies: Report error; may indicate schema design issue
- If syntax error detected: Report line number and fix before writing

**Write output file:**

Create: `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql`

**Structure:**

```sql
-- ========================================================================
-- Schema Design for TSK-NNN: [Task Name]
-- ========================================================================
-- Generated from: data-modeling.TSK-NNN.md
-- Task ID: TSK-NNN
-- Mission ID: MIS-...
-- Generated: YYYY-MM-DDTHH:mm:ssZ
--
-- This file contains all DDL statements (CREATE TABLE, CREATE INDEX)
-- needed to set up the database schema for this task.
--
-- How to apply:
--   psql -d database_name -f schema-design.TSK-NNN.sql
-- ========================================================================

-- ========================================================================
-- Prerequisites / Extensions
-- ========================================================================
--
-- Ensure these extensions are available:
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- For gen_random_uuid()
-- CREATE EXTENSION IF NOT EXISTS uuid-ossp;  -- Alternative UUID provider

-- ========================================================================
-- Tables (in dependency order: referenced tables first)
-- ========================================================================

[CREATE TABLE statements in dependency order]

-- ========================================================================
-- Junction Tables (for many-to-many relationships)
-- ========================================================================

[CREATE TABLE statements for junction tables]

-- ========================================================================
-- Indexes (on FK and search columns)
-- ========================================================================

[CREATE INDEX statements]

-- ========================================================================
-- Triggers (if needed: auto-update updated_at timestamp)
-- ========================================================================
--
-- Optional: If your ORM/application does NOT automatically update
-- the updated_at timestamp on every UPDATE, add a trigger:
--
-- CREATE OR REPLACE FUNCTION update_updated_at_column()
-- RETURNS TRIGGER AS $$
-- BEGIN
--   NEW.updated_at = NOW();
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
--
-- CREATE TRIGGER update_media_files_updated_at
-- BEFORE UPDATE ON media_files
-- FOR EACH ROW
-- EXECUTE FUNCTION update_updated_at_column();
--
-- [Repeat for each table]

-- ========================================================================
-- End of Schema Design DDL
-- ========================================================================
```

---

## Post-Execution Summary

After successfully writing the output file, print a confirmation message:

```
✓ schema-design.TSK-NNN.sql written to:
  .ssdam/{id}/output/design/schema-design.TSK-NNN.sql

Tables created: [count]
Indexes created: [count]
Junction tables created: [count]

To apply this schema to your database:
  psql -d database_name -f .ssdam/{id}/output/design/schema-design.TSK-NNN.sql

Next: run /backend-design <task-spec-path>
     (backend-design will read this schema as the authoritative DB contract)
```

---

## Error Handling Reference

| Error | Condition | Action |
|-------|-----------|--------|
| **data-modeling.TSK-NNN.md not found** | File does not exist at expected path | Stop. Inform user: "Run /data-modeling first." |
| **No entities in data-modeling** | entities section is empty | Stop. Inform user: "No entities to generate schema for." |
| **Entity without primary key** | Entity defined but PK is missing | Add default `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`. Warn user. |
| **Field type is invalid** | Field type is not a PostgreSQL type | Error. Report which field and type. Suggest valid replacement. |
| **FK references non-existent entity** | Relationship references entity not in data-modeling | Error. Note which entity is missing. Suggest checking architecture-design. |
| **FK without corresponding index** | Field is a FK but no index defined | Error. Add required index. Warn user. |
| **Circular table dependencies** | Table A references B, B references A (without junction table) | Error. Likely a schema design issue. Suggest refactoring with mediator table. |
| **SQL syntax error** | Parser fails on generated SQL | Error. Report which statement failed and why. Show the problematic SQL. |
| **Duplicate table names** | Two entities have same table_name | Error. Inform user: "Duplicate table names in data-modeling." |
| **Directory not writable** | `.ssdam/{id}/output/design/` cannot be written to | Stop. Report permission error. Suggest checking directory permissions. |

---

## Implementation Notes for the Agent

1. **Workspace Derivation:**
   - Input path: `.ssdam/media-marketplace-20260221-001/output/task-spec.TSK-001.yaml`
   - Workspace: `.ssdam/media-marketplace-20260221-001/`
   - Design output dir: `.ssdam/media-marketplace-20260221-001/output/design/`
   - Output filename: `schema-design.TSK-001.sql`

2. **Task ID Extraction:**
   - From task-spec filename `task-spec.TSK-NNN.yaml`, extract `NNN`
   - Use in output filename: `schema-design.TSK-NNN.sql`

3. **Database Type Assumption:**
   - This skill assumes PostgreSQL
   - If `tech_stack.database` is different (MySQL, SQLite, etc.), adjust syntax accordingly
   - Key differences:
     - PostgreSQL: `gen_random_uuid()`, `TIMESTAMPTZ`, `BIGINT` for serial
     - MySQL: `UUID()`, `DATETIME`, `BIGINT AUTO_INCREMENT`
     - SQLite: Limited UUID support; may require custom logic

4. **ON DELETE Behavior:**
   - Choose based on domain logic, not one-size-fits-all
   - Cascading deletes: user deletion removes all their media files
   - Set NULL: employee deletion orphans their comments (if designed)
   - Restrict: prevent deletion if children exist (enforce data integrity)

5. **Indexes Strategy:**
   - Every FK gets an index (mandatory)
   - Sort columns (ORDER BY) get indexes
   - Filter columns (WHERE) get indexes if high cardinality
   - Do NOT over-index (maintenance cost, write performance)

6. **Primary Key Strategy:**
   - Always use UUID with `gen_random_uuid()`
   - Never use SERIAL (not portable across shards)
   - Never use composite PK in main tables (use surrogate UUID + compound indexes)

7. **Comment Preservation:**
   - Keep SQL comments from template intact
   - Add entity-specific comments if helpful (e.g., "-- Stores user-uploaded media files")

8. **Next Skill Decision:**
   - Always recommend `/backend-design` after schema-design completes
   - Backend-design will read this schema-design.TSK-NNN.sql as the contract

