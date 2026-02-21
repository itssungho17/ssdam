---
name: frontend-implementation
description: Final frontend step in the SSDAM execution chain. Reads frontend-design and directly implements frontend code (Svelte components, stores, API client, routes, tests) in the project root. This skill is for Cursor AI agent autonomous execution.
compatibility: Cursor AI agent (autonomous code execution)
metadata:
  author: itssungho
  version: "v1.0.0"
  framework: SSDAM
  schema_version: "v1.0.0"
---

# Frontend-Implementation AgentSkill

## Overview

**frontend-implementation** is the seventh and final step in the SSDAM execution pipeline. It reads the `frontend-design.TSK-NNN.md` specification and directly implements all frontend code into the project root (Svelte components, stores, API client, routes, tests).

This skill is designed for **autonomous execution by Cursor AI agents** — it requires no human intervention and produces working, tested code.

## Skill Chain Context

```
frontend-design.TSK-NNN.md (required)
  + backend-design.TSK-NNN.md (optional)
    ↓
[frontend-implementation]  ← YOU ARE HERE
    ↓
Code in project_root/:
  src/routes/       ← SvelteKit pages
  src/lib/
    components/     ← Svelte components
    stores/         ← Svelte stores
    api/            ← API client functions
    types/          ← TypeScript interfaces
  tests/            ← Component and store tests
```

## Trigger and I/O

| Aspect | Details |
|--------|---------|
| **Trigger** | `/frontend-implementation <task-spec-path>` |
| **Input** | `task-spec.TSK-NNN.yaml` + `frontend-design.TSK-NNN.md` (required) + `backend-design.TSK-NNN.md` (optional) |
| **Output** | Code written directly to `project_root/` (no design document) |
| **Framework** | Svelte 5 (or from task-spec.tech_stack.frontend) |

## Execution Procedure

### Step 1: Load Inputs and Create Implementation Plan

1. **Parse task-spec.TSK-NNN.yaml:**
   - Extract `execution_plan.tech_stack.frontend` (framework: Svelte 5 by default)
   - Extract `execution_plan.tech_stack.project_root` (where to write code)
   - Extract `acceptance_criteria` (requirements for the implementation)
   - Extract `requirement_ids` (for traceability)

2. **Read frontend-design.TSK-NNN.md fully:**
   - Extract `pages` list (routes and page components)
   - Extract `components` list (all components to implement)
   - Extract `stores` list (Svelte stores to create)
   - Extract `api_integration` (API client functions)
   - Extract `file_structure` (directory/file plan)
   - Extract `test_strategy` (what to test)

3. **If backend-design.TSK-NNN.md exists:**
   - Read `api_endpoints` for precise URL, method, schema details
   - Read `schemas` for exact TypeScript interface definitions
   - Use these for API client implementation (override frontend-design if more precise)

4. **Create ordered implementation plan:**
   ```
   Phase 1: TypeScript types
     └─ Create src/lib/types/{domain}.ts files with all interfaces

   Phase 2: Svelte stores
     └─ Create src/lib/stores/{storeName}.ts files

   Phase 3: API client
     └─ Create src/lib/api/{domain}.ts files with fetch functions

   Phase 4: Atomic components
     └─ Create src/lib/components/atomic/{Component}.svelte (bottom-up)

   Phase 5: Feature components
     └─ Create src/lib/components/features/{Feature}/{Component}.svelte

   Phase 6: Layout components
     └─ Create src/lib/components/layout/{Layout}.svelte

   Phase 7: Page components
     └─ Create src/routes/{route}/+page.svelte

   Phase 8: Tests
     └─ Create tests/ directory structure and test files

   Phase 9: Verification
     └─ Run npm run test, verify all tests pass
     └─ Verify acceptance_criteria are met
   ```

**Rationale for bottom-up order:** Atomic components don't depend on others; feature components depend on atomic; page components depend on features. This ensures dependencies are met as we build.

---

### Step 2: Implement TypeScript Interfaces

For each type mentioned in `frontend-design.api_integration` and `frontend-design.stores`:

1. **Identify all types needed:**
   - Response types (from API endpoints)
   - Request types (for POST/PUT bodies)
   - Store state interfaces
   - Component-specific interfaces (if needed)

2. **Create type files in `src/lib/types/`:**
   - Group related types by domain (e.g., `src/lib/types/media.ts`, `src/lib/types/auth.ts`)
   - If backend-design exists, copy exact field names and types from its schemas

3. **Example implementation:**
   ```typescript
   // src/lib/types/media.ts
   export interface MediaFile {
     id: string;
     filename: string;
     size: number;
     mimetype: string;
     uploadedAt: Date;
     ownerId: string;
   }

   export interface UploadFileRequest {
     filename: string;
     mimetype: string;
     size: number;
   }

   export interface MediaFilesState {
     items: MediaFile[];
     loading: boolean;
     error: string | null;
     selectedIds: string[];
   }
   ```

4. **Ensure all types are TypeScript interfaces, not `any`.**
5. **Export all types from a barrel file (optional but recommended):**
   ```typescript
   // src/lib/types/index.ts
   export * from './media';
   export * from './auth';
   ```

---

### Step 3: Implement Svelte Stores

For each store in `frontend-design.stores`:

1. **Create store file at `src/lib/stores/{storeName}.ts`:**

2. **Implement writable store with initial state:**
   ```typescript
   import { writable, derived } from 'svelte/store';
   import type { MediaFilesState, MediaFile } from '../types';

   const initialState: MediaFilesState = {
     items: [],
     loading: false,
     error: null,
     selectedIds: []
   };

   export const mediaFilesStore = writable<MediaFilesState>(initialState);
   ```

3. **Implement all actions from frontend-design:**
   ```typescript
   export async function fetchFiles() {
     mediaFilesStore.update(state => ({ ...state, loading: true, error: null }));
     try {
       const files = await api.fetchMediaFiles();
       mediaFilesStore.update(state => ({ ...state, items: files, loading: false }));
     } catch (err) {
       mediaFilesStore.update(state => ({
         ...state,
         error: err instanceof Error ? err.message : 'Unknown error',
         loading: false
       }));
     }
   }

   export function selectFile(id: string) {
     mediaFilesStore.update(state => ({
       ...state,
       selectedIds: [...state.selectedIds, id]
     }));
   }

   export function deselectFile(id: string) {
     mediaFilesStore.update(state => ({
       ...state,
       selectedIds: state.selectedIds.filter(sid => sid !== id)
     }));
   }
   ```

4. **Implement derived stores (if defined in frontend-design):**
   ```typescript
   export const selectedCount$ = derived(mediaFilesStore, $store => $store.selectedIds.length);
   ```

5. **Export all store functions and derived stores.**

**Key points:**
- Do NOT call API directly in stores; stores call API client functions (defined in Step 4)
- Always set `loading: true` before async operation, `false` in finally
- Always catch errors and update `error` field
- Never use `any` type; use typed state interface

---

### Step 4: Implement API Client

For each endpoint in `frontend-design.api_integration`:

1. **Create or update `src/lib/api/{domain}.ts`:**

2. **Import types and utility functions:**
   ```typescript
   import type { MediaFile, UploadFileRequest } from '../types';
   ```

3. **Implement async fetch functions:**
   ```typescript
   const API_BASE = process.env.VITE_API_BASE || 'http://localhost:3000';

   export async function fetchMediaFiles(): Promise<MediaFile[]> {
     const res = await fetch(`${API_BASE}/api/media/files`, {
       method: 'GET',
       headers: { 'Content-Type': 'application/json' }
     });

     if (!res.ok) throw new Error(`Failed to fetch files: ${res.statusText}`);
     return res.json();
   }

   export async function uploadFile(file: File): Promise<MediaFile> {
     const formData = new FormData();
     formData.append('file', file);

     const res = await fetch(`${API_BASE}/api/uploads`, {
       method: 'POST',
       body: formData
     });

     if (!res.ok) throw new Error(`Upload failed: ${res.statusText}`);
     return res.json();
   }

   export async function deleteFile(id: string): Promise<void> {
     const res = await fetch(`${API_BASE}/api/media/files/${id}`, {
       method: 'DELETE',
       headers: { 'Content-Type': 'application/json' }
     });

     if (!res.ok) throw new Error(`Delete failed: ${res.statusText}`);
   }
   ```

4. **Add Authorization header for auth_required endpoints:**
   ```typescript
   import { get } from 'svelte/store';
   import { authStore } from '../stores';

   export async function fetchPrivateFiles(): Promise<MediaFile[]> {
     const $auth = get(authStore);
     const res = await fetch(`${API_BASE}/api/media/files`, {
       method: 'GET',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': `Bearer ${$auth.token}`
       }
     });

     if (!res.ok) throw new Error(`Failed to fetch: ${res.statusText}`);
     return res.json();
   }
   ```

5. **Error handling:**
   - Always throw descriptive Error objects (not raw strings)
   - Include HTTP status or message
   - Do NOT catch and suppress errors — let caller handle them

6. **Do NOT make HTTP calls directly in stores or components — always use API client.**

---

### Step 5: Implement Atomic Components

Implement reusable, presentation-only components in `src/lib/components/atomic/`:

1. **For each atomic component in frontend-design:**

2. **Create `.svelte` file with TypeScript:**
   ```svelte
   <script lang="ts">
     interface Props {
       label: string;
       type?: 'button' | 'submit' | 'reset';
       disabled?: boolean;
       size?: 'sm' | 'md' | 'lg';
       variant?: 'primary' | 'secondary' | 'danger';
     }

     let { label, type = 'button', disabled = false, size = 'md', variant = 'primary' }: Props = $props();
   </script>

   <button
     {type}
     {disabled}
     class:disabled
     class:sm={size === 'sm'}
     class:md={size === 'md'}
     class:lg={size === 'lg'}
     class:primary={variant === 'primary'}
     class:secondary={variant === 'secondary'}
     class:danger={variant === 'danger'}
     on:click
   >
     {label}
   </button>

   <style module>
     button {
       @apply px-4 py-2 rounded font-medium transition;
     }
     .primary { @apply bg-blue-600 text-white hover:bg-blue-700; }
     .secondary { @apply bg-gray-200 text-gray-800 hover:bg-gray-300; }
     .danger { @apply bg-red-600 text-white hover:bg-red-700; }
     .sm { @apply text-sm px-2 py-1; }
     .lg { @apply text-lg px-6 py-3; }
     .disabled { @apply opacity-50 cursor-not-allowed; }
   </style>
   ```

3. **Key rules:**
   - All props must be typed (no `any`)
   - No API calls, no store mutations
   - Use TailwindCSS for styling
   - Emit events if needed: `on:click`, custom events via `dispatch()`
   - Props should be simple types or interfaces, not functions

4. **Implement all atomic components before proceeding to feature components.**

---

### Step 6: Implement Feature and Page Components

Implement feature components in `src/lib/components/features/`:

1. **Feature components** (medium-complexity, domain-specific):
   ```svelte
   <script lang="ts">
     import { onMount } from 'svelte';
     import { mediaFilesStore } from '../../stores/mediaFiles';
     import * as api from '../../api/mediaFiles';
     import Button from '../atomic/Button.svelte';
     import MediaGrid from './MediaGallery/Grid.svelte';

     let loading = false;
     let error: string | null = null;

     async function handleUpload() {
       loading = true;
       error = null;
       try {
         const input = document.createElement('input');
         input.type = 'file';
         input.onchange = async (e) => {
           const file = (e.target as HTMLInputElement).files?.[0];
           if (file) {
             const result = await api.uploadFile(file);
             mediaFilesStore.addFile(result);
           }
         };
         input.click();
       } catch (err) {
         error = err instanceof Error ? err.message : 'Upload failed';
       } finally {
         loading = false;
       }
     }

     onMount(async () => {
       try {
         await mediaFilesStore.fetchFiles();
       } catch (err) {
         error = err instanceof Error ? err.message : 'Failed to load files';
       }
     });
   </script>

   <div class="space-y-4">
     {#if error}
       <div class="p-4 bg-red-100 text-red-800 rounded">
         {error}
       </div>
     {/if}

     <Button label="Upload File" on:click={handleUpload} disabled={loading} />

     {#if loading}
       <div class="text-center py-8">Loading...</div>
     {:else}
       <MediaGrid items={$mediaFilesStore.items} />
     {/if}
   </div>
   ```

2. **Page components** in `src/routes/{route}/+page.svelte`:
   ```svelte
   <script lang="ts">
     import AppLayout from '../../lib/components/layout/AppLayout.svelte';
     import MediaUpload from '../../lib/components/features/MediaUpload.svelte';
   </script>

   <AppLayout>
     <div class="container mx-auto">
       <h1 class="text-2xl font-bold mb-6">Media Library</h1>
       <MediaUpload />
     </div>
   </AppLayout>
   ```

3. **Key principles:**
   - Feature components call API functions and update stores
   - Page components orchestrate layout and feature components
   - All async operations must have loading + error states
   - Use `onMount` to load page data
   - Use `$store` syntax to read store values reactively

---

### Step 7: Implement Loading and Error States

For every API call in every component:

1. **Create reactive state variables:**
   ```typescript
   let loading = false;
   let error: string | null = null;
   ```

2. **Wrap API calls with try-catch-finally:**
   ```typescript
   async function fetchData() {
     loading = true;
     error = null;
     try {
       const data = await api.fetchData();
       store.update(s => ({ ...s, data }));
     } catch (err) {
       error = err instanceof Error ? err.message : 'An error occurred';
     } finally {
       loading = false;
     }
   }
   ```

3. **Show loading UI while loading:**
   ```svelte
   {#if loading}
     <Skeleton />
   {:else if error}
     <ErrorMessage message={error} />
   {:else}
     <Content />
   {/if}
   ```

4. **Disable form submissions while loading:**
   ```svelte
   <Button
     label="Submit"
     on:click={handleSubmit}
     disabled={loading}
   />
   ```

---

### Step 8: Write Tests and Verify

1. **Create test files using Vitest + Svelte Testing Library:**
   ```typescript
   // tests/components/Button.test.ts
   import { describe, it, expect } from 'vitest';
   import { render, screen } from '@testing-library/svelte';
   import userEvent from '@testing-library/user-event';
   import Button from '../../src/lib/components/atomic/Button.svelte';

   describe('Button', () => {
     it('renders with label', () => {
       render(Button, { props: { label: 'Click me' } });
       expect(screen.getByText('Click me')).toBeInTheDocument();
     });

     it('dispatches click event', async () => {
       const { component } = render(Button, { props: { label: 'Click' } });
       let clicked = false;
       component.$on('click', () => { clicked = true; });

       await userEvent.click(screen.getByRole('button'));
       expect(clicked).toBe(true);
     });

     it('disables when disabled prop is true', () => {
       render(Button, { props: { label: 'Click', disabled: true } });
       expect(screen.getByRole('button')).toBeDisabled();
     });
   });
   ```

2. **Test store actions:**
   ```typescript
   // tests/stores/mediaFiles.test.ts
   import { describe, it, expect } from 'vitest';
   import { mediaFilesStore, selectFile } from '../../src/lib/stores/mediaFiles';

   describe('mediaFilesStore', () => {
     it('initializes with empty items', () => {
       let state;
       mediaFilesStore.subscribe(s => { state = s; });
       expect(state.items).toEqual([]);
     });

     it('selectFile adds ID to selectedIds', () => {
       selectFile('file-123');
       let state;
       mediaFilesStore.subscribe(s => { state = s; });
       expect(state.selectedIds).toContain('file-123');
     });
   });
   ```

3. **Run tests and verify they pass:**
   ```bash
   npm run test
   ```

4. **Verify acceptance criteria:**
   - For each criterion in task-spec, verify the implementation satisfies it
   - Manual testing: navigate the app, test key workflows
   - Check for console errors or warnings

---

### Step 9: Final Verification

1. **Run full test suite:**
   ```bash
   npm run test
   ```
   - All tests must pass.
   - No errors, no warnings.

2. **Verify file structure matches frontend-design.file_structure:**
   - All specified directories exist
   - All specified files exist
   - No unexpected files

3. **Verify acceptance criteria are met:**
   - For each criterion in task-spec.acceptance_criteria, verify the implementation satisfies it
   - Document any unmet criteria (should be none)

4. **Check for TypeScript errors:**
   ```bash
   npm run check
   ```
   - No TypeScript errors or warnings

5. **Check for build errors:**
   ```bash
   npm run build
   ```
   - Build succeeds without errors

---

## Post-Execution

On successful completion:

```
✓ Frontend implementation complete for TSK-NNN.

Files created/modified:
  ✓ src/lib/types/media.ts (3 interfaces)
  ✓ src/lib/types/auth.ts (2 interfaces)
  ✓ src/lib/stores/mediaFiles.ts
  ✓ src/lib/stores/auth.ts
  ✓ src/lib/api/mediaFiles.ts (5 functions)
  ✓ src/lib/api/auth.ts (3 functions)
  ✓ src/lib/components/atomic/Button.svelte
  ✓ src/lib/components/atomic/TextField.svelte
  ✓ src/lib/components/layout/AppLayout.svelte
  ✓ src/lib/components/features/MediaGallery/Grid.svelte
  ✓ src/routes/+page.svelte
  ✓ src/routes/library/+page.svelte
  ✓ tests/ (N test files)

Tests:
  npm run test result: 24 passed, 0 failed

Build:
  npm run build: SUCCESS

Acceptance criteria verified:
  ✓ Users can upload media files
  ✓ Users can browse media gallery
  ✓ Users can delete media files
  ✓ All API calls include auth headers
  ✓ All async operations show loading/error states

Next: Deploy to production or proceed to next task phase
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `frontend-design.TSK-NNN.md` not found | Stop. Instruct agent: "Run /frontend-design first." |
| TypeScript compilation errors | Stop and report: "[list errors]". Agent must fix. |
| Test failures | Stop and report: "[list failed tests]". Agent must fix. |
| Missing prop typing | Stop and report: "[component] has untyped props". Agent must fix. |
| API call without auth header | Stop and report: "[function] missing auth header". Agent must fix. |
| Inline API calls in components | Stop and report: "[component] makes fetch directly". Refactor to API client. |

---

## References

- **input.template.yaml**: Schema for frontend-design input, task-spec, backend-design
- **output.template.yaml**: Contract showing what was implemented
- **rules.md**: Mandatory conventions (must enforce during implementation)

---

## Compatibility Notes

- **Framework:** Read `task-spec.execution_plan.tech_stack.frontend` to determine framework. This skill is optimized for **Svelte 5** but patterns apply to other frameworks (React, Vue, etc.).
- **Project setup:** Assumes SvelteKit (v2+) with TypeScript, Tailwind CSS, Vitest pre-configured.
- **API base:** Reads `VITE_API_BASE` environment variable; defaults to `http://localhost:3000`.
- **Auth:** Assumes JWT token in `authStore.token`; adjust for other auth methods.
