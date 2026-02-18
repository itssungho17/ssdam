# SSDAM Reference

## Framework

SSDAM (SOLID Stage-Driven Automation Mechanism):
A quality/validation/evidence-centered execution mechanism where Stage is the top-level purpose unit.

### Core Principles

1. Stage is a purpose unit, not a task unit.
2. Progress is defined by Checkpoint PASS, not by activity completion.
3. All decisions require Evidence. No evidence-free judgment is permitted.
4. Failure is a designed state transition event, not an exception.

### Stage Execution Loop

```
Execution → Artifact → Evaluation → Evidence → Checkpoint → (Next Stage | Recovery)
```

---

## Pipeline Position (stage-spec)

```
[quest-seed.yaml + quest-plan.yaml] → THIS SKILL (per stage) → [element chain]
```

- predecessor: quest-plan.template (produces quest-plan.yaml)
- successor: execution.template (element chain start)
- **Run once per stage** in quest-plan.yaml's stage_list.
  After all stage-specs are defined, begin the element chain for each stage.

---

## Handoff Contract

stage-spec의 출력 필드가 element chain 템플릿의 입력으로 매핑되는 계약:

| stage-spec 출력 필드 | → | 소비 템플릿 |
|---------------------|---|------------|
| metadata.quest_id + stage_id | → | element chain input (all) |
| output_contract[].artifact_id | → | artifact.template input |
| evaluation_criteria[] | → | evaluation.template input |
| checkpoint | → | checkpoint.template input |
| recovery_mapping[] | → | recovery.template input |
| handoff.handoff_artifacts | → | next stage input_contract |
| handoff.handoff_evidence | → | traceability records |
