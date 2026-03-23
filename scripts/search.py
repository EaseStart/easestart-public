#!/usr/bin/env python3
"""
EaseStart — Knowledge Graph Search CLI

Usage:
    python3 scripts/search.py "query"
    python3 scripts/search.py "query" --domain tools
    python3 scripts/search.py "query" --stage 3
    python3 scripts/search.py --stats
"""

import argparse
import sys
import os
from typing import Optional

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.core import search, detect_domain, get_stats, EASESTART_CONFIG


# --- Display Formatters ---

DOMAIN_ICONS = {
    "stages":     "🎯",
    "tools":      "🔧",
    "tools_anti_patterns": "⚠️",
    "programs":   "💰",
    "resources":  "📚",
    "frameworks": "🧩",
    "playbook":   "📋",
    "reasoning":  "🧠",
    "industries": "🏭",
    "team_vetting":   "👥",
    "team_equity":    "📊",
    "legal":          "⚖️",
    "contracts":      "📜",
    "security":       "🔒",
    "pricing":        "💵",
    "metrics":        "📈",
    "metrics_quality": "🎯",
    "psychology":     "🧘",
    "casestudies":    "🎬",
    "templates":      "📝",
    "mkt_channels":   "📣",
    "mkt_email":      "📧",
    "mkt_content":    "✍️",
    "mkt_landing":    "🌐",
    "mkt_community":  "🤝",
    "fin_bookkeeping": "💰",
    "fin_economics":   "📊",
    "ops_automation":  "⚙️",
    "ops_support":     "🎧",
    "analytics_events":  "📊",
    "analytics_funnels": "🔀",
    "analytics_tools":   "🛠️",
}

DOMAIN_DISPLAY_COLS = {
    "stages":     ["No", "Stage", "Exit_Criteria", "Key_Metrics"],
    "tools":      ["Name", "Category", "Pricing_Model", "Best_For", "Quality_Score"],
    "tools_anti_patterns": ["Tool_Name", "When_Not_To_Use", "Warning", "Stage_Anti_Pattern"],
    "programs":   ["Name", "Provider", "Credits_Value", "Eligibility"],
    "resources":  ["Title", "Author", "Type", "Key_Takeaways"],
    "frameworks": ["Name", "Author", "Key_Concepts", "Applicable_Stages"],
    "playbook":   ["Rule", "Do", "Dont", "Stage", "Severity"],
    "reasoning":  ["Context", "Recommended_Action", "Stage", "Severity"],
    "industries": ["Industry", "TAM_Range", "Typical_Stage_Challenges", "Counter_Position_Examples", "Giantiny_Fit_Score"],
    "team_vetting":   ["Check", "Question", "Green_Flag", "Red_Flag", "Weight"],
    "team_equity":    ["Scenario", "Recommended_Split", "Vesting", "Reasoning", "Anti_Pattern"],
    "legal":          ["Item", "Category", "Stage", "Priority", "Cost_Estimate", "DIY_Tool"],
    "pricing":        ["Strategy", "Description", "Best_For", "Pros", "Example_Companies"],
    "metrics":        ["Stage", "North_Star_Metric", "Key_Metrics", "Vanity_Metrics_To_Ignore"],
    "metrics_quality": ["Metric", "Real_Or_Vanity", "Why", "What_To_Track_Instead"],
    "psychology":     ["Signal", "Severity", "Self_Check_Question", "Intervention"],
    "casestudies":    ["Company", "Industry", "Stage_0_Problem", "Key_Lesson", "Giantiny_Alignment"],
    "templates":      ["Template", "Category", "Stage", "Purpose", "Sections"],
    "analytics_events":  ["Event_Name", "Category", "Stage", "Priority", "Why_Track"],
    "analytics_funnels": ["Funnel_Name", "Product_Type", "Steps", "Healthy_Range"],
    "analytics_tools":   ["Tool", "Category", "Stage", "Pricing", "Best_For"],
}


def format_result(result: dict, rank: int) -> str:
    """Format a single search result for display."""
    domain = result.get("_domain", "unknown")
    score = result.get("_score", 0)
    icon = DOMAIN_ICONS.get(domain, "📄")
    cols = DOMAIN_DISPLAY_COLS.get(domain, list(result.keys()))

    # Confidence-level indicators (Lucius L5)
    confidence = result.get("_confidence", "")
    conf_indicator = {"HIGH": "✅", "MEDIUM": "⁉️", "LOW": "⚠️"}.get(confidence, "")
    conf_label = f" {conf_indicator} {confidence}" if confidence else ""

    lines = [f"\n  {icon} [{rank}] Score: {score:.2f} ({domain}){conf_label}"]
    lines.append("  " + "─" * 50)

    for col in cols:
        value = result.get(col, "")
        if value and not col.startswith("_"):
            # Truncate long values
            display_val = str(value)
            if len(display_val) > 120:
                display_val = display_val[:117] + "..."
            lines.append(f"    {col}: {display_val}")

    # Show anti-pattern warning if present
    warning = result.get("_anti_pattern_warning")
    if warning and rank == 1:  # show once, on first result
        lines.append("")
        lines.append("  ⚠️  ANTI-PATTERN WARNING:")
        for w in warning.split(" | "):
            lines.append(f"    {w}")

    return "\n".join(lines)


def print_results(results: list, query: str, domain: Optional[str]):
    """Pretty-print search results."""
    detected = detect_domain(query) if domain is None else domain

    print(f"\n{'='*60}")
    print(f"  🔍 EaseStart Search")
    print(f"  Query: \"{query}\"")
    if detected:
        print(f"  Domain: {DOMAIN_ICONS.get(detected, '')} {detected}")
    else:
        print(f"  Domain: 🌐 all (auto-detect)")
    print(f"  Results: {len(results)}")
    print(f"{'='*60}")

    if not results:
        print("\n  ⚠️  No confident results above score threshold.")
        print("  💡 Choose: A) Refine query with more specific keywords, or B) Search a different domain?")
        return

    for i, result in enumerate(results, 1):
        print(format_result(result, i))

    print(f"\n{'─'*60}\n")


def print_stats():
    """Print knowledge graph statistics."""
    stats = get_stats()

    print(f"\n{'='*60}")
    print(f"  📊 EaseStart Knowledge Graph Stats")
    print(f"{'='*60}\n")

    for domain, count in stats.items():
        if domain == "total":
            continue
        icon = DOMAIN_ICONS.get(domain, "📄")
        bar = "█" * min(count, 50) + "░" * max(0, 50 - count)
        print(f"  {icon} {domain:12s} {bar[:30]} {count:4d} rows")

    print(f"\n  {'─'*40}")
    print(f"  📦 Total: {stats['total']} rows across {len(stats)-1} domains")
    print(f"\n{'='*60}\n")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="🔍 EaseStart — Search the startup knowledge graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/search.py "analytics tool for startup"
  python3 scripts/search.py "how to validate idea" --domain frameworks
  python3 scripts/search.py "startup credits" --domain programs
  python3 scripts/search.py "what stage" --stage 2
  python3 scripts/search.py --stats
        """
    )

    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--domain", "-d", choices=sorted(EASESTART_CONFIG.keys()),
                        help="Search specific domain (auto-detected if omitted)")
    parser.add_argument("--stage", "-s", type=int, choices=range(7),
                        help="Filter by startup stage (0-6)")
    parser.add_argument("--top", "-n", type=int, default=5,
                        help="Number of results (default: 5)")
    parser.add_argument("--stats", action="store_true",
                        help="Show knowledge graph statistics")

    args = parser.parse_args()

    if args.stats:
        print_stats()
        return

    if not args.query:
        parser.print_help()
        return

    results = search(
        query=args.query,
        domain=args.domain,
        top_k=args.top,
        stage=args.stage,
    )

    print_results(results, args.query, args.domain)


if __name__ == "__main__":
    main()
