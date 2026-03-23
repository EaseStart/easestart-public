# EaseStart — Hướng Dẫn Sử Dụng Chi Tiết

> Bạn là CEO. Bạn có ý tưởng. Bạn muốn biến nó thành sản phẩm.
> Clone EaseStart, mở AI IDE, và bắt đầu hỏi — 13 chuyên gia sẵn sàng thực thi cho bạn.

---

## Mục Lục

1. [Bạn Cần Gì Trước Khi Bắt Đầu?](#1-bạn-cần-gì-trước-khi-bắt-đầu)
2. [Cài Đặt (2 Phút)](#2-cài-đặt-2-phút)
3. [Hiểu Cách EaseStart Hoạt Động](#3-hiểu-cách-easestart-hoạt-động)
4. [Ngày Đầu Tiên — "Tôi Có Ý Tưởng"](#4-ngày-đầu-tiên--tôi-có-ý-tưởng)
5. [Tuần Đầu — Validate Ý Tưởng](#5-tuần-đầu--validate-ý-tưởng)
6. [Tháng Đầu — Build MVP](#6-tháng-đầu--build-mvp)
7. [Sau 3 Tháng — Tìm PMF](#7-sau-3-tháng--tìm-pmf)
8. [Sau 6 Tháng — Growth](#8-sau-6-tháng--growth)
9. [Embedded Tools — Công Cụ Tích Hợp](#9-embedded-tools--công-cụ-tích-hợp)
10. [Quản Lý Dự Án Hàng Ngày](#10-quản-lý-dự-án-hàng-ngày)
11. [FAQ — Hỏi & Đáp](#11-faq--hỏi--đáp)
12. [Cheat Sheet — Tất Cả Lệnh](#12-cheat-sheet--tất-cả-lệnh)

---

## 1. Bạn Cần Gì Trước Khi Bắt Đầu?

### Kỹ năng

| Cần | Không cần |
|-----|-----------|
| Biết dùng terminal cơ bản | Biết code |
| Biết tiếng Anh đọc hiểu | Kinh nghiệm startup |
| Có ý tưởng hoặc vấn đề muốn giải quyết | Tiền |

### Phần mềm

| Bắt buộc | Khuyên dùng |
|----------|-------------|
| Python 3.9+ (đã có sẵn trên macOS/Linux) | Một AI IDE (xem bảng dưới) |
| Git | VS Code (miễn phí) |
| Terminal (Terminal.app, iTerm2, Warp...) | |

### AI IDE — Chọn một trong các công cụ sau

EaseStart hoạt động **bên trong AI coding IDE** của bạn. Clone repo, mở IDE, và agents tự load.

| AI IDE | Cách setup | Ghi chú |
|--------|-----------|--------|
| **Antigravity** | Mở folder `easestart/` → agents tự load qua `.agent/` | Recommended — full agent support |
| **Claude Code** | Mở folder `easestart/` → agents tự load qua `.agent/` | Full support |
| **Gemini CLI** | Mở folder `easestart/` → GEMINI.md + `.agent/` tự config | Full support |
| **Cursor** | `python3 cli/main.py init` → MCP server tự cài | MCP integration |
| **Windsurf** | `python3 cli/main.py init` → MCP server tự cài | MCP integration |
| **Open Code** | Mở folder `easestart/` → agents tự load | Community support |

### Tâm thế

EaseStart không viết code cho bạn. EaseStart biến AI IDE của bạn thành **đội ngũ 13 chuyên gia AI** — mỗi agent là một chuyên gia trong một lĩnh vực. Bạn là CEO, bạn ra quyết định, agents thực thi.

---

## 2. Cài Đặt (2 Phút)

### Bước 1: Clone repo

```bash
git clone https://github.com/EaseStart/easestart.git
cd easestart
```

### Bước 2: Kiểm tra hệ thống

```bash
python3 scripts/search.py "hello"
# Nếu thấy kết quả → bạn sẵn sàng. Không cần pip install gì.
```

### Bước 3 (Tùy chọn): Cài đặt công cụ mở rộng

```bash
# Chỉ cài khi bạn cần — core hoạt động không cần gì cả
pip install -r requirements-tools.txt
```

| Tool | Cần cài khi... | Dung lượng |
|------|----------------|------------|
| `chromadb + sentence-transformers` | Bạn muốn search thông minh hơn (hiểu nghĩa, không chỉ từ khóa) | ~200MB |
| `flask` | Bạn muốn xem dashboard trực quan | ~2MB |
| `weasyprint` | Bạn muốn xuất báo cáo PDF | ~10MB |

### Bước 4: Mở AI IDE

**Antigravity / Claude Code / Gemini CLI / Open Code:**
```bash
# Chỉ cần mở folder easestart/ trong IDE — agents tự load
cd easestart
# Mở IDE tại folder này
```

**Cursor / Windsurf:**
```bash
python3 cli/main.py init
# Auto-detects IDE → cài MCP server → agents sẵn sàng
```

Sau bước này, bạn có thể **nói chuyện trực tiếp** với agents trong IDE. Hỏi bất cứ gì — orchestrator tự route đến đúng chuyên gia.

---

## 3. Hiểu Cách EaseStart Hoạt Động

### Mô hình 7 giai đoạn

Mỗi startup đi qua 7 giai đoạn. EaseStart biết bạn đang ở đâu và chỉ đưa ra lời khuyên phù hợp với giai đoạn đó.

```
Stage 0: Pre-Idea      → "Tôi muốn khởi nghiệp nhưng chưa có ý tưởng"
Stage 1: Ideation       → "Tôi có ý tưởng, cần đánh giá nó"
Stage 2: Validation     → "Tôi cần xác nhận người dùng thực sự cần sản phẩm này"
Stage 3: MVP            → "Tôi cần build phiên bản đầu tiên"
Stage 4: Product-Market Fit → "Tôi có người dùng, cần tìm PMF"
Stage 5: Growth         → "PMF đạt, cần scale"
Stage 6: Scale          → "Cần team, vốn, quy trình"
```

### 13 chuyên gia (Agents)

Bạn không nói chuyện với "1 AI". Bạn có đội ngũ 13 chuyên gia:

| Khi bạn hỏi về... | Agent trả lời |
|-------------------|---------------|
| "Nên làm sản phẩm gì?" | 💡 ideation-agent |
| "Làm sao biết người dùng cần?" | 🔍 validation-agent |
| "Dùng tech gì để build?" | 🔨 mvp-agent |
| "Định giá bao nhiêu?" | 📈 growth-agent |
| "Cần gọi vốn không?" | 💰 fundraising-agent |
| "Cần thuê AI hay cần tuyển người?" | ⚙️ ops-agent |
| "Nên tìm co-founder không?" | 👥 cofounder-agent |
| "Cần đăng ký công ty chưa?" | ⚖️ legal-agent |
| "Tôi burn out quá" | 🧘 wellness-agent |
| "Marketing bắt đầu từ đâu?" | 📢 marketing-agent |
| "Quản lý tài chính thế nào?" | 💵 finance-agent |
| "Hôm nay cần làm gì?" | 📋 pm-agent |

**Orchestrator** tự động route câu hỏi đến đúng agent. Bạn không cần chọn.

### Kho kiến thức 554 dòng

Mỗi lời khuyên đều có nguồn — không phải AI bịa ra. Kiến thức được curate từ:
- Y Combinator, Paul Graham, First Round Capital
- Lean Startup, Jobs-to-be-Done, Shape Up
- Case studies: Stripe, Basecamp, Linear, Figma, Notion
- 30 ngành công nghiệp khác nhau

---

## 4. Ngày Đầu Tiên — "Tôi Có Ý Tưởng"

### Kịch bản: Bạn muốn build một app quản lý chi tiêu cho Gen Z

#### Bước 1: Hỏi EaseStart về ý tưởng

```bash
python3 scripts/search.py "personal finance app for Gen Z"
```

**Kết quả:** EaseStart trả về frameworks, tools, và case studies liên quan.

#### Bước 2: Kiểm tra ngành

```bash
python3 scripts/search.py "fintech personal finance" --domain industries
```

**Kết quả:** FinTech industry data — TAM, stage challenges, revenue models, example companies.

#### Bước 3: Bắt đầu Lean Canvas (trong AI IDE)

Mở AI IDE (Antigravity / Claude Code / Gemini CLI / Cursor / Windsurf) và nói:

```
Tôi muốn build một app quản lý chi tiêu cho Gen Z tại Việt Nam.
Giúp tôi tạo Lean Canvas và đánh giá ý tưởng này.
```

**ideation-agent** sẽ:
1. Hỏi bạn 5 câu hỏi Socratic để hiểu rõ vấn đề
2. Tạo Lean Canvas v1
3. Cho điểm ý tưởng (Idea Score) dựa trên 5 tiêu chí
4. Đề xuất counter-positioning (cách khác biệt với Momo, VNPAY)

#### Bước 4: So sánh với startup tương tự

```bash
python3 scripts/search.py "fintech startup case study" --domain casestudies
```

### ⚠️ Sai lầm phổ biến ở Stage 0-1

```bash
python3 scripts/search.py "common mistakes ideation stage" --domain playbook
```

EaseStart sẽ cảnh báo bạn:
- ❌ Build trước khi validate (Premature Building)
- ❌ Giải quyết vấn đề của người khác, không phải của mình
- ❌ Bỏ qua đối thủ "đủ tốt" (Good Enough Competitors)

---

## 5. Tuần Đầu — Validate Ý Tưởng

### Kịch bản: Bạn cần nói chuyện với khách hàng tiềm năng

#### Bước 1: Lấy template phỏng vấn

```bash
python3 scripts/search.py "customer interview script" --domain templates
```

**Kết quả:** Mom Test interview template — cách hỏi để khách hàng nói thật, không nói cho bạn vui.

#### Bước 2: Học cách phỏng vấn đúng

```bash
python3 scripts/search.py "Mom Test interview how to validate" --domain frameworks
```

**Kết quả:** Mom Test framework — 3 quy tắc:
1. Hỏi về cuộc sống của họ, không phải ý tưởng của bạn
2. Hỏi về quá khứ cụ thể, không phải tương lai giả định
3. Ít nói hơn, nghe nhiều hơn

#### Bước 3: Sau 10 cuộc phỏng vấn — đo PMF

Trong AI IDE:

```
Tôi đã phỏng vấn 12 người. Đây là kết quả:
- 8/12 nói vấn đề quản lý chi tiêu là "rất khó chịu"
- 5/12 đang dùng Excel
- 3/12 dùng app nhưng bỏ sau 1 tuần
Giúp tôi đánh giá PMF score.
```

**validation-agent** sẽ:
1. Tính Sean Ellis Score (% "rất thất vọng" nếu không có sản phẩm)
2. Phân tích pain points
3. Suggest tiếp tục validate hay move to MVP

#### Bước 4: Track metric

```bash
python3 scripts/metrics.py log --metric="interviews_done" --value=12 --stage=2
python3 scripts/metrics.py log --metric="pmf_score" --value=35 --stage=2 --notes="Chưa đạt 40% threshold"
```

---

## 6. Tháng Đầu — Build MVP

### Kịch bản: PMF score đạt 42%. Thời điểm build!

#### Bước 1: Chọn tech stack

```bash
python3 scripts/search.py "solo founder MVP tech stack" --domain tools
```

Trong AI IDE:

```
Tôi là solo founder, non-technical. Budget: $0.
Cần build app quản lý chi tiêu — cross-platform (iOS + Android).
Gợi ý tech stack và timeline.
```

**mvp-agent** sẽ:
1. Đề xuất stack phù hợp (vd: Flutter + Supabase)
2. Chia nhỏ thành sprint 2 tuần
3. Cảnh báo anti-patterns (đừng build features thừa)

#### Bước 2: Kiểm tra anti-patterns

```bash
python3 scripts/search.py "MVP anti-patterns" --domain tools_anti_patterns
```

**Kết quả:** Danh sách tools và khi nào KHÔNG nên dùng chúng.

#### Bước 3: Tìm startup programs

```bash
python3 scripts/search.py "free credits startup" --domain programs
```

**Kết quả:** AWS Activate, Google for Startups, Vercel Pro... — credits miễn phí bạn nên apply.

#### Bước 4: Sprint tracking hàng ngày

Trong AI IDE, bắt đầu mỗi ngày với:

```
/daily-ops
```

**pm-agent** sẽ hỏi:
1. Hôm qua làm gì?
2. Hôm nay plan gì?
3. Có blocker gì không?

Và tự log vào `pm/daily/YYYY-MM-DD.md`.

---

## 7. Sau 3 Tháng — Tìm PMF

### Kịch bản: App live, 200 users. Cần tối ưu retention.

#### Bước 1: Đo metric đúng

```bash
python3 scripts/search.py "PMF metrics retention" --domain metrics
python3 scripts/search.py "vanity metrics to avoid" --domain metrics_quality
```

**Kết quả:** North Star Metric cho Stage 4 = **% users "very disappointed" nếu mất sản phẩm**. Tránh vanity metrics như total downloads.

#### Bước 2: Track metrics liên tục

```bash
python3 scripts/metrics.py log --metric="dau" --value=45 --stage=4
python3 scripts/metrics.py log --metric="d7_retention" --value=28 --stage=4
python3 scripts/metrics.py log --metric="pmf_score" --value=38 --stage=4

# Xem trend
python3 scripts/metrics.py trend --metric="pmf_score"
```

**Kết quả:**
```
📊 PMF_SCORE — Trend (5 data points)
───────────────────────────────────────────
2026-01-10 │████████         35.0
2026-02-01 │██████████       38.0
2026-02-15 │████████████     40.0 ← PMF threshold!
2026-03-01 │██████████████   42.0
2026-03-15 │████████████████ 45.0 ← Growing!
───────────────────────────────────────────
Latest: 45.0  ↑ 3.0 (7%) from previous
```

#### Bước 3: Hỏi pricing strategy

```bash
python3 scripts/search.py "freemium vs subscription pricing SaaS" --domain pricing
```

Trong AI IDE:

```
App của tôi có 200 users, chủ yếu Gen Z.
PMF score 45%. D7 retention 32%.
Nên dùng freemium hay subscription? Giá bao nhiêu?
```

**growth-agent** sẽ phân tích dựa trên:
- Stage hiện tại (4 — PMF)
- Ngành (FinTech)
- Dữ liệu pricing strategies trong knowledge base
- Anti-patterns ("Đừng freemium nếu chưa có 1000 users")

---

## 8. Sau 6 Tháng — Growth

### Mở dashboard

```bash
python3 scripts/dashboard.py
# Mở http://localhost:5050
```

Dashboard hiện:
- Stage badge (Stage 5 — Growth)
- Current focus, key decisions, active blockers
- 554 knowledge rows, 29 domains, 13 agents
- Toàn bộ agent roster

### Marketing channels

```bash
python3 scripts/search.py "best marketing channels for fintech app" --domain mkt_channels
```

### Email sequences

```bash
python3 scripts/search.py "onboarding email sequence" --domain mkt_email
```

### Landing page optimization

```bash
python3 scripts/search.py "landing page conversion optimization" --domain mkt_landing
```

### Xuất báo cáo tuần để gửi advisor

```bash
python3 scripts/report.py
# → Tạo pm/reports/2026-W12.md

python3 scripts/report.py --pdf
# → Tạo cả file PDF (cần pip install weasyprint)
```

---

## 9. Embedded Tools — Công Cụ Tích Hợp

### 📊 Metrics Tracker (Zero deps)

```bash
# Ghi dữ liệu
python3 scripts/metrics.py log --metric="mrr" --value=2500 --notes="$500 MoM growth"

# Xem trend
python3 scripts/metrics.py trend --metric="mrr"

# Xem tất cả metrics
python3 scripts/metrics.py status --stage=5

# Gợi ý metrics nên track
python3 scripts/metrics.py suggest --stage=4

# Xuất CSV
python3 scripts/metrics.py export
```

### 🔍 Semantic Search (pip install chromadb sentence-transformers)

```bash
# Index toàn bộ knowledge base (chạy 1 lần)
python3 scripts/embed.py index

# Search bằng ngữ nghĩa (thông minh hơn BM25 keyword)
python3 scripts/embed.py search "nên đăng ký LLC hay C-Corp"

# Hybrid search (BM25 + semantic)
python3 scripts/embed.py search "tìm co-founder kỹ thuật" --hybrid

# Kiểm tra index
python3 scripts/embed.py status
```

**Tại sao cần?** BM25 chỉ match từ khóa. "Nên incorporate" → không tìm thấy domain "legal". Semantic search hiểu nghĩa → route chính xác.

### 🖥️ Dashboard (pip install flask)

```bash
python3 scripts/dashboard.py
# → Mở http://localhost:5050
```

### 📄 Report Generator (Zero deps cho Markdown, weasyprint cho PDF)

```bash
python3 scripts/report.py              # Markdown
python3 scripts/report.py --pdf        # + PDF
python3 scripts/report.py --week=2026-W10  # Tuần cụ thể
```

---

## 10. Quản Lý Dự Án Hàng Ngày

### Workflow hàng ngày (5 phút)

```
Sáng: Mở AI IDE → gõ /daily-ops
→ pm-agent hỏi 3 câu → tự log

Chiều: Nếu cần quyết định → gõ /decide
→ pm-agent tạo ADR (Architecture Decision Record)

Cuối tuần: Gõ /weekly-retro
→ pm-agent tạo retrospective
```

### Workflow hàng tuần (15 phút)

```bash
# 1. Xem dashboard
python3 scripts/dashboard.py

# 2. Xem trend metrics
python3 scripts/metrics.py status --stage=4

# 3. Xuất report
python3 scripts/report.py

# 4. Chia sẻ report cho co-founder/advisor
```

### Khi gặp vấn đề

| Vấn đề | Hỏi EaseStart |
|--------|---------------|
| "Không biết nên làm gì tiếp" | `/diagnose` → EaseStart phát hiện stage + gợi ý next steps |
| "Revenue không tăng" | Search `pricing optimization` + hỏi growth-agent |
| "Co-founder muốn chia tay" | Hỏi cofounder-agent về equity + vesting |
| "Burn out quá" | Hỏi wellness-agent → burnout signals + intervention |
| "Cần gọi vốn" | Hỏi fundraising-agent → pitch deck template + investor research |
| "Bị kiện" | Hỏi legal-agent → legal checklist + contract review |

---

## 11. FAQ — Hỏi & Đáp

### EaseStart có miễn phí không?

**Hoàn toàn miễn phí.** Open-source, MIT license. Không có plan trả phí, không có premium features ẩn.

### Cần API key không?

**Không cần API key nào cho EaseStart.** Search engine chạy offline, knowledge base là CSV files. Bạn chỉ cần API key/subscription của AI IDE (Antigravity, Claude Code, Cursor...) — nhưng đó là chi phí IDE, không phải của EaseStart.

### Dùng với AI IDE nào?

**6 IDE được hỗ trợ:** Antigravity, Claude Code, Gemini CLI, Cursor, Windsurf, Open Code. Bất kỳ AI IDE nào hỗ trợ `.agent/` folder hoặc MCP server đều dùng được.

### EaseStart khác gì ChatGPT?

| | ChatGPT | EaseStart |
|-|---------|-----------|
| Kiến thức | Chung, 2024 cutoff | 554 dòng curated, cập nhật liên tục |
| Lời khuyên | Chung cho mọi stage | Stage-gated — biết bạn ở đâu |
| Anti-patterns | Không cảnh báo | ⚠️ Cảnh báo sai lầm phổ biến |
| Source | "AI bịa" | Mỗi dòng có nguồn (YC, PG, First Round) |
| Agents | 1 AI chung | 13 chuyên gia riêng biệt |
| Offline | Không | `core.py` chạy hoàn toàn offline |

### Dữ liệu của tôi có an toàn không?

**100% local.** Không có server, không có cloud, không gửi data đi đâu. Metrics lưu trong SQLite local. State lưu trong markdown files. Dashboard chạy trên localhost.

### Tôi không biết code. Dùng được không?

**Được.** Bạn chỉ cần biết copy-paste lệnh terminal. EaseStart không yêu cầu bạn code.

### Tôi ở ngoài Mỹ. Có phù hợp không?

**Có.** Knowledge base cover 30 industries globally. Legal agent sẽ lưu ý bạn tìm luật sư địa phương cho các vấn đề pháp lý cụ thể từng quốc gia.

---

## 12. Cheat Sheet — Tất Cả Lệnh

### Search (Zero deps)

```bash
python3 scripts/search.py "query"                        # Auto-detect domain
python3 scripts/search.py "query" --domain pricing       # Specific domain
python3 scripts/search.py "query" --domain industries    # Industry data
python3 scripts/search.py --stats                        # Knowledge stats
```

### CLI Commands

```bash
python3 cli/main.py init                  # Setup IDE integration
python3 cli/main.py search "query"        # Search knowledge
python3 cli/main.py doctor                # Health checks
python3 cli/main.py skills list           # List domains
python3 cli/main.py skills info pricing   # Domain details
```

### Metrics (Zero deps)

```bash
python3 scripts/metrics.py log -m "metric" -v 42        # Log data point
python3 scripts/metrics.py trend -m "metric"             # ASCII trend chart
python3 scripts/metrics.py status                        # All metrics summary
python3 scripts/metrics.py suggest --stage=3             # Stage-appropriate metrics
python3 scripts/metrics.py export                        # Export to CSV
```

### Semantic Search (chromadb)

```bash
python3 scripts/embed.py index                           # Index knowledge base
python3 scripts/embed.py search "query"                  # Semantic search
python3 scripts/embed.py search "query" --hybrid         # BM25 + semantic
python3 scripts/embed.py status                          # Index stats
```

### Dashboard (flask)

```bash
python3 scripts/dashboard.py                             # Start at :5050
```

### Reports (Zero deps for MD, weasyprint for PDF)

```bash
python3 scripts/report.py                                # This week's report
python3 scripts/report.py --pdf                          # + PDF export
python3 scripts/report.py --week=2026-W10                # Specific week
```

### AI IDE Workflows

```
/startup-journey     # Full 7-stage guided experience
/diagnose            # Detect stage + next steps
/validate-idea       # Mom Test → PMF measurement
/build-mvp           # Tech stack → launch
/daily-ops           # Daily standup tracking
/weekly-retro        # Sprint retrospective
/decide              # Decision record (ADR)
/deep-research       # Multi-source research
```

### Quality & Testing

```bash
python3 scripts/simulate.py                              # Run 10 persona simulations
python3 -m unittest scripts/test_core.py -v              # Run 19 unit tests
python3 autoresearch/evaluate.py                         # Quality evaluation
```

---

## Tiếp Theo

- 🌐 [Landing Page](../landing/index.html) — Tổng quan visual về EaseStart
- 📖 [PHILOSOPHY.md](PHILOSOPHY.md) — Giantiny Biz philosophy
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) — System architecture
- 📊 [ONTOLOGY.md](ONTOLOGY.md) — Knowledge graph schemas
- 🔬 [RESEARCH.md](RESEARCH.md) — Market research

---

*Bạn không cần biết tất cả để bắt đầu. Clone repo → mở AI IDE → hỏi đi.*

**Built by [Jang Trịnh](https://linkedin.com/in/jangtrinh)** · EaseStart · Giantiny Philosophy
