# SSDAM Agent Prompt — Execution Plan

<protocol>
  <framework>
    name: SSDAM (SOLID Stage-Driven Automation Mechanism)
    purpose: A quality/validation/evidence-centered execution mechanism where Stage is the top-level purpose unit.
    core_flow: Each Stage follows → Execution-Plan → Execution → Artifact → Evaluation → Evidence → Checkpoint → (Next Stage | Recovery)
    principles:
      - Stage is a purpose unit, not a task unit.
      - Progress is defined by Checkpoint PASS, not by activity completion.
      - All decisions require Evidence. No evidence-free judgment is permitted.
      - Failure is a designed state transition event, not an exception.
    element_chain: execution-plan → execution → artifact → evaluation → evidence → checkpoint → (recovery)
  </framework>

  <position>
    template_id: execution-plan.template
    phase: element (04_elements)
    role: Decomposes a stage's output_contract into concrete, executable tasks for AI coding tools.
    predecessor: stage-spec.template
    successor: execution.template
  </position>

  <input_contract>
    source_templates:
      - stage-spec.template (stage-spec.STG-XX.yaml)
      - user-input.template (quest-seed.yaml — for tech stack)
    source_files:
      - stage-spec.STG-XX.yaml
      - quest-seed.yaml
    required_fields_from_stage_spec:
      - metadata.quest_id → quest_id
      - metadata.stage_id → stage_id
      - metadata.stage_name → stage_name
      - metadata.requirement_ids → requirement_ids
      - purpose.statement → scope alignment
      - output_contract[] → artifacts to decompose into tasks
      - input_contract[] → entry conditions (for first task)
    required_fields_from_quest_seed:
      - constraints.backend_stack → backend technology
      - constraints.frontend_stack → frontend technology
      - constraints.project_root → local filesystem project root path
    how_to_use: |
      The user will paste this template together with stage-spec.STG-XX.yaml and quest-seed.yaml.
      Read the output_contract from stage-spec and decompose it into executable tasks.
      Read the tech stack from quest-seed to specify concrete tools and frameworks per task.
      Read the project_root from quest-seed to use as the base path for all output_files.
  </input_contract>

  <output_contract>
    format: YAML (.yaml file)
    output_filename: execution-plan.STG-XX.yaml
    target_template: execution.template
    handoff_fields:
      - metadata (quest_id, stage_id)
      - tech_stack (backend, frontend)
      - tasks[] (task_id, task_name, task_type, description, target_artifacts, dependencies, output_files, tech_context, acceptance_criteria)
      - task_flow.default_sequence → execution order
  </output_contract>

  <next_action>
    on_complete: |
      Output a single YAML document as execution-plan.STG-XX.yaml.
      After the plan is complete, feed each task (one at a time) together with
      stage-spec.STG-XX.yaml into execution.template for an AI coding tool to execute.
      Execution unit: 1 task = 1 execution prompt.
  </next_action>
</protocol>

<system>
You are an execution planning agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution-Plan → Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role is to **decompose** a stage's output_contract into concrete tasks:
1. **Extract tech stack & project root** — identify backend/frontend technologies and project_root from quest-seed.
2. **Decompose artifacts** — break each artifact into implementable tasks.
3. **Order tasks** — follow the default flow: Architecture → ERD → DDL → Backend → Frontend.
4. **Specify output files** — define concrete LOCAL file paths each task must produce, rooted at project_root.
5. **Define acceptance criteria** — what "done" means for each task.

**CRITICAL CONSTRAINT:**
- You produce a **plan**, not code.
- Do NOT write implementation code, SQL, or UI components.
- Only define WHAT needs to be done, in WHAT order, producing WHAT files.
- Each task must be executable by an AI coding tool in a single session.
</system>

<context>
This template sits between stage-spec and execution in the SSDAM element chain:

```
stage-spec.STG-XX.yaml → THIS TEMPLATE → execution.template (per task) → artifact → ...
```

### Default Task Flow

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

**Rules:**
- This 5-step flow is the DEFAULT. Only add sub-tasks (TASK-04a, TASK-04b) when complexity demands it.
- Every artifact_id from stage-spec's output_contract must be covered by at least one task.
- Tasks must have clear dependencies (e.g., TASK-03 depends on TASK-02).
- output_files must be LOCAL filesystem paths rooted at project_root, specifying the **top-level output directory** only (e.g., `{project_root}/docs/`, `{project_root}/backend/`). Internal directory structure within each top-level directory is the AI coding tool's responsibility during execution.

### Task Decomposition Rules
- Architecture task covers ALL artifacts (it's a cross-cutting design step).
- ERD and DDL tasks cover DB-related artifacts only.
- Backend task covers API/server artifacts.
- Frontend task covers UI artifacts.
- If an artifact spans multiple tasks (e.g., OpenAPI spec is both architecture and backend), list it in target_artifacts for both tasks.

### Acceptance Criteria Rules
- Must be verifiable (file exists, compiles, tests pass, diagram renders).
- NOT PASS/FAIL judgment — just "is the task done or not."
- Examples: "마이그레이션 파일이 존재하고 flyway migrate가 오류 없이 실행됨", "API 엔드포인트가 200 응답을 반환함"
</context>

<input>
Attached files:
1. **stage-spec.STG-01.yaml** (output from stage-spec.template)
2. **quest-seed.yaml** (output from user-input.template — for tech stack)

Target stage: **STG-01** (specified by user)

Read the following fields from stage-spec.STG-01.yaml:
- `metadata.quest_id` → use as quest_id
- `metadata.stage_id` → use as stage_id
- `metadata.stage_name` → use as stage_name
- `metadata.requirement_ids` → use as requirement_ids
- `purpose.statement` → use for scope alignment check
- `output_contract[]` → use as task decomposition basis
- `input_contract[]` → use for first task's entry condition

Read the following fields from quest-seed.yaml:
- `constraints.backend_stack` → use as backend technology context
- `constraints.frontend_stack` → use as frontend technology context
- `constraints.project_root` → use as base path for all output_files

<attached_file>
# SSDAM Stage Specification
# source_template: stage-spec.template
# schema_version: v1.0.0
# input_files: [quest-seed.yaml, quest-plan.yaml]

metadata:
  quest_id: "QST-20260216-001"
  stage_id: "STG-01"
  stage_name: "소유 자료 3Depth 조회·상세 보기"
  document_id: stage-spec
  stage_owner: "stage_owner"
  version: "v0.1.0"
  timestamp: "2026-02-17T15:00:00+09:00"
  requirement_ids: [REQ-001, REQ-002, REQ-003]

purpose:
  statement: "기본 제공 자료와 구매 자료가 숨김 처리된 항목을 제외하고 3Depth(폴더→하위폴더→자료)로 탐색되며 더블클릭(또는 동등 상호작용)으로 상세 보기(이미지 확대/동영상 재생)가 동작하는 소유 자료 조회 경험을 PASS 기준으로 확정한다."
  scope_included:
    - "소유 자료 페이지의 3Depth 탐색 UI 및 상호작용(폴더/하위폴더/자료 선택)"
    - "자료 상세 보기(이미지 확대 또는 동영상 재생) 화면/모달 및 진입 동작"
    - "소유 자료 목록 조회 API(기본 제공 + 구매 자료)와 숨김 제외 로직"
    - "3Depth 탐색을 위한 최소 DB 스키마 및 마이그레이션(폴더/하위폴더/자료/소유 상태)"
    - "핵심 시나리오 E2E(탐색/상세보기) 및 백엔드 통합 테스트"
  scope_excluded:
    - "편집 모드(이름 변경/이동/복사/숨기기) 기능"
    - "업로드/내 업로드 관리 및 파일 타입 검증"
    - "공개 자료 마켓/검색/구매 처리 및 구매 이력 UI"
    - "실제 결제/정산, DRM/워터마크, 대규모 스트리밍 최적화(CDN/트랜스코딩)"

input_contract:
  - input_item: "none"
    artifact_id: "none"
    contract_requirement: "시작 스테이지이므로 선행 산출물 입력 없음"

output_contract:
  - output_artifact: "3Depth 탐색 및 상세 보기 동작이 확인 가능한 소유 자료 페이지(프론트엔드)"
    artifact_id: "ART-STG-01-001"
    contract_specification: >-
      Svelte 기반 소유 자료 페이지 1개 이상을 제공하며,
      (1) 폴더→하위폴더→자료의 3Depth 탐색이 가능하고,
      (2) 자료 항목 더블클릭(또는 동등 상호작용) 시 상세 보기 UI가 열린다.
      상세 보기 UI는 이미지(확대 가능) 또는 동영상(재생 가능)을 렌더링한다.
      숨김 처리된 자료는 목록에 표시되지 않는다.
  - output_artifact: "소유 자료 3Depth 조회/상세 조회 백엔드 API + OpenAPI 계약"
    artifact_id: "ART-STG-01-002"
    contract_specification: >-
      Spring Boot 기반 REST API를 제공하며,
      (1) 소유 자료 3Depth 트리 조회 엔드포인트 1개 이상,
      (2) 자료 상세 조회(메타데이터 및 미디어 접근 정보) 엔드포인트 1개 이상,
      (3) OpenAPI 스펙 파일 1개(repo:/docs/api/openapi.yaml)를 포함한다.
      API는 기본 제공 자료와 구매 자료를 통합하여 반환하며, 숨김 처리된 자료는 제외한다.
  - output_artifact: "3Depth 탐색을 위한 최소 DB 스키마 및 마이그레이션"
    artifact_id: "ART-STG-01-003"
    contract_specification: >-
      PostgreSQL 마이그레이션 파일 1개 이상(repo:/db/migration/)을 포함하며,
      (1) 폴더, 하위폴더, 자료(미디어) 엔티티의 3Depth 관계를 표현할 수 있고,
      (2) 사용자별 소유 상태(기본 제공/구매) 및 숨김 여부를 저장할 수 있다.
      외래키/유니크 제약 등 기본 정합성 제약을 포함한다.

evaluation_criteria:
  - criterion_id: "CRIT-01"
    criterion: "REQ-001: 기본 제공 자료가 3Depth(폴더→하위폴더→자료) 구조로 조회 가능해야 하며, E2E 핵심 시나리오(3Depth 탐색) 실패 건수는 0이어야 한다."
    policy_reference: "QPOL-02"
    measurement_method: "Playwright/Cypress에서 3Depth 탐색 핵심 시나리오 1개 이상 실행 후 실패 건수 집계"
    pass_threshold: "= 0"
  - criterion_id: "CRIT-02"
    criterion: "REQ-002: 소유 자료 페이지에서 기본 제공 + 구매 자료가 통합 목록으로 표시되어야 하며, 숨김 처리된 자료 노출 오류 건수는 0이어야 한다."
    policy_reference: "QPOL-04"
    measurement_method: "백엔드 통합 테스트에서 숨김 자료 포함 케이스를 포함하여 노출 오류(숨김 노출/미소유 노출/소유 누락) 건수 집계"
    pass_threshold: "= 0"
  - criterion_id: "CRIT-03"
    criterion: "REQ-003: 소유 자료 페이지에서 더블클릭(또는 동등 상호작용)으로 상세 보기(이미지 확대/동영상 재생 포함)가 제공되어야 하며, E2E 핵심 시나리오(상세 보기) 실패 건수는 0이어야 한다."
    policy_reference: "QPOL-02"
    measurement_method: "Playwright/Cypress에서 상세 보기 핵심 시나리오 1개 이상 실행 후 실패 건수 집계"
    pass_threshold: "= 0"
  - criterion_id: "CRIT-04"
    criterion: "백엔드 API 통합 테스트 통과율이 95% 이상이어야 한다."
    policy_reference: "QPOL-01"
    measurement_method: "Spring Boot 테스트 실행 결과(JUnit/Gradle 또는 Maven)에서 통과율 계산"
    pass_threshold: ">= 95%"
  - criterion_id: "CRIT-05"
    criterion: "정적 분석/린트 오류 건수는 0이어야 한다."
    policy_reference: "QPOL-03"
    measurement_method: "백엔드(Checkstyle/SpotBugs 등) 및 프론트엔드(ESLint) 실행 결과의 오류 건수 합산"
    pass_threshold: "= 0"

checkpoint:
  checkpoint_id: "CP-STG-01"
  gate_id: "GATE-STG-01"
  gate_type: "hybrid"
  final_approver: "stage_owner"
  evaluation_policy_references: [QPOL-01, QPOL-02, QPOL-03, QPOL-04]
  recovery_policy_reference: "RPOL-01"

handoff:
  next_stage_id: "STG-02"
  handoff_artifacts: [ART-STG-01-001, ART-STG-01-002, ART-STG-01-003]
  handoff_evidence: [EVD-STG-01-001, EVD-STG-01-002, EVD-STG-01-003, EVD-STG-01-004]

recovery_mapping:
  - failure_type: "테스트 실패(단위/통합/E2E)"
    rpol_reference: "RPOL-01"
    max_retry: 2
    recovery_strategy: "Re-execution"
    escalation_trigger: "동일 스테이지에서 연속 실패가 N >= 2이면 ESC-FAIL-N 적용"
  - failure_type: "테스트 실패(단위/통합/E2E) 재시도 후에도 실패 지속"
    rpol_reference: "RPOL-01"
    max_retry: 2
    recovery_strategy: "Correction"
    escalation_trigger: "수정 후에도 연속 실패가 N >= 2이면 ESC-FAIL-N 적용"
  - failure_type: "데이터/권한 정합성 실패(소유 상태/숨김 상태 불일치 또는 미소유 접근)"
    rpol_reference: "RPOL-02"
    max_retry: 1
    recovery_strategy: "Re-stage"
    escalation_trigger: "risk_level >= 2 또는 권한 모델 변경 필요 시 ESC-RISK 적용"
  - failure_type: "데이터/권한 정합성 실패가 모델/스키마 변경을 요구하거나 롤백이 필요한 경우"
    rpol_reference: "RPOL-02"
    max_retry: 1
    recovery_strategy: "Rollback"
    escalation_trigger: "stage_owner 수동 승인 필수, 필요 시 quest_owner로 ESC-RISK 에스컬레이션"
  - failure_type: "요구사항 해석 불명확 또는 판정 불확실성 증가"
    rpol_reference: "RPOL-04"
    max_retry: 1
    recovery_strategy: "Correction"
    escalation_trigger: "uncertainty > 0.35이면 ESC-UNCERTAINTY 적용"

self_validation:
  purpose_single_sentence_testable: true
  input_output_contracts_verifiable: true
  all_criteria_pass_fail_decidable: true
  all_criteria_reference_policy_ids: true
  checkpoint_gate_type_valid: true
  recovery_references_rpol_ids: true
  handoff_fields_complete: true
  solid_principles_applied: true
</attached_file>

<attached_file>
# SSDAM Quest Seed
# source_template: user-input.template
# schema_version: v1.0.0

idea_validation:
  status: PASS
  checks:
    has_goal: true
    has_testable_outcome: true
    is_actionable: true

metadata:
  quest_id: "QST-20260216-001"
  quest_name: "이미지/동영상 라이브러리 + 업로드 + 마켓(구매) 토이 웹앱"
  quest_owner: "undefined"
  domain: "software development (web application)"
  timestamp: "2026-02-16T18:00:00+09:00"

goal:
  statement: "Spring Boot + PostgreSQL + Svelte로 이미지/동영상 파일을 3Depth로 관리하고(보기/편집), 업로드·공개 설정·검색·구매·구매내역 확인까지 가능한 학습용 토이 웹앱을 구현한다."
  success_criteria:
    - id: SC-01
      description: "기본 제공 자료와 구매한 자료가 '소유 자료 페이지'에서 3Depth(폴더→하위폴더→자료)로 조회되면 PASS."
    - id: SC-02
      description: "사용자가 이미지/동영상 파일만 업로드할 수 있고, 업로드된 파일의 이름 변경 및 공개/비공개 설정을 변경할 수 있으면 PASS."
    - id: SC-03
      description: "다른 사용자가 공개한 파일을 이름/태그로 검색하여 조회하고, 구매 처리 후 구매 표시(테두리/체크 등)와 구매 목록 반영이 되면 PASS."
  out_of_scope:
    - "실제 결제 PG 연동(카드/간편결제 등) 및 정산"
    - "DRM/워터마크/저작권 분쟁 처리"
    - "대규모 트래픽/대용량 미디어 스트리밍 최적화(CDN, 트랜스코딩 파이프라인 등)"

requirements:
  - id: REQ-001
    statement: "시스템은 기본 제공 이미지/동영상 자료를 3Depth(폴더→하위폴더→자료) 구조로 조회할 수 있어야 한다."
    priority: must
  - id: REQ-002
    statement: "시스템은 소유 자료 페이지에서 사용자의 소유 자료(기본 제공 + 구매한 자료)를 숨김 처리된 자료를 제외하고 목록으로 표시해야 한다."
    priority: must
  - id: REQ-003
    statement: "시스템은 소유 자료 페이지에서 더블클릭(또는 동등한 상호작용)으로 자료 상세 보기(이미지 확대/동영상 재생 포함)를 제공해야 한다."
    priority: must
  - id: REQ-004
    statement: "시스템은 소유 자료 페이지에서 편집 모드 시 자료의 이름 변경/이동/복사/숨기기 기능을 제공해야 한다."
    priority: should
  - id: REQ-005
    statement: "시스템은 사용자가 이미지/동영상 파일만 업로드할 수 있도록 제한해야 하며, 업로드된 파일을 업로드 일자 기준으로 조회할 수 있어야 한다."
    priority: must
  - id: REQ-006
    statement: "시스템은 사용자가 업로드한 파일에 대해 이름 변경 및 타 사용자에게 표시 여부(공개/비공개)를 설정할 수 있어야 하며, 각 파일의 구매 횟수를 표시해야 한다."
    priority: should
  - id: REQ-007
    statement: "시스템은 다른 사용자가 공개한 파일을 목록으로 조회할 수 있어야 하며, 이름 또는 #태그로 검색할 수 있어야 한다."
    priority: must
  - id: REQ-008
    statement: "시스템은 다른 사용자가 공개한 파일에 대해 구매 기능을 제공해야 하며, 구매 완료된 파일은 구매 표시(테두리/체크 등) 또는 구매 항목 숨기기로 구분할 수 있어야 한다."
    priority: must

stages:
  - id: STG-01
    name: "소유 자료 3Depth 조회·상세 보기"
    purpose: "기본 제공 자료와 구매 자료를 3Depth로 탐색하고 상세 보기까지 가능한 소유 자료 조회 경험을 확정한다."
    key_artifact: "3Depth 자료 탐색/상세 보기 동작이 확인 가능한 소유 자료 페이지(프론트 + 백엔드 API + DB 스키마 최소 세트)"
    mapped_requirements: [REQ-001, REQ-002, REQ-003]
  - id: STG-02
    name: "소유 자료 편집 및 업로드 관리"
    purpose: "소유 자료의 편집(이름/이동/복사/숨김)과 사용자 업로드 자료의 제한 업로드·조회·공개 설정을 확정한다."
    key_artifact: "편집 모드가 포함된 소유 자료 페이지 + 업로드/내 업로드 관리 페이지 + 관련 API/DB 스키마"
    mapped_requirements: [REQ-004, REQ-005, REQ-006]
  - id: STG-03
    name: "공개 자료 마켓·검색·구매 흐름"
    purpose: "타 사용자 공개 자료의 조회/검색과 구매 처리, 구매 표시 및 소유 자료 반영을 통해 마켓 가치 흐름을 완결한다."
    key_artifact: "공개 자료 페이지(검색/구매/구매표시) + 구매 기록/권한 반영 로직 + 관련 API/DB 스키마"
    mapped_requirements: [REQ-007, REQ-008, REQ-002]

constraints:
  timeline: "undefined"
  budget: "undefined"
  backend_stack: "Spring Boot + PostgreSQL"
  frontend_stack: "Svelte"
  team: "undefined"
  risks:
    - "미디어 파일 저장 방식(로컬/오브젝트 스토리지)과 서빙 방식 선택에 따라 구현 난이도가 크게 달라질 수 있음"
    - "구매/소유 권한 모델(소유/공개/구매내역) 설계가 불명확하면 페이지 간 데이터 정합성이 깨질 수 있음"
  existing_artifacts: []

handoff:
  next_template: quest-plan.template
  payload:
    quest_id: "QST-20260216-001"
    quest_owner: "undefined"
    quest_goal: "Spring Boot + PostgreSQL + Svelte로 이미지/동영상 파일을 3Depth로 관리하고(보기/편집), 업로드·공개 설정·검색·구매·구매내역 확인까지 가능한 학습용 토이 웹앱을 구현한다."
    domain: "software development (web application)"
    stage_list: [STG-01, STG-02, STG-03]
    requirement_ids: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008]
  instruction: >
    Feed this YAML file together with quest-plan.template.md
    into your next AI call.

self_validation:
  goal_is_testable: true
  all_requirements_pass_fail: true
  all_requirements_mapped: true
  all_stages_single_purpose: true
  handoff_complete: true
  no_vague_terms: true
  constraints_filled: true
</attached_file>
</input>

<instructions>
Produce an execution plan by following these 6 steps.
Your final output MUST be a single YAML document matching the schema in <output_format>.

## Step 1: Extract Tech Stack & Project Root

From quest-seed.yaml constraints:
- backend_stack → tech_stack.backend (e.g., "Spring Boot + PostgreSQL")
- frontend_stack → tech_stack.frontend (e.g., "Svelte")
- project_root → tech_stack.project_root (e.g., "/home/user/projects/my-app")

If backend_stack or frontend_stack is "undefined", infer from stage-spec's output_contract
descriptions (which often mention specific frameworks).

**project_root** is the local filesystem absolute path where the project resides.
All output_files paths MUST start with this value. If project_root is "undefined",
use a placeholder like "/project" and note it in self_validation.

## Step 2: Write Metadata

From stage-spec, extract:
- quest_id, stage_id, stage_name, requirement_ids

## Step 3: Decompose into Default Task Flow

Apply the 5-step default flow:
1. **Architecture Design** — System structure for this stage's scope
2. **ERD (Mermaid)** — Entity-Relationship diagram for DB artifacts
3. **DDL** — Migration files for DB artifacts
4. **Backend** — API implementation for server artifacts
5. **Frontend** — UI implementation for frontend artifacts

For each task:
- Assign task_id (TASK-01 through TASK-05)
- Map target_artifacts from output_contract
- Define dependencies (TASK-02 depends on TASK-01, etc.)
- List output_files as top-level directory paths (e.g., {project_root}/backend/)
- Specify tech_context from tech_stack

**Rules:**
- Only add sub-tasks if a single task would be too large for one AI coding session.
- Every artifact_id from output_contract must appear in at least one task's target_artifacts.

## Step 4: Define Acceptance Criteria

For each task, write a concrete acceptance criterion:
- Must be verifiable (file exists, compiles, runs)
- NOT a quality judgment — just completion check

## Step 5: Define Task Flow

- default_sequence: ordered list of task_ids
- parallel_groups: tasks that can run in parallel (usually empty for default flow)

## Step 6: Self-Validation

Verify ALL items before outputting. If any fails, fix it first.

- All artifact_ids from output_contract are covered by at least one task.
- Task dependencies form a DAG (no cycles).
- Default 5-step flow is present (architecture → erd → ddl → backend → frontend).
- Tech stack is specified for both backend and frontend.
- Every task has output_files paths starting with project_root (top-level directory only).
- Every task has a verifiable acceptance_criteria.
- All output_files use local absolute paths (no `repo:/` or abstract prefixes).
- output_files specify top-level directories, NOT deep internal file paths.
</instructions>

<output_format>
Output a SINGLE YAML document. No markdown, no prose, no explanations outside the YAML.

**Language rule:** All human-readable text (descriptions, criteria) MUST be in the
same language as the stage-spec.STG-01.yaml content. YAML keys remain in English.

**YAML Schema — follow this structure EXACTLY. Do not add, remove, rename, or reorder keys.**

```yaml
# SSDAM Execution Plan
# source_template: execution-plan.template
# schema_version: v1.0.0
# input_files: [stage-spec.STG-01.yaml, quest-seed.yaml]

metadata:
  quest_id: "from stage-spec"
  stage_id: "STG-01"
  stage_name: "from stage-spec"
  document_id: execution-plan
  version: "v0.1.0"
  timestamp: "ISO 8601"
  requirement_ids: [REQ-XXX, REQ-YYY]  # from stage-spec metadata.requirement_ids

tech_stack:
  backend: "from quest-seed constraints.backend_stack"   # e.g., "Spring Boot + PostgreSQL"
  frontend: "from quest-seed constraints.frontend_stack"  # e.g., "Svelte"
  project_root: "from quest-seed constraints.project_root"  # e.g., "/home/user/projects/my-app"

tasks:
  - task_id: "TASK-01"
    task_name: "아키텍처 설계"  # 언어 규칙 준수
    task_type: "architecture"   # architecture / erd / ddl / backend / frontend
    description: "태스크 설명"  # 언어 규칙 준수
    target_artifacts: [ART-STG-01-001, ART-STG-01-002]  # 이 태스크가 기여하는 artifact_id
    dependencies: []  # 선행 task_id 목록
    output_files:     # project_root 기준 상위 디렉토리 경로 목록. 내부 구조는 실행 시 결정.
      - "{project_root}/docs/"
    tech_context: "사용 기술/도구"  # 언어 규칙 준수
    acceptance_criteria: "완료 기준"  # 언어 규칙 준수. 검증 가능해야 함

  - task_id: "TASK-02"
    task_name: "ERD 설계"
    task_type: "erd"
    description: "Mermaid 기반 ERD 다이어그램 작성"
    target_artifacts: [ART-STG-01-003]
    dependencies: [TASK-01]
    output_files:
      - "{project_root}/erd/"
    tech_context: "Mermaid"
    acceptance_criteria: "ERD 파일이 존재하고 Mermaid 문법 오류 없이 렌더링됨"

  # TASK-03 (ddl), TASK-04 (backend), TASK-05 (frontend) 동일 패턴...

task_flow:
  default_sequence: [TASK-01, TASK-02, TASK-03, TASK-04, TASK-05]
  parallel_groups: []  # 병렬 실행 가능한 태스크 그룹 (있으면)

handoff:
  next_element: execution.template
  execution_unit: "task"  # task 1개 = execution 1회
  total_executions: 5     # tasks 배열 길이와 일치

self_validation:
  all_artifacts_covered: true/false
  task_dependencies_acyclic: true/false
  default_flow_complete: true/false
  tech_stack_specified: true/false
  all_paths_use_project_root: true/false  # 모든 output_files가 project_root로 시작하는지
```

**CRITICAL RULES:**
1. Output ONLY valid YAML. No markdown headers, no commentary, no explanations.
2. Do NOT wrap the output in code fences (``` or ```yaml). Output raw YAML directly.
3. Every key shown above MUST appear in your output.
4. Do NOT add keys not shown in the schema.
5. All string values containing special characters (colons, #, commas, etc.) MUST be quoted.
6. Multi-line strings MUST use YAML block scalar (> or |).
7. Indentation MUST use 2 spaces consistently. No tabs.
8. The output MUST be parseable by any standard YAML parser (e.g., PyYAML, SnakeYAML, js-yaml).
9. **NESTED QUOTE PROHIBITION:** A double-quoted string MUST NOT contain inner double quotes.
   - BAD:  `tech_context: "기술이 "Spring Boot"를 사용"`  ← parser error
   - GOOD: `tech_context: "기술이 Spring Boot를 사용"`  ← inner quotes removed
   - GOOD: `tech_context: >-`  (block scalar, then value on next line)
   If a value references another field's quoted content, drop the inner quotes or use `>-` block scalar.
10. **NO IMPLEMENTATION CODE.** This is a plan, not code. Do not include SQL, Java, Svelte, or any other code.
11. **LOCAL PATH RULE:** All output_files MUST be local filesystem absolute paths starting with project_root, specifying the **top-level output directory** only. Do NOT use `repo:/` or abstract prefixes. Do NOT specify deep internal paths (package structure, nested subdirectories). Internal structure is decided by the AI coding tool during execution.
    - GOOD: `"/home/user/my-app/backend/"` — top-level directory
    - GOOD: `"/home/user/my-app/erd/"` — top-level directory
    - BAD:  `"/home/user/my-app/backend/src/main/java/com/example/..."` — too deep
    - BAD:  `"repo:/backend/"` — abstract prefix

**OUTPUT DELIVERY:**
If the AI tool supports file output (e.g., Claude Artifacts, ChatGPT Canvas, file download),
deliver the output as a downloadable file named `execution-plan.STG-01.yaml`.
If file output is not available, output raw YAML text directly (no code fences).
</output_format>
</input>

결과를 다운로드 할 수 있는 파일로 작성해줘.
