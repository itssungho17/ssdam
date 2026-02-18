# SSDAM Reference

## Framework

SSDAM (SOLID Stage-Driven Automation Mechanism):
A quality/validation/evidence-centered execution mechanism where Stage is the top-level purpose unit.

### Core Principles

1. Stage is a purpose unit, not a task unit.
2. Progress is defined by Checkpoint PASS, not by activity completion.
3. All decisions require Evidence. No evidence-free judgment is permitted.
4. Failure is a designed state transition event, not an exception.

### Element Chain

```
execution-plan → execution → artifact → evaluation → evidence → checkpoint → (recovery)
```

---

## Pipeline Position (execution-plan)

```
stage-spec.STG-XX.yaml → THIS SKILL → execution.template (per task) → artifact → ...
```

- predecessor: stage-spec.template (produces stage-spec.STG-XX.yaml)
- successor: execution.template
- This is the **first element** in the SSDAM element chain.
- **Execution unit:** 1 task = 1 execution prompt.
  Feed each task (one at a time) together with stage-spec into execution.template.

---

## Handoff Contract

execution-plan의 출력 필드가 execution.template의 입력으로 매핑되는 계약:

| execution-plan 출력 필드 | → | 소비 템플릿 |
|-------------------------|---|------------|
| metadata (quest_id, stage_id) | → | execution.template input |
| tech_stack (backend, frontend, project_root) | → | execution.template context |
| tasks[].task_id | → | execution.template target task |
| tasks[].description + tech_context | → | execution.template instructions |
| tasks[].output_files | → | execution.template deliverables |
| tasks[].acceptance_criteria | → | execution.template completion check |
| task_flow.default_sequence | → | execution order |
