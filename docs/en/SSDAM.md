# SSDAM (SOLID Stage-Driven Automation Mechanism)

SSDAM is a **development, design, and AI collaborative operation system** that  
**defines Stage as the top-level unit**,  
operates on an execution structure where each Stage is designed to follow **SOLID principles**,  
and structurizes and validates artifacts and evidence through the  
**Execution → Artifact → Evaluation → Evidence → Checkpoint** flow,  
thereby securing **quality, traceability, and recoverability** simultaneously.

---

## 🎯 1. Objectives

Goals of SSDAM:

- Establish Stage design based on SOLID principles  
- Build an artifact-driven development framework  
- Secure a verifiable decision-making structure  
- Transform failures into controllable events  
- Strengthen the reliability of agent-based development  

---

## 🧱 2. Core Model

SSDAM operates on the following execution model:

```
Start → Stage 1 → Stage 2 → ... → Stage N → END
```

Each Stage follows this flow:

```
Execution → Artifact → Evaluation → Evidence → Checkpoint → Next Stage / Recovery
```

---

| Element | Description |
|--------|-------------|
| **Stage** | **Top-level purpose unit designed with SOLID principles** |
| **Execution** | Activities performed within a Stage |
| **Artifact** | Reviewable output of Execution |
| **Evaluation** | Verification / judgment process applied to an Artifact |
| **Evidence** | Justification supporting the Evaluation result |
| **Checkpoint** | Pass / Fail decision gate |
| **Next Stage** | Progression target when Checkpoint passes |
| **Recovery** | Recovery actions when Checkpoint fails |

---

## 🧩 3. Stage Design Principles (SOLID)

All Stages in SSDAM adhere to the following **SOLID principles**:

| Principle | Meaning in Stage Design |
|----------|--------------------------|
| **S — Single Responsibility** | A Stage must have one clear purpose |
| **O — Open/Closed** | Stage structure should remain stable; extension allowed, modification discouraged |
| **L — Liskov Substitution** | Input / Output contracts must remain valid under Stage variations or refinements |
| **I — Interface Segregation** | Stage contracts must be defined in minimal, segregated units |
| **D — Dependency Inversion** | A Stage depends on abstractions (contracts), not concrete implementations |

---

## 🚦 4. Stage

A Stage is not a unit of work but a **unit of purpose**.  
Each Stage must define a clear objective and termination criteria,  
and must produce **verifiable artifacts**.

### ✅ Stage Definition Criteria

- Has a single purpose  
- Defines explicit Input / Output contracts  
- Produces verifiable Artifacts  
- Supports Evaluation  
- Enables Evidence-based judgment  
- Has Checkpoint termination criteria  

---

### 📥 Stage Inputs

- Artifacts from preceding Stages  
- Relevant Evidence  
- Defined Contracts (requirements / specifications / etc.)

---

### 📤 Stage Outputs

- Reviewable Artifacts  
- Evaluation Results  
- Generated Evidence  

---

### 🔄 Stage Termination

A Stage terminates via **Checkpoint Evaluation**:

- **PASS** → Proceed to Next Stage  
- **FAIL** → Record failure + Execute Recovery  

---

### 🧱 Example Stages

- Idea Definition  
- Product Requirements Document  
- Architecture Sketch  
- Entity Relationship Diagram  
- Data Definition Language  
- Backend Slice  
- Frontend Slice  
- Testing & Validation  
- Deployment Plan  
- Post-Deployment Review  

---

## 🔁 5. Failure Handling Philosophy

In SSDAM, failure is not an exception but:

> **A controllable state transition event**

Failure is declared when one or more of the following occur:

- Evaluation criteria not satisfied  
- Artifact contract violation  
- Missing mandatory Evidence  
- Quality threshold not met  
- Risk level exceeds tolerance  

Failure handling procedure:

1. Failure Classification  
2. Evidence Preservation  
3. Recovery Strategy Selection  
4. Re-execution / Re-evaluation / Re-stage  

---

## 🔗 6. Traceability Principle

SSDAM links all decisions through the following chain:

```
Requirement
→ Stage
→ Execution
→ Artifact
→ Evaluation
→ Evidence
→ Checkpoint
```

When changes occur, the traceability chain must be preserved,  
and revision history must remain uninterrupted.

**Effects:**

- Decision backtracking  
- Audit / review readiness  
- AI judgment justification  
- Failure root cause analysis  

---

## 🤖 7. Agent Compatibility

SSDAM is designed for **Human / AI Agent coexistence**.

| Role | Possible Actor |
|------|----------------|
| Execution | Human / Agent |
| Evaluation | Human / Agent |
| Checkpoint | Policy / Human |
| Recovery | Human / Agent |

Agents may perform roles,  
but ultimate responsibility belongs to the **Stage Owner**.

Humans may override agent decisions at any time.  
Escalation to humans occurs under high-risk failures or rising uncertainty.

Agent-based evaluations must include:

- Confidence metadata  
- Uncertainty metadata  

**Checkpoint Types:**

- Automated Policy Gate  
- Human Approval Gate  
- Hybrid Gate  

---

## 📐 8. Design Goals

SSDAM pursues the following characteristics:

- **Deterministic Flow**  
- **Artifact-Driven Progress**  
- **Evidence-Backed Decisions**  
- **Explicit Failure Control**  
- **Composable Stage Architecture**  
- **Traceable Decisions**  
- **Recoverable Failures**

These design goals are treated as **invariants**.

Extensions or variations violating these goals  
are not considered SSDAM-compatible.

**Deterministic Flow** refers to:

- Deterministic state transition rules  
- Deterministic Checkpoint evaluation criteria  

---

## 📚 9. References

**Overview**

- `00_overview/README.md`  
- `00_overview/quickstart.md`  

**Architecture**

- `02_architecture/stage-lifecycle.md`  
- `02_architecture/flow-architecture.md`  
- `02_architecture/stage-composition.md`  

**Methodology**

- `03_methodology/stage-design-guide.md`  
- `03_methodology/quest-planning-guide.md`  

**Specifications & Definitions**

- `06_specs/glossary.md`  
- `06_specs/id-metadata-conventions.md`  
- `07_reference/execution.md`  
- `07_reference/artifact.md`  
- `07_reference/evaluation.md`  
- `07_reference/evidence.md`  
- `07_reference/checkpoint.md`  
- `07_reference/recovery.md`  
- `07_reference/traceability.md`  

---

## ✅ 10. Summary

SSDAM is:

> **Not a "task management system,"  
> but a "quality, validation, and evidence-centered execution mechanism."**

Progress in SSDAM is defined not by activity,  
but by **verifiable state transitions**.

- **Stage** → Unit of progression  
- **Artifact** → Unit of advancement  
- **Evidence** → Unit of trust  

Completion is declared not by Artifact existence,  
but by **Checkpoint PASS**.

Failure is not an exception,  
but a **controllable system event**.

Recovery is not correction,  
but the **execution of a designed recovery strategy**.

SSDAM is designed to ensure:

- Prevention of arbitrary progress  
- Blocking of evidence-free decisions  
- Structural management of failures  
- Traceability of changes  
- Stability of Human / Agent collaboration  

Ultimately, SSDAM operates on:

> **"What has been validated"  
> rather than  
> "What has been done."**