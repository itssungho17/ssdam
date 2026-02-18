# Governance & Policy Reference

## Governance Axes

### Role System
- **quest_owner**: Finalizes quest-level policies/structure. Approves quest-level policies. Excluded from individual execution details.
- **stage_owner**: Responsible for stage contract/decision. Approves stage-level checkpoints. Excluded from changing quest-wide policies.
- **agent**: Automates execution/evaluation/recovery. Auto-decides within policy-permitted scope. Excluded from final accountability for decisions outside policy.

### Gate Type
- **automatic**: Decidable by quantitative criteria alone
- **human**: Requires contextual/strategic judgment
- **hybrid**: Automated evaluation + human confirmation

### Escalation
Triggers for human involvement based on repeated failures, uncertainty, or risk level.

---

## Stage Map Principles

- Dependencies are **Artifact-based** (not activity sequence-based).
- All stages must have PASS/FAIL branch rules.
- FAIL branches without Recovery paths cannot exist.
- Composition patterns: Sequential / Parallel / Conditional / Iterative

---

## Policy Domains

- **Quality Policy (QPOL)**: Quantitative thresholds, measurement methods, PASS/FAIL criteria
- **Recovery Policy (RPOL)**: Max retries, rollback scope, escalation conditions
- **Traceability Policy (TPOL)**: Record items, required links, retention periods

---

## Immutable Rules

- Final accountability always rests with people (quest_owner or stage_owner).
- Agents can only auto-decide within policy-permitted scope.
- High-risk / high-uncertainty situations must escalate to human stakeholders.
- All quality criteria must be PASS/FAIL-decidable. No ambiguous language.
- Policy IDs must be referenceable in stage-spec and checkpoint documents.
