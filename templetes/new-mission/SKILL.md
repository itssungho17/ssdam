---
name: new-mission
description: Entry point of the SSDAM pipeline. Transforms a user's raw idea into a fully structured `mission-spec.yaml`. Its output is the direct input for the `new-task` skill.
compatibility: Universal. Can be used with any AI agent capable of YAML output, including ChatGPT, Claude, Cursor, Codex, etc.
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

## File Paths Reference

### Skill Definition Files (read-only)

| File | Path | Purpose |
|------|------|---------|
| This file | `templetes/new-mission/SKILL.md` | Skill definition and execution procedure |
| Input schema | `templetes/new-mission/references/input.template.yaml` | Reference schema for agent-generated input |
| Output template | `templetes/new-mission/references/output.template.yaml` | Structure of the generated output |
| Rules | `templetes/new-mission/references/rules.md` | ID conventions, immutable rules, anti-patterns |
| Setup script | `templetes/new-mission/scripts/init.py` | Creates workspace folder structure (agent runs this) |

### Runtime Files (created per mission)

| File | Path | Who creates it |
|------|------|----------------|
| Input | `.ssdam/{id}/input/mission-input.yaml` | **This agent** (generated from user command) |
| Output | `.ssdam/{id}/output/mission-spec.yaml` | **This agent** |

> `{id}` is derived from the user's command text (sanitized slug).
> The agent creates all folders and files automatically — the user writes nothing manually.

### Skill Chain

```
[User]: /new-mission [idea or feature list]
        ↓
[new-mission AgentSkill]  ← YOU ARE HERE
  Phase 0 : Parse command → detect project context → generate mission-input.yaml
  Phase 1–7: Analyze → Design → Validate
        ↓
[.ssdam/{id}/output/mission-spec.yaml]
        ↓
[new-task AgentSkill]  (reads mission-spec.yaml as its input)
```

---

## Overview

| | |
|---|---|
| **Trigger** | `/new-mission [idea or feature list]` |
| **Input** | User command text + auto-detected project context |
| **Work** | Generate input → Analyze → Design Mission-Spec (Phase 0 + 15 steps) |
| **Output** | `.ssdam/{id}/output/mission-spec.yaml` |
| **Next skill** | `new-task` |

The agent receives the user's command directly, auto-detects the project
context from the file system, generates `mission-input.yaml`, then produces a
`mission-spec.yaml` that fully defines: the mission goal, requirements, task
breakdown, governance, dependency map, and quality/recovery/traceability policies.

---

## Input

**Trigger:** `/new-mission [idea or feature list]`

Everything after `/new-mission` is treated as the raw `idea`. The user does not
write or edit any YAML file. The agent generates `mission-input.yaml` in Phase 0.

**What the user provides via command:**

- `idea` — The text after `/new-mission` (free-form, feature list, natural language)

**What the agent auto-detects from the project:**

- `project_root` — Current working directory
- `ssdam_root` — `{project_root}/.ssdam`
- `backend_stack` — From `assets/package.json`
- `frontend_stack` — From `assets/package.json` (react, vue, angular, next, nuxt, etc.)
- `database` — From `assets/package.json`
- `mission_owner` — From `assets/package.json` or `git config user.name` (fallback: ask user)

**What the agent asks the user (minimal, only if not detectable):**

- `mission_owner` — If git config is unavailable
- `team` — "Who is on the team? (name:role pairs, or press Enter to skip)"
- `constraints` — "Any hard constraints? (timeline, budget, etc. — or press Enter to skip)"

**Generated file:** `.ssdam/{id}/input/mission-input.yaml`
**Schema reference:** `templetes/new-mission/references/input.template.yaml`

---

## Work

The agent executes Phase 0 (input generation) followed by 15 steps across 7 phases.
Read `references/rules.md` before starting — all IDs, state rules, and
anti-patterns apply throughout.

---

### PHASE 0 — Input Generation

> Triggered by: `/new-mission [idea text]`
> Goal: Collect all necessary input, create the workspace, and write `mission-input.yaml`.

#### Step 0-1: Parse Command

Extract the raw idea from the user command:
- Everything after `/new-mission` is the `idea`.
- If nothing follows `/new-mission` → ask: `"What would you like to build or accomplish?"`
- Do not interpret or restructure the idea yet — store it verbatim.

#### Step 0-2: Auto-Detect Project Context

Scan the project root (current working directory) to detect:

| Field | Detection method |
|-------|-----------------|
| `project_root` | Current working directory |
| `ssdam_root` | `{project_root}/.ssdam` |
| `backend_stack` | Check `assets/package.json` (backend_stack field) |
| `frontend_stack` | Check `assets/package.json` (frontend_stack field) |
| `database` | Check `assets/package.json` (database field) |
| `mission_owner` | Check `assets/package.json` (mission_owner field) or run `git config user.name`; use result if non-empty |

If a field cannot be detected, set it to `"undefined"` — do not guess.

#### Step 0-3: Collect Missing Info (Minimal Prompts)

Ask the user only for what could not be auto-detected:

- If `mission_owner` is still `"undefined"`:
  → Ask: `"Who is the mission owner? (name or role)"`

- Ask once:
  → `"Team members? Format: name:role, name:role — or press Enter to skip"`
  → Parse comma-separated pairs. If skipped, set `team: []`.

- Ask once:
  → `"Any hard constraints? (e.g., '2 weeks', 'GDPR required') — or press Enter to skip"`
  → If skipped, all `constraints` fields default to `"undefined"`.

**Never ask more than 3 questions in Phase 0.**
If a field is ambiguous but not critical, use `"undefined"` and continue.

#### Step 0-4: Create Workspace

Generate the workspace ID from the idea text:
- Take the first 3–5 significant words from `idea`
- Lowercase, replace spaces/special chars with `-`
- Append today's date: `{slug}-YYYYMMDD-NNN`
- NNN = next available 3-digit sequence for today
- Check `.ssdam/` for existing `{slug}-YYYYMMDD-*` folders to determine NNN
- Start at `001` if none exist for today
- Example: `user-auth-api-20260221-001`

Check for ID collision:
- If `.ssdam/{id}/` already exists → append `-2`, `-3`, etc.

Create directories:
```
{project_root}/.ssdam/{id}/input/
{project_root}/.ssdam/{id}/output/
```

#### Step 0-5: Generate mission-input.yaml

Write `.ssdam/{id}/input/mission-input.yaml` using all collected data.
Use `templetes/new-mission/references/input.template.yaml` as the schema reference.

Show the generated file to the user:
```
📋 Generated mission-input.yaml:
---
idea: |
  <verbatim idea text>
mission_owner: <detected or provided>
project_context:
  backend_stack: <detected>
  ...
```

Then ask:
> `"Does this look right? Type 'yes' to proceed, or tell me what to change."`

- If user confirms (`yes`, `ok`, `proceed`, `go`, `y`) → continue to PRE-EXECUTION.
- If user requests changes → apply the changes to `mission-input.yaml`, show the diff, ask again.
- Maximum 2 revision rounds. After 2 rounds, proceed regardless.

---

### PRE-EXECUTION

After Phase 0 completes, load all required references before Step 1:

**P-1. Read mission-input.yaml**
Parse the generated `.ssdam/{id}/input/mission-input.yaml` completely.
Validate that `idea`, `mission_owner`, `project_context.project_root`,
and `project_context.ssdam_root` are present and non-empty.

**P-2. Read rules.md**
Load `templetes/new-mission/references/rules.md`.
All ID formats, state rules, and anti-patterns in that file apply to every
step below.

**P-3. Read output.template.yaml**
Load `templetes/new-mission/references/output.template.yaml`.
The final output must conform to this structure.

**P-4. Confirm output directory**
Check that `.ssdam/{id}/output/` exists (created in Step 0-4).
If not, create it silently and continue.

---

### PHASE 1 — Idea Intake

#### Step 1: Idea Validation

Evaluate the `idea` field from the input file against these criteria:

- Can the goal be stated as a single testable outcome?
- Can success/failure be determined without subjective judgment?
- Is the scope bounded (not "build everything" or "improve it")?
- Does it reference only systems that are accessible or describable?

**If INCOMPLETE** (any criterion fails):
1. Set `idea_validation.status: INCOMPLETE`
2. Write specific `clarifying_questions` — each question must be answerable
   by the user with a concrete addition to the `idea` field.
3. Write partial output to `.ssdam/{id}/output/mission-spec.yaml`
   containing only the `metadata` (partial) and `idea_validation` blocks.
4. **STOP.** Do not proceed to Step 2.
   Print: `Idea incomplete. See clarifying_questions in output file.`

**If COMPLETE**:
1. Set `idea_validation.status: COMPLETE`
2. Proceed to Step 2.

#### Step 2: Mission Metadata

Generate the mission's identifying metadata:

- `mission_id`: Format `MIS-YYYYMMDD-NNN`
  - Date = today in UTC (YYYYMMDD)
  - NNN = next available 3-digit sequence for today
  - Check `.ssdam/` for existing `MIS-YYYYMMDD-*` folders to determine NNN
  - Start at `001` if none exist for today
- `created_at`: ISO-8601 UTC timestamp (e.g., `2026-02-21T09:00:00Z`)
- `domain`: Infer from idea + stack:
  `backend` | `frontend` | `data` | `infra` | `fullstack` | `mobile` | `other`
- `schema_version`: `"1.0.0"`
- `mission_owner`: Copy from `input.mission_owner`

---

### PHASE 2 — Goal & Requirements

#### Step 3: Goal Structuring

Write a single `goal.statement` that:
- Is one sentence
- Ends in a specific, testable outcome
- Does not use vague language ("improve", "enhance", "make better")

Then define `success_criteria` (minimum 2, format `SC-NNN`):
- Each criterion must be binary PASS/FAIL verifiable
- Each criterion must be directly derivable from the goal statement

**Reject** vague statements. Rewrite them:
- ❌ "Improve the authentication system"
- ✅ "Implement JWT-based authentication with login, token refresh, and logout
      endpoints, all returning correct HTTP status codes under load"

#### Step 4: Requirements Extraction

Extract requirements from the goal and idea. Rules:
- Minimum 3 requirements
- Format: `REQ-NNN`
- Every requirement must be PASS/FAIL verifiable
- Include both functional and non-functional requirements
- Every requirement must be traceable to at least one task (enforced in Step 5)

For each requirement, set:
- `statement`: Specific, testable condition
- `type`: `functional` or `non_functional`
- `verifiable`: `true` (if not verifiable, rewrite the requirement)

---

### PHASE 3 — Task Decomposition

#### Step 5: Task Definition

Decompose the mission into Tasks. Rules:
- Minimum 2 tasks
- Format: `TSK-NNN`
- Each task must have a single, clear `purpose` (one sentence, testable)
- Each task must cover at least one requirement (`requirements` field)
- All requirements must be covered across all tasks
- Initial state is always `PENDING`

For each task, define:
- `checkpoint.id`: `CP-TSK-NNN` (matching task number)
- `checkpoint.criteria`: Exact binary PASS/FAIL condition
- `artifact.description`: What concrete output the task produces
  (file, API endpoint, migration, test suite, etc.)

#### Step 6: Dependency Mapping

For each task pair, determine the relationship type:
- `sequential`: Task B cannot start until Task A completes (`PASS`)
- `parallel`: Tasks can run simultaneously (no dependency)
- `conditional`: Task B starts only if Task A result meets a stated condition

Build `task_map.dependency_graph` as a list of `{from, to, type}` entries.
Then identify `task_map.critical_path`: the longest sequential chain through
all tasks. List task IDs in execution order.

---

### PHASE 4 — Governance

#### Step 7: Role Assignment

From `input.team`, assign:
- `governance.roles.mission_owner`: Copy from `input.mission_owner`
- `governance.roles.task_owners`: Map each `TSK-NNN` to a team member
  - Prefer assigning by role match (developer → implementation tasks, qa → test tasks)
  - Every task must have an owner
- `governance.roles.reviewers`: List of team members who review artifacts
  - Must include at least one person other than the task owner

#### Step 8: Gate Definition

For every task, define a Gate:
- `id`: `GATE-TSK-NNN` (matching task number)
- `task_id`: the corresponding `TSK-NNN`
- `criteria`: Binary pass criteria — what must be true for the gate to open

Gate criteria must be concrete and machine-evaluable where possible:
- ✅ "All unit tests pass with coverage ≥ 80%"
- ✅ "API returns HTTP 200 for all defined endpoints in the test suite"
- ❌ "Code looks good to the reviewer"

#### Step 9: Escalation Rules

Define three escalation parameters:
- `repeated_failure_threshold`: Integer — after N consecutive FAILs on a task,
  escalate to `escalation_target`
- `blocked_duration_threshold`: Time string — after a task is `BLOCKED` for
  this duration, escalate (e.g., `"24h"`, `"3 days"`)
- `escalation_target`: A name or role from `governance.roles.reviewers`
  or `governance.roles.mission_owner`

---

### PHASE 5 — Policies

#### Step 10: Quality Policy (QPOL-01)

Define the quality rules that apply to all tasks in this mission:
- What artifacts are mandatory per task
- Minimum quality bar (e.g., test coverage threshold, linting rules)
- Defect severity classification used in evaluations

Assign `id: "QPOL-01"`.

#### Step 11: Recovery Policy (RPOL-01)

Map failure conditions to recovery strategies. Use the decision table from
`references/rules.md` Section 8.

For each strategy entry, define:
- `condition`: What failure scenario triggers this strategy
- `action`: `retry` | `partial_fix` | `task_redesign`
- `max_attempts`: How many times this strategy may be applied

At minimum, define three entries:
1. First FAIL → `retry`
2. Second consecutive FAIL → `partial_fix`
3. Third consecutive FAIL or structural collapse → `task_redesign`

Assign `id: "RPOL-01"`.

#### Step 12: Traceability Policy (TPOL-01)

Set `required_chain` to:
```
Requirement → Task → Execution → Artifact → Evaluation → Evidence → Checkpoint
```

Define rules:
- Every artifact must reference its source `task_id` and `requirement_ids`
- Every checkpoint must reference its `evaluation_id`
- No task may be marked `PASS` without a recorded checkpoint

Assign `id: "TPOL-01"`.

---

### PHASE 6 — Constraints & Handoff

#### Step 13: Project Context & Constraints

**Project Context (propagate from mission-input.yaml)**

Copy `project_context` fields verbatim from `input.project_context` into
`mission-spec.project_context`. If a field was not auto-detected, it remains
`"undefined"` — do NOT infer or substitute values.

```yaml
project_context:
  backend_stack:  <input.project_context.backend_stack>   # e.g., "Python/FastAPI"
  frontend_stack: <input.project_context.frontend_stack>  # e.g., "React/Next.js"
  database:       <input.project_context.database>        # e.g., "PostgreSQL"
  project_root:   <input.project_context.project_root>    # e.g., "/Users/dev/my-project"
```

This block is the **authoritative tech stack source** consumed by the `new-task`
skill. If all five fields are `"undefined"`, `new-task` will prompt the user to
provide them before generating the execution plan.

**Constraints (propagate from mission-input.yaml)**

Copy constraints verbatim from `input.constraints`. Do not infer or add any
constraint not explicitly stated. For any field not mentioned in the input,
set the value to `"undefined"`.

**Anti-pattern to avoid:**
> The input lists `backend_stack: Python/FastAPI` → agent writes
> `performance: "FastAPI handles 1000 req/s"` ❌
> (This is inference, not user input.)

#### Step 14: Handoff

Prepare the handoff block that tells the next skill what to do:

```yaml
handoff:
  next_template: "new-task"
  payload:
    mission_id: "<generated mission_id>"
    task_list:  [<TSK-NNN in dependency order>]
    requirement_ids: [<all REQ-NNN IDs>]
  instruction: >
    Execute the new-task skill for each task in task_list, in dependency order.
    Read .ssdam/{id}/output/mission-spec.yaml as the input source.
    Create a separate Task-Spec for each TSK-NNN.
```

`task_list` must be ordered so that all dependencies of a task appear
before that task in the list.

---

### PHASE 7 — Self-Validation

#### Step 15: Validation Checklist

Before writing output, verify every item below. If any item fails, fix it
and re-verify. **Never write output with a failed check.**

**IDs**
- [ ] `mission_id` matches `^MIS-[0-9]{8}-[0-9]{3}$`
- [ ] All tasks use `TSK-NNN` format
- [ ] All requirements use `REQ-NNN` format
- [ ] All success criteria use `SC-NNN` format
- [ ] All checkpoints use `CP-TSK-NNN` format
- [ ] All gates use `GATE-TSK-NNN` format
- [ ] Policies use `QPOL-01`, `RPOL-01`, `TPOL-01`
- [ ] `created_at` is ISO-8601 UTC

**Coverage**
- [ ] Every `REQ-NNN` is referenced by at least one task's `requirements` field.
  **Verification method**: iterate the full `requirements` list; for each REQ-NNN,
  confirm it appears in at least one task's `requirements` array.
  This applies to **all types** — `type: non_functional` is NOT exempt.
  If a non-functional requirement (latency, security, etc.) has no covering task,
  either assign it to an existing task or create a dedicated verification task.
- [ ] Every task references at least one requirement
- [ ] Every task has exactly one checkpoint with binary criteria
- [ ] Every task has an artifact description
- [ ] Every task has exactly one gate
- [ ] `task_list` in handoff covers all TSK-NNN IDs
- [ ] `requirement_ids` in handoff covers all REQ-NNN IDs

**Dependency Graph Completeness**
- [ ] For every task B, every ID in `B.dependencies` has a corresponding
  `{from: A, to: B}` edge in `task_map.dependency_graph`.
  **Verification method**: for each task, iterate `dependencies`; confirm
  each entry exists as a `from` value in an edge where `to` equals this task.
  Transitive reachability does NOT satisfy this check — direct edges are required.

**Project Context**
- [ ] `project_context` section exists in output
- [ ] All five fields present: `backend_stack`, `frontend_stack`, `database`, `project_root`
- [ ] All values copied verbatim from `mission-input.yaml` — no inference
- [ ] If all five values are `"undefined"`, add a soft warning to `self_validation.failed_checks`:
  `"WARNING: All project_context fields are undefined. new-task will prompt the user for tech stack info."`

**State**
- [ ] All tasks have `initial_state: PENDING`
- [ ] No task has any state other than `PENDING`

**Governance**
- [ ] `mission_owner` is defined and non-empty
- [ ] Every task has an assigned owner in `task_owners`
- [ ] If `team` is non-empty: `reviewers` contains at least one person
  who is NOT listed as a `task_owner` for any task
- [ ] If `team` is empty or all members share `mission_owner`'s identity:
  `reviewers` is `["TBD"]`, `escalation_target` is `"TBD"`,
  and `self_validation.failed_checks` contains the solo-team warning
  (see `references/rules.md` Section 5)
- [ ] `escalation_target` is defined (may be `"TBD"` for empty-team case)
- [ ] `repeated_failure_threshold` is a positive integer
- [ ] `blocked_duration_threshold` is a time string

**Handoff**
- [ ] `next_template` is `"new-task"`
- [ ] `task_list` is in valid dependency order
  (no task appears before its dependencies)

Set `self_validation.passed: true` if all hard checks pass.
The solo-team governance warning is a **soft warning** — it goes into
`failed_checks` but does NOT set `passed: false`.
All other failures must be fixed before writing output.
`self_validation.passed: false` must **never** be written to disk.

---

### POST-EXECUTION

After all 15 steps complete and self-validation passes:

1. **Write output file** to `.ssdam/{id}/output/mission-spec.yaml`.
2. **Confirm the file was written** — read it back and verify it is non-empty
   and parseable YAML.
3. **Print completion summary**:

```
✅ Mission-Spec generated successfully.

   mission_id : MIS-YYYYMMDD-NNN
   domain     : <domain>
   Tasks      : TSK-001, TSK-002, ...
   Output     : .ssdam/{id}/output/mission-spec.yaml

   Next step  : Run the new-task AgentSkill.
                It will read the output above as its input.
```

---

## Error Handling

| Condition | Action |
|-----------|--------|
| `/new-mission` with no text | Ask: `"What would you like to build or accomplish?"` |
| Project context undetectable | Set field to `"undefined"`. Never guess. Continue. |
| `git config user.name` unavailable | Ask user for `mission_owner`. |
| Workspace ID collision | Append `-2`, `-3` suffix until unique. |
| User requests >2 revisions in Step 0-5 | Apply last revision and proceed regardless. |
| `idea` fails validation (Step 1) | Stop. Write partial output with `clarifying_questions`. Ask user to re-run `/new-mission`. |
| Requirement not coverable by any task | Flag to user. Ask to reduce scope or add a task. |
| Output directory missing | Create it silently. Continue. |
| Self-validation fails | Fix all failures inline. Re-verify. Never write a failed spec. |
| Output file unwritable (permissions) | Stop. Print the error. Do not silently fail. |

---

## Output

**File:** `.ssdam/{id}/output/mission-spec.yaml`
**Template:** `templetes/new-mission/references/output.template.yaml`

The output file contains the complete `mission-spec.yaml` with all sections
populated:

- `metadata` — Mission ID, owner, domain, timestamp
- `idea_validation` — Validation result
- `goal` — Structured goal statement + success criteria
- `requirements` — REQ-NNN entries, all verifiable
- `tasks` — TSK-NNN entries with checkpoints and artifacts
- `governance` — Roles, gates, escalation rules
- `task_map` — Dependency graph + critical path
- `policies` — QPOL-01, RPOL-01, TPOL-01
- `constraints` — Copied verbatim from input
- `handoff` — Pointer to `new-task` with payload
- `self_validation` — Checklist result (always `passed: true` in written output)

This file becomes the **input** for the `new-task` AgentSkill.
