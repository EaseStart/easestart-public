# trace2prompt — Research Summary

> **Repo:** [thuanDaoSE/trace2prompt](https://github.com/thuanDaoSE/trace2prompt) | Go + JS | MIT | 6 commits
> **Research date:** 2026-03-18
> **Researcher:** AI Agent (EaseStart repo-research skill)

---

## One-Sentence Summary

Go daemon that auto-collects E2E OpenTelemetry traces (Frontend clicks → HTTP → Backend SQL/logs) and generates structured LLM prompts for AI-assisted debugging.

## Key Findings

| Category | Finding | Impact |
|----------|---------|--------|
| Core Value | Solves "AI is blind to runtime context" — zero-config trace collection | 🟢 High |
| Data Architecture | All in-memory, no persistence, `traceMap` leaks unboundedly | 🟡 Medium risk |
| Algorithms | Fuzzy TraceID matching (±3s), N+1 SQL detection, auto-sensitive-data-redaction | 🟢 Excellent |
| Security | Privacy-first: JWT claims only, cookie keys only, 4-regex masking | 🟢 Excellent |
| Dependencies | Minimal (only OTel pdata library) | 🟢 Excellent |
| Maturity | 6 commits, 1 contributor, hardcoded namespace | 🔴 Low |

## Applicable Patterns

| # | Pattern | Score | Action |
|---|---------|-------|--------|
| 1 | Structured 6-section runtime context prompt template | **P0** | Create `runtime-context-template.md` |
| 2 | Sensitive data auto-redaction protocol | **P1** | Create `sensitive-data-redaction.md` |
| 3 | N+1 query detection heuristic | **P1** | Update debugging checklist |
| 4 | E2E trace stitching via time-window | P2 | Document as best practice |
| 5 | MCP tool for AI-IDE integration | P2 | Inspire future MCP server |
| 6 | Bilingual prompt dictionary | P3 | Archive |

## Anti-Patterns to Avoid

- Unbounded map growth (no TTL/eviction)
- No input size limits on HTTP endpoints
- Hardcoded project namespace in stacktrace filter
- Single mutex for all shared state (contention risk)
- Silent error handling on proto deserialization

## Next Steps

1. ✅ Implement P0: Create runtime context prompt template for debugging skill
2. ✅ Implement P1: Create sensitive data redaction reference
3. ✅ Implement P1: Add N+1 detection heuristic to debugging checklist
4. ⏸️ Consider forking trace2prompt with configurable namespace if team adopts OTel

## Files

- [system_analysis.md](./system_analysis.md) — Categories 1-3 technical deep-dive
- [architecture_review.md](./architecture_review.md) — Categories 4-6 trade-offs & security
- [integration_brief.md](./integration_brief.md) — Pattern extraction & integration proposals
