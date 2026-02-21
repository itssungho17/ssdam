# new-mission: Rules & Conventions

> This file is the authoritative reference for all rules the agent must follow
> when executing the new-mission skill.
>
> Source documents:
> - `en/02_core_concepts/id-metadata-conventions.md`
> - `en/02_core_concepts/glossary.md`
> - `en/03_architecture/task-lifecycle.md`
> - `en/05_references/`

---

## 1. ID Conventions

All identifiers must follow these exact patterns. No exceptions.

| Element             | Prefix  | Format                      | Example              |
|---------------------|---------|-----------------------------|----------------------|
| Mission             | `MIS`   | `MIS-YYYYMMDD-NNN`          | `MIS-20260221-001`   |
| Task                | `TSK`   | `TSK-NNN` (3+ digits)       | `TSK-001`            |
| Requirement         | `REQ`   | `REQ-NNN` (3+ digits)       | `REQ-001`            |
| Success Criterion   | `SC`    | `SC-NNN` (3+ digits)        | `SC-001`             |
| Checkpoint          | `CP`    | `CP-TSK-NNN`                | `CP-TSK-001`         |
| Recovery            | `RCV`   | `RCV-TSK-NNN-NN`            | `RCV-TSK-001-01`     |
| Gate                | `GATE`  | `GATE-TSK-NNN`              | `GATE-TSK-001`       |
| Quality Policy      | `QPOL`  | `QPOL-NN` (2+ digits)       | `QPOL-01`            |
| Recovery Policy     | `RPOL`  | `RPOL-NN` (2+ digits)       | `RPOL-01`            |
| Traceability Policy | `TPOL`  | `TPOL-NN` (2+ digits)       | `TPOL-01`            |

### ID Rules

- IDs are **never reused**. Once assigned, an ID is retired even if the element is deleted.
- IDs must not encode runtime states or execution order.
- `NNN` sequences start at `001` and increment without gaps within a mission.
- `mission_id` sequence: check existing `.ssdam/MIS-YYYYMMDD-*` folders to determine NNN.

### Timestamp Format

All timestamps must be **ISO-8601 UTC**:
```
YYYY-MM-DDTHH:mm:ssZ
```
Example: `2026-02-21T09:30:00Z`

❌ Date-only (`2026-02-21`) is prohibited
❌ Missing timezone is prohibited

---

## 2. Task State Machine

Tasks are created in `PENDING` state. Only the following transitions are valid:

```
PENDING     → IN_PROGRESS  (entry conditions satisfied)
PENDING     → BLOCKED      (dependency unresolvable before start)
IN_PROGRESS → PASS         (Checkpoint PASS)
IN_PROGRESS → FAILED       (Checkpoint FAIL)
IN_PROGRESS → BLOCKED      (dependency / constraint violated mid-execution)
BLOCKED     → IN_PROGRESS  (dependency resolved / constraint lifted)
BLOCKED     → FAILED       (escalation decision)
FAILED      → IN_PROGRESS  (recovery completed → re-entry)
```

### Immutable State Rules

1. A Task may **never** transition directly from `PENDING` to `PASS`.
2. A Task may **never** be marked `PASS` without a recorded Checkpoint.
3. A Task may **never** skip the `IN_PROGRESS` state.
4. `PASS` and `FAILED` are **terminal states** — no further transitions.
5. `BLOCKED` is not a terminal state — it must resolve to `IN_PROGRESS` or `FAILED`.

### Initial State

All tasks in `mission-spec.yaml` must have `initial_state: PENDING`.
The agent does not assign any other initial state at mission creation time.

---

## 3. Terminology

Use only the current (v2) terminology. The old terminology is prohibited.

| ❌ Old (prohibited)  | ✅ Current           |
|----------------------|----------------------|
| Quest                | Mission              |
| Stage                | Task                 |
| `quest_id`           | `mission_id`         |
| `stage_id`           | `task_id`            |
| `STG-NNN`            | `TSK-NNN`            |
| `GATE-STG-NNN`       | `GATE-TSK-NNN`       |
| `READY`              | `PENDING`            |
| `COMPLETED`          | `PASS`               |
| `RE-STAGE`           | Task Redesign        |
| Stage Spec           | Task Spec            |
| quest-seed.yaml      | (merged into mission-spec.yaml) |
| quest-plan.yaml      | mission-spec.yaml    |

---

## 4. Coverage Rules

These rules are enforced at self-validation (Step 15).

- Every `REQ-NNN` must be covered by **at least one task**.
  **This applies to ALL requirement types without exception — `type: non_functional`
  is NOT exempt.** Non-functional requirements (latency, security, reliability, etc.)
  must be explicitly assigned to at least one task's `requirements` field,
  or to a dedicated verification/performance task if no other task covers them.
- Every `TSK-NNN` must satisfy **at least one requirement**.
- Every `TSK-NNN` must have exactly one Checkpoint (`CP-TSK-NNN`).
- Every `TSK-NNN` must have exactly one Gate (`GATE-TSK-NNN`).
- Every `TSK-NNN` must produce at least one describable artifact.
- The `task_list` in `handoff.payload` must list tasks in **dependency order**.

### Dependency Graph Completeness

The `task_map.dependency_graph` must be a **complete representation** of all
direct dependencies declared in `task.dependencies`.

Formal rule: for every Task B where `B.dependencies` contains Task A,
the entry `{from: "A", to: "B", type: "..."}` **must** exist in `dependency_graph`.

```
# Example: TSK-004 has dependencies: ["TSK-001", "TSK-003"]
# Both edges are required in dependency_graph:
dependency_graph:
  - {from: TSK-001, to: TSK-004, type: sequential}   ← required
  - {from: TSK-003, to: TSK-004, type: sequential}   ← required
```

Transitive reachability does **not** substitute for explicit direct dependency edges.
If A→B and B→C are both declared in dependencies, both edges must be in the graph,
even though A→C is reachable transitively.

---

## 5. Governance Rules

### Roles

- `mission_owner` must be a named person or role (not a team or department).
- Every task must have a named `task_owner`.
- `reviewers` must include at least one person other than the task owner.

**Solo / Empty Team Edge Case:**
If `input.team` is empty (`[]`) or every team member shares the same identity as
`mission_owner` (i.e., no distinct reviewer candidate exists):
1. Set `governance.roles.reviewers` to `["TBD"]`
2. Set `governance.escalation.escalation_target` to `"TBD"`
3. Add the following entry to `self_validation.failed_checks`:
   ```
   "WARNING: No reviewer distinct from task_owner.
    Assign a reviewer in mission-input.yaml before executing tasks."
   ```
4. The spec **may still be written** with `self_validation.passed: true`,
   but the `failed_checks` warning entry is **mandatory**.
   A spec with an empty-team governance issue but no warning is invalid.

### Gates

- Gate criteria must be **binary (PASS/FAIL)** — no subjective criteria allowed.
- A task cannot be marked `PASS` if its gate criteria are not met.
- Gates are evaluated at Checkpoint time, not before.

### Escalation

- `repeated_failure_threshold` must be a positive integer.
- `blocked_duration_threshold` must be a time value (e.g., `"24h"`, `"3 days"`).
- `escalation_target` must be a named person or role from `governance.roles`.

---

## 6. Constraint Rules

- Record **only** what the user explicitly states in `input.mission-input.yaml`.
- Never infer constraints from the tech stack, team size, or idea description.
- If a constraint field is not mentioned, set it to `"undefined"`.
- **Anti-pattern**: "The team uses React, so timeline must be at least 2 weeks." ❌

---

## 7. Traceability Chain

The required trace chain for every element in SSDAM is:

```
Requirement → Task → Execution → Artifact → Evaluation → Evidence → Checkpoint
```

The `mission-spec.yaml` establishes the first two links:

- Every **Requirement** (`REQ-NNN`) maps to one or more **Tasks** (`TSK-NNN`).
- Every **Task** maps to a **Checkpoint** (`CP-TSK-NNN`) and an **Artifact**.

The remaining chain links (`Execution → Artifact → Evaluation → Evidence → Checkpoint`)
are established during task execution by the `new-task` skill.

---

## 8. Recovery Strategy Selection

Choose the recovery strategy based on failure type:

| Failure Type                         | Strategy         |
|--------------------------------------|------------------|
| Transient / environmental failure    | `retry`          |
| Partial implementation failure       | `partial_fix`    |
| Task objective failure / structural  | `task_redesign`  |

**Task Redesign** conditions:
- Task objective is fundamentally unachievable with current definition.
- Structural collapse: the approach itself is invalid.
- Action: Discard current task definition. Define a new task with corrected scope.

---

## 9. Idea Validation Criteria

An idea is `INCOMPLETE` if ANY of the following are true:

- The goal cannot be stated as a single testable outcome.
- Success/failure cannot be determined without subjective judgment.
- The scope is unbounded ("build everything", "make it perfect").
- The idea references undefined external systems with no available interface.

When `INCOMPLETE`, the agent must:
1. Set `idea_validation.status: INCOMPLETE`
2. List specific `clarifying_questions` (not generic advice)
3. **Stop execution** — do not proceed to Step 2

---

## 10. Anti-Patterns

The agent must never produce output that contains any of the following:

| Anti-Pattern                                            | Why It's Prohibited                         |
|---------------------------------------------------------|---------------------------------------------|
| Task with no checkpoint                                 | Cannot determine completion                 |
| Task with no artifact                                   | Unverifiable work                           |
| Requirement not covered by any task                     | Requirement will never be satisfied         |
| `type: non_functional` requirement with no covering task | Non-functional reqs require task coverage just like functional |
| Gate criteria that use "good enough" or "looks right"   | Not binary — unenforceable                  |
| `initial_state` other than `PENDING`                    | Agent cannot pre-assign runtime states      |
| `mission_id` without checking existing IDs for sequence | Creates duplicate IDs                       |
| Constraints inferred from tech stack                    | Agent hallucination — user did not state it |
| `self_validation.passed: false` in written output       | Failed spec must never be saved             |
| Empty `task_list` in handoff                            | new-task has no work to execute             |
| `reviewers` contains only the same person as `task_owner` with no warning | Governance is unverifiable — solo-team warning is mandatory |
| `task.dependencies` entry not reflected as edge in `dependency_graph` | Creates inconsistent dependency model; new-task cannot reliably trace execution order |
