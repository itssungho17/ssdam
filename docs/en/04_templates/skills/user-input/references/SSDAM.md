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

## Pipeline Position (user-input)

```
[User Idea] → user-input → quest-plan → stage-spec → [element chain]
```

- predecessor: none (this is the entry point)
- successor: quest-plan.template
- user-input is the only template that accepts free-form input.
  All subsequent templates receive structured YAML from their predecessor's output.

---

## Handoff Contract

user-input의 출력 필드가 quest-plan의 입력으로 매핑되는 계약:

| user-input 출력 필드 | → | quest-plan 입력 필드 |
|---------------------|---|---------------------|
| metadata.quest_id | → | quest-plan.input.quest_id |
| metadata.quest_owner | → | quest-plan.input.quest_owner |
| goal.statement | → | quest-plan.input.quest_goal |
| metadata.domain | → | quest-plan.input.domain |
| stages[].id | → | quest-plan.input.stage_list |
| requirements[].id | → | stage-spec.input.requirement_ids |
