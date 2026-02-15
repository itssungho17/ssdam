# 📘 SSDAM Glossary

## 🧱 Stage (Stage)

**Definition:**
The highest-level purposeful unit in SSDAM. Not a bundle of tasks, but a **structural unit with a clear purpose (Purpose)**.

**Core Characteristics:**

- Single Responsibility
- Clear input / output contract
- Verifiable Artifact generation
- Checkpoint-based termination

**Misconception Prevention:**

- ❌ Task bundle
- ❌ Simple phase
- ✅ Purpose-centered execution unit

---

## ⚙️ Execution (Execution)

**Definition:**
Actual activities performed within a Stage.

**Example Components:**

- Design
- Implementation
- Analysis
- Documentation
- Test execution

**Characteristics:**

- Artifact generation purpose
- Must result in evaluable state

---

## 📦 Artifact (Artifact)

**Definition:**
**Reviewable / evaluable output** resulting from Execution.

**Examples:**

- Documents (PRD, Spec, etc.)
- Code
- Diagrams
- Test reports
- Model definitions

**Required Conditions:**

- Clear format
- Re-verifiable
- Contract compliance

---

## 🔍 Evaluation (Evaluation)

**Definition:**
Process of judging whether an Artifact meets defined standards / contracts.

**Types:**

- Automated policy evaluation
- Human review
- Hybrid evaluation

**Results:**

- PASS / FAIL
- Confidence / Uncertainty metadata possible

---

## 🧾 Evidence (Evidence)

**Definition:**
**Verifiable information that justifies** Evaluation results.

**Examples:**

- Test logs
- Static analysis results
- Review records
- Measurement metrics
- Policy check results

**Role:**

- Justify decision-making
- Ensure traceability
- Enable failure analysis

---

## 🚦 Checkpoint (Checkpoint)

**Definition:**
Formal evaluation point determining Stage termination.

**Result States:**

- **PASS** → Next Stage
- **FAIL** → Recovery

**Characteristics:**

- Deterministic judgment criteria
- Policy / human / hybrid capable

---

## 🔄 Recovery (Recovery)

**Definition:**
**Designed response strategy** performed after Checkpoint FAIL.

**Example Types:**

- Re-execution
- Re-evaluation
- Stage rollback
- Remediation work
- Redesign

**Philosophy:**

- Failure = Exception ❌
- Failure = Controllable state transition event ✅

---

## 🔗 Traceability (Traceability)

**Definition:**
Structure connecting decision-making and change history in the following chain:

```
Requirement → Stage → Execution → Artifact → Evaluation → Evidence → Checkpoint
```

**Assurance Effects:**

- Backward traceability
- Audit response
- Failure root cause analysis
- AI judgment explainability

---

## 📥 Stage Input (Stage Input)

**Components:**

- Preceding Artifact
- Related Evidence
- Requirements / contract
- Policies / constraints

---

## 📤 Stage Output (Stage Output)

**Components:**

- Artifact
- Evaluation result
- Evidence
- State transition result

---

## ❌ Failure (Failure)

**Definition:**
Official state declared when one or more of the following conditions are met:

- Evaluation criteria not met
- Contract violation
- Required Evidence missing
- Quality threshold not reached
- Risk level exceeds tolerance

**Interpretation:**

- Exception ❌
- State transition event ✅

---

## ✅ PASS

**Definition:**
State where Checkpoint criteria are met.

**Meaning:**

- Stage completed
- Next Stage progression authorized

---

## ⛔ FAIL

**Definition:**
State where Checkpoint criteria are not met.

**Meaning:**

- Progression halted
- Recovery required

---

## 🤖 Agent (Agent)

**Definition:**
Automated entity capable of performing roles within SSDAM (AI / Bot / System).

**Capable Roles:**

- Execution
- Evaluation
- Recovery

**Constraints:**

- Final responsibility attributed to Stage Owner
- Confidence / Uncertainty metadata may be required

---

## 👤 Stage Owner (Stage Owner)

**Definition:**
**Final responsible entity** for the Stage.

**Responsibility Scope:**

- Contract definition
- Evaluation criteria approval
- PASS / FAIL responsibility
- Authority to redefine Agent judgment

---

## 🔄 Stage State (Stage State)

**Definition:**
State value representing the execution progress of a Stage.

**State List:**

| State | Description |
|------|------|
| **IN_PROGRESS** | Stage execution in progress |
| **COMPLETED** | Terminated with Checkpoint PASS |
| **FAILED** | Terminated with Checkpoint FAIL |

**State Transition Rules:**

```
IN_PROGRESS → (PASS) → COMPLETED
IN_PROGRESS → (FAIL) → FAILED
FAILED → (Recovery) → IN_PROGRESS
```

---

## 📐 Deterministic Flow (Deterministic Flow)

**Definition:**
Characteristic where state transitions and Checkpoint judgments are determined by **clear and reproducible rules**.

---

## 🧩 Composable Stage Architecture (Composable Stage Architecture)

**Definition:**
Architecture designed so that Stages are reusable / recombineable
based on independent contracts and interfaces.

---

## 🎯 Contract (Contract)

**Definition:**
Specification / requirements that a Stage or Artifact must fulfill.

**Components:**

- Input conditions
- Output conditions
- Quality criteria
- Evaluation criteria

---

## 📊 Quality Threshold (Quality Threshold)

**Definition:**
Minimum quality standard required for PASS judgment.

---

## 🔁 State Transition (State Transition)

**Definition:**
In SSDAM, progression is not defined as activity but as
**state change based on verification results**.

---

## 📌 Core Summary

In SSDAM:

- Stage = progression unit
- Artifact = progress unit
- Evidence = trust unit

Completion is not a deliverable but:

> **Checkpoint PASS**
