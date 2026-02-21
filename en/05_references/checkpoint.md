# 🚦 Checkpoint — SSDAM Reference

## 1. Definition

**Checkpoint** is a **PASS / FAIL judgment mechanism** performed at Task termination.

In SSDAM, Checkpoint is not simply confirming completion but:

> **"A decision point that authorizes or denies state transition"**

---

## 2. Purpose

Role of Checkpoint:

- Determine Task termination
- Verify output quality
- Confirm contract compliance
- Force evidence-based decision-making
- Control next Task progression
- Structure failure events

---

## 3. Checkpoint Location

Checkpoint is positioned at the final step of the following flow:

```
Execution → Artifact → Evaluation → Evidence → 🚦 Checkpoint
```

Conditions before Checkpoint:

✔ Output exists
✔ Evaluation completed
✔ Evidence secured

---

## 4. Decision Types

| Decision | Meaning | Result |
|------|------|------|
| **PASS** | Task objective met | Next Task progression |
| **FAIL** | Objective or contract not met | Failure record + Recovery |

---

## 5. PASS Conditions

All of the following conditions must be met:

- Defined objectives achieved
- Output contract compliance
- Evaluation criteria passed
- Required Evidence present
- Quality threshold met

PASS does not mean "work completed" but:

> **"Approval of verified state transition"**

---

## 6. FAIL Conditions

FAIL when one or more of the following apply:

- Evaluation criteria not met
- Output contract violation
- Evidence insufficient or missing
- Quality threshold not met
- Risk level exceeds tolerance

FAIL is not an exception but:

> **"Declaration of a controllable failure event"**

---

## 7. Checkpoint Components

Checkpoint consists of the following elements:

| Element | Description |
|------|------|
| **Input** | Artifact + Evaluation + Evidence |
| **Policy** | PASS / FAIL judgment rules |
| **Decision** | PASS / FAIL |
| **Output** | State transition result |
| **Trace** | Judgment justification record |

---

## 8. Policy-Governed Judgment

Checkpoint judgment must be performed by **explicit policy**.

Policy examples:

- Quality criteria (Coverage ≥ 80%)
- Performance criteria (Latency ≤ 200ms)
- Specification compliance (Schema Validation PASS)
- Review approval (Human Approval)

Checkpoint without policy is an SSDAM violation.

---

## 9. Checkpoint Types

| Type | Description |
|------|------|
| **Automated Policy Gate** | Rule-based automatic judgment |
| **Human Approval Gate** | Review/approval required |
| **Hybrid Gate** | Automated evaluation + human judgment |

---

## 10. State Transition Rules

Checkpoint controls the following state transitions:

```
IN_PROGRESS → (PASS)     → PASS
IN_PROGRESS → (FAIL)     → FAILED
FAILED      → (Recovery) → IN_PROGRESS
```

---

## 11. Traceability Requirements

Checkpoint must record:

- Judgment result (PASS / FAIL)
- Applied policy
- Evaluation summary
- Evidence links
- Judgment timestamp
- Responsible entity (Human / Agent / Policy)

---

## 12. Role in Agent Environment

When an AI Agent is involved in Checkpoint:

Required metadata:

- Confidence
- Uncertainty
- Evaluation criteria used
- Evidence source

On high-risk FAIL / increased uncertainty:

→ Human Escalation

---

## 13. Anti-Patterns

❌ PASS based on output alone
❌ Approval without Evidence
❌ Judgment without policy
❌ FAIL ignored, progression continues
❌ Evaluation skipped

---

## 14. Core Principles Summary

Checkpoint is:

> **Not a "completion confirmation point"
> but "a device authorizing verified state transitions"**

In SSDAM:

- Completion = PASS
- Failure = FAIL
- Progression = Authorized transition

---

## ✅ Conclusion

Checkpoint is SSDAM's **quality defense line**
and the core control mechanism ensuring system determinism.
