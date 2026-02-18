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

## Pipeline Position (quest-plan)

```
[quest-seed.yaml] → THIS SKILL → stage-spec → [element chain]
```

- predecessor: user-input.template (produces quest-seed.yaml)
- successor: stage-spec.template
- This is the only quest-level planning step.
  stage-spec must be able to begin defining individual stages using only quest-seed.yaml + quest-plan.yaml.

---

## Handoff Contract

quest-plan의 출력 필드가 stage-spec 및 후속 템플릿의 입력으로 매핑되는 계약:

| quest-plan 출력 필드 | → | 소비 템플릿 |
|---------------------|---|------------|
| metadata.quest_id | → | stage-spec.input.quest_id |
| governance.roles | → | all subsequent templates (referenced) |
| governance.gates[] | → | stage-spec checkpoint policy |
| governance.escalation_rules[] | → | recovery template |
| stage_map.dependencies[] | → | stage-spec input contracts |
| stage_map.branch_rules[] | → | checkpoint PASS/FAIL routing |
| policies.quality_policy[] | → | evaluation criteria |
| policies.recovery_policy[] | → | recovery template |
