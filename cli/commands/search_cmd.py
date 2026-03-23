"""
EaseStart CLI — search command

Wraps scripts/core.py search engine with CLI-friendly output.
"""

import sys
from pathlib import Path


def _ensure_core():
    """Ensure scripts/core.py is importable."""
    # Try current directory first, then parent
    for base in [Path.cwd(), Path.cwd() / "easestart", Path(__file__).parent.parent.parent]:
        scripts_dir = base / "scripts"
        if (scripts_dir / "core.py").exists():
            if str(base) not in sys.path:
                sys.path.insert(0, str(base))
            return True
    return False


def _print_result(i: int, result: dict, domain: str):
    """Format a single search result for terminal output."""
    score = result.pop("_score", 0)
    result_domain = result.pop("_domain", domain or "?")

    # Pick the best display fields
    name = (
        result.get("Name") or result.get("Title") or result.get("Company")
        or result.get("Strategy") or result.get("Rule") or result.get("Template")
        or result.get("Channel") or result.get("Metric") or result.get("Signal")
        or result.get("Stage") or result.get("Item") or result.get("Check")
        or result.get("Content_Type") or result.get("Element") or result.get("Topic")
        or result.get("Workflow") or result.get("Contract_Type") or result.get("Area")
        or "—"
    )

    # Get secondary info
    secondary_keys = [
        "Category", "Type", "Best_For", "Description", "Keywords",
        "Key_Lesson", "Do", "Formula", "Purpose", "Platform",
    ]
    secondary = ""
    for key in secondary_keys:
        val = result.get(key, "")
        if val:
            secondary = f"\n    {key}: {val}"
            break

    emoji_map = {
        "tools": "🔧", "stages": "📍", "frameworks": "📐", "resources": "📚",
        "playbook": "📋", "reasoning": "🧠", "pricing": "💰", "metrics": "📊",
        "psychology": "🧘", "casestudies": "📖", "templates": "📄", "legal": "⚖️",
        "programs": "🎁", "industries": "🏭", "team_vetting": "👥", "team_equity": "📊",
        "mkt_channels": "📢", "mkt_content": "✍️", "mkt_email": "📧",
        "mkt_landing": "🖥️", "mkt_community": "🤝", "fin_bookkeeping": "📒",
        "fin_economics": "💵", "ops_support": "🎧", "ops_automation": "⚙️",
        "contracts": "📃", "security": "🛡️",
    }
    emoji = emoji_map.get(result_domain, "🔍")

    print(f"  {emoji} [{i}] {name}  (score: {score:.2f}, {result_domain})")
    print(f"  {'─' * 46}")
    if secondary:
        print(f"  {secondary.strip()}")
    print()


def run_search(args):
    """Execute the search command."""
    if not _ensure_core():
        print("❌ Cannot find EaseStart data. Run 'easestart init' first.")
        sys.exit(1)

    from scripts.core import search, get_stats, EASESTART_CONFIG

    # --stats: show statistics
    if args.stats:
        stats = get_stats()
        print("\n" + "=" * 50)
        print("  📊 EaseStart Knowledge Graph")
        print("=" * 50 + "\n")

        # Group by pillar
        pillars = {
            "🔨 Build": ["stages", "tools", "tools_anti_patterns", "frameworks", "resources", "templates"],
            "📢 Grow": ["mkt_channels", "mkt_content", "mkt_email", "mkt_landing", "mkt_community"],
            "💰 Money": ["pricing", "fin_bookkeeping", "fin_economics", "programs"],
            "👥 People": ["team_vetting", "team_equity", "psychology", "casestudies"],
            "🛡️ Protect": ["legal", "contracts", "security"],
            "⚙️ Operate": ["playbook", "reasoning", "metrics", "metrics_quality", "ops_support", "ops_automation", "industries"],
        }
        for pillar_name, domains in pillars.items():
            pillar_total = sum(stats.get(d, 0) for d in domains)
            print(f"  {pillar_name}: {pillar_total} rows")
            for d in domains:
                count = stats.get(d, 0)
                if count > 0:
                    print(f"    └─ {d}: {count}")
            print()

        print(f"  Total: {stats.get('total', 0)} rows / {len(EASESTART_CONFIG)} domains")
        print()
        return

    # --domains: list all domains
    if args.domains:
        print("\n  Available domains:\n")
        for domain in sorted(EASESTART_CONFIG.keys()):
            print(f"    {domain}")
        print()
        return

    # Search requires a query
    if not args.query:
        print("❌ Please provide a search query. Example:")
        print('   easestart search "best tool for MVP"')
        sys.exit(1)

    results = search(
        query=args.query,
        domain=args.domain,
        top_k=args.top,
        stage=args.stage,
    )

    domain_display = f" in '{args.domain}'" if args.domain else ""
    stage_display = f" (stage {args.stage})" if args.stage is not None else ""

    print(f"\n{'=' * 50}")
    print(f'  🔍 "{args.query}"{domain_display}{stage_display}')
    print(f"  Results: {len(results)}")
    print(f"{'=' * 50}\n")

    if not results:
        print("  No results found. Try a different query or domain.\n")
        return

    for i, result in enumerate(results, 1):
        _print_result(i, result, args.domain)
