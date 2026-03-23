#!/usr/bin/env python3
"""
Founder's Intel Memo — CEO-grade idea validation report.

Synthesizes Amazon 6-pager (narrative), McKinsey SCR (structure),
CIA PDB (verdict first), YC (7 forced questions), and
Sequoia Arc (why now + market sizing) into one deliverable.

Usage:
    python3 scripts/validate_idea.py "Your idea in one sentence"
    python3 scripts/validate_idea.py "AI advisor for founders" --industry devtools --stage 1
    python3 scripts/validate_idea.py "Fintech app for Gen Z" --save
"""
import sys
import os
import argparse
import textwrap
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.core import search, detect_domain

# Optional: OSINT Digital Intelligence
try:
    from scripts.osint_intel import run_osint_pipeline, format_markdown as osint_md
    OSINT_AVAILABLE = True
except ImportError:
    OSINT_AVAILABLE = False


# ─── Constants ───────────────────────────────────────────────────────
WIDTH = 68
STAGE_NAMES = {
    0: "Pre-Idea", 1: "Ideation", 2: "Validation",
    3: "MVP", 4: "PMF", 5: "Growth", 6: "Scale",
}

INDUSTRY_KEYWORDS = {
    "fintech": ["fintech", "finance", "payment", "banking", "money"],
    "edtech": ["edtech", "education", "learning", "course", "school"],
    "healthtech": ["health", "medical", "clinic", "patient", "wellness"],
    "devtools": ["developer", "developer tools", "devtools", "code", "IDE", "API", "SDK"],
    "ecommerce": ["ecommerce", "shop", "store", "retail"],
    "saas": ["saas", "software", "subscription", "platform"],
    "marketplace": ["marketplace", "two-sided", "supply", "demand", "matching", "freelance", "no-code marketplace"],
    "ai": ["ai", "artificial intelligence", "machine learning", "ml", "llm", "gpt"],
    "social": ["social", "community", "network", "messaging", "chat"],
    "creator": ["creator", "content", "media", "video", "podcast", "newsletter"],
}


# ─── Helpers ─────────────────────────────────────────────────────────

def detect_industry(idea: str) -> str:
    """Auto-detect industry from idea text."""
    idea_lower = idea.lower()
    best_match = "saas"
    best_score = 0
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in idea_lower)
        if score > best_score:
            best_score = score
            best_match = industry
    return best_match


def detect_stage_from_idea(idea: str) -> int:
    """Heuristic stage detection from idea text."""
    idea_lower = idea.lower()
    if any(w in idea_lower for w in ["scale", "series", "growth", "million users"]):
        return 5
    if any(w in idea_lower for w in ["pmf", "product market fit", "retention"]):
        return 4
    if any(w in idea_lower for w in ["mvp", "prototype", "build", "launch"]):
        return 3
    if any(w in idea_lower for w in ["validate", "test", "interview", "survey"]):
        return 2
    if any(w in idea_lower for w in ["idea", "concept", "thinking about"]):
        return 1
    return 1  # Default to ideation


def wrap(text: str, indent: int = 4) -> str:
    """Wrap text to fit terminal width."""
    prefix = " " * indent
    return textwrap.fill(text, width=WIDTH - indent,
                         initial_indent=prefix, subsequent_indent=prefix)


def section_header(title: str) -> str:
    return f"\n  ■ {title}\n  {'─' * (WIDTH - 4)}"


def bar(score: int, max_score: int = 20, length: int = 20) -> str:
    """Generate a progress bar."""
    filled = int(score / max_score * length)
    return "█" * filled + "░" * (length - filled)


def score_label(total: int) -> str:
    """Convert score to verdict label."""
    if total >= 80:
        return "STRONG — Proceed with conviction"
    if total >= 60:
        return "PROMISING — Validate further, then commit"
    if total >= 40:
        return "MODERATE — Significant pivots needed"
    return "WEAK — Reconsider fundamentally"


# ─── Section Generators ─────────────────────────────────────────────

def generate_verdict(idea: str, industry: str, stage: int, scores: dict) -> str:
    """CIA PDB style — bottom line up front, 1 paragraph."""
    total = sum(scores.values())
    label = score_label(total)

    # Pull the most relevant anti-pattern
    warnings = search("common mistake don't avoid", stage=stage)
    top_warning = ""
    if warnings:
        for w in warnings:
            ap = w.get("AntiPatterns", "")
            if ap and "⚠️" in ap:
                parts = [p.strip() for p in ap.split("⚠️") if p.strip()]
                if parts:
                    top_warning = parts[0][:80]
                    break

    verdict = (
        f"This idea scores {total}/100 ({label}). "
        f"In the {industry} space at Stage {stage} ({STAGE_NAMES.get(stage, '?')}), "
    )

    if total >= 70:
        verdict += (
            f"the problem signal is strong enough to invest time building. "
            f"Key risk: {top_warning or 'execution speed'}. "
            f"Next move: validate with 5 real customer conversations this week."
        )
    elif total >= 50:
        verdict += (
            f"there's signal but not yet conviction. "
            f"Key risk: {top_warning or 'unclear differentiation'}. "
            f"Next move: run Mom Test interviews before writing any code."
        )
    else:
        verdict += (
            f"signal is weak — the problem may not be painful enough to pay for. "
            f"Key risk: {top_warning or 'solution looking for a problem'}. "
            f"Next move: pivot the positioning or find a sharper pain point."
        )

    return wrap(verdict)


def generate_situation(idea: str, industry: str, stage: int) -> str:
    """McKinsey — what's happening in this market."""
    lines = []

    # Industry data
    industry_results = search(f"{industry} market size", stage=stage)
    if industry_results:
        top = industry_results[0]
        ind_name = top.get("Industry", industry)
        tam = top.get("TAM", "?")
        growth = top.get("GrowthRate", "?")
        trend = top.get("Trend", "?")
        lines.append(f"    Market: {ind_name} — TAM {tam}, growing {growth}")
        if trend and trend != "?":
            lines.append(f"    Trend: {trend}")

    # Case studies in this space
    cases = search(f"case study {industry} bootstrapped grew", stage=stage)
    if cases:
        for c in cases[:2]:
            company = c.get("Company", "")
            lesson = c.get("Lesson", "")
            if company:
                lines.append(f"    Comparable: {company} — {lesson[:60]}")

    if not lines:
        lines.append(f"    Market data for '{industry}' — use --industry flag for specifics")

    return "\n".join(lines)


def generate_complication(idea: str, industry: str, stage: int) -> str:
    """McKinsey — why this is hard, what founders miss."""
    lines = []

    # Anti-patterns for this stage (try with and without stage filter)
    anti = search("common mistake don't avoid", stage=stage)
    if not anti:
        anti = search("common mistake don't avoid")
    seen = set()
    for r in anti[:5]:
        ap = r.get("AntiPatterns", "")
        if ap and "⚠️" in ap:
            parts = [p.strip() for p in ap.split("⚠️") if p.strip()]
            for p in parts:
                clean = p.split("|")[0].strip()[:70]
                if clean and clean not in seen:
                    seen.add(clean)
                    lines.append(f"    ⚠️  {clean}")
                if len(seen) >= 4:
                    break
        if len(seen) >= 4:
            break

    # Tools anti-patterns
    tools_anti = search(f"wrong tool for {industry}", stage=stage)
    for r in tools_anti[:2]:
        context = r.get("Context", "")
        if context and context not in seen:
            seen.add(context)
            lines.append(f"    ⚠️  Tool trap: {context[:65]}")

    if not lines:
        lines.append("    No specific anti-patterns found for this stage/industry.")

    return "\n".join(lines)


def generate_resolution(idea: str, industry: str, stage: int) -> str:
    """McKinsey — what makes your angle defensible."""
    lines = []

    # Counter-positioning
    reasoning = search(f"help me think about {industry} startup", stage=stage)
    if reasoning:
        for r in reasoning[:2]:
            context = r.get("Context", r.get("Name", ""))
            if context:
                lines.append(f"    → {str(context)[:65]}")

    # Frameworks
    frameworks = search("lean canvas customer discovery", stage=stage)
    if frameworks:
        top = frameworks[0]
        name = top.get("Name", top.get("Framework", ""))
        if name:
            lines.append(f"    Recommended framework: {name}")

    # Pricing angle
    pricing = search(f"pricing {industry}", stage=stage)
    if pricing:
        top = pricing[0]
        strategy = top.get("Strategy", "")
        if strategy:
            lines.append(f"    Pricing model: {strategy}")

    if not lines:
        lines.append("    Analyze counter-positioning with: search 'decide between X and Y'")

    return "\n".join(lines)


def generate_seven_questions(idea: str, industry: str, stage: int) -> str:
    """YC + Sequoia — 7 forced questions."""
    questions = [
        ("Problem", "Who hurts and how badly?",
         f"burnout stress overwhelmed {industry}"),
        ("Solution", "What's the painkiller (not vitamin)?",
         f"framework method approach {industry}"),
        ("Why Now", "What changed that makes this possible today?",
         f"{industry} market trends"),
        ("Market", "TAM → SAM → SOM",
         f"{industry} market size tam"),
        ("Unfair Advantage", "What can't be copied in 6 months?",
         f"counter-positioning {industry}"),
        ("Risk Map", "Top 3 kill-this-idea risks",
         f"common mistake don't avoid {industry}"),
        ("First Dollar", "Path to revenue within 90 days",
         f"pricing monetize {industry}"),
    ]

    lines = []
    for i, (label, question, query) in enumerate(questions, 1):
        results = search(query, stage=stage)
        insight = ""
        if results:
            top = results[0]
            # Find best display field — prefer content-rich fields
            for field in ["Description", "Details", "Tip", "Rule",
                          "Strategy", "Framework", "Context", "Signal", "Name"]:
                if field in top and top[field]:
                    val = str(top[field]).strip()
                    # Skip if it's just the industry name
                    if len(val) > 5 and val.lower() != industry.lower():
                        insight = val[:55]
                        break

        lines.append(f"    {i}. {label}: {question}")
        if insight:
            lines.append(f"       💡 {insight}")
        else:
            lines.append(f"       → Answer this yourself.")

    return "\n".join(lines)


def generate_signals(idea: str, stage: int) -> str:
    """Digital validation — pain signals from the wild."""
    lines = []

    # Try to get digital validation data
    try:
        from scripts.digital_validate import search_reddit, search_hackernews, analyze_results
        all_posts = []
        keywords = idea.lower().split()[:4]
        query = " ".join(keywords)

        reddit = search_reddit(query, limit=50)
        all_posts.extend(reddit)
        hn = search_hackernews(query, limit=50)
        all_posts.extend(hn)

        if all_posts:
            analysis = analyze_results(all_posts, query)
            total = analysis.get("total_posts", 0)
            pain_pct = analysis.get("pain_percentage", 0)
            avg_eng = analysis.get("avg_engagement", 0)

            lines.append(f"    📊 Posts analyzed: {total}")
            lines.append(f"    🔥 Pain prevalence: {pain_pct:.0f}%")
            lines.append(f"    📈 Avg engagement: {avg_eng:.0f}")

            # Top pain signals
            pain_signals = analysis.get("pain_signals", [])
            if pain_signals:
                top_3 = pain_signals[:3]
                lines.append(f"    Pain signals: {', '.join(top_3)}")

            # Top quotes
            quotes = analysis.get("top_quotes", [])
            if quotes:
                lines.append(f"    💬 \"{quotes[0][:60]}...\"")

            return "\n".join(lines)
    except (ImportError, Exception):
        pass

    lines.append("    Run: python3 scripts/digital_validate.py \"your idea\" for live data")
    lines.append("    (Searches Reddit + Hacker News for pain signals)")
    return "\n".join(lines)


def generate_anti_patterns(stage: int) -> str:
    """Stage-specific warnings from EaseStart playbook."""
    lines = []

    playbook = search("common mistake don't advice rule avoid", stage=stage)
    seen = set()
    for r in playbook[:5]:
        rule = r.get("Rule", "")
        if rule and rule not in seen:
            seen.add(rule)
            lines.append(f"    🚫 {rule[:65]}")

    if not lines:
        lines.append(f"    No stage-{stage} warnings found.")

    return "\n".join(lines)


def generate_next_moves(idea: str, industry: str, stage: int) -> str:
    """Amazon tenets style — concrete, time-bound actions."""
    moves = {
        0: [
            "This week: Talk to 5 people who match your target persona",
            "This week: Write your idea as a tweet (< 280 chars). If you can't, it's too complex",
            "Next week: Fill out a Lean Canvas (scripts/search.py 'lean canvas')",
        ],
        1: [
            "This week: Run 5 Mom Test interviews (don't mention your solution)",
            "This week: Create a 1-page landing page and measure signups",
            "Next week: Analyze competitors using scripts/search.py 'counter-positioning'",
        ],
        2: [
            "This week: Get 3 people to pay (even $1) before building",
            "This week: Run digital validation: python3 scripts/digital_validate.py",
            "Next week: Define your success metric (1 North Star number)",
        ],
        3: [
            "This week: Ship the ugliest MVP that solves 1 problem well",
            "This week: Set up analytics on your core action (not vanity metrics)",
            "Next week: Get first 10 paying users and interview ALL of them",
        ],
        4: [
            "This week: Run Sean Ellis survey ('very disappointed' ≥ 40%)",
            "This week: Identify your #1 growth channel and double down",
            "Next week: Establish unit economics (LTV > 3× CAC)",
        ],
        5: [
            "This week: Automate your top 3 manual processes",
            "This week: Build community (Discord/forum) for power users",
            "Next week: Document and systematize everything for first hire",
        ],
        6: [
            "This week: Define equity structure and vesting schedule",
            "This week: Set up proper bookkeeping (P&L, runway tracking)",
            "Next week: Evaluate if you need funding or can bootstrap further",
        ],
    }

    stage_moves = moves.get(stage, moves[1])
    lines = []
    for i, move in enumerate(stage_moves, 1):
        lines.append(f"    {i}. {move}")
    return "\n".join(lines)


def calculate_scores(idea: str, industry: str, stage: int) -> dict:
    """Calculate 5-dimension confidence score."""
    scores = {
        "Problem Clarity": 0,
        "Market Opportunity": 0,
        "Competitive Edge": 0,
        "Validation Evidence": 0,
        "Execution Readiness": 0,
    }

    # 1. Problem Clarity (0-20)
    psych = search("burnout stress overwhelmed solo founder", stage=stage)
    playbook = search("common mistake don't avoid", stage=stage)
    problem_hits = len(psych) + len(playbook)
    scores["Problem Clarity"] = min(20, problem_hits * 3 + 5)

    # 2. Market Opportunity (0-20)
    market = search(f"{industry} market size tam", stage=stage)
    cases = search(f"case study {industry} bootstrapped", stage=stage)
    market_hits = len(market) + len(cases)
    scores["Market Opportunity"] = min(20, market_hits * 3 + 2)

    # 3. Competitive Edge (0-20)
    reasoning = search(f"help me think decide between", stage=stage)
    frameworks = search("lean canvas customer discovery validate", stage=stage)
    edge_hits = len(reasoning) + len(frameworks)
    scores["Competitive Edge"] = min(20, edge_hits * 2 + 4)

    # 4. Validation Evidence (0-20)
    # Check if digital validation data exists
    try:
        from scripts.digital_validate import search_reddit
        reddit_posts = search_reddit(idea.split()[0], limit=10)
        if len(reddit_posts) > 5:
            scores["Validation Evidence"] = 16
        elif len(reddit_posts) > 0:
            scores["Validation Evidence"] = 10
        else:
            scores["Validation Evidence"] = 4
    except Exception:
        # Fallback: check playbook coverage
        val = search("validate mom test", stage=stage)
        scores["Validation Evidence"] = min(20, len(val) * 4 + 2)

    # 5. Execution Readiness (0-20)
    tools = search(f"tech stack recommend tool for {industry}", stage=stage)
    programs = search("free credits startup program", stage=stage)
    exec_hits = len(tools) + len(programs)
    scores["Execution Readiness"] = min(20, exec_hits * 2 + 4)

    return scores


# ─── OSINT Digital Intelligence Section ──────────────────────────────

def _extract_startup_name(idea: str) -> str:
    """Try to extract a potential startup/product name from the idea.
    Uses heuristic: first capitalized word or first 1-2 words."""
    words = idea.split()
    # Look for a capitalized word that's not a common word
    common = {"the", "a", "an", "my", "our", "i", "we", "for", "to", "in"}
    for w in words[:5]:
        if w[0].isupper() and w.lower() not in common and len(w) > 2:
            return w
    # Fallback: use first two meaningful words
    meaningful = [w for w in words[:4] if w.lower() not in common and len(w) > 2]
    return "-".join(meaningful[:2]) if meaningful else ""


def generate_digital_intel(idea: str, stage: int) -> str:
    """Generate OSINT Digital Intelligence section for the Intel Memo."""
    if not OSINT_AVAILABLE:
        return "    ⚠️  OSINT module not available (scripts/osint_intel.py missing)\n"

    # Only run OSINT at Stage 0-2 (Pre-Idea, Ideation, Validation)
    if stage > 2:
        return "    ℹ️  OSINT scan skipped (recommended for Stages 0-2 only)\n"

    name = _extract_startup_name(idea)
    lines = []

    try:
        results = run_osint_pipeline(
            idea=idea,
            startup_name=name,
            stage=stage,
            verbose=False,
        )

        summary = results.get("summary", {})
        brand = results.get("brand", {})
        comp = results.get("competitors", {})

        # Summary line
        modules = summary.get("modules_run", 0)
        confidence = summary.get("confidence", "LOW")
        elapsed = summary.get("elapsed_seconds", 0)
        lines.append(f"    📊 Scanned {modules}/6 modules | "
                     f"Confidence: {confidence} | {elapsed}s")
        lines.append("")

        # Brand availability
        if brand.get("status") == "ok":
            risk = brand.get("risk_level", "?")
            taken = brand.get("taken_count", 0)
            total = len(brand.get("platforms", []))
            dom_taken = brand.get("domain_taken_count", 0)
            lines.append(f"    🏷️  Brand '{name}': {risk} risk")
            lines.append(f"       {taken}/{total} platforms taken, "
                         f"{dom_taken} domains registered")

            # Show domain availability
            for d in brand.get("domains", [])[:5]:
                icon = "❌" if d["available"] is False else "✅" if d["available"] else "❓"
                lines.append(f"       {icon} {d['domain']}")
            lines.append("")

        # Competitor findings
        if comp.get("competitors"):
            found = comp.get("total_competitors_found", 0)
            lines.append(f"    🏢 {found} competitors found:")
            for c in comp["competitors"][:5]:
                eng = c.get("engagement", 0)
                src = c.get("source", "")
                lines.append(f"       ↑{eng:>4d} [{src}] {c['name'][:55]}")
            lines.append("")

        # Demand signals
        if comp.get("demand_signals"):
            demand = comp.get("total_demand_signals", 0)
            lines.append(f"    📡 {demand} demand signals (people asking for solutions):")
            for ds in comp["demand_signals"][:3]:
                eng = ds.get("engagement", 0)
                lines.append(f"       ↑{eng:>4d} {ds['title'][:55]}")
            lines.append("")

        # Risk factors
        if summary.get("risk_factors"):
            lines.append("    ⚠️  Risks:")
            for r in summary["risk_factors"]:
                lines.append(f"       • {r}")
            lines.append("")

        # Opportunities
        if summary.get("opportunities"):
            lines.append("    ✅ Opportunities:")
            for o in summary["opportunities"]:
                lines.append(f"       • {o}")
            lines.append("")

        if not lines:
            lines.append("    No significant intelligence found.")

    except Exception as e:
        lines.append(f"    ⚠️  OSINT scan failed: {str(e)[:60]}")

    return "\n".join(lines) + "\n"


# ─── Main Generator ─────────────────────────────────────────────────

def generate_memo(idea: str, industry: str = None, stage: int = None,
                  save: bool = False) -> str:
    """Generate the full Founder's Intel Memo."""

    # Auto-detect if not provided
    if not industry:
        industry = detect_industry(idea)
    if stage is None:
        stage = detect_stage_from_idea(idea)

    # Calculate scores first (needed for verdict)
    scores = calculate_scores(idea, industry, stage)
    total = sum(scores.values())

    # Classification
    if total >= 80:
        classification = "🟢 STRONG"
    elif total >= 60:
        classification = "🟡 PROMISING"
    elif total >= 40:
        classification = "🟠 MODERATE"
    else:
        classification = "🔴 WEAK"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ─── Build the memo ───
    lines = []

    # Header
    lines.append("╔" + "═" * WIDTH + "╗")
    lines.append("║" + "  🔍 FOUNDER'S INTEL MEMO".ljust(WIDTH) + "║")
    lines.append("║" + ("  " + "─" * (WIDTH - 4)).ljust(WIDTH) + "║")
    lines.append("║" + f"  Subject: {idea[:WIDTH-12]}".ljust(WIDTH) + "║")
    lines.append("║" + f"  Classification: {classification}".ljust(WIDTH) + "║")
    lines.append("║" + f"  Date: {now}  │  Stage: {stage} ({STAGE_NAMES.get(stage, '?')})".ljust(WIDTH) + "║")
    lines.append("║" + f"  Industry: {industry.upper()}".ljust(WIDTH) + "║")
    lines.append("╠" + "═" * WIDTH + "╣")

    # Verdict (CIA PDB)
    lines.append(section_header("VERDICT"))
    lines.append(generate_verdict(idea, industry, stage, scores))

    # Situation (McKinsey)
    lines.append(section_header("SITUATION — What's happening"))
    lines.append(generate_situation(idea, industry, stage))

    # Complication (McKinsey)
    lines.append(section_header("COMPLICATION — Why this is hard"))
    lines.append(generate_complication(idea, industry, stage))

    # Resolution (McKinsey)
    lines.append(section_header("RESOLUTION — Your defensible angle"))
    lines.append(generate_resolution(idea, industry, stage))

    # The 7 Questions (YC + Sequoia)
    lines.append(section_header("THE 7 QUESTIONS"))
    lines.append(generate_seven_questions(idea, industry, stage))

    # Validation Signals (Digital)
    lines.append(section_header("VALIDATION SIGNALS"))
    lines.append(generate_signals(idea, stage))

    # OSINT Digital Intelligence
    lines.append(section_header("DIGITAL INTELLIGENCE"))
    lines.append(generate_digital_intel(idea, stage))

    # Anti-Pattern Warnings (Playbook)
    lines.append(section_header("STAGE WARNINGS"))
    lines.append(generate_anti_patterns(stage))

    # Next 3 Moves (Amazon Tenets)
    lines.append(section_header("NEXT 3 MOVES"))
    lines.append(generate_next_moves(idea, industry, stage))

    # Score Breakdown
    lines.append(section_header("CONFIDENCE SCORE"))
    for dim, score in scores.items():
        lines.append(f"    {dim:22s} {bar(score)} {score}/20")
    lines.append(f"\n    {'TOTAL':22s} {bar(total, 100)} {total}/100")
    lines.append(f"    {score_label(total)}")

    # Footer
    lines.append("\n╚" + "═" * WIDTH + "╝")
    lines.append(f"  Powered by EaseStart Knowledge Base")
    lines.append(f"  Format: Amazon 6-Pager × McKinsey SCR × CIA PDB × YC × Sequoia")
    lines.append("")

    memo = "\n".join(lines)

    # Save if requested
    if save:
        slug = idea.lower().replace(" ", "-")[:30]
        filename = f"intel-memo-{slug}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), filename)
        with open(filepath, "w") as f:
            f.write(f"# Founder's Intel Memo\n\n```\n{memo}\n```\n")
        print(f"\n  📄 Saved to: {filename}")

    return memo


# ─── HTML Generator ──────────────────────────────────────────────────

def _collect_data(idea: str, industry: str, stage: int) -> dict:
    """Collect all data needed for both terminal and HTML output."""
    if not industry:
        industry = detect_industry(idea)
    if stage is None:
        stage = detect_stage_from_idea(idea)

    scores = calculate_scores(idea, industry, stage)
    total = sum(scores.values())

    # Classification
    if total >= 80:
        cls_label, cls_color = "STRONG", "#22c55e"
    elif total >= 60:
        cls_label, cls_color = "PROMISING", "#eab308"
    elif total >= 40:
        cls_label, cls_color = "MODERATE", "#f97316"
    else:
        cls_label, cls_color = "WEAK", "#ef4444"

    # Collect section data
    data = {
        "idea": idea,
        "industry": industry,
        "stage": stage,
        "stage_name": STAGE_NAMES.get(stage, "?"),
        "scores": scores,
        "total": total,
        "cls_label": cls_label,
        "cls_color": cls_color,
        "now": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "verdict_label": score_label(total),
    }

    # Verdict text
    warnings = search("common mistake don't avoid", stage=stage)
    top_warning = ""
    if warnings:
        for w in warnings:
            ap = w.get("AntiPatterns", "")
            if ap and "⚠️" in ap:
                parts = [p.strip() for p in ap.split("⚠️") if p.strip()]
                if parts:
                    top_warning = parts[0][:80]
                    break

    if total >= 70:
        data["verdict_text"] = (
            f"This idea scores {total}/100 ({score_label(total)}). "
            f"In the {industry} space at Stage {stage} ({STAGE_NAMES.get(stage, '?')}), "
            f"the problem signal is strong enough to invest time building. "
            f"Key risk: {top_warning or 'execution speed'}. "
            f"Next move: validate with 5 real customer conversations this week."
        )
    elif total >= 50:
        data["verdict_text"] = (
            f"This idea scores {total}/100 ({score_label(total)}). "
            f"In the {industry} space at Stage {stage} ({STAGE_NAMES.get(stage, '?')}), "
            f"there's signal but not yet conviction. "
            f"Key risk: {top_warning or 'unclear differentiation'}. "
            f"Next move: run Mom Test interviews before writing any code."
        )
    else:
        data["verdict_text"] = (
            f"This idea scores {total}/100 ({score_label(total)}). "
            f"In the {industry} space at Stage {stage} ({STAGE_NAMES.get(stage, '?')}), "
            f"signal is weak — the problem may not be painful enough to pay for. "
            f"Key risk: {top_warning or 'solution looking for a problem'}. "
            f"Next move: pivot the positioning or find a sharper pain point."
        )

    # Situation
    sit_items = []
    industry_results = search(f"{industry} market size", stage=stage)
    if industry_results:
        top = industry_results[0]
        sit_items.append({
            "label": "Market",
            "value": f"{top.get('Industry', industry)} — TAM {top.get('TAM', '?')}, growing {top.get('GrowthRate', '?')}"
        })
        trend = top.get("Trend", "?")
        if trend and trend != "?":
            sit_items.append({"label": "Trend", "value": trend})

    cases = search(f"case study {industry} bootstrapped grew", stage=stage)
    for c in cases[:2]:
        company = c.get("Company", "")
        lesson = c.get("Lesson", "")
        if company:
            sit_items.append({"label": "Comparable", "value": f"{company} — {lesson[:70]}"})
    data["situation"] = sit_items

    # Complication
    comp_items = []
    anti = search("common mistake don't avoid", stage=stage)
    if not anti:
        anti = search("common mistake don't avoid")
    seen = set()
    for r in anti[:5]:
        ap = r.get("AntiPatterns", "")
        if ap and "⚠️" in ap:
            parts = [p.strip() for p in ap.split("⚠️") if p.strip()]
            for p in parts:
                clean = p.split("|")[0].strip()[:80]
                if clean and clean not in seen:
                    seen.add(clean)
                    comp_items.append(clean)
                if len(seen) >= 4:
                    break
        if len(seen) >= 4:
            break
    data["complication"] = comp_items

    # Resolution
    res_items = []
    reasoning = search(f"help me think about {industry} startup", stage=stage)
    for r in reasoning[:2]:
        ctx = r.get("Context", r.get("Name", ""))
        if ctx:
            res_items.append({"type": "angle", "value": str(ctx)[:75]})

    frameworks = search("lean canvas customer discovery", stage=stage)
    if frameworks:
        name = frameworks[0].get("Name", frameworks[0].get("Framework", ""))
        if name:
            res_items.append({"type": "framework", "value": name})

    pricing = search(f"pricing {industry}", stage=stage)
    if pricing:
        strat = pricing[0].get("Strategy", "")
        if strat:
            res_items.append({"type": "pricing", "value": strat})
    data["resolution"] = res_items

    # 7 Questions
    questions = [
        ("Problem", "Who hurts and how badly?",
         f"burnout stress overwhelmed {industry}"),
        ("Solution", "What's the painkiller (not vitamin)?",
         f"framework method approach {industry}"),
        ("Why Now", "What changed that makes this possible today?",
         f"{industry} market trends"),
        ("Market", "TAM → SAM → SOM",
         f"{industry} market size tam"),
        ("Unfair Advantage", "What can't be copied in 6 months?",
         f"counter-positioning {industry}"),
        ("Risk Map", "Top 3 kill-this-idea risks",
         f"common mistake don't avoid {industry}"),
        ("First Dollar", "Path to revenue within 90 days",
         f"pricing monetize {industry}"),
    ]
    q_data = []
    for label, question, query in questions:
        results = search(query, stage=stage)
        insight = ""
        if results:
            top = results[0]
            for field in ["Description", "Details", "Tip", "Rule",
                          "Strategy", "Framework", "Context", "Signal", "Name"]:
                if field in top and top[field]:
                    val = str(top[field]).strip()
                    if len(val) > 5 and val.lower() != industry.lower():
                        insight = val[:65]
                        break
        q_data.append({"label": label, "question": question, "insight": insight})
    data["questions"] = q_data

    # Anti-patterns
    ap_items = []
    playbook = search("common mistake don't advice rule avoid", stage=stage)
    seen2 = set()
    for r in playbook[:5]:
        rule = r.get("Rule", "")
        if rule and rule not in seen2:
            seen2.add(rule)
            ap_items.append(rule[:75])
    data["anti_patterns"] = ap_items

    # Next moves
    moves = {
        0: [
            ("This week", "Talk to 5 people who match your target persona"),
            ("This week", "Write your idea as a tweet (< 280 chars). If you can't, it's too complex"),
            ("Next week", "Fill out a Lean Canvas"),
        ],
        1: [
            ("This week", "Run 5 Mom Test interviews (don't mention your solution)"),
            ("This week", "Create a 1-page landing page and measure signups"),
            ("Next week", "Analyze competitors and counter-positioning"),
        ],
        2: [
            ("This week", "Get 3 people to pay (even $1) before building"),
            ("This week", "Run digital validation across Reddit + HN"),
            ("Next week", "Define your success metric (1 North Star number)"),
        ],
        3: [
            ("This week", "Ship the ugliest MVP that solves 1 problem well"),
            ("This week", "Set up analytics on your core action (not vanity metrics)"),
            ("Next week", "Get first 10 paying users and interview ALL of them"),
        ],
        4: [
            ("This week", "Run Sean Ellis survey ('very disappointed' ≥ 40%)"),
            ("This week", "Identify your #1 growth channel and double down"),
            ("Next week", "Establish unit economics (LTV > 3× CAC)"),
        ],
        5: [
            ("This week", "Automate your top 3 manual processes"),
            ("This week", "Build community (Discord/forum) for power users"),
            ("Next week", "Document and systematize everything for first hire"),
        ],
        6: [
            ("This week", "Define equity structure and vesting schedule"),
            ("This week", "Set up proper bookkeeping (P&L, runway tracking)"),
            ("Next week", "Evaluate if you need funding or can bootstrap further"),
        ],
    }
    data["next_moves"] = moves.get(stage, moves[1])

    return data


def generate_html_memo(idea: str, industry: str = None, stage: int = None) -> str:
    """Generate a beautiful HTML Intel Memo using workshop design system."""
    import html as html_module

    d = _collect_data(idea, industry, stage)
    e = html_module.escape  # shorthand

    # Build score bars (HTML)
    score_rows = ""
    for dim, score in d["scores"].items():
        pct = score / 20 * 100
        score_rows += f'''
        <div class="score-row">
          <div class="score-label">{e(dim)}</div>
          <div class="score-track">
            <div class="score-fill" style="width:{pct}%"></div>
          </div>
          <div class="score-val">{score}/20</div>
        </div>'''

    total_pct = d["total"] / 100 * 100

    # Build situation rows
    sit_html = ""
    for item in d["situation"]:
        sit_html += f'<div class="data-row"><span class="data-label">{e(item["label"])}</span> {e(item["value"])}</div>'
    if not sit_html:
        sit_html = '<div class="data-row">Use --industry flag for market specifics</div>'

    # Build complication rows
    comp_html = ""
    for item in d["complication"]:
        comp_html += f'<div class="warning-item">⚠️ {e(item)}</div>'
    if not comp_html:
        comp_html = '<div class="data-row">No specific anti-patterns found for this stage.</div>'

    # Build resolution rows
    res_html = ""
    for item in d["resolution"]:
        if item["type"] == "angle":
            res_html += f'<div class="data-row"><span class="data-label">→</span> {e(item["value"])}</div>'
        elif item["type"] == "framework":
            res_html += f'<div class="data-row"><span class="data-label">Framework</span> {e(item["value"])}</div>'
        elif item["type"] == "pricing":
            res_html += f'<div class="data-row"><span class="data-label">Pricing</span> {e(item["value"])}</div>'
    if not res_html:
        res_html = '<div class="data-row">Analyze counter-positioning with EaseStart search</div>'

    # Build 7 questions
    q_html = ""
    for i, q in enumerate(d["questions"], 1):
        insight_html = f'<div class="q-insight">💡 {e(q["insight"])}</div>' if q["insight"] else '<div class="q-answer">→ Answer this yourself.</div>'
        q_html += f'''
        <div class="question">
          <div class="q-number">{i}</div>
          <div class="q-content">
            <div class="q-label">{e(q["label"])}</div>
            <div class="q-text">{e(q["question"])}</div>
            {insight_html}
          </div>
        </div>'''

    # Build anti-patterns
    ap_html = ""
    for item in d["anti_patterns"]:
        ap_html += f'<div class="warning-item">🚫 {e(item)}</div>'
    if not ap_html:
        ap_html = f'<div class="data-row">No stage-{d["stage"]} warnings found.</div>'

    # Build next moves
    moves_html = ""
    for i, (timing, action) in enumerate(d["next_moves"], 1):
        moves_html += f'''
        <div class="move">
          <div class="move-number">{i}</div>
          <div class="move-content">
            <span class="move-timing">{e(timing)}</span>
            <span class="move-action">{e(action)}</span>
          </div>
        </div>'''

    # Build stage indicator dots
    stage_dots = ""
    for s in range(7):
        active = "active" if s == d["stage"] else ""
        stage_dots += f'<div class="stage-dot {active}"><div class="dot-num">{s}</div><div class="dot-label">{STAGE_NAMES[s]}</div></div>'

    html = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intel Memo — {e(d["idea"][:50])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --sf: ui-rounded, 'SF Pro Rounded', 'SF Pro Display', system-ui, -apple-system, sans-serif;
    --heading: 'Barlow Condensed', 'Impact', sans-serif;
    --mono: 'SF Mono', 'Fira Code', monospace;
    --black: #000000; --white: #ffffff; --slate: #4e4b66;
    --border: #e0e0e0; --bg-muted: #fafafa; --bg-code: #f5f5f5;
    --accent: {d["cls_color"]};
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:var(--sf); background:var(--white); color:var(--black); line-height:1.6; -webkit-font-smoothing:antialiased; }}

  .page {{ max-width:1000px; margin:0 auto; padding:60px 73px; }}
  @media (max-width:768px) {{ .page {{ padding:24px 20px; }} }}

  /* ── Header ── */
  .memo-badge {{ font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:3px; color:var(--slate); margin-bottom:12px; }}
  .memo-title {{ font-family:var(--heading); font-size:56px; font-weight:700; text-transform:uppercase; letter-spacing:1px; line-height:1.1; margin-bottom:16px; }}
  .memo-subject {{ font-size:22px; color:var(--slate); margin-bottom:8px; line-height:1.4; }}
  .memo-meta {{ display:flex; gap:24px; flex-wrap:wrap; font-size:15px; color:var(--slate); margin-bottom:32px; }}
  .meta-item {{ display:flex; align-items:center; gap:6px; }}

  /* ── Classification Badge ── */
  .classification {{ display:inline-flex; align-items:center; gap:8px; padding:8px 20px; font-family:var(--heading); font-size:28px; font-weight:700; letter-spacing:2px; text-transform:uppercase; border:3px solid var(--accent); margin-bottom:40px; }}
  .cls-dot {{ width:14px; height:14px; border-radius:50%; background:var(--accent); }}

  /* ── Stats Row ── */
  .stats {{ display:grid; grid-template-columns:repeat(5,1fr); gap:0; border:3px solid var(--black); margin-bottom:48px; }}
  .stat {{ text-align:center; padding:20px 8px; border-right:1px solid var(--border); }}
  .stat:last-child {{ border-right:none; }}
  .stat-val {{ font-family:var(--heading); font-size:36px; font-weight:700; line-height:1; }}
  .stat-label {{ font-size:13px; color:var(--slate); margin-top:4px; text-transform:uppercase; letter-spacing:1px; }}

  /* ── Stage Indicator ── */
  .stage-bar {{ display:flex; gap:0; margin-bottom:48px; border:3px solid var(--black); }}
  .stage-dot {{ flex:1; text-align:center; padding:12px 4px; border-right:1px solid var(--border); font-size:13px; color:var(--slate); }}
  .stage-dot:last-child {{ border-right:none; }}
  .stage-dot.active {{ background:var(--black); color:var(--white); }}
  .dot-num {{ font-family:var(--heading); font-size:22px; font-weight:700; }}
  .dot-label {{ font-size:11px; text-transform:uppercase; letter-spacing:1px; }}

  /* ── Section Headers ── */
  h2 {{ font-family:var(--heading); font-size:36px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:48px 0 16px; padding-bottom:8px; border-bottom:3px solid var(--black); }}
  .section-source {{ font-size:13px; color:var(--slate); text-transform:uppercase; letter-spacing:2px; margin-top:-8px; margin-bottom:16px; }}

  /* ── Verdict Block ── */
  .verdict {{ background:var(--bg-muted); border-left:4px solid var(--accent); padding:24px 28px; margin:16px 0 40px; font-size:20px; line-height:1.6; }}

  /* ── Data Rows ── */
  .data-row {{ font-size:18px; padding:10px 0; border-bottom:1px solid var(--border); line-height:1.5; }}
  .data-row:last-child {{ border-bottom:none; }}
  .data-label {{ font-weight:700; margin-right:8px; }}

  /* ── Warning Items ── */
  .warning-item {{ font-size:18px; padding:10px 0; border-bottom:1px solid var(--border); line-height:1.5; }}
  .warning-item:last-child {{ border-bottom:none; }}

  /* ── 7 Questions ── */
  .question {{ display:flex; gap:16px; padding:16px 0; border-bottom:1px solid var(--border); }}
  .question:last-child {{ border-bottom:none; }}
  .q-number {{ width:40px; height:40px; background:var(--black); color:var(--white); display:flex; align-items:center; justify-content:center; font-family:var(--heading); font-size:22px; font-weight:700; flex-shrink:0; }}
  .q-content {{ flex:1; }}
  .q-label {{ font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:var(--slate); }}
  .q-text {{ font-size:20px; font-weight:600; margin:4px 0; }}
  .q-insight {{ font-size:17px; color:var(--slate); margin-top:4px; }}
  .q-answer {{ font-size:17px; color:var(--slate); font-style:italic; margin-top:4px; }}

  /* ── Next Moves ── */
  .move {{ display:flex; gap:16px; padding:14px 0; border-bottom:1px solid var(--border); align-items:center; }}
  .move:last-child {{ border-bottom:none; }}
  .move-number {{ width:36px; height:36px; border:2px solid var(--black); display:flex; align-items:center; justify-content:center; font-family:var(--heading); font-size:20px; font-weight:700; flex-shrink:0; }}
  .move-content {{ flex:1; font-size:18px; }}
  .move-timing {{ font-weight:700; padding:2px 10px; background:var(--bg-code); font-size:13px; text-transform:uppercase; letter-spacing:1px; margin-right:8px; }}
  .move-action {{ font-size:18px; }}

  /* ── Scorecard ── */
  .scorecard {{ border:3px solid var(--black); padding:28px; margin:48px 0; }}
  .scorecard-title {{ font-family:var(--heading); font-size:28px; font-weight:700; text-transform:uppercase; letter-spacing:2px; margin-bottom:20px; }}
  .score-row {{ display:flex; gap:16px; align-items:center; padding:10px 0; border-bottom:1px solid var(--border); }}
  .score-row:last-child {{ border-bottom:none; }}
  .score-label {{ width:180px; font-size:16px; font-weight:600; flex-shrink:0; }}
  .score-track {{ flex:1; height:12px; background:var(--bg-code); border:1px solid var(--border); position:relative; }}
  .score-fill {{ height:100%; background:var(--black); transition:width 0.6s ease; }}
  .score-val {{ width:60px; text-align:right; font-family:var(--mono); font-size:15px; font-weight:700; flex-shrink:0; }}
  .score-total {{ display:flex; gap:16px; align-items:center; padding:16px 0; margin-top:8px; border-top:3px solid var(--black); }}
  .score-total .score-label {{ font-family:var(--heading); font-size:22px; text-transform:uppercase; letter-spacing:2px; }}
  .score-total .score-val {{ font-family:var(--heading); font-size:28px; }}
  .score-total .score-fill {{ background:var(--accent); }}
  .score-verdict {{ font-size:18px; color:var(--slate); margin-top:8px; }}

  /* ── Footer ── */
  .footer {{ margin-top:60px; padding-top:24px; border-top:3px solid var(--black); font-size:14px; color:var(--slate); }}
  .footer-brand {{ font-family:var(--heading); font-size:18px; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:var(--black); margin-bottom:4px; }}

  @media print {{
    .page {{ padding:20px; }}
    h2 {{ margin-top:24px; }}
    .scorecard {{ break-inside:avoid; }}
  }}
</style>
</head><body>
<div class="page">

  <!-- Header -->
  <div class="memo-badge">Founder's Intel Memo</div>
  <h1 class="memo-title">Idea<br>Validation</h1>
  <div class="memo-subject">{e(d["idea"])}</div>
  <div class="memo-meta">
    <div class="meta-item">📅 {d["now"]}</div>
    <div class="meta-item">🏭 {e(d["industry"].upper())}</div>
    <div class="meta-item">📍 Stage {d["stage"]} — {e(d["stage_name"])}</div>
  </div>
  <div class="classification">
    <div class="cls-dot"></div>
    {e(d["cls_label"])}
    <span style="font-size:18px;font-weight:400;color:var(--slate)">{d["total"]}/100</span>
  </div>

  <!-- Stats -->
  <div class="stats">
    <div class="stat"><div class="stat-val">{d["total"]}</div><div class="stat-label">Score</div></div>
    <div class="stat"><div class="stat-val">{d["stage"]}</div><div class="stat-label">Stage</div></div>
    <div class="stat"><div class="stat-val">{len(d["situation"])}</div><div class="stat-label">Signals</div></div>
    <div class="stat"><div class="stat-val">{len(d["complication"])}</div><div class="stat-label">Risks</div></div>
    <div class="stat"><div class="stat-val">{len(d["questions"])}</div><div class="stat-label">Questions</div></div>
  </div>

  <!-- Stage Indicator -->
  <div class="stage-bar">{stage_dots}</div>

  <!-- VERDICT -->
  <h2>Verdict</h2>
  <div class="section-source">CIA President's Daily Brief format</div>
  <div class="verdict">{e(d["verdict_text"])}</div>

  <!-- SITUATION -->
  <h2>Situation</h2>
  <div class="section-source">McKinsey SCR — What's happening</div>
  {sit_html}

  <!-- COMPLICATION -->
  <h2>Complication</h2>
  <div class="section-source">McKinsey SCR — Why this is hard</div>
  {comp_html}

  <!-- RESOLUTION -->
  <h2>Resolution</h2>
  <div class="section-source">McKinsey SCR — Your defensible angle</div>
  {res_html}

  <!-- 7 QUESTIONS -->
  <h2>The 7 Questions</h2>
  <div class="section-source">Y Combinator + Sequoia Arc format</div>
  {q_html}

  <!-- ANTI-PATTERNS -->
  <h2>Stage Warnings</h2>
  <div class="section-source">EaseStart Playbook — Stage {d["stage"]} ({e(d["stage_name"])})</div>
  {ap_html}

  <!-- NEXT 3 MOVES -->
  <h2>Next 3 Moves</h2>
  <div class="section-source">Amazon Tenets — Time-bound actions</div>
  {moves_html}

  <!-- SCORECARD -->
  <div class="scorecard">
    <div class="scorecard-title">Confidence Score</div>
    {score_rows}
    <div class="score-total">
      <div class="score-label">Total</div>
      <div class="score-track"><div class="score-fill" style="width:{total_pct}%"></div></div>
      <div class="score-val">{d["total"]}/100</div>
    </div>
    <div class="score-verdict">{e(d["verdict_label"])}</div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <div class="footer-brand">EaseStart</div>
    <div>Format: Amazon 6-Pager × McKinsey SCR × CIA PDB × Y Combinator × Sequoia Arc</div>
    <div>Generated {d["now"]} · Built for the overwhelmed solo founder.</div>
  </div>

</div>
</body></html>'''

    return html


# ─── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Founder's Intel Memo — CEO-grade idea validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 scripts/validate_idea.py "AI startup advisor for solo founders"
              python3 scripts/validate_idea.py "Fintech app for Gen Z" --industry fintech --stage 1
              python3 scripts/validate_idea.py "No-code marketplace" --save
              python3 scripts/validate_idea.py "SaaS tool" --html
        """),
    )
    parser.add_argument("idea", help="Your startup idea in one sentence")
    parser.add_argument("--industry", "-i", help="Industry (auto-detected if omitted)")
    parser.add_argument("--stage", "-s", type=int, choices=range(7),
                        help="Current stage 0-6 (auto-detected if omitted)")
    parser.add_argument("--save", action="store_true",
                        help="Save memo as markdown file")
    parser.add_argument("--html", action="store_true",
                        help="Generate beautiful HTML memo and open in browser")
    parser.add_argument("--report", action="store_true",
                        help="Generate full HVS-style validation report")

    args = parser.parse_args()

    if args.report:
        from scripts.generate_validation_report import generate_report
        report_dir = generate_report(args.idea, industry=args.industry)
        import subprocess
        subprocess.run(["open", os.path.join(report_dir, "index.html")],
                       check=False)
    elif args.html:
        stage_num = args.stage if args.stage is not None else detect_stage_from_idea(args.idea)
        html_content = generate_html_memo(args.idea, industry=args.industry,
                                          stage=args.stage)
        slug = args.idea.lower().replace(" ", "-")[:30]
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        stage_label = STAGE_NAMES.get(stage_num, "unknown").lower()
        filename = f"intel-memo-stage{stage_num}-{stage_label}.html"
        filepath = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), filename)
        with open(filepath, "w") as f:
            f.write(html_content)
        print(f"\n  📄 HTML memo saved: {filename}")
        print(f"  🌐 Opening in browser...")
        import subprocess
        subprocess.run(["open", filepath], check=False)
    else:
        memo = generate_memo(args.idea, industry=args.industry,
                             stage=args.stage, save=args.save)
        print(memo)


if __name__ == "__main__":
    main()
