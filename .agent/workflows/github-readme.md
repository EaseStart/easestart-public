---
description: Create or improve GitHub Profile READMEs and Project READMEs — from strategy to pixel-perfect markdown with dynamic stats, badges, and automation.
---

# /github-readme — GitHub README Workflow

> **Skill required:** `@[skills/github-readme]` — Read SKILL.md before starting.

> **Lucius:** L2 (Phase→Artifact→Gate) · L5 (visual checklist score)
> **Owner:** mvp-agent

---

## Phase 1: DISCOVERY (Understand the Subject)

1. **Clarify scope:**
   - Profile README or Project README?
   - Target audience? (recruiters, devs, open-source community, personal brand)
   - Existing GitHub profile? → Audit current state

2. **Gather inputs:**
   - GitHub username
   - Current role, company, key achievements
   - Top 3-5 technologies to highlight
   - Key projects to feature (max 4)
   - Social links (LinkedIn, Twitter/X, website, email)
   - Personal brand vibe: "Minimalist", "Stats Powerhouse", "Creative", "Professional", "Dynamic", "Full Package"

3. **Research context:**
   - Check user's existing repos for star counts, language breakdown
   - Identify pinnable repos (most-starred or most-representative)
   - Check if user has a blog/RSS feed for auto-updates

---

## Phase 2: STRATEGY (Architecture Decisions)

4. **Select archetype** from the 6 archetypes (see SKILL.md §2):
   - Match to user's goals and audience
   - Default: "Professional" for job seekers, "Stats Powerhouse" for OSS maintainers

5. **Choose widget stack** (select from SKILL.md §4):
   - **Must-have (pick all 3):** GitHub Stats + Top Languages + Streak Stats
   - **Differentiators (pick 2-3):** Trophy, Activity Graph, Blog Posts, Spotify, WakaTime
   - **Personality (pick 0-1):** Quotes, Visitor Badge, Jokes

6. **Pick theme** — one theme for ALL widgets:
   - Dark profiles: `tokyonight`, `radical`, `dracula`
   - Light profiles: `buefy`, `vue`, `default`
   - Always use `hide_border=true`

7. **Choose layout pattern** (see SKILL.md §6):
   - Pattern A (two-column stats) — most common
   - Pattern B (centered) — minimalist
   - Pattern C (left-right split) — professional
   - Pattern D (section headers) — comprehensive

---

## Phase 3: BUILD (Write the README)

8. **Create the hero section:**
   - Option A: Generate custom banner image with AI (`generate_image` tool)
   - Option B: Use Readme Typing SVG with personalized text
   - Option C: Capsule Render dynamic wave header
   - Option D: Clean text heading (minimalist)

9. **Write identity block:**
   - 4-5 bullet points max
   - Every line passes the "So what?" test (SKILL.md §10)
   - Use power verbs: Built, Shipped, Scaled, Launched

10. **Add tech stack badges:**
    - 8-12 badges max (SKILL.md §5)
    - Consistent style (`for-the-badge` or `flat`)
    - Order: Languages → Frameworks → Databases → Cloud → Tools

11. **Add stats widgets:**
    - All using the SAME theme
    - Place in chosen layout pattern

12. **Add featured projects:**
    - Pin up to 4 repos using github-readme-stats pin cards
    ```markdown
    <a href="https://github.com/USER/REPO">
      <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=USER&repo=REPO&theme=THEME" />
    </a>
    ```

13. **Add social links section:**
    - Use shields.io badges for consistency
    - Center-aligned
    - 3-5 links max

14. **(Optional) Set up GitHub Actions:**
    - Blog post workflow (if user has RSS)
    - Activity readme (for dynamic updates)
    - Use templates from SKILL.md §7

---

## Phase 4: REVIEW (Quality Gate)

15. **Visual audit checklist:**
    - [ ] Hero section is compelling in first 3 seconds
    - [ ] No more than 12 tech badges
    - [ ] All widgets use the same theme
    - [ ] `hide_border=true` on all stat cards
    - [ ] No broken images or links
    - [ ] Readable on both GitHub light AND dark mode
    - [ ] Total visible content < 200 lines
    - [ ] At least 1 dynamic element (stats, blog posts, typing SVG)
    - [ ] Social links present and working
    - [ ] "So what?" test passes on every text line

16. **Browser verification:**
    - Open the rendered README in browser
    - Check both light and dark mode appearance
    - Verify all dynamic embeds load correctly
    - Check mobile rendering (GitHub mobile)

17. **Anti-pattern scan** (SKILL.md §11):
    - No badge overload
    - No wall of text
    - No broken images
    - No mixed themes
    - No template-looking README

---

## Quick Reference: Copy-Paste Snippets

### Stats Cards

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=USERNAME&show_icons=true&theme=tokyonight&hide_border=true)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=USERNAME&layout=compact&theme=tokyonight&hide_border=true)

![GitHub Streak](https://streak-stats.demolab.com/?user=USERNAME&theme=tokyonight&hide_border=true)

![Trophy](https://github-profile-trophy.vercel.app/?username=USERNAME&theme=tokyonight&no-frame=true&row=1&column=6)
```

### Typing SVG

```markdown
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=4000&pause=1000&color=2F81F7&center=true&vCenter=true&width=600&height=55&lines=Your+Name+—+Your+Title;Building+Amazing+Things)](https://git.io/typing-svg)
```

### Dynamic Wave Header

```markdown
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=Your%20Name&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32" />
```

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Discovery | Understand subject + goals | Research notes | Clear purpose + audience |
| **2** Strategy | Architecture decisions | README skeleton | Section order + badge strategy decided |
| **3** Build | Write markdown + add dynamic elements | `README.md` | All sections populated + links work |
| **4** Review | Quality gate | Review checklist | Visual hierarchy ✅ + mobile readable ✅ |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All sections filled + badges load + responsive | → Ship README |
| **MEDIUM** | Content complete but some badges/stats not loading | → Binary: A) Ship without dynamic badges, B) Debug badge URLs |
| **LOW** | Subject matter unclear or README purpose undefined | → Stop, return to Phase 1 |

### Anti-Patterns
- ❌ Starting to write without understanding the project's unique selling points
- ❌ Using generic template without customization
- ❌ Badge overload — max 5-6 badges in hero section
- ❌ Not testing README render on GitHub (dark + light mode)
