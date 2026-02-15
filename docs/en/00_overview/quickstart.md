# SSDAM Quickstart

## 1. Objective
This document provides the **minimum path to complete 1 Stage to `COMPLETED` status**
when applying SSDAM for the first time.

Expected duration: 30~60 minutes

---

## 2. Prerequisites

- Project identifier (`PRJ-XXX`)
- At least 1 requirement ID (`REQ-001`)
- 1 Stage name (`STG-01`)
- Basic policy thresholds (e.g., test pass rate, review approval criteria)

ID format follows `06_specs/id-metadata-conventions.md`.

---

## 3. Step 1 — Write 3 Common Project Documents

1. `04_templates/01_project/project-governance.template.md`
2. `04_templates/01_project/project-policy.template.md`
3. `04_templates/01_project/project-stage-map.template.md`

Completion criteria:
- Roles/approval authority/escalation are defined.
- Policy IDs (`QPOL/RPOL/TPOL`) are defined.
- PASS/FAIL branching paths for `STG-01` exist.

---

## 4. Step 2 — Write Stage Contract

Open `04_templates/02_stage/stage-spec.template.md` and write `STG-01`.

Required:
- Single purpose (1)
- Input contract/Output contract
- Evaluation criteria that allow PASS/FAIL decision
- Checkpoint policy (`checkpoint_id`, `policy_id`)
- Recovery mapping by failure type

---

## 5. Step 3 — Record Execution Chain 5 Documents

The following order must be strictly maintained.

1. `04_templates/03_elements/execution.template.md`
2. `04_templates/03_elements/artifact.template.md`
3. `04_templates/03_elements/evaluation.template.md`
4. `04_templates/03_elements/evidence.template.md`
5. `04_templates/03_elements/checkpoint.template.md`

Decision rules:
- If `checkpoint.decision = PASS`, then `to_state = COMPLETED`
- If `checkpoint.decision = FAIL`, then `to_state = FAILED` + `recovery_id` required

---

## 6. Step 4 — Rehearse FAIL Path Once

Assuming checkpoint FAIL, write the following:

1. `04_templates/03_elements/recovery.template.md`
2. Re-evaluation results and Evidence links
3. Re-entry transition record (`FAILED -> IN_PROGRESS -> ...`)

Purpose:
- Ensure the team understands that failure is a designed event, not an exception.

---

## 7. Step 5 — Verify Completion

Quickstart is complete when all of the following are satisfied:

- [ ] `stage-spec` has PASS/FAIL/Recovery predefined.
- [ ] 5 execution chain documents are connected with the same `stage_id`.
- [ ] Checkpoint decision includes Evidence links.
- [ ] FAIL triggers Recovery document and re-evaluation results are connected.
- [ ] Traceability chain is unbroken.

Traceability chain standard: `07_reference/traceability.md`

---

## 8. Minimum Deliverable Set

- Project documents: `project-governance`, `project-policy`, `project-stage-map`
- Stage document: `stage-spec`
- Execution documents: `execution`, `artifact`, `evaluation`, `evidence`, `checkpoint`
- Failure rehearsal document: `recovery` (recommended)

---

## 9. Common Mistakes

- ❌ Create Artifact only and skip Checkpoint
- ❌ Use ambiguous sentences in PASS/FAIL criteria ("mostly acceptable")
- ❌ Make judgment without Evidence links
- ❌ Overwrite FAIL records

Correct approach:
- Record all judgments with policy + rationale + documentation.
