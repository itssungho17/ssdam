# 🛠 Stage Design Guide — Stage Design Guide

## 1. Overview

This document defines the **practical procedure for designing an SSDAM Stage from scratch**.

It assumes the immutable rules of `01_principles` and the structure of `02_architecture`,
and connects the element definitions in `07_reference` to actual design activities.

Design flow:

```
Purpose Definition → Contract Design → Evaluation Criteria → Checkpoint Policy → Recovery Strategy → Design Validation
```

---

## 2. Step 1 — Define the Purpose

Stage design begins by defining a **single Purpose**.

### 2.1 Required Entries

| Item | Description | Example |
|------|-------------|---------|
| Purpose | What this Stage aims to achieve | "Structure relationships between entities" |
| Scope | Boundary of the purpose | "Only logical models. Physical optimization is out of scope." |
| Completion Criteria | How achievement is judged | "All entity relationships are represented in an ERD." |

### 2.2 Validation Questions

- Can the purpose be explained in a single sentence?
- Does the purpose contain multiple concerns?
- Are the completion criteria verifiable?

### 2.3 Anti-Patterns

- ❌ "Implement the entire backend" → Multiple purposes, requires separation  
- ❌ "Write code and tests" → Mixed concerns  
- ✅ "Implement API endpoints" → Single purpose  

---

## 3. Step 2 — Design the Contracts

Once the purpose is defined, design the **Input Contract** and **Output Contract**.

### 3.1 Input Contract

What is required to start the Stage:

| Item | Description |
|------|-------------|
| Preceding Artifact | Required prior outputs |
| Format | Required structure/format |
| Quality Conditions | Minimum quality threshold |
| Additional Inputs | Requirements, policies, constraints |

Example:

```
Input Contract:

* requirements.md (PRD, Checkpoint PASS)
* constraints.md (Technical constraints)
```

### 3.2 Output Contract

What the Stage must produce:

| Item | Description |
|------|-------------|
| Artifact List | Outputs to generate |
| Format | Required structure/format |
| Quality Criteria | Minimum acceptable quality |
| Metadata | Version, author, timestamp |

Example:

```
Output Contract:

* schema.mmd (Mermaid ERD including all entities)
* data-dictionary.md (Field definitions, types, constraints)
```

### 3.3 Contract Design Principles

- Do not force outputs unused by downstream Stages (Interface Segregation)
- Depend on formats/structures, not implementations (Dependency Inversion)
- Include only truly necessary inputs

---

## 4. Step 3 — Establish Evaluation Criteria

Define **how Artifacts will be evaluated** before execution.

### 4.1 Select Evaluation Types

| Type | When to Use | Example |
|------|-------------|---------|
| Contract Validation | Format compliance | Schema validation |
| Quality Validation | Accuracy/consistency | Test coverage ≥ 80% |
| Policy Validation | Organizational/regulatory compliance | Security scan PASS |
| Human Review | Contextual judgment needed | Architecture decision review |
| Agent Evaluation | Suitable for automation | Static analysis |

Multiple types may be combined.

### 4.2 Define Quality Thresholds

Set quantitative PASS/FAIL boundaries.

| Criterion | Threshold | Measurement |
|----------|-----------|-------------|
| Test Pass Rate | ≥ 95% | Automated reports |
| Coverage | ≥ 80% | Coverage tools |
| Latency | ≤ 200ms (P95) | Benchmark |
| Security Issues | Critical = 0 | Security scanner |

### 4.3 Qualitative Criteria

Document decision standards when quantification is difficult.

Example:

```
Architecture Review Criteria:

* Alignment with requirements is explainable
* Expansion scenarios are identifiable
* Technical debt risks are documented
```

### 4.4 Validation Questions

- Can all criteria be judged PASS/FAIL?
- Are any criteria ambiguous or unmeasurable?
- Can Evidence support the evaluation?

---

## 5. Step 4 — Choose Checkpoint Policy

Decide **who and how PASS/FAIL is determined**.

### 5.1 Gate Types

| Type | Usage Context |
|------|---------------|
| Automated Policy Gate | Clear quantitative criteria |
| Human Approval Gate | High-risk/contextual decisions |
| Hybrid Gate | Automation + human confirmation |

### 5.2 Selection Logic

```
Quantitative only? → Automated Policy Gate
Context/strategy?  → Human Approval Gate
Both required?     → Hybrid Gate
```

### 5.3 Policy Specification

Checkpoint policy must define:

- PASS conditions  
- FAIL conditions  
- Decision authority  
- Recorded data  

---

## 6. Step 5 — Predefine Recovery Strategy

Design failure handling **before failures occur**.

### 6.1 Identify Expected Failures

| Failure Type | Example |
|-------------|---------|
| Validation Failure | Tests fail |
| Contract Violation | Output format mismatch |
| Missing Evidence | Review logs missing |
| Quality Failure | Coverage below threshold |
| Logical Failure | Design inconsistency |
| Dependency Failure | External API outage |

### 6.2 Map Recovery Strategies

| Failure Type | Strategy | Auto/Manual |
|-------------|----------|-------------|
| Validation Failure | Fix Artifact → Re-evaluate | Auto possible |
| Contract Violation | Restore contract compliance | Manual recommended |
| Missing Evidence | Supplement evidence | Auto/Manual |
| Quality Failure | Refactor → Re-run | Auto possible |
| Logical Failure | Structural redesign (Re-stage) | Manual required |
| Dependency Failure | Retry / fallback | Auto possible |

### 6.3 Escalation Conditions

Define:

- Maximum recovery attempts  
- Human intervention triggers  
- Uncertainty thresholds  

---

## 7. Step 6 — Validate the Design

Final validation checklist:

### 7.1 SSDAM Compatibility Checklist

**Purpose**

- [ ] Single purpose defined  
- [ ] Explainable in one sentence  
- [ ] Verifiable completion criteria  

**Contracts**

- [ ] Input contract defined  
- [ ] Output contract defined  
- [ ] No unnecessary IO  
- [ ] Structure-based dependencies  

**Evaluation**

- [ ] Evaluation types selected  
- [ ] Quantitative thresholds defined  
- [ ] PASS/FAIL determinable  
- [ ] Evidence-supportable  

**Checkpoint**

- [ ] Gate type selected  
- [ ] PASS/FAIL conditions defined  
- [ ] Decision authority defined  

**Recovery**

- [ ] Failure types identified  
- [ ] Recovery mapping defined  
- [ ] Escalation rules defined  

**SOLID**

- [ ] Single Responsibility  
- [ ] Open/Closed  
- [ ] Liskov Substitution  
- [ ] Interface Segregation  
- [ ] Dependency Inversion  

---

## 8. Design Template

```md
# Stage: [Stage Name]

## Purpose
[Single sentence]

## Scope
- Included: [...]
- Excluded: [...]

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
| Expected Failure | Strategy | Auto/Manual |

## Escalation
- Max Recovery Attempts:
- Human Intervention Conditions:
```

---

## 9. Practical Example

### Stage: Entity Relationship Diagram (ERD)

**Purpose:**
Structure relationships between entities derived from requirements.

**Scope:**

* Included: Logical entity modeling
* Excluded: Physical optimization

**Input Contract**

| Artifact        | Format   | Source             |
| --------------- | -------- | ------------------ |
| requirements.md | Markdown | Requirements Stage |
| constraints.md  | Markdown | Architecture Stage |

**Output Contract**

| Artifact           | Format      | Usage            |
| ------------------ | ----------- | ---------------- |
| schema.mmd         | Mermaid ERD | Data design base |
| data-dictionary.md | Markdown    | Field reference  |

**Evaluation Criteria**

| Type                | Criterion                | Threshold | Measurement       |
| ------------------- | ------------------------ | --------- | ----------------- |
| Contract Validation | All entities included    | 100%      | Cross-check       |
| Quality Validation  | Naming compliance        | 100%      | Static validation |
| Human Review        | Relationship consistency | Approval  | Design review     |

**Checkpoint Policy**

* Gate Type: Hybrid
* PASS: All validations PASS + Review approval
* FAIL: Any unmet condition
* Authority: Policy + Reviewer

**Recovery Strategy**

| Failure            | Strategy                 | Auto/Manual   |
| ------------------ | ------------------------ | ------------- |
| Missing entity     | Update ERD → Re-evaluate | Auto possible |
| Relationship error | Fix design → Re-review   | Manual        |
| Naming violation   | Auto-fix → Re-validate   | Auto          |

**Escalation**

* Max Recovery Attempts: 3
* Architect intervention after repeated FAIL

---

## ✅ Key Summary

Stage design is:

> **Not "listing tasks", but
> "structuring Purpose · Contract · Evaluation · Recovery in advance."**

Anything undefined at design time becomes confusion at execution time.
A well-designed SSDAM Stage is already verifiable before execution.
