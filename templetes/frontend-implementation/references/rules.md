# Frontend-Implementation Skill: Mandatory Rules

These rules are immutable enforcement constraints for the frontend-implementation skill. Violations should halt execution and report errors to the operator.

---

## 1. Never Overwrite Existing Files Without Frontend-Design Intent

### Rule 1.1: File Overwrite Protection
- Do NOT modify files that exist in `project_root/` unless they are:
  - Listed in `frontend-design.file_structure` (approved for creation/modification)
  - Part of the Svelte/Next/Vue framework boilerplate (e.g., `svelte.config.js`, `vite.config.ts`)
  - Utility/helper files explicitly required by the design (e.g., `src/lib/utils.ts`)
- If an existing file is not in `frontend-design.file_structure`, **ask the operator for confirmation before modifying**.

### Rule 1.2: Preserve User Code
- Do NOT delete or modify code in files outside the scope of this task.
- If a file contains both generated code and user code:
  - Preserve the user code
  - Integrate new code carefully (e.g., append exports, add new functions)
  - Document any changes

### Rule 1.3: Verification Before Overwrite
- If a file exists and is marked for modification in frontend-design:
  - Read the file first to understand its current state
  - Preserve any existing logic/styles
  - Merge new code with existing code (do not replace wholesale)

---

## 2. TypeScript Interfaces Must Match Backend Schemas Exactly

### Rule 2.1: Field Name Correspondence
- Every field in a TypeScript interface must match the backend schema (from `backend-design.schemas`) **exactly** (case-sensitive).
- Do NOT rename backend fields to "more convenient" names.
  - **Bad:** Backend has `owner_id`, you rename it to `ownerId` in the interface.
  - **Good:** Backend has `owner_id`, interface field is exactly `owner_id` (preserve snake_case if that's what backend uses).

### Rule 2.2: Type Compatibility
- TypeScript types must be compatible with the JSON types from the backend:
  - Backend `string` → TypeScript `string`
  - Backend `number` → TypeScript `number`
  - Backend `boolean` → TypeScript `boolean`
  - Backend `null` → TypeScript `null | <type>` (optional field)
  - Backend `array` → TypeScript `<type>[]`
  - Backend `object` → TypeScript `interface` or `Record<string, unknown>`

### Rule 2.3: Date Handling
- If backend returns ISO 8601 date strings (e.g., `"2024-02-21T10:30:00Z"`):
  - Interface field type: `string` (not `Date`)
  - In components: parse to `new Date(dateString)` when needed
  - Never assume automatic Date parsing from JSON

### Rule 2.4: Null/Undefined Fields
- If a field can be null in the response:
  - Interface field: `fieldName: TypeOrNull | null`
- If a field can be missing entirely:
  - Interface field: `fieldName?: Type` (optional)
- Do NOT use `any` to handle optional/nullable fields.

---

## 3. All Stores Must Be Typed

### Rule 3.1: Store Type Definition
- Every store must declare its state type explicitly:
  ```typescript
  import { writable } from 'svelte/store';
  import type { MediaFilesState } from '../types';

  export const mediaFilesStore = writable<MediaFilesState>(initialState);
  ```
- Do NOT use untyped stores: `writable({})` (no generic type).

### Rule 3.2: State Interface
- Define a TypeScript interface for each store's state:
  ```typescript
  interface MediaFilesState {
    items: MediaFile[];
    loading: boolean;
    error: string | null;
    selectedIds: string[];
  }
  ```
- All fields must be typed; no `any` fields.

### Rule 3.3: Initial State
- Provide concrete initial values matching the interface:
  ```typescript
  const initialState: MediaFilesState = {
    items: [],
    loading: false,
    error: null,
    selectedIds: []
  };
  ```
- Never use `null` or `undefined` for fields that should have defaults.

### Rule 3.4: Export Everything Explicitly
- Export stores and all action functions:
  ```typescript
  export const mediaFilesStore = writable<MediaFilesState>(...);
  export async function fetchFiles() { ... }
  export function selectFile(id: string) { ... }
  ```
- Do NOT use `export default`.

---

## 4. API Client: All Fetch Calls Must Be in `src/lib/api/`

### Rule 4.1: Centralized API Calls
- Do NOT make `fetch()` or `axios()` calls anywhere except `src/lib/api/*.ts`.
- Components must call API client functions, not make HTTP requests directly.
- Stores must call API client functions (and then update their own state).

### Rule 4.2: API Function Exports
- Export async functions from `src/lib/api/`:
  ```typescript
  // src/lib/api/mediaFiles.ts
  export async function fetchMediaFiles(): Promise<MediaFile[]> { ... }
  export async function uploadFile(file: File): Promise<MediaFile> { ... }
  export async function deleteFile(id: string): Promise<void> { ... }
  ```
- Function names must match `function_name` in `frontend-design.api_integration`.

### Rule 4.3: Authorization Headers
- For endpoints requiring authentication (`auth_required: true`):
  - Read auth token from store: `const token = get(authStore).token`
  - Include Authorization header in fetch:
    ```typescript
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
    ```
- For public endpoints: omit Authorization header.

### Rule 4.4: Error Handling
- Always throw descriptive Error objects:
  ```typescript
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  ```
- Do NOT return error objects; throw them.
- Do NOT suppress errors silently.

### Rule 4.5: Base URL Configuration
- Read API base URL from environment variable:
  ```typescript
  const API_BASE = process.env.VITE_API_BASE || 'http://localhost:3000';
  ```
- Never hardcode URLs like `http://localhost:3000`.

---

## 5. Component Implementation Order

### Rule 5.1: Bottom-Up Implementation
- Implement in this order (dependencies first):
  1. **TypeScript types** (`src/lib/types/`)
  2. **Stores** (`src/lib/stores/`)
  3. **API client** (`src/lib/api/`)
  4. **Atomic components** (`src/lib/components/atomic/`)
  5. **Feature components** (`src/lib/components/features/`)
  6. **Layout components** (`src/lib/components/layout/`)
  7. **Page components** (`src/routes/`)

### Rule 5.2: Why Bottom-Up?
- Atomic components don't depend on others.
- Feature components depend on atomic components.
- Layout components depend on feature/atomic.
- Page components depend on everything.
- This order ensures no circular dependencies and each layer can be tested independently.

---

## 6. TypeScript in Every Svelte Component

### Rule 6.1: `<script lang="ts">` Mandatory
- Every `.svelte` file must declare:
  ```svelte
  <script lang="ts">
    // TypeScript code here
  </script>
  ```
- Do NOT use `<script>` (JavaScript-only).

### Rule 6.2: Typed Props
- Define a `Props` interface:
  ```typescript
  interface Props {
    label: string;
    disabled?: boolean;
    size?: 'sm' | 'md' | 'lg';
  }
  ```
- Assign to component variables:
  ```typescript
  let { label, disabled = false, size = 'md' }: Props = $props();
  ```

### Rule 6.3: No `any` in Components
- Do NOT use `any` for:
  - Props
  - Local variables (infer or type explicitly)
  - Store values (import the state interface)
  - Event handlers (use proper event types)

### Rule 6.4: Event Types
- Dispatch typed events:
  ```typescript
  const dispatch = createEventDispatcher<{ id: string }>();
  dispatch('select', { id: 'file-123' });
  ```
- Parent component receives typed event:
  ```svelte
  on:select={(e) => { const id = e.detail.id; }}
  ```

---

## 7. Loading States: Mandatory for Every API Call

### Rule 7.1: Three-State Pattern
Every component with async operations must show:
1. **Loading:** Spinner, skeleton, or disabled button
2. **Error:** Error message (user-friendly, not stack trace)
3. **Success:** Actual content

### Rule 7.2: Implementation Pattern
```typescript
let loading = false;
let error: string | null = null;

async function fetchData() {
  loading = true;
  error = null;
  try {
    const data = await api.fetch();
    // update component/store state
  } catch (err) {
    error = err instanceof Error ? err.message : 'An unknown error occurred';
  } finally {
    loading = false;
  }
}
```

### Rule 7.3: UI Reflection
```svelte
{#if loading}
  <Skeleton />
{:else if error}
  <ErrorMessage message={error} />
{:else}
  <Content data={data} />
{/if}
```

### Rule 7.4: Disable Interactions
- During loading, disable submit buttons, file inputs, etc.:
  ```svelte
  <Button label="Upload" on:click={handleUpload} disabled={loading} />
  ```

---

## 8. Anti-Patterns: Do NOT Do This

### Rule 8.1: No Inline Fetch in Components
**WRONG:**
```svelte
<script lang="ts">
  onMount(async () => {
    const res = await fetch('/api/files');
    files = await res.json();
  });
</script>
```

**RIGHT:**
```svelte
<script lang="ts">
  import * as api from '../../api/mediaFiles';

  onMount(async () => {
    files = await api.fetchMediaFiles();
  });
</script>
```

### Rule 8.2: No Untyped Stores
**WRONG:**
```typescript
export const store = writable({});  // No type!
```

**RIGHT:**
```typescript
export const store = writable<StoreState>(initialState);
```

### Rule 8.3: No Global Mutable Objects
**WRONG:**
```typescript
let globalState = { files: [] };  // Not a store, no reactivity!
```

**RIGHT:**
```typescript
export const filesStore = writable<FilesState>({ files: [] });
```

### Rule 8.4: No `any` Types
**WRONG:**
```typescript
interface Props {
  data: any;  // Cop-out!
}
```

**RIGHT:**
```typescript
interface Props {
  data: MediaFile[];  // Explicit type!
}
```

### Rule 8.5: No Custom CSS Unless Necessary
**WRONG:**
```svelte
<div style="color: blue; padding: 10px;">...</div>
<style>
  .custom { border: 2px solid red; }
</style>
```

**RIGHT:**
```svelte
<div class="text-blue-600 p-2 border-2 border-red-600">...</div>
```
Use TailwindCSS utility classes; avoid `<style>` blocks unless absolutely necessary (e.g., complex animations).

### Rule 8.6: No Business Logic in Atomic Components
**WRONG:**
```svelte
<!-- Button.svelte -->
<script lang="ts">
  async function handleClick() {
    const res = await fetch('/api/data');
    const data = await res.json();
    globalStore.update(s => ({ ...s, data }));
  }
</script>
<button on:click={handleClick}>Click Me</button>
```

**RIGHT:**
```svelte
<!-- Button.svelte -->
<script lang="ts">
  interface Props {
    label: string;
    onClick?: () => void;
  }
  let { label, onClick }: Props = $props();
</script>
<button on:click={onClick}>{label}</button>
```
Business logic belongs in feature/page components or stores.

---

## 9. Testing Requirements

### Rule 9.1: Test Coverage
- At minimum, test:
  - **Atomic components:** Rendering, props, events, disabled states
  - **Feature components:** Data loading, store integration, error handling, event dispatch
  - **Stores:** Action execution, state updates, derived values
  - **API client:** Correct endpoint call, proper headers, error handling

### Rule 9.2: Test Organization
```
tests/
  components/
    atomic/
      Button.test.ts
      TextField.test.ts
    features/
      MediaGrid.test.ts
      UploadModal.test.ts
  stores/
    mediaFiles.test.ts
    auth.test.ts
  api/
    mediaFiles.test.ts
```

### Rule 9.3: Test Framework
- Use **Vitest** (test runner) + **Svelte Testing Library** (component testing)
- Mock fetch/API calls using `vi.mock()` or MSW (Mock Service Worker)

### Rule 9.4: All Tests Must Pass
- Run `npm run test` before completion
- No skipped tests (no `test.skip()` or `describe.skip()`)
- No pending tests (all tests must verify real behavior)

---

## 10. Build and Deployment Validation

### Rule 10.1: TypeScript Compilation
- Run `npm run check` (or `tsc --noEmit`) before completion.
- No TypeScript errors or warnings.
- Strict mode must be enabled: `"strict": true` in `tsconfig.json`.

### Rule 10.2: Build Success
- Run `npm run build` before completion.
- Build must succeed without warnings.
- No console errors during build.

### Rule 10.3: Production Readiness
- All source maps should be optional (for debugging, not production).
- Minification should be enabled.
- Environment variables should be read at runtime (not hardcoded).

---

## Validation Checklist

Before marking implementation as complete, verify:

- [ ] All files in `frontend-design.file_structure` are created
- [ ] No files outside the design spec are modified
- [ ] All TypeScript types match backend schemas (field names, types)
- [ ] All stores are typed with interfaces
- [ ] All API calls are in `src/lib/api/`
- [ ] All auth-required endpoints include Authorization headers
- [ ] Every async operation in components has loading + error states
- [ ] All components have `<script lang="ts">`
- [ ] No `any` types anywhere
- [ ] TailwindCSS is used for styling (minimal/no custom CSS)
- [ ] All tests pass (`npm run test`)
- [ ] TypeScript check passes (`npm run check`)
- [ ] Build succeeds (`npm run build`)
- [ ] Acceptance criteria are met (manual verification)
- [ ] No circular dependencies between modules
- [ ] API base URL is from environment variable, not hardcoded
- [ ] Error messages are user-friendly (not stack traces)

---

## Summary

**Core enforcement:**
1. **File safety:** Never overwrite files outside the design spec
2. **Type safety:** TypeScript everywhere, match backend schemas exactly
3. **API isolation:** All fetch calls in `src/lib/api/`
4. **Store typing:** Every store has a TypeScript interface
5. **Async safety:** Loading + error states for every API call
6. **Testing:** All tests pass, minimum coverage on critical paths
7. **Build success:** TypeScript, build, and tests all pass

Violations of these rules should halt execution and report errors. The agent must not proceed with incomplete or invalid code.
