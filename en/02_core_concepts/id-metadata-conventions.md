# 🧾 ID & Metadata Conventions

## 1. Purpose

This document standardizes the **identifier (ID), metadata, and reference notation rules**
used throughout SSDAM.

It ensures:

- Deterministic traceability
- Agent-compatible parsing
- Non-ambiguous referencing
- Structural integrity across artifacts

---

## 2. Common Principles

- Every structural element must have a **unique ID**
- IDs must be **stable and non-reusable**
- IDs and timestamps must be recorded **together**
- References must be readable by **humans and agents**
- Metadata must be **explicit, never implicit**

---

## 3. ID Schema

| Target | Prefix | Example | Pattern |
|--------|--------|---------|---------|
| Mission | `MIS` | `MIS-20260221-001` | `^MIS-[0-9]{8}-[0-9]{3}$` |
| Task | `TSK` | `TSK-042` | `^TSK-[0-9]{3,}$` |
| Requirement | `REQ` | `REQ-012` | `^REQ-[0-9]{3,}$` |
| Execution | `EXE` | `EXE-0042` | `^EXE-[0-9]{3,}$` |
| Artifact | `ART` | `ART-104` | `^ART-[0-9]{3,}$` |
| Evaluation | `EVAL` | `EVAL-104` | `^EVAL-[0-9]{3,}$` |
| Evidence | `EVD` | `EVD-104` | `^EVD-[0-9]{3,}$` |
| Checkpoint | `CP` | `CP-TSK-042` | `^CP-[A-Z0-9-]+$` |
| Recovery | `RCV` | `RCV-TSK-042-01` | `^RCV-[A-Z0-9-]+$` |
| Quality Policy | `QPOL` | `QPOL-01` | `^QPOL-[0-9]{2,}$` |
| Recovery Policy | `RPOL` | `RPOL-02` | `^RPOL-[0-9]{2,}$` |
| Traceability Policy | `TPOL` | `TPOL-01` | `^TPOL-[0-9]{2,}$` |

---

## 4. ID Assignment Rules

- IDs must **never be reused**
- Deleted element IDs remain retired
- IDs must not encode volatile runtime states
- Ordering is governed by composition structures, not numbering

Insertion Rule:

If insertion is required mid-sequence:

→ Increment ID without renumbering prior elements

---

## 5. Timestamp Rules

**Required Format:** ISO-8601 UTC

```
YYYY-MM-DDTHH:mm:ssZ
```

Example:

`2026-02-21T05:30:00Z`

**Permitted:**

- Local offset notation (`+09:00`) for Evidence source recording only

**Prohibited:**

❌ Date-only  
❌ Missing timezone  

---

## 6. Actor Field Rules

Allowed values:

- `human`
- `agent`
- `policy`

Optional auxiliary fields:

- `actor_id`
- `actor_role`

Example:

```
actor: agent
actor_id: agent:gpt-reviewer-v1
actor_role: evaluator
```

---

## 7. Versioning Rules

Recommended: **Semantic Versioning (SemVer)**

`vMAJOR.MINOR.PATCH`

| Component | Meaning |
|-----------|----------|
| MAJOR | Breaking structural change |
| MINOR | Backward-compatible expansion |
| PATCH | Non-functional corrections |

Policy documents must include:

`policy_version`

---

## 8. Integrity & Hash Rules

Artifacts and Evidence should record:

- Hash value (recommended: `sha256`)
- Lock/freeze method (optional)

Example:

```
hash: sha256:8f3b...
lock_method: immutable
```

---

## 9. Reference Notation Rules

Priority:

1️⃣ ID Reference  
2️⃣ Path Reference  
3️⃣ External URI  

Example:

```
artifact_id: ART-104
location: docs/artifacts/schema.mmd
source_ref: https://...
```

Rules:

- ID-only references allowed only when context is unambiguous
- External URIs require `collected_at`

---

## 10. Filename Conventions

Recommended patterns:

| Type | Pattern |
|------|---------|
| Template | `*.template.md` |
| Instance | `<type>-<id>.md` |

Examples:

- `task-spec-TSK-042.md`
- `evaluation-EVAL-104.md`
- `checkpoint-CP-TSK-042.md`

---

## 11. Metadata Integrity Rules

Required fields (minimum):

- `id`
- `timestamp`
- `actor`

Optional but recommended:

- `version`
- `hash`
- `policy_ref`

---

## 12. Validation Checklist

- [ ] Unique ID assigned
- [ ] Timestamp recorded (UTC)
- [ ] Actor value valid
- [ ] Version present (if applicable)
- [ ] Hash recorded (if applicable)
- [ ] References resolvable

---

## ✅ Key Summary

ID & Metadata Conventions ensure:

- Deterministic PASS / FAIL traceability
- Agent-parsable structures
- Immutable decision history
- Stable cross-document references

Loose ID rules → Traceability collapse → Non-deterministic system behavior.
