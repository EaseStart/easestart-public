---
description: End-to-end workshop creation — research, content design, HTML build, multi-modal content generation (Gemini TTS + NotebookLM podcasts/video/quiz/flashcards/slides/reports via notebooklm-py), GitHub Pages deploy, and Lucius quality review.
---

# /workshop — Workshop Creation Pipeline

6-phase pipeline: `Research → Design → Build → Audio → Deploy → Review`

> **Lucius:** L2 (6-phase gated) · L5 (Lucius quality review in Phase 6)
> **Owner:** ops-agent

Each phase loads specific skills, produces a named artifact, and has a quality gate.

---

## Phase 1: RESEARCH → Understand the Domain

> **Trigger:** "create workshop for [topic]", "thiết kế khoá học [X]"
> **Output:** Topic analysis + curriculum outline
> **Gate:** User confirms scope before designing sessions.

### Actions

1. **Domain Mapping:** What are the key concepts? What's the skill progression (beginner → advanced)?
2. **Audience Analysis:** Who is the learner? What do they already know? What's their goal?
3. **Benchmark (Lucius Hướng Loang):** Find WORLD-CLASS workshops, not average ones. Cross-domain research mandatory.
4. **Scope Decision:** How many levels? How many sessions per level? What's the depth?

### World-Class Research Protocol (Mandatory)

> Source: Lucius Neural Propagation — hướng loang ban đầu quyết định chất lượng.

| Step | Action | Output |
|------|--------|--------|
| **① Benchmark** | Find the BEST workshops/courses in this domain, not average ones. Look at university courses, conference talks, industry leaders | Best-in-class patterns + what makes them memorable |
| **② First Principles** | What does the learner ACTUALLY need to be able to DO? Strip away conventions | 1-sentence learning signal |
| **③ Cross-Domain** | What can we steal from other domains? Game design? Sales training? UX onboarding? | 1+ cross-domain insight to differentiate |
| **④ Trade-offs** | What do we emphasize vs de-emphasize? What's essential vs nice-to-have? | Trade-off table: emphasize X, de-emphasize Y, because Z |
| **⑤ Executability** | Can every exercise be completed with what the learner has? | Adjusted scope within constraints |

### Socratic Gate (Mandatory)

Ask minimum 3 questions before proceeding:
- Who is the primary audience and what's their current skill level?
- What should they be able to DO after the workshop (not just know)?
- What format — self-paced, guided, in-person?

### Output Artifact

```
{artifact-dir}/workshop-{topic}.md
```

Contains: learning objectives, level breakdown, session outlines, key concepts per session.

---

## Phase 2: DESIGN → Write Detailed Session Content

> **Trigger:** "write content", "chi tiết vào", "fill in sessions"
> **Prerequisite:** Phase 1 outline approved.
> **Output:** Detailed content for each session (markdown or direct HTML).
> **Gate:** User reviews content accuracy + Gagné checklist passes.

### Content Structure Per Session

Each session needs:

| Component | Purpose | Gagné Event |
|-----------|---------|-------------|
| **Attention Hook** | Surprising stat, "what goes wrong" scenario | ① Gain Attention |
| **Objectives** | What the learner will be able to DO | ② State Objectives |
| **Bridge** paragraph | "Ở session trước..." connect to prior knowledge | ③ Recall Prior Knowledge |
| **Why** box | Context — why this matters | ④ Present Content |
| **Core Concept** | The key idea, formula, or framework | ④ Present Content |
| **Comparison Table** | Show trade-offs, alternatives, platform differences | ④ Present Content |
| **Best Practice** callout | The #1 tip to remember | ⑤ Provide Guidance |
| **Code/Template Block** | Actionable templates with copy button | ⑤ Provide Guidance |
| **Exercise** | Hands-on practice with textarea + **success criteria** | ⑥ Elicit Practice |
| **Expected Output** | "What good looks like" — example answer or screenshot | ⑦ Provide Feedback |
| **Self-Check Quiz** (per level) | 3-5 questions at end of each level | ⑧ Assess Performance |
| **Apply Challenge** | "Apply this to YOUR project" prompt | ⑨ Enhance Transfer |

### Gagné's 9 Events Checklist (Per Session)

> 🔴 **Every session must cover at least 7 of 9 events.** Events ⑧ and ⑨ can be per-level instead of per-session.

```
[ ] ① Gain Attention — hook or surprising stat at start
[ ] ② State Objectives — clear "you will be able to..." statement
[ ] ③ Recall Prior Knowledge — bridge to previous session
[ ] ④ Present Content — core concept + examples
[ ] ⑤ Provide Guidance — best practices, tips, callouts
[ ] ⑥ Elicit Practice — exercise with clear task
[ ] ⑦ Provide Feedback — expected output / "what good looks like"
[ ] ⑧ Assess Performance — self-check quiz (per level minimum)
[ ] ⑨ Enhance Transfer — "apply to your project" challenge (per level minimum)
```

### Anti-Patterns
- ❌ Don't write abstract theory without practical examples
- ❌ Don't skip exercises — every session needs hands-on practice
- ❌ Don't make sessions too long — max 3 concepts per session
- ❌ Don't omit "what good looks like" — exercises without expected outputs are useless

---

## Phase 3: BUILD → Generate HTML Pages

> **Trigger:** "build HTML", "xây page", "tạo HTML"
> **Prerequisite:** Session content finalized.
> **Output:** HTML files in target directory.
> **Gate:** Visual inspection in browser.

### Load Context

- Check existing workshop/course HTML pages in the project for design patterns
- Load `shared.css` or relevant stylesheet
- Follow the established component vocabulary (`.why`, `.reflection`, `.code-block`, etc.)

### Page Structure

| Page | Purpose |
|------|---------|
| `index.html` | Hub page — overview of all levels |
| `level-{n}-{name}.html` | Per-level page with all sessions |

### HTML Requirements

| Requirement | Details |
|-------------|---------|
| **Sidebar nav** | Links to all levels + hub |
| **Objectives block** | 🎯 Learning objectives at top of each level |
| **Session headers** | `<h2>` with session number + title + difficulty indicator |
| **Interactive elements** | `<textarea>` for exercises, copy buttons for code |
| **Audio placeholders** | Space for audio players (added in Phase 4) |
| **Bottom nav** | Previous/next level links |
| **Self-check quiz** | At end of each level page |
| **Semantic HTML** | `lang` attribute, `role` regions, `aria-label` on interactive elements |

### Progressive Disclosure Pattern

Use expandable sections for advanced content to reduce cognitive load:

```html
<!-- Difficulty indicators -->
<span class="difficulty" data-level="1">⚡ Foundation</span>
<span class="difficulty" data-level="2">⚡⚡ Applied</span>
<span class="difficulty" data-level="3">⚡⚡⚡ Advanced</span>

<!-- Expandable advanced content -->
<details class="advanced">
  <summary>🔍 Deep Dive: [Topic]</summary>
  <!-- Advanced content hidden by default -->
</details>
```

### Design Rules (Mandatory)

> These rules ensure visual consistency across all workshop pages.

#### Icons

| Rule | Details |
|------|---------|
| **Library** | [Phosphor Icons](https://phosphoricons.com/) via CDN |
| **CDN** | `<script src="https://unpkg.com/@phosphor-icons/web"></script>` |
| **Usage** | `<i class="ph ph-{icon-name}"></i>` |
| **No Emoji** | All UI icons must be Phosphor. Emoji only allowed inside `<pre>` code blocks (user-copyable content) |

Icon mapping reference:

| Context | Icon | Class |
|---------|------|-------|
| Learning objectives | Target | `ph-target` |
| Audio/podcast | Headphones | `ph-headphones` |
| Concept labels | Book | `ph-book-open` |
| Exercises | Pencil | `ph-pencil-simple` |
| Best practices / Do | Check | `ph-check-circle` |
| Don'ts | X Circle | `ph-x-circle` |
| Warnings | Warning | `ph-warning` |
| Callout links | Pin | `ph-push-pin` |
| Comparisons | Chart | `ph-chart-bar` |
| Prohibit | Prohibit | `ph-prohibit` |

#### Colors (Monochrome)

```css
--black: #000000;   /* Primary, headings, borders */
--white: #ffffff;   /* Background */
--slate: #4e4b66;   /* Secondary text, labels */
--border: #e0e0e0;  /* Borders, dividers */
--bg-muted: #fafafa; /* Muted backgrounds */
--bg-code: #f5f5f5;  /* Code blocks */
```

> 🔴 **No colors outside this palette.** Status indicators use `ph-circle-fill` with inline `style="color:#22c55e"` (green), `style="color:#eab308"` (yellow), or default black.

#### Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Headings (h1, h2) | Barlow Condensed | 56px / 48px | Uppercase, bold, letter-spacing |
| Body | SF Pro Rounded | 20px | Line-height 28px |
| Labels | System | 14px | Uppercase, bold, 2px spacing |
| Code | SF Mono / Fira Code | 15px | Pre-wrap |

#### Component Vocabulary

| Class | Purpose |
|-------|---------|
| `.why` | Rationale/context box (left border) |
| `.best-practice` | Best practice callout |
| `.reflection` | Exercise with textarea |
| `.code-block` | Code block with copy button |
| `.insight` | Insight callout |
| `.warning` | Warning callout |
| `.example-good` / `.example-bad` | Do/don't examples |
| `.objectives` | Learning objectives block |
| `.tab-bar` + `.tab-panel` | Tabbed content sections |

### Anti-Patterns
- ❌ Don't use inline styles when CSS classes exist
- ❌ Don't skip the sidebar navigation
- ❌ Don't forget `lang="vi"` for Vietnamese content
- ❌ Don't show all content at once — use `<details>` for advanced topics

---

## Phase 4: MEDIA → Generate Audio + Content Artifacts

> **Trigger:** "tạo audio", "generate content", "add media", "tạo quiz"
> **Prerequisite:** HTML pages exist.
> **Output:** Audio, video, quiz, flashcards, slides, infographics, study guides in output subdirectories.
> **Gate:** All generated files load/play correctly + content accuracy spot-check.
>
> 🔧 **Tool:** [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py) — unofficial Python API/CLI for NotebookLM.
> Install: `pip install "notebooklm-py[browser]" && playwright install chromium`
> Auth: `notebooklm login` (one-time browser login)

### Dual-Modality Audio Strategy

> Research basis: Dual Coding Theory — learning improves when both visual and auditory channels are engaged. TTS + reading = stronger memory traces.

| Audio Type | Cognitive Purpose | Placement | Tool |
|------------|------------------|-----------|------|
| **Podcast** | Engagement + big picture | TOP of level — listen BEFORE reading | NotebookLM |
| **TTS Narration** | Reinforcement + retention | After each session h2 — listen WHILE reading | Gemini TTS |
| **Recap Quiz** (optional) | Self-assessment | BOTTOM of level — listen AFTER exercises | Gemini TTS |

```
Audio Placement Rule:
  Podcast → TOP of level page (preview/hook)
  TTS     → After each session <h2> (reinforcement)
  Recap   → BOTTOM of level (before navigation)
```

### Approach A: Gemini TTS → Per-Session Narration

For detailed, consistent narration with a **single fixed voice** across all sessions.

**Setup:**
```bash
# Requires GEMINI_API_KEY environment variable
export GEMINI_API_KEY="your-key"
```

**Voice Selection:**
Use ONE voice consistently across all sessions. Available voices:

| Voice | Style |
|-------|-------|
| `Zephyr` | Calm, friendly, clear |
| `Puck` | Energetic, upbeat |
| `Charon` | Deep, authoritative |
| `Kore` | Warm, approachable |
| `Fenrir` | Bold, confident |
| `Leda` | Gentle, soothing |
| `Orus` | Professional, neutral |
| `Aoede` | Bright, engaging |

> 🔴 **Rule:** Always use the SAME `voice_name` for ALL sessions in a workshop. This ensures voice consistency. Default: `Zephyr`.

**Generation Pattern (batch by level, not all at once):**
```python
# Use uv for Python 3.12+ (system Python may be too old)
# Run one batch per level to avoid timeouts

import os, struct
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def generate_session_audio(name, script, voice='Zephyr', output_dir='audio'):
    response = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents=f'Đọc đoạn sau bằng giọng tiếng Việt, tone thân thiện, rõ ràng:\n\n{script}',
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice
                    )
                )
            ),
        ),
    )
    data = response.candidates[0].content.parts[0].inline_data.data
    # Save as WAV (24kHz, 16-bit mono)
    sr = 24000
    path = f'{output_dir}/{name}.wav'
    with open(path, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(data)))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sr, sr*2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(data)))
        f.write(data)
```

**Cost:** ~$0.04 per 9 sessions (~6 min total audio). Essentially free.

**Script Writing Rules:**
- Write in the learner's language (Vietnamese for VN workshops)
- Conversational tone — "Chào bạn", "chúng ta sẽ..."
- Summarize the session's key points, don't read the entire page
- 80-150 words per script (~30-60 seconds audio)

**Batching Strategy:**
- Generate 3 files at a time (1 level per batch)
- Add `time.sleep(2)` between API calls
- Run via `uv run --python 3.12 --with google-genai`

### Approach B: NotebookLM → Podcast-Style Overview

For engaging 2-host podcast discussions per level.

**Setup:**
```bash
# Authenticate (one-time)
notebooklm login

# Set language
notebooklm language set vi
```

**Pipeline:**
```bash
# 1. Create or use existing notebook
notebooklm create "Workshop - [Level Name]"

# 2. Add workshop content as source
notebooklm source add file content.md

# 3. Generate audio (async — takes 5-30 min)
notebooklm generate audio "Tạo podcast giới thiệu tổng quan" \
  --format deep-dive \
  --language vi \
  --no-wait

# 4. Download when ready
notebooklm download audio --all ./audio/
```

**Format Options:**
| Format | Hosts | Best For |
|--------|-------|----------|
| `deep-dive` | 2 | Level overviews, in-depth discussion |
| `brief` | 1 | Short summaries |
| `critique` | 2 | Critical analysis |
| `debate` | 2 | Exploring trade-offs |

> ⚠️ **Limitation:** NotebookLM does NOT allow voice selection. Each generation may produce different voices. Use `instructions` text to guide tone, but cannot guarantee consistency.

### Approach C: NotebookLM Studio Artifacts → Quiz, Flashcards, Slides, Reports

Generate supplementary learning materials directly from workshop content.

> 🔴 **These features are NOT available in the web UI** — only via `notebooklm-py` CLI/API.

**Setup:** Same auth as Approach B (`notebooklm login` + create notebook + add sources).

**Quiz Generation (per level):**
```bash
# Generate quiz from workshop content
notebooklm generate quiz --difficulty medium --quantity standard --json
# Wait for completion
notebooklm artifact wait <artifact_id>
# Download as Markdown (for embedding in HTML) or JSON (for interactive quiz)
notebooklm download quiz --format markdown ./quiz/level-N-quiz.md
notebooklm download quiz --format json ./quiz/level-N-quiz.json
```

**Flashcards (per level):**
```bash
notebooklm generate flashcards --difficulty medium --quantity more --json
notebooklm artifact wait <artifact_id>
notebooklm download flashcards --format json ./flashcards/level-N.json
notebooklm download flashcards --format markdown ./flashcards/level-N.md
```

**Study Guide Report:**
```bash
notebooklm generate report --format study-guide \
  --append "Target audience: beginners. Language: Vietnamese. Focus on practical takeaways." --json
notebooklm artifact wait <artifact_id>
notebooklm download report ./reports/study-guide.md
```

**Slide Deck (for in-person presentations):**
```bash
notebooklm generate slide-deck --format detailed --json
notebooklm artifact wait <artifact_id>
# Download as editable PPTX (web UI only offers PDF!)
notebooklm download slide-deck ./slides/workshop-slides.pptx --format pptx
# Or PDF for static sharing
notebooklm download slide-deck ./slides/workshop-slides.pdf
```

**Slide Revision (edit individual slides):**
```bash
# Fix or customize a specific slide after generation
notebooklm generate revise-slide "Add a real-world example from EaseUI" \
  --artifact <slide_artifact_id> --slide 3 --wait
```

**Infographic (visual summary per level):**
```bash
notebooklm generate infographic --style sketch-note --orientation landscape --json
notebooklm artifact wait <artifact_id>
notebooklm download infographic ./infographics/level-N.png
```

**Style options for infographics:** `auto`, `sketch-note`, `professional`, `bento-grid`, `editorial`, `instructional`, `bricks`, `clay`, `anime`, `kawaii`, `scientific`

**Mind Map (hierarchical JSON):**
```bash
notebooklm generate mind-map  # Sync, instant — no wait needed
notebooklm download mind-map ./mindmaps/level-N.json
```

**Data Table (structured comparisons):**
```bash
notebooklm generate data-table "Compare key concepts across all sessions" --json
notebooklm artifact wait <artifact_id>
notebooklm download data-table ./tables/concepts-comparison.csv
```

### Approach D: Video Generation (Explainer + Cinematic)

Generate video content for marketing or in-workshop use.

```bash
# Explainer video (shorter, instructional)
notebooklm generate video --style whiteboard --format explainer --json
notebooklm artifact wait <artifact_id>
notebooklm download video ./video/explainer.mp4

# Cinematic video (documentary-style, longer)
notebooklm generate cinematic-video "Documentary-style overview of this workshop" --json
notebooklm artifact wait <artifact_id>
notebooklm download cinematic-video ./video/overview.mp4
```

**Video style options:** `auto`, `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro-print`, `heritage`, `paper-craft`

### Approach E: Auto-Research (Deep Web Research)

Auto-discover and import relevant web sources before generating content.

```bash
# Fast research (5-10 sources, seconds)
notebooklm source add-research "workshop topic keywords" --mode fast

# Deep research (20+ sources, 2-5 min)
notebooklm source add-research "topic deep dive" --mode deep --import-all

# Check research status
notebooklm research status
notebooklm research wait --import-all
```

> 💡 **Use case:** Before generating a podcast or quiz, enrich the notebook with more sources to improve quality.

### Subagent Async Pattern (Non-Blocking Generation)

NotebookLM generation takes 5-30 minutes. Use background agents to avoid blocking.

```
# After starting generation, spawn a background agent:
Task(
  prompt="Wait for artifact {artifact_id} in notebook {notebook_id} to complete.
          Use: notebooklm artifact wait {artifact_id} -n {notebook_id} --timeout 600
          Then: notebooklm download audio ./audio/podcast.mp3 -a {artifact_id} -n {notebook_id}
          Report success or timeout.",
  subagent_type="general-purpose"
)
# Main conversation continues while agent waits in background
```

> 🔴 **Rule:** For batch generation (audio + quiz + flashcards + slides), generate ALL artifacts first, then spawn ONE subagent to wait + download all. More efficient than sequential blocking.

### Embed Audio Players (Accessible)

After generating audio files, embed players with transcripts:

```html
<!-- Level overview podcast (top of page, after subtitle) -->
<div class="audio-guide" role="region" aria-label="Podcast tổng quan Level N">
  <div class="audio-label">🎧 Podcast — Nghe tổng quan Level N</div>
  <audio controls preload="none" style="width:100%">
    <source src="audio/podcast-level-N.mp3" type="audio/mpeg">
  </audio>
</div>

<!-- Per-session narration with transcript (after each h2) -->
<div class="audio-guide" role="region" aria-label="Audio hướng dẫn session N.N">
  <audio controls preload="none" style="width:100%;margin:8px 0 4px">
    <source src="audio/session-N.N-name.wav" type="audio/wav">
  </audio>
  <details class="transcript">
    <summary>📝 Transcript</summary>
    <p>[Full text of TTS script — free since we already wrote it]</p>
  </details>
</div>
```

> 🔴 **Accessibility rule:** Since we ALREADY write the TTS scripts, transcripts are free — always embed them. This makes audio content accessible to deaf/hearing-impaired learners and improves SEO.

**Player placement:**
- **Podcast player:** After page subtitle, before objectives block
- **Session player + transcript:** Directly after each `<h2>` session header
- **Recap audio (optional):** Before bottom navigation

---

## Phase 5: REVIEW → Lucius Theory Quality Scan

> **Trigger:** Automatic after Phase 4 complete, or "review quality", "kiểm tra chất lượng"
> **Output:** Quality report with scores per dimension
> **Gate:** Weighted average ≥ 4.0

### Lucius Quality Scoring Matrix

Rate each dimension 1-5. Quality gate: **weighted average ≥ 4.0**.

| # | Dimension | Weight | 1 (Fail) | 3 (Acceptable) | 5 (World-Class) |
|---|-----------|--------|----------|-----------------|------------------|
| **1** | **Hướng Loang** (Research Depth) | 15% | Generic examples | Good examples from domain | Cross-domain insights, world-class benchmarks |
| **2** | **Cân Bằng Động** (Theory/Practice) | 20% | All theory or all cookbook | 50/50 mix | Practice-led with theory surfaced at point of need |
| **3** | **Phản Hồi** (Feedback Loops) | 15% | No exercises | Exercises exist | Exercises with expected outputs + self-check quiz |
| **4** | **Progression Arc** | 15% | Random session order | Logical flow | Deliberate scaffolding, each session builds on previous |
| **5** | **Anti-Fragility** | 10% | Happy path only | Anti-patterns listed | Failure scenarios explored with recovery strategies |
| **6** | **Executability** | 15% | Abstract instructions | Copy-paste templates | Runnable with verification + success criteria |
| **7** | **Gagné Coverage** | 10% | < 4 events/session | 6-7 events/session | 9/9 events covered systematically |

### Scoring

```
Score = (D1×0.15 + D2×0.20 + D3×0.15 + D4×0.15 + D5×0.10 + D6×0.15 + D7×0.10)

≥ 4.0 → Ship ✅
3.0-3.9 → Fix warnings, re-review ⚠️
< 3.0 → Redesign required ❌
```

### Quality Checklist

```
CRITICAL (must pass):
[ ] Every session has a learning objective
[ ] Every session has a hands-on exercise
[ ] Every exercise has success criteria + expected output
[ ] Anti-patterns are covered (not just happy paths)
[ ] Progression is logical (no forward references)
[ ] All code/template blocks have copy buttons
[ ] Audio files load and play correctly
[ ] Audio transcripts embedded for accessibility
[ ] Quiz/flashcard files generated and accessible
[ ] Video files load and play (if generated)

WARNING (should fix):
[ ] Examples are from real projects, not generic
[ ] Cross-domain insights exist (not just textbook content)
[ ] Each level has a self-check quiz (auto-generated or manual)
[ ] Each level takes roughly equal time
[ ] Slide deck reviewed for accuracy (auto-gen may have errors)

INFO (nice to have):
[ ] Recommended reading/resources per level
[ ] Recap section at end of each level
[ ] Printable cheat sheet or reference card
[ ] Progressive disclosure for advanced content
[ ] Infographic per level for visual learners
[ ] Mind map JSON exported for visualization
```

### Review Actions

1. **Read through all HTML pages** as a learner would — follow the progression
2. **Run the scoring matrix** — rate each of 7 dimensions
3. **Spot-check audio** — play at least 1 file per level, verify transcript matches
4. **Test all interactive elements** — copy buttons, textareas, `<details>` expand
5. **Verify links** — sidebar nav, bottom nav, hub links
6. **Gagné audit** — for each session, check which of the 9 events are present

---

## Quick Reference

| Phase | Trigger | Output | Gate |
|-------|---------|--------|------|
| **1. Research** | "create workshop" | Topic analysis + outline | User confirms scope |
| **2. Design** | "write content" | Session content + Gagné checklist | User reviews + 7/9 events per session |
| **3. Build** | "build HTML" | HTML pages + progressive disclosure | Browser inspection |
| **4. Media** | "generate content" | Audio + Video + Quiz + Flashcards + Slides + Reports | Playback + accuracy |
| **5. Review** | Auto / "review quality" | Scored quality report | Weighted average ≥ 4.0 |
| **6. Deploy** | "deploy" / "đưa lên github" | Live GitHub Pages site | Site loads + all links work |

## File Structure

```
workshop-{name}/
├── index.html                          # Hub page (ONLY html at root)
├── shared.css                          # Design system (copied locally)
├── .github/workflows/deploy.yml        # GitHub Pages deploy
├── .gitignore                          # .DS_Store
├── levels/
│   ├── level-1-{name}.html             # Level pages
│   ├── level-2-{name}.html
│   └── level-3-{name}.html
├── appendix/
│   ├── examples-personas.html          # Supplementary content
│   └── examples-personas.md            # Source markdown
├── audio/
│   ├── {podcast-name}.mp3              # NotebookLM podcasts
│   ├── session-1.1-{topic}.wav         # Gemini TTS narrations
│   ├── session-1.2-{topic}.wav
│   ├── examples-{persona}.wav          # Persona narrations
│   └── ...
├── video/                              # NotebookLM video generation
│   ├── explainer.mp4                   # Whiteboard/explainer style
│   └── overview.mp4                    # Cinematic documentary style
├── quiz/                               # Auto-generated quizzes
│   ├── level-1-quiz.md                 # Markdown format
│   └── level-1-quiz.json               # JSON for interactive embedding
├── flashcards/                         # Auto-generated flashcards
│   ├── level-1.json                    # JSON format
│   └── level-1.md                      # Markdown format
├── slides/                             # Auto-generated slide decks
│   ├── workshop-slides.pptx            # Editable PowerPoint
│   └── workshop-slides.pdf             # Static PDF
├── reports/                            # Auto-generated reports
│   └── study-guide.md                  # Study guide for learners
├── infographics/                       # Visual summaries
│   └── level-N.png                     # Per-level infographic
├── mindmaps/                           # Hierarchical knowledge maps
│   └── level-N.json                    # JSON for visualization
├── tables/                             # Structured data exports
│   └── concepts-comparison.csv         # Concept comparisons
└── scripts/
    └── generate_tts.py                 # TTS generation script
```

### Path Rules

| From | CSS path | Audio path | Hub link | Sibling link |
|------|----------|------------|----------|--------------|
| `index.html` (root) | `shared.css` | `audio/` | — | `levels/level-*.html` |
| `levels/*.html` | `../shared.css` | `../audio/` | `../index.html` | Same folder |
| `appendix/*.html` | `../shared.css` | `../audio/` | `../index.html` | `../levels/level-*.html` |

### Sidebar Navigation

All level pages and appendix pages must include:

```html
<nav class="sidebar">
  <div class="sidebar-brand"><h2>Workshop</h2><p>Topic · Name</p></div>
  <div class="nav-group">
    <div class="nav-label">Modules</div>
    <a href="../index.html" class="nav-link">← Hub</a>
    <a href="level-1-{name}.html" class="nav-link">Level 1</a>
    <a href="level-2-{name}.html" class="nav-link">Level 2</a>
    <a href="level-3-{name}.html" class="nav-link active">Level 3</a>
  </div>
  <div class="nav-group">
    <div class="nav-label">Phụ lục</div>
    <a href="../appendix/{page}.html" class="nav-link">Appendix Page</a>
  </div>
</nav>
```

---

## Phase 6: DEPLOY → GitHub Pages

> **Trigger:** "deploy", "đưa lên github", "publish"
> **Prerequisite:** All HTML pages finalized + audio generated.
> **Output:** Live site on `https://{user}.github.io/{repo}/`
> **Gate:** Site loads correctly in browser.

### Pre-deploy Checklist

```
[ ] shared.css is copied INTO the repo (not external reference)
[ ] All CSS paths use relative paths (../shared.css from subfolders)
[ ] All audio paths use relative paths (../audio/ from subfolders)
[ ] All nav links use correct relative paths
[ ] .gitignore includes .DS_Store
[ ] No file exceeds 100MB (GitHub limit)
[ ] Total repo under 1GB (soft limit)
```

### Steps

// turbo-all

1. **Initialize git repo:**
   ```bash
   cd workshop-{name}
   echo ".DS_Store" > .gitignore
   git init && git add -A
   git commit -m "feat: {workshop-name} — full content + audio"
   ```

2. **Create GitHub repo + push:**
   ```bash
   gh repo create {repo-name} --public --source=. --push \
     --description "{workshop description}"
   ```

3. **Enable GitHub Pages:**
   ```bash
   gh api repos/{user}/{repo}/pages -X POST \
     -f "build_type=workflow" \
     -f "source[branch]=main" \
     -f "source[path]=/"
   ```

4. **Create deploy workflow:**

   File: `.github/workflows/deploy.yml`
   ```yaml
   name: Deploy to GitHub Pages
   on:
     push:
       branches: ["main"]
     workflow_dispatch:
   permissions:
     contents: read
     pages: write
     id-token: write
   concurrency:
     group: "pages"
     cancel-in-progress: false
   jobs:
     deploy:
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/configure-pages@v5
         - uses: actions/upload-pages-artifact@v3
           with:
             path: '.'
         - id: deployment
           uses: actions/deploy-pages@v4
   ```

5. **Push workflow + verify:**
   ```bash
   git add .github/ && git commit -m "ci: add GitHub Pages deploy"
   git push
   gh run watch --exit-status  # Wait for deploy
   ```

6. **Verify live site:**
   Open `https://{user}.github.io/{repo}/` and check:
   - [ ] Hub page loads with correct CSS
   - [ ] All level pages accessible via sidebar
   - [ ] Appendix pages accessible
   - [ ] Audio files play correctly
   - [ ] Phosphor icons render
   - [ ] Navigation links work across all pages

### Future Updates

After initial deploy, any `git push` to `main` auto-deploys:

```bash
git add -A && git commit -m "fix: description" && git push
# Site updates in ~30s
```


---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Research | Domain analysis + Socratic gate | Research notes | 3+ quality sources identified |
| **2** Design | Session content + Gagné's 9 Events | Session outlines (markdown) | All sessions have learning objectives |
| **3** Build | HTML page generation | Workshop HTML pages | Pages render correctly |
| **4** Audio | TTS narration + NotebookLM podcasts | Audio files (.mp3) | Audio matches content |
| **5** Deploy | GitHub Pages deployment | Live URL | Site accessible + all links work |
| **6** Review | Lucius quality review | Review report | Score ≥ 7.0 |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All 6 phases pass + Lucius review ≥ 7.0 | → Workshop ready for delivery |
| **MEDIUM** | Phases 1-5 pass but review has suggestions | → Binary: A) Ship with improvements noted, B) Iterate |
| **LOW** | Content gaps or HTML rendering issues | → Stop, return to Phase 2 |

### Anti-Patterns
- ❌ Skipping Socratic gate in Phase 1 — building without understanding domain
- ❌ Sessions without Gagné's 9 Events checklist — pedagogy matters
- ❌ Deploying without audio content — dual coding improves learning 40%+
- ❌ Skipping Phase 6 Lucius review — quality gate exists for a reason
