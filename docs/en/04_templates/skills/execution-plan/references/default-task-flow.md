# Default Task Flow & Rules

## Default 5-Step Flow

Every stage follows this 5-step default flow unless the stage's scope requires adjustment:

```
TASK-01: Architecture Design (아키텍처 설계)
  → System diagram, layer separation, module boundaries, API contract draft
  → Covers ALL artifacts (cross-cutting design)

TASK-02: ERD Design (ERD 설계 — Mermaid)
  → Entity-Relationship diagram in Mermaid syntax
  → Covers DB-related artifacts

TASK-03: DDL (DDL 작성)
  → Database migration files (Flyway/Liquibase/raw SQL)
  → Covers DB schema artifacts

TASK-04: Backend Implementation (백엔드 구현)
  → Controllers, Services, Repositories, DTOs, tests
  → Covers backend API artifacts

TASK-05: Frontend Implementation (프론트엔드 구현)
  → Pages, components, API integration, E2E tests
  → Covers frontend artifacts
```

---

## Task Flow Rules

- This 5-step flow is the **DEFAULT**. Only add sub-tasks (TASK-04a, TASK-04b) when complexity demands it.
- Every artifact_id from stage-spec's output_contract must be covered by at least one task.
- Tasks must have clear dependencies (e.g., TASK-03 depends on TASK-02).
- output_files must be LOCAL filesystem paths rooted at project_root, specifying the **top-level output directory** only.

---

## Task Decomposition Rules

- **Architecture** task covers ALL artifacts (it's a cross-cutting design step).
- **ERD** and **DDL** tasks cover DB-related artifacts only.
- **Backend** task covers API/server artifacts.
- **Frontend** task covers UI artifacts.
- If an artifact spans multiple tasks (e.g., OpenAPI spec is both architecture and backend), list it in `target_artifacts` for both tasks.

---

## Acceptance Criteria Rules

- Must be verifiable (file exists, compiles, tests pass, diagram renders).
- NOT PASS/FAIL judgment — just "is the task done or not."
- Examples:
  - "마이그레이션 파일이 존재하고 flyway migrate가 오류 없이 실행됨"
  - "API 엔드포인트가 200 응답을 반환함"
  - "ERD 파일이 존재하고 Mermaid 문법 오류 없이 렌더링됨"
