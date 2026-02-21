# 🔗 Traceability — SSDAM Reference

## 1. Definition

Traceability is a structure in SSDAM that
**connects decision-making and change history without interruption
from requirements to Checkpoint**.

---

## 2. Purpose

- Enable backward traceability of decision-making basis
- Enable change impact analysis
- Enable audit/review response
- Enable Agent judgment explainability

---

## 3. Trace Chain

Basic SSDAM chain:

```
Requirement → Task → Execution → Artifact → Evaluation → Evidence → Checkpoint
```

Extended chain on FAIL occurrence:

```
Checkpoint(FAIL) → Recovery → Re-Evaluation → Evidence → Checkpoint
```

---

## 4. Required Links per Document

| Document | Required Identifiers | Required Connections |
|---|---|---|
| Task Spec | `project_id`, `task_id`, `requirement_ids` | `policy_id`, `checkpoint_id` |
| Execution | `execution_id`, `task_id` | Input contract basis, generated `artifact_id` |
| Artifact | `artifact_id`, `task_id` | `requirement_ids`, location/version/hash |
| Evaluation | `evaluation_id`, `artifact_id` | `criterion_id`, metric, result |
| Evidence | `evidence_id`, `evaluation_id` | source, measured_value, immutable information |
| Checkpoint | `checkpoint_id`, `task_id` | `evaluation_id`, `evidence_id`, `policy_id` |
| Recovery | `recovery_id`, `task_id` | source checkpoint, change target, re-evaluation result |

---

## 5. Immutable Rules

- Judgment without link is invalid.
- FAIL record deletion/overwrite is prohibited.
- ID reuse in the same chain is prohibited. (New execution cycle requires new ID)
- Reference target must be version/timestamp identifiable.
- State transition must match Checkpoint result.

---

## 6. Change Tracking Procedure

1. Identify change target Artifact (`artifact_id`)
2. Link change reason with Requirement or policy ID
3. Perform new Evaluation (`evaluation_id` new)
4. Generate/freeze new Evidence (`evidence_id` new)
5. Record new Checkpoint judgment (`checkpoint_id` reusable, judgment record is new timestamp)

Key:
- Record not "modified" but "what basis enabled re-judgment"

---

## 7. Audit Perspective Minimum Queries

- What Checkpoint determined fulfillment of specific `requirement_id`?
- What are the Evidence source and generation timestamp of that judgment?
- What Recovery strategy was selected after FAIL?
- Did repeated FAIL frequency of the same Task exceed policy threshold?

---

## 8. Quality Indicators

| Indicator | Definition | Target Example |
|---|---|---|
| Link Completeness Rate | Ratio of required ID/reference fields met | 100% |
| Evidence Connection Rate | Ratio of Checkpoints with Evidence link | 100% |
| Reproducibility Rate | Ratio of records enabling judgment reproduction | >= 95% |
| FAIL Recovery Tracking Rate | Ratio of FAIL records with Recovery connection | 100% |

---

## 9. Anti-patterns

- ❌ Documents have IDs but are not connected to each other
- ❌ Only PASS records exist, no FAIL/Recovery records
- ❌ Evidence source is unclear or lacks tampering prevention information
- ❌ Policy ID change history is not recorded

---

## 10. Checklist

- [ ] All Checkpoints reference `evaluation_id` and `evidence_id`.
- [ ] All Artifacts are connected with `requirement_ids`.
- [ ] FAIL records are connected via `recovery_id`.
- [ ] Timestamp/actor/policy version information required for audit exists.

---

## 11. Summary

Traceability is not a record but **a structure of judgment reliability**.
In SSDAM, progression is recognized only as traceable transition.
