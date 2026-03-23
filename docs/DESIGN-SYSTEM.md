# EaseStart Design System

> Visual identity and design tokens for EaseStart brand assets, graphics, and generated content.

---

## Design Tokens

### Colors (Monochrome)

| Token | Value | Usage |
|-------|-------|-------|
| `bg-primary` | `#000000` | Dashboard backgrounds, hero sections |
| `bg-surface` | `#1A1A1A` | Cards, chart backgrounds |
| `text-primary` | `#FFFFFF` | Headings, key metrics |
| `text-secondary` | `#4E4B66` | Metadata, labels, descriptions |
| `border` | `#333333` | Dividers, chart gridlines |
| `accent` | `#FFFFFF` | CTAs, highlights (just white on black) |

> **No purple. No blue. No color.** Monochrome only.

### Typography

| Role | Font | Weight | Style |
|------|------|--------|-------|
| **Headings** | Saira Condensed (DIN alternative) | 700 | UPPERCASE |
| **Body** | SF Pro Rounded / system-ui | 400 | Normal |
| **Code** | IBM Plex Mono | 400 | Normal |

### Icons

| Library | URL | Usage |
|---------|-----|-------|
| **Phosphor Icons** | [phosphoricons.com](https://phosphoricons.com/) | All icons in graphics, charts, infographics |

**Phosphor rules:**
- **Weight:** Bold for headings/heroes, Regular for labels, Light for dense data
- **Style:** Outline preferred over Fill (matches flat design)
- **Color:** White on black backgrounds, Black on white backgrounds
- **Size:** 24px standard, 32px for heroes, 16px for compact

**Key icons for EaseStart domains:**
| Domain | Phosphor Icon |
|--------|--------------|
| CEO/Founder | `user-circle-gear` |
| Ideation | `lightbulb` |
| Validation | `check-circle` |
| Build/MVP | `hammer` |
| Marketing | `megaphone` |
| Operations | `gear-six` |
| Finance | `currency-circle-dollar` |
| Legal | `scales` |
| Wellness | `heart` |
| Growth | `trend-up` |
| Search | `magnifying-glass` |
| Knowledge | `books` |

### Layout

- **Max width:** 1920px (16:9)
- **Aspect ratios:** 16:9 (hero), 1:1 (social), 4:3 (slides)
- **Padding:** 80px outer, 40px inner
- **Grid:** 12-column, 24px gutter

### Style

- **Flat design** — no shadows, no gradients, no 3D
- **High contrast** — white text on pure black
- **Data-driven** — charts, numbers, diagrams > decorative elements
- **Minimalist** — every element must earn its place

---

## Source

Design tokens derived from:
- [Jang's CV Design System](../CV-html/DS-Foundations.md) — monochrome, DIN + SF Pro Rounded
- [Phosphor Icons](https://phosphoricons.com/) — flexible icon family

---

## Assets

| File | Purpose |
|------|---------|
| `assets/hero.png` | GitHub README hero graphic |
| `assets/knowledge-coverage.png` | 6 Pillars bar chart |
