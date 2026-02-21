#!/usr/bin/env python3
"""
init.py — new-mission workspace setup script

Creates the .ssdam/{id}/ folder structure and copies the input template
so the user can fill it in before running the new-mission AgentSkill.

Usage:
    python templetes/new-mission/scripts/init.py [slug]

    slug  Optional. A short, memorable name for this mission folder.
          If omitted, a timestamp-based ID is generated.

Examples:
    python templetes/new-mission/scripts/init.py user-auth-api
    python templetes/new-mission/scripts/init.py erp-refactor-2026
    python templetes/new-mission/scripts/init.py

Output structure:
    .ssdam/{id}/
    ├── input/
    │   └── mission-input.yaml   ← fill this in, then run the agent
    └── output/
        └── (agent will write mission-spec.yaml here)
"""

import os
import re
import sys
import shutil
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT  = os.path.dirname(SCRIPT_DIR)          # templetes/new-mission/
TEMPLATE_SRC = os.path.join(
    SKILL_ROOT, "references", "input.template.yaml"
)


def find_project_root() -> str:
    """
    Walk up from the skill root to find the project root.

    Assumes the skill lives at:
        {project_root}/templetes/new-mission/

    So the project root is two levels above SKILL_ROOT.
    """
    return os.path.dirname(os.path.dirname(SKILL_ROOT))


# ---------------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------------

def sanitize_slug(slug: str) -> str:
    """Normalize a user-provided slug to a safe folder name."""
    slug = slug.lower().strip()
    slug = re.sub(r"[^a-z0-9\-]", "-", slug)   # replace invalid chars with -
    slug = re.sub(r"-{2,}", "-", slug)           # collapse consecutive -
    slug = slug.strip("-")                        # remove leading/trailing -
    return slug


def generate_id(slug: str | None) -> str:
    """Return the unique folder ID to use for this mission workspace."""
    if slug:
        return sanitize_slug(slug)
    # Fallback: timestamp — easy to sort, guaranteed unique per second
    now = datetime.now(timezone.utc)
    return now.strftime("mission-%Y%m%d-%H%M%S")


# ---------------------------------------------------------------------------
# Folder creation
# ---------------------------------------------------------------------------

def create_workspace(project_root: str, unique_id: str) -> tuple[str, str]:
    """
    Create .ssdam/{unique_id}/input/ and .ssdam/{unique_id}/output/.

    Returns:
        (input_dir, output_dir) — absolute paths
    """
    base       = os.path.join(project_root, ".ssdam", unique_id)
    input_dir  = os.path.join(base, "input")
    output_dir = os.path.join(base, "output")

    os.makedirs(input_dir,  exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    return input_dir, output_dir


# ---------------------------------------------------------------------------
# Template copy
# ---------------------------------------------------------------------------

def copy_input_template(input_dir: str) -> tuple[str, bool]:
    """
    Copy input.template.yaml → {input_dir}/mission-input.yaml.

    Returns:
        (dest_path, was_copied)
        was_copied is False if the file already existed (no overwrite).
    """
    dest = os.path.join(input_dir, "mission-input.yaml")

    if os.path.exists(dest):
        return dest, False

    if not os.path.exists(TEMPLATE_SRC):
        raise FileNotFoundError(
            f"Input template not found at: {TEMPLATE_SRC}\n"
            "Make sure you are running this script from the project root."
        )

    shutil.copy2(TEMPLATE_SRC, dest)
    return dest, True


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def check_existing_missions(project_root: str, unique_id: str) -> None:
    """Warn if the chosen ID already exists."""
    ssdam_dir = os.path.join(project_root, ".ssdam")
    target    = os.path.join(ssdam_dir, unique_id)

    if os.path.exists(target):
        print(f"\n⚠️  WARNING: .ssdam/{unique_id}/ already exists.")
        print("   Existing files will NOT be overwritten.")
        print("   Use a different slug if you want a fresh workspace.\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    slug       = sys.argv[1] if len(sys.argv) > 1 else None
    unique_id  = generate_id(slug)
    proj_root  = find_project_root()

    print()
    print("🚀  new-mission — workspace init")
    print(f"    Project root : {proj_root}")
    print(f"    Workspace ID : {unique_id}")

    check_existing_missions(proj_root, unique_id)

    input_dir, output_dir = create_workspace(proj_root, unique_id)
    input_file, was_copied = copy_input_template(input_dir)

    # Summary
    print()
    print("✅  Folder structure ready:")
    print(f"    .ssdam/{unique_id}/input/   ← your input workspace")
    print(f"    .ssdam/{unique_id}/output/  ← agent will write here")
    print()

    if was_copied:
        print("📄  Input template copied to:")
        print(f"    {input_file}")
    else:
        print("📄  Input file already exists (not overwritten):")
        print(f"    {input_file}")

    print()
    print("📝  Next steps:")
    print(f"    1. Open and fill in:  {input_file}")
    print( "    2. Run the new-mission AgentSkill.")
    print(f"       Output → .ssdam/{unique_id}/output/mission-spec.yaml")
    print()
    print( "    Then run the new-task AgentSkill using the output above.")
    print()


if __name__ == "__main__":
    main()
