---
name: stage-spec
description: "SSDAM stage specification skill. Produces stage-spec.STG-XX.yaml defining purpose, input/output contracts, evaluation criteria, checkpoint policy, and recovery mapping for a single stage. Run once per stage. Use when: stage-level design, evaluation criteria definition, or checkpoint/recovery setup is needed."
compatibility: "Universal. Can be used with any AI agent capable of YAML output, including ChatGPT, Claude, Cursor, Codex, etc."
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# Stage Specification Design (SSDAM Stage)

## When to Use

Activate this skill when:
- quest-seed.yaml and quest-plan.yaml exist, and a stage needs to be designed
- Evaluation criteria, checkpoint policy, or recovery mapping must be defined for a stage
- The user specifies a target stage (e.g., "Design STG-01")

Pipeline position:
```
[quest-seed.yaml + quest-plan.yaml] → THIS SKILL (per stage) → [element chain]
```

**Run this skill once per stage** in quest-plan.yaml's stage_list.
After all stage-specs are defined, begin the element chain for each stage.

---

## Core Responsibility

You are a stage design agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role: produce a single stage specification defining:
1. **Purpose & Scope** — what this stage achieves (single responsibility)
2. **Input/Output Contracts** — what artifacts come in and go out
3. **Evaluation Criteria** — how to judge PASS/FAIL (quantitative, no ambiguity)
4. **Checkpoint Policy** — gate type, approver, policy references
5. **Recovery Mapping** — what to do on failure

SOLID principles apply to stage design (S/O/L/I/D).

> For SOLID details and all design rules → [references/stage-design-rules.md](references/stage-design-rules.md)
> For full framework details → [references/SSDAM.md](references/SSDAM.md)

---

## Input

Two source files + a user-specified target stage:

**Source 1: quest-seed.yaml** (from user-input skill)

| Field | Usage |
|-------|-------|
| metadata.quest_id | → quest_id |
| stages[target].id | → stage_id |
| stages[target].name | → stage_name |
| stages[target].purpose | → purpose basis |
| stages[target].key_artifact | → output contract basis |
| stages[target].mapped_requirements | → requirement_ids |
| requirements[] | → evaluation criteria derivation |
| constraints.ssdam_root | → SSDAM 산출물 저장 경로 (Output Delivery에서 사용) |

**Source 2: quest-plan.yaml** (from quest-plan skill)

| Field | Usage |
|-------|-------|
| governance.gates[target] | → checkpoint (gate_type, pass_condition, final_approver) |
| governance.escalation_rules[] | → recovery escalation context |
| stage_map.dependencies[target] | → input contract (predecessor artifact) |
| stage_map.branch_rules[target] | → handoff (on_pass → next_stage_id) |
| policies.quality_policy[] | → evaluation criteria (QPOL references) |
| policies.recovery_policy[] | → recovery mapping (RPOL references) |
| policies.traceability_policy[] | → evidence requirements |

## Output

A single YAML document: `stage-spec.STG-XX.yaml`

> Full schema → [assets/stage-spec.schema.yaml](assets/stage-spec.schema.yaml)
> Handoff contract → [references/SSDAM.md](references/SSDAM.md) § Handoff Contract

---

## Process

### Step 1 — Metadata

From quest-seed.yaml and quest-plan.yaml, extract:
- `quest_id`, `stage_id`, `stage_name`, `requirement_ids`
- `stage_owner`: use "stage_owner" role from quest-plan governance.roles
- Set `document_id: stage-spec`, `version: v0.1.0`, `timestamp` in ISO 8601

### Step 2 — Purpose and Scope

Write a single-sentence purpose statement based on quest-seed.yaml's stages[target].purpose.

Rules:
- Must be testable (can determine PASS/FAIL)
- Must describe **WHAT** this stage achieves, not **HOW**
- `scope_included`: what is covered by this stage
- `scope_excluded`: what is explicitly NOT part of this stage (boundaries)

### Step 3 — Input Contract

From quest-plan.yaml stage_map.dependencies[target]:
- If `predecessor_stage_id = "none"` → `input_item: "none"`, `artifact_id: "none"`
- Otherwise → specify the predecessor's output artifact as this stage's input
- `contract_requirement`: what the input must satisfy (structure/content conditions)

### Step 4 — Output Contract

Based on quest-seed.yaml stages[target].key_artifact:
- Define concrete artifacts this stage must produce
- artifact_id format: `ART-STG-XX-NNN` (e.g., ART-STG-01-001)
- Each artifact must have a clear `contract_specification` (format, structure, content)
- Artifacts must be reviewable and evaluable

### Step 5 — Evaluation Criteria

For each mapped requirement, define PASS/FAIL-decidable criteria:
- Reference `QPOL-XX` from quest-plan.yaml policies.quality_policy
- Each criterion must have a quantitative `pass_threshold`
- `measurement_method` must be specific (automated test, manual verification, etc.)
- criterion_id format: `CRIT-01`

**Forbidden terms:** "generally good", "adequate", "user-friendly", "appropriate"

### Step 6 — Checkpoint Policy

From quest-plan.yaml governance.gates[target]:
- `checkpoint_id`: CP-STG-XX
- `gate_id`: GATE-STG-XX (from quest-plan)
- `gate_type`: from quest-plan gates (automatic / human / hybrid)
- `final_approver`: from quest-plan gates
- `evaluation_policy_references`: list of QPOL-XX used in evaluation criteria
- `recovery_policy_reference`: primary RPOL-XX for this stage's failure type

### Step 7 — Handoff

From quest-plan.yaml stage_map.branch_rules[target]:
- `next_stage_id`: from on_pass (or `"END"` for last stage)
- `handoff_artifacts`: list of artifact_ids from output_contract
- `handoff_evidence`: `EVD-STG-XX-NNN` format

### Step 8 — Recovery Mapping

From quest-plan.yaml policies.recovery_policy:
- Map failure types relevant to this stage
- Reference `RPOL-XX`
- Strategies MUST be from: Re-execution / Correction / Re-stage / Rollback
- Define `escalation_trigger` linking to ESC rules from quest-plan

### Step 9 — Self-Validation

Verify ALL before outputting. If any fails, fix first.

- [ ] Purpose statement is single sentence and testable
- [ ] Input/output contracts are concrete and verifiable
- [ ] All evaluation criteria are PASS/FAIL-decidable (no ambiguous language)
- [ ] All criteria reference QPOL policy_ids from quest-plan
- [ ] Checkpoint gate_type matches quest-plan gates
- [ ] Recovery strategies reference RPOL_ids from quest-plan
- [ ] Handoff fields (next_stage_id, artifacts, evidence) are complete
- [ ] SOLID principles applied (single responsibility, contracts, no overlap)

---

## Output Rules

1. Output ONLY valid YAML. No markdown, no prose, no explanations outside YAML.
2. Do NOT wrap in code fences. Raw YAML directly.
3. Every key in [assets/stage-spec.schema.yaml](assets/stage-spec.schema.yaml) MUST appear. No extra keys.
4. Strings containing special characters (`: # ,` etc.) MUST be quoted.
5. Multi-line strings MUST use YAML block scalar (`>` or `|`).
6. Indentation: 2 spaces. No tabs.
7. Output MUST be parseable by PyYAML / SnakeYAML / js-yaml.
8. **NESTED QUOTE PROHIBITION:** A double-quoted string MUST NOT contain inner double quotes.
   - BAD: `escalation_trigger: "N이 "N >= 2"이면 적용"` ← parser error
   - GOOD: `escalation_trigger: "N >= 2이면 적용"` ← inner quotes removed
   - GOOD: `escalation_trigger: >-` (block scalar, then value on next line)
9. **Language rule:** All human-readable text (descriptions, scopes, criteria) MUST match the language of quest-seed.yaml content. YAML keys remain English.

**Delivery:**
- `ssdam_root`가 지정된 경우 (quest-seed.yaml constraints.ssdam_root) → `{ssdam_root}/stage-spec.STG-XX.yaml`로 저장
- `ssdam_root`가 `"undefined"`이고 파일 출력 지원 시 → `stage-spec.STG-XX.yaml`로 전달
- 파일 출력 미지원 시 → raw YAML 텍스트 직접 출력 (코드 펜스 없이)
