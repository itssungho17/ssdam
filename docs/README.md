# SSDAM — SOLID Stage-Driven Automation Mechanism

SSDAM is a development, design, and AI collaborative operation system that defines **Stage** as the top-level unit, structures artifacts and evidence through the **Execution → Artifact → Evaluation → Evidence → Checkpoint** flow, and secures quality, traceability, and recoverability simultaneously.

---

## Languages

| Language | Path | Overview |
|----------|------|----------|
| 🇰🇷 한국어 | [`ko/`](ko/) | [`ko/README.md`](ko/00_overview/README.md) |
| 🇺🇸 English | [`en/`](en/) | [`en/README.md`](en/00_overview/README.md) |

---

## Documentation Structure

```
docs/
├── README.md                ← This file
├── en/                      ← English documentation
│   ├── SSDAM.md             ← Framework overview
│   ├── 00_overview/         ← Entry point & quickstart
│   ├── 01_principles/       ← Immutable rules
│   ├── 02_architecture/     ← Flow, lifecycle, composition
│   ├── 03_methodology/      ← Stage design & project planning guides
│   ├── 04_templates/        ← AI agent prompt templates
│   │   ├── 01_project/      ← Project-level prompts
│   │   ├── 02_stage/        ← Stage-level prompts
│   │   └── 03_elements/     ← Element-level prompts
│   ├── 05_examples/         ← Usage examples
│   ├── 06_specs/            ← Glossary, ID & metadata conventions
│   └── 07_reference/        ← Element reference definitions
└── ko/                      ← Korean documentation (same structure)
```

---

## Quick Navigation

| Layer | What it answers | Path |
|-------|-----------------|------|
| Overview | What is SSDAM? | `SSDAM.md` |
| Principles | What rules must never be broken? | `01_principles/` |
| Architecture | How do elements and state transitions connect? | `02_architecture/` |
| Methodology | How do you design stages and plan projects? | `03_methodology/` |
| Templates | How do you record documents? (AI agent prompts) | `04_templates/` |
| Examples | Real-world usage examples | `05_examples/` |
| Specs | Terminology, ID, and metadata rules | `06_specs/` |
| Reference | Definitions and judgment criteria for each element | `07_reference/` |

---

## Core Execution Model

```
Execution → Artifact → Evaluation → Evidence → Checkpoint
```

Every Stage follows this immutable flow. Progress is defined not by activity, but by **verified state transitions** through PASS/FAIL judgments.

---

## Getting Started

1. Read [`SSDAM.md`](en/SSDAM.md) for the framework overview
2. Review [`01_principles/`](en/01_principles/principles.md) for immutable rules
3. Follow [`00_overview/quickstart.md`](en/00_overview/quickstart.md) to complete your first Stage

---

## License

This project is proprietary. All rights reserved.
