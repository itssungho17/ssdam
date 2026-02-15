# 📎 Evidence — Definition

## 1. Concept Definition

**Evidence (basis)** is a **set of objective information that justifies and makes verifiable**
Evaluation (evaluation) results.

In SSDAM, Evidence is:

> **Not "the reason for judgment"
> but "evidence structure enabling verification and reproduction of judgment"**

---

## 2. Role

Core roles of Evidence:

- Justify evaluation results
- Ensure decision verification possibility
- Strengthen Checkpoint judgment reliability
- Connect Traceability chain
- Enable failure analysis

---

## 3. Position (Within Execution Model)

```
Execution → Artifact → Evaluation → Evidence → Checkpoint
```

Evidence is not a byproduct of Evaluation but:

> **A mandatory input element for Checkpoint judgment**

---

## 4. Evidence Required Attributes

| Attribute | Description |
|------|------|
| **Objectivity** | Verifiable information, not subjective opinion |
| **Reproducibility** | Identical judgment possible under identical conditions |
| **Traceability** | Source and generation process identifiable |
| **Immutability** | Prohibited from arbitrary modification after recording |
| **Connectivity** | Linkable with Evaluation / Artifact |

---

## 5. Evidence Types

### ✅ 5.1 Quantitative

- Test pass rate
- Performance metrics (latency, memory, throughput)
- Coverage
- Error rate
- Cost figures

**Example**
```
API response average 82ms (SLA < 100ms met)
Test pass rate 97.3%
```

---

### ✅ 5.2 Qualitative

- Review approval record
- Design review comments
- UX evaluation result
- Policy compliance judgment

**Example**
```
Architecture Review PASS
Security Policy Compliance Confirmed
```

---

### ✅ 5.3 Artifact-derived

- Build logs
- Test reports
- Static analysis results
- CI/CD results

---

### ✅ 5.4 External Verification

- Audit results
- User test results
- Operational metrics
- Regulatory compliance documents

---

## 6. Evidence Quality Criteria

Evidence is not a simple attachment.
Must satisfy the following criteria:

- Verifiable
- Clear source
- Includes timestamp
- Prevents tampering
- Directly connected to Evaluation

---

## 7. Evidence Generation Principles

### ✅ MUST

- 1:1 correspondence with Evaluation result
- Explicit measurement/judgment criteria
- Record generation timestamp
- Preserve original data
- Maintain linkable structure

---

### ❌ MUST NOT

- Vague expressions
  → "Good", "OK", "Seems fine"

- Unverifiable claims
  → "Largely stable"

- PASS declaration without basis

---

## 8. Evidence Lifecycle

```
Generation → Recording → Frozen → Reference → Audit/Analysis
```

| Phase | Description |
|------|------|
| Generation | Generated during Evaluation execution |
| Recording | Stored in system/document |
| Frozen | Change-prohibited state |
| Reference | Used in Checkpoint / Traceability / Recovery |
| Analysis | Failure cause / Quality audit |

---

## 9. Relationship with Checkpoint

Checkpoint judgment is based on:

- Artifact existence ❌
- Activity execution ❌
- **Evidence fulfillment ✅**

---

## 10. Failure and Evidence

When FAIL occurs, Evidence:

- Provides failure classification basis
- Enables cause analysis
- Justifies Recovery strategy selection
- Serves as re-evaluation criteria

---

## 11. Metadata Requirements (Agent Evaluation Included)

AI/Agent-based Evidence has additional attributes:

| Item | Description |
|------|------|
| Confidence (Confidence) | Evaluation confidence level |
| Uncertainty (Uncertainty) | Judgment uncertainty |
| Evaluation Model | Used Agent/Policy |
| Input Data Range | Evaluation target range |

---

## 12. Examples

### ✅ GOOD Evidence

```
Unit Test: 124 / 124 PASS
Coverage: 86.2%
P95 Latency: 94ms
Security Scan: No Critical Issues
Reviewer Approval: PASS
```

---

### ❌ BAD Evidence

```
Tests work well
Speed is fast
No problems
```

---

## 13. Anti-Patterns

| Anti-Pattern | Problem |
|-------------|------|
| Opinion as Evidence | Subjective judgment |
| Missing Source | Non-traceable |
| Editable Evidence | Tampering risk |
| Aggregated Without Context | Evaluation criteria unclear |
| PASS Without Evidence | SSDAM violation |

---

## 14. Practical Checklist

### ✅ Evidence Preparation Check

- [ ] Evaluation criteria clear
- [ ] Measurement values exist
- [ ] Source recorded
- [ ] Timestamp included
- [ ] Artifact connected
- [ ] Change-prohibited state

---

## ✅ Core Summary

Evidence is:

> **Not "a sentence explaining why PASS"
> but "a structure proving PASS is verifiable"**

Trust in SSDAM is:

- Activity (Activity) ❌
- Artifact existence ❌
- **Evidence (Evidence) ✅**
