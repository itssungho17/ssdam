# SSDAM Agent Prompt Hub — 04_templates

## 1. Purpose
`04_templates` is a collection of **AI Agent prompts for the SSDAM framework**.
Each prompt is designed as a self-contained protocol with `<protocol>`, `<system>`, `<context>`, `<input>`, `<instructions>`, `<output_format>` structure,
guiding any AI model to autonomously generate structured YAML documents while adhering to SSDAM rules.

## 1.1 Directory Structure
```text
04_templates/
├── README.md                              ← This file (prompt hub)
├── 01_entry/                              ← Entry-level prompt
│   └── user-input.template.md             ← Decompose user idea into quest-seed.yaml
├── 02_quest/                              ← Quest-level prompt
│   └── quest-plan.template.md             ← Define governance/stage-map/policies → quest-plan.yaml
├── 03_stage/                              ← Stage-level prompts
│   └── stage-spec.template.md             ← Design single stage specification (TODO)
└── 04_elements/                           ← Execution element-level prompts (TODO)
    ├── execution.template.md
    ├── artifact.template.md
    ├── evaluation.template.md
    ├── evidence.template.md
    ├── checkpoint.template.md
    └── recovery.template.md
```

## 2. Template Chain (Execution Sequence)
Templates form a chain where each output feeds into the next:

```
[User Idea] → user-input → quest-plan → stage-spec → [element chain]
```

Detailed flow:
1. `user-input` → Decompose idea into quest-seed.yaml (quest_id, stages, requirements)
2. `quest-plan` → Define governance (roles/gates/escalation), stage map (dependencies/branches), policies (quality/recovery/traceability) → quest-plan.yaml
3. `stage-spec` → Materialize each stage's contract/evaluation/checkpoint/recovery (run once per stage)
4. During stage execution, call in order: `execution → artifact → evaluation → evidence → checkpoint`
5. On FAIL, call `recovery`

## 3. Prompt Selection Guide

| Situation | Prompt to Call |
|---|---|
| Start a new quest from a user idea | `01_entry/user-input.template.md` |
| Define quest governance, stage map, and policies | `02_quest/quest-plan.template.md` |
| Design a single stage's contract and decision rules | `03_stage/stage-spec.template.md` |
| Record execution input verification and activity history | `04_elements/execution.template.md` |
| Record artifact identification/version/hash/change information | `04_elements/artifact.template.md` |
| Record evaluation criteria/metrics/decision/risks | `04_elements/evaluation.template.md` |
| Record evaluation evidence source/measurements/immutable state | `04_elements/evidence.template.md` |
| Record policy-based PASS/FAIL decision and state transition | `04_elements/checkpoint.template.md` |
| Record recovery strategy and re-entry decision after FAIL | `04_elements/recovery.template.md` |

## 4. Prompt Common Structure
All prompts follow this structure:

```xml
<protocol>  Template identity, position in chain, input/output contracts </protocol>
<system>    Define agent role </system>
<context>   SSDAM rules/principles/constraints </context>
<input>     Attached file from previous step + field extraction instructions </input>
<instructions> Step-by-step execution procedure + self-validation checklist </instructions>
<output_format> YAML schema to follow EXACTLY </output_format>
```

Key design principles:
- Each template is **self-contained** — any AI model can execute it without prior SSDAM knowledge.
- Output is always **structured YAML** (not markdown).
- Language rule: human-readable text matches input language; YAML keys stay in English.

## 5. Minimum Completion Criteria
To declare a single stage as `COMPLETED`, at minimum the following prompts must be executed:

1. Use `stage-spec` prompt to define stage contract/evaluation/checkpoint/recovery
2. Use `execution` prompt to record execution
3. Use `artifact` prompt to record artifacts
4. Use `evaluation` prompt to record evaluation
5. Use `evidence` prompt to record evidence
6. Use `checkpoint` prompt to make PASS decision
7. On PASS, fill all next stage handoff fields (`next_stage_id`, `handoff_artifact_ids`, `handoff_evidence_ids`)

## 6. Validation Scenarios

### 6.1 Happy Path
1. Define one arbitrary stage using `stage-spec` prompt
2. Execute `execution → artifact → evaluation → evidence → checkpoint` prompts in sequence
3. Validate missing next stage handoff fields after Checkpoint PASS

### 6.2 Failure/Recovery Flow
1. Make FAIL decision in `checkpoint` prompt
2. Use `recovery` prompt to classify failure + select strategy + re-evaluate
3. Validate complete state transition records: `FAILED → IN_PROGRESS → COMPLETED`

### 6.3 Traceability Validation
1. Connect one requirement ID across `stage-spec`, `artifact`, `evaluation`, `checkpoint`
2. Verify all decision documents contain Evidence links

### 6.4 Quality Validation
1. Check all criteria in `evaluation` prompt are PASS/FAIL-decidable sentences
2. Check for absence of ambiguous language like "generally good"

## 7. Assumptions and Defaults
1. Output format is unified as YAML.
2. All prompts receive input via `<attached_file>` from the previous chain step.
3. All prompts include a **self-validation checklist** at the end.
4. Example data is managed in `05_examples`, not in `04_templates`.
5. File names/section names use SSDAM reference terminology as-is.
