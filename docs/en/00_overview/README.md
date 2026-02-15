# 00_overview

## 1. Purpose
`00_overview` is the **entry point** for the SSDAM documentation set.
It helps first-time readers quickly understand the overall structure, reading order, and minimum execution path.

---

## 2. Documentation Structure

| Document | Role |
|---|---|
| `00_overview/README.md` | Documentation map and reading order |
| `00_overview/quickstart.md` | Minimum execution path (complete 1 Stage) |

---

## 3. SSDAM Documentation Map

| Layer | Path | Question |
|---|---|---|
| Overview | `SSDAM.md` | What is SSDAM? |
| Principles | `01_principles/principles.md` | What are the rules that must never be broken? |
| Architecture | `02_architecture/*.md` | How are elements and state transitions connected? |
| Methodology | `03_methodology/*.md` | What is the procedure for actual design/planning? |
| Templates | `04_templates/**` | In what format are documents recorded? |
| Specifications | `06_specs/*.md` | What are the terminology/ID/metadata rules? |
| Reference | `07_reference/*.md` | What are the definitions and judgment criteria for each element? |

---

## 4. Recommended Reading Order

### 4.1 When Adopting for the First Time
1. `SSDAM.md`
2. `01_principles/principles.md`
3. `02_architecture/flow-architecture.md`
4. `00_overview/quickstart.md`
5. `04_templates/README.md`

### 4.2 When Designing a Stage
1. `03_methodology/stage-design-guide.md`
2. `07_reference/execution.md`
3. `07_reference/evaluation.md`
4. `07_reference/checkpoint.md`
5. `04_templates/02_stage/stage-spec.template.md`

### 4.3 When Operating a Project
1. `03_methodology/project-planning-guide.md`
2. `07_reference/traceability.md`
3. `06_specs/id-metadata-conventions.md`
4. `04_templates/01_project/*.template.md`

---

## 5. Minimum Onboarding Checklist

- [ ] Understood that state transitions occur with PASS/FAIL only.
- [ ] Applied `execution -> artifact -> evaluation -> evidence -> checkpoint` sequence without omission.
- [ ] Enforced that all judgments have Evidence links.
- [ ] Predefined Recovery path for FAIL scenarios.
- [ ] Applied common ID rules consistently across the entire project.

---

## 6. Starting Points

- Quick start: `00_overview/quickstart.md`
- Start with templates: `04_templates/README.md`
- Check definitions: `06_specs/glossary.md`
