---
name: user-input
description: "SSDAM entry skill. Transforms a user's unstructured idea, goal, or problem into quest-seed.yaml. Use when: structuring raw ideas, project initialization, generating a quest seed, starting SSDAM, or when deriving goals, requirements, and stages is needed."
compatibility: Universal. Can be used with any AI agent capable of YAML output, including ChatGPT, Claude, Cursor, Codex, etc.
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# User Input Structuring (SSDAM Entry)

## When to Use

Activate this skill when:
- A user provides an unstructured idea, goal, or problem
- The task requires deriving goals, requirements, or stage candidates
- An SSDAM quest-seed.yaml must be generated

Pipeline position:
```
[User Idea] → THIS SKILL → quest-plan → stage-spec → [element chain]
```

This is the **only** skill that accepts free-form input.
All subsequent templates receive structured YAML from their predecessor.

---

## Core Responsibility

You are the entry-point agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role: receive a user's unstructured idea and transform it into a structured quest seed (YAML)
that subsequent SSDAM templates can consume without additional context.

> For full framework details → [references/SSDAM.md](references/SSDAM.md)

---

## Input

| Field | Required | Description |
|-------|----------|-------------|
| idea_raw | Yes | Free-form text: user's idea, goal, or problem |
| constraints | No | Known constraints (budget, timeline, technology, team, etc.) |
| domain | No | Industry or domain context |
| existing_artifacts | No | Existing documents, code, designs already available |

## Output

A single YAML document: `quest-seed.yaml`

> Full schema → [assets/quest-seed.schema.yaml](assets/quest-seed.schema.yaml)
> Handoff contract → [references/SSDAM.md](references/SSDAM.md) § Handoff Contract

---

## Process

### Step 1 — Idea Validation

Assess whether the input is actionable. Check ALL:
- Contains an identifiable goal or problem to solve
- Specific enough to derive at least one testable outcome
- Not a single-word or purely abstract concept

**If any check fails** → output ONLY:

```yaml
idea_validation:
  status: INCOMPLETE
  clarifying_questions:
    - "question 1"
    - "question 2"
  guidance: "Please provide answers and resubmit."
```

Do NOT proceed further. Do NOT produce a partial seed.

**If all checks pass** → proceed to Step 2.

### Step 2 — Quest Metadata

- quest_id: `QST-YYYYMMDD-NNN`
- quest_owner: read from [assets/user-input.yaml](assets/user-input.yaml) metadata.quest_owner or `"undefined"`. Do NOT guess or infer.
- domain: from input **as-is**. Do NOT reinterpret or translate.

### Step 3 — Goal Structuring

Convert the raw idea into a testable quest goal:
- Clear subject (what will be built/achieved)
- Success condition (how to verify)
- Bounded scope (not open-ended)

Each success criterion must be PASS/FAIL decidable.

**Anti-patterns — rewrite if matched:**
- "Build a good system" → not testable (what is "good"?)
- "Improve performance" → not bounded (by how much? of what?)
- "Create an app" → no success condition

### Step 4 — Requirements Extraction

Extraction order:
1. Functional requirements directly stated or implied by the idea
2. Non-functional requirements only if the user mentioned constraints

Do NOT invent requirements the user did not mention or imply.

Rules:
- Every statement must be PASS/FAIL verifiable (no "user-friendly", "fast", "secure" without thresholds)
- Minimum 3 requirements for non-trivial quests
- ID format: `REQ-001`

### Step 5 — Stage Candidates

Decompose by **value delivery sequence**, not by technical layer.
Ask: "What must be validated BEFORE the next thing can start?"

- Bad: "Backend Implementation" → "Frontend Implementation" (technical layer split)
- Good: "Auth & Access Control" → "Core Transaction Logic" (value delivery sequence)

Rules:
- Minimum 2 stages
- Every REQ-XXX mapped to at least one stage
- No stage should have more than 3 primary requirements (split if necessary)
- Stage names: purpose-oriented, not activity-oriented
- Each stage's Checkpoint must be independently verifiable
- ID format: `STG-01`

### Step 6 — Constraints

Record ONLY what the user explicitly stated. Do NOT infer.
Read from [assets/user-input.yaml](assets/user-input.yaml) constraints.
Use `"undefined"` for any field not mentioned — never leave blank, never guess.

Key fields:
- `backend_stack`: server framework + DB (e.g., "Spring Boot + PostgreSQL") or `"undefined"`
- `frontend_stack`: frontend framework (e.g., "Svelte") or `"undefined"`
- `project_root`: local absolute path to project worktree (e.g., "/home/user/my-app") or `"undefined"`
- `ssdam_root`: Path where SSDAM artifacts are stored (e.g., "/home/user/my-app/.ssdam") or `"undefined"`. All subsequent skills save their YAML artifacts to this path.
- `timeline`, `budget`, `team`: from user input or `"undefined"`

### Step 7 — Handoff

Generate handoff section with:
- `next_template: quest-plan.template`
- `payload`: quest_id, quest_owner, quest_goal, domain, stage_list, requirement_ids
- `instruction`: "Feed this YAML + quest-plan.template.md into next AI call."

### Step 8 — Self-Validation

Verify ALL before outputting. If any fails, fix first.

- [ ] Quest goal is a single testable statement with success criteria
- [ ] All requirements are PASS/FAIL decidable (no ambiguous language)
- [ ] Every requirement maps to at least one stage candidate
- [ ] Every stage has a single purpose and a concrete artifact
- [ ] Handoff contains all fields required by quest-plan.template
- [ ] No "generally good", "user-friendly", "adequate" or similar vague terms
- [ ] Constraints section is filled (with "undefined" for unknowns, not blank)

---

## Output Rules

1. Output ONLY valid YAML. No markdown, no prose, no explanations outside YAML.
2. Do NOT wrap in code fences. Raw YAML directly.
3. Every key in [assets/quest-seed.schema.yaml](assets/quest-seed.schema.yaml) MUST appear. No extra keys.
4. If `idea_validation.status` is `INCOMPLETE` → output ONLY the idea_validation block. Nothing else.
5. Strings containing special characters (`: # ,` etc.) MUST be quoted.
6. Multi-line strings MUST use YAML block scalar (`>` or `|`).
7. Indentation: 2 spaces. No tabs.
8. Output MUST be parseable by PyYAML / SnakeYAML / js-yaml.
9. **Language rule:** All human-readable text (descriptions, statements, names) MUST match the language of idea_raw. YAML keys remain English.

**Delivery:**
- If `ssdam_root` is specified → Save to `{ssdam_root}/quest/quest-seed.yaml`
- If `ssdam_root` is `"undefined"` and file output is supported → Provide as `quest-seed.yaml`
- If file output is not supported → Output raw YAML text directly (without a code fence)