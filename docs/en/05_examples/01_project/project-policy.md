# Project Policy — Image Upload & Download Service

## Document Metadata

```yaml
project_id: PRJ-001
document_id: project-policy
version: v0.1.0
timestamp: 2026-02-15T12:00:00Z
```

---

## 1. Quality Policies (QPOL)

| policy_id | Quality Item | Threshold | Measurement Method | Judgment |
|-----------|-------------|-----------|-------------------|----------|
| QPOL-01 | Artifact completeness | All required sections present = 100% | Section checklist verification | PASS/FAIL |
| QPOL-02 | Evaluation criteria clarity | 0 ambiguous expressions (e.g., "generally good", "seems fine") | Text scan for vague language | PASS/FAIL |
| QPOL-03 | Test coverage (code stages) | >= 80% | Coverage tool measurement | PASS/FAIL |
| QPOL-04 | API response time | P95 <= 500ms | Load test measurement | PASS/FAIL |
| QPOL-05 | Security vulnerability | 0 critical/high severity issues | Security scanner | PASS/FAIL |
| QPOL-06 | Traceability link completeness | All checkpoints have evidence links = 100% | Link audit | PASS/FAIL |

---

## 2. Recovery Policies (RPOL)

| policy_id | Failure Type | Max Retry | Allowed Rollback Scope | Auto/Manual | Allowed Strategies | Escalation Condition |
|-----------|-------------|-----------|----------------------|-------------|-------------------|---------------------|
| RPOL-01 | Validation Failure | 3 | Current stage | Auto first | Re-execution, Correction | Retry > 3 |
| RPOL-02 | Contract Violation | 2 | Current stage | Manual first | Correction, Re-stage | Recurrence after fix |
| RPOL-03 | Missing Evidence | 3 | Current stage | Auto/Manual | Re-execution, Correction | Evidence re-collection failure |
| RPOL-04 | Quality Failure | 2 | Current stage | Auto first | Correction, Re-execution | Threshold repeatedly unmet |
| RPOL-05 | Logical Failure | 1 | Previous 1 stage | Manual required | Re-stage, Rollback | Immediately |
| RPOL-06 | Dependency Failure | 2 | Previous 1 stage | Manual first | Rollback, Re-execution | External dependency unrecovered |

---

## 3. Traceability Policies (TPOL)

| policy_id | Record Item | Required Links | Retention Period | Storage Location |
|-----------|------------|----------------|-----------------|-----------------|
| TPOL-01 | Requirement-Stage mapping | requirement_id → stage_id | Project lifetime | 05_examples/01_project/ |
| TPOL-02 | Execution chain record | execution → artifact → evaluation → evidence → checkpoint | Project lifetime | 05_examples/03_execution/STG-XX/ |
| TPOL-03 | Failure/Recovery record | checkpoint FAIL → recovery → re-evaluation | Project lifetime | 05_examples/03_execution/STG-XX/ |

---

## Self-Validation

- [x] All quality criteria are PASS/FAIL-decidable statements.
- [x] No ambiguous expressions ("generally good", "seems fine", etc.) exist.
- [x] Recovery max retry counts and rollback scopes are defined.
- [x] Traceability retention periods and storage locations are defined.
- [x] Policy IDs (QPOL/RPOL/TPOL) are referenceable from stage-spec and checkpoint documents.
