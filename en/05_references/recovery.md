# 🔧 Recovery — Recovery Mechanism

## 1. Purpose

Recovery is a **structural mechanism for restoring the system to a stable execution flow after FAIL state** in SSDAM.

Recovery goals:

- Prevent uncontrolled spread of failure
- Ensure evidence-based re-entry
- Enable re-execution without quality degradation
- Maintain state transition integrity

Recovery is not a simple correction activity but:

> **Execution of a designed failure response strategy**

---

## 2. Definition

| Element | Description |
|------|------|
| **Recovery** | Recovery activity performed after Checkpoint FAIL |
| **Recovery Trigger** | Failure condition initiating Recovery |
| **Recovery Strategy** | Recovery approach corresponding to failure type |
| **Recovery Artifact** | Output generated during recovery |
| **Recovery Evidence** | Basis justifying recovery judgment |

---

## 3. Recovery Trigger Conditions

Recovery starts when one or more of the following are met:

- Checkpoint FAIL judgment
- Evaluation criteria not met
- Contract violation
- Required Evidence missing
- Quality threshold not met

FAIL declaration is the **only entry trigger for Recovery**.

---

## 4. Recovery Design Principles

### ✅ 4.1 Maintain Determinism

Recovery is not ad hoc response but
**must be performed based on pre-defined strategy**.

Prohibited:

- Emotional correction
- Retry without basis
- Skip failure cause analysis

---

### ✅ 4.2 Separate Failure Cause

Must perform before Recovery:

1. Failure Classification
2. Root Cause Identification
3. Evidence Preservation

---

### ✅ 4.3 State Transition Integrity

Recovery does not overwrite existing flow.

Maintenance conditions:

- Preserve FAIL record
- Maintain existing Artifact
- Track change history

---

### ✅ 4.4 Evidence-Based Recovery

Recovery completion is not determined by correction but:

> **Checkpoint re-passage**

---

## 5. Failure Classification Based Strategy

| Failure Type | Description | Recovery Strategy |
|--------------|------|------------------|
| **Validation Failure** | Evaluation criteria not met | Correct and re-evaluate |
| **Contract Violation** | Input/output contract violation | Restore contract consistency |
| **Missing Evidence** | Evidence missing | Supplement Evidence |
| **Quality Failure** | Quality criteria not met | Refactor / Re-implement |
| **Logical Failure** | Design/logic error | Restructure design |
| **Dependency Failure** | External element failure | Alternative path / Retry |

---

## 6. Recovery Strategy Patterns

### 🔁 6.1 Re-execution

Conditions:

- Execution error
- Non-deterministic failure

Approach:

- Maintain identical input
- Correct environment, then re-execute

---

### 🛠 6.2 Artifact Correction

Conditions:

- Output quality problem
- Partial error

Approach:

- Minimal correction principle
- Explicitly specify change reason

---

### 🧩 6.3 Task Redesign

Conditions:

- Task objective failure
- Structural collapse

Approach:

- Discard current Task definition
- Define new Task with corrected scope and contracts

---

### 🔄 6.4 Evaluation Re-definition

Conditions:

- Evaluation criteria error
- Wrong policy

Approach:

- Correct criteria
- Track impact range

---

### 🚑 6.5 Rollback

Conditions:

- Unrecoverable
- High-risk failure

Approach:

- Return to previous Checkpoint PASS state

---

## 7. Recovery Artifacts

Recovery **must generate Artifact**.

Examples:

- Corrected design document
- Refactored code
- Supplemented tests
- Failure analysis report

---

## 8. Recovery Evidence

Required inclusions:

- Failure cause
- Execution strategy
- Change content
- Re-evaluation result

Recovery without Evidence is invalid.

---

## 9. Recovery Completion Conditions

Recovery termination is declared when following conditions are met:

- Re-evaluation PASS
- Contract fulfillment confirmed
- Quality criteria met
- Evidence verification completed

---

## 10. Anti-Patterns

| Anti-pattern | Problem |
|--------------|------|
| ❌ Unconditional retry | Conceal failure cause |
| ❌ Delete FAIL record | Collapse traceability |
| ❌ Correction without basis | Quality risk |
| ❌ Excessive redesign | Cost explosion |
| ❌ Skip evaluation | Neutralize Checkpoint |

---

## 11. Design Guidelines

### ✅ Pre-define Recovery Strategy

Each Task must specify:

- Anticipated failure types
- Response strategies
- Re-entry conditions

---

### ✅ Distinguish Automatic vs. Manual Recovery

| Type | Application Situation |
|------|------------|
| **Automatic Recovery** | Repeatable / Low-risk |
| **Manual Recovery** | High-risk / Judgment needed |
| **Hybrid** | Conditional automation |

---

### ✅ Escalation Rules

Human involvement on:

- Repeated FAIL
- Increased uncertainty
- Conflicting Evidence
- Possible policy violation

---

## 12. Example Scenarios

### 📌 Case 1 — Test FAIL

Failure Type: Quality Failure
Strategy: Artifact Correction
Actions:

1. Analyze failed test
2. Correct code
3. Re-run test
4. Confirm PASS
5. Record Evidence

---

### 📌 Case 2 — Contract Violation

Failure Type: Contract Violation
Strategy: Contract Recovery

1. Review contract definition
2. Correct input/output
3. Track affected Tasks
4. Re-evaluate

---

### 📌 Case 3 — Design Collapse

Failure Type: Logical Failure
Strategy: Task Redesign

1. Redefine Task objective
2. Restructure design
3. Generate new Artifact

---

## 13. Recovery Metrics

| Metric | Meaning |
|--------|------|
| **Recovery Rate** | Success rate of recovery vs. FAIL |
| **Mean Recovery Time (MRT)** | Average recovery time |
| **Repeat Failure Ratio** | Recurrence rate of same failure |
| **Rollback Frequency** | Frequency of rollback occurrence |

---

## ✅ 14. Checklist

- [ ] Failure cause classified
- [ ] Evidence preserved
- [ ] Strategy selection reason specified
- [ ] Artifact corrected/generated
- [ ] Re-evaluation performed
- [ ] PASS confirmed
- [ ] Recovery record saved

---

## 🔒 15. Immutable Rules

Recovery:

- Does not hide FAIL
- Does not delete records
- Does not terminate without basis
- Does not complete without evaluation

---

## 🧭 Summary

Recovery is SSDAM's **quality safeguard and flow recovery engine**.

> Not removing failure but
> maintaining system reliability and determinism after failure
> is the mechanism

In SSDAM, recovery is not optional:

> **A designed mandatory phase**
