"""
EaseStart — Decision Impact Analysis Engine

Inspired by GitNexus's impact() tool. Traces upstream (what's affected)
and downstream (what you need) effects of startup decisions.

Zero external dependencies. Pure Python implementation.

Usage:
    python3 scripts/impact.py "switch to freemium pricing"
    python3 scripts/impact.py "hire first employee" --stage 2
"""

import csv
import sys
from pathlib import Path
from typing import Optional

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from core import (
    search,
    detect_domain,
    tokenize,
    CROSS_DOMAIN_LINKS,
    EASESTART_CONFIG,
    DATA_DIR,
    _find_anti_pattern_warnings,
)


IMPACT_RULES_FILE = DATA_DIR / "reasoning" / "impact-rules.csv"


def _load_impact_rules() -> list[dict]:
    """Load impact rules CSV."""
    if not IMPACT_RULES_FILE.exists():
        return []
    try:
        with open(IMPACT_RULES_FILE, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except (csv.Error, UnicodeDecodeError, IOError):
        return []


def _match_rule(decision: str, rules: list[dict]) -> Optional[dict]:
    """Find the best matching impact rule for a decision."""
    decision_lower = decision.lower()
    decision_tokens = set(tokenize(decision))

    best_match = None
    best_score = 0

    for rule in rules:
        keywords = rule.get("Keywords", "").lower().split(",")
        score = 0
        for kw in keywords:
            kw = kw.strip()
            if not kw:
                continue
            # Phrase match scores higher
            if kw in decision_lower:
                score += 3
            # Token overlap
            kw_tokens = set(tokenize(kw))
            overlap = decision_tokens & kw_tokens
            score += len(overlap)

        if score > best_score:
            best_score = score
            best_match = rule

    # Require minimum match quality
    if best_score < 2:
        return None

    return best_match


def _get_affected_domains(decision: str) -> list[str]:
    """Detect which knowledge domains a decision touches."""
    primary = detect_domain(decision)
    domains = []

    if primary:
        domains.append(primary)
        # Walk cross-domain links
        linked = CROSS_DOMAIN_LINKS.get(primary, [])
        domains.extend(linked)

    # Also detect secondary domains from decision text
    decision_lower = decision.lower()
    domain_hints = {
        "pricing": ["pricing", "fin_economics"],
        "hire": ["team_vetting", "team_equity", "legal", "contracts"],
        "cofounder": ["team_vetting", "team_equity", "contracts"],
        "funding": ["stages", "metrics", "legal"],
        "launch": ["mkt_channels", "mkt_landing", "tools"],
        "marketing": ["mkt_channels", "mkt_content", "mkt_email"],
        "legal": ["legal", "contracts", "security"],
        "pivot": ["stages", "frameworks", "reasoning"],
        "feature": ["tools", "metrics", "playbook"],
        "mobile": ["tools", "metrics"],
        "community": ["mkt_community", "ops_support"],
        "automat": ["ops_automation", "tools"],
        "content": ["mkt_content", "mkt_channels"],
        "international": ["legal", "mkt_channels", "ops_support"],
    }

    for hint, hint_domains in domain_hints.items():
        if hint in decision_lower:
            for d in hint_domains:
                if d not in domains:
                    domains.append(d)

    return domains[:8]  # Cap at 8 related domains


def analyze_impact(decision: str, stage: int = -1) -> dict:
    """
    Trace upstream/downstream effects of a startup decision.

    Args:
        decision: Description of the decision (e.g. "switch to freemium")
        stage: Current startup stage (0-6). -1 for no filter.

    Returns:
        Dict with target, risk_level, upstream, downstream,
        anti_patterns, related_domains, and rule_match.
    """
    stage_filter = stage if stage >= 0 else None
    rules = _load_impact_rules()
    matched_rule = _match_rule(decision, rules)

    # Build upstream (what's affected) and downstream (what's needed)
    upstream = []
    downstream = []
    anti_patterns = []
    risk_level = "LOW"

    if matched_rule:
        # Parse from rule
        for area in matched_rule.get("Upstream_Areas", "").split("|"):
            area = area.strip()
            if area:
                upstream.append({"area": area, "source": "impact-rules"})

        for need in matched_rule.get("Downstream_Needs", "").split("|"):
            need = need.strip()
            if need:
                downstream.append({"need": need, "source": "impact-rules"})

        risk_level = matched_rule.get("Risk_Level", "MEDIUM")

        stage_warning = matched_rule.get("Stage_Warning", "").strip()
        if stage_warning:
            anti_patterns.append(stage_warning)

        anti_pattern = matched_rule.get("Anti_Pattern", "").strip()
        if anti_pattern:
            anti_patterns.append(anti_pattern)

    # Enrich with cross-domain search
    affected_domains = _get_affected_domains(decision)

    for domain in affected_domains[:5]:
        # Search for related warnings
        warning = _find_anti_pattern_warnings(decision, domain, stage_filter)
        if warning:
            for w in warning.split(" | "):
                w = w.strip()
                if w and w not in anti_patterns:
                    anti_patterns.append(w)

        # Search for related knowledge
        results = search(decision, domain=domain, top_k=2, stage=stage_filter)
        for r in results:
            if r.get("_confidence") in ("HIGH", "MEDIUM"):
                # Add as related context
                label = r.get("Rule") or r.get("Strategy") or r.get("Name") or r.get("Stage") or ""
                if label and label not in [u.get("area") for u in upstream]:
                    upstream.append({
                        "area": f"{label} ({domain})",
                        "confidence": r.get("_confidence", "LOW"),
                        "source": domain,
                    })

    # Elevate risk if many anti-patterns found
    if len(anti_patterns) >= 3 and risk_level != "HIGH":
        risk_level = "HIGH"
    elif len(anti_patterns) >= 1 and risk_level == "LOW":
        risk_level = "MEDIUM"

    # Lucius L5: Map risk level to confidence
    confidence = {"HIGH": "LOW", "MEDIUM": "MEDIUM", "LOW": "HIGH"}.get(risk_level, "LOW")

    return {
        "target": decision,
        "risk_level": risk_level,
        "_confidence": confidence,
        "upstream": upstream[:8],
        "downstream": downstream[:6],
        "anti_patterns": anti_patterns[:5],
        "related_domains": affected_domains,
        "rule_match": matched_rule.get("Decision_Type", "") if matched_rule else None,
    }


def format_impact(result: dict) -> str:
    """Format impact analysis result as readable text."""
    lines = []
    risk_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(result["risk_level"], "⚪")

    lines.append(f"Decision Impact Analysis")
    lines.append(f"{'─' * 50}")
    lines.append(f"TARGET: {result['target']}")
    lines.append(f"RISK: {risk_icon} {result['risk_level']}")

    # Lucius L5 confidence
    confidence = result.get('_confidence', 'LOW')
    conf_icon = {"HIGH": "✅", "MEDIUM": "⁉️", "LOW": "⚠️"}.get(confidence, "⚠️")
    lines.append(f"CONFIDENCE: {conf_icon} {confidence}")
    if result.get("rule_match"):
        lines.append(f"MATCHED RULE: {result['rule_match']}")

    if result["upstream"]:
        lines.append(f"\nUPSTREAM (what's affected):")
        for u in result["upstream"]:
            confidence = u.get("confidence", "")
            conf_str = f" [{confidence}]" if confidence else ""
            lines.append(f"  ⚡ {u['area']}{conf_str}")

    if result["downstream"]:
        lines.append(f"\nDOWNSTREAM (what you need):")
        for d in result["downstream"]:
            lines.append(f"  📋 {d['need']}")

    if result["anti_patterns"]:
        lines.append(f"\n⚠️ WARNINGS:")
        for ap in result["anti_patterns"]:
            lines.append(f"  ❌ {ap}")

    if result["related_domains"]:
        lines.append(f"\nRELATED DOMAINS: {', '.join(result['related_domains'])}")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="EaseStart — Decision Impact Analysis",
    )
    parser.add_argument("decision", help="Describe the decision to analyze")
    parser.add_argument("--stage", "-s", type=int, default=-1, help="Current stage (0-6)")
    args = parser.parse_args()

    result = analyze_impact(args.decision, stage=args.stage)
    print(f"\n{format_impact(result)}\n")


if __name__ == "__main__":
    main()
