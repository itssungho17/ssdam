# 🛠 Task Design Guide — Task Design Guide

## 1. Overview

This document defines the **practical procedure for designing an SSDAM Task from scratch**.

It assumes the immutable rules of `02_core_concepts/` and the structures defined in `03_architecture/`.

Design Flow:

```
Purpose Definition → Contract Design → Evaluation Criteria → Checkpoint Policy → Recovery Strategy → Design Validation
```

---

## 2. Step 1 — Define the Purpose

Task design begins with a **single Purpose**.

### 2.1 Required Entries

| Item | Description | Example |
|------|-------------|---------|
| Purpose | What this Task aims to achieve | "Implement REST API endpoints" |
| Scope | Boundary of responsibility | "Endpoints only. Auth handled separately." |
| Completion Criteria | How success is judged | "All endpoints compiled and tested." |

### 2.2 Validation Questions

- Can the purpose be expressed in one sentence?
- Does the purpose mix multiple concerns?
- Are completion criteria objectively verifiable?

### 2.3 Anti-Patterns

❌ "Build the entire backend"  
❌ "Write code and tests and deploy"  
✅ "Implement API endpoints"

---

## 3. Step 2 — Design the Contracts

Define **Input Contract** and **Output Contract**.

### 3.1 Input Contract

What is required for Task entry:

| Item | Description |
|------|-------------|
| Required Artifacts | Upstream outputs |
| Format | Schema / structure |
| Quality Conditions | Minimum acceptable quality |
| Additional Inputs | Requirements / Policies / Constraints |

Example:

```
Input Contract:

* api-spec.yaml (Checkpoint PASS)
* constraints.md
```

---

### 3.2 Output Contract

What the Task must produce:

| Item | Description |
|------|-------------|
| Artifact List | Outputs |
| Format | Required schema/structure |
| Quality Criteria | PASS boundaries |
| Metadata | ID / Version / Timestamp |

Example:

```
Output Contract:

* compiled-service
* test-report.json
```

---

### 3.3 Contract Design Principles

- Include only necessary inputs
- Avoid forcing unused outputs downstream
- Depend on structure/format, not implementation

---

## 4. Step 3 — Establish Evaluation Criteria

Define **how Artifacts will be evaluated** before execution.

### 4.1 Evaluation Types

| Type | Usage Context |
|------|---------------|
| Contract Validation | Format/schema compliance |
| Quality Validation | Metrics/thresholds |
| Policy Validation | Rules/compliance |
| Human Review | Contextual judgment |
| Agent Evaluation | Automation-friendly checks |

---

### 4.2 Quantitative Criteria

| Criterion | Threshold | Measurement |
|----------|-----------|-------------|
| Test Pass Rate | ≥ 95% | CI report |
| Coverage | ≥ 80% | Coverage tool |
| Latency (P95) | ≤ 200ms | Benchmark |
| Critical Issues | 0 | Scanner |

---

### 4.3 Qualitative Criteria

Example:

```
Architecture Consistency:

* Design rationale explainable
* Constraint compliance verifiable
```

---

### 4.4 Validation Questions

- Are PASS/FAIL decisions deterministic?
- Are criteria measurable or assessable?
- Can Evidence support evaluation?

---

## 5. Step 4 — Define Checkpoint Policy

Specify **how PASS / FAIL is determined**.

### 5.1 Gate Types

| Type | When Used |
|------|-----------|
| Automated Policy Gate | Deterministic metrics |
| Human Approval Gate | High uncertainty/risk |
| Hybrid Gate | Both required |

---

### 5.2 Policy Must Define

- PASS conditions
- FAIL conditions
- Decision authority
- Decision records

---

## 6. Step 5 — Predefine Recovery Strategy

Design failure handling **before execution**.

### 6.1 Expected Failure Types

| Failure Type | Example |
|-------------|---------|
| Validation Failure | Tests fail |
| Contract Violation | Schema mismatch |
| Missing Evidence | Logs absent |
| Quality Failure | Threshold unmet |
| Logical Failure | Inconsistency |
| Dependency Failure | External outage |

---

### 6.2 Recovery Mapping

| Failure | Strategy |
|--------|----------|
| Validation Failure | Fix → Re-evaluate |
| Contract Violation | Correct structure |
| Missing Evidence | Supplement |
| Quality Failure | Refactor / Re-run |
| Logical Failure | Redesign |
| Dependency Failure | Retry / Fallback |

---

### 6.3 Escalation Rules

Define:

- Retry limits
- Human intervention triggers
- Uncertainty thresholds

---

## 7. Step 6 — Validate the Design

### 7.1 SSDAM Compatibility Checklist

**Purpose**

- [ ] Single purpose defined
- [ ] One-sentence clarity
- [ ] Verifiable completion criteria

**Contracts**

- [ ] Input contract defined
- [ ] Output contract defined
- [ ] No unnecessary IO
- [ ] Explicit formats

**Evaluation**

- [ ] Evaluation types defined
- [ ] Thresholds defined
- [ ] PASS/FAIL determinable
- [ ] Evidence-supportable

**Checkpoint**

- [ ] Gate type selected
- [ ] PASS/FAIL conditions defined
- [ ] Decision authority defined

**Recovery**

- [ ] Failure types identified
- [ ] Recovery strategies mapped
- [ ] Escalation rules defined

---

## 8. Task Design Template

```md
# Task: [Task Name]

## Purpose
[Single sentence]

## Scope
- Included:
- Excluded:

## Input Contract
| Artifact | Format | Source |

## Output Contract
| Artifact | Format | Usage |

## Evaluation Criteria
| Type | Criterion | Threshold | Measurement |

## Checkpoint Policy
- Gate Type:
- PASS Conditions:
- FAIL Conditions:
- Decision Authority:

## Recovery Strategy
| Expected Failure | Strategy |

## Escalation
- Retry Limits:
- Human Intervention Conditions:
```

---

## 9. Practical Example

### Task: REST API Endpoint Implementation

**Purpose:**  
Implement defined REST endpoints based on API specification.

**Scope:**

- Included: Endpoint logic
- Excluded: Deployment / Infra

**Input Contract:**

| Artifact | Format |
|----------|--------|
| api-spec.yaml | YAML |
| schema.mmd | Mermaid |

**Output Contract:**

| Artifact | Format |
|----------|--------|
| compiled-service | Binary |
| test-report.json | JSON |

**Evaluation Criteria:**

| Type | Criterion | Threshold |
|------|----------|-----------|
| Contract Validation | API compliance | 100% |
| Quality Validation | Tests PASS | ≥ 95% |
| Agent Evaluation | Static analysis | PASS |

**Checkpoint Policy:**

- Gate Type: Automated / Hybrid
- PASS: All validations PASS
- FAIL: Any unmet criterion

**Recovery Strategy:**

| Failure | Strategy |
|---------|----------|
| Test FAIL | Fix → Re-run |
| Contract violation | Correct → Re-validate |

---

## ✅ Key Summary

Task design is:

> **Not “listing activities”, but  
> “structuring Purpose · Contract · Evaluation · Recovery in advance.”**

Undefined design → Non-deterministic execution → Traceability breakdown.
