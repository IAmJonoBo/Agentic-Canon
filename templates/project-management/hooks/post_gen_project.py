"""Post-generation setup hook for project-management template."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path
from types import ModuleType


def _load_hooks() -> ModuleType:
    template_root = Path("{{ cookiecutter._template }}").resolve()
    if template_root.exists():
        repo_root = template_root.parent.parent
        for candidate in (repo_root, template_root.parent):
            candidate_str = str(candidate)
            if candidate_str and candidate_str not in sys.path:
                sys.path.insert(0, candidate_str)

    return importlib.import_module("templates._shared.hooks")


hooks = _load_hooks()

CONFIG = {
    "issue_triage": "{{ cookiecutter.enable_issue_triage }}",
    "pr_followups": "{{ cookiecutter.enable_pr_followups }}",
    "stale_issues": "{{ cookiecutter.auto_close_stale_issues }}",
    "todo_tracking": "{{ cookiecutter.enable_todo_tracking }}",
    "tasklist_tracking": "{{ cookiecutter.enable_tasklist_tracking }}",
    "projects_board": "{{ cookiecutter.enable_projects_board }}",
    "branch_protection": "{{ cookiecutter.enable_branch_protection }}",
    "default_branch": "{{ cookiecutter.default_branch }}",
    "require_approvals": "{{ cookiecutter.require_approvals }}",
}

PROJECT_ROOT = Path(".").resolve()

hooks.run_post_gen("project-management", PROJECT_ROOT, CONFIG)


def run_command(cmd: list[str], description: str) -> bool:
    try:
        print(f"🔨 {description}...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} complete")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"❌ {description} failed: {exc.stderr}", file=sys.stderr)
        return False


def setup_git_repo() -> None:
    if hooks.should_suppress_messages():
        return
    print("\n🚀 Setting up project management automation...\n")
    if not (PROJECT_ROOT / ".git").exists():
        run_command(["git", "init"], "Initialize git repository")
        run_command(["git", "branch", "-M", CONFIG["default_branch"]], "Set default branch")


def setup_github_labels() -> None:
    if hooks.should_suppress_messages():
        return
    labels = [
        ("task", "0e8a16", "General task"),
        ("from:todo", "d4c5f9", "Created from TODO comment"),
        ("from:tasklist", "bfdadc", "Created from tasklist"),
        ("from:pr-review", "fbca04", "Follow-up from PR review"),
        ("follow-up", "fef2c0", "Follow-up work required"),
        ("needs-triage", "ededed", "Needs initial triage"),
        ("bug", "d73a4a", "Bug report"),
        ("enhancement", "a2eeef", "Feature request"),
        ("documentation", "0075ca", "Documentation improvement"),
        ("security", "d93f0b", "Security issue"),
        ("performance", "f9d0c4", "Performance improvement"),
        ("question", "d876e3", "Question"),
    ]

    print("\n📋 GitHub Labels Setup")
    print("=" * 50)
    print("To create labels, run:")
    print("```bash")
    for name, color, desc in labels:
        print(f'gh label create "{name}" --color "{color}" --description "{desc}" --force')
    print("```\n")


def setup_branch_protection() -> None:
    if hooks.should_suppress_messages() or CONFIG["branch_protection"].lower() != "yes":
        return
    print("\n🔒 Branch Protection Setup")
    print("=" * 50)
    print("To enable branch protection, run:")
    print("```bash")
    print("gh api repos/$OWNER/$REPO/branches/{{ cookiecutter.default_branch }}/protection \\")
    print("  --method PUT \\")
    print("  --field required_status_checks[strict]=true \\")
    print("  --field enforce_admins=true \\")
    print("  --field required_pull_request_reviews[dismiss_stale_reviews]=true \\")
    print("  --field required_pull_request_reviews[require_code_owner_reviews]=true \\")
    approval_field = (
        "  --field "
        "required_pull_request_reviews[required_approving_review_count]="
        "{{ cookiecutter.require_approvals }} \\"
    )
    print(approval_field)
    print("  --field required_linear_history=true \\")
    print("  --field allow_force_pushes=false \\")
    print("  --field allow_deletions=false")
    print("```\n")


def setup_projects_board() -> None:
    if hooks.should_suppress_messages() or CONFIG["projects_board"].lower() != "yes":
        return
    print("\n📊 GitHub Projects Setup")
    print("=" * 50)
    print("To create a GitHub Project:")
    print("1. Go to: https://github.com/orgs/{{ cookiecutter.github_org }}/projects")
    print("2. Click 'New project'")
    print("3. Choose 'Board' template")
    print("4. Add custom fields:")
    print("   - Priority: Single select (High, Medium, Low)")
    print("   - Iteration: Iteration field")
    print("5. Enable automation:")
    print("   - Auto-add: Add new issues to project")
    print("   - Auto-archive: Archive closed items after 14 days")
    print("   - Status sync: Sync issue state with column")
    print("\n")


def display_next_steps() -> None:
    if hooks.should_suppress_messages():
        return
    print("\n✨ Project Management Setup Complete!")
    print("=" * 50)
    print("\n📝 Next Steps:\n")
    steps = [
        "1. Review generated workflows in .github/workflows/",
        "2. Commit and push to GitHub:",
        "   git add .",
        "   git commit -m 'chore: add project management automation'",
        "   git push",
        "3. Set up GitHub labels (see instructions above)",
    ]

    if CONFIG["branch_protection"].lower() == "yes":
        steps.append("4. Configure branch protection (see instructions above)")

    if CONFIG["projects_board"].lower() == "yes":
        steps.append("5. Create GitHub Projects board (see instructions above)")

    steps.extend(
        [
            "6. Test the automation by:",
            "   - Adding a TODO comment to code",
            "   - Creating unchecked items in TASKS.md",
            "   - Opening a PR with follow-up comments",
            "7. Review and customize workflows as needed",
        ]
    )

    for step in steps:
        print(step)

    print("\n📚 Documentation:")
    print("- See README.md for detailed usage")
    print("- See PROJECT_MANAGEMENT.md for workflow details")
    print("\n")


def main() -> None:
    setup_git_repo()
    setup_github_labels()
    setup_branch_protection()
    setup_projects_board()
    display_next_steps()
    if not hooks.should_suppress_messages():
        print("✅ Setup complete!\n")


if __name__ == "__main__":
    main()
