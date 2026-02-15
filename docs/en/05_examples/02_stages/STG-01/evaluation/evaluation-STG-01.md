# Evaluation Record — STG-01: Idea Definition

## Document Metadata

```yaml
project_id: PRJ-001
stage_id: STG-01
artifact_id: ART-STG-01-001
evaluation_id: EVAL-STG-01-001
evidence_id: EVD-STG-01-001
checkpoint_id: CP-STG-01
timestamp: 2026-02-15T12:25:00Z
actor: agent
requirement_ids: [REQ-001]
```

---

## 1. Criteria-Based Judgment

| criterion_id | Criterion | Type | Threshold | Judgment |
|---|---|---|---|---|
| CRIT-01 | Problem statement is a single, clear sentence | contract | Exactly 1 sentence, no vague terms | PASS |
| CRIT-02 | Target user is specifically described (who + context) | contract | Both "who" and "context" present | PASS |
| CRIT-03 | Core features are listed, maximum 3 items | contract | 1 <= count <= 3 | PASS |
| CRIT-04 | At least 1 success criterion is quantitatively measurable | quality | >= 1 measurable criterion | PASS |

---

## 2. Measurement Metrics

| metric_id | metric_name | measured_value | threshold | measurement_method |
|---|---|---|---|---|
| M-01 | Problem statement sentence count | 1 | = 1 | Manual count of sentences in §1 |
| M-02 | Target user fields present | 2 (who + context) | >= 2 | Manual check of §2 for "Who" and "Context" sections |
| M-03 | Core feature count | 3 | <= 3 | Count of numbered items in §3 |
| M-04 | Measurable success criteria count | 3 | >= 1 | Count of criteria with numeric thresholds in §4 |

---

## 3. Overall Judgment

| result | Judgment Summary |
|---|---|
| PASS | All 4 criteria met: single-sentence problem, specific user persona, 3 core features within limit, 3 quantitative success criteria. |

---

## 4. Risk / Uncertainty Assessment

| risk_level | uncertainty | Description | escalation_needed |
|---|---|---|---|
| low | 0.15 | Problem is well-scoped for a personal/small-team tool. Low market risk for a self-hosted utility. Success criteria are measurable but real validation requires STG-02. | NO |

---

## 5. Evidence Link

- primary_evidence_id: EVD-STG-01-001
- evidence_links: [05_examples/03_execution/STG-01/idea-brief.md]

---

## Self-Validation

- [x] All criteria are judged as PASS or FAIL only (no intermediate values or vague expressions).
- [x] Overall judgment (PASS) is declared.
- [x] Agent evaluation includes uncertainty value (0.15).
- [x] Uncertainty does not exceed threshold (0.15 < 0.7) → escalation_needed: NO.
- [x] Evidence link (primary_evidence_id, evidence_links) is recorded.
- [x] No evaluation exists without evidence.
