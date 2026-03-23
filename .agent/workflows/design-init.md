---
description: Initialize or refresh a project's design system — extracts tokens, inventories components, generates guidelines, sets up Storybook
---

# /design-init {project}

> Run once on project init or when design changes significantly. Creates AI-readable design context + interactive Storybook catalog.

## Prerequisites
- Project must have a CSS file with design tokens (globals.css or equivalent)
- Project must have a `components/` directory
- `.project-agent.md` must exist in project root

---

## Phase 1: EXTRACT — Tokens from CSS

1. **Find the project's main CSS file:**
   - Check `.project-agent.md` for CSS source path
   - Common locations: `app/globals.css`, `src/app/globals.css`

2. **Read the CSS file and extract into `{project}/design-system/tokens.json`:**

   Extract these categories:
   ```
   color:      @theme color tokens, :root CSS custom properties, semantic colors
   typography: font families, font sizes + line heights, font weights, font features
   shadow:     all shadow tokens (rest, hover, elevated, modal, glow)
   radius:     all border-radius tokens
   animation:  easing curves, keyframe names + durations, CSS classes
   effects:    glassmorphism definitions, gradients, overlays, scrollbar styles
   spacing:    section padding, grid values (if defined)
   ```

   Format: Style Dictionary compatible JSON (see `sodeal/design-system/tokens.json` for reference)

---

## Phase 2: INVENTORY — Components from codebase

3. **Scan all `.tsx` files in `{project}/components/` (or `{project}/src/components/`):**
   ```bash
   find {project}/components -name "*.tsx" | sort
   ```

4. **Generate `{project}/design-system/component-registry.md`:**
   - Group by directory (ui/, layout/, landing/, feature/, etc.)
   - For each component: name, file path, purpose (1 sentence)
   - Add "⚠️ Reuse Rules" section at the bottom
   - Note any icon components separately

---

## Phase 3: ANALYZE — Guidelines from patterns

5. **Analyze CSS patterns and generate `{project}/design-system/design-guidelines.md`:**
   - **Brand Identity** table (primary color, palette, material metaphor, personality)
   - **Color Usage** table (token → hex → when to use → when NOT)
   - **Typography** (font pairing, weights, usage)
   - **Shadow system** (level → token → usage)
   - **Animation Patterns** (animation → duration → class → use case)
   - **Established Patterns** (cards, hover, focus, loading, etc.)
   - **❌ Anti-Patterns** table (don't → do instead)

---

## Phase 4: STORYBOOK — Interactive component catalog

> 🔴 **MANDATORY.** Every project MUST have a Storybook instance.
> Load `@[skills/storybook]` before executing this phase. Read `configuration.md` for setup details.

### 4a. Init Storybook (if not exists)

6. **Run the init script:**
   ```bash
   python .agent/skills/storybook/scripts/storybook_init.py {project}
   ```
   This auto-detects CSS path, creates `.storybook/main.ts` + `preview.tsx`, sets up directory structure.

7. **Install dependencies:**
   ```bash
   cd {project}
   npm install -D @storybook/nextjs-vite @storybook/addon-docs storybook-design-token
   npm install -D @storybook/react @storybook/test
   npm install
   ```

   > Uses `@storybook/nextjs-vite` framework (Vite-powered, NOT Webpack).

### 4b. Generate stories for UI components

8. **Run the story generator (dry-run first to preview):**
   ```bash
   python .agent/skills/storybook/scripts/story_generator.py {project} --dry-run
   python .agent/skills/storybook/scripts/story_generator.py {project}
   ```

9. **Review and enhance generated stories:**
   - Add `play` functions for interactive components (buttons, forms, modals)
   - Add variants for different states (loading, error, disabled)
   - Customize argTypes for better Storybook controls
   - See `@[skills/storybook]/story-patterns.md` for CSF3 patterns

   **Priority rules:**
   - P0: UI primitives (Button, Modal, Input) — ALL variants + interaction tests
   - P1: Forms (empty → filled → error → success states)
   - P1: Layout shells (wrapper stories with slot content)
   - P2: Icons (single gallery story)
   - P2: Feature components (key states + edge cases)

### 4c. Verify Storybook runs

10. **Start Storybook and verify:**
    ```bash
    cd {project}
    npm run storybook
    ```
    - Confirm all stories render correctly
    - Confirm Tailwind styles are applied
    - Confirm design tokens are visible in token addon

11. **Run the audit script:**
    ```bash
    python .agent/skills/storybook/scripts/storybook_audit.py {project}
    ```
    - Target: ≥80% coverage for UI primitives
    - All stories should use CSF3 object format
    - No CSF2 function format warnings

### 4d. Testing integration (optional)

12. **Set up Vitest portable stories (if project uses Vitest):**
    - See `@[skills/storybook]/testing-integration.md` for setup
    - Install: `npm install -D vitest vite-plugin-storybook-nextjs`
    - Stories with `play` functions can be reused as unit tests via `composeStories`

13. **Run story tests:**
    ```bash
    npx storybook test          # built-in interaction + a11y tests
    npx storybook test --watch  # watch mode
    ```

---

## Phase 5: SYNC — Update project config

12. **Update `{project}/.project-agent.md` Design System section:**
    ```markdown
    ## Design System

    **Tokens:** [`design-system/tokens.json`](design-system/tokens.json) — {brief description}
    **Components:** [`design-system/component-registry.md`](design-system/component-registry.md) — {N} components across {M} categories
    **Guidelines:** [`design-system/design-guidelines.md`](design-system/design-guidelines.md) — {brief description}
    **Storybook:** `npm run storybook` → `localhost:6006` — interactive component catalog
    **CSS Source:** `{css-path}` — raw CSS source of truth

    > 🔴 **MANDATORY:** Read `design-system/` BEFORE any design work. Never guess tokens.
    ```

13. **ByteRover sync (if available):**
    ```bash
    brv curate "{project} design system extracted — tokens, components, guidelines, storybook"
    ```

---

## Phase 6: VERIFY

14. **Confirm all files exist:**
    ```bash
    ls -la {project}/design-system/tokens.json \
           {project}/design-system/component-registry.md \
           {project}/design-system/design-guidelines.md \
           {project}/.storybook/main.ts \
           {project}/.storybook/preview.ts
    ```

15. **Spot-check:** Read tokens.json and verify colors match actual CSS values.

16. **Storybook smoke test:** Run `npm run storybook` and verify at least 1 story renders.

---

## Refresh Mode

To refresh an existing design system after CSS/component changes:

```
/design-init {project}
```

- **Tokens changed:** Overwrite `tokens.json`
- **Components added/removed:** Overwrite `component-registry.md`, generate new stories
- **Guidelines changed:** Overwrite `design-guidelines.md`
- **Storybook exists:** Only add stories for new components

---

## Output Summary

| File | Purpose | Format |
|------|---------|--------|
| `tokens.json` | Machine-readable design tokens | JSON (Style Dictionary compatible) |
| `component-registry.md` | Complete component inventory | Markdown tables |
| `design-guidelines.md` | Visual language + anti-patterns | Markdown |
| `.storybook/` | Storybook configuration | TypeScript config |
| `stories/` | Interactive component stories | TSX (Storybook format) |

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Extract | CSS → design tokens | `design-tokens.json` | All tokens categorized |
| **2** Inventory | Codebase → component list | `component-inventory.md` | All UI components found |
| **3** Analyze | Patterns → guidelines | `design-guidelines.md` | Guidelines cover all patterns |
| **4** Storybook | Interactive catalog | Running Storybook instance | All components have stories |
| **5** Sync | Update project config | Updated configs | Configs reference tokens |
| **6** Verify | End-to-end validation | Verification report | All stories render correctly |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All 6 phases pass + Storybook runs | → Design system ready |
| **MEDIUM** | Storybook partial (some stories fail) | → Binary: A) Ship with gaps, B) Fix broken stories |
| **LOW** | Token extraction incomplete or CSS too complex | → Stop, manual token mapping needed |

### Anti-Patterns
- ❌ Skipping token extraction and hardcoding values
- ❌ Generating stories without testing they render
- ❌ Inventory missing components that exist in the codebase
- ❌ Not running Storybook verification (Phase 6) before delivery
