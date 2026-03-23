"""
EaseStart CLI — init command

3-Phase Pipeline (inspired by ClaudeKit's 8-phase, simplified):
  Phase 1: DETECT  — Python version, AI IDE, project structure
  Phase 2: INSTALL — Clone data + agents + MCP config
  Phase 3: CONFIGURE — Stage selection, first search verification
"""

import json
import os
import platform
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_URL = "https://github.com/EaseStart/easestart.git"

# IDE detection: config file paths
IDE_CONFIGS = {
    "claude": {
        "name": "Claude Desktop",
        "config_paths": [
            Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",  # macOS
            Path.home() / ".config" / "claude" / "claude_desktop_config.json",  # Linux
        ],
        "detect_dirs": [".claude"],
    },
    "cursor": {
        "name": "Cursor",
        "config_paths": [
            Path.home() / ".cursor" / "mcp.json",
        ],
        "detect_dirs": [".cursor"],
    },
    "windsurf": {
        "name": "Windsurf",
        "config_paths": [
            Path.home() / ".windsurf" / "mcp.json",
        ],
        "detect_dirs": [".windsurf"],
    },
    "gemini": {
        "name": "Gemini (Antigravity)",
        "config_paths": [
            Path.home() / ".gemini" / "settings.json",
        ],
        "detect_dirs": [".gemini"],
    },
}

STAGES = {
    0: "Pre-Idea — You have a problem but no clear idea",
    1: "Ideation — You have ideas, need to pick the best one",
    2: "Validation — Testing your idea with real customers",
    3: "MVP — Building the first version",
    4: "Product-Market Fit — Users love it, need to prove it",
    5: "Growth — Scaling acquisition and revenue",
    6: "Scale — Building team and processes",
}

# UX Psychology: Diderot Effect — every outcome leads to a natural next action.
# Each stage maps to personalized suggestions so the founder always knows what to do next.
STAGE_NEXT_STEPS = {
    0: {
        "primary": "/startup-journey",
        "primary_desc": "Guided problem discovery — find problems worth solving",
        "secondary": 'easestart search "problems worth solving"',
        "secondary_desc": "Explore the knowledge base for inspiration",
        "tip": "Start by listing 3 problems YOU personally face. Customer Zero = strongest signal.",
    },
    1: {
        "primary": "/validate-idea",
        "primary_desc": "End-to-end idea validation — DOV scoring + Lean Canvas",
        "secondary": 'easestart search "lean canvas"',
        "secondary_desc": "Learn about Lean Canvas frameworks",
        "tip": "Don't skip Founder-Opportunity Fit. Ideas without domain expertise fail 3x more.",
    },
    2: {
        "primary": "/validate-idea",
        "primary_desc": "Deploy + observe + interview — behavioral validation",
        "secondary": 'easestart preflight "interview customers" --stage 2',
        "secondary_desc": "Check guardrails before customer interviews",
        "tip": "Talk to 15 users who TRIED your product, not hypothetical ones.",
    },
    3: {
        "primary": "/build-mvp",
        "primary_desc": "Scope → tech stack → sprint plan → deploy",
        "secondary": 'easestart search "mvp pattern"',
        "secondary_desc": "Explore MVP patterns (Concierge, Wizard of Oz, etc.)",
        "tip": "Build the ONE feature that solves the Weakchain. Nothing else.",
    },
    4: {
        "primary": "/sprint-growth",
        "primary_desc": "Channel selection + pricing optimization + PMF measurement",
        "secondary": 'easestart search "pmf survey sean ellis"',
        "secondary_desc": "Learn about Product-Market Fit measurement",
        "tip": "40%+ users must be 'very disappointed' without you. Below that = iterate.",
    },
    5: {
        "primary": "/sprint-growth",
        "primary_desc": "Scale acquisition channels + optimize unit economics",
        "secondary": 'easestart search "unit economics ltv cac"',
        "secondary_desc": "Check your LTV:CAC ratio health",
        "tip": "Focus on 1 channel until it's exhausted. Multi-channel too early kills startups.",
    },
    6: {
        "primary": "/daily-ops",
        "primary_desc": "PM standup — blocker triage, priority setting, accountability",
        "secondary": 'easestart search "hiring playbook first hire"',
        "secondary_desc": "Learn when and how to make your first hire",
        "tip": "Document SOPs before hiring. No SOPs = no delegation = you become the bottleneck.",
    },
}


def _print_phase(phase: int, title: str):
    print(f"\n{'─' * 50}")
    print(f"  Phase {phase}: {title}")
    print(f"{'─' * 50}")


def _check(label: str, ok: bool, detail: str = ""):
    icon = "✅" if ok else "❌"
    suffix = f" — {detail}" if detail else ""
    print(f"  {icon} {label}{suffix}")
    return ok


def _detect_ide() -> Optional[str]:
    """Auto-detect installed AI IDE."""
    for ide_key, config in IDE_CONFIGS.items():
        for cfg_path in config["config_paths"]:
            if cfg_path.exists():
                return ide_key
        # Check for project-level dirs
        for d in config["detect_dirs"]:
            if Path(d).exists():
                return ide_key
    return None


def _detect_python() -> tuple[bool, str]:
    """Check Python version >= 3.9."""
    version = sys.version_info
    ok = version >= (3, 9)
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return ok, version_str


def _detect_git() -> bool:
    """Check if git is available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _detect_dap() -> tuple[bool, str]:
    """Check if dap (Debug Adapter Protocol CLI) is available."""
    try:
        result = subprocess.run(
            ["dap", "--help"], capture_output=True, text=True, timeout=5
        )
        return True, "available"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False, "not found (install: brew install AlmogBaku/tap/dap)"


def _install_mcp_config(ide: str, easestart_path: Path):
    """Install MCP server config for the detected IDE."""
    config = IDE_CONFIGS.get(ide)
    if not config:
        return

    mcp_entry = {
        "easestart": {
            "command": "uv",
            "args": [
                "run", "--directory",
                str(easestart_path / "mcp-server"),
                "python", "server.py"
            ]
        }
    }

    for cfg_path in config["config_paths"]:
        if cfg_path.parent.exists():
            # Read existing config or create new
            existing = {}
            if cfg_path.exists():
                try:
                    with open(cfg_path, "r") as f:
                        existing = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            if "mcpServers" not in existing:
                existing["mcpServers"] = {}

            existing["mcpServers"].update(mcp_entry)

            cfg_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cfg_path, "w") as f:
                json.dump(existing, f, indent=2)

            print(f"  ✅ MCP config written to {cfg_path}")
            return

    print(f"  ⚠️  Could not find config directory for {config['name']}")


def _detect_gcloud() -> tuple[bool, str]:
    """Check if gcloud CLI is available and which account is active."""
    try:
        result = subprocess.run(
            ["gcloud", "config", "get", "account"],
            capture_output=True, text=True, timeout=5
        )
        account = result.stdout.strip()
        if account:
            return True, account
        return True, "(no active account)"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False, "not found"


def _detect_gws() -> tuple[bool, str]:
    """Check if gws CLI is installed."""
    try:
        result = subprocess.run(
            ["gws", "--version"], capture_output=True, text=True, timeout=5
        )
        version = result.stdout.strip()
        return True, version if version else "installed"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False, "not installed"


def _detect_gws_auth() -> tuple[bool, str]:
    """Check if gws is authenticated (has valid token)."""
    try:
        result = subprocess.run(
            ["gws", "auth", "status"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return True, "authenticated"
        return False, "not authenticated"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False, "unknown"


def _gcloud_list_accounts() -> list[str]:
    """List all authenticated gcloud accounts."""
    try:
        result = subprocess.run(
            ["gcloud", "auth", "list", "--format=value(account)"],
            capture_output=True, text=True, timeout=5
        )
        return [a.strip() for a in result.stdout.strip().split("\n") if a.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []


def _run_gws_powerup(args) -> bool:
    """Phase 4: POWER-UP — Interactive gws setup.
    
    UX Psychology applied:
    - Progressive Disclosure: only shown after core setup succeeds
    - Commitment & Consistency: small yes (stage) → medium yes (gws)
    - Default Effect: Enter = skip, no pressure
    
    Returns True if gws was successfully connected.
    """
    # Step 1: Auto-detect environment
    gcloud_ok, gcloud_account = _detect_gcloud()
    gws_ok, gws_version = _detect_gws()
    gws_auth_ok, _ = _detect_gws_auth() if gws_ok else (False, "")

    # Already authenticated? Skip entirely.
    if gws_auth_ok:
        print("  ✅ Google Workspace already connected")
        return True

    # No gcloud? Can't proceed — skip gracefully.
    if not gcloud_ok:
        print("  ⚠️  gcloud CLI not found — skipping Google Workspace setup")
        print("  💡 Install gcloud first, then run /gws-setup anytime")
        return False

    # Show value proposition before asking
    print("""
  EaseStart agents can connect to your Google Workspace
  to execute actions directly:

    📅 Calendar — auto-pull schedule, create events
    📧 Gmail    — triage inbox, draft replies
    📊 Sheets   — track metrics, log momentum
    📁 Drive    — manage SOPs and documents
    ✅ Tasks    — create blockers, track to-dos
""")

    # The ask — Default is skip (N), no pressure
    try:
        answer = input("  Connect Google Workspace now? (y/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = "n"
        print()

    if answer != "y":
        print("\n  👍 No worries! Run /gws-setup anytime to connect later.")
        return False

    # ── User said YES — guided setup ──
    print()

    # Step 2: Install gws if needed
    if not gws_ok:
        # Check npm exists first
        try:
            subprocess.run(["npm", "--version"], capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            _check("gws CLI", False, "npm not found — install Node.js first")
            print("  💡 Install Node.js from https://nodejs.org, then run /gws-setup")
            return False

        print("  ⏳ Installing gws CLI...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "@googleworkspace/cli"],
                capture_output=True, check=True, timeout=60
            )
            _check("gws CLI", True, "installed")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            _check("gws CLI", False, f"install failed: {e}")
            print("  💡 Try manually: npm install -g @googleworkspace/cli")
            return False
    else:
        _check("gws CLI", True, gws_version)

    # Step 3: Pick Google account
    accounts = _gcloud_list_accounts()
    email = ""

    if len(accounts) == 1:
        email = accounts[0]
        print(f"\n  Using account: {email}")
    elif len(accounts) > 1:
        print("\n  Available Google accounts:")
        for i, acc in enumerate(accounts, 1):
            marker = " ←" if acc == gcloud_account else ""
            print(f"    [{i}] {acc}{marker}")
        try:
            choice = input(f"\n  Which account? (1-{len(accounts)}): ").strip()
            idx = int(choice) - 1 if choice.isdigit() else 0
            email = accounts[max(0, min(idx, len(accounts) - 1))]
        except (EOFError, KeyboardInterrupt, ValueError):
            email = accounts[0]
            print()
    else:
        try:
            email = input("\n  Enter your Google email: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  ⚠️  Skipping. Run /gws-setup later.")
            return False

    if not email:
        print("  ⚠️  No email provided. Run /gws-setup later.")
        return False

    print(f"  ✅ Account: {email}")

    # Step 4: Create GCP project (automated)
    project_id = f"easestart-gws-{random.randint(1000, 9999)}"

    print(f"\n  ⏳ Creating GCP project ({project_id})...")
    try:
        subprocess.run(
            ["gcloud", "config", "set", "account", email],
            capture_output=True, check=True, timeout=10
        )
        subprocess.run(
            ["gcloud", "projects", "create", project_id,
             f"--name=EaseStart GWS", "--set-as-default"],
            capture_output=True, check=True, timeout=30
        )
        _check("GCP project", True, project_id)
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else str(e)
        if "already exists" in stderr:
            _check("GCP project", True, f"{project_id} (exists)")
        else:
            _check("GCP project", False, stderr[:100])
            print("  💡 You can create it manually and run /gws-setup")
            return False

    # Step 5: Enable APIs (automated)
    apis = [
        "calendar-json.googleapis.com", "drive.googleapis.com",
        "sheets.googleapis.com", "gmail.googleapis.com",
        "docs.googleapis.com", "slides.googleapis.com",
        "tasks.googleapis.com", "chat.googleapis.com",
    ]
    print("\n  ⏳ Enabling 8 Google APIs...")
    try:
        subprocess.run(
            ["gcloud", "services", "enable"] + apis,
            capture_output=True, check=True, timeout=60
        )
        _check("APIs", True, "8 services enabled")
    except subprocess.CalledProcessError as e:
        _check("APIs", False, "some APIs failed — run /gws-setup to retry")

    # Step 6: Manual steps — OAuth (can't be automated)
    print(f"""
  ╔══════════════════════════════════════════════════╗
  ║  ⚠️  One manual step needed (Google requires it) ║
  ╚══════════════════════════════════════════════════╝

  Open these 2 links in your browser:

  1️⃣  OAuth Consent Screen:
     https://console.cloud.google.com/apis/credentials/consent?project={project_id}
     → Select "External" → App name: "gws CLI"
     → Add your email as support + developer contact
     → Save through all screens
     → ⚠️ Go to "Test users" → Add: {email}

  2️⃣  Create OAuth Client:
     https://console.cloud.google.com/apis/credentials?project={project_id}
     → "+ CREATE CREDENTIALS" → "OAuth client ID"
     → Type: "Desktop app" (⚠️ NOT Web application!)
     → Name: "gws CLI" → Create → Download JSON
""")

    try:
        input("  Press Enter when you've downloaded the JSON... ")
    except (EOFError, KeyboardInterrupt):
        print("\n  💡 Complete this later with /gws-setup")
        return False

    # Move JSON to correct location
    gws_config = Path.home() / ".config" / "gws"
    gws_config.mkdir(parents=True, exist_ok=True)
    downloads = Path.home() / "Downloads"
    json_files = sorted(downloads.glob("client_secret_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

    if json_files:
        target = gws_config / "client_secret.json"
        shutil.copy2(json_files[0], target)
        _check("OAuth JSON", True, f"saved to {target}")

        # Verify it's Desktop type
        try:
            with open(target) as f:
                data = json.load(f)
            if "installed" not in data:
                print("  ❌ Wrong type! You selected 'Web application' instead of 'Desktop app'.")
                print("     Please go back and create a new OAuth client with type 'Desktop app'.")
                return False
        except (json.JSONDecodeError, IOError):
            pass
    else:
        print("  ⚠️  No client_secret JSON found in Downloads.")
        print("  💡 Download it and run: mv ~/Downloads/client_secret_*.json ~/.config/gws/client_secret.json")
        return False

    # Step 7: Login
    print("\n  ⏳ Starting gws login (browser will open)...")
    try:
        result = subprocess.run(
            ["gws", "auth", "login", "-s",
             "drive,gmail,sheets,calendar,tasks,slides,docs,chat"],
            timeout=120
        )
        if result.returncode == 0:
            _check("gws auth", True, f"connected as {email}")
            return True
        else:
            _check("gws auth", False, "login failed — run /gws-setup to retry")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        _check("gws auth", False, "timeout — run /gws-setup to retry")
        return False


def _show_first_win(gws_connected: bool, easestart_dir: Path):
    """Phase 5: FIRST WIN — demonstrate a live capability.
    
    UX Psychology: Peak-End Rule — end with a wow moment.
    """
    if gws_connected:
        # Show live calendar data
        print("\n  🎯 Let's see your schedule today:\n")
        try:
            result = subprocess.run(
                ["gws", "calendar", "+agenda", "--today"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                for line in output.split("\n"):
                    if "keyring" not in line.lower():
                        print(f"     {line}")
                print("\n  ✨ Your PM agent can now use this data in /daily-ops!")
            else:
                print("  ✨ Google Workspace connected! Try: gws calendar +agenda --today")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("  ✨ Google Workspace connected! Try: gws calendar +agenda --today")
    else:
        # Show knowledge search
        print("\n  🎯 Let's try your first knowledge search:\n")
        try:
            sys.path.insert(0, str(easestart_dir))
            from scripts.core import search
            results = search("how to validate a startup idea", top_k=2)
            for r in results[:2]:
                source = r.get("source", "unknown")
                text = r.get("text", "")[:80]
                print(f"     📄 [{source}] {text}...")
            if results:
                print("\n  ✨ Your agents can search 80+ frameworks like this!")
        except Exception:
            print("  ✨ Try: easestart search \"how to validate a startup idea\"")


def _show_capability_status(stage: int, gws_connected: bool, stats: dict):
    """Show setup completeness with progress bar (Zeigarnik Effect).
    
    Incomplete items drive future action without being pushy.
    """
    items = [
        ("Core knowledge loaded", True),
        ("Search engine ready", stats.get("total", 0) > 0),
        (f"Stage detected (Stage {stage})", True),
        ("Google Workspace connected", gws_connected),
    ]

    done = sum(1 for _, ok in items if ok)
    total = len(items)
    pct = int(done / total * 100)
    filled = int(pct / 100 * 16)

    print(f"\n  Your EaseStart Setup:")
    print(f"  {'█' * filled}{'░' * (16 - filled)}  {pct}% complete\n")

    for label, ok in items:
        icon = "✅" if ok else "⬜"
        suffix = ""
        if not ok and "Workspace" in label:
            suffix = "  ← Run /gws-setup to unlock"
        print(f"  {icon} {label}{suffix}")


def run_init(args):
    """Execute the init command: 5-phase UX-driven pipeline.

    Phase 1: DETECT     — Auto-detect environment (no input)
    Phase 2: INSTALL    — Clone data + agents + MCP config
    Phase 3: CONFIGURE  — Stage selection (interactive)
    Phase 4: POWER-UP   — Optional Google Workspace connection
    Phase 5: FIRST WIN  — Live demo for wow moment
    """
    print(f"\n🚀 EaseStart — Initializing...\n")

    # First-time vs re-init detection
    easestart_marker = Path.cwd() / ".easestart_initialized"
    is_reinit = easestart_marker.exists()

    # ── Phase 1: DETECT ──
    _print_phase(1, "DETECT")

    # Python
    py_ok, py_version = _detect_python()
    _check("Python", py_ok, f"v{py_version}" if py_ok else f"v{py_version} (need ≥3.9)")
    if not py_ok:
        print("\n  ❌ Python 3.9+ required. Aborting.")
        sys.exit(1)

    # Git
    git_ok = _detect_git()
    _check("Git", git_ok, "available" if git_ok else "not found")

    # IDE
    if args.ide == "auto":
        detected_ide = _detect_ide()
    else:
        detected_ide = args.ide

    if detected_ide:
        _check("IDE", True, IDE_CONFIGS[detected_ide]["name"])
    else:
        _check("IDE", False, "none detected (use --ide to specify)")

    # dap (interactive debugger)
    dap_ok, dap_detail = _detect_dap()
    _check("dap (debugger)", dap_ok, dap_detail)

    # Platform
    _check("Platform", True, f"{platform.system()} {platform.machine()}")

    # ── Phase 2: INSTALL ──
    _print_phase(2, "INSTALL")

    cwd = Path.cwd()
    easestart_dir = cwd

    # Check if we're already in an EaseStart project
    if (cwd / "scripts" / "core.py").exists():
        print("  ✅ Already in EaseStart project")
    elif (cwd / "easestart" / "scripts" / "core.py").exists():
        easestart_dir = cwd / "easestart"
        print("  ✅ Found EaseStart in ./easestart/")
    else:
        # Clone from GitHub
        if not git_ok:
            print("  ❌ Git required to clone EaseStart. Install git first.")
            sys.exit(1)

        print("  ⏳ Cloning from GitHub...")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", REPO_URL],
                check=True, capture_output=True
            )
            easestart_dir = cwd / "easestart"
            print("  ✅ Cloned successfully")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Clone failed: {e.stderr.decode()[:200]}")
            sys.exit(1)

    # Verify installation
    data_dir = easestart_dir / "data"
    if data_dir.exists():
        csv_count = len(list(data_dir.rglob("*.csv")))
        _check("Data", csv_count > 0, f"{csv_count} CSV files found")
    else:
        _check("Data", False, "data/ not found")

    agents_dir = easestart_dir / ".agent" / "agents"
    if agents_dir.exists():
        agent_count = len(list(agents_dir.glob("*.md")))
        _check("Agents", agent_count > 0, f"{agent_count} agent definitions")
    else:
        _check("Agents", False, ".agent/agents/ not found")

    # Install MCP config if IDE detected
    if detected_ide:
        _install_mcp_config(detected_ide, easestart_dir)

    # ── Phase 3: CONFIGURE ──
    _print_phase(3, "CONFIGURE")

    # Stage selection
    stage = args.stage
    if stage is None and not args.yes:
        print("\n  What stage is your startup at?\n")
        for s, desc in STAGES.items():
            print(f"    [{s}] {desc}")
        print()
        try:
            stage_input = input("  Enter stage (0-6): ").strip()
            stage = int(stage_input) if stage_input.isdigit() and 0 <= int(stage_input) <= 6 else 0
        except (EOFError, KeyboardInterrupt):
            stage = 0
            print()
    elif stage is None:
        stage = 0

    print(f"  ✅ Stage set to {stage} — {STAGES[stage].split('—')[0].strip()}")

    # Verify search works
    stats = {}
    print("\n  ⏳ Running verification search...")
    try:
        sys.path.insert(0, str(easestart_dir))
        from scripts.core import search, get_stats
        stats = get_stats()
        results = search("startup idea validation", top_k=1)
        _check("Search", len(results) > 0, f"{stats.get('total', 0)} rows indexed, search working")
    except Exception as e:
        _check("Search", False, f"Error: {e}")

    # ── Phase 4: POWER-UP (Google Workspace) ──
    _print_phase(4, "POWER-UP ⚡")

    gws_connected = False
    if args.yes:
        # Non-interactive mode: skip gws setup
        print("  ⏭️  Skipping (non-interactive mode). Run /gws-setup later.")
    else:
        gws_connected = _run_gws_powerup(args)

    # ── Phase 5: FIRST WIN ──
    _print_phase(5, "FIRST WIN 🎯")

    _show_first_win(gws_connected, easestart_dir)

    # ── Final Summary ──
    _show_capability_status(stage, gws_connected, stats)

    # Write marker file for first-time detection
    try:
        marker = easestart_dir / ".easestart_initialized"
        if not marker.exists():
            marker.write_text(f"initialized={stage}\n")
    except OSError:
        pass

    print(f"\n{'═' * 50}")
    if is_reinit:
        print("  ✅ EaseStart re-initialized!")
    else:
        print("  🎉 EaseStart initialized!")
    print(f"{'═' * 50}")

    # Stage-aware next steps (Diderot Effect)
    next_steps = STAGE_NEXT_STEPS.get(stage, STAGE_NEXT_STEPS[0])
    print(f"""
  Your stage: Stage {stage} — {STAGES[stage].split('—')[0].strip()}

  🎯 What to do next:

    1. {next_steps['primary']}
       {next_steps['primary_desc']}

    2. {next_steps['secondary']}
       {next_steps['secondary_desc']}

  💡 {next_steps['tip']}

  Other useful commands:
    easestart doctor                    Verify everything is healthy
    easestart search "your question"    Search the knowledge graph
    easestart skills list               Browse all {len(stats) - 1 if stats else '49'} knowledge domains
    """)

