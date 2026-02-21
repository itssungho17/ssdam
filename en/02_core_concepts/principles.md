# 📜 SSDAM Principles

## 🎯 Objective

SSDAM Principles define the **immutable rules** that must be preserved
throughout the mechanism’s design, extension, and operation.

---

## 🧱 Principle 1 — Task is the Top-Level Execution Unit

A **Task is the highest-level executable unit** in SSDAM.

Immutable Rules:
- Single clear purpose
- Explicit exit criteria
- Verifiable Artifacts

Anti-Patterns:
- Multi-purpose Tasks
- Missing exit criteria
- No Artifacts

---

## 🚀 Principle 2 — Mission Governs Intent, Not Execution

A **Mission is an intent-level container** composed of multiple Tasks.

Immutable Rules:
- Missions are not directly executable
- State transitions occur only through Tasks

---

## 🧩 Principle 3 — Contract-Driven Task Design

Every Task must define **explicit Contracts**.

Immutable Rules:
- No Task without Input / Output Contract
- No ambiguous Contracts

---

## 🔄 Principle 4 — Artifact-Driven Progress

Progress is defined by **Artifact validation**, not activity.

Immutable Rules:
- Every Task produces Artifacts
- Artifacts must be reviewable & evaluable

---

## ✅ Principle 5 — Evidence-Based Decision Making

Decision → Evidence required

Immutable Rules:
- No PASS without Evidence
- No FAIL without Evidence

---

## 🚦 Principle 6 — Checkpoint Authority

Checkpoint = sole decision gate

Immutable Rules:
- Only PASS / FAIL
- No implicit transitions

---

## 🔁 Principle 7 — Failure is a Designed Event

FAIL → Record → Preserve Evidence → Recovery

---

## 🔗 Principle 8 — End-to-End Traceability

Requirement → Task → Execution → Artifact → Evaluation → Evidence → Checkpoint

---

## 🤖 Principle 9 — Human / Agent Responsibility Model

Agent = executor  
Human = accountability owner

---

## 📐 Principle 10 — Deterministic Flow

Same input → Same judgment expected

---

## 🧩 Principle 11 — Structural Recovery Enforcement

Recovery must modify:
- Input / Strategy / Constraints / Skill Selection

---

## 🧩 Principle 12 — SSDAM Compatibility Constraints

Not allowed:
- Bypassing Checkpoints
- Removing Evidence
- Breaking Traceability

---

## ✅ Summary

SSDAM operates on:

**Not “What was executed,” but “What was validated.”**
