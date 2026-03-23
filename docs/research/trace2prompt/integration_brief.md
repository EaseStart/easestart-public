# trace2prompt — Integration Brief

> EaseStart Repo Research Skill — Phase 3 (Extract) + Phase 4 (Integrate)

---

## Extracted Patterns

### Pattern 1: Structured Prompt Template for Runtime Context

**What:** trace2prompt uses a fixed 6-section prompt format that gives AI maximum context:
1. Environment & Infrastructure (OS, runtime, DB, CPU/RAM)
2. HTTP Request Context (method, URL, status, auth)
3. Frontend Journey (clicks, API calls, console logs, crashes)
4. Backend Logs (INFO/WARN before error)
5. Exception Stacktrace (filtered, framework calls hidden)
6. Flame Graph (execution tree with timing + SQL)

**Why it works:** AI performs dramatically better with structured, labeled context than raw log dumps. The template acts as a "contract" between the tool and the LLM.

**Applicability:** **P0 — Direct Apply**

**EaseStart impact:** Create a `debug-context-template` in the agent skills that structures runtime context in a similar format. Even without trace2prompt running, the AI agent can use this template to ask developers for the right information in the right format. This is a **prompt engineering pattern**, not a tool dependency.

**Proposed file:** `.agent/skills/debugging/references/runtime-context-template.md`

---

### Pattern 2: Sensitive Data Auto-Redaction Protocol

**What:** 4-layer regex masking before any data reaches the prompt:
1. Bearer tokens, API keys → `[REDACTED]`
2. Emails → `[EMAIL_HIDDEN]`
3. SQL password/secret columns → `[REDACTED]`
4. AWS/GCP signed URLs → `[SIGNED_PARAMS_HIDDEN]`

Plus cookie value stripping and JWT payload-only extraction.

**Applicability:** **P1 — Adapt & Apply**

**EaseStart impact:** When AI agents collect debug context (logs, error traces), they should auto-strip sensitive data before including it in prompts. Create a `sensitive-data-protocol` reference that agent skills can follow.

**Proposed file:** `.agent/skills/debugging/references/sensitive-data-redaction.md`

---

### Pattern 3: E2E Trace Stitching via Time-Window Fuzzy Matching

**What:** When TraceID doesn't match across frontend/backend, use URL + timestamp matching (±3s window) to correlate. Frontend events within -2s to +10s of the target trace are included as context.

**Applicability:** **P2 — Inspire Only**

This is tool-level logic (Go code), not directly applicable to agent skills. But the *concept* — "look at what happened 10 seconds before the error" — is a powerful debugging heuristic that could be documented as a best practice.

---

### Pattern 4: N+1 Query Detection via Consecutive Span Comparison

**What:** When building the flame graph tree, if consecutive child spans have identical SQL + name, flag as N+1 query.

**Applicability:** **P1 — Adapt & Apply**

This heuristic can be documented as a debugging checklist item: "When reviewing SQL traces, check for identical queries appearing consecutively — this indicates N+1 problem."

**Proposed file:** Update `.agent/skills/debugging/references/systematic-debugging.md` checklist

---

### Pattern 5: MCP Tool for AI-IDE Integration

**What:** Simple MCP server with single tool (`get_latest_trace`) that fetches the latest error context. Zero-config for AI IDE users.

**Applicability:** **P2 — Inspire Only**

Interesting pattern for future EaseStart MCP server — but requires trace2prompt to be running. Not directly applicable to the skill system.

---

### Pattern 6: Bilingual Prompt Dictionary

**What:** All prompt strings stored in a `PromptDict` struct with EN/VI variants. Language selected via `--lang` flag.

**Applicability:** **P3 — Archive**

Interesting i18n approach but not relevant to EaseStart's English-first agent system.

---

## Anti-Patterns Discovered

| Anti-Pattern | Description | EaseStart Should Avoid |
|-------------|-------------|----------------------|
| Unbounded map growth | `traceMap` never evicts — memory leak | ✅ Always use TTL or LRU for caches |
| No input size limits | `io.ReadAll(r.Body)` with no cap | ✅ Always limit input sizes |
| Hardcoded namespace | `ProjectNamespace = "com.coffeeshop"` | ✅ Always make configs configurable |
| Silent error handling | Proto unmarshal error ignored in trace handler | ✅ Always log or handle errors |
| Single mutex for all state | Contention under load | ✅ Use fine-grained locking |

---

## Integration Proposals

### P0: Runtime Context Prompt Template (Direct Apply)

**Target:** `.agent/skills/debugging/references/runtime-context-template.md` [NEW]

Create a structured template that the debugging skill uses when collecting runtime context. Based on trace2prompt's 6-section format:

```markdown
## Runtime Context Collection Template

When debugging, collect and structure the following information:

### 1. Environment
- Service name, OS, runtime version, database type
- CPU/RAM at time of error (if available)

### 2. HTTP Context
- Method, URL, status code
- Auth present? (don't include actual tokens)

### 3. User Journey (last 10 seconds before error)
- What did the user click/navigate?
- What API calls preceded this one?

### 4. Relevant Logs
- INFO/WARN logs printed before the error
- System background errors (if any)

### 5. Exception Details
- Full stacktrace (filtered to project code only)
- Error message and type

### 6. Execution Flow
- What queries/services were called?
- Execution timing for each step
- Any N+1 patterns? (same query repeated consecutively)
```

### P1: Sensitive Data Redaction Reference (Adapt & Apply)

**Target:** `.agent/skills/debugging/references/sensitive-data-redaction.md` [NEW]

Document the categories of sensitive data to strip before including in AI prompts:
- Bearer tokens, API keys, passwords
- Email addresses, PII
- SQL injection vectors
- Signed cloud URLs (AWS, GCP presigned)
- Cookie values (keep names only)
- JWT: include claims, remove signature

### P1: N+1 Detection Heuristic (Adapt & Apply)

**Target:** Update `.agent/skills/debugging/SKILL.md` — add to Phase 2 (Isolate) checklist

Add: "When reviewing DB queries or API calls, check for identical operations appearing consecutively — this indicates N+1 problem."

---

## Decision

```
✅ P0 patterns found → Create runtime-context-template.md
✅ P1 patterns found → Create sensitive-data-redaction.md + update debugging checklist
```

**Action:** Implement P0 + P1 patterns into the debugging skill. No need to fork or run trace2prompt — we extract the **knowledge patterns**, not the tool.
