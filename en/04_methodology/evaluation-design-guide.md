# 🔍 Evaluation Design Guide — Evaluation Design Guide

## 1. Overview

This document defines the **methodology for designing Evaluation structures**
within SSDAM.

Evaluation determines whether an Artifact satisfies:

- Contract requirements  
- Quality thresholds  
- Policy constraints  
- Risk tolerance  

Poorly designed Evaluation → Non-deterministic PASS/FAIL → System instability

---

## 2. Evaluation Design Objectives

Evaluation design must ensure:

- Deterministic judgments  
- PASS / FAIL decidability  
- Evidence-generating capability  
- Agent / Human compatibility  
- Traceability preservation  

---

## 3. Step 1 — Define Evaluation Purpose

Every Evaluation must have a **clear validation objective**.

| Item | Description |
|------|-------------|
| Validation Target | What is being evaluated |
| Evaluation Scope | What is NOT evaluated |
| Decision Type | PASS / FAIL criteria |

---

### Example

✅ "Validate API contract compliance"  
❌ "Check if implementation looks good"

---

## 4. Step 2 — Select Evaluation Types

Multiple Evaluation Types may coexist.

| Type | Purpose |
|------|---------|
| Contract Validation | Format/schema compliance |
| Quality Validation | Metrics/thresholds |
| Policy Validation | Rules/compliance |
| Risk Evaluation | Risk tolerance |
| Human Review | Contextual judgment |
| Agent Evaluation | Automation checks |

---

## 5. Step 3 — Define PASS / FAIL Criteria

Evaluation must produce:

> **Binary, deterministic outcomes**

---

### Rules

- PASS / FAIL only  
- No ambiguous conditions  
- No partial PASS  
- No effort/activity-based judgment  

---

### Example

❌ "Code quality acceptable"  
✅ "Static analysis critical issues = 0"

---

## 6. Step 4 — Define Quantitative Criteria

Use measurable thresholds whenever possible.

| Criterion | Threshold | Measurement |
|----------|-----------|-------------|
| Test Pass Rate | ≥ 95% | CI Report |
| Coverage | ≥ 80% | Coverage Tool |
| Latency (P95) | ≤ 200ms | Benchmark |
| Error Rate | ≤ 0.1% | Monitoring |

---

### Rules

- Threshold explicitly defined  
- Measurement method defined  
- PASS/FAIL boundary deterministic  

---

## 7. Step 5 — Define Qualitative Criteria

When quantification is difficult, define **decision standards**.

---

### Example

```
Architecture Consistency:

- Design rationale explainable  
- Constraint alignment verifiable  
- Trade-offs documented  
```

---

### Rules

- Still PASS/FAIL decidable  
- Avoid subjective phrasing  
- Linkable to Evidence  

---

## 8. Step 6 — Evidence Design Alignment

Evaluation must be capable of generating:

> **Evidence supporting PASS / FAIL decisions**

---

### Evidence Sources

- Test reports  
- Static analysis outputs  
- Review records  
- Metrics/logs  
- Policy validation results  

---

### Rules

- Evidence mapping 1:1 with criteria  
- Evidence source identifiable  
- Timestamp recorded  

---

## 9. Step 7 — Determinism Enforcement

Evaluation must guarantee:

- Same input → Same judgment  
- Explicit criteria  
- No hidden heuristics  

---

### Handling Non-Deterministic Factors

Allowed only if explicitly defined:

- Probabilistic evaluation  
- Confidence intervals  
- Human Checkpoint escalation  

---

## 10. Step 8 — Agent / Human Compatibility

Evaluation design must define:

| Aspect | Rule |
|--------|------|
| Agent Evaluation | Requires machine-parseable criteria |
| Human Evaluation | Requires decision guidelines |
| Hybrid Evaluation | Define responsibility split |

---

### Agent Constraints

- Must emit Confidence metadata  
- Must emit Uncertainty metadata  
- Evidence-backed decisions only  

---

## 11. Evaluation Failure Conditions

Evaluation FAIL occurs when:

- Criteria unmet  
- Evidence insufficient  
- Measurement invalid  
- Policy violation  
- Risk threshold exceeded  

---

## 12. Evaluation Design Checklist

**Purpose**

- [ ] Validation objective defined  
- [ ] Scope boundaries defined  

**Criteria**

- [ ] PASS/FAIL determinable  
- [ ] Quantitative thresholds explicit  
- [ ] Qualitative standards explicit  

**Evidence**

- [ ] Evidence source defined  
- [ ] Evidence mapping clear  

**Determinism**

- [ ] Criteria deterministic  
- [ ] No ambiguous language  

**Compatibility**

- [ ] Agent-parseable (if automated)  
- [ ] Human-guided (if manual)  

---

## 13. Evaluation Design Template

```md
# Evaluation: [Evaluation Name]

## Purpose
[Validation objective]

## Scope
- Included:
- Excluded:

## Evaluation Criteria
| Type | Criterion | Threshold | Measurement |

## PASS Conditions
- [...]

## FAIL Conditions
- [...]

## Evidence Mapping
| Criterion | Evidence Source |

## Determinism Rules
- [...]

## Actor Compatibility
- Agent / Human / Hybrid
```

---

## ✅ Key Summary

Evaluation Design is:

> **Not defining opinions, but structuring deterministic validation logic.**

Well-designed Evaluation:

- Prevents arbitrary PASS/FAIL  
- Stabilizes Checkpoint decisions  
- Enables reliable Evidence  
- Preserves SSDAM determinism  
