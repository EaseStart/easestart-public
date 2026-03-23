---
description: EaseUI design workflow — orchestrates product-designer, easeui-core-components, and ux-psychology skills for all UI/UX work
---

# EaseUI Design Workflow

Streamlined 4-step workflow for all UI/UX work within EaseUI. This workflow is the orchestrator — it delegates to the project's tailored skills rather than duplicating rules.

## When to Use

- Designing new components, pages, or features for EaseUI
- Reviewing/fixing existing UI for design system compliance
- Building prototypes or mockups within the EaseUI editor
- Any `/ui-ux-pro-max` slash command

---

## Step 1: Load Context

// turbo
```bash
brv query "EaseUI design system tokens components"
```

Then read these skills in order:

1. **`easeui-core-components/SKILL.md`** — EaseUI's actual tokens, components, animations
2. **`product-designer/SKILL.md`** — Design thinking, UX psychology, quality standards
3. **`easeui-docs/SKILL.md`** → read relevant `docs/*/README.md` if modifying an existing feature

> 🔴 **Never design from memory.** Always load tokens first. Every color, shadow, radius, and animation class is documented.

---

## Step 2: Analyze the Work

Classify the request:

| Type | Approach |
|------|----------|
| **New component** | Check `component-catalog.ts` for existing wireframes. Follow Component Specimen rules from product-designer |
| **New page/feature** | Read the feature's `plans/specs/*/brainstorm.md` first. Run Deep Design Thinking Protocol |
| **UI fix/review** | Run `python3 scripts/ux_audit.py` + `accessibility_checker.py` against the target |
| **Design system work** | Reference `docs/design-systems/README.md` for extraction/generation architecture |

**Stack:** EaseUI is **Next.js 15 + Tailwind CSS v4 + TypeScript**. No other stacks apply.

---

## Step 3: Design (Creative Phase)

Before writing any code:

1. **Run the Deep Design Thinking Protocol** (product-designer § Deep Design Thinking)
   - What emotion? What's the #1 focal point? What material metaphor?

2. **Apply UX Psychology** (product-designer § UX Psychology Reference)
   - Which UX laws apply? (Hick's for navigation, Fitts' for CTAs, Miller's for grouping)
   - Which Gestalt principles drive the layout?

3. **Run the Anti-Template Protocol** — reject generic patterns

4. **Score against the 10-Point Design Audit** (DESIGN PHASE gate)
   - Must score ≥ 8/10 before writing code

**EaseUI-specific constraints:**
- Use tokens from `easeui-core-components` — `--green`, `--blue`, `--shadow-toolbar`, etc.
- Buttons: `.btn-primary` / `.btn-secondary` / `.btn-red` / `.btn-ghost` — never custom
- Animations: use established patterns (`.page-transition`, `.reveal-*`, `.streaming-border`)
- Typography: Inter only, 7 sizes from `.text-xs` to `.text-3xl`
- Easing: `0.4s cubic-bezier(0.16, 1, 0.3, 1)` for page transitions

---

## Step 4: Deliver (Code Phase)

After implementation:

1. **Run the Pre-Delivery Checklist** (product-designer § Pre-Delivery Checklist)
   - Visual quality, accessibility, interaction, light/dark mode, layout

2. **Verify design system compliance:**
   - [ ] All colors use CSS custom properties (`var(--green)`) or Tailwind tokens
   - [ ] All shadows use `var(--shadow-*)` tokens
   - [ ] All radii use `var(--radius-*)` tokens
   - [ ] Animations use established keyframe patterns from globals.css
   - [ ] No invented values — everything traces back to `easeui-core-components`

3. **Test at breakpoints:** 375px, 768px, 1024px, 1440px

4. **Update knowledge:**
// turbo
```bash
brv curate "implemented [component/page name] using EaseUI design tokens" -f path/to/file
```
---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Context | Load design system + requirements | Design brief | Requirements clear |
| **2** Analyze | Study existing patterns + user flows | Analysis notes | Understand current state |
| **3** Design | Creative exploration + mockups | Design deliverable (HTML/Figma) | CEO review (HARD_GATE) |
| **4** Deliver | Code + documentation | Production-ready code + docs | Tests pass + accessible |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Design system tokens used + responsive + accessible | → Ship code |
| **MEDIUM** | Design works but accessibility or edge cases uncertain | → Binary: A) Ship with known gaps, B) Fix gaps first |
| **LOW** | Design direction unclear or conflicting requirements | → Stop, return to Socratic gate |

### Anti-Patterns
- ❌ Designing without loading existing design system tokens
- ❌ Skipping accessibility check (contrast, keyboard nav, screen readers)
- ❌ Building custom components when design system has existing ones
- ❌ Delivering designs without responsive breakpoints
