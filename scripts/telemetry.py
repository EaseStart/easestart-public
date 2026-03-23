#!/usr/bin/env python3
from __future__ import annotations
"""
Track Layer — Workflow Telemetry.

Lightweight event logging for workflow execution. Tracks which workflows ran,
gates passed/failed, and compliance check results. Generates compliance reports.

Usage:
    python3 scripts/telemetry.py log --type workflow_start --workflow feature-dev --agent mvp-agent
    python3 scripts/telemetry.py log --type gate_pass --workflow feature-dev --details "Phase 2 gate passed"
    python3 scripts/telemetry.py report
    python3 scripts/telemetry.py report --last 7
"""
import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PM_DIR = PROJECT_ROOT / "pm"
TELEMETRY_FILE = PM_DIR / "telemetry.jsonl"

VALID_EVENT_TYPES = [
    "workflow_start",
    "workflow_complete",
    "gate_pass",
    "gate_fail",
    "compliance_check",
    "audit_skip",
    "guardrail_violation",
    "agent_route",
    "session_start",
    "session_end",
]


def log_event(
    event_type: str,
    workflow: str = "",
    agent: str = "",
    details: str = "",
    metadata: dict | None = None,
):
    """Append a telemetry event to the log."""
    TELEMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "workflow": workflow,
        "agent": agent,
        "details": details,
    }
    if metadata:
        event["metadata"] = metadata

    with open(TELEMETRY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event


def read_events(last_days: int | None = None) -> list[dict]:
    """Read all telemetry events, optionally filtered by recency."""
    if not TELEMETRY_FILE.exists():
        return []

    events = []
    cutoff = None
    if last_days is not None:
        cutoff = datetime.now() - timedelta(days=last_days)

    with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if cutoff:
                    event_time = datetime.fromisoformat(event["timestamp"])
                    if event_time < cutoff:
                        continue
                events.append(event)
            except (json.JSONDecodeError, KeyError):
                continue

    return events


def generate_report(last_days: int | None = None) -> dict:
    """Analyze telemetry events and generate compliance report."""
    events = read_events(last_days)

    if not events:
        return {
            "period": f"Last {last_days} days" if last_days else "All time",
            "total_events": 0,
            "message": "No telemetry data found.",
        }

    type_counts = Counter(e["type"] for e in events)
    workflow_counts = Counter(
        e["workflow"] for e in events if e.get("workflow")
    )
    agent_counts = Counter(
        e["agent"] for e in events if e.get("agent")
    )

    # Compute compliance rate
    gate_passes = type_counts.get("gate_pass", 0)
    gate_fails = type_counts.get("gate_fail", 0)
    total_gates = gate_passes + gate_fails
    compliance_rate = (gate_passes / total_gates * 100) if total_gates > 0 else None

    # Compute completion rate
    workflow_starts = type_counts.get("workflow_start", 0)
    workflow_completes = type_counts.get("workflow_complete", 0)
    completion_rate = (
        workflow_completes / workflow_starts * 100
    ) if workflow_starts > 0 else None

    # Detect audit skips
    audit_skips = type_counts.get("audit_skip", 0)

    # Guardrail violations
    violations = [e for e in events if e["type"] == "guardrail_violation"]
    violation_count = len(violations)

    report = {
        "period": f"Last {last_days} days" if last_days else "All time",
        "total_events": len(events),
        "event_breakdown": dict(type_counts),
        "workflows_started": workflow_starts,
        "workflows_completed": workflow_completes,
        "completion_rate": f"{completion_rate:.0f}%" if completion_rate is not None else "N/A",
        "gate_passes": gate_passes,
        "gate_fails": gate_fails,
        "compliance_rate": f"{compliance_rate:.0f}%" if compliance_rate is not None else "N/A",
        "audit_skips": audit_skips,
        "guardrail_violations": violation_count,
        "top_workflows": dict(workflow_counts.most_common(5)),
        "top_agents": dict(agent_counts.most_common(5)),
    }

    # Compliance health
    if compliance_rate is not None:
        if compliance_rate >= 90:
            report["health"] = "🟢 HEALTHY"
        elif compliance_rate >= 70:
            report["health"] = "🟡 NEEDS ATTENTION"
        else:
            report["health"] = "🔴 CRITICAL"
    else:
        report["health"] = "⚪ NO DATA"

    if audit_skips > 0:
        report["health_notes"] = f"⚠️ {audit_skips} audit steps were skipped."

    return report


def format_report(report: dict) -> str:
    """Format report for terminal display."""
    lines = [
        "=" * 60,
        f"  📊 Compliance Report — {report['period']}",
        "=" * 60,
        "",
    ]

    if report["total_events"] == 0:
        lines.append("  No telemetry data found.")
        return "\n".join(lines)

    lines.extend([
        f"  Health: {report['health']}",
        f"  Total events: {report['total_events']}",
        "",
        "  📈 Workflow Execution:",
        f"    Started:    {report['workflows_started']}",
        f"    Completed:  {report['workflows_completed']}",
        f"    Completion: {report['completion_rate']}",
        "",
        "  🛡️ Gate Compliance:",
        f"    Passed:     {report['gate_passes']}",
        f"    Failed:     {report['gate_fails']}",
        f"    Rate:       {report['compliance_rate']}",
        "",
        f"  ⚠️  Audit skips:          {report['audit_skips']}",
        f"  🚨 Guardrail violations:  {report['guardrail_violations']}",
    ])

    if report.get("health_notes"):
        lines.append(f"\n  {report['health_notes']}")

    if report.get("top_workflows"):
        lines.append("\n  🔄 Top Workflows:")
        for wf, count in report["top_workflows"].items():
            lines.append(f"    {wf}: {count} events")

    if report.get("top_agents"):
        lines.append("\n  🤖 Top Agents:")
        for agent, count in report["top_agents"].items():
            lines.append(f"    {agent}: {count} events")

    lines.append(f"\n{'─' * 60}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Track Layer — Workflow Telemetry"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a telemetry event")
    log_parser.add_argument("--type", "-t", required=True, choices=VALID_EVENT_TYPES)
    log_parser.add_argument("--workflow", "-w", default="")
    log_parser.add_argument("--agent", "-a", default="")
    log_parser.add_argument("--details", "-d", default="")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate compliance report")
    report_parser.add_argument("--last", type=int, help="Days to include (default: all)")
    report_parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.command == "log":
        event = log_event(
            event_type=args.type,
            workflow=args.workflow,
            agent=args.agent,
            details=args.details,
        )
        print(f"✅ Logged: {event['type']} ({event['timestamp'][:19]})")

    elif args.command == "report":
        report = generate_report(last_days=args.last)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_report(report))


if __name__ == "__main__":
    main()
