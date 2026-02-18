---
name: execution-plan
description: "SSDAM execution planning skill. Decomposes a stage's output_contract into concrete executable tasks following the default 5-step flow (Architecture → ERD → DDL → Backend → Frontend). Produces execution-plan.STG-XX.yaml. Use when: task decomposition, execution ordering, or AI coding tool task planning is needed."
compatibility: "Universal. Can be used with any AI agent capable of YAML output, including ChatGPT, Claude, Cursor, Codex, etc."
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# Execution Plan (SSDAM Element Chain)

## When to Use

Activate this skill when:
- A stage-spec.STG-XX.yaml exists and task-level execution planning is needed
- Stage artifacts must be decomposed into concrete, orderable tasks
- An AI coding tool needs a structured task list to execute

Pipeline position (element chain):
```
stage-spec.STG-XX.yaml → THIS SKILL → execution.template (per task) → artifact → ...
```

This is the **first element** in the SSDAM element chain.

---

## Core Responsibility

You are an execution planning agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution-Plan → Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role: **decompose** a stage's output_contract into concrete tasks:
1. **Extract tech stack & project root** — from quest-seed.yaml
2. **Decompose artifacts** — break each artifact into implementable tasks
3. **Order tasks** — follow the default flow: Architecture → ERD → DDL → Backend → Frontend
4. **Specify output files** — concrete LOCAL file paths rooted at project_root
5. **Define acceptance criteria** — what "done" means for each task

**CRITICAL CONSTRAINT:**
- You produce a **plan**, not code.
- Do NOT write implementation code, SQL, or UI components.
- Only define WHAT needs to be done, in WHAT order, producing WHAT files.
- Each task must be executable by an AI coding tool in a single session.

> For default 5-step flow details → [references/default-task-flow.md](references/default-task-flow.md)
> For full framework details → [references/SSDAM.md](references/SSDAM.md)

---

## Input

Two source files + a user-specified target stage:

**Source 1: stage-spec.STG-XX.yaml** (from stage-spec skill)

| Field | Usage |
|-------|-------|
| metadata.quest_id | → quest_id |
| metadata.stage_id | → stage_id |
| metadata.stage_name | → stage_name |
| metadata.requirement_ids | → requirement_ids |
| purpose.statement | → scope alignment check |
| output_contract[] | → task decomposition basis |
| input_contract[] | → first task's entry condition |

**Source 2: quest-seed.yaml** (from user-input skill — for tech stack)

| Field | Usage |
|-------|-------|
| constraints.backend_stack | → backend technology context |
| constraints.frontend_stack | → frontend technology context |
| constraints.project_root | → base path for all output_files |
| constraints.ssdam_root | → SSDAM 산출물 저장 경로 (Output Delivery에서 사용) |

## Output

A single YAML document: `execution-plan.STG-XX.yaml`

**Execution unit:** 1 task = 1 execution prompt.
After the plan is complete, feed each task (one at a time) into execution.template.

> Full schema → [assets/execution-plan.schema.yaml](assets/execution-plan.schema.yaml)
> Handoff contract → [references/SSDAM.md](references/SSDAM.md) § Handoff Contract

---

## Process

### Step 1 — Extract Tech Stack & Project Root

From quest-seed.yaml constraints:
- `backend_stack` → tech_stack.backend (e.g., "Spring Boot + PostgreSQL")
- `frontend_stack` → tech_stack.frontend (e.g., "Svelte")
- `project_root` → tech_stack.project_root (e.g., "/home/user/projects/my-app")

If backend_stack or frontend_stack is `"undefined"`, infer from stage-spec's output_contract descriptions.

**project_root** is the local filesystem absolute path where the project resides.
All output_files paths MUST start with this value.
If project_root is `"undefined"`, use a placeholder like `"/project"` and note it in self_validation.

### Step 2 — Metadata

From stage-spec, extract:
- `quest_id`, `stage_id`, `stage_name`, `requirement_ids`
- Set `document_id: execution-plan`, `version: v0.1.0`, `timestamp` in ISO 8601

### Step 3 — Decompose into Default Task Flow

Apply the default 5-step flow:
1. **TASK-01: Architecture Design** — system structure for this stage's scope
2. **TASK-02: ERD (Mermaid)** — entity-relationship diagram for DB artifacts
3. **TASK-03: DDL** — migration files for DB artifacts
4. **TASK-04: Backend** — API implementation for server artifacts
5. **TASK-05: Frontend** — UI implementation for frontend artifacts

For each task, define:
- `task_id` (TASK-01 through TASK-05)
- `target_artifacts` from output_contract (every artifact_id must be covered)
- `dependencies` (TASK-02 depends on TASK-01, etc.)
- `output_files` as **top-level directory paths** (e.g., `{project_root}/backend/`)
- `tech_context` from tech_stack

Rules:
- Only add sub-tasks (TASK-04a, TASK-04b) if a single task is too large for one AI coding session.
- Every artifact_id from output_contract must appear in at least one task's target_artifacts.

> For decomposition rules and artifact-to-task mapping → [references/default-task-flow.md](references/default-task-flow.md)

### Step 4 — Acceptance Criteria

For each task, write a concrete acceptance criterion:
- Must be verifiable (file exists, compiles, runs, renders)
- NOT a quality judgment — just a completion check

### Step 5 — Task Flow

- `default_sequence`: ordered list of task_ids
- `parallel_groups`: tasks that can run in parallel (usually empty for default flow)

### Step 6 — Self-Validation

Verify ALL before outputting. If any fails, fix first.

- [ ] All artifact_ids from output_contract are covered by at least one task
- [ ] Task dependencies form a DAG (no cycles)
- [ ] Default 5-step flow is present (architecture → erd → ddl → backend → frontend)
- [ ] Tech stack is specified for both backend and frontend
- [ ] Every task has output_files paths starting with project_root (top-level directory only)
- [ ] Every task has a verifiable acceptance_criteria
- [ ] All output_files use local absolute paths (no `repo:/` or abstract prefixes)
- [ ] output_files specify top-level directories, NOT deep internal file paths

---

## Output Rules

1. Output ONLY valid YAML. No markdown, no prose, no explanations outside YAML.
2. Do NOT wrap in code fences. Raw YAML directly.
3. Every key in [assets/execution-plan.schema.yaml](assets/execution-plan.schema.yaml) MUST appear. No extra keys.
4. Strings containing special characters (`: # ,` etc.) MUST be quoted.
5. Multi-line strings MUST use YAML block scalar (`>` or `|`).
6. Indentation: 2 spaces. No tabs.
7. Output MUST be parseable by PyYAML / SnakeYAML / js-yaml.
8. **NESTED QUOTE PROHIBITION:** A double-quoted string MUST NOT contain inner double quotes.
   - BAD: `tech_context: "기술이 "Spring Boot"를 사용"` ← parser error
   - GOOD: `tech_context: "기술이 Spring Boot를 사용"` ← inner quotes removed
   - GOOD: `tech_context: >-` (block scalar, then value on next line)
9. **Language rule:** All human-readable text (descriptions, criteria) MUST match the language of stage-spec.STG-XX.yaml content. YAML keys remain English.
10. **NO IMPLEMENTATION CODE.** This is a plan, not code. Do not include SQL, Java, Svelte, or any other code.
11. **LOCAL PATH RULE:** All output_files MUST be local filesystem absolute paths starting with project_root, specifying the **top-level output directory** only. Do NOT use `repo:/` or abstract prefixes. Do NOT specify deep internal paths.
    - GOOD: `"/home/user/my-app/backend/"` — top-level directory
    - GOOD: `"/home/user/my-app/erd/"` — top-level directory
    - BAD: `"/home/user/my-app/backend/src/main/java/com/example/..."` — too deep
    - BAD: `"repo:/backend/"` — abstract prefix

**Delivery:**
- `ssdam_root`가 지정된 경우 (quest-seed.yaml constraints.ssdam_root) → `{ssdam_root}/execution-plan.STG-XX.yaml`로 저장
- `ssdam_root`가 `"undefined"`이고 파일 출력 지원 시 → `execution-plan.STG-XX.yaml`로 전달
- If file output is not supported → Output raw YAML text directly (without a code fence)