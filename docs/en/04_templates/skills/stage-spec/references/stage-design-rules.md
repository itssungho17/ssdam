# Stage Design Rules

## SOLID Principles for Stage Design

- **S (Single Responsibility)**: One testable purpose per stage.
- **O (Open/Closed)**: Stage structure is stable; extend via artifact variants.
- **L (Liskov Substitution)**: Output artifacts are interchangeable if they meet contract.
- **I (Interface Segregation)**: Contracts expose only necessary attributes.
- **D (Dependency Inversion)**: Stage depends on abstract contracts, not concrete implementations.

---

## Input Contract Rules

- First stage (no predecessor): `input_item = "none"`, `artifact_id = "none"`
- Other stages: input must reference specific artifact_ids from predecessor stage's output

---

## Output Contract Rules

- artifact_id format: `ART-STG-XX-NNN` (e.g., ART-STG-01-001)
- Each artifact must have a concrete contract_specification (format, structure, content)
- Artifacts must be reviewable and evaluable

---

## Evaluation Criteria Rules

- Must reference `QPOL-XX` from quest-plan.yaml policies.quality_policy
- Each criterion must have a quantitative `pass_threshold`
- Measurement method must be automated or clearly defined manual process

---

## Checkpoint Rules

- Must match `gate_type` from quest-plan.yaml's governance.gates[target]
- gate_type: `automatic` (quantitative only) / `human` (requires judgment) / `hybrid` (auto + human)

---

## Recovery Rules

- Must reference `RPOL-XX` from quest-plan.yaml policies.recovery_policy
- Strategies must be from: Re-execution / Correction / Re-stage / Rollback
- Escalation triggers must link to ESC rules from quest-plan.yaml

---

## Immutable Rules

- Final accountability rests with stage_owner (person), not agent.
- All criteria must be PASS/FAIL-decidable. No ambiguous language.
- Every FAIL path must have a Recovery mapping.
