---
name: frontend-design
description: Frontend-specialised design skill. Reads architecture-design (required) and backend-design (optional) to produce a complete frontend specification: pages, component tree, state management, API integration, and routing. Its output drives frontend-implementation.
compatibility: Universal.
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# Frontend-Design AgentSkill

## Overview

**frontend-design** is the sixth step in the SSDAM execution pipeline (after backend-design, optional). It transforms architectural and backend specifications into a complete frontend design specification covering pages, components, state management, API integration, and routing.

This skill produces a single output document (frontend-design.TSK-NNN.md) that drives the final implementation step (frontend-implementation).

## Skill Chain Context

```
task-spec.TSK-NNN.yaml
  + architecture-design.TSK-NNN.md (required)
  + backend-design.TSK-NNN.md      (optional — provides API specs)
    ↓
[frontend-design]  ← YOU ARE HERE
    ↓
.ssdam/{id}/output/design/frontend-design.TSK-NNN.md
    ↓
[frontend-implementation]
```

## Trigger and I/O

| Aspect | Details |
|--------|---------|
| **Trigger** | `/frontend-design <task-spec-path>` |
| **Input** | `task-spec.TSK-NNN.yaml` + `architecture-design.TSK-NNN.md` (req.) + `backend-design.TSK-NNN.md` (opt.) |
| **Output** | `.ssdam/{id}/output/design/frontend-design.TSK-NNN.md` |
| **Tech Stack** | Svelte 5, TypeScript, TailwindCSS, Vite, SvelteKit (varies by task-spec.tech_stack) |

## Execution Procedure

### Step 1: Load Inputs

1. Parse `task-spec.TSK-NNN.yaml`:
   - Extract `purpose.scope_included` (features/views requiring frontend)
   - Extract `purpose.scope_excluded` (out-of-scope frontend features)
   - Read `execution_plan.tech_stack` to determine frontend framework (default: Svelte 5)
   - Extract `requirement_ids` and `output_contract` (acceptance criteria)

2. Read `architecture-design.TSK-NNN.md`:
   - Extract `domain_entities` (data model overview)
   - Extract `api_contract_overview` (high-level API structure)
   - Extract `module_boundaries` (system partitioning)
   - Note any user roles and permission levels

3. If `backend-design.TSK-NNN.md` exists:
   - Read `api_endpoints` section (precise endpoints, methods, paths)
   - Read `schemas` section (TypeScript interfaces for request/response types)
   - Use these details for precise API integration plan (override api_contract_overview if conflicting)

**Error handling:**
- If `architecture-design.TSK-NNN.md` not found: Stop and instruct user to run `/architecture-design` first.
- If no frontend scope in `scope_included`: Warn that this task has no frontend work — skip frontend chain entirely.

### Step 2: Identify Pages and Routes

For each item in `scope_included` that involves user interface:

1. **Page identification:** List each distinct page or view.
   - Page name: descriptive (e.g., "Library", "UploadManagement", "Marketplace")
   - Route: SvelteKit route pattern (e.g., `/`, `/uploads`, `/marketplace/[id]`)
   - Purpose: one-sentence description of what the page does
   - Accessed by: which user role(s) can access this page (from architecture-design)
   - Layout: which layout wrapper component (e.g., "AppLayout", "AuthLayout", "BlankLayout")

2. Verify all UI-related scope_included items are represented by at least one page.

### Step 3: Design Component Tree

For each page identified in Step 2:

1. **Page component:** Create a top-level page component.
   - File: `src/routes/{route}/+page.svelte`
   - Responsibility: page-level layout, data loading orchestration, page-specific state

2. **Layout components:** Identify shared UI (header, sidebar, footer, navigation).
   - Shared across pages → `src/lib/components/layout/` (e.g., `AppHeader.svelte`, `AppSidebar.svelte`)
   - One layout per page category (e.g., "AppLayout" for authenticated pages, "AuthLayout" for login/signup)

3. **Feature components:** Components specific to a feature or page.
   - File: `src/lib/components/features/{FeatureName}/`
   - Examples: `MediaGrid.svelte`, `FileUploadModal.svelte`, `FilterPanel.svelte`
   - Responsibility: handle a discrete feature or interaction

4. **Atomic components:** Reusable, primitive components.
   - File: `src/lib/components/atomic/` (e.g., `Button.svelte`, `TextField.svelte`, `Modal.svelte`)
   - Responsibility: single, focused UI pattern (no business logic)

**For each component, define:**

| Attribute | Format | Example |
|-----------|--------|---------|
| Component name | PascalCase | `MediaGrid`, `FileUploadModal` |
| File path | Relative to project_root | `src/lib/components/features/MediaGallery/Grid.svelte` |
| Category | page \| layout \| feature \| atomic | `feature` |
| Props | List with types | `items: MediaFile[]`, `selectedId: string \| null` |
| Events | Custom events dispatched | `on:select={...}` → `{ detail: { id: string } }` |
| Stores used | List of stores read/written | `mediaFilesStore`, `authStore` |

### Step 4: Design State Management

For each piece of shared state (data needed across multiple components):

1. **Store identification:** One store per domain concept.
   - Examples: `authStore`, `mediaFilesStore`, `purchasesStore`, `uiStateStore`
   - Do NOT create one massive global store — partition by domain.

2. **For each store, define:**

| Attribute | Format | Example |
|-----------|--------|---------|
| Store name | camelCase | `mediaFilesStore` |
| Store file | `src/lib/stores/{storeName}.ts` | `src/lib/stores/mediaFiles.ts` |
| State interface | TypeScript interface | `interface MediaFilesState { items: MediaFile[]; loading: boolean }` |
| Initial state | Concrete values | `{ items: [], loading: false, error: null }` |
| Actions/methods | Named operations | `fetchFiles()`, `uploadFile(file)`, `deleteFile(id)` |
| Derived stores | Computed values | `selectedCount$ = derived(...)` |

### Step 5: Design API Integration

For each API call the frontend needs to make:

1. **Endpoint mapping:** Match each component action to a backend endpoint.
   - Method: GET, POST, PUT, DELETE, PATCH
   - Path: e.g., `/api/media/files`, `/api/uploads/{id}`
   - Source: from `backend-design.api_endpoints` if available, else from `architecture-design.api_contract_overview`

2. **Trigger identification:** Which user action initiates each call.
   - Example: "Click 'Upload' button" → `POST /api/uploads`
   - Example: "Page load on /library" → `GET /api/media/files`
   - Example: "Delete media" → `DELETE /api/media/files/{id}`

3. **Component/store responsibility:** Which component/store makes the call.
   - Prefer stores for shared data (mediaFilesStore.fetchFiles())
   - Prefer components for isolated actions

4. **TypeScript types:** For each endpoint, define request and response types.
   - Request interface (if body is required): `CreateUploadRequest { filename: string; mimetype: string }`
   - Response interface: `MediaFile { id: string; filename: string; size: number; uploadedAt: Date }`
   - Match field names exactly with backend schemas (from backend-design)

5. **Loading and error handling:**
   - Every API call must update a loading state before fetch, unset in finally block
   - Every API call must catch errors and update error state
   - Components displaying results show loading spinner, error message, or success state

6. **Group into API client module:**
   - File: `src/lib/api/{domain}.ts` (e.g., `src/lib/api/mediaFiles.ts`)
   - Export async functions (not methods on a class)
   - Examples:
     ```typescript
     export async function fetchMediaFiles(): Promise<MediaFile[]> { ... }
     export async function uploadFile(file: File): Promise<MediaFile> { ... }
     ```

### Step 6: UI/UX Decisions

For each significant interaction identified in Steps 2-5:

1. **Interaction pattern:** Name the interaction (e.g., "double-click to open detail", "drag-to-reorder", "search-to-filter")

2. **Component responsible:** Which component handles it.

3. **Behavior:** What happens in response.
   - Example: "Double-click media → open detail modal"
   - Example: "Type in search field → filter list in real-time"
   - Example: "Click upload → show file picker"

4. **State changes:** Which store(s) update, and how.
   - Example: `mediaFilesStore.setSelectedId(id)` → detail modal becomes visible

### Step 7: Define File Structure

List all files and directories to be created in `project_root/`:

| Directory/File | Description | Example |
|----------------|-------------|---------|
| `src/routes/` | SvelteKit page routes | `src/routes/+page.svelte`, `src/routes/library/+page.svelte` |
| `src/lib/components/` | Reusable components | `src/lib/components/MediaGrid.svelte` |
| `src/lib/components/layout/` | Layout wrappers | `src/lib/components/layout/AppLayout.svelte` |
| `src/lib/components/atomic/` | Primitive components | `src/lib/components/atomic/Button.svelte` |
| `src/lib/stores/` | Svelte stores | `src/lib/stores/mediaFiles.ts` |
| `src/lib/api/` | API client functions | `src/lib/api/mediaFiles.ts` |
| `src/lib/types/` | TypeScript interfaces | `src/lib/types/media.ts`, `src/lib/types/auth.ts` |
| `tests/` | Component and store tests | `tests/components/MediaGrid.test.ts` |

### Step 8: Test Strategy and Write Output

1. **Define testing approach:**
   - Test runner: Vitest + Svelte Testing Library
   - Per-component testing: component renders, props work, events dispatch, stores integrate
   - Store testing: actions update state correctly, derived values compute
   - API client testing: functions call correct endpoints, handle errors, transform responses

2. **Write output document** `.ssdam/{id}/output/design/frontend-design.TSK-NNN.md`:
   - Follow structure in `references/output.template.yaml`
   - Include all pages, components, stores, API integrations, file structure, test strategy
   - Self-validation: verify all scope_included UI items are addressed

## Post-Execution

On successful completion:

```
✓ frontend-design.TSK-NNN.md written.
  - N pages defined
  - N components defined
  - N stores defined
  - N API endpoints integrated

Next: run /frontend-implementation <task-spec-path>
```

## Error Handling

| Error | Action |
|-------|--------|
| `architecture-design.TSK-NNN.md` not found | Stop. Instruct user: "Run /architecture-design first." |
| No frontend scope in `task-spec.scope_included` | Warn: "This task has no frontend work — skipping frontend chain." Do not produce a document. |
| `backend-design.TSK-NNN.md` not found | Proceed using `api_contract_overview` from architecture-design as fallback. Document the fallback. |
| Incomplete pages/components | Return error: "Step 3: [list missing components needed for scope_included]" |
| Missing API integration for a page action | Return error: "Step 5: [page/action] has no API endpoint defined." |

## References

- **input.template.yaml**: Template for parsing task-spec, architecture-design, backend-design
- **output.template.yaml**: Schema for the output frontend-design.TSK-NNN.md document
- **rules.md**: Mandatory conventions (naming, store design, component structure, etc.)

## Compatibility Notes

- **Framework detection:** Read `task-spec.execution_plan.tech_stack.frontend` to determine framework (Svelte 5, React, Vue, etc.). This skill is optimized for Svelte 5 but abstracts patterns for other frameworks.
- **TypeScript:** All interface definitions must match backend schemas exactly (same field names, compatible types).
- **Styling:** TailwindCSS is the default CSS framework. Adjust if task-spec specifies otherwise.
