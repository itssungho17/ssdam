# 🧾 ID & Metadata Conventions

## 1. Purpose

This document unifies ID rules, metadata rules, and reference notation rules
used throughout SSDAM documentation.

---

## 2. Common Principles

- All documents have a unique identifier.
- IDs follow a meaningful prefix + numbering system.
- Identifiers and timestamp (`timestamp`) are always recorded together.
- Links are maintained in a format parseable by both humans and agents.

---

## 3. ID Schema

| Target | Prefix | Example Format | Pattern |
|---|---|---|---|
| Project | `PRJ` | `PRJ-001` | `^PRJ-[0-9]{3,}$` |
| Requirement | `REQ` | `REQ-012` | `^REQ-[0-9]{3,}$` |
| Stage | `STG` | `STG-03` | `^STG-[0-9]{2,}$` |
| Execution | `EXE` | `EXE-0042` | `^EXE-[0-9]{3,}$` |
| Artifact | `ART` | `ART-104` | `^ART-[0-9]{3,}$` |
| Evaluation | `EVAL` | `EVAL-104` | `^EVAL-[0-9]{3,}$` |
| Evidence | `EVD` | `EVD-104` | `^EVD-[0-9]{3,}$` |
| Checkpoint | `CP` | `CP-STG-03` | `^CP-(STG-[0-9]{2,}|[A-Z0-9-]+)$` |
| Recovery | `RCV` | `RCV-STG-03-01` | `^RCV-[A-Z0-9-]+$` |
| Quality Policy | `QPOL` | `QPOL-01` | `^QPOL-[0-9]{2,}$` |
| Recovery Policy | `RPOL` | `RPOL-02` | `^RPOL-[0-9]{2,}$` |
| Traceability Policy | `TPOL` | `TPOL-01` | `^TPOL-[0-9]{2,}$` |

---

## 4. ID Assignment Rules

- IDs are not reused within the same prefix.
- Deleted item IDs are not reassigned.
- If mid-operation insertion is necessary, increment the final number. (Insertion after `STG-02` can also use `STG-11`)
- Human reading order and ID order may differ. Order is managed by `project-stage-map`.

---

## 5. Timestamp Rules

Recommended format: ISO-8601 UTC

```
YYYY-MM-DDTHH:mm:ssZ
```

Examples:
- `2026-02-15T09:30:00Z`

Permitted:
- Local offset notation (`+09:00`) only for Evidence source timestamp recording

Prohibited:
- Date only (`2026-02-15`)
- Time without timezone (`2026-02-15T09:30:00`)

---

## 6. Actor Field Rules

The `actor(human/agent/policy)` field uses only the following values:

- `human`
- `agent`
- `policy`

Add auxiliary fields when necessary:
- `actor_id` (e.g., `user:kim`, `agent:gpt-ops-v2`)
- `actor_role` (e.g., `stage_owner`, `reviewer`)

---

## 7. Version Rules

Recommended: SemVer (`vMAJOR.MINOR.PATCH`)

- `MAJOR`: Breaking change
- `MINOR`: Compatible expansion
- `PATCH`: Typo/non-functional fixes

Policy documents must record `policy_version`.

---

## 8. Integrity/Hash Rules

- Artifact/Evidence should record hash whenever possible.
- Recommended algorithm: `sha256`
- If using signature repository, specify in `lock_method`.

Examples:
- `hash: sha256:8f3b...`
- `lock_method: signature`

---

## 9. Reference Notation Rules

Document references follow this priority:

1. ID reference (`artifact_id: ART-104`)
2. Path reference (`location: docs/output/auth-spec.md`)
3. External URI reference (`source_ref: https://...`)

Required:
- If ID reference alone doesn't convey meaning, record path/URI together.
- External URIs must be accompanied by collection time (`collected_at`).

---

## 10. Filename Recommendation Rules

- Template: `*.template.md`
- Instance: `<type>-<id>.md` recommended

Examples:
- `stage-spec-STG-03.md`
- `evaluation-EVAL-104.md`
- `checkpoint-CP-STG-03.md`

---

## 11. Validation Checklist

- [ ] All documents have required ID and timestamp.
- [ ] `actor` values do not exceed the permitted set (`human/agent/policy`).
- [ ] Policy IDs are referenceable in Checkpoint/Stage Spec.
- [ ] Artifact/Evidence contain hash or lock information.
- [ ] FAIL records are connected via Recovery ID.

---

## 12. Summary

ID and metadata rules are the foundation for SSDAM's traceability and automation compatibility.
When rules become loose, reproducibility of PASS/FAIL judgments immediately deteriorates.
