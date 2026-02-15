# Stage Specification — STG-01: Idea Definition

## Document Metadata

```yaml
project_id: PRJ-001
stage_id: STG-01
stage_name: Idea Definition
stage_owner: sungho
document_id: stage-spec
version: v0.1.0
timestamp: 2026-02-15T12:00:00Z
requirement_ids: [REQ-001]
```

---

## 1. Purpose and Scope

**Purpose**: Define the problem to solve and the project goal so that subsequent stages have a clear, validated direction.

**Scope**:
- **Included**: Problem statement, target user identification, core feature list, success criteria
- **Excluded**: Technical feasibility analysis, architecture decisions, implementation details

---

## 2. Input Contract

| Input Item | Artifact ID | Contract Requirement |
|---|---|---|
| Market/User Hypothesis | N/A (external input) | A written assumption about user need for image upload/download functionality. At minimum: who needs it and why. |

> STG-01 is the start stage. Input is an external hypothesis, not a predecessor artifact.

---

## 3. Output Contract

| Output Artifact | artifact_id | Contract Specification |
|---|---|---|
| Idea Brief | ART-STG-01-001 | Markdown document containing: (1) Problem statement in one sentence, (2) Target user description, (3) Core features (max 3), (4) Measurable success criteria (min 1). All sections must be non-empty. |

---

## 4. Evaluation Criteria

| criterion_id | Criterion | Policy Reference | Measurement Method | PASS Threshold |
|---|---|---|---|---|
| CRIT-01 | Problem statement is a single, clear sentence | QPOL-01 | Manual review: sentence count = 1, no ambiguity | Exactly 1 sentence, no vague terms |
| CRIT-02 | Target user is specifically described (who, context) | QPOL-01 | Manual review: user persona has who + usage context | Both "who" and "context" present |
| CRIT-03 | Core features are listed, maximum 3 items | QPOL-01 | Count of feature items | 1 <= count <= 3 |
| CRIT-04 | At least 1 success criterion is quantitatively measurable | QPOL-02 | Manual review: contains a numeric threshold | >= 1 measurable criterion |

---

## 5. Checkpoint Policy

```yaml
checkpoint_id: CP-STG-01
gate_type: human
evaluation_policy_references: [QPOL-01, QPOL-02]
recovery_policy_reference: RPOL-01
```

---

## 6. Next Stage Handoff

```yaml
next_stage_id: STG-02
handoff_artifacts: [ART-STG-01-001]
handoff_evidence: [EVD-STG-01-001]
```

---

## 7. Recovery Mapping

| Failure Type | RPOL Reference | Max Retry | Recovery Strategy | Escalation Trigger |
|---|---|---|---|---|
| Validation Failure (vague problem/criteria) | RPOL-01 | 3 | Correction — revise idea-brief sections that failed criteria | Retry > 3 |
| Contract Violation (missing sections) | RPOL-02 | 2 | Correction — add missing required sections | Recurrence after fix |

---

## Self-Validation

- [x] Purpose statement is single sentence and testable.
- [x] Input/output contracts are concrete and verifiable.
- [x] All evaluation criteria are PASS/FAIL-decidable (no ambiguous language).
- [x] All criteria reference policy_ids from project-policy (QPOL-01, QPOL-02).
- [x] Checkpoint gate_type is one of: automatic/human/hybrid → human.
- [x] Recovery strategies reference RPOL_ids from project-policy (RPOL-01, RPOL-02).
- [x] Next stage handoff fields are complete.
- [x] SOLID principles applied: single responsibility (idea definition only), interface segregation (minimal output contract).
