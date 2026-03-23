"""
EaseStart CLI — update command

3-Phase Reconciliation Pipeline (adapted from ClaudeKit's RECONCILE→EXECUTE→REPORT):

  Phase 1: RECONCILE — Compare local data vs latest GitHub release.
           SHA-256 checksums detect user customizations.
  Phase 2: EXECUTE   — Apply changes. Preserve user edits.
  Phase 3: REPORT    — Terraform-style summary of what changed.

Zero external dependencies. Uses git for fetching updates.
"""

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

REPO_URL = "https://github.com/EaseStart/easestart.git"

# Files that are NEVER overwritten during update (like ClaudeKit's Protected Files)
PROTECTED_PATTERNS = {
    ".env", ".env.local",
    "pm/STATE.md",
    "output/",          # User-generated outputs
}


def _sha256(filepath: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:16]  # Short hash for display
    except (IOError, OSError):
        return "0" * 16


def _is_protected(rel_path: str) -> bool:
    """Check if a file matches protected patterns."""
    for pattern in PROTECTED_PATTERNS:
        if rel_path.startswith(pattern) or rel_path == pattern:
            return True
    return False


def _find_project_root() -> Optional[Path]:
    """Find EaseStart project root."""
    for base in [Path.cwd(), Path.cwd() / "easestart", Path(__file__).parent.parent.parent]:
        if (base / "scripts" / "core.py").exists():
            return base
    return None


def _phase_header(phase: int, title: str):
    print(f"\n{'─' * 50}")
    print(f"  Phase {phase}: {title}")
    print(f"{'─' * 50}")


def run_update(args):
    """Execute the update command: 3-phase reconciliation pipeline."""
    print("\n🔄 EaseStart — Update\n")

    project_root = _find_project_root()
    if not project_root:
        print("  ❌ EaseStart not found. Run 'easestart init' first.")
        sys.exit(1)

    # ── Phase 1: RECONCILE ──
    _phase_header(1, "RECONCILE")
    print("  ⏳ Fetching latest version from GitHub...")

    # Clone latest to temp dir
    tmp_dir = Path(tempfile.mkdtemp(prefix="easestart-update-"))
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet", REPO_URL, str(tmp_dir / "latest")],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ❌ Failed to fetch: {result.stderr[:200]}")
            sys.exit(1)

        latest_dir = tmp_dir / "latest"
        print("  ✅ Fetched latest version")

        # Compare files: build reconciliation plan
        plan = {
            "add": [],      # New files not in local
            "update": [],   # Changed files (source changed, local unchanged)
            "conflict": [], # Changed files (both source AND local changed)
            "skip": [],     # Protected or unchanged files
            "delete": [],   # Files removed from source (informational)
        }

        # Track directories to compare
        compare_dirs = ["data", "scripts", ".agent", "docs", "cli", "templates"]

        for dir_name in compare_dirs:
            source_dir = latest_dir / dir_name
            local_dir = project_root / dir_name

            if not source_dir.exists():
                continue

            # Walk source files
            for source_file in source_dir.rglob("*"):
                if source_file.is_dir():
                    continue
                if "__pycache__" in str(source_file) or ".git" in str(source_file):
                    continue

                rel_path = str(source_file.relative_to(latest_dir))
                local_file = project_root / rel_path

                # Protected file check
                if _is_protected(rel_path):
                    plan["skip"].append({"path": rel_path, "reason": "protected"})
                    continue

                source_hash = _sha256(source_file)

                if not local_file.exists():
                    plan["add"].append({
                        "path": rel_path,
                        "hash": source_hash,
                        "size": source_file.stat().st_size,
                    })
                else:
                    local_hash = _sha256(local_file)

                    if source_hash == local_hash:
                        plan["skip"].append({"path": rel_path, "reason": "unchanged"})
                    else:
                        # Check if this is a user customization
                        # (we'd need a registry for perfect detection,
                        #  for now: CSV files in data/ are likely user-edited)
                        is_data = rel_path.startswith("data/")
                        if is_data:
                            plan["conflict"].append({
                                "path": rel_path,
                                "local_hash": local_hash,
                                "source_hash": source_hash,
                            })
                        else:
                            plan["update"].append({
                                "path": rel_path,
                                "local_hash": local_hash,
                                "source_hash": source_hash,
                            })

        # ── Terraform-style Plan Display ──
        print()
        total_changes = len(plan["add"]) + len(plan["update"]) + len(plan["conflict"])

        if total_changes == 0:
            print("  ✅ Already up to date! No changes needed.")
            _cleanup(tmp_dir)
            return

        print(f"  Plan: {len(plan['add'])} to add, {len(plan['update'])} to update, "
              f"{len(plan['conflict'])} conflicts, {len(plan['skip'])} unchanged\n")

        if plan["add"]:
            for item in plan["add"][:10]:
                print(f"    + {item['path']}")
            if len(plan["add"]) > 10:
                print(f"    ... and {len(plan['add']) - 10} more")

        if plan["update"]:
            for item in plan["update"][:10]:
                print(f"    ~ {item['path']}")
            if len(plan["update"]) > 10:
                print(f"    ... and {len(plan['update']) - 10} more")

        if plan["conflict"]:
            print()
            print("  ⚠️  Conflicts (local customizations detected):")
            for item in plan["conflict"]:
                print(f"    ⚠ {item['path']} (local: {item['local_hash']}, source: {item['source_hash']})")

        # ── Phase 2: EXECUTE ──
        _phase_header(2, "EXECUTE")

        if not args.yes:
            try:
                confirm = input(f"\n  Apply {total_changes} changes? [y/N] ").strip().lower()
                if confirm != "y":
                    print("  ❌ Update cancelled.")
                    _cleanup(tmp_dir)
                    return
            except (EOFError, KeyboardInterrupt):
                print("\n  ❌ Update cancelled.")
                _cleanup(tmp_dir)
                return

        # Create backup before applying
        backup_count = 0
        applied = 0
        skipped_conflicts = 0

        # Apply additions
        for item in plan["add"]:
            source_file = latest_dir / item["path"]
            target_file = project_root / item["path"]
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)
            applied += 1

        # Apply updates (non-data files)
        for item in plan["update"]:
            source_file = latest_dir / item["path"]
            target_file = project_root / item["path"]

            # Backup existing file
            backup_path = project_root / ".easestart-backup" / item["path"]
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_file, backup_path)
            backup_count += 1

            # Overwrite with source
            shutil.copy2(source_file, target_file)
            applied += 1

        # Handle conflicts
        for item in plan["conflict"]:
            if args.force:
                # Force overwrite
                source_file = latest_dir / item["path"]
                target_file = project_root / item["path"]

                backup_path = project_root / ".easestart-backup" / item["path"]
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_file, backup_path)
                backup_count += 1

                shutil.copy2(source_file, target_file)
                applied += 1
            else:
                # Keep local version (preserve customizations)
                skipped_conflicts += 1

        # ── Phase 3: REPORT ──
        _phase_header(3, "REPORT")
        print()
        print(f"  ✅ Applied: {applied} files")
        if backup_count > 0:
            print(f"  📦 Backed up: {backup_count} files → .easestart-backup/")
        if skipped_conflicts > 0:
            print(f"  ⚠️  Preserved: {skipped_conflicts} customized files (use --force to overwrite)")
        print(f"  ⏭️  Skipped: {len(plan['skip'])} unchanged files")

        # Verify after update
        print("\n  ⏳ Verifying update...")
        try:
            sys.path.insert(0, str(project_root))
            from scripts.core import get_stats
            stats = get_stats()
            print(f"  ✅ Data integrity: {stats.get('total', 0)} rows / {len(stats) - 1} domains")
        except Exception as e:
            print(f"  ⚠️  Verification warning: {e}")

        print(f"\n{'═' * 50}")
        print("  🎉 Update complete!")
        print(f"{'═' * 50}\n")

    finally:
        _cleanup(tmp_dir)


def _cleanup(tmp_dir: Path):
    """Remove temporary directory."""
    try:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    except Exception:
        pass
