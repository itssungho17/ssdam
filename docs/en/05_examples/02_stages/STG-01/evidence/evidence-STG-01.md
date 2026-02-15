# Evidence Record — STG-01: Idea Definition

## Document Metadata

```yaml
project_id: PRJ-001
stage_id: STG-01
artifact_id: ART-STG-01-001
evaluation_id: EVAL-STG-01-001
evidence_id: EVD-STG-01-001
checkpoint_id: CP-STG-01
timestamp: 2026-02-15T12:28:00Z
actor: agent
requirement_ids: [REQ-001]
```

---

## 1. Source

| source_type | source_ref | collector |
|---|---|---|
| review | 05_examples/03_execution/STG-01/idea-brief.md | agent |

---

## 2. Measured Values

| metric_name | measured_value | unit | threshold |
|---|---|---|---|
| Problem statement sentence count | 1 | sentences | = 1 |
| Target user fields present | 2 | fields (who, context) | >= 2 |
| Core feature count | 3 | items | <= 3 |
| Measurable success criteria count | 3 | criteria | >= 1 |

---

## 3. Generation Timestamp

| generated_at | collected_at | timezone |
|---|---|---|
| 2026-02-15T12:20:00Z | 2026-02-15T12:28:00Z | UTC |

---

## 4. Immutable State

| immutable | lock_method | lock_reference |
|---|---|---|
| true | hash | sha256:a51279e0a2ced16494464f487c66d7aa07856d39380a5fbc734a2324447ce122 |

---

## 5. Linked Targets

| target_type | target_id | relation |
|---|---|---|
| artifact | ART-STG-01-001 | supports |
| evaluation | EVAL-STG-01-001 | justifies |
| checkpoint | CP-STG-01 | decision_basis |

---

## Self-Validation

- [x] Source (source_type, source_ref) is clearly recorded.
- [x] Measured values with units and thresholds are recorded.
- [x] Generation/collection timestamps are in ISO 8601 format.
- [x] immutable is set to true and lock_method is specified.
- [x] Linked targets (artifact, evaluation, checkpoint) are recorded.
- [x] Correspondence with evaluation_id is specified.
