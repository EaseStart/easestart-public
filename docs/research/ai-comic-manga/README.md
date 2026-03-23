# 🎨 AI Comic & Manga Generation — Research Report

> **Founder Input:** "Tôi muốn build tool generate comic, manga bằng AI"
> **Ngày nghiên cứu:** 18/03/2026
> **Phase:** 0 (DISCOVER) + Phase 1 (SCAN) completed
> **Trạng thái:** ✅ Shortlist ready → Awaiting founder confirmation for Deep Dive

---

## Phase 0: Discovery Results

### Search Queries Executed

| # | Query | Source | Results |
|---|-------|--------|---------|
| 1 | "AI comic manga generator open source GitHub 2025 2026" | GitHub | 9 repos |
| 2 | "awesome AI comic generation manga stable diffusion consistent characters" | GitHub + Web | 7 repos + 6 techniques |
| 3 | "best open source AI manga webtoon comic panel layout tool 2025" | Web | 4 repos + 6 commercial tools |

### Quality Filtering Applied

| Signal | Threshold | Eliminated |
|--------|-----------|------------|
| Stars | ≥100 | 4 repos (too small/new) |
| Last commit | <6 months | 2 repos (abandoned) |
| License | MIT/Apache | 0 (all pass) |
| README quality | Architecture section | 3 repos (landing page only) |

---

## Shortlist (5 Repos — Ranked by Relevance)

### ⭐ Priority 1: Direct Match (Same Problem Domain)

| # | Repo | Description | Why Research |
|---|------|-------------|-------------|
| 1 | **[StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion)** | Consistent Self-Attention for character-consistent image generation. NeurIPS 2024 Spotlight. | Core algorithm for character consistency — the #1 hardest problem in AI comics. Hot-pluggable with SD1.5 + SDXL. |
| 2 | **[ai-comic-factory](https://github.com/jbilcke-hf/ai-comic-factory)** | LLM + SDXL comic panel generator. HuggingFace-powered. TypeScript/Next.js. | Full-stack reference architecture — LLM generates story → SDXL renders panels. Multiple LLM backends (OpenAI, Groq, Anthropic). |
| 3 | **[Komiko](https://github.com/Story-Engine-Inc/Komiko)** | AI Comic Factory — comics, manhwa, manga, webtoons. Consistent character DB, infinite canvas, speech bubbles. | Most feature-complete: character DB, panel layout canvas, line art colorization, background removal, animation generation. Product-level reference. |

### ⭐ Priority 2: Adjacent Match (Architecture Patterns)

| # | Repo | Description | Why Research |
|---|------|-------------|-------------|
| 4 | **[comic-book-generator](https://github.com/tfrere/comic-book-generator)** | Interactive AI narrative game → comic book. Mistral AI + voice narration. Full-stack (client/server). | Interactive storytelling architecture — user makes choices, story branches. Novel UX pattern for comic creation. |
| 5 | **[Manga-Panel-LayoutGAN](https://github.com/asmaends/Manga-Panel-LayoutGAN)** | LayoutGAN++ for AI-powered manga panel layout prediction. | Specialized panel layout algorithm — generates optimal panel positions. Solves a specific sub-problem that other tools handle manually. |

### Notable Mentions (Not Shortlisted)

| Repo | Reason Not Shortlisted |
|------|----------------------|
| `mangagen` (BluePointDigital) | Gemini-only, very new, limited architecture docs |
| `AI-Comic-Generation` (alsaif1431) | Proof-of-concept only, no production architecture |
| `multiverse-origin-studio` | Custom MoE from scratch — too research-heavy for founder context |
| `ComfyUI Panels` | Extension, not standalone — requires deep ComfyUI knowledge |

---

## Key Technical Insights (from Phase 0)

### The 3 Core Problems in AI Comic Generation

| Problem | Difficulty | Current Best Solution |
|---------|-----------|----------------------|
| **Character Consistency** | 🔴 Hardest | StoryDiffusion (Consistent Self-Attention), LoRA, IP-Adapter |
| **Panel Layout** | 🟡 Medium | LayoutGAN++, manual canvas (Komiko), template-based |
| **Story → Panels** | 🟢 Solved | LLM generates panel descriptions → image model renders |

### Architecture Patterns Detected

```
Pattern A: "LLM → Image Pipeline" (ai-comic-factory)
  User prompt → LLM (story + panel descriptions) → SDXL (panel images) → Layout → Output

Pattern B: "Interactive Canvas" (Komiko)
  Character DB → Infinite canvas → AI generate per-panel → Manual arrange → Export

Pattern C: "Research Model" (StoryDiffusion)
  Text prompts (3-6) → Consistent Self-Attention → Batch generate → Video/Comic
```

### Competitive Landscape

| | Open Source | Commercial |
|---|---|---|
| **Full pipeline** | ai-comic-factory, Komiko | ComicsMaker.ai, Dashtoon |
| **Character consistency** | StoryDiffusion | Dzine AI, Anifusion |
| **Panel layout** | Manga-Panel-LayoutGAN | PanelPilot |
| **Gap (blue ocean)** | No tool combines ALL THREE with simple UX for non-technical creators | — |

---

## Recommendation for Founder

> **Khoảng trống:** Chưa có tool nào kết hợp đồng thời (1) character consistency + (2) smart panel layout + (3) LLM story generation trong 1 UX đơn giản cho non-technical creators.

### Suggested Deep Dive Order

1. **StoryDiffusion** → Extract character consistency algorithm
2. **ai-comic-factory** → Extract full-stack pipeline architecture
3. **Komiko** → Extract product features + UX patterns
4. _(Optional)_ comic-book-generator → Interactive storytelling UX
5. _(Optional)_ Manga-Panel-LayoutGAN → Panel layout algorithm

### Next Steps

- [ ] Founder confirms shortlist (add/remove repos?)
- [ ] Phase 2: DEEP DIVE on top 3 repos (6-category analysis)
- [ ] Phase 3: EXTRACT applicable patterns
- [ ] Phase 4: INTEGRATE findings into EaseStart knowledge graph
