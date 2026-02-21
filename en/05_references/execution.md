# ⚙️ Execution — SSDAM Reference

## 1. Definition

**Execution** is a **concrete work activity (Activity Set)**
performed within a Task to achieve its purpose.

Execution is not a simple task list but:

> **"A set of intentional acts for generating output"**

---

## 2. Role

Core roles of Execution:

- Realize Task objective
- Generate verifiable Artifact
- Provide Evaluation target
- Ensure observability of changes and failures

Execution itself does not imply completion state.
Completion is declared only by **Checkpoint PASS**.

---

## 3. Execution Responsibility Scope

Execution is responsible for:

| Responsibility | Description |
|------|------|
| Objective Alignment | Directly connected to Task goals |
| Output Generation | Generate verifiable Artifact |
| Contract Compliance | Maintain defined input/output contract |
| Reproducibility | Reproducible under identical conditions |
| Traceability | Record execution history |

Execution does **not bear quality assurance responsibility**.
Quality judgment is the role of Evaluation phase.

---

## 4. Inputs (Inputs)

Execution inputs are one or more of:

- Preceding Task Artifact
- Evidence
- Requirements / specification / policies
- Environment configuration / constraints

### ✅ Input Conditions

- Explicitly defined
- Referenceable
- Version identifiable
- No contract violation

---

## 5. Outputs (Outputs)

Execution must generate:

- **Artifact (mandatory)**
- Execution log / change history (recommended)
- Evaluation readiness state (mandatory)

### ❌ Unacceptable Outputs

- Non-verifiable results
- Implicit state changes
- Judgment without basis

---

## 6. Execution Rules

Execution follows the following rules:

1. **Purpose Orientation**
   - Must be directly connected to Task goals

2. **Output Centrality**
   - Artifact generation is core, not activity

3. **Contract-Based Execution**
   - Comply with defined Input/Output contract

4. **Reproducibility**
   - Identical input → Identical result structure possible

5. **Observability**
   - Leave execution traces (Log / Diff / Trace)

---

## 7. Execution Lifecycle

```
Preparation → Execution → Artifact Generation → Termination
```

| Phase | Description |
|------|------|
| Preparation | Input validation / environment confirmation |
| Execution | Perform defined work |
| Generation | Output generation |
| Termination | Transfer to Evaluation phase |

Execution termination ≠ Task termination

---

## 8. Quality-Related Principles

Execution does not judge quality.

✔ Execution → Produce result
✔ Evaluation → Judge quality

Quality activities possible in Execution phase:

- Run static analysis
- Perform tests
- Generate validation data

But **PASS/FAIL judgment is prohibited**

---

## 9. Failure and Execution

Execution failure types:

| Type | Example |
|------|------|
| Technical Failure | Build failure, runtime error |
| Contract Failure | Input format violation |
| Generation Failure | Artifact not generated |
| Environment Failure | Missing dependency |

On Execution failure:

→ Not immediate Task FAIL
→ Collect Evidence, then Evaluation phase judges

---

## 10. Anti-Patterns

### ❌ Activity-Centered Execution
- Perform work without Artifact

### ❌ Objective Mismatch Execution
- Work unrelated to Task goals

### ❌ Implicit Change
- State change without recording

### ❌ Evaluation Mixing
- Declare PASS in Execution phase

---

## 11. Recommended Metrics

| Metric | Meaning |
|--------|------|
| Artifact Generation Rate | Execution validity |
| Re-execution Stability | Determinism |
| Failure Type Distribution | Structural issue detection |
| Average Execution Time | Bottleneck analysis |

---

## 12. Examples

### 🧱 Task: ERD Definition

**Execution**
- Write Mermaid ERD
- Model entity relationships
- Apply naming conventions

**Artifact**
- `schema.mmd`

---

### 🧱 Task: Backend Slice

**Execution**
- Implement Controller
- Write UseCase
- Define Repository interface

**Artifact**
- Compilable code
- Test pass results

---

## 13. Agent Considerations

Agent Execution requirements:

- Strict input contract compliance
- Automatic change history recording
- Minimize non-determinism
- Structured failure cause

Agents can perform:

✔ Code generation
✔ Document writing
✔ Test execution

But:

❌ No PASS judgment authority (before Checkpoint)

---

## ✅ Core Summary

Execution is:

> **Not "act for achieving objective"
> but "structured execution phase for Artifact generation"**

Value of Execution in SSDAM is:

- What was done ❌
- What was generated ✔
- What is verifiable ✔
