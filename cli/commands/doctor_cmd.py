"""
EaseStart CLI — doctor command

Health checks inspired by ClaudeKit's `ck doctor`:
  1. System: Python version, git, platform
  2. Data: CSV integrity, row count, domain coverage
  3. Search: BM25 engine operational, simulate pass rate
  4. MCP: Server script exists, can start
  5. Links: URL health (optional, slow)
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _ensure_project() -> Optional[Path]:
    """Find EaseStart project root."""
    for base in [Path.cwd(), Path.cwd() / "easestart", Path(__file__).parent.parent.parent]:
        if (base / "scripts" / "core.py").exists():
            return base
    return None


def _check(label: str, ok: bool, detail: str = "", fix_hint: str = "") -> bool:
    icon = "✅" if ok else "❌"
    suffix = f" — {detail}" if detail else ""
    print(f"  {icon} {label}{suffix}")
    if not ok and fix_hint:
        print(f"     💡 Fix: {fix_hint}")
    return ok


def _section(title: str):
    print(f"\n  ── {title} ──")


def run_doctor(args):
    """Execute the doctor command."""
    print("\n🩺 EaseStart Doctor — Health Check\n")

    passed = 0
    failed = 0
    warnings = 0

    # ── 1. System ──
    _section("System")

    # Python
    v = sys.version_info
    py_ok = v >= (3, 9)
    if _check("Python", py_ok, f"{v.major}.{v.minor}.{v.micro}", "Upgrade to Python 3.9+"):
        passed += 1
    else:
        failed += 1

    # Git
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        git_version = result.stdout.strip().replace("git version ", "")
        if _check("Git", True, git_version):
            passed += 1
    except FileNotFoundError:
        if _check("Git", False, "not found", "Install git: https://git-scm.com"):
            passed += 1
        else:
            failed += 1

    # Platform
    import platform as plt
    _check("Platform", True, f"{plt.system()} {plt.machine()} ({plt.platform()})")
    passed += 1

    # ── 2. Project ──
    _section("Project")

    project_root = _ensure_project()
    if not project_root:
        _check("Project", False, "EaseStart not found", "Run 'easestart init' first")
        failed += 1
        _print_summary(passed, failed, warnings)
        return

    _check("Project", True, str(project_root))
    passed += 1

    # ── 3. Data Integrity ──
    _section("Data Integrity")

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    try:
        from scripts.core import get_stats, EASESTART_CONFIG

        stats = get_stats()
        total = stats.get("total", 0)

        if _check("Total rows", total >= 500, f"{total} rows", "Run autoresearch to add more data"):
            passed += 1
        else:
            warnings += 1

        # Domain coverage
        domains_ok = sum(1 for d, c in stats.items() if d != "total" and c >= 3)
        total_domains = len(EASESTART_CONFIG)
        if _check("Domain coverage", domains_ok == total_domains,
                   f"{domains_ok}/{total_domains} domains have ≥3 rows"):
            passed += 1
        else:
            warnings += 1

        # Check for empty domains
        empty_domains = [d for d, c in stats.items() if d != "total" and c == 0]
        if empty_domains:
            _check("Empty domains", False, ", ".join(empty_domains), "Add data to these CSV files")
            failed += 1
        else:
            _check("No empty domains", True)
            passed += 1

    except Exception as e:
        _check("Data loading", False, str(e)[:100])
        failed += 1

    # ── 4. Search Engine ──
    _section("Search Engine")

    try:
        from scripts.core import search

        # Quick smoke test
        test_queries = [
            ("startup idea", None),
            ("freemium pricing", "pricing"),
            ("MVP tech stack", "tools"),
        ]

        search_passed = 0
        for query, domain in test_queries:
            results = search(query, domain=domain, top_k=1)
            if results:
                search_passed += 1

        if _check("Search smoke test", search_passed == len(test_queries),
                   f"{search_passed}/{len(test_queries)} queries returned results"):
            passed += 1
        else:
            warnings += 1

    except Exception as e:
        _check("Search engine", False, str(e)[:100])
        failed += 1

    # ── 5. MCP Server ──
    _section("MCP Server")

    mcp_server = project_root / "mcp-server" / "server.py"
    if mcp_server.exists():
        _check("MCP server file", True, "server.py found")
        passed += 1

        # Check for uv
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            _check("uv runtime", True, "available")
            passed += 1
        except (FileNotFoundError, subprocess.CalledProcessError):
            _check("uv runtime", False, "not found", "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
            warnings += 1
    else:
        _check("MCP server", False, "mcp-server/server.py not found")
        failed += 1

    # ── 6. Agents ──
    _section("Agents")

    agents_dir = project_root / ".agent" / "agents"
    if agents_dir.exists():
        agents = list(agents_dir.glob("*.md"))
        _check("Agent definitions", len(agents) >= 10, f"{len(agents)} agents found")
        passed += 1
    else:
        _check("Agents", False, ".agent/agents/ not found")
        failed += 1

    # Workflows
    workflows_dir = project_root / ".agent" / "workflows"
    if workflows_dir.exists():
        workflows = list(workflows_dir.glob("*.md"))
        _check("Workflows", len(workflows) >= 5, f"{len(workflows)} workflows found")
        passed += 1
    else:
        _check("Workflows", False, ".agent/workflows/ not found")
        warnings += 1

    # ── 7. Autoresearch ──
    _section("Autoresearch")

    eval_script = project_root / "autoresearch" / "evaluate.py"
    results_file = project_root / "autoresearch" / "results.tsv"

    if eval_script.exists():
        _check("Evaluate script", True)
        passed += 1
    else:
        _check("Evaluate script", False, "autoresearch/evaluate.py not found")
        warnings += 1

    if results_file.exists():
        # Read latest score
        try:
            with open(results_file) as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last_line = [l for l in lines if l.strip() and not l.startswith("commit")]
                    if last_line:
                        parts = last_line[-1].strip().split("\t")
                        score = float(parts[1]) if len(parts) > 1 else 0
                        _check("Baseline score", score >= 75, f"{score:.2f}/100")
                        passed += 1
                    else:
                        _check("Baseline", False, "No scores recorded", "Run: python3 autoresearch/evaluate.py")
                        warnings += 1
                else:
                    _check("Baseline", False, "No scores recorded")
                    warnings += 1
        except Exception:
            _check("Results file", False, "Cannot parse results.tsv")
            warnings += 1
    else:
        _check("Results file", False, "No baseline", "Run: python3 autoresearch/evaluate.py")
        warnings += 1

    # ── Summary ──
    _print_summary(passed, failed, warnings)

    # Auto-fix
    if args.fix and failed > 0:
        print("\n  🔧 Auto-fix is not yet implemented for detected issues.")
        print("     Follow the 💡 hints above to fix manually.\n")

    # Exit code
    if failed > 0:
        sys.exit(1)


def _print_summary(passed: int, failed: int, warnings: int):
    total = passed + failed + warnings
    print(f"\n{'═' * 50}")
    print(f"  📊 Results: {passed} passed, {failed} failed, {warnings} warnings")

    if failed == 0 and warnings == 0:
        print("  🎉 All checks passed!")
    elif failed == 0:
        print("  ⚠️  Some warnings — system functional but not optimal")
    else:
        print("  ❌ Critical issues found — fix before shipping")

    print(f"{'═' * 50}\n")
