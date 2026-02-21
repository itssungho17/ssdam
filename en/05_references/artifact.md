# 📦 Artifact — SSDAM Reference

## 1. Definition

**Artifact** is the **verifiable and evaluable output** generated as a result of Execution.

In SSDAM, Artifact is not a simple deliverable but:

> **"A formal evidence object that enables state transitions"**

---

## 2. Role

Core roles of Artifact:

- Provide input for Evaluation
- Provide basis for Evidence generation
- Subject of Checkpoint judgment
- Node connecting Traceability

Progression in SSDAM is defined by
**Artifact creation and verification**, not activity.

---

## 3. Required Characteristics

All Artifacts must have the following characteristics:

| Characteristic | Description |
|------|------|
| **Verifiability** | Objectively evaluable |
| **Explicitness** | Form and content are clear |
| **Reproducibility** | Reproducible under identical conditions |
| **Identifiability** | Version / ID / hash, etc. |
| **Traceability** | Connected to requirements and Task |

---

## 4. Artifact Types

### 🧱 Document
- PRD
- Architecture Spec
- ADR
- Design Doc

### 🧩 Model
- ERD (Mermaid)
- UML
- State Diagram

### 💻 Code
- Source Code
- Config
- Script

### 🧪 Verification
- Test Report
- Coverage Result
- Benchmark Result

### 🚀 Operations
- Deployment Plan
- Release Note
- Runbook

---

## 5. Artifact Creation Rules

Artifact must:

1. Be a result of Execution
2. Have explicit structure
3. Be in evaluable state
4. Comply with contract (Input/Output)
5. Be storable and referenceable

---

## 6. Artifact Quality Criteria

Artifact must satisfy the following criteria:

| Criterion | Question |
|------|------|
| Completeness | Are all necessary information present |
| Consistency | Are there internal contradictions |
| Clarity | Is interpretation ambiguity minimized |
| Verifiability | Is the structure evaluable |
| Contract Compliance | Does it meet defined requirements |

---

## 7. Anti-Patterns

### ❌ Implicit Artifact
- Verbal agreements
- Undocumented decisions

### ❌ Non-Verifiable Artifact
- "Roughly completed"
- Output without criteria

### ❌ Non-Traceable Artifact
- No requirement connection
- No version information

### ❌ Non-Evaluable Artifact
- Cannot make PASS/FAIL determination

---

## 8. Artifact and State Transition

In SSDAM:

✔ Artifact exists → Part of progression conditions met
✔ Artifact verification PASS → State transition possible

Task is not completed by Artifact creation alone.

---

## 9. Change Management

When changing an Artifact:

- Increment version
- Record change history
- Track affected Tasks
- Determine if Evidence re-verification is needed

### 🔁 Change Types

| Type | Description |
|------|------|
| Modification | Content correction |
| Extension | Scope increase |
| Reduction | Scope decrease |
| Deprecation | Artifact invalidation |

---

## 10. Artifact Storage Principles

Artifact:

- Can be persistently stored
- Is accessible
- Has guaranteed integrity
- Is linkable

Recommended elements:

- Version
- Author / Agent
- Timestamp
- Hash / Signature
- Related Task

---

## 11. Relationship with Evidence

Artifact is **the subject of evaluation**,
Evidence is **the basis of evaluation**.

```
Execution → Artifact → Evaluation → Evidence
```

Artifact ≠ Evidence

---

## 12. Agent Considerations

Agent-generated Artifact requirements:

- Structured format
- Clear contract compliance
- May include uncertainty metadata
- Ensure reproducibility

Agent Artifacts must:

✔ Be human-reviewable
✔ Be automatically evaluable

---

## 13. Examples

### 🧱 Task: Requirement Definition

**Artifact**
- `PRD.md`

---

### 🧱 Task: Data Design

**Artifact**
- `schema.mmd`
- `migration.sql`

---

### 🧱 Task: Testing

**Artifact**
- `test-report.json`
- `coverage.xml`

---

## ✅ Core Summary

Artifact is:

> **Not a "deliverable"
> but "a formal object enabling verification and state transitions"**

Meaning of Artifact in SSDAM:

- Activity record ❌
- Evaluation subject ✔
- Decision input ✔
- Traceability node ✔
