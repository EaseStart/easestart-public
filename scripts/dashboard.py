"""
EaseStart — Founder Dashboard
Local web dashboard showing startup progress, knowledge stats, and agent roster.

Command:
  python3 scripts/dashboard.py
  → Opens http://localhost:5050

Design:
  Based on DS-Foundations.md design tokens:
  - Monochrome: #000, #FFF, #4E4B66
  - Typography: Saira Condensed (headings, uppercase), SF Pro Rounded (body)
  - Layout: Flat design, no shadows, high-contrast

Install:
  pip install flask
  (Optional — dashboard is a bonus tool, not required for core EaseStart)
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, render_template_string
except ImportError:
    print("  ❌ Flask not installed. Install with:")
    print("     pip install flask")
    print()
    print("  Why Flask?")
    print("  The dashboard needs a local web server to render your startup")
    print("  progress visually. Flask is lightweight (~2MB) and runs locally.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from core import get_stats, EASESTART_CONFIG

PROJECT_ROOT = Path(__file__).parent.parent
PM_DIR = PROJECT_ROOT / "pm"
DATA_DIR = PROJECT_ROOT / "data"

app = Flask(__name__)

# -- Design System Tokens (from DS-Foundations.md) --
# Monochrome palette, Saira Condensed + system-ui, flat design

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EaseStart — Founder Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* DS-Foundations Tokens */
        :root {
            --color-bg-primary: #ffffff;
            --color-bg-inverse: #000000;
            --color-text-primary: #000000;
            --color-text-inverse: #ffffff;
            --color-text-secondary: #4e4b66;
            --color-border: #e0e0e0;
            --color-accent: #14b8a6;
            --color-warning: #f59e0b;
            --color-danger: #ef4444;
            --color-success: #22c55e;
            --font-heading: 'Saira Condensed', 'Impact', sans-serif;
            --font-body: 'ui-rounded', 'SF Pro Rounded', system-ui, sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: var(--font-body);
            background: var(--color-bg-primary);
            color: var(--color-text-primary);
            line-height: 1.5;
        }

        /* Header — inverse (black bg) */
        .header {
            background: var(--color-bg-inverse);
            color: var(--color-text-inverse);
            padding: 40px 48px;
        }
        .header h1 {
            font-family: var(--font-heading);
            font-size: 48px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }
        .header .subtitle {
            font-size: 16px;
            color: #999;
        }
        .stage-badge {
            display: inline-block;
            background: var(--color-accent);
            color: var(--color-bg-inverse);
            padding: 6px 16px;
            font-family: var(--font-heading);
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 12px;
        }

        /* Main content */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 48px;
        }

        /* Section headings */
        .section-heading {
            font-family: var(--font-heading);
            font-size: 32px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 24px;
            padding-bottom: 8px;
            border-bottom: 3px solid var(--color-bg-inverse);
        }

        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-bottom: 48px;
        }

        /* Cards — flat, no shadows */
        .card {
            border: 2px solid var(--color-bg-inverse);
            padding: 24px;
        }
        .card-title {
            font-family: var(--font-heading);
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--color-text-secondary);
            margin-bottom: 8px;
        }
        .card-value {
            font-size: 36px;
            font-weight: 700;
            line-height: 1.2;
        }
        .card-detail {
            font-size: 14px;
            color: var(--color-text-secondary);
            margin-top: 4px;
        }

        /* State section */
        .state-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 48px;
        }
        .state-item {
            padding: 16px;
            border-left: 3px solid var(--color-bg-inverse);
        }
        .state-label {
            font-family: var(--font-heading);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--color-text-secondary);
        }
        .state-value {
            font-size: 16px;
            margin-top: 4px;
        }

        /* Agent table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 48px;
        }
        th {
            font-family: var(--font-heading);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 3px solid var(--color-bg-inverse);
            color: var(--color-text-secondary);
        }
        td {
            padding: 10px 16px;
            border-bottom: 1px solid var(--color-border);
            font-size: 14px;
        }
        tr:hover { background: #f8f8f8; }

        /* Domain pills */
        .domain-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 48px;
        }
        .domain-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border: 1px solid var(--color-bg-inverse);
            font-size: 13px;
            font-family: var(--font-body);
        }
        .domain-pill .count {
            font-weight: 700;
            font-size: 12px;
            background: var(--color-bg-inverse);
            color: var(--color-text-inverse);
            padding: 2px 6px;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--color-text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--color-border);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header { padding: 24px; }
            .header h1 { font-size: 32px; }
            .container { padding: 24px; }
            .state-grid { grid-template-columns: 1fr; }
            .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <h1>{{ project_name }}</h1>
        <div class="subtitle">Founder Dashboard — EaseStart CLI</div>
        <div class="stage-badge">Stage {{ stage_num }} — {{ stage_name }}</div>
    </div>

    <div class="container">
        <!-- State Overview -->
        <h2 class="section-heading">Current State</h2>
        <div class="state-grid">
            <div class="state-item">
                <div class="state-label">Focus</div>
                <div class="state-value">{{ current_focus }}</div>
            </div>
            <div class="state-item">
                <div class="state-label">Key Decisions</div>
                <div class="state-value">{{ key_decisions }}</div>
            </div>
            <div class="state-item">
                <div class="state-label">Active Blockers</div>
                <div class="state-value">{{ active_blockers }}</div>
            </div>
            <div class="state-item">
                <div class="state-label">Last Update</div>
                <div class="state-value">{{ last_update }}</div>
            </div>
        </div>

        <!-- Knowledge Stats -->
        <h2 class="section-heading">Knowledge Base</h2>
        <div class="grid">
            <div class="card">
                <div class="card-title">Total Rows</div>
                <div class="card-value">{{ total_rows }}</div>
                <div class="card-detail">across {{ domain_count }} domains</div>
            </div>
            <div class="card">
                <div class="card-title">Agents</div>
                <div class="card-value">13</div>
                <div class="card-detail">specialist agents</div>
            </div>
            <div class="card">
                <div class="card-title">Workflows</div>
                <div class="card-value">11</div>
                <div class="card-detail">automated workflows</div>
            </div>
            <div class="card">
                <div class="card-title">Test Quality</div>
                <div class="card-value">{{ test_quality }}</div>
                <div class="card-detail">{{ test_detail }}</div>
            </div>
        </div>

        <!-- Domain Breakdown -->
        <h2 class="section-heading">Domains ({{ domain_count }})</h2>
        <div class="domain-grid">
            {% for domain, count in domains %}
            <div class="domain-pill">
                {{ domain }}
                <span class="count">{{ count }}</span>
            </div>
            {% endfor %}
        </div>

        <!-- Agent Roster -->
        <h2 class="section-heading">Agent Roster</h2>
        <table>
            <thead>
                <tr>
                    <th>Agent</th>
                    <th>Stages</th>
                    <th>Domain</th>
                </tr>
            </thead>
            <tbody>
                {% for agent in agents %}
                <tr>
                    <td><strong>{{ agent.name }}</strong></td>
                    <td>{{ agent.stages }}</td>
                    <td>{{ agent.domain }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="footer">
        EaseStart CLI · Generated {{ generated_at }} · Giantiny Philosophy
    </div>
</body>
</html>"""


def _parse_state():
    """Parse pm/STATE.md for dashboard data."""
    state_path = PM_DIR / "STATE.md"
    state = {
        "project_name": "EaseStart",
        "stage_num": "?",
        "stage_name": "Unknown",
        "current_focus": "—",
        "key_decisions": "—",
        "active_blockers": "None",
        "last_update": "—",
    }

    stage_names = {
        "0": "Pre-Idea", "1": "Ideation", "2": "Validation",
        "3": "MVP", "4": "Distribution", "5": "Growth", "6": "Scale",
    }

    if not state_path.exists():
        return state

    content = state_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("**Project:**"):
            state["project_name"] = line.replace("**Project:**", "").strip()
        elif line.startswith("**Stage:**"):
            raw = line.replace("**Stage:**", "").strip()
            # Extract number
            match = re.search(r"(\d+)", raw)
            if match:
                state["stage_num"] = match.group(1)
                state["stage_name"] = stage_names.get(state["stage_num"], raw)
        elif line.startswith("**Current Focus:**"):
            state["current_focus"] = line.replace("**Current Focus:**", "").strip()
        elif line.startswith("**Key Decisions:**"):
            state["key_decisions"] = line.replace("**Key Decisions:**", "").strip()
        elif line.startswith("**Active Blockers:**"):
            state["active_blockers"] = line.replace("**Active Blockers:**", "").strip()
        elif line.startswith("**Last Update:**"):
            state["last_update"] = line.replace("**Last Update:**", "").strip()
        elif line.startswith("**Last Test:**"):
            state["test_quality"] = line.replace("**Last Test:**", "").strip()

    return state


AGENTS = [
    {"name": "easestart-orchestrator", "stages": "0-6", "domain": "Routing + stage detection"},
    {"name": "ideation-agent", "stages": "0-1", "domain": "Ideas + Lean Canvas"},
    {"name": "validation-agent", "stages": "1-2", "domain": "Mom Test + PMF survey"},
    {"name": "mvp-agent", "stages": "2-3", "domain": "Tech stack + build"},
    {"name": "growth-agent", "stages": "3-5", "domain": "Channels + retention + pricing"},
    {"name": "fundraising-agent", "stages": "4-6", "domain": "VC + bootstrap + term sheets"},
    {"name": "ops-agent", "stages": "5-6", "domain": "Hiring + SOPs + MOATs"},
    {"name": "cofounder-agent", "stages": "0-4", "domain": "Team + equity + conflict"},
    {"name": "legal-agent", "stages": "1-6", "domain": "Legal + compliance + contracts"},
    {"name": "wellness-agent", "stages": "0-6", "domain": "Burnout + resilience"},
    {"name": "marketing-agent", "stages": "2-6", "domain": "Content + SEO + email + community"},
    {"name": "finance-agent", "stages": "2-6", "domain": "Bookkeeping + tax + cash flow"},
    {"name": "pm-agent", "stages": "0-6", "domain": "Daily ops + decisions + blockers"},
]


@app.route("/")
def dashboard():
    """Render the founder dashboard."""
    state = _parse_state()
    stats = get_stats()

    # Domain breakdown sorted by count
    domain_data = [(d, c) for d, c in sorted(stats.items(), key=lambda x: -x[1]) if d != "total"]

    return render_template_string(
        HTML_TEMPLATE,
        project_name=state["project_name"],
        stage_num=state["stage_num"],
        stage_name=state["stage_name"],
        current_focus=state["current_focus"],
        key_decisions=state["key_decisions"],
        active_blockers=state["active_blockers"],
        last_update=state["last_update"],
        total_rows=stats.get("total", 0),
        domain_count=len(stats) - 1,  # exclude 'total'
        test_quality=state.get("test_quality", "—"),
        test_detail="unit + simulation + evaluation",
        domains=domain_data,
        agents=AGENTS,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


if __name__ == "__main__":
    import webbrowser
    import threading

    port = 5050
    print(f"\n  🚀 EaseStart Dashboard")
    print(f"  {'─' * 40}")
    print(f"  Open: http://localhost:{port}")
    print(f"  Press Ctrl+C to stop")
    print()

    # Open browser after short delay
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    app.run(host="0.0.0.0", port=port, debug=False)
