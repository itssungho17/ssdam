# 📏 Evaluation — Artifact Verification Mechanism

## 1. Definition

**Evaluation** is a **verification act** that judges whether an **Artifact (output)**
generated in a Task meets defined **Contract**, **Quality Criteria**, and **Exit Criteria**.

In SSDAM, Evaluation is:

> **Not "review"
> but "a verifiable judgment stage"**

---

## 2. Purpose

Core purposes of Evaluation:

- Verify output validity
- Judge contract compliance
- Confirm quality threshold
- Secure PASS / FAIL judgment basis
- Justify next state transition

---

## 3. Position (Role in Execution Flow)

```
Execution → Artifact → **Evaluation** → Evidence → Checkpoint
```

Evaluation:

- Takes Artifact as input
- Generates judgment result
- Induces Evidence generation

---

## 4. Input

Evaluation inputs:

- Verification target Artifact
- Task contract / requirements
- Evaluation criteria / policies
- Quality thresholds
- Related Evidence (when necessary)

---

## 5. Output

Evaluation outputs:

- Evaluation result (PASS / FAIL)
- Evaluation report
- Generated or linked Evidence
- Quality metric (Metric Snapshot)
- Risk / Uncertainty information

---

## 6. Evaluation Types

### ✅ 6.1 Contract Evaluation

Verification targets:

- Requirement fulfillment
- Input/output contract compliance
- Interface consistency

Examples:

- API response structure match
- Schema compliance
- Required field presence

---

### ✅ 6.2 Quality Evaluation

Verification targets:

- Accuracy
- Completeness
- Consistency
- Performance
- Stability

Examples:

- Test pass rate
- Coverage
- Performance metrics
- Error rate

---

### ✅ 6.3 Policy Evaluation

Verification targets:

- Organizational rules
- Security policies
- Style guides
- Regulatory compliance

Examples:

- Code conventions
- Security vulnerabilities
- License rules

---

### ✅ 6.4 Human Review

Characteristics:

- High-risk judgment
- Strategic review
- Context-based evaluation

Application:

- Architecture decisions
- UX quality
- Business alignment

---

### ✅ 6.5 Agent Evaluation

Characteristics:

- Automatable
- Suitable for repetitive verification
- Advantageous for batch processing

Required included metadata:

- Confidence (Confidence)
- Uncertainty (Uncertainty)
- Used model / version
- Evaluation criteria ID

---

## 7. PASS / FAIL Rules

Evaluation must be judgeable.

### ✅ PASS Conditions

- Contract criteria met
- Quality threshold exceeded
- Required Evidence secured

---

### ❌ FAIL Conditions

- Contract violation
- Quality criteria not met
- Evidence insufficient
- Uncertainty threshold exceeded

---

## 8. Relationship with Evidence

Evaluation results must be justified by **Evidence**.

```
Evaluation → Evidence
```

Evidence examples:

- Test reports
- Logs
- Analysis results
- Review comments
- Measurement metrics

**Evaluation without basis is invalid**

---

## 9. Relationship with Checkpoint

Checkpoint judgment depends on Evaluation output.

```
Evaluation Result → Checkpoint Decision
```

Checkpoint:

- PASS / FAIL determination
- State transition authorization
- Recovery trigger

---

## 10. Quality Metrics (Metrics)

Evaluation may include quantitative metrics.

Examples:

| Metric | Description |
|------|------|
| Coverage | Test coverage |
| Error Rate | Error ratio |
| Latency | Response delay |
| Consistency Score | Consistency evaluation |
| Confidence | Evaluation confidence |

---

## 11. Agent Evaluation Metadata

Required items for agent-based Evaluation:

| Item | Description |
|------|------|
| Model | Model used |
| Version | Model version |
| Criteria | Evaluation criteria ID |
| Confidence | Confidence level |
| Uncertainty | Uncertainty |
| Timestamp | Evaluation timestamp |

---

## 12. Anti-Patterns

### ❌ Formal Evaluation

- Evaluation only for PASS
- No substantive verification

---

### ❌ Judgment Without Basis

- Missing Evidence
- Intuition-based judgment

---

### ❌ Ambiguous Criteria

- Unclear PASS/FAIL
- Unmeasurable

---

### ❌ Evaluation Omission

- Proceed based on Artifact existence alone
- Corrupt Checkpoint

---

## 13. Evaluation Design Principles

- Must be judgeable
- Criteria must be explicit
- Evidence connection mandatory
- Consider automation possibility
- Must be reproducible

---

## 14. Example Template

```md
## Evaluation Report

**Task:**
**Artifact:**
**Evaluator:** (Human / Agent)

### Criteria
- [ ] Contract satisfied
- [ ] Quality threshold met
- [ ] Evidence attached

### Metrics
| Metric | Value |
|--------|-------|

### Result
PASS / FAIL

### Evidence
- Link / File / Reference

### Notes
- Risks
- Observations
- Uncertainty
```

---

## ✅ Core Summary

Evaluation is:

> **Not a "confirmation stage"
> but "a verification gate authorizing or blocking state transitions"**

In SSDAM:

* Progression is determined not by Execution but by Evaluation
* Completion is declared not by Artifact but by PASS judgment
