# Project Governance — Image Upload & Download Service

## Document Metadata

```yaml
project_id: PRJ-001
document_id: project-governance
version: v0.1.0
owner: sungho
timestamp: 2026-02-15T12:00:00Z
```

---

## 1. Role Definitions

| Role | Responsibility | Approval Scope | Exclusion |
|------|---------------|----------------|-----------|
| project_owner (sungho) | Project-level policy and structure decisions | Project-level policy approval, stage-map changes | Individual execution implementation details |
| stage_owner (sungho) | Stage contract definition and checkpoint judgment | Stage-level PASS/FAIL approval | Project-wide policy changes |
| agent (AI assistant) | Execution, evaluation, and recovery automation | Automatic judgment within policy-allowed scope | Final responsibility decisions outside policy |

---

## 2. Approval Authority Matrix

| gate_id | Target | gate_type | PASS Condition | Final Approver |
|---------|--------|-----------|----------------|----------------|
| GATE-01 | STG-01 Idea Definition | human | Problem and goal clearly defined | project_owner |
| GATE-02 | STG-02 Problem Validation | human | Problem priority and feasibility verified | project_owner |
| GATE-03 | STG-03 Requirements Definition | human | Functional/non-functional requirements structured | stage_owner |
| GATE-04 | STG-04 Architecture Sketch | hybrid | Architecture constraints satisfied + owner review | stage_owner |
| GATE-05 | STG-05 Data Model Design | hybrid | Schema validation PASS + owner review | stage_owner |
| GATE-06 | STG-06 Backend Implementation | automatic | All tests pass, coverage >= 80% | policy |
| GATE-07 | STG-07 Frontend Implementation | automatic | All tests pass, accessibility checks pass | policy |
| GATE-08 | STG-08 Integration Testing | automatic | Integration test pass rate >= 95% | policy |
| GATE-09 | STG-09 Deployment/Release | hybrid | Deployment verification + owner approval | stage_owner |
| GATE-10 | STG-10 Post-Deploy Review | human | Retrospective completed with action items | project_owner |

---

## 3. Escalation Rules

| rule_id | Trigger Condition | Threshold | Escalation Target | Action |
|---------|-------------------|-----------|-------------------|--------|
| ESC-FAIL-N | Consecutive failures on the same stage | N >= 2 | project_owner | Pause stage, review root cause, decide re-stage or rollback |
| ESC-UNCERTAINTY | Uncertainty threshold exceeded | uncertainty > 0.7 | stage_owner | Human review of agent evaluation result |
| ESC-RISK | Risk level threshold exceeded | risk_level >= high | project_owner | Full project risk assessment and mitigation planning |

---

## Self-Validation

- [x] All stages have an assigned owner.
- [x] All checkpoints have a gate type and final approver.
- [x] Escalation rules for failure count, uncertainty, and risk are defined.
- [x] Default escalation thresholds are defined (N=2, uncertainty=0.7, risk=high).
- [x] gate_type values are one of: automatic / human / hybrid.
