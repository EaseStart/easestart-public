---
description: EaseUI Elite Feature Development Workflow (Amazon, Stripe, Basecamp, Linear)
---

# EaseUI Feature Development Workflow

4-phase pipeline modeled after Amazon, Basecamp, Stripe, and Linear. Each phase produces a specific artifact, loads the right skills, and requires approval before advancing.

**Pipeline:** `Brainstorm → Plan → Document → Dev`

**Entry at any phase:** If earlier artifacts already exist, start at the next phase.

---

## Phase 1: BRAINSTORM → `brainstorm.md`

> **Trigger:** "brainstorm [feature]", "ideate", "explore", "shape"
> **Output:** `plans/specs/{feature-id}/brainstorm.md`
> **Gate:** User approves brainstorm before advancing to Phase 2.

### Load Context First
// turbo
```bash
brv query "{feature} EaseUI architecture"
```
- Read `prompt-engineer/SKILL.md` — optimize the problem framing
- Read `easeui-docs/SKILL.md` → check `docs/*/README.md` for any related existing features

### Actions
1. **Press Release (Amazon):** 1-2 paragraph hypothetical announcement. What problem is solved? Why should users be excited?
2. **User Stories:** *"As a [Persona], I want to [Action], so that [Benefit]."*
3. **MoSCoW Prioritization:** Must (P0) / Should (P1) / Could (P2) / Won't (backlog).
4. **Appetite & No-Gos (Basecamp):** Time budget + rabbit holes we will NOT build.
5. **World-Class Research Protocol** (replaces Deep-Thinking + Prior Art):

   > Source: Lucius neural propagation theory — hướng loang ban đầu quyết định chất lượng.
   > Mục tiêu: Đảm bảo AI research GỐC RỄ, không chỉ bề mặt.

   | Step | Action | Output |
   |------|--------|--------|
   | **① Benchmark** | Ai giải quyết vấn đề này tốt nhất? Tìm đỉnh (Figma, Linear, Stripe, v0...), không tìm trung bình | Best-in-class examples + cách họ giải quyết |
   | **② First Principles** | Bóc hết triệu chứng. Vấn đề GỐC RỄ là gì? World-class giải quyết gốc, không giải quyết bề mặt | Root problem statement (1 câu) |
   | **③ Proven Frameworks** | Mô hình tư duy / phương pháp luận đã thành công ở quy mô lớn? (McKinsey, Toyota, YC... tùy lĩnh vực) | Framework áp dụng + lý do chọn |
   | **④ Cross-Domain** | Ý tưởng xuất sắc thường đến từ ngành khác. Tìm giải pháp "chuyển dịch" từ lĩnh vực bên ngoài | 1+ cross-domain insight |
   | **⑤ Trade-offs** | Không có giải pháp hoàn hảo. Đang đánh đổi cái gì? Lựa chọn có chủ đích | Trade-off table (chọn X, mất Y, chấp nhận vì Z) |
   | **⑥ Executability** | Giải pháp brilliant mà không thực thi được = vô nghĩa. Điều chỉnh cho phù hợp nguồn lực, ràng buộc | Adjusted solution + constraints acknowledged |

### Anti-Patterns
- ❌ Don't jump to solutions — define the problem first (First Principles)
- ❌ Don't skip No-Gos — scope creep kills projects
- ❌ Don't brainstorm in a vacuum — query ByteRover for existing patterns
- ❌ Don't benchmark averages — find the BEST in the world, not the industry norm
- ❌ Don't ignore cross-domain — the best solution often comes from outside your field

---

## Phase 2: PLAN → `usecases.md`

> **Trigger:** "plan [feature]", "use cases", "define requirements"
> **Prerequisite:** `brainstorm.md` must exist. If not, run Phase 1 first.
> **Compliance Gate:** Run `python3 scripts/compliance_checker.py {feature-id} --phase 1` — must PASS before starting Phase 2.
> **Output:** `plans/specs/{feature-id}/usecases.md`
> **Gate:** User approves use cases before advancing to Phase 3.

### Load Skills
- Read `product-designer/SKILL.md` — apply **UX Psychology** (Hick's Law for navigation, Fitts' for CTAs, Miller's for grouping)
- Read `easeui-core-components/SKILL.md` — know what tokens, components, and animations already exist
- Read `product-designer/ux-psychology.md` — ground every decision in a UX law

### Actions
1. **Use Cases:** Define each UC with ID, title, actor, precondition, happy path, and edge cases.
2. **Acceptance Criteria (Gherkin):** For each Must UC: *Given [Context] → When [Action] → Then [Outcome].*
3. **Edge Cases & Error States:** Network drops, empty states, permissions denied, rate limits.
4. **UX Decisions Table:** Map every major decision to a UX law or Gestalt principle.
5. **Design System Check:** List which existing tokens/components from `easeui-core-components` apply. Flag any new tokens needed.
6. **Appetite Check (Shape Up):** For each UC, estimate effort vs value. Defer low-ROI items *before* Phase 3 specs them.
   ```
   | UC | Effort | Value | Ship this cycle? |
   |----|--------|-------|------------------|
   | UC-08 | High (cross-cutting) | Low (AI-only) | ❌ Defer |
   ```

### Anti-Patterns
- ❌ Don't plan only the happy path — the sad path IS the product quality
- ❌ Don't ignore existing components — check `component-catalog.ts` first
- ❌ "It looks nice" is never sufficient rationale — cite a UX law
- ❌ Don't spec UCs you know will be deferred — mark them in Appetite Check first

### Auto-Research Integration (autoresearch)

> 🔬 **Auto-trigger:** After brainstorm research produces new insights, consider feeding them into the knowledge base.

```
IF brainstorm revealed new frameworks/patterns/tools:
  → Feed into EaseStart CSVs via autoresearch loop
  → Run: python3 autoresearch/evaluate.py to verify quality
  → Log successful additions to autoresearch/results.tsv
```

---

## Phase 3: DOCUMENT → `blueprint.md` + `STATUS.md`

> **Trigger:** "document [feature]", "spec [feature]", "blueprint", "tech spec"
> **Prerequisite:** `usecases.md` must exist. If not, run Phase 2 first.
> **Compliance Gate:** Run `python3 scripts/compliance_checker.py {feature-id} --phase 2` — must PASS before starting Phase 3.
> **Output:** `plans/specs/{feature-id}/blueprint.md` + `STATUS.md` (created/updated)
> **Gate:** User approves blueprint before advancing to Phase 4.

### Load Skills
- Read `product-designer/SKILL.md` — apply UX psychology and spatial layout thinking for ASCII wireframes
- Read `easeui-docs/SKILL.md` → read `docs/*/README.md` for the feature area being modified
- Read `easeui-core-components/SKILL.md` — specify exact tokens (`var(--green)`, `.btn-primary`, `.streaming-border`)
- Read `dev-rules.md` workflow — coding standards for file structure, naming, TypeScript patterns
- **If feature has animations/micro-interactions:** Read `motionwind/SKILL.md` — specify animation classes in blueprint
- Reference `plans/templates/feature-implementation-template.md` for spec structure

### Actions
1. **Information Architecture:** Page/component hierarchy, navigation flow.
2. **ASCII Wireframes (MANDATORY for UI changes):** For every UC that adds or modifies UI, include an ASCII wireframe showing spatial layout, element placement, and interaction states. This is the single highest-value artifact for AI implementation fidelity.
   ```
   Example format:
   ┌─────────────────────────────────┐
   │  [🔍 Search...]  [Filter] [Sort]│
   │  ┌──────┐  ┌──────┐  ┌──────┐  │
   │  │ Card │  │ Card │  │ Card │  │
   │  └──────┘  └──────┘  └──────┘  │
   └─────────────────────────────────┘
   ```
   **Why:** AI tokenizes ASCII losslessly (~50 tokens) vs images (~1000+ tokens, lossy). ASCII wireframes are git-diffable, survive context truncation, and map directly to Tailwind layout classes.
3. **File Structure:** `[NEW]` and `[MOD]` files with full paths.
4. **Component API Contracts:** TypeScript interfaces, props, return types.
5. **State Management:** Zustand store slices, actions, selectors.
6. **Design Token Mapping:** Exact tokens from `easeui-core-components` for every visual element.
7. **Data Contracts:** Table aligning every shared field across all data sources. Prevents format mismatches.
   ```
   | Field | Source | Format | Example |
   |-------|--------|--------|---------|
   | phase | README.md | `P{n}` | `"P1"` |
   | phase | STATUS.md | `P{n}` (normalized) | `"P0"` |
   | status | STATUS.md | kebab-case enum | `"in-progress"` |
   ```
8. **Accessibility Plan:** WCAG requirements, keyboard nav, screen reader behavior.
9. **Create/Update STATUS.md:** YAML frontmatter (`status: specced`), UC checklist, key files table.

### Anti-Patterns
- ❌ Don't invent new design tokens — use what exists in `easeui-core-components`
- ❌ Don't write vague specs ("make it look good") — specify exact classes, shadows, radii
- ❌ Don't skip STATUS.md — PM Hub reads it directly
- ❌ Don't skip ASCII wireframes for UI changes — they are the #1 source of implementation accuracy

---

## Phase 4: DEV → Source Code

> **Trigger:** "build [feature]", "implement", "develop", "code"
> **Prerequisite:** `blueprint.md` must exist. If not, run Phase 3 first.
> **Compliance Gate:** Run `python3 scripts/compliance_checker.py {feature-id} --phase 3` — must PASS before starting Phase 4.
> **Output:** Working source code, verified and synced.

### Load Skills
- Read `design.md` workflow — full design orchestrator
- Read `easeui-core-components/SKILL.md` — build with real tokens
- Read `dap-debugging/SKILL.md` — interactive debugger for runtime issues
- Read `react-best-practices/SKILL.md` — React/Next.js performance: waterfalls, bundle size, rerenders
- **If feature has animations:** Read `motionwind/SKILL.md` + grep `motionwind/data/patterns.csv` for ready-made patterns
- **If building reusable components:** Read `storybook/SKILL.md` — CSF3 stories, interaction testing, portable stories
- Grep CSVs in `easeui-core-components/data/` for relevant patterns (UX guidelines, React performance, Next.js, accessibility)

### Execute (Linear Method)
1. **Atomic Tasks:** Break into clear, non-verbose items in `task.md`.
2. **Fixed Time, Variable Scope (Shape Up):** If stuck, cut scope to hit the primary objective.
3. **Code strictly** per the approved blueprint. Every color uses `var(--*)`, every shadow uses `var(--shadow-*)`.

### Debug Protocol (when bugs arise during dev)

> **Rule:** Print-debugging is the LAST resort. Use `dap` first.

| Situation | Action |
|-----------|--------|
| Runtime crash / wrong output | `dap debug <file> --break <file>:<line>` → inspect locals |
| Print-debug failed 2× | **Escalate to dap** — `dap debug --break-on-exception raised` |
| Complex data flow | `dap eval "<expr>" --frame N` — trace up the call stack |
| Loop / N+1 bug | `dap debug --break "file:line:condition"` — conditional breakpoint |
| Fix applied, need verify | `dap restart` — re-run with same breakpoints |
| Done debugging | `dap stop` — always cleanup |

### Confidence Protocol

Before advancing each gate, rate confidence 0-100%:

| Score | Action |
|-------|--------|
| ≥ 70% | Proceed autonomously — no notification |
| 40-69% | Notify human **once** with binary choice ("A or B? I recommend A"). Timeout 5 min → proceed with best guess |
| < 40% | Stop and wait — spec is unclear, needs human input |
| Same gate fails 2× | Auto-escalate regardless of score |

> ❌ **Anti-pattern:** Never ask open-ended "What should I do?" — always present binary choices with a recommendation.

### Verify (Stripe Quality Bar)
4. **Run `/review-gate` workflow** — deterministic checks + multi-pass AI review.
5. **Smoke Test Matrix:** Auto-generate from Gherkin acceptance criteria — one checkbox per UC's core assertion.
   ```
   - [ ] UC-05: Click P1 chip → only P1 features visible
   - [ ] UC-06: Sort by priority → P1 cards appear first
   - [ ] UC-07: Malform STATUS.md → ⚠️ badge on card
   ```
6. **Run 10-Point Design Audit** (creative gate) — must score ≥ 8/10.
7. **Test at breakpoints:** 375px, 768px, 1024px, 1440px.

### Post-Dev Compliance Audit (MANDATORY — HARD_GATE)

> 🔴 **After coding, BEFORE claiming complete. This is NOT optional.**

// turbo
```bash
python3 scripts/compliance_checker.py {feature-id} --full
```

If compliance_checker fails → FIX before proceeding. Log result:
// turbo
```bash
python3 scripts/telemetry.py log --type compliance_check --workflow feature-dev --details "{feature-id} full check"
```

### Auto-Fix Retry (Gates 2, 4, 5 only)

If a gate fails:
1. **Retry from original code** (not from the previous failed fix — prevents compounding errors).
2. **Re-run ALL gates** after each fix (prevents cascading regressions).
3. **Max 3 attempts.** After 3 failures → escalate to human with failure log.
4. Gate 3 (Visual Quality) is never auto-fixed — human always decides.

### PM Hub Sync (Mandatory — follow `/pm-hub-sync`)
8. Update `STATUS.md` — check off UCs, update status, add key files.
9. Update `plans/specs/README.md` — status icon and documents column.
10. `brv curate` with what was built.

---

## Quick Reference

| Phase | Trigger Words | Output | Skills Used | Gate |
|-------|--------------|--------|-------------|------|
| **1. Brainstorm** | brainstorm, ideate, shape, explore | `brainstorm.md` | prompt-engineer, easeui-docs, byterover | User approval |
| **2. Plan** | plan, use cases, requirements | `usecases.md` | product-designer, core-components, ux-psychology | User approval |
| **3. Document** | spec, blueprint, document, tech spec | `blueprint.md` + `STATUS.md` | easeui-docs, core-components, development-rules | User approval + Gate 1 |
| **4. Dev** | build, implement, develop, code | Source code | easeui-design, core-components, **dap-debugging**, **react-best-practices**, **motionwind** (if animations), **storybook** (if components), CSVs | `/review-gate` + Confidence Protocol + Debug Protocol |
