"""Post-generation setup hook for project-management template."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a shell command and return success status."""
    try:
        print(f"🔨 {description}...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}", file=sys.stderr)
        return False


def setup_git_repo():
    """Initialize git repository if not already initialized."""
    if not Path(".git").exists():
        run_command(["git", "init"], "Initialize git repository")
        run_command(
            ["git", "branch", "-M", "{{ cookiecutter.default_branch }}"],
            "Set default branch",
        )


def setup_github_labels():
    """Create standard GitHub labels."""
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
        print(
            f'gh label create "{name}" --color "{color}" --description "{desc}" --force'
        )
    print("```\n")


def setup_branch_protection():
    """Display branch protection setup instructions."""
    if "{{ cookiecutter.enable_branch_protection }}" == "yes":
        print("\n🔒 Branch Protection Setup")
        print("=" * 50)
        print("To enable branch protection, run:")
        print("```bash")
        print(
            "gh api repos/$OWNER/$REPO/branches/{{ cookiecutter.default_branch }}/protection \\"
        )
        print("  --method PUT \\")
        print("  --field required_status_checks[strict]=true \\")
        print("  --field enforce_admins=true \\")
        print("  --field required_pull_request_reviews[dismiss_stale_reviews]=true \\")
        print(
            "  --field required_pull_request_reviews[require_code_owner_reviews]=true \\"
        )
        print(
            "  --field required_pull_request_reviews[required_approving_review_count]={{ cookiecutter.require_approvals }} \\"
        )
        print("  --field required_linear_history=true \\")
        print("  --field allow_force_pushes=false \\")
        print("  --field allow_deletions=false")
        print("```\n")


def setup_projects_board():
    """Display GitHub Projects setup instructions."""
    if "{{ cookiecutter.enable_projects_board }}" == "yes":
        print("\n📊 GitHub Projects Setup")
        print("=" * 50)
        print("To create a GitHub Project:")
        print(
            "1. Go to: https://github.com/orgs/{{ cookiecutter.github_org }}/projects"
        )
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


def display_next_steps():
    """Display next steps for the user."""
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

    if "{{ cookiecutter.enable_branch_protection }}" == "yes":
        steps.append("4. Configure branch protection (see instructions above)")

    if "{{ cookiecutter.enable_projects_board }}" == "yes":
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


def main():
    """Run post-generation setup."""
    print("\n🚀 Setting up project management automation...\n")

    setup_git_repo()
    setup_github_labels()
    setup_branch_protection()
    setup_projects_board()
    display_next_steps()

    print("✅ Setup complete!\n")


if __name__ == "__main__":
    main()
