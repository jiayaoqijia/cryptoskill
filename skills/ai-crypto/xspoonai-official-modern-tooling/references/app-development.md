---
name: app-development
description: Conventions for modern web application development using Vue/Nuxt and React/Next.js. Covers framework selection, component structure, and state management.
---

# App Development Standards

## Framework Selection

| Use Case               | Recommended Stack            |
| :--------------------- | :--------------------------- |
| **SPA / Client-only**  | Vite + Vue / React           |
| **SSR / SEO-critical** | Nuxt (Vue) / Next.js (React) |
| **Static Sites (SSG)** | Nuxt / Astro / Next.js       |
| **Documentation**      | VitePress / Starlight        |

## Vue Conventions

| Convention           | Preference                                   |
| :------------------- | :------------------------------------------- |
| **Syntax**           | `<script setup lang="ts">`                   |
| **Reactivity**       | Prefer `ref()` over `reactive()` for clarity |
| **State Management** | Pinia (avoid Vuex)                           |
| **Styling**          | UnoCSS / Tailwind CSS                        |
| **Utilities**        | VueUse                                       |

### Component Structure (Vue)

```vue
<script setup lang="ts">
interface Props {
  title: string;
  count?: number;
}

interface Emits {
  (e: "update", value: number): void;
  (e: "close"): void;
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
});

const emit = defineEmits<Emits>();
</script>

<template>
  <div class="p-4">
    <h1>{{ title }}</h1>
    <button @click="emit('update', count + 1)">Count: {{ count }}</button>
  </div>
</template>
```

## React Conventions

| Convention           | Preference                                                  |
| :------------------- | :---------------------------------------------------------- |
| **Components**       | Functional Components with Hooks                            |
| **State Management** | Zustand / TanStack Query (Server State)                     |
| **Styling**          | Tailwind CSS / CSS Modules                                  |
| **Routing**          | React Router / TanStack Router (SPA), File-system (Next.js) |

### Component Structure (React)

```tsx
interface Props {
  title: string;
  count?: number;
  onUpdate: (value: number) => void;
  onClose: () => void;
}

export function Counter({ title, count = 0, onUpdate }: Props) {
  return (
    <div className="p-4">
      <h1>{title}</h1>
      <button onClick={() => onUpdate(count + 1)}>Count: {count}</button>
    </div>
  );
}
```

## General Best Practices

- **Composables/Hooks**: Extract logic into reusable functions (`useCounter`, `useFetch`).
- **Type Safety**: Use TypeScript for all props, state, and API responses.
- **Directory Structure**:
  - `components/`: UI components
  - `composables/` or `hooks/`: Reusable logic
  - `pages/`: Route components
  - `utils/`: Helper functions
  - `types/`: Shared type definitions
