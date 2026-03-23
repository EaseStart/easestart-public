# trace2prompt — System Analysis (Categories 1-3)

> EaseStart Repo Research Skill — Phase 2: Deep Dive
> Repo: [thuanDaoSE/trace2prompt](https://github.com/thuanDaoSE/trace2prompt) | Go 67% + JS 20% + HTML 13% | MIT | 6 commits

---

## Category 1: System Boundaries & Core Value

### 1.1 What exact narrow technical problem does this codebase solve?

**Auto-collects E2E runtime context (Frontend → Backend → DB) and formats it into structured LLM prompts for AI-assisted debugging.**

The pain point: When devs ask AI to debug, they manually copy-paste fragmented logs from 3-4 different sources (browser console, backend terminal, DB logs). trace2prompt eliminates this friction by acting as an OTLP collector that stitches everything together.

**Evidence:** `main.go` — single entry point runs either OTLP HTTP server (port 4318) or MCP stdio server (`--mcp` flag).

### 1.2 Anti-goals (what is deliberately NOT handled)?

- ❌ **NOT a production monitoring tool** — no alerting, no dashboards, no historical retention
- ❌ **NOT a log aggregation system** — ring buffer of 2000 spans, then oldest are discarded
- ❌ **NOT a code analysis engine** — doesn't read source code, only runtime traces
- ❌ **NOT an AI itself** — generates prompts but doesn't call any LLM

**Evidence:** `const MaxBufferSize = 2000` in `main.go`, no external API calls in entire codebase.

### 1.3 Load limits & collapse thresholds

| Parameter | Value | Collapse Risk |
|-----------|-------|---------------|
| Span buffer | 2000 events (ring buffer) | Older traces silently lost after 2000 spans — no warning |
| Trace map | Unbounded `map[string]*TraceRecord` | 🔴 **Memory leak** — `traceMap` grows indefinitely, no eviction |
| System logs buffer | 20 entries | Very small window for background errors |
| Recent traces API | 100 entries (`MAX_RECENT_TRACES`) | Only latest 100 traces visible in Web UI |
| HTTP body | No size limit on `/v1/traces` endpoint | 🔴 **DoS risk** — large payloads fully read into memory |
| MCP buffer | 10MB max (`scanner.Buffer`) | Reasonable |

**Collapse scenario:** In a busy microservices setup with 50+ services, `traceMap` will grow without bound. After hours/days of continuous operation, RAM usage will climb until OOM. No garbage collection or TTL logic exists.

---

## Category 2: Data Architecture & State

### 2.1 Source of truth & consistency

**Fully in-memory, no persistence.** All state lives in:
- `spanBuffer []SpanRecord` — ring buffer, 2000 max
- `traceMap map[string]*TraceRecord` — unbounded map
- `systemLogsBuffer []string` — ring buffer, 20 max
- `latestMetrics` — single snapshot struct
- `latestPrompt string` — just the last generated prompt

**No consensus mechanism.** Single-process, single-threaded access via `sync.Mutex`. If process restarts, all data is lost.

### 2.2 Normalization vs denormalization

**Heavily denormalized.** `TraceRecord` contains flattened data from multiple spans: HTTP info, OS info, DB info, Java version, K8s pod name, Docker container ID, auth context, JWT claims — all stored as flat string fields.

**Evidence:** `TraceRecord` struct in `main.go` has 18+ fields, most redundantly extracted from span attributes.

### 2.3 Read vs write pattern

**Write-heavy design.** OTLP agents send spans continuously. Reads only happen on:
1. Web UI poll (`/v1/recent-traces`, `/v1/prompt`)
2. MCP call (`get_latest_trace`)

Read-to-write ratio approximately 1:100+. No indexing (sequential scan of `spanBuffer` with reverse iteration). Acceptable at 2000 buffer size, but would collapse at 100K+.

---

## Category 3: Execution Engine & Algorithms

### 3.1 State transitions & pipeline

```
OTel Agent → Proto deserialize → Span extraction → Attribute masking → Buffer insert
                                                                           ↓
                                                               Error detected? (HTTP 5xx)
                                                                           ↓
                                                               2s debounce → generateE2EPrompt()
                                                                           ↓
                                                               findBestTraceMatch() → Fuzzy match FE↔BE
                                                                           ↓
                                                               Build: Environment → Frontend Journey
                                                                     → Backend Logs → Exception → Flame Graph
                                                                           ↓
                                                               latestPrompt = result
```

**Most expensive bottleneck:** `generateE2EPrompt()` — locks mutex, scans entire `spanBuffer` (up to 2000 entries) with time-window matching (±10s), builds span tree, detects N+1 patterns. All under mutex lock.

### 3.2 Key algorithms

| Algorithm | Location | Description |
|-----------|----------|-------------|
| **Fuzzy TraceID matching** | `findBestTraceMatch()` | If TraceID not in `traceMap`, reverse-scan `spanBuffer` for URL match within ±3s window |
| **Frontend time-window** | `buildFrontendJourney()` | Collects spans within -2s to +10s of target trace timestamp |
| **N+1 detection** | `buildTreeStr()` | Sequential comparison of child spans — if consecutive children have identical SQL + name, flag as N+1 |
| **Sensitive data masking** | `maskSensitiveData()` | 4 regex patterns: token, email, SQL sensitive columns, signed URLs |
| **JWT auto-decode** | `extractJwtPayload()` | Base64 decode JWT payload part for AI context |
| **Stacktrace filtering** | `filterStacktrace()` | Keep first 3 lines + lines matching `ProjectNamespace`, collapse rest |
| **Truncated JSON repair** | `prettyJSONWithMarker()` | Count `{[` vs `}]` mismatches, auto-close brackets to pretty-print truncated JSON |

### 3.3 Optimistic assumptions & worst cases

| Assumption | Risk |
|------------|------|
| Frontend TraceID matches Backend TraceID | ✅ True when W3C trace context propagation works. ⚠️ Fails without proper CORS headers |
| Span buffer is sufficient at 2000 | ⚠️ High-throughput services can fill buffer in seconds, losing older context |
| `ProjectNamespace` is `com.coffeeshop` | 🔴 **Hardcoded** — stacktrace filter won't work for other projects |
| OTel agent sends data within 2s debounce | ⚠️ README says agent may delay 5s — race condition possible |
| Single prompt is sufficient | ⚠️ `latestPrompt` only keeps one — concurrent errors overwrite each other |

### 3.4 Concurrency model

**Mutex-based (lock-based).** Single `sync.Mutex` (`mu`) guards all shared state: `traceMap`, `spanBuffer`, `isDebouncing`, `latestPrompt`. Additionally `latestMetrics.mu` guards metrics.

**Deadlock risk:** Low — flat lock hierarchy (never nested except metrics inside trace lock). But **contention risk** is real: `generateE2EPrompt()` holds `mu` for entire prompt generation duration (scanning 2000+ spans under lock).

**Evidence:** `mu.Lock()` / `defer mu.Unlock()` at start of `generateE2EPrompt()`.
