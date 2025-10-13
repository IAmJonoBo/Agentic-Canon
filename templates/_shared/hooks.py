"""Shared hook utilities for template post-generation steps."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .manifest import get_template_config


def _stringify(value: Any) -> str:
    return str(value or "").strip()


def _normalize_option(value: Any) -> str:
    return _stringify(value).lower()


def remove_paths(base_path: Path, paths: Iterable[str]) -> None:
    """Remove files or directories relative to ``base_path``."""
    for relative in paths:
        target = (base_path / relative).resolve()
        if not target.exists():
            continue
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()


def replace_workflow_placeholders(
    project_path: Path, workflows: Sequence[Mapping[str, Any]]
) -> None:
    """Replace templated placeholders inside rendered workflow files."""
    for workflow in workflows or []:
        if not isinstance(workflow, Mapping):
            continue
        file_path = workflow.get("path") or workflow.get("file")
        if not file_path:
            continue
        replacements: Mapping[str, str] = (
            workflow.get("replacements") or workflow.get("placeholders") or {}
        )
        target = project_path / file_path
        if not target.exists():
            continue
        content = target.read_text(encoding="utf-8")
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        target.write_text(content, encoding="utf-8")


def run_commands(project_path: Path, commands: Iterable[Any]) -> None:
    """Execute bootstrap commands best-effort."""
    for command in commands or []:
        try:
            if isinstance(command, str):
                subprocess.run(command, cwd=project_path, shell=True, check=True)
            else:
                subprocess.run(list(command), cwd=project_path, check=True)
        except (OSError, subprocess.CalledProcessError):
            # Bootstrap commands should never break template generation.
            pass


def ensure_git_repo(
    project_path: Path, git_config: Mapping[str, Any], context: Mapping[str, Any]
) -> None:
    """Initialise a git repository when enabled."""
    if (
        not git_config
        or not git_config.get("init")
        or os.environ.get("AGENTIC_CANON_SKIP_GIT_INIT")
    ):
        return

    try:
        subprocess.run(["git", "init", "-q"], cwd=project_path, check=False)
        default_branch_var = git_config.get("default_branch_variable")
        if default_branch_var:
            branch_name = _stringify(context.get(default_branch_var))
            if branch_name:
                subprocess.run(["git", "branch", "-M", branch_name], cwd=project_path, check=False)
    except OSError:
        # Git may not be available in constrained environments.
        pass


def remove_optional_components(project_path: Path, paths: Iterable[str]) -> None:
    """Convenience wrapper to remove optional assets driven by the manifest."""
    remove_paths(project_path, paths)


def _apply_actions(project_path: Path, actions: Mapping[str, Any]) -> None:
    if not actions:
        return
    removals = actions.get("remove") or []
    if removals:
        remove_paths(project_path, removals)

    workflow_actions = actions.get("workflows")
    if workflow_actions:
        if isinstance(workflow_actions, Mapping):
            replace_workflow_placeholders(project_path, [workflow_actions])
        else:
            replace_workflow_placeholders(project_path, workflow_actions)

    commands = actions.get("commands") or []
    if commands:
        run_commands(project_path, commands)


def _apply_option_matrix(
    project_path: Path, options: Mapping[str, Any], context: Mapping[str, Any]
) -> None:
    for option_name, option_config in (options or {}).items():
        desired_value = context.get(option_name)
        if desired_value is None and "default" in option_config:
            desired_value = option_config.get("default")
        normalized = _normalize_option(desired_value)
        cases = option_config.get("cases", {})
        actions = cases.get(normalized)
        if actions:
            _apply_actions(project_path, actions)


def _apply_legacy_features(
    project_path: Path, config: Mapping[str, Any], context: Mapping[str, Any]
) -> None:
    for feature in config.get("features", []) or []:
        variable = feature.get("variable")
        if not variable:
            continue
        actions_map = feature.get("actions", {})
        desired_value = _normalize_option(context.get(variable))
        if desired_value in actions_map:
            _apply_actions(project_path, actions_map[desired_value])


def _apply_cleanup(project_path: Path, hooks_config: Mapping[str, Any]) -> None:
    cleanup_cfg = hooks_config.get("cleanup", {}) if hooks_config else {}
    remove_optional_components(project_path, cleanup_cfg.get("remove_after_render", []))


def run_post_gen(template_name: str, project_path: Path, context: dict[str, Any]) -> None:
    """Apply manifest-driven post-generation customisations."""
    config = get_template_config(template_name)
    hooks_config: Mapping[str, Any] = config.get("hooks", {})

    replace_workflow_placeholders(project_path, hooks_config.get("workflows", []))
    _apply_option_matrix(project_path, hooks_config.get("options", {}), context)
    _apply_legacy_features(project_path, config, context)
    _apply_cleanup(project_path, hooks_config)

    manifest_commands = hooks_config.get("commands", [])
    if manifest_commands:
        run_commands(project_path, manifest_commands)
    run_commands(project_path, config.get("bootstrap", []))

    ensure_git_repo(project_path, config.get("git", {}), context)


def apply_template_config(
    template_name: str, project_path: Path, context: dict[str, Any]
) -> None:
    """
    Backwards-compatible alias for older hooks.

    Historically the templates invoked ``apply_template_config``. We keep the
    entry point intact so upgrades remain seamless.
    """
    run_post_gen(template_name, project_path, context)


def should_suppress_messages() -> bool:
    return bool(os.environ.get("AGENTIC_CANON_SKIP_MESSAGES"))
