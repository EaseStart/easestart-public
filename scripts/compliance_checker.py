#!/usr/bin/env python3
from __future__ import annotations
"""
Guard Layer — Workflow Compliance Checker.

Validates that workflow phases produce required artifacts and pass gates.
Run between phases or after workflow completion to enforce compliance.

Usage:
    python3 scripts/compliance_checker.py <feature-id> [--phase N] [--full]
    python3 scripts/compliance_checker.py test-feature --phase 1
    python3 scripts/compliance_checker.py test-feature --full
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SPECS_DIR = PROJECT_ROOT / "plans" / "specs"
PM_DIR = PROJECT_ROOT / "pm"
TELEMETRY_FILE = PM_DIR / "telemetry.jsonl"

# Phase artifact requirements
PHASE_ARTIFACTS = {
    1: {
        "file": "brainstorm.md",
        "name": "Brainstorm",
        "min_size_bytes": 200,
        "required_sections": ["Press Release", "User Stories"],
    },
    2: {
        "file": "usecases.md",
        "name": "Use Cases",
        "min_size_bytes": 300,
        "required_sections": ["Use Case", "Acceptance Criteria"],
    },
    3: {
        "file": "blueprint.md",
        "name": "Blueprint",
        "min_size_bytes": 500,
        "required_sections": ["Information Architecture", "File Structure"],
    },
    4: {
        "file": "STATUS.md",
        "name": "Status Tracker",
        "min_size_bytes": 50,
        "required_sections": [],
    },
}

# Phase dependencies (phase N requires these earlier phases)
PHASE_DEPS = {
    2: [1],
    3: [1, 2],
    4: [1, 2, 3],
}


class CheckResult:
    """Result of a single compliance check."""

    def __init__(self, name: str, passed: bool, message: str, severity: str = "INFO"):
        self.name = name
        self.passed = passed
        self.message = message
        self.severity = severity  # INFO, WARN, BLOCK


class ComplianceReport:
    """Aggregated compliance report."""

    def __init__(self, feature_id: str, phase: int | None = None):
        self.feature_id = feature_id
        self.phase = phase
        self.checks: list[CheckResult] = []
        self.timestamp = datetime.now().isoformat()

    def add(self, check: CheckResult):
        self.checks.append(check)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def block_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "BLOCK")

    @property
    def warn_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "WARN")

    def print_report(self):
        """Print formatted compliance report."""
        scope = f"Phase {self.phase}" if self.phase else "Full"
        print("=" * 60)
        print(f"  🛡️  Compliance Check — {self.feature_id} ({scope})")
        print("=" * 60)

        for check in self.checks:
            icon = "✅" if check.passed else ("❌" if check.severity == "BLOCK" else "⚠️")
            print(f"  {icon}  {check.name}")
            if not check.passed:
                print(f"      → {check.message}")

        print(f"\n{'─' * 60}")
        if self.passed:
            print(f"  ✅  ALL CHECKS PASSED ({len(self.checks)} checks)")
        else:
            print(f"  ❌  FAILED — {self.block_count} blocks, {self.warn_count} warnings")
        print(f"{'─' * 60}\n")

    def to_dict(self) -> dict:
        return {
            "feature_id": self.feature_id,
            "phase": self.phase,
            "timestamp": self.timestamp,
            "passed": self.passed,
            "block_count": self.block_count,
            "warn_count": self.warn_count,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "message": c.message,
                    "severity": c.severity,
                }
                for c in self.checks
            ],
        }


def check_artifact_exists(spec_dir: Path, artifact: dict) -> CheckResult:
    """Check if a phase artifact file exists and meets quality bar."""
    filepath = spec_dir / artifact["file"]

    if not filepath.exists():
        return CheckResult(
            name=f"{artifact['name']} artifact exists",
            passed=False,
            message=f"Missing: {artifact['file']}",
            severity="BLOCK",
        )

    content = filepath.read_text(encoding="utf-8")
    size = len(content.encode("utf-8"))

    if size < artifact["min_size_bytes"]:
        return CheckResult(
            name=f"{artifact['name']} artifact quality",
            passed=False,
            message=f"{artifact['file']} is too small ({size}B < {artifact['min_size_bytes']}B min). Likely placeholder.",
            severity="WARN",
        )

    # Check required sections
    missing_sections = []
    for section in artifact.get("required_sections", []):
        pattern = re.compile(re.escape(section), re.IGNORECASE)
        if not pattern.search(content):
            missing_sections.append(section)

    if missing_sections:
        return CheckResult(
            name=f"{artifact['name']} required sections",
            passed=False,
            message=f"Missing sections in {artifact['file']}: {', '.join(missing_sections)}",
            severity="WARN",
        )

    return CheckResult(
        name=f"{artifact['name']} artifact ({artifact['file']})",
        passed=True,
        message="OK",
    )


def check_phase_dependencies(spec_dir: Path, phase: int) -> list[CheckResult]:
    """Check that prerequisite phase artifacts exist before advancing."""
    results = []
    deps = PHASE_DEPS.get(phase, [])

    for dep_phase in deps:
        artifact = PHASE_ARTIFACTS[dep_phase]
        filepath = spec_dir / artifact["file"]

        if filepath.exists():
            results.append(CheckResult(
                name=f"Phase {dep_phase} prerequisite ({artifact['file']})",
                passed=True,
                message="OK",
            ))
        else:
            results.append(CheckResult(
                name=f"Phase {dep_phase} prerequisite ({artifact['file']})",
                passed=False,
                message=f"Phase {phase} requires Phase {dep_phase} artifact: {artifact['file']}",
                severity="BLOCK",
            ))

    return results


def check_status_md(spec_dir: Path) -> CheckResult:
    """Check STATUS.md exists and has required structure."""
    filepath = spec_dir / "STATUS.md"

    if not filepath.exists():
        return CheckResult(
            name="STATUS.md tracking",
            passed=False,
            message="STATUS.md missing — PM Hub cannot track this feature.",
            severity="WARN",
        )

    content = filepath.read_text(encoding="utf-8")

    # Check for YAML frontmatter or status field
    if "status:" not in content.lower():
        return CheckResult(
            name="STATUS.md structure",
            passed=False,
            message="STATUS.md missing 'status:' field.",
            severity="WARN",
        )

    return CheckResult(name="STATUS.md tracking", passed=True, message="OK")


def check_review_gate(spec_dir: Path) -> CheckResult:
    """Check if review-gate artifacts exist (indicates review was run)."""
    # Look for review/audit indicators in the spec directory or pm/reports
    review_indicators = [
        spec_dir / "review-report.md",
        spec_dir / "qa-test-report.md",
    ]

    # Also check if STATUS.md mentions review
    status_file = spec_dir / "STATUS.md"
    if status_file.exists():
        content = status_file.read_text(encoding="utf-8")
        if any(kw in content.lower() for kw in ["review", "audit", "qa", "passed"]):
            return CheckResult(
                name="Review gate completed",
                passed=True,
                message="Review mentioned in STATUS.md",
            )

    for indicator in review_indicators:
        if indicator.exists():
            return CheckResult(
                name="Review gate completed",
                passed=True,
                message=f"Found: {indicator.name}",
            )

    return CheckResult(
        name="Review gate completed",
        passed=False,
        message="No review/audit artifacts found. Run /review-gate before shipping.",
        severity="WARN",
    )


def check_spec_dir_exists(feature_id: str) -> tuple[Path | None, CheckResult | None]:
    """Check if the feature spec directory exists."""
    spec_dir = SPECS_DIR / feature_id

    if not spec_dir.exists():
        return None, CheckResult(
            name="Feature directory exists",
            passed=False,
            message=f"Directory not found: plans/specs/{feature_id}/",
            severity="BLOCK",
        )

    return spec_dir, None


def run_phase_check(feature_id: str, phase: int) -> ComplianceReport:
    """Run compliance checks for a specific phase."""
    report = ComplianceReport(feature_id, phase=phase)

    spec_dir, err = check_spec_dir_exists(feature_id)
    if err:
        report.add(err)
        return report

    # Check phase dependencies
    for dep_check in check_phase_dependencies(spec_dir, phase):
        report.add(dep_check)

    # Check current phase artifact
    if phase in PHASE_ARTIFACTS:
        report.add(check_artifact_exists(spec_dir, PHASE_ARTIFACTS[phase]))

    return report


def run_full_check(feature_id: str) -> ComplianceReport:
    """Run all compliance checks for a feature."""
    report = ComplianceReport(feature_id)

    spec_dir, err = check_spec_dir_exists(feature_id)
    if err:
        report.add(err)
        return report

    # Check all phase artifacts
    for phase_num, artifact in PHASE_ARTIFACTS.items():
        report.add(check_artifact_exists(spec_dir, artifact))

    # Check STATUS.md
    report.add(check_status_md(spec_dir))

    # Check review gate
    report.add(check_review_gate(spec_dir))

    return report


def log_compliance_event(report: ComplianceReport):
    """Log compliance check result to telemetry."""
    TELEMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": report.timestamp,
        "type": "compliance_check",
        "feature_id": report.feature_id,
        "phase": report.phase,
        "passed": report.passed,
        "block_count": report.block_count,
        "warn_count": report.warn_count,
    }

    with open(TELEMETRY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Guard Layer — Workflow Compliance Checker"
    )
    parser.add_argument("feature_id", help="Feature ID (directory name under plans/specs/)")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4], help="Check specific phase")
    parser.add_argument("--full", action="store_true", help="Run all compliance checks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.phase:
        report = run_phase_check(args.feature_id, args.phase)
    elif args.full:
        report = run_full_check(args.feature_id)
    else:
        report = run_full_check(args.feature_id)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        report.print_report()

    # Log to telemetry
    log_compliance_event(report)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
