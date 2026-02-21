# Frontend-Design Skill: Mandatory Rules

These rules are immutable and must be enforced during frontend-design execution. Violations should trigger validation errors and halt completion.

---

## 1. Component Naming and Organization

### Rule 1.1: Naming Conventions
- **Component files:** PascalCase (e.g., `MediaGrid.svelte`, `FileUploadModal.svelte`)
- **Store files:** camelCase (e.g., `mediaFilesStore.ts`, `authStore.ts`)
- **API client files:** camelCase (e.g., `mediaFiles.ts`, `auth.ts`)
- **Directory names:** camelCase (e.g., `src/lib/components/features/mediaGallery/`)

### Rule 1.2: Component File Structure
```
src/
  routes/                          # SvelteKit pages (one per route)
    +page.svelte
    [id]/+page.svelte
  lib/
    components/
      layout/                      # Shared layout components
        AppLayout.svelte
        AuthLayout.svelte
      features/                    # Feature-specific components
        mediaGallery/
          Grid.svelte
          DetailModal.svelte
      atomic/                      # Primitive, reusable components
        Button.svelte
        TextField.svelte
        Modal.svelte
    stores/                        # Svelte stores
      mediaFiles.ts
      auth.ts
    api/                           # API client functions
      mediaFiles.ts
      auth.ts
    types/                         # TypeScript interfaces
      media.ts
      auth.ts
```

### Rule 1.3: One Component, One Responsibility
- Each component must have a single, well-defined purpose.
- Do NOT combine layout + feature logic in one component.
- Do NOT put business logic (API calls, state mutations) in atomic components.

---

## 2. Page and Route Design

### Rule 2.1: One Top-Level Page Component Per Route
- Every SvelteKit route must have exactly one `+page.svelte` file.
- This page component is the entry point for that route.
- It may contain nested child components but must orchestrate them.

### Rule 2.2: Page Component Responsibility
- Load page-level data (via `load` function or `onMount`)
- Manage page-level state (which store values apply to this page?)
- Orchestrate layout and feature components
- Handle page-level error/loading states

### Rule 2.3: Layout Wrapping
- Every page must be wrapped in a layout component (AppLayout, AuthLayout, etc.).
- Use SvelteKit's `+layout.svelte` files for shared layout logic.
- Do NOT hardcode layout in every page component.

### Rule 2.4: Route Naming
- Routes must reflect the user-visible navigation structure.
- Use SvelteKit conventions:
  - `/` → home page
  - `/library` → library page
  - `/library/[id]` → dynamic library item detail
  - `/upload/[...steps]` → multi-step flow with optional nested routes

---

## 3. Shared Component Library

### Rule 3.1: Shared Components Must Be in `src/lib/components/`
- Components imported by multiple pages or used across the app must live in `src/lib/components/`.
- Page-specific components can be co-located in `src/routes/[page]/` if truly unique to that page.
- Prefer centralization in `src/lib/components/` unless there is strong reason for co-location.

### Rule 3.2: Atomic Components Are NOT Business-Logic Components
- Atomic components (Button, TextField, Modal, etc.) must be presentation-only.
- No API calls, no store mutations, no custom hooks that fetch data.
- All props must be simple primitives, enums, or interfaces (no functions for complex behavior).

### Rule 3.3: Props Must Be Typed
- Every prop must have an explicit TypeScript type.
- Do NOT use `any` type for component props.
- Use interfaces for complex prop objects:
  ```typescript
  interface MediaGridProps {
    items: MediaFile[];
    selectedId: string | null;
    isLoading: boolean;
  }
  ```

---

## 4. State Management (Stores)

### Rule 4.1: One Store Per Domain Concept
- **Good:** `authStore`, `mediaFilesStore`, `purchasesStore`, `uiStateStore`
- **Bad:** `globalStore` (too broad), `appStore` (vague), one store per component
- Domain concepts: Auth, MediaFiles, Purchases, UiState, Notifications, etc.

### Rule 4.2: Store Typing
- All stores must be typed with TypeScript interfaces.
- Use `writable<StateInterface>(initialState)` or `readable<StateInterface>(initialState)`.
- Define the state interface explicitly in the store file or imported from `src/lib/types/`.

### Rule 4.3: Store Naming and File Locations
- Store name: camelCase ending in "Store" (e.g., `mediaFilesStore`)
- File: `src/lib/stores/{storeName}.ts` → `src/lib/stores/mediaFiles.ts`
- Export the store as a named export: `export const mediaFilesStore = writable<...>(...)`

### Rule 4.4: Store Responsibilities
- Store holds domain state (data, loading flag, error messages).
- Store exports actions (functions) to update state.
- Store does NOT directly make API calls (API calls live in `src/lib/api/` and update the store).
- Store does NOT directly manipulate the DOM.

### Rule 4.5: Derived Stores for Computed State
- If a value is derived from multiple store values, use `derived()`:
  ```typescript
  export const selectedCount$ = derived(mediaFilesStore, $store => $store.selected.length);
  ```
- Do NOT duplicate derived data in the base store state.

---

## 5. API Client and Integration

### Rule 5.1: All API Calls Must Be in `src/lib/api/`
- Do NOT make fetch/axios calls inline in components.
- Do NOT make API calls in stores.
- Create API client functions in `src/lib/api/{domain}.ts`:
  ```typescript
  export async function fetchMediaFiles(): Promise<MediaFile[]> { ... }
  export async function uploadFile(file: File): Promise<MediaFile> { ... }
  ```

### Rule 5.2: API Functions Must Be Async
- Export async functions that return Promises.
- Use `await` for fetch/axios operations.
- Throw typed Error objects with meaningful messages on failure.

### Rule 5.3: Request and Response Types
- Define TypeScript interfaces for every API request body and response.
- Match field names exactly with backend schemas (from backend-design).
- Include all optional/required field markers:
  ```typescript
  interface UploadFileRequest {
    filename: string;
    mimetype: string;
    size: number;
  }

  interface MediaFile {
    id: string;
    filename: string;
    uploadedAt: Date;
    owner_id: string;
  }
  ```

### Rule 5.4: Authorization Headers
- For endpoints requiring authentication, include Authorization header:
  ```typescript
  const headers = { Authorization: `Bearer ${$authStore.token}` };
  ```
- Read auth token from `authStore` (or appropriate auth store).
- Never hardcode tokens in the client.

### Rule 5.5: Loading and Error State Handling
- Every component that calls an API must manage loading and error states.
- Component must show:
  - Skeleton/spinner during loading
  - Error message on failure (including user-friendly text)
  - Success content on completion
- Never display bare error objects to the user.

---

## 6. TypeScript Usage

### Rule 6.1: All Components Must Use `<script lang="ts">`
- Every Svelte component must declare `<script lang="ts">`.
- Do NOT use `<script>` (non-TypeScript) in Svelte files.

### Rule 6.2: Typed Component Props
- Define a TypeScript interface for all component props:
  ```typescript
  interface Props {
    items: MediaFile[];
    selectedId: string | null;
    isLoading: boolean;
  }
  let { items = [], selectedId = null, isLoading = false }: Props = $props();
  ```
- Or use the newer Svelte 5 syntax with explicit typing.

### Rule 6.3: No `any` Type
- Do NOT use `any` in function signatures, prop definitions, or store state.
- If type is truly flexible, use a union type or `unknown` (which is safer).
- Use `type-safe-store` patterns (store interfaces, not `any`).

### Rule 6.4: Interfaces for API Types
- Store all API types in `src/lib/types/` as TypeScript interfaces.
- Import types from `src/lib/types/` into stores, API client, and components.
- Do NOT define the same type in multiple places.

---

## 7. Loading and Error States

### Rule 7.1: Mandatory For Every API Call
- Every component that initiates an API call must have:
  - `loading` state (boolean or from store)
  - `error` state (string or Error object, for display to user)
- Set `loading = true` before fetch, unset in `finally` block.

### Rule 7.2: User-Friendly Error Messages
- Do NOT show raw error objects or backend stack traces.
- Transform errors into user-friendly messages:
  ```typescript
  catch (err) {
    error = (err instanceof Error) ? err.message : "An unknown error occurred";
  }
  ```

### Rule 7.3: Disable Interactions During Loading
- Disable submit buttons, file uploads, etc. while `loading = true`.
- Show loading spinner or skeleton while loading.
- Show error message if an error occurred.

---

## 8. Anti-Patterns: Do NOT Do This

### Rule 8.1: Do NOT Fetch Directly in Components
**Bad:**
```typescript
onMount(async () => {
  const res = await fetch('/api/files');
  files = await res.json();
});
```

**Good:**
```typescript
onMount(async () => {
  files = await mediaFilesStore.fetchFiles();
});
```

### Rule 8.2: Do NOT Use Global Mutable Objects Instead of Stores
**Bad:**
```typescript
let globalState = { files: [] };  // No reactivity, not a store!
```

**Good:**
```typescript
export const mediaFilesStore = writable<MediaFilesState>({ files: [] });
```

### Rule 8.3: Do NOT Mix Business Logic and UI in One Component
**Bad:**
```typescript
// Component that does everything: API calls, state management, rendering
export default function MediaGrid() {
  async function fetchAndSort() { ... }
  async function uploadFile(file) { ... }
  return <Grid ... />
}
```

**Good:**
```typescript
// Component: just renders
// Store: manages state and actions
// API: handles HTTP calls
```

### Rule 8.4: Do NOT Use `<style>` Blocks for Core Styling
- Use TailwindCSS utility classes for all styling.
- Do NOT use `<style>` blocks unless TailwindCSS is insufficient (e.g., complex animations).
- Prefer TailwindCSS consistency over custom CSS.

### Rule 8.5: Do NOT Hardcode API Endpoints in Components
**Bad:**
```typescript
const res = await fetch('http://localhost:3000/api/files');
```

**Good:**
```typescript
// Define endpoint in API client (src/lib/api/mediaFiles.ts)
// Reuse the function from the client
```

### Rule 8.6: Do NOT Put Complex Logic in Templates
- Keep templates (HTML) simple and data-driven.
- Move computed values to stores or component script.
- Use derived stores for filtering, sorting, mapping.

---

## 9. Validation Checklist

Before marking the design as complete, verify:

- [ ] All pages in `scope_included` have a corresponding route and page component
- [ ] All user interactions have a clear component responsible for handling them
- [ ] Every API endpoint from backend-design (or api_contract_overview) has an integration plan
- [ ] Every API integration has loading and error state handling
- [ ] All stores follow the naming/structure rules
- [ ] All component props are typed with TypeScript interfaces
- [ ] File structure matches the rules (atomic/feature/layout organization)
- [ ] Test strategy covers at least: rendering, props, events, store actions, API error handling
- [ ] No component has `any` types
- [ ] No API calls are defined outside `src/lib/api/`
- [ ] All authentication-required endpoints have Authorization header in the plan
- [ ] UI/UX interaction patterns are explicitly documented for complex interactions

---

## 10. Framework-Specific Adjustments

These rules assume **Svelte 5** as the frontend framework. If another framework is used (React, Vue, Angular), adapt as follows:

| Rule | Svelte | React | Vue |
|------|--------|-------|-----|
| **Stores** | Svelte stores (writable, derived) | Redux, Zustand, or Context API | Vuex, Pinia |
| **Reactive bindings** | `$store` syntax | useState hook | ref/reactive |
| **Component syntax** | `.svelte` files | `.jsx/.tsx` files | `.vue` files |
| **Styling** | TailwindCSS + optional `<style>` | Tailwind + CSS-in-JS | Tailwind + scoped `<style>` |
| **Load data** | onMount, SvelteKit load | useEffect, React loaders | onMounted, async setup |
| **Emit events** | dispatch() | callback props | emit() |

Always read `task-spec.execution_plan.tech_stack.frontend` to determine the actual framework.

---

## Summary

**Core principles:**
1. **One component, one responsibility** — clear separation of concerns
2. **Typed everything** — TypeScript all the way (no `any`)
3. **Centralized API client** — all HTTP calls in `src/lib/api/`
4. **Stores for shared state** — not global objects, not component props drilling
5. **Loading + error states** — mandatory for every async operation
6. **TailwindCSS first** — prefer utility classes over custom CSS
7. **Testability** — design components to be easily testable (dependency injection via props/stores)

Enforcing these rules ensures the frontend design is maintainable, scalable, and ready for autonomous implementation.
