---
name: clean-code
description: "Pragmatic coding standards — concise, direct, no over-engineering, no unnecessary comments. THINK FIRST before editing."
---

# Clean Code — EaseUI Standards

> Be **concise, direct, solution-focused**. The user wants working code, not a programming lesson.

## 🔴 THINK FIRST Before Editing

| Question | Why |
|----------|-----|
| What imports this file? | They might break |
| What does this file import? | Interface changes |
| What tests cover this? | Tests might fail |
| Is this shared? | Multiple places affected |

> Edit the file + all dependent files in the SAME task. Never leave broken imports.

## EaseUI Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Comment every line | Self-documenting code |
| Helper for one-liner | Inline it |
| utils.ts with 1 function | Put code where used |
| Deep nesting | Guard clauses + early returns |
| Magic numbers | Named constants |
| God functions (100+ lines) | Split by responsibility |

## 🔴 Component Reuse Protocol (MANDATORY)

Before creating ANY new component:
1. Check `easeui-core-components` → Component Registry table
2. Search existing: `find app/src/components -name "*keyword*"`
3. If it exists → **reuse it**. If similar exists → **extend it**
4. Only create new if confirmed absent from both checks

> Never reinvent: Tooltip, Toast, Skeleton, CopyButton, EmptyState, ErrorBoundary, or any component in the registry.

## Self-Check Before Completing

- ✅ Did I do exactly what user asked?
- ✅ Did I modify all necessary files?
- ✅ Does TypeScript compile?
- ✅ Any edge cases missed?
- ✅ No broken imports?

## Done Condition

Code compiles + all dependent files updated + self-check passed + user's request fulfilled exactly
