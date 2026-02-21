#!/usr/bin/env python3
"""
validate.py — Pre-flight validator for new-task AgentSkill
===========================================================

Usage:
  python scripts/validate.py <mission-spec-path> <TSK-NNN>

  Example:
    python scripts/validate.py .ssdam/media-asset-platform-20260221/output/mission-spec.yaml TSK-001

Exit codes:
  0 — All hard checks pass (agent may proceed; warnings printed to stdout)
  1 — One or more HARD errors found (agent must not proceed)
  2 — Invalid arguments or file not found

This script is called automatically by the new-task AgentSkill before
generating task-spec.TSK-NNN.yaml. Do not call it manually unless debugging.
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(2)


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def is_undefined(value) -> bool:
    """Return True if the value is considered undefined/empty."""
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ("", "undefined", "tbd", "n/a"):
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def contains_tbd(value, path: str, findings: list):
    """Recursively scan a value for any literal 'TBD' strings."""
    if isinstance(value, str) and "TBD" in value.upper():
        findings.append(f"  TBD found at: {path}")
    elif isinstance(value, dict):
        for k, v in value.items():
            contains_tbd(v, f"{path}.{k}", findings)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            contains_tbd(item, f"{path}[{i}]", findings)


def validate_task_id_format(task_id: str) -> bool:
    """TSK-NNN: prefix TSK, 3+ digits."""
    return bool(re.fullmatch(r"TSK-\d{3,}", task_id))


# ──────────────────────────────────────────────────────────────
# Main validator
# ──────────────────────────────────────────────────────────────

def validate(mission_spec_path: str, target_task_id: str) -> int:
    """
    Run all validation checks.

    Returns:
      0 — All hard checks pass
      1 — One or more hard errors
    """
    errors = []    # Hard errors — block execution
    warnings = []  # Soft warnings — agent proceeds but should note these

    spec_path = Path(mission_spec_path)
    workspace_dir = spec_path.parent.parent  # .ssdam/{id}/

    # ── 1. File existence ──────────────────────────────────────
    if not spec_path.exists():
        print(f"HARD ERROR: File not found: {mission_spec_path}")
        return 1

    # ── 2. YAML parse ─────────────────────────────────────────
    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"HARD ERROR: mission-spec.yaml is not valid YAML.\n  {e}")
        return 1

    if not isinstance(spec, dict):
        print("HARD ERROR: mission-spec.yaml root must be a YAML mapping.")
        return 1

    # ── 2b. Unwrap optional mission_spec root key ──────────────
    # mission-spec.yaml uses a top-level `mission_spec:` wrapper key.
    if "mission_spec" in spec and isinstance(spec["mission_spec"], dict):
        spec = spec["mission_spec"]

    # ── 3. Target task ID format ───────────────────────────────
    if not validate_task_id_format(target_task_id):
        errors.append(f"Target task ID '{target_task_id}' does not match format TSK-NNN (e.g., TSK-001).")

    # ── 4. self_validation.passed ─────────────────────────────
    sv = spec.get("self_validation", {})
    if not isinstance(sv, dict) or sv.get("passed") is not True:
        errors.append(
            "mission-spec.yaml self_validation.passed is not true. "
            "The mission spec failed its own validation — fix it before running new-task."
        )
    else:
        # Surface any warnings from mission-spec's own failed_checks
        failed_checks = sv.get("failed_checks", [])
        if failed_checks:
            for fc in failed_checks:
                warnings.append(f"(from mission-spec self_validation) {fc}")

    # ── 5. Required top-level sections ────────────────────────
    required_sections = ["metadata", "tasks", "governance", "task_map", "policies"]
    for section in required_sections:
        if section not in spec:
            errors.append(f"Required section missing in mission-spec.yaml: '{section}'")

    if errors:
        # Structural errors — no point continuing deeper checks
        _print_results(errors, warnings, target_task_id, fatal=True)
        return 1

    # ── 6. metadata fields ────────────────────────────────────
    metadata = spec.get("metadata", {})
    for field in ["mission_id", "mission_owner"]:
        if is_undefined(metadata.get(field)):
            errors.append(f"metadata.{field} is missing or undefined.")

    # ── 7. Target task existence ───────────────────────────────
    tasks = spec.get("tasks", [])
    if not isinstance(tasks, list) or len(tasks) == 0:
        errors.append("mission-spec.yaml has no tasks defined.")
        _print_results(errors, warnings, target_task_id, fatal=True)
        return 1

    target_task = None
    for task in tasks:
        if isinstance(task, dict) and task.get("id") == target_task_id:
            target_task = task
            break

    if target_task is None:
        task_ids = [t.get("id", "?") for t in tasks if isinstance(t, dict)]
        errors.append(
            f"Task '{target_task_id}' not found in mission-spec.yaml. "
            f"Available tasks: {task_ids}"
        )
        _print_results(errors, warnings, target_task_id, fatal=True)
        return 1

    # ── 8. Target task initial_state ──────────────────────────
    initial_state = target_task.get("initial_state", "")
    if initial_state != "PENDING":
        errors.append(
            f"Task '{target_task_id}' initial_state is '{initial_state}'. "
            f"Expected 'PENDING'. Only PENDING tasks may be spec'd."
        )

    # ── 9. Required task fields ────────────────────────────────
    task_required_fields = ["name", "purpose", "requirements"]
    for field in task_required_fields:
        val = target_task.get(field)
        if is_undefined(val):
            errors.append(f"Task '{target_task_id}'.{field} is missing or undefined.")

    # Check artifact description
    artifact = target_task.get("artifact", {})
    if is_undefined(artifact) or is_undefined(artifact.get("description") if isinstance(artifact, dict) else None):
        errors.append(f"Task '{target_task_id}'.artifact.description is missing or undefined.")

    # Check checkpoint id
    checkpoint = target_task.get("checkpoint", {})
    if is_undefined(checkpoint) or is_undefined(checkpoint.get("id") if isinstance(checkpoint, dict) else None):
        errors.append(f"Task '{target_task_id}'.checkpoint.id is missing or undefined.")

    # ── 10. Governance: reviewers, gates ──────────────────────
    governance = spec.get("governance", {})
    roles = governance.get("roles", {})
    reviewers = roles.get("reviewers", [])
    if is_undefined(reviewers):
        errors.append("governance.roles.reviewers is missing or undefined.")
    elif reviewers == ["TBD"]:
        warnings.append(
            "governance.roles.reviewers is ['TBD']. "
            "Assign a real reviewer before executing tasks."
        )

    gates = governance.get("gates", [])
    if not isinstance(gates, list) or len(gates) == 0:
        errors.append("governance.gates is missing or empty.")
    else:
        # Check target task has a gate
        gate_for_task = None
        for gate in gates:
            if isinstance(gate, dict) and gate.get("task_id") == target_task_id:
                gate_for_task = gate
                break
        if gate_for_task is None:
            errors.append(f"No gate defined for task '{target_task_id}' in governance.gates.")

    # ── 11. task_owners ───────────────────────────────────────
    task_owners = roles.get("task_owners", {})
    if isinstance(task_owners, dict):
        owner = task_owners.get(target_task_id)
        if is_undefined(owner):
            errors.append(f"governance.roles.task_owners.{target_task_id} is missing or undefined.")
    else:
        errors.append("governance.roles.task_owners is not a mapping.")

    # ── 12. Policies ──────────────────────────────────────────
    policies = spec.get("policies", {})
    quality = policies.get("quality", {})
    recovery = policies.get("recovery", {})

    if is_undefined(quality) or is_undefined(quality.get("id") if isinstance(quality, dict) else None):
        errors.append("policies.quality.id is missing or undefined.")
    if is_undefined(recovery) or is_undefined(recovery.get("id") if isinstance(recovery, dict) else None):
        errors.append("policies.recovery.id is missing or undefined.")

    # ── 13. Escalation ────────────────────────────────────────
    escalation = governance.get("escalation", {})
    if isinstance(escalation, dict):
        escalation_target = escalation.get("escalation_target", "")
        if escalation_target == "TBD":
            warnings.append(
                "governance.escalation.escalation_target is 'TBD'. "
                "Assign a real escalation target before executing tasks."
            )
        for field in ["repeated_failure_threshold", "blocked_duration_threshold"]:
            if is_undefined(escalation.get(field)):
                errors.append(f"governance.escalation.{field} is missing or undefined.")

    # ── 14. TBD scan on target task ───────────────────────────
    tbd_findings = []
    contains_tbd(target_task, f"tasks[{target_task_id}]", tbd_findings)
    if tbd_findings:
        for finding in tbd_findings:
            warnings.append(f"TBD value found:{finding}")

    # ── 15. Tech stack & project_root (recoverable hard checks) ──
    #
    # Priority order:
    #   1. mission-spec.yaml → mission_spec.project_context  (written by new-mission)
    #   2. mission-input.yaml → project_context              (fallback)
    #   3. Neither → TECH_STACK_UNDEFINED / PROJECT_ROOT_UNDEFINED (hard error)
    #
    mission_input_path = workspace_dir / "input" / "mission-input.yaml"

    def _resolve_project_context() -> dict:
        """Return the best available project_context dict (may have undefined values)."""
        # Source 1: mission-spec.project_context
        ctx = spec.get("project_context", {})
        if isinstance(ctx, dict) and any(
            not is_undefined(ctx.get(f))
            for f in ("backend_stack", "frontend_stack", "database", "project_root")
        ):
            return ctx

        # Source 2: mission-input.yaml fallback
        if mission_input_path.exists():
            try:
                with open(mission_input_path, "r", encoding="utf-8") as f:
                    mi = yaml.safe_load(f)
                if isinstance(mi, dict):
                    fallback = mi.get("project_context", {})
                    if isinstance(fallback, dict):
                        return fallback
            except Exception:
                pass

        return {}

    resolved_ctx = _resolve_project_context()
    backend   = resolved_ctx.get("backend_stack", "")
    frontend  = resolved_ctx.get("frontend_stack", "")
    proj_root = resolved_ctx.get("project_root", "")

    # At least one of backend/frontend must be defined
    if is_undefined(backend) and is_undefined(frontend):
        errors.append(
            "[TECH_STACK_UNDEFINED] Neither backend_stack nor frontend_stack is defined. "
            "Run the tech stack recovery procedure: "
            "provide stack info → update mission-input.yaml → re-run validate.py."
        )

    # project_root must always be defined
    if is_undefined(proj_root):
        errors.append(
            "[PROJECT_ROOT_UNDEFINED] project_root is not defined. "
            "Run the project root recovery procedure: "
            "provide the absolute project path → update mission-input.yaml → re-run validate.py."
        )

    # ── 16. dependency_graph completeness for target task ─────
    task_map = spec.get("task_map", {})
    dep_graph = task_map.get("dependency_graph", [])
    declared_deps = target_task.get("dependencies", []) or []

    if isinstance(dep_graph, list) and isinstance(declared_deps, list):
        graph_edges_to_target = set()
        for edge in dep_graph:
            if isinstance(edge, dict) and edge.get("to") == target_task_id:
                graph_edges_to_target.add(edge.get("from"))

        for dep in declared_deps:
            if dep not in graph_edges_to_target:
                errors.append(
                    f"Task '{target_task_id}' declares dependency on '{dep}', "
                    f"but no edge {{from: {dep}, to: {target_task_id}}} exists in task_map.dependency_graph."
                )

    # ── Final output ──────────────────────────────────────────
    _print_results(errors, warnings, target_task_id, fatal=len(errors) > 0)
    return 1 if errors else 0


def _print_results(errors: list, warnings: list, task_id: str, fatal: bool):
    """Print a structured validation report."""
    print("=" * 60)
    print(f"  new-task validate.py — {task_id}")
    print("=" * 60)

    if errors:
        print(f"\n❌ HARD ERRORS ({len(errors)}) — agent cannot proceed:\n")
        for i, e in enumerate(errors, 1):
            print(f"  [{i}] {e}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}) — agent may proceed with caution:\n")
        for i, w in enumerate(warnings, 1):
            print(f"  [{i}] {w}")

    print()
    if fatal:
        print("✗  RESULT: VALIDATION FAILED — fix hard errors before running new-task.")
    else:
        if warnings:
            print("✓  RESULT: VALIDATION PASSED WITH WARNINGS — agent may proceed.")
        else:
            print("✓  RESULT: VALIDATION PASSED — agent may proceed.")
    print("=" * 60)


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        print("Usage: python scripts/validate.py <mission-spec-path> <TSK-NNN>")
        sys.exit(2)

    mission_spec_path = sys.argv[1]
    target_task_id = sys.argv[2]

    result = validate(mission_spec_path, target_task_id)
    sys.exit(result)
