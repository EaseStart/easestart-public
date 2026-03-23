#!/usr/bin/env python3
"""
EaseStart CLI — AI Startup Co-pilot

Commands:
    easestart init       Initialize EaseStart in current project
    easestart search     Search the knowledge graph
    easestart preflight  Check guardrails before executing an action
    easestart doctor     Run health checks
    easestart update     Update data + agents from GitHub
    easestart skills     Manage knowledge domains

Zero external dependencies. Pure Python 3.9+.
"""

import argparse
import sys
from pathlib import Path

from cli.commands.init_cmd import run_init
from cli.commands.search_cmd import run_search
from cli.commands.doctor_cmd import run_doctor
from cli.commands.update_cmd import run_update
from cli.commands.skills_cmd import run_skills
from cli.commands.preflight_cmd import run_preflight
from cli.commands.publish_cmd import run_publish

VERSION = "1.0.0"


def _get_dynamic_banner() -> str:
    """Generate banner with live stats from the knowledge graph."""
    try:
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.core import get_stats, EASESTART_CONFIG
        stats = get_stats()
        total_rows = stats.get("total", 0)
        total_domains = len(EASESTART_CONFIG)

        agents_dir = project_root / ".agent" / "agents"
        agent_count = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0
    except Exception:
        total_rows, total_domains, agent_count = "?", "?", "?"

    return f"""
┌──────────────────────────────────────────┐
│  🚀 EaseStart — AI Startup Co-pilot     │
│  {total_rows} rows · {total_domains} domains · {agent_count} agents      │
│  v{VERSION}                                  │
└──────────────────────────────────────────┘
"""


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="easestart",
        description="AI-powered Startup Co-pilot — search curated knowledge across 29 domains",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  easestart init                              Initialize in current project
  easestart search "best tool for MVP"        Search knowledge graph
  easestart search --stats                    Show knowledge graph statistics
  easestart doctor                            Run health checks
  easestart update                            Update from GitHub
  easestart skills list                       List all knowledge domains
  easestart skills info pricing               Show domain details
  easestart skills health                     Domain quality report

Built by Jang Trịnh — github.com/EaseStart/easestart
        """,
    )
    parser.add_argument("-v", "--version", action="version", version=f"easestart {VERSION}")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- init ---
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize EaseStart in current project",
        description="3-phase pipeline: detect environment → install agents/data → configure IDE",
    )
    init_parser.add_argument(
        "--ide",
        choices=["claude", "cursor", "windsurf", "gemini", "auto"],
        default="auto",
        help="Target IDE for MCP config (default: auto-detect)",
    )
    init_parser.add_argument(
        "--stage", type=int, choices=range(7), default=None,
        help="Set startup stage (0-6). Prompted if not provided",
    )
    init_parser.add_argument(
        "--yes", "-y", action="store_true",
        help="Non-interactive mode (accept defaults)",
    )

    # --- search ---
    search_parser = subparsers.add_parser(
        "search",
        help="Search the knowledge graph",
        description="BM25-powered search across 534 rows and 29 domains",
    )
    search_parser.add_argument("query", nargs="?", help="Search query")
    search_parser.add_argument(
        "-d", "--domain", default=None,
        help="Search specific domain (e.g., tools, pricing, playbook)",
    )
    search_parser.add_argument(
        "-s", "--stage", type=int, default=None,
        help="Filter results by startup stage (0-6)",
    )
    search_parser.add_argument(
        "-n", "--top", type=int, default=5,
        help="Number of results (default: 5)",
    )
    search_parser.add_argument(
        "--stats", action="store_true",
        help="Show knowledge graph statistics",
    )
    search_parser.add_argument(
        "--domains", action="store_true",
        help="List all available domains",
    )

    # --- doctor ---
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Run health checks",
        description="Verify Python, data integrity, MCP server, and search engine",
    )
    doctor_parser.add_argument(
        "--fix", action="store_true",
        help="Auto-fix common issues",
    )
    doctor_parser.add_argument(
        "--verbose", action="store_true",
        help="Show detailed check output",
    )

    # --- update ---
    update_parser = subparsers.add_parser(
        "update",
        help="Update data + agents from GitHub",
        description="3-phase reconciliation: compare → apply → report. Preserves your customizations.",
    )
    update_parser.add_argument(
        "--yes", "-y", action="store_true",
        help="Non-interactive mode (skip confirmation)",
    )
    update_parser.add_argument(
        "--force", action="store_true",
        help="Overwrite local customizations (creates backups first)",
    )
    update_parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would change without applying",
    )

    # --- skills ---
    skills_parser = subparsers.add_parser(
        "skills",
        help="Manage knowledge domains",
        description="List, inspect, and check health of knowledge domains",
    )
    skills_parser.add_argument(
        "action", nargs="?", default="list",
        choices=["list", "info", "health"],
        help="Action: list (default), info <domain>, health",
    )
    skills_parser.add_argument(
        "domain_name", nargs="?", default=None,
        help="Domain name (for 'info' action)",
    )
    skills_parser.add_argument(
        "--verbose", action="store_true",
        help="Show detailed domain info",
    )

    # --- preflight ---
    preflight_parser = subparsers.add_parser(
        "preflight",
        help="Check guardrails before executing an action",
        description="Validates a proposed action against guardrails.json hard gates and warnings",
    )
    preflight_parser.add_argument("action", help="Describe the action to check")
    preflight_parser.add_argument(
        "-s", "--stage", type=int, choices=range(7), default=None,
        help="Current startup stage (0-6). Required.",
    )

    # --- publish ---
    publish_parser = subparsers.add_parser(
        "publish",
        help="Publish content to Facebook Page + Threads",
        description="Publish marketing content with preview/confirm flow and golden hour scheduling",
    )
    publish_parser.add_argument("file", help="Content file (.md or .txt)")
    publish_parser.add_argument(
        "-p", "--platform",
        choices=["facebook", "threads", "all"],
        default="all",
        help="Target platform (default: all)",
    )
    publish_parser.add_argument(
        "--now", action="store_true",
        help="Post immediately (skip golden hour scheduling)",
    )
    publish_parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview only, do not publish",
    )
    publish_parser.add_argument(
        "--media",
        help="Attach image or video file",
    )
    publish_parser.add_argument(
        "--yes", "-y", action="store_true",
        help="Skip confirmation prompt",
    )
    publish_parser.add_argument(
        "--images", nargs="+",
        help="Attach multiple images for carousel post",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        print(_get_dynamic_banner())
        parser.print_help()
        sys.exit(0)

    commands = {
        "init": run_init,
        "search": run_search,
        "preflight": run_preflight,
        "doctor": run_doctor,
        "update": run_update,
        "skills": run_skills,
        "publish": run_publish,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

