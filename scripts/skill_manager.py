#!/usr/bin/env python3
import os
import sys
import re
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# Security Configuration
MAX_FILE_SIZE = 100 * 1024  # 100KB
SKILLS_DIR = Path(".agent/skills")
TRASH_DIR = SKILLS_DIR / ".trash"

# Layer 1: Content Guard Regex Patterns
FORBIDDEN_PATTERNS = [
    r'rm\s+-rf',            # Destructive deletion
    r'curl\s+.*\s*\|\s*bash', # Pipe to bash
    r'wget\s+.*\s*\|\s*bash',
    r'nc\s+-e',             # Netcat bind shell
    r'>\s*/dev/.*',         # Dev device overwrite
    r'mkfifo',              # Named pipes (often used in reverse shells)
    r'chmod\s+777',         # Dangerous permissions
    r'(aws_access_key_id|AWS_SECRET_ACCESS_KEY|sk_live_|ghp_)', # Credential exfiltration
]

def check_layer1_content_guard(content: str) -> list:
    """Check content against destructive regex patterns."""
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(pattern)
    return violations

def check_layer2_ownership(role: str) -> bool:
    """Verify the caller has permission to modify skills. Currently simple string check."""
    return role.lower() in ["ceo", "admin", "agent"]

def check_layer3_system_skill(skill_name: str) -> bool:
    """Check if the skill is a protected system skill."""
    # Read existing skill if it exists
    skill_path = SKILLS_DIR / skill_name
    if not skill_path.exists():
        return False
    
    # Simple check for 'is_system: true' in frontmatter across all versions
    for version_dir in skill_path.iterdir():
        if version_dir.is_dir() and (version_dir / "SKILL.md").exists():
            content = (version_dir / "SKILL.md").read_text()
            if re.search(r'is_system:\s*true', content, re.IGNORECASE):
                return True
    return False

def check_layer4_filesystem_safety(skill_name: str, content: str) -> list:
    """Prevent path traversal and enforce size limits."""
    violations = []
    # Path traversal check
    if ".." in skill_name or "/" in skill_name or "\\" in skill_name:
        violations.append("Path traversal detected in skill name")
    
    # Size limit
    if len(content.encode('utf-8')) > MAX_FILE_SIZE:
        violations.append(f"Content exceeds {MAX_FILE_SIZE/1024}KB limit")
        
    return violations

def get_latest_version(skill_dir: Path) -> int:
    """Find the highest version number in the skill directory."""
    if not skill_dir.exists():
        return 0
    versions = []
    for item in skill_dir.iterdir():
        if item.is_dir() and item.name.isdigit():
            versions.append(int(item.name))
    return max(versions) if versions else 0

def create_or_patch_skill(skill_name: str, content: str, role: str):
    """Safely create or update a skill with versioning."""
    
    # --- Execute 4-Layer Security Checks ---
    if not check_layer2_ownership(role):
        print("❌ DENIED (Layer 2 - Ownership): Role not authorized.", file=sys.stderr)
        sys.exit(1)
        
    fs_violations = check_layer4_filesystem_safety(skill_name, content)
    if fs_violations:
        print(f"❌ DENIED (Layer 4 - Filesystem): {', '.join(fs_violations)}", file=sys.stderr)
        sys.exit(1)
        
    if check_layer3_system_skill(skill_name):
        print(f"❌ DENIED (Layer 3 - System): '{skill_name}' is a protected system skill.", file=sys.stderr)
        sys.exit(1)
        
    content_violations = check_layer1_content_guard(content)
    if content_violations:
        print("❌ DENIED (Layer 1 - Content Guard): Malicious patterns detected.", file=sys.stderr)
        sys.exit(1)
        
    # --- End Security Checks ---

    skill_dir = SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    current_version = get_latest_version(skill_dir)
    next_version = current_version + 1
    
    version_dir = skill_dir / str(next_version)
    version_dir.mkdir()
    
    # Create the SKILL.md
    (version_dir / "SKILL.md").write_text(content)
    print(f"✅ SUCCESS: Skill '{skill_name}' created/patched at version {next_version}")

def soft_delete_skill(skill_name: str, role: str):
    """Soft delete a skill by moving it to .trash/"""
    
    if not check_layer2_ownership(role):
        print("❌ DENIED (Layer 2 - Ownership): Role not authorized.", file=sys.stderr)
        sys.exit(1)
        
    if ".." in skill_name or "/" in skill_name:
        print("❌ DENIED (Layer 4 - Filesystem): Path traversal detected.", file=sys.stderr)
        sys.exit(1)
        
    if check_layer3_system_skill(skill_name):
        print(f"❌ DENIED (Layer 3 - System): '{skill_name}' is a protected system skill.", file=sys.stderr)
        sys.exit(1)

    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        print(f"⚠️ Warning: Skill '{skill_name}' does not exist.")
        sys.exit(0)
        
    TRASH_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())
    trash_path = TRASH_DIR / f"{skill_name}.{timestamp}"
    
    shutil.move(skill_dir, trash_path)
    print(f"✅ SUCCESS: Skill '{skill_name}' soft-deleted to {trash_path}")


def main():
    parser = argparse.ArgumentParser(description="GoClaw Skill Manager for EaseStart (4-Layer Security)")
    subparsers = parser.add_subparsers(dest="action", required=True)
    
    # Create / Patch
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Name of the skill directory")
    create_parser.add_argument("content", help="Content of SKILL.md")
    create_parser.add_argument("--role", default="agent", help="Role executing the command (ceo, agent)")
    
    patch_parser = subparsers.add_parser("patch")
    patch_parser.add_argument("name", help="Name of the skill directory")
    patch_parser.add_argument("content", help="New content of SKILL.md")
    patch_parser.add_argument("--role", default="agent", help="Role executing the command (ceo, agent)")
    
    # Delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("name", help="Name of the skill directory")
    delete_parser.add_argument("--role", default="agent", help="Role executing the command (ceo, agent)")

    args = parser.parse_args()
    
    # Ensure root skills dir exists
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    if args.action in ["create", "patch"]:
        create_or_patch_skill(args.name, args.content, args.role)
    elif args.action == "delete":
        soft_delete_skill(args.name, args.role)

if __name__ == "__main__":
    main()
