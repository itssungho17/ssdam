---
name: quest-plan
description: "SSDAM quest planning skill. Produces quest-plan.yaml defining governance (roles, gates, escalation), stage map (dependencies, branch rules), and policies (quality, recovery, traceability) from a quest-seed.yaml. Use when: quest-level planning, governance definition, stage dependency mapping, or policy setup is needed."
compatibility: "Universal. Can be used with any AI agent capable of YAML output, including ChatGPT, Claude, Cursor, Codex, etc."
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# Quest Plan Definition (SSDAM Quest)

## When to Use

Activate this skill when:
- A quest-seed.yaml exists and quest-level planning is needed
- Governance structure (roles, gates, escalation) must be defined
- Stage dependencies and branch rules must be mapped
- Quest-wide policies (quality, recovery, traceability) must be established

Pipeline position:
```
[quest-seed.yaml] → THIS SKILL → stage-spec → [element chain]
```

---

## Core Responsibility

You are the quest planning agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role: produce a single, unified quest plan covering:
1. **Governance** — who decides what (roles, approval gates, escalation rules)
2. **Stage Map** — how stages connect (dependencies, branch rules)
3. **Policies** — what rules apply across all stages (quality, recovery, traceability)

This is the **only** quest-level planning step. Your output must be comprehensive enough
for stage-spec to begin defining individual stages without additional quest-level documents.

> For full framework details → [references/SSDAM.md](references/SSDAM.md)
> For governance axes, policy domains, immutable rules → [references/governance-and-policies.md](references/governance-and-policies.md)

---

## Input

Source: **quest-seed.yaml** (output from user-input skill)

| quest-seed.yaml Field | Usage |
|----------------------|-------|
| metadata.quest_id | → quest_id |
| metadata.quest_owner | → quest_owner |
| metadata.domain | → domain context |
| goal.statement | → quest_goal |
| stages[].id, stages[].name | → stage_list |
| stages[].purpose, stages[].key_artifact | → dependency analysis |
| stages[].mapped_requirements | → gate condition derivation |
| constraints | → risk/escalation/policy context |
| constraints.ssdam_root | → SSDAM 산출물 저장 경로 (Output Delivery에서 사용) |

## Output

A single YAML document: `quest-plan.yaml`

> Full schema → [assets/quest-plan.schema.yaml](assets/quest-plan.schema.yaml)
> Handoff contract → [references/SSDAM.md](references/SSDAM.md) § Handoff Contract

---

## Process

### Step 1 — Metadata

From quest-seed.yaml, extract:
- `quest_id`, `quest_owner`, `domain`
- Set `document_id: quest-plan`, `version: v0.1.0`, `timestamp` in ISO 8601

### Step 2 — Governance: Role Scope

Define three roles with non-overlapping boundaries:

- **quest_owner**: Finalizes quest-level policies/structure. Approves quest-level policies. Excluded from individual execution details.
- **stage_owner**: Responsible for stage contract/decision. Approves stage-level checkpoints. Excluded from changing quest-wide policies.
- **agent**: Automates execution/evaluation/recovery. Auto-decides within policy-permitted scope. Excluded from final accountability for decisions outside policy.

Role boundaries MUST NOT overlap.

### Step 3 — Governance: Approval Gates

For each stage from quest-seed.yaml, define a checkpoint gate (`GATE-STG-{number}`).

Gate type selection:
- Decidable by quantitative criteria alone → `automatic`
- Requires contextual/strategic judgment → `human`
- Automated evaluation + human confirmation → `hybrid`

### Step 4 — Governance: Escalation Rules

Define at least three escalation trigger types:
- **ESC-FAIL-N**: Consecutive failures in same stage exceeds threshold
- **ESC-UNCERTAINTY**: Agent uncertainty exceeds threshold
- **ESC-RISK**: Risk level exceeds threshold

Use constraints and risks from quest-seed.yaml to calibrate thresholds.

### Step 5 — Stage Map: Dependencies

For each stage, identify required Artifacts from predecessor stages.

**Guiding question**: "What Artifacts must exist before this stage can start?"
- Stages that don't reference each other's Artifacts → parallel candidates
- Circular dependencies found → flag as error

Dependencies must be **Artifact-based**, not activity sequence-based.

### Step 6 — Stage Map: Branch Rules

For each stage, define PASS/FAIL branch rules:
- `on_pass`: next stage_id or `END` (for last stage)
- `on_fail`: recovery path (`RCV-STG-{number}`)

Every FAIL branch MUST have a Recovery path. No dead-end failures.

Include a `flow_diagram` in Mermaid `graph TD` syntax.

### Step 7 — Policies: Quality Policy

Define quest-wide quality criteria (`QPOL-{number}`). Each item must have:
- Quantitative threshold (e.g., `>= 95%`, `= 0 instances`)
- Automated measurement method
- Binary PASS/FAIL decision (no ambiguous criteria)

### Step 8 — Policies: Recovery Policy

Define recovery rules by failure type (`RPOL-{number}`):
- Allowed strategies: Re-execution / Correction / Re-stage / Rollback
- Logical Failure → `manual` required (always)
- When retry limit exceeded → escalation path must be defined

### Step 9 — Policies: Traceability Policy

Define what must be recorded, linked, and retained (`TPOL-{number}`):
- `record_item`: what to record
- `required_link`: what it links to
- `retention_period`: how long to keep
- `storage_location`: where to store

### Step 10 — Self-Validation

Verify ALL before outputting. If any fails, fix first.

- [ ] All stages have assigned gate types and final approvers
- [ ] Escalation rules for failures / uncertainty / risk are defined
- [ ] gate_type values are one of: automatic / human / hybrid
- [ ] No role boundaries overlap
- [ ] All dependencies are Artifact-based (not activity sequence)
- [ ] No circular dependencies exist
- [ ] All FAIL branches have Recovery paths
- [ ] All quality criteria are PASS/FAIL-decidable
- [ ] No ambiguous language ("generally good", "adequate", etc.)
- [ ] Recovery max retry and rollback scope are defined
- [ ] Policy IDs (QPOL/RPOL/TPOL) are referenceable

---

## Output Rules

1. Output ONLY valid YAML. No markdown, no prose, no explanations outside YAML.
2. Do NOT wrap in code fences. Raw YAML directly.
3. Every key in [assets/quest-plan.schema.yaml](assets/quest-plan.schema.yaml) MUST appear. No extra keys.
4. Strings containing special characters (`: # ,` etc.) MUST be quoted.
5. Multi-line strings MUST use YAML block scalar (`>` or `|`).
6. Indentation: 2 spaces. No tabs.
7. Output MUST be parseable by PyYAML / SnakeYAML / js-yaml.
8. **NESTED QUOTE PROHIBITION:** A double-quoted string MUST NOT contain inner double quotes.
   - BAD: `escalation_condition: "N이 "N >= 2"이면 적용"` ← parser error
   - GOOD: `escalation_condition: "N >= 2이면 적용"` ← inner quotes removed
   - GOOD: `escalation_condition: >-` (block scalar, then value on next line)
9. **Language rule:** All human-readable text (descriptions, scopes, conditions) MUST match the language of quest-seed.yaml content. YAML keys remain English.

**Delivery:**
- `ssdam_root`가 지정된 경우 (quest-seed.yaml constraints.ssdam_root) → `{ssdam_root}/quest-plan.yaml`로 저장
- `ssdam_root`가 `"undefined"`이고 파일 출력 지원 시 → `quest-plan.yaml`로 전달
- 파일 출력 미지원 시 → raw YAML 텍스트 직접 출력 (코드 펜스 없이)
