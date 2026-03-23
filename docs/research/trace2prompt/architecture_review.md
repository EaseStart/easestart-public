# trace2prompt — Architecture Review (Categories 4-6)

> EaseStart Repo Research Skill — Phase 2: Deep Dive
> Repo: [thuanDaoSE/trace2prompt](https://github.com/thuanDaoSE/trace2prompt)

---

## Category 4: Architecture Decisions & Trade-offs

### 4.1 CAP sacrifice

**Sacrifices Durability & Consistency for Performance.**

- No persistence — all data in-memory, lost on restart
- No replication — single instance only
- Optimized for ultra-low latency ingestion (Go + direct memory)
- Trade-off is explicit: this is a dev tool, not production infrastructure

### 4.2 Critical dependencies

| Dependency | Role | Single Point of Failure? |
|------------|------|-------------------------|
| `go.opentelemetry.io/collector/pdata` | OTLP proto deserialization | 🔴 Yes — entire trace ingestion depends on this |
| Go stdlib (`net/http`, `encoding/json`) | HTTP server, JSON | ✅ Stable |
| `embed` (Go 1.16+) | Static file bundling | ✅ Stable |

**Minimal dependency surface** — only 1 external dependency (OTel pdata library). Excellent for a dev tool. No database, no message queue, no external services.

---

## Category 5: Communication Boundaries & Integration

### 5.1 Sync vs async, backpressure

| Flow | Type | Backpressure Handling |
|------|------|----------------------|
| OTLP /v1/traces | **Sync HTTP** | ❌ None — `io.ReadAll(r.Body)` with no size limit |
| OTLP /v1/logs | **Sync HTTP** | ❌ Same issue |
| OTLP /v1/metrics | **Sync HTTP** | ❌ Same issue |
| /v1/frontend-spans | **Sync HTTP** (JSON) | ❌ No rate limiting |
| Prompt generation | **Async goroutine** (2s debounce) | ✅ Debounce prevents flood |
| MCP server | **Sync stdio** (blocking scanner) | ✅ One request at a time |

**Critical gap:** No backpressure anywhere except debounce on prompt generation. A misconfigured OTel agent sending bursts could overwhelm the server. In practice, this is acceptable for local dev use but would fail in shared environments.

### 5.2 API exposure of internal structures

**Moderate risk.** The `/v1/prompt` endpoint returns raw text (not JSON), which is good for LLM consumption but:
- `/v1/recent-traces` returns `TraceSummary` struct directly — internal field names exposed (`traceId`, `hasError`)
- MCP tool response wraps in standard MCP format — clean

Internal `SpanRecord`, `TraceRecord`, `SpanNode` structures are NOT exposed in APIs — properly bounded.

### 5.3 Memory leak & cleanup

| Resource | Cleanup? |
|----------|----------|
| `spanBuffer` | ✅ Ring buffer — oldest auto-evicted at 2000 |
| `traceMap` | 🔴 **NO cleanup** — grows forever |
| `systemLogsBuffer` | ✅ Ring buffer — 20 max |
| `latestPrompt` | ✅ Overwritten on each new error |
| HTTP connections | ✅ Go stdlib handles connection pooling |
| Goroutines | ✅ `triggerE2EPromptCreation` goroutines are short-lived (2s + processing) |

**The `traceMap` leak is the biggest architectural concern.** A simple TTL or LRU cache would fix it. Each `TraceRecord` can hold many `SpanNode` pointers, so this grows with both trace count AND span complexity.

---

## Category 6: Security & Resilience

### 6.1 Input validation & sanitization

| Input | Validation | Risk |
|-------|-----------|------|
| OTLP trace proto | ✅ `ptraceotlp.UnmarshalProto` validates structure | Low |
| OTLP log proto | ✅ Same | Low |
| Frontend JSON spans | ⚠️ `json.Decoder` but no schema validation | Medium — malformed spans accepted |
| Query string (`?traceId=`) | ❌ No validation | Low impact (used as map key) |
| Request body size | 🔴 No limit (`io.ReadAll`) | High — memory exhaustion via large payload |

**Sensitive data handling is excellent:**
- 4 regex patterns auto-redact: Bearer tokens, emails, SQL passwords, signed URLs
- Cookie values stripped (only keys kept)
- JWT payload decoded but secrets don't leak (only claims shown)
- `[REDACTED_SECRET]` for any attribute with sensitive key names

### 6.2 Credential management

**Privacy-first approach — well implemented:**
- `extractCookieKeys()` — only returns key names, discards values
- `extractJwtPayload()` — decodes claims but never exposes the full token
- `maskSensitiveData()` — regex-based, runs on all text before prompt generation
- `maskSQLQuery()` — specifically targets SQL columns named password/secret/token
- `signedUrlRegex` — strips AWS/GCP signed URL parameters

**Log leak risk:** Low — all prompt output passes through masking. Server console logs show TraceIDs and span names only, no payload data.

### 6.3 Failure resilience

| Failure | Behavior |
|---------|----------|
| Backend OTel agent disconnects | ✅ Frontend-only mode — warns in prompt |
| Frontend script not loaded | ✅ Backend-only mode — no crash |
| Proto deserialization fails | ⚠️ Silent — `req.UnmarshalProto(body)` error not checked in trace handler |
| MCP server can't reach HTTP API | ✅ Returns helpful error message |
| Port 4318/4319 already in use | 🔴 Fatal crash (`log.Fatal`) |

No circuit breaker, no retry, no graceful degradation beyond the above. Acceptable for a local dev tool.

### 6.4 Crash recovery

**No WAL, no persistence, no crash recovery.** All state lost on restart. This is by design — the tool is ephemeral.

Notably, `triggerE2EPromptCreation` uses a goroutine with fixed 2s delay, so if the process crashes mid-generation, no corruption occurs (nothing to corrupt — it's all in memory).
