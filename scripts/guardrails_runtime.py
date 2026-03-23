#!/usr/bin/env python3
from __future__ import annotations
"""
Guard Layer — Runtime Guardrails Evaluator.

Evaluates guardrails.json rules against current project state (STATE.md)
and user query to detect anti-pattern violations BEFORE routing to agents.

Usage:
    python3 scripts/guardrails_runtime.py --query "growth hacking" --state pm/STATE.md
    python3 scripts/guardrails_runtime.py --query "hire a developer" --stage 2
"""
import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
GUARDRAILS_FILE = PROJECT_ROOT / "data" / "guardrails.json"
STATE_FILE = PROJECT_ROOT / "pm" / "STATE.md"

# Domain signal keywords → guardrail domains to check
DOMAIN_SIGNALS = {
    "growth": ["growth", "scale", "marketing", "ads", "channel", "acquisition", "traffic",
               "seo", "social media", "content marketing", "viral", "growth hack"],
    "paid_ads": ["paid ads", "facebook ads", "google ads", "advertising", "ad campaign",
                 "ppc", "cpm", "spend on ads", "paid traffic"],
    "fundraising": ["fundraise", "raise money", "vc", "investor", "pitch deck",
                    "seed round", "series a", "angel investor", "venture capital"],
    "hiring": ["hire", "hiring", "recruit", "full-time", "team member",
               "job opening", "employee", "first hire"],
    "scaling": ["scale", "scaling", "grow fast", "10x", "expand"],
    "equity": ["equity", "shares", "stock", "vesting", "cap table",
               "ownership", "co-founder split"],
    "launch": ["launch", "product hunt", "go live", "release", "public launch",
               "ship it", "announce"],
    "finance": ["runway", "burn rate", "cash", "budget", "expenses"],
    "leverage": ["manual", "labor", "hire someone to", "outsource to humans"],
    "authenticity": ["brand", "positioning", "personal brand", "content strategy"],
    "content_safety": ["publish", "post"],
    "content_strategy": ["content", "publish", "blog"],
}


def parse_state_md(state_path: Path | None = None) -> dict:
    """Parse STATE.md into structured data."""
    path = state_path or STATE_FILE
    state = {
        "stage": 0,
        "project": "unknown",
        "current_focus": "",
        "active_blockers": "",
        "last_update": "",
    }

    if not path.exists():
        return state

    content = path.read_text(encoding="utf-8")

    # Extract stage number
    stage_match = re.search(r"\*\*Stage:\*\*\s*(\d+)", content)
    if stage_match:
        state["stage"] = int(stage_match.group(1))

    # Extract project name
    project_match = re.search(r"\*\*Project:\*\*\s*(.+?)(?:\n|$)", content)
    if project_match:
        state["project"] = project_match.group(1).strip()

    # Extract current focus
    focus_match = re.search(r"\*\*Current Focus:\*\*\s*(.+?)(?:\n|$)", content)
    if focus_match:
        state["current_focus"] = focus_match.group(1).strip()

    # Extract blockers
    blocker_match = re.search(r"\*\*Active Blockers:\*\*\s*(.+?)(?:\n|$)", content)
    if blocker_match:
        state["active_blockers"] = blocker_match.group(1).strip()

    # Extract last update
    update_match = re.search(r"\*\*Last Update:\*\*\s*(.+?)(?:\n|$)", content)
    if update_match:
        state["last_update"] = update_match.group(1).strip()

    return state


def detect_query_domains(query: str) -> list[str]:
    """Detect which guardrail domains a query might trigger."""
    query_lower = query.lower()
    triggered_domains = []

    for domain, keywords in DOMAIN_SIGNALS.items():
        for keyword in keywords:
            if keyword in query_lower:
                if domain not in triggered_domains:
                    triggered_domains.append(domain)
                break

    return triggered_domains


def evaluate_rule(rule: dict, state: dict, query_domains: list[str]) -> dict | None:
    """Evaluate a single guardrail rule against state and query.

    Returns violation dict if rule is triggered, None otherwise.
    """
    rule_domain = rule["domain"]

    # Rule only applies if query touches this domain
    if rule_domain not in query_domains:
        return None

    # Evaluate condition based on rule type
    condition = rule.get("condition", "")
    stage = state.get("stage", 0)
    triggered = False

    # Stage-based conditions
    if "stage <" in condition:
        stage_match = re.search(r"stage\s*<\s*(\d+)", condition)
        if stage_match:
            threshold = int(stage_match.group(1))
            if stage < threshold:
                triggered = True

    elif "stage ==" in condition:
        stage_match = re.search(r"stage\s*==\s*(\d+)", condition)
        if stage_match:
            threshold = int(stage_match.group(1))
            if stage == threshold:
                triggered = True

    # Domain-presence conditions (if query mentions the domain, rule fires)
    elif "action.domain IN" in condition:
        triggered = True  # Already filtered by domain match above

    elif "action.type ==" in condition:
        triggered = True  # Already filtered by domain match above

    elif "action.type IN" in condition:
        triggered = True

    elif "action.requires_manual_labor" in condition:
        triggered = True

    elif "action.aligned_with_founder_identity" in condition:
        triggered = True

    if not triggered:
        return None

    return {
        "id": rule["id"],
        "type": rule["type"],
        "domain": rule["domain"],
        "message": rule["message"],
        "severity": rule["severity"],
        "rationale": rule.get("rationale", ""),
    }


def evaluate_guardrails(
    query: str,
    state: dict | None = None,
    stage_override: int | None = None,
) -> list[dict]:
    """Evaluate all guardrails against query and state.

    Returns list of violation dicts.
    """
    if state is None:
        state = parse_state_md()

    if stage_override is not None:
        state["stage"] = stage_override

    # Load guardrails
    if not GUARDRAILS_FILE.exists():
        return []

    with open(GUARDRAILS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    rules = data.get("rules", [])
    query_domains = detect_query_domains(query)

    if not query_domains:
        return []

    violations = []
    for rule in rules:
        violation = evaluate_rule(rule, state, query_domains)
        if violation:
            violations.append(violation)

    # Sort: BLOCK first, then WARN
    violations.sort(key=lambda v: 0 if v["type"] == "BLOCK" else 1)

    return violations


def format_violations(violations: list[dict]) -> str:
    """Format violations for display."""
    if not violations:
        return "✅ No guardrail violations detected."

    lines = []
    blocks = [v for v in violations if v["type"] == "BLOCK"]
    warns = [v for v in violations if v["type"] == "WARN"]

    if blocks:
        lines.append("🛡️ BLOCKED:")
        for v in blocks:
            lines.append(f"  {v['message']}")
            lines.append(f"  └ Rationale: {v['rationale']}")
            lines.append("")

    if warns:
        lines.append("⚠️ WARNINGS:")
        for v in warns:
            lines.append(f"  {v['message']}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Guard Layer — Runtime Guardrails Evaluator"
    )
    parser.add_argument("--query", "-q", required=True, help="User query to evaluate")
    parser.add_argument("--state", type=Path, help="Path to STATE.md (default: pm/STATE.md)")
    parser.add_argument("--stage", type=int, help="Override stage number")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    state = parse_state_md(args.state) if args.state else parse_state_md()

    violations = evaluate_guardrails(
        query=args.query,
        state=state,
        stage_override=args.stage,
    )

    if args.json:
        print(json.dumps(violations, indent=2))
    else:
        print(format_violations(violations))

    # Exit code: 2 if BLOCK, 1 if WARN only, 0 if clean
    if any(v["type"] == "BLOCK" for v in violations):
        sys.exit(2)
    elif violations:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
