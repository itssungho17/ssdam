# SSDAM Agent Prompt Hub — 04_templates

## 1. Purpose
`04_templates` is a collection of **AI Agent prompts for the SSDAM framework**.
Each prompt is designed with a `<system>`, `<context>`, `<input>`, `<instructions>`, `<output_format>` structure,
guiding agents to autonomously generate documents while adhering to SSDAM rules.

## 1.1 Directory Structure
```text
04_templates/
├── README.md                              ← This file (prompt hub)
├── 01_project/                            ← Project-level prompts
│   ├── project-governance.template.md     ← Define roles/approvals/escalations
│   ├── project-stage-map.template.md      ← Design stage sequence/dependencies/branches
│   └── project-policy.template.md         ← Define quality/recovery/traceability policies
├── 02_stage/                              ← Stage-level prompts
│   ├── stage-spec.template.md             ← Design single stage specification
│   └── stage-catalog.template.md          ← Construct stage candidate catalog
└── 03_elements/                           ← Execution element-level prompts
    ├── execution.template.md              ← Execution record
    ├── artifact.template.md               ← Artifact record
    ├── evaluation.template.md             ← Evaluation record
    ├── evidence.template.md               ← Evidence record
    ├── checkpoint.template.md             ← Checkpoint decision
    └── recovery.template.md               ← Recovery record
```

## 2. Prompt Execution Sequence
Agents call prompts in the following order:

```
01_project definition → 02_stage design → 03_elements execution records
```

Detailed flow:
1. `project-governance` → Establish role/approval system
2. `project-stage-map` → Design overall stage flow
3. `project-policy` → Define common quality/recovery/traceability rules
4. `stage-catalog` → Select stage candidates (optional)
5. `stage-spec` → Materialize each stage's contract/evaluation/checkpoint/recovery
6. During stage execution, call in order: `execution → artifact → evaluation → evidence → checkpoint`
7. On FAIL, call `recovery`

## 3. Prompt Selection Guide

| Situation | Prompt to Call |
|---|---|
| Define project responsibility/approval/escalation system | `01_project/project-governance.template.md` |
| Design overall stage sequence/dependencies/branch paths | `01_project/project-stage-map.template.md` |
| Define project-wide common rules for quality/recovery/traceability | `01_project/project-policy.template.md` |
| Design a single stage's contract and decision rules | `02_stage/stage-spec.template.md` |
| Quickly select stage candidates for early project phase | `02_stage/stage-catalog.template.md` |
| Record execution input verification and activity history | `03_elements/execution.template.md` |
| Record artifact identification/version/hash/change information | `03_elements/artifact.template.md` |
| Record evaluation criteria/metrics/decision/risks | `03_elements/evaluation.template.md` |
| Record evaluation evidence source/measurements/immutable state | `03_elements/evidence.template.md` |
| Record policy-based PASS/FAIL decision and state transition | `03_elements/checkpoint.template.md` |
| Record recovery strategy and re-entry decision after FAIL | `03_elements/recovery.template.md` |

## 4. Prompt Common Structure
All prompts follow this XML structure:

```xml
<system>    Define agent role </system>
<context>   SSDAM rules/principles/constraints </context>
<input>     Variables to pass to agent ({{variable_name}}) </input>
<instructions> Step-by-step execution procedure + self-validation checklist </instructions>
<output_format> Output format constraints </output_format>
```

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
1. Output format is unified as Markdown.
2. All prompts receive input in `{{variable}}` format.
3. All prompts include a **self-validation checklist** at the end.
4. Example data is managed in `05_examples`, not in `04_templates`.
5. File names/section names use SSDAM reference terminology as-is.
