# new-task: Rules & Conventions

> This file is the authoritative reference for all rules the agent must follow
> when executing the new-task skill.
>
> Source documents:
> - `en/02_core_concepts/id-metadata-conventions.md`
> - `en/02_core_concepts/glossary.md`
> - `en/03_architecture/task-lifecycle.md`
> - `en/05_references/execution.md`
> - `en/05_references/artifact.md`
> - `old-templetes/stage-spec/references/stage-design-rules.md`
> - `old-templetes/execution-plan/references/default-task-flow.md`

---

## 1. ID Conventions

All identifiers used in `task-spec.TSK-NNN.yaml` must follow these exact patterns.

| Element             | Prefix  | Format                         | Example              |
|---------------------|---------|--------------------------------|----------------------|
| Task                | `TSK`   | `TSK-NNN` (3+ digits)          | `TSK-001`            |
| Artifact            | `ART`   | `ART-TSK-NNN-NN`               | `ART-TSK-001-01`     |
| Evidence            | `EVD`   | `EVD-TSK-NNN-NN`               | `EVD-TSK-001-01`     |
| Checkpoint          | `CP`    | `CP-TSK-NNN`                   | `CP-TSK-001`         |
| Gate                | `GATE`  | `GATE-TSK-NNN`                 | `GATE-TSK-001`       |
| Criterion           | `CRIT`  | `CRIT-NN` (2+ digits)          | `CRIT-01`            |
| Execution Step      | `EXEC`  | `EXEC-NN` (2+ digits)          | `EXEC-01`            |
| Quality Policy      | `QPOL`  | `QPOL-NN` (2+ digits)          | `QPOL-01`            |
| Recovery Policy     | `RPOL`  | `RPOL-NN` (2+ digits)          | `RPOL-01`            |

### ID Rules

- IDs are **derived** from `mission-spec.yaml` (`TSK-NNN`, `CP-TSK-NNN`, `GATE-TSK-NNN`, `QPOL-NN`, `RPOL-NN`).
- IDs are **generated** by the agent for new elements (`ART-TSK-NNN-NN`, `CRIT-NN`, `EXEC-NN`, `EVD-TSK-NNN-NN`).
- `ART-TSK-NNN-NN`: `NNN` is the 3-digit task number; `NN` is a 2-digit sequence starting at `01`.
- `CRIT-NN` sequences start at `01` and increment without gaps within a task spec.
- `EXEC-NN` sequences start at `01` and increment without gaps among **included** steps only.
  - Skipped steps (e.g., ERD omitted for frontend-only task) do NOT leave gaps.
  - Example: If ERD and DDL are skipped, remaining steps are `EXEC-01`, `EXEC-02`, `EXEC-03`.

### Timestamp Format

All timestamps must be **ISO-8601 UTC**:
```
YYYY-MM-DDTHH:mm:ssZ
```
Example: `2026-02-21T09:30:00Z`

❌ Date-only (`2026-02-21`) is prohibited
❌ Missing timezone is prohibited

---

## 2. Input Contract Rules

The `input_contract` section documents what this task requires as input from predecessor tasks.

### First Task (no dependencies)

If the target task has no `dependencies` in `mission-spec.yaml`:

```yaml
input_contract:
  - input_item:           "none"
    artifact_id:          "none"
    contract_requirement: "none"
```

### Non-First Tasks

For each dependency listed in `mission-spec.task.dependencies`:
- `input_item`: describe the concrete input required (e.g., "Database schema DDL from TSK-001")
- `artifact_id`: use the `ART-TSK-NNN-NN` from the predecessor's task-spec output contract
  - If the predecessor's task-spec has not yet been generated, use placeholder `"ART-TSK-NNN-??"` and add a soft warning to `self_validation.failed_checks`
- `contract_requirement`: the verifiable condition the input must satisfy

### Input Contract Completeness

Every entry in `mission-spec.task.dependencies` must correspond to at least one `input_contract` entry.

---

## 3. Output Contract Rules

The `output_contract` section must be a **complete, concrete expansion** of `mission-spec.tasks[target].artifact.description`.

### Coverage

- Every deliverable mentioned in `artifact.description` must be represented in at least one output contract entry.
- Underspecified deliverables must be made concrete.

❌ Underspecified: `"API implementation"`
✅ Concrete: `"RESTful API endpoints for /api/v1/assets (CRUD) with OpenAPI spec at docs/api.yaml"`

### Artifact ID

- Format: `ART-TSK-NNN-NN`
- `NNN` comes from the target task number (e.g., TSK-003 → `003`).
- `NN` is a per-artifact sequence starting at `01`.
- Multiple artifacts from one task: `ART-TSK-003-01`, `ART-TSK-003-02`, etc.

### Contract Specification

Must be format-specific, structure-specific, and content-specific. Must be verifiable by inspection or automated test.

❌ Vague: `"A working backend implementation"`
✅ Concrete: `"Python FastAPI application with /api/v1/assets endpoints: GET (list), POST (create), GET/:id, PATCH/:id, DELETE/:id — each returning JSON per documented schema"`

---

## 4. Evaluation Criteria Rules

### Binary Requirement

Every criterion must be decidable as **PASS** or **FAIL** with no subjective judgment.

Forbidden terms in `criterion` and `pass_threshold`:
- `"generally"`, `"adequately"`, `"appropriately"`, `"reasonably"`, `"good enough"`, `"looks right"`
- `"most"`, `"some"`, `"sufficient"`, `"acceptable"`

### Criterion Count

- Minimum: **3 criteria** per task spec.
- No upper limit; add as many as needed to fully cover all output contract specifications.

### Measurement Method

Must specify exactly how the criterion is measured:
- `automated test` — specify test type (unit test, integration test, linter, etc.)
- `manual verification` — specify what the reviewer checks
- `file existence check` — specify the exact file path
- `CLI command` — specify the exact command and expected output

### Policy Reference

Each `policy_reference` must match a `QPOL-NN` from `mission-spec.policies.quality`.
If the mission-spec has only one quality policy, all criteria reference it.

### Pass Threshold

Must be quantitative:

❌ Vague: `"All tests pass"`
✅ Concrete: `"100% of pytest tests in /tests/test_api.py pass (0 failures, 0 errors)"`

---

## 5. Checkpoint Rules

### Derived Fields (read from mission-spec.yaml)

- `checkpoint_id`: `CP-TSK-NNN` from `mission-spec.tasks[target].checkpoint.id`
- `gate_id`: `GATE-TSK-NNN` from `mission-spec.governance.gates[target].id`
- `final_approver`: from `mission-spec.governance.roles.reviewers`
- `evaluation_policy_references`: all `QPOL-NN` from `mission-spec.policies.quality`
- `recovery_policy_reference`: `RPOL-NN` from `mission-spec.policies.recovery`

### Gate Type Selection

| gate_type   | When to use                                                               |
|-------------|---------------------------------------------------------------------------|
| `automatic` | All criteria measurable by automated tests; no human review needed        |
| `human`     | At least one criterion requires human judgment (UI review, design, etc.)  |
| `hybrid`    | Some criteria are automated; others require human review                   |

---

## 6. Recovery Mapping Rules

### Coverage

Every possible failure path must have a recovery entry. Minimum three entries covering:
1. Transient / environmental failure
2. Partial implementation failure
3. Structural / objective failure

### Strategy Selection

| Failure Type                          | Strategy          |
|---------------------------------------|-------------------|
| Transient / environmental failure     | `retry`           |
| Partial implementation failure        | `partial_fix`     |
| Task objective / structural failure   | `task_redesign`   |

### max_retry

- Derive from `mission-spec.policies.recovery.strategies.max_attempts`.
- Default: `3` if not specified in mission-spec.
- `task_redesign` strategy: always set `max_retry: 0`.

### Escalation Trigger

Format: `"After N FAILs or M time blocked, escalate to <escalation_target>"`
- Derive N from `mission-spec.governance.escalation.repeated_failure_threshold`
- Derive M from `mission-spec.governance.escalation.blocked_duration_threshold`
- Derive `<escalation_target>` from `mission-spec.governance.escalation.escalation_target`

---

## 7. Execution Plan Rules

### SOLID Principles for Step Design

The execution plan must respect the following principles (adapted from software engineering):

| Principle                 | Application to Execution Steps                                                                   |
|---------------------------|--------------------------------------------------------------------------------------------------|
| **Single Responsibility** | Each `EXEC-NN` step covers exactly one concern (architecture, data model, backend, etc.). A step must not mix concerns (e.g., "backend + frontend" in one step). |
| **Open/Closed**           | Step descriptions must be complete enough that a new agent can execute them without modifying previous steps. |
| **Liskov Substitution**   | Each step's `acceptance_criteria` must be independently verifiable without executing the next step. |
| **Interface Segregation** | Steps must not depend on artifacts they do not use. `dependencies` must list only directly required predecessor steps. |
| **Dependency Inversion**  | Steps must depend on the contracts (artifact specs), not on internal implementation details of predecessor steps. |

### Default Execution Flow

Apply the default five-step flow; include only applicable steps:

```
EXEC-01: Architecture Design         — always included
EXEC-02: Data Model (ERD)            — omit if no database entities
EXEC-03: Schema / Migration (DDL)    — omit if no database schema changes
EXEC-04: Backend Implementation      — omit if purely frontend task
EXEC-05: Frontend Implementation     — omit if no frontend work
```

### Adaptive Steps and Renumbering

**Include only steps that apply to this task. Renumber continuously without gaps.**

Example — frontend-only task (no DB, no backend):
```
EXEC-01: Architecture Design
EXEC-02: Frontend Implementation
```

Example — backend API + DB (no frontend):
```
EXEC-01: Architecture Design
EXEC-02: Data Model (ERD)
EXEC-03: Schema / Migration (DDL)
EXEC-04: Backend Implementation
```

### Step Dependency Rules

- First step (`EXEC-01`): `dependencies: []` always.
- Subsequent steps: list only **direct** predecessor step IDs (using the renumbered IDs).
- ERD step depends on Architecture step.
- DDL step depends on ERD step.
- Backend step depends on Architecture; if DDL is present, depends on DDL instead.
- Frontend step depends on Backend if present; otherwise depends on Architecture.

### Acceptance Criteria (per step)

Must specify a **verifiable completion check**:
- File exists at path X
- Command Y exits with code 0
- Schema migration runs without errors
- Component renders without console errors in dev build

❌ Vague: `"Architecture is designed"`
✅ Concrete: `"docs/architecture.md exists and contains sections: Overview, Module Boundaries, API Contracts"`

### Tech Stack

**Priority order for tech stack resolution (check in order, stop at first hit):**

1. `mission-spec.yaml` → `mission_spec.project_context` (primary source; written by `new-mission`)
2. `mission-input.yaml` → `project_context` in the same workspace's `input/` folder (fallback)
3. Neither source has usable values → **hard error** — validate.py exits 1; agent runs recovery procedure

**Resolution rules:**

- A field is considered "resolved" if its value is non-empty and not `"undefined"` / `"n/a"`.
- At least one of `backend_stack` or `frontend_stack` must be resolved (not both may be undefined).
- `database` may be `"undefined"` if the task involves no persistence layer.
- `project_root` must always be resolved; if undefined, it is also a hard error.
- **Never infer tech stack from idea description, task name, or requirement text.**

### output_files

- Must be top-level directory or file paths, not generated code content.
- `project_root` is a required value (validated as a recoverable hard check); it will always be resolved before EXEC steps are generated.
- Use `project_root` value directly in paths. Example: `["/Users/dev/my-project/src/api/"]`

### total_steps

`execution_handoff.total_steps` must equal the exact count of included steps in `execution_plan.steps`.
Skipped steps do not count.

---

## 8. Handoff Rules

### next_task_id

- Inspect `mission-spec.task_map.dependency_graph` for edges where `from == target_task_id`.
- If one outgoing edge exists, use `to` as `next_task_id`.
- If multiple outgoing edges exist, use `"PARALLEL_SPLIT"` and note both in `handoff_artifacts`.
- If no outgoing edge exists (last task in chain), set `next_task_id: "END"`.

### handoff_artifacts

- Must list all `artifact_id` values from this task's `output_contract`.
- Format: `[ART-TSK-NNN-01, ART-TSK-NNN-02, ...]`

### handoff_evidence

- List expected evidence IDs that will be generated during execution.
- Format: `[EVD-TSK-NNN-01, ...]`
- One evidence entry per evaluation criterion that produces verifiable output.
- Evidence IDs are placeholders at task-spec time; actual content is created during execution.

---

## 9. Self-Validation Rules

Perform all checks before writing the output file.

### Hard Checks (spec cannot be written if any fail)

| Check | Verification Method |
|-------|---------------------|
| Target `TSK-NNN` exists in mission-spec tasks list | Match `id` field |
| Target task `initial_state` is `PENDING` | Direct field check |
| `checkpoint_id` matches `mission-spec.tasks[target].checkpoint.id` | String match |
| `gate_id` matches `mission-spec.governance.gates` entry for this task | String match |
| All `QPOL-NN` in `evaluation_policy_references` exist in mission-spec | Reference match |
| `RPOL-NN` in `recovery_policy_reference` exists in mission-spec | Reference match |
| At least one `output_contract` entry exists | Count ≥ 1 |
| At least 3 `evaluation_criteria` entries | Count ≥ 3 |
| At least 3 `recovery_mapping` entries | Count ≥ 3 |
| All `execution_plan.steps` have unique `exec_id` values | No duplicates |
| `exec_id` sequence is consecutive starting at `EXEC-01` | Sequence check |
| `execution_handoff.total_steps` equals count of steps | Integer match |
| Every `mission-spec.task.dependencies` entry has ≥1 `input_contract` entry | Coverage check |
| `output_contract` fully covers `mission-spec.tasks[target].artifact.description` | Content coverage |

### Recoverable Hard Checks (hard error — but agent runs recovery procedure before aborting)

These checks fail like hard checks (spec is not written), but the failure triggers an
interactive recovery procedure rather than an immediate stop. See SKILL.md PRE-EXECUTION.

| Check | Error Code | Recovery Action |
|-------|-----------|-----------------|
| At least one of `backend_stack` or `frontend_stack` is not `"undefined"` (from `mission-spec.project_context` or `mission-input.yaml`) | `TECH_STACK_UNDEFINED` | Ask user for stack info; update `mission-input.yaml` and `mission-spec.project_context`; retry |
| `project_root` is not `"undefined"` (from same sources) | `PROJECT_ROOT_UNDEFINED` | Ask user for project root; update both files; retry |

### Soft Checks (write spec, add to `failed_checks`)

| Check | Warning Message |
|-------|-----------------|
| Any field contains literal `"TBD"` | `"WARNING: Field <field_path> is TBD. Resolve before executing this task."` |
| Input contract artifact_id contains `"??"` | `"WARNING: input_contract artifact_id for predecessor TSK-NNN not resolved. Generate that task-spec first."` |

### Output Rule

- All hard checks pass → `self_validation.passed: true`, write file.
- Any hard check fails → do NOT write file; report failure to user with specific check name.
- Recoverable hard check fails → do NOT write file; run recovery procedure (SKILL.md PRE-EXECUTION); re-run validate.py after recovery.
- Only soft check failures → `self_validation.passed: true`, populate `failed_checks`, write file.

---

## 10. Terminology

Use only the current (v2) terminology.

| ❌ Old (prohibited)    | ✅ Current            |
|------------------------|-----------------------|
| Quest                  | Mission               |
| Stage                  | Task                  |
| Stage Spec             | Task Spec             |
| `quest_id`             | `mission_id`          |
| `stage_id`             | `task_id`             |
| `STG-NNN`              | `TSK-NNN`             |
| `ART-STG-XX-NNN`       | `ART-TSK-NNN-NN`      |
| `CP-STG-XX`            | `CP-TSK-NNN`          |
| `GATE-STG-XX`          | `GATE-TSK-NNN`        |
| `EVD-STG-XX-NNN`       | `EVD-TSK-NNN-NN`      |
| `TASK-01` (exec step)  | `EXEC-01`             |
| `READY`                | `PENDING`             |
| `COMPLETED`            | `PASS`                |

---

## 11. Anti-Patterns

The agent must never produce output containing any of the following:

| Anti-Pattern | Why It's Prohibited |
|---|---|
| `input_contract` missing an entry for a declared task dependency | Predecessor output undocumented; execution cannot trace inputs |
| `output_contract` that does not fully cover `mission-spec.tasks[target].artifact.description` | Requirements silently dropped |
| `contract_specification` using vague language ("working", "correct", "adequate") | Not verifiable at checkpoint |
| Fewer than 3 `evaluation_criteria` | Insufficient gate coverage |
| `criterion` using forbidden terms ("generally", "appropriately", "good enough") | Not binary PASS/FAIL decidable |
| `pass_threshold` without a quantitative value | Unenforceable |
| Execution step covering more than one concern | Violates Single Responsibility; creates ambiguous checkpoint |
| Gap in `exec_id` sequence (e.g., EXEC-01 then EXEC-03 with no EXEC-02) | Breaks flow reference integrity |
| `total_steps` not matching actual step count | Misleads execution agent |
| `next_task_id` not in mission-spec task list and not `"END"` | Broken handoff chain |
| `handoff_artifacts` missing an artifact from `output_contract` | Evidence not propagated to next task |
| `self_validation.passed: false` in written output | Failed spec must never be saved |
| Tech stack inferred from task name or idea description | Agent hallucination — only derive from mission-spec.project_context or mission-input.yaml |
| `acceptance_criteria` that cannot be verified without running the next step | Violates Liskov Substitution |
