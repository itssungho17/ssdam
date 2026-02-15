# Checkpoint Record — STG-01: Idea Definition

## Document Metadata

```yaml
project_id: PRJ-001
stage_id: STG-01
artifact_id: ART-STG-01-001
evaluation_id: EVAL-STG-01-001
evidence_id: EVD-STG-01-001
checkpoint_id: CP-STG-01
timestamp: 2026-02-15T12:30:00Z
actor: human
requirement_ids: [REQ-001]
```

---

## 1. Policy Confirmation

| policy_id | gate_type | policy_version |
|---|---|---|
| QPOL-01 | human | v0.1.0 |
| QPOL-02 | human | v0.1.0 |

---

## 2. Decision

| decision | summary |
|---|---|
| PASS | All 4 evaluation criteria met: clear single-sentence problem, specific target user, 3 core features within limit, 3 measurable success criteria. |

---

## 3. State Transition

| from_state | to_state | next_stage_id | handoff_artifact_ids | handoff_evidence_ids | recovery_id |
|---|---|---|---|---|---|
| IN_PROGRESS | COMPLETED | STG-02 | ART-STG-01-001 | EVD-STG-01-001 | NA |

---

## 4. Decision Basis Links

- evaluation_ref: EVAL-STG-01-001
- evidence_ref: EVD-STG-01-001
- decision_basis_links: [05_examples/03_execution/STG-01/evaluation-STG-01.md, 05_examples/03_execution/STG-01/evidence-STG-01.md]

---

## Self-Validation

- [x] All required criteria are judged as PASS/FAIL.
- [x] No decision was completed without evidence links.
- [x] PASS → next_stage_id (STG-02) and handoff Artifact/Evidence are specified.
- [x] No conditional pass language used (no "mostly PASS", "PASS with caveats", etc.).
