"""
EaseStart CLI — skills command

Manage knowledge domains (inspired by ClaudeKit's skills management):
  - List all installed domains with row counts
  - Show domain details and search columns
  - Enable/disable domains for search
  - Check domain health (data quality per domain)

Adapted from ClaudeKit's skills/ domain:
  - Detection (config, dependencies)
  - Customization scanning with hash comparison
  - Registry tracking
"""

import csv
import sys
from pathlib import Path
from typing import Optional


def _find_project_root() -> Optional[Path]:
    """Find EaseStart project root."""
    for base in [Path.cwd(), Path.cwd() / "easestart", Path(__file__).parent.parent.parent]:
        if (base / "scripts" / "core.py").exists():
            return base
    return None


def _ensure_core(project_root: Path):
    """Ensure scripts/core.py is importable."""
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


# Domain metadata for display
PILLAR_MAP = {
    "🔨 Build": ["stages", "tools", "tools_anti_patterns", "frameworks", "resources", "templates",
                  "mvp_patterns"],
    "📢 Grow": ["mkt_channels", "mkt_content", "mkt_email", "mkt_landing", "mkt_community",
                 "mkt_launch", "mkt_sales", "mkt_growth", "user_research", "positioning",
                 "brand_identity"],
    "💰 Money": ["pricing", "fin_bookkeeping", "fin_economics", "programs",
                  "fundraising", "revenue_opt"],
    "👥 People": ["team_vetting", "team_equity", "psychology", "casestudies",
                   "hiring", "leadership", "remote_work", "founder_psych"],
    "🛡️ Protect": ["legal", "contracts", "security", "privacy", "legal_resources",
                     "insurance_risk"],
    "⚙️ Operate": ["playbook", "reasoning", "metrics", "metrics_quality", "ops_support",
                    "ops_automation", "industries", "startup_tools", "customer_success",
                    "automation"],
    "📊 Analytics": ["analytics", "analytics_events", "analytics_funnels", "analytics_tools"],
}


def _get_pillar(domain: str) -> str:
    """Get the pillar name for a domain."""
    for pillar, domains in PILLAR_MAP.items():
        if domain in domains:
            return pillar
    return "❓ Other"


def _cmd_list(project_root: Path, verbose: bool = False):
    """List all installed knowledge domains."""
    _ensure_core(project_root)
    from scripts.core import get_stats, EASESTART_CONFIG

    stats = get_stats()

    print(f"\n{'=' * 55}")
    print("  📚 EaseStart Knowledge Domains")
    print(f"{'=' * 55}\n")

    # Group by pillar
    for pillar_name, domains in PILLAR_MAP.items():
        pillar_rows = sum(stats.get(d, 0) for d in domains)
        print(f"  {pillar_name} ({pillar_rows} rows)")

        for domain in domains:
            count = stats.get(domain, 0)
            if count == 0:
                status = "❌ empty"
            elif count < 5:
                status = "⚠️  thin"
            else:
                status = "✅"

            config = EASESTART_CONFIG.get(domain, {})
            file_path = config.get("file", "?")

            if verbose:
                cols = ", ".join(config.get("search_cols", [])[:3])
                print(f"    {status} {domain:25s} {count:3d} rows  ({file_path})")
                print(f"         Search: {cols}")
            else:
                print(f"    {status} {domain:25s} {count:3d} rows")

        print()

    total = stats.get("total", 0)
    domain_count = len(EASESTART_CONFIG)
    print(f"  Total: {total} rows / {domain_count} domains")
    print()


def _cmd_info(project_root: Path, domain_name: str):
    """Show detailed info about a specific domain."""
    _ensure_core(project_root)
    from scripts.core import get_stats, EASESTART_CONFIG, load_csv, DOMAIN_KEYWORDS, CROSS_DOMAIN_LINKS

    if domain_name not in EASESTART_CONFIG:
        print(f"\n  ❌ Unknown domain: '{domain_name}'\n")
        print("  Available domains:")
        for d in sorted(EASESTART_CONFIG.keys()):
            print(f"    {d}")
        return

    config = EASESTART_CONFIG[domain_name]
    rows, search_cols = load_csv(domain_name)
    keywords = DOMAIN_KEYWORDS.get(domain_name, [])
    cross_links = CROSS_DOMAIN_LINKS.get(domain_name, [])
    pillar = _get_pillar(domain_name)

    print(f"\n{'=' * 55}")
    print(f"  📊 Domain: {domain_name}")
    print(f"{'=' * 55}\n")

    print(f"  Pillar:      {pillar}")
    print(f"  File:        data/{config['file']}")
    print(f"  Rows:        {len(rows)}")
    print(f"  Search cols: {', '.join(search_cols)}")
    print(f"  Keywords:    {', '.join(keywords[:5])}")
    if cross_links:
        print(f"  Cross-links: {', '.join(cross_links)}")

    # Sample data
    if rows:
        print(f"\n  Sample rows (first 3):")
        print(f"  {'─' * 45}")
        for i, row in enumerate(rows[:3], 1):
            # Show first meaningful column
            first_col = search_cols[0] if search_cols else list(row.keys())[0]
            value = row.get(first_col, "—")[:60]
            print(f"    [{i}] {first_col}: {value}")
        if len(rows) > 3:
            print(f"    ... and {len(rows) - 3} more")

    # Data quality
    print(f"\n  Data quality:")
    filled_count = 0
    for row in rows:
        filled = sum(1 for col in search_cols if row.get(col, "").strip())
        if filled >= 2:
            filled_count += 1
    quality = (filled_count / len(rows) * 100) if rows else 0
    icon = "✅" if quality >= 80 else "⚠️" if quality >= 50 else "❌"
    print(f"    {icon} {filled_count}/{len(rows)} rows have ≥2 filled search columns ({quality:.0f}%)")
    print()


def _cmd_health(project_root: Path):
    """Check health of all domains — data quality report."""
    _ensure_core(project_root)
    from scripts.core import get_stats, EASESTART_CONFIG, load_csv

    print(f"\n{'=' * 55}")
    print("  🏥 Domain Health Report")
    print(f"{'=' * 55}\n")

    issues = []

    for domain in sorted(EASESTART_CONFIG.keys()):
        config = EASESTART_CONFIG[domain]
        rows, search_cols = load_csv(domain)

        if not rows:
            issues.append((domain, "empty", "No data"))
            print(f"  ❌ {domain:25s} — EMPTY")
            continue

        # Quality: check filled columns
        low_quality = []
        for i, row in enumerate(rows, 1):
            filled = sum(1 for col in search_cols if row.get(col, "").strip())
            if filled < 2:
                low_quality.append(i)

        if low_quality:
            issues.append((domain, "quality", f"{len(low_quality)} rows with thin data"))
            print(f"  ⚠️  {domain:25s} {len(rows):3d} rows, {len(low_quality)} thin")
        elif len(rows) < 5:
            issues.append((domain, "thin", f"Only {len(rows)} rows"))
            print(f"  ⚠️  {domain:25s} {len(rows):3d} rows (thin coverage)")
        else:
            print(f"  ✅ {domain:25s} {len(rows):3d} rows")

    print(f"\n{'─' * 55}")
    if issues:
        print(f"  ⚠️  {len(issues)} domains need attention")
        for domain, issue_type, detail in issues:
            print(f"    → {domain}: {detail}")
    else:
        print("  🎉 All domains healthy!")
    print()


def run_skills(args):
    """Execute the skills command."""
    project_root = _find_project_root()
    if not project_root:
        print("  ❌ EaseStart not found. Run 'easestart init' first.")
        sys.exit(1)

    # Subcommand routing
    action = args.action if hasattr(args, "action") and args.action else "list"

    if action == "list":
        _cmd_list(project_root, verbose=getattr(args, "verbose", False))
    elif action == "info":
        domain = getattr(args, "domain_name", None)
        if not domain:
            print("  ❌ Please specify a domain: easestart skills info <domain>")
            sys.exit(1)
        _cmd_info(project_root, domain)
    elif action == "health":
        _cmd_health(project_root)
    else:
        _cmd_list(project_root)
