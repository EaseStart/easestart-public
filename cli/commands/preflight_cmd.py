"""
EaseStart — Pre-flight Check Command

Validates a proposed action against guardrails.json BEFORE execution.
Enforces hard gates (BLOCK) and surfaces warnings (WARN) based on
the founder's current stage and action context.

Usage:
    easestart preflight "hire a marketing manager" --stage 2
    easestart preflight "run Facebook ads" --stage 3
    easestart preflight "raise seed round" --stage 1
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent.parent / "data"
GUARDRAILS_PATH = DATA_DIR / "guardrails.json"


def _load_guardrails() -> list[dict]:
    """Load guardrails rules from JSON."""
    if not GUARDRAILS_PATH.exists():
        return []
    with open(GUARDRAILS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("rules", [])


# Map action keywords to guardrail domains + conditions
ACTION_SIGNALS = {
    "growth": {
        "keywords": ["growth", "scale user", "acquire user", "user acquisition", "grow"],
        "domain": "growth",
    },
    "paid_ads": {
        "keywords": ["paid ad", "facebook ad", "google ad", "tiktok ad", "instagram ad",
                      "run ads", "paid advertising", "ad spend", "ad budget", "ppc",
                      "paid campaign", "boost post"],
        "domain": "paid_ads",
    },
    "fundraising": {
        "keywords": ["raise", "fundraise", "seed round", "series a", "vc", "investor",
                      "pitch deck for investors", "angel investor", "pre-seed"],
        "domain": "fundraising",
    },
    "hiring": {
        "keywords": ["hire", "recruit", "full-time", "full time", "employee",
                      "hiring manager", "job posting", "head of", "vp of"],
        "domain": "hiring",
    },
    "scaling": {
        "keywords": ["scale", "scaling", "expand market", "international expansion",
                      "new market", "scale acquisition"],
        "domain": "scaling",
    },
    "equity": {
        "keywords": ["equity", "shares", "stock", "cap table", "co-founder split",
                      "ownership", "equity split"],
        "domain": "equity",
    },
    "launch": {
        "keywords": ["launch", "public launch", "product hunt", "go live",
                      "announce", "press release"],
        "domain": "launch",
    },
    "channels": {
        "keywords": ["marketing channel", "new channel", "add channel",
                      "tiktok", "youtube", "podcast", "influencer"],
        "domain": "channels",
    },
    "content_branding": {
        "keywords": ["rebrand", "brand identity", "positioning change",
                      "change messaging", "new brand"],
        "domain": "authenticity",
    },
}


def _detect_action_domains(action: str) -> list[str]:
    """Detect which guardrail domains an action triggers."""
    action_lower = action.lower()
    triggered = []
    for signal_key, signal in ACTION_SIGNALS.items():
        for kw in signal["keywords"]:
            if kw in action_lower:
                domain = signal["domain"]
                if domain not in triggered:
                    triggered.append(domain)
                break
    return triggered


def _evaluate_rule(rule: dict, action: str, stage: int) -> Optional[dict]:
    """Evaluate a single guardrail rule against action + stage.
    Returns a result dict if the rule fires, None otherwise."""
    condition = rule.get("condition", "")
    domain = rule.get("domain", "")
    rule_type = rule.get("type", "WARN")

    # Stage-based conditions: extract "stage < N" patterns
    stage_match = re.search(r"stage\s*<\s*(\d+)", condition, re.IGNORECASE)
    if stage_match:
        threshold = int(stage_match.group(1))
        if stage >= threshold:
            return None  # Stage is high enough, rule doesn't fire

    # PMF score conditions (always flag as warning if scaling detected)
    pmf_match = re.search(r"pmf_score\s*<\s*(\d+)", condition, re.IGNORECASE)
    if pmf_match and domain == "scaling":
        # Can't verify PMF score programmatically, issue as advisory
        return {
            "rule_id": rule["id"],
            "type": "WARN",
            "domain": domain,
            "message": rule["message"] + " (Cannot verify PMF score — confirm manually)",
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Runway conditions (advisory — we can't know actual runway)
    runway_match = re.search(r"runway_months\s*<\s*(\d+)", condition, re.IGNORECASE)
    if runway_match and domain == "finance":
        return {
            "rule_id": rule["id"],
            "type": "WARN",
            "domain": domain,
            "message": rule["message"] + " (Check your actual runway)",
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Equity without vesting
    if domain == "equity" and "vesting" in condition.lower():
        return {
            "rule_id": rule["id"],
            "type": rule_type,
            "domain": domain,
            "message": rule["message"],
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Irreversible action warning
    if domain == "irreversible":
        return {
            "rule_id": rule["id"],
            "type": "WARN",
            "domain": domain,
            "message": rule["message"],
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Leverage test (manual labor)
    if domain == "leverage":
        action_lower = action.lower()
        manual_hints = ["manual", "hire", "person", "team", "staff", "employee",
                        "contractor", "va ", "virtual assistant"]
        if any(h in action_lower for h in manual_hints):
            return {
                "rule_id": rule["id"],
                "type": rule_type,
                "domain": domain,
                "message": rule["message"],
                "severity": rule["severity"],
                "rationale": rule.get("rationale", ""),
            }
        return None

    # Authenticity gate
    if domain == "authenticity":
        return {
            "rule_id": rule["id"],
            "type": "WARN",
            "domain": domain,
            "message": rule["message"] + " (Verify alignment with founder identity)",
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Consultation rule
    if domain == "consultation":
        return None  # Advisory only, skip in preflight

    # Context decay
    if domain == "context_decay":
        return None  # Handled by Context Decay system

    # Budget warning
    if domain == "budget":
        return {
            "rule_id": rule["id"],
            "type": "WARN",
            "domain": domain,
            "message": rule["message"],
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    # Platform risk
    if domain == "platform_risk":
        return None

    # Channel concentration
    if domain == "channels" and stage_match:
        threshold = int(stage_match.group(1))
        if stage < threshold:
            return {
                "rule_id": rule["id"],
                "type": rule_type,
                "domain": domain,
                "message": rule["message"],
                "severity": rule["severity"],
                "rationale": rule.get("rationale", ""),
            }
        return None

    # Default: if the rule has a stage gate and we passed it, fire
    if stage_match:
        return {
            "rule_id": rule["id"],
            "type": rule_type,
            "domain": domain,
            "message": rule["message"],
            "severity": rule["severity"],
            "rationale": rule.get("rationale", ""),
        }

    return None


def run_preflight(args) -> None:
    """Run pre-flight guardrail checks against a proposed action."""
    action = args.action
    stage = args.stage

    if not action:
        print("  ❌ No action specified. Usage: easestart preflight \"your action\" --stage N")
        sys.exit(1)

    if stage is None:
        print("  ❌ --stage is required for preflight checks.")
        print("  Usage: easestart preflight \"hire marketing manager\" --stage 2")
        sys.exit(1)

    rules = _load_guardrails()
    if not rules:
        print("  ⚠️ No guardrails found. Check data/guardrails.json")
        sys.exit(1)

    # Detect which domains this action touches
    triggered_domains = _detect_action_domains(action)

    # Evaluate all relevant rules
    blocks = []
    warnings = []

    for rule in rules:
        rule_domain = rule.get("domain", "")

        # Check rules whose domain matches triggered domains
        should_check = (
            rule_domain in triggered_domains
            or rule_domain in ("irreversible", "budget", "leverage", "consultation",
                                "context_decay", "platform_risk")
        )
        if not should_check:
            continue

        result = _evaluate_rule(rule, action, stage)
        if result is None:
            continue

        if result["type"] == "BLOCK":
            blocks.append(result)
        else:
            warnings.append(result)

    # --- Output ---
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║  🛫 EaseStart Pre-flight Check                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print(f"  ACTION:  {action}")
    print(f"  STAGE:   {stage}")
    print(f"  DOMAINS: {', '.join(triggered_domains) if triggered_domains else '(none detected)'}")
    print()

    if not blocks and not warnings:
        print("  ✅ ALL CLEAR — No guardrails triggered.")
        print("  Action is safe to proceed at Stage {}.".format(stage))
        print()
        return

    if blocks:
        print(f"  🛑 BLOCKED ({len(blocks)} hard gate{'s' if len(blocks) > 1 else ''}):")
        print("  " + "─" * 52)
        for b in blocks:
            print(f"  [{b['rule_id']}] {b['message']}")
            if b.get("rationale"):
                print(f"         WHY: {b['rationale']}")
            print()

    if warnings:
        print(f"  ⚠️  WARNINGS ({len(warnings)}):")
        print("  " + "─" * 52)
        for w in warnings:
            print(f"  [{w['rule_id']}] {w['message']}")
            if w.get("rationale"):
                print(f"         WHY: {w['rationale']}")
            print()

    # Verdict
    if blocks:
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║  ❌ VERDICT: ACTION BLOCKED                     ║")
        print("  ║  Resolve hard gates before proceeding.          ║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()
        sys.exit(1)
    else:
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║  ⚠️  VERDICT: PROCEED WITH CAUTION              ║")
        print("  ║  Review warnings above before executing.        ║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()
