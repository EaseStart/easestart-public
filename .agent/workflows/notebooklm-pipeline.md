---
description: "Run NotebookLM content/research pipeline — create notebook, add sources, generate content, download artifacts."
---

# /notebooklm-pipeline

> Generate content or research artifacts using NotebookLM. Works with any agent that has the `notebooklm` skill.

## Prerequisites

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

**Verify:** `notebooklm auth check --test`

---

## Steps

### 1. Create or Select Notebook

```bash
# New notebook
notebooklm create "{Startup} - {Purpose}"
# Purpose examples: Content Marketing, Customer Validation, Market Research, Growth Research, Fundraising Intel, PM Reports

# Or use existing
notebooklm list
notebooklm use <notebook_id>
```

### 2. Add Sources

```bash
# URLs
notebooklm source add "https://example.com/article"

# Files (PDF, MD, TXT, DOCX, audio, video, images)
notebooklm source add "./document.pdf"

# YouTube
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"

# AI Research (most powerful — finds sources automatically)
notebooklm source add-research "{query}" --mode deep --import-all
```

### 3. Generate Content

Choose based on your agent's need:

| Agent Need | Command |
|------------|---------|
| Blog post | `notebooklm generate report --format blog-post --wait` |
| Research summary | `notebooklm generate report --format briefing-doc --wait` |
| Study materials | `notebooklm generate report --format study-guide --wait` |
| Podcast | `notebooklm generate audio --format brief --length short --wait` |
| Explainer video | `notebooklm generate video --style classic --wait` |
| Social infographic | `notebooklm generate infographic --style professional --wait` |
| Comparison table | `notebooklm generate data-table "{description}" --wait` |
| Theme visualization | `notebooklm generate mind-map` |
| Quiz / Flashcards | `notebooklm generate quiz --difficulty medium --wait` |
| Slide deck | `notebooklm generate slide-deck --wait` |

### 4. Download Artifacts

```bash
# Download to standardized output directory
notebooklm download report ./output/{company}/notebooklm/{category}/report.md
notebooklm download audio ./output/{company}/notebooklm/{category}/podcast.mp3
notebooklm download data-table ./output/{company}/notebooklm/{category}/data.csv
notebooklm download mind-map ./output/{company}/notebooklm/{category}/mindmap.json
notebooklm download infographic ./output/{company}/notebooklm/{category}/infographic.png
notebooklm download video ./output/{company}/notebooklm/{category}/video.mp4
notebooklm download slide-deck --format pptx ./output/{company}/notebooklm/{category}/slides.pptx
notebooklm download quiz --format markdown ./output/{company}/notebooklm/{category}/quiz.md
notebooklm download flashcards --format json ./output/{company}/notebooklm/{category}/cards.json
```

**Categories:** `content/`, `validation/`, `research/`, `pitch/`, `pm/`

### 5. Ask Follow-up Questions (Optional)

```bash
notebooklm ask "{question}" --save-as-note
notebooklm ask "{question}" --json
```

---

## Tips

- **Reuse notebooks** — don't create a new one every request. Organize by purpose.
- **Generation is async** — audio/video can take 5-30+ minutes. Use `--wait` for blocking, or `--no-wait` + `artifact poll` for async.
- **Batch downloads** — `notebooklm download {type} --all` downloads all artifacts of that type.
- **Language** — `notebooklm language set vi` for Vietnamese output.
- **Source limit** — Each notebook has a cap on sources. Remove old ones with `source delete`.

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Setup | Create notebook + add sources | Notebook ready | Sources added successfully |
| **2** Generate | Create multi-format content | Generated files (audio/video/report) | Content is coherent + accurate |
| **3** Download | Retrieve and organize outputs | Local files in output/ | Files exist + playable |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Sources quality + generation success + content coherent | → Use outputs |
| **MEDIUM** | Generation succeeded but content needs review | → CEO reviews before using |
| **LOW** | Generation failed or sources too thin | → Add more sources, retry |

### Anti-Patterns
- ❌ Generating content from a single thin source
- ❌ Not downloading outputs after generation
- ❌ Using generated content without CEO review
