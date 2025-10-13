#!/usr/bin/env python3
"""
Agentic Canon CLI - Interactive project scaffolding wizard.

This CLI provides an interactive way to create new projects using
Cookiecutter templates with built-in best practices.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SAFE_PIP_SPEC = "pip @ git+https://github.com/pypa/pip@f2b92314da012b9fffa36b3f3e67748a37ef464a"
"""Patched pip build that includes the GHSA-4xh5-x5gv-qwph fix."""


def print_banner() -> None:
    """Print the Agentic Canon banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🚀 Agentic Canon CLI 🚀                     ║
    ║                                                           ║
    ║   Machine-readable, agent-friendly project scaffolding   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def select_template() -> str:
    """Interactive template selection."""
    print("\n📦 Select a project template:\n")
    templates = {
        "1": ("python-service", "Python Service (FastAPI/Flask)"),
        "2": ("node-service", "Node.js Service (TypeScript)"),
        "3": ("react-webapp", "React WebApp (Vite + TypeScript)"),
        "4": ("go-service", "Go Service"),
        "5": ("docs-only", "Documentation Only (Jupyter Book)"),
        "6": ("project-management", "Project Management Automation"),
    }

    for key, (_slug, desc) in templates.items():
        print(f"  {key}. {desc}")

    while True:
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        if choice in templates:
            template_slug, template_name = templates[choice]
            print(f"\n✅ Selected: {template_name}")
            return template_slug
        print("❌ Invalid choice. Please enter a number between 1 and 6.")


def get_project_details() -> dict[str, Any]:
    """Collect project details from user."""
    print("\n📝 Project Configuration:\n")

    details = {}

    # Project name
    while True:
        name = input("  Project name (e.g., 'My Awesome Service'): ").strip()
        if name:
            details["project_name"] = name
            break
        print("  ❌ Project name cannot be empty.")

    # Project slug (kebab-case)
    default_slug = name.lower().replace(" ", "-")
    slug = input(f"  Project slug [{ default_slug}]: ").strip() or default_slug
    details["project_slug"] = slug

    # Package name (snake_case) - for Python/relevant templates
    default_pkg = slug.replace("-", "_")
    pkg = input(f"  Package name [{default_pkg}]: ").strip() or default_pkg
    details["pkg_name"] = pkg

    # Description
    description = (
        input("  Description: ").strip() or "A modern, production-ready service"
    )
    details["project_description"] = description

    # Author
    author_name = input("  Author name: ").strip() or "Your Name"
    details["author_name"] = author_name

    author_email = input("  Author email: ").strip() or "your.email@example.com"
    details["author_email"] = author_email

    return details


def select_features() -> dict[str, str]:
    """Select optional features."""
    print("\n⚙️  Optional Features:\n")

    features = {}

    # Jupyter Book
    jupyter_book = (
        input("  Include Jupyter Book documentation? (Y/n): ").strip().lower()
    )
    features["include_jupyter_book"] = "yes" if jupyter_book != "n" else "no"

    # Security gates
    security = (
        input("  Enable security gates (CodeQL, secret scanning)? (Y/n): ")
        .strip()
        .lower()
    )
    features["enable_security_gates"] = "yes" if security != "n" else "no"

    # SBOM
    sbom = input("  Enable SBOM generation and signing? (Y/n): ").strip().lower()
    features["enable_sbom_signing"] = "yes" if sbom != "n" else "no"

    # Contract tests
    contract = input("  Enable contract testing? (Y/n): ").strip().lower()
    features["enable_contract_tests"] = "yes" if contract != "n" else "no"

    # CI provider
    print("\n  CI/CD Provider:")
    print("    1. GitHub Actions")
    print("    2. GitLab CI")
    print("    3. Azure Pipelines")
    ci_choice = input("  Select (1-3) [1]: ").strip() or "1"
    ci_map = {"1": "github", "2": "gitlab", "3": "azure"}
    features["ci_provider"] = ci_map.get(ci_choice, "github")

    # License
    print("\n  License:")
    print("    1. Apache-2.0")
    print("    2. MIT")
    print("    3. Proprietary")
    license_choice = input("  Select (1-3) [1]: ").strip() or "1"
    license_map = {"1": "Apache-2.0", "2": "MIT", "3": "Proprietary"}
    features["license"] = license_map.get(license_choice, "Apache-2.0")

    return features


def _run_command(
    cmd: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess:
    """Run a shell command, capturing output for diagnostics."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )
    return result


def _summarize_process_output(result: subprocess.CompletedProcess) -> str:
    """Return the last non-empty line from stdout or stderr."""

    for stream in (result.stdout, result.stderr):
        if not stream:
            continue
        lines = [line for line in stream.strip().splitlines() if line.strip()]
        if lines:
            return lines[-1]
    return ""


def _venv_python_path(venv_path: Path) -> Path:
    """Return the python executable within a virtual environment."""
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def _ensure_virtualenv() -> tuple[bool, str]:
    """Ensure a local virtual environment is ready when requirements exist."""
    requirements = Path("requirements.txt")
    if not requirements.exists():
        return True, "No requirements.txt detected, skipping Python environment setup"

    venv_path = Path(".venv")
    if not venv_path.exists():
        result = _run_command([sys.executable, "-m", "venv", str(venv_path)])
        if result.returncode != 0:
            detail = (
                result.stderr.strip() or result.stdout.strip() or "venv creation failed"
            )
            return False, detail

    venv_python = _venv_python_path(venv_path)
    if not venv_python.exists():
        return False, "Unable to locate python executable inside .venv"

    upgrade = _run_command(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            SAFE_PIP_SPEC,
        ]
    )
    if upgrade.returncode != 0:
        detail = (
            upgrade.stderr.strip() or upgrade.stdout.strip() or "pip upgrade failed"
        )
        return False, detail

    install = _run_command(
        [str(venv_python), "-m", "pip", "install", "-r", str(requirements)]
    )
    if install.returncode != 0:
        detail = (
            install.stderr.strip() or install.stdout.strip() or "pip install failed"
        )
        return False, detail

    return True, "Python virtual environment ready"


def _install_precommit_hooks() -> tuple[bool, str]:
    """Install pre-commit hooks when configuration is present."""
    config = Path(".pre-commit-config.yaml")
    if not config.exists():
        return True, "No .pre-commit-config.yaml detected"

    venv_path = Path(".venv")
    if not venv_path.exists():
        success, detail = _ensure_virtualenv()
        if not success:
            return False, detail

    venv_python = _venv_python_path(venv_path)
    install_pkg = _run_command([str(venv_python), "-m", "pip", "install", "pre-commit"])
    if install_pkg.returncode != 0:
        detail = (
            install_pkg.stderr.strip()
            or install_pkg.stdout.strip()
            or "Unable to install pre-commit"
        )
        return False, detail

    hook_install = _run_command([str(venv_python), "-m", "pre_commit", "install"])
    if hook_install.returncode != 0:
        detail = (
            hook_install.stderr.strip()
            or hook_install.stdout.strip()
            or "pre-commit install failed"
        )
        return False, detail

    return True, "pre-commit hooks installed"


def _run_sanity_check(skip_templates: bool = False) -> tuple[bool, str]:
    """Execute the repository sanity check and optional template validation."""

    script = Path(".dev/sanity-check.sh")
    if not script.exists():
        return True, "Sanity check script not found; skipped"

    include_templates = not skip_templates
    pipeline_summary: str | None = None

    if include_templates:
        pipeline_script = Path(".dev/validate-templates.sh")
        if pipeline_script.exists():
            pipeline_cmd = ["bash", str(pipeline_script), "--all", "--quiet"]
            pipeline_result = _run_command(pipeline_cmd)
            if pipeline_result.returncode != 0:
                summary = (
                    _summarize_process_output(pipeline_result)
                    or "Template validation pipeline failed"
                )
                return False, summary
            pipeline_summary = (
                _summarize_process_output(pipeline_result)
                or "Template validation pipeline completed"
            )
        else:
            pipeline_summary = "Template validation pipeline skipped (script missing)"

    sanity_cmd = ["bash", str(script), "--quiet"]
    if skip_templates:
        sanity_cmd.append("--skip-templates")

    result = _run_command(sanity_cmd)
    if result.returncode == 0:
        detail = "Sanity check passed"
        if include_templates:
            if pipeline_summary:
                detail = f"{detail} ({pipeline_summary})"
            else:
                detail = f"{detail} (template checks included)"
        else:
            detail = f"{detail} (template checks skipped)"
        return True, detail

    summary = _summarize_process_output(result) or "Review sanity-check output"
    return False, summary


def _run_validation_check() -> tuple[bool, str]:
    """Run structural validation and summarize the outcome."""
    status = cmd_validate()
    if status == 0:
        return True, "Validation checks passed"
    return False, "Validation reported issues (see above)"


def generate_project(template: str, context: dict[str, Any]) -> bool:
    """Generate project using Cookiecutter."""
    print("\n🔨 Generating project...\n")

    # Get template path
    repo_root = Path(__file__).parent.parent
    template_path = repo_root / "templates" / template

    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return False

    # Build cookiecutter command
    cmd = ["cookiecutter", str(template_path), "--no-input"]

    # Add context parameters
    for key, value in context.items():
        cmd.extend([f"{key}={value}"])

    try:
        result = _run_command(cmd)
        if result.returncode != 0:
            print(f"\n❌ Cookiecutter failed: {result.stderr or result.stdout}")
            return False
        print("\n✅ Project generated successfully!")
        return True
    except FileNotFoundError:
        print("\n❌ Cookiecutter not installed. Install with: pip install cookiecutter")
        return False


def show_next_steps(project_slug: str) -> None:
    """Display next steps after project generation."""
    print("\n📋 Next Steps:\n")
    print(f"  1. cd {project_slug}")
    print("  2. python -m venv venv")
    print("  3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("  4. pip install -e .[dev]")
    print("  5. pre-commit install")
    print("  6. git add . && git commit -m 'Initial commit'")
    print("  7. Create a GitHub repository and push your code")
    print("  8. Enable GitHub Actions in repository settings")
    print("  9. Configure GitHub Pages (Settings → Pages → Source: gh-pages)")
    print("\n🎉 Happy coding!\n")


def cmd_init() -> int:
    """Interactive wizard to create a new project."""
    try:
        print_banner()

        # Step 1: Select template
        template = select_template()

        # Step 2: Get project details
        details = get_project_details()

        # Step 3: Select features
        features = select_features()

        # Merge all context
        context = {**details, **features}

        # Step 4: Confirmation
        print("\n📊 Project Summary:")
        print(f"  Template: {template}")
        print(f"  Name: {context['project_name']}")
        print(f"  Slug: {context['project_slug']}")
        print(
            f"  Features: {', '.join([k for k, v in features.items() if v == 'yes'])}"
        )

        confirm = input("\n✅ Generate project? (Y/n): ").strip().lower()
        if confirm == "n":
            print("\n❌ Project generation cancelled.")
            return 1

        # Step 5: Generate project
        if generate_project(template, context):
            show_next_steps(context["project_slug"])
            return 0
        else:
            return 1

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


def cmd_repo_init() -> int:
    """Initialize project management automation in current repository."""
    print("\n🔧 Repository Management Setup\n")

    # Get current directory name as default project slug
    current_dir = Path.cwd().name

    print("This will set up automated project management in the current directory.")
    print("Features: TODO tracking, tasklist automation, PR follow-ups, issue triage\n")

    # Ask for confirmation
    confirm = (
        input(f"Initialize project management in '{current_dir}'? (Y/n): ")
        .strip()
        .lower()
    )
    if confirm == "n":
        print("\n❌ Cancelled.")
        return 1

    # Collect details
    details = {}
    details["project_name"] = (
        input(f"  Project name [{current_dir}]: ").strip() or current_dir
    )
    details["project_slug"] = current_dir
    details["github_org"] = input("  GitHub organization/user: ").strip() or "my-org"
    details["project_description"] = (
        input("  Description: ").strip() or "A well-managed project"
    )

    # Features with defaults
    print("\n⚙️  Enable features (Y/n):\n")
    details["enable_todo_tracking"] = (
        "no" if input("  TODO tracking? [Y/n]: ").strip().lower() == "n" else "yes"
    )
    details["enable_tasklist_tracking"] = (
        "no" if input("  Tasklist tracking? [Y/n]: ").strip().lower() == "n" else "yes"
    )
    details["enable_pr_followups"] = (
        "no" if input("  PR follow-ups? [Y/n]: ").strip().lower() == "n" else "yes"
    )
    details["enable_issue_triage"] = (
        "no" if input("  Issue auto-triage? [Y/n]: ").strip().lower() == "n" else "yes"
    )
    details["auto_close_stale_issues"] = (
        "no"
        if input("  Auto-close stale issues? [Y/n]: ").strip().lower() == "n"
        else "yes"
    )
    details["enable_codeowners"] = (
        "no" if input("  CODEOWNERS file? [Y/n]: ").strip().lower() == "n" else "yes"
    )

    details["enable_projects_board"] = "yes"
    details["enable_branch_protection"] = "yes"
    details["default_branch"] = "main"
    details["require_approvals"] = "2"
    details["stale_days"] = "60"

    # Generate using cookiecutter
    repo_root = Path(__file__).parent.parent
    template_path = repo_root / "templates" / "project-management"

    if not template_path.exists():
        print(f"\n❌ Template not found: {template_path}")
        return 1

    # Build cookiecutter command
    cmd = ["cookiecutter", str(template_path), "--no-input", "--output-dir", "/tmp"]
    for key, value in details.items():
        cmd.extend([f"{key}={value}"])

    try:
        subprocess.run(cmd, check=True)

        # Copy generated files to current directory
        temp_project = Path("/tmp") / details["project_slug"]
        if temp_project.exists():
            # Copy workflows
            os.makedirs(".github/workflows", exist_ok=True)
            for workflow in (temp_project / ".github" / "workflows").glob("*.yml"):
                # Only copy non-empty workflow files (not disabled by cookiecutter)
                content = workflow.read_text()
                if content.strip():
                    dest = Path(".github/workflows") / workflow.name
                    dest.write_text(content)
                    print(f"  ✅ Created {dest}")

            # Copy other .github files
            if (temp_project / ".github" / "CODEOWNERS").exists():
                dest = Path(".github/CODEOWNERS")
                dest.write_text((temp_project / ".github" / "CODEOWNERS").read_text())
                print(f"  ✅ Created {dest}")

            if (temp_project / ".github" / "PULL_REQUEST_TEMPLATE.md").exists():
                dest = Path(".github/PULL_REQUEST_TEMPLATE.md")
                dest.write_text(
                    (temp_project / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text()
                )
                print(f"  ✅ Created {dest}")

            # Copy issue templates
            os.makedirs(".github/ISSUE_TEMPLATE", exist_ok=True)
            for template_file in (temp_project / ".github" / "ISSUE_TEMPLATE").glob(
                "*.md"
            ):
                dest = Path(".github/ISSUE_TEMPLATE") / template_file.name
                dest.write_text(template_file.read_text())
                print(f"  ✅ Created {dest}")

            # Copy docs
            if (temp_project / "PROJECT_MANAGEMENT.md").exists():
                dest = Path("PROJECT_MANAGEMENT.md")
                if not dest.exists():
                    dest.write_text(
                        (temp_project / "PROJECT_MANAGEMENT.md").read_text()
                    )
                    print(f"  ✅ Created {dest}")

            if (temp_project / "TASKS.md").exists():
                dest = Path("TASKS.md")
                if not dest.exists():
                    dest.write_text((temp_project / "TASKS.md").read_text())
                    print(f"  ✅ Created {dest}")

            # Cleanup temp directory
            import shutil

            shutil.rmtree(temp_project)

        print("\n✅ Project management automation setup complete!")
        print("\n📋 Next Steps:")
        print("  1. Review generated workflows in .github/workflows/")
        print(
            "  2. git add . && git commit -m 'chore: add project management automation'"
        )
        print("  3. git push")
        print("  4. Create GitHub labels (see PROJECT_MANAGEMENT.md)")
        print("  5. Configure branch protection (see PROJECT_MANAGEMENT.md)")
        print("\n📚 See PROJECT_MANAGEMENT.md for detailed documentation\n")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to generate: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


def cmd_validate() -> int:
    """Validate project structure and configuration."""
    print("\n🔍 Validating Project Structure\n")

    issues = []
    warnings = []

    # Check for common files
    required_files = ["README.md"]
    recommended_files = ["CONTRIBUTING.md", "SECURITY.md", "LICENSE", ".gitignore"]

    for file in required_files:
        if not Path(file).exists():
            issues.append(f"Missing required file: {file}")
        else:
            print(f"  ✅ {file}")

    for file in recommended_files:
        if not Path(file).exists():
            warnings.append(f"Missing recommended file: {file}")
        else:
            print(f"  ✅ {file}")

    # Check .github structure
    if Path(".github").exists():
        print("  ✅ .github/")

        # Check for workflows
        if Path(".github/workflows").exists():
            workflows = list(Path(".github/workflows").glob("*.yml")) + list(
                Path(".github/workflows").glob("*.yaml")
            )
            if workflows:
                print(f"  ✅ .github/workflows/ ({len(workflows)} workflows)")
            else:
                warnings.append("No workflows found in .github/workflows/")
    else:
        warnings.append("No .github/ directory found")

    # Check for git repository
    if Path(".git").exists():
        print("  ✅ Git repository initialized")
    else:
        issues.append("Not a git repository")

    # Summary
    print("\n📊 Validation Summary:")
    checks_passed = (
        len(required_files)
        + len(recommended_files)
        - len(issues)
        - len(warnings)
    )
    print(f"  ✅ Checks passed: {checks_passed}")

    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")

    if issues:
        print(f"\n❌ Issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("\n✅ Validation passed!\n")
    return 0


def cmd_doctor() -> int:
    """Check environment setup and dependencies."""
    print("\n🩺 Environment Diagnostic\n")

    checks = []

    # Check Python version
    import sys

    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    checks.append(("Python version", python_version, sys.version_info >= (3, 8)))

    # Check for git
    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )
        git_version = result.stdout.strip()
        checks.append(("Git", git_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("Git", "Not found", False))

    # Check for gh CLI
    try:
        result = subprocess.run(
            ["gh", "--version"], capture_output=True, text=True, check=True
        )
        gh_version = result.stdout.split("\n")[0].strip()
        checks.append(("GitHub CLI", gh_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("GitHub CLI", "Not installed", False))

    # Check for cookiecutter
    try:
        result = subprocess.run(
            ["cookiecutter", "--version"], capture_output=True, text=True, check=True
        )
        cc_version = result.stdout.strip()
        checks.append(("Cookiecutter", cc_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("Cookiecutter", "Not installed", False))

    # Check for pre-commit
    try:
        result = subprocess.run(
            ["pre-commit", "--version"], capture_output=True, text=True, check=True
        )
        pc_version = result.stdout.strip()
        checks.append(("pre-commit", pc_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("pre-commit", "Not installed", False))

    # Display results
    for name, version, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {name}: {version}")

    # Recommendations
    failed = [c for c in checks if not c[2]]
    if failed:
        print("\n📦 Installation Recommendations:")
        for name, _, _ in failed:
            if name == "GitHub CLI":
                print("  - Install GitHub CLI: https://cli.github.com/")
            elif name == "Cookiecutter":
                print("  - Install Cookiecutter: pip install cookiecutter")
            elif name == "pre-commit":
                print("  - Install pre-commit: pip install pre-commit")

    print()
    return 0 if not failed else 1


def cmd_audit() -> int:
    """Run security and quality audit on project."""
    print("\n🔒 Security & Quality Audit\n")

    audit_items = []

    # Check for security files
    if Path("SECURITY.md").exists():
        audit_items.append(("Security policy", True, "SECURITY.md exists"))
    else:
        audit_items.append(("Security policy", False, "SECURITY.md missing"))

    # Check for .gitignore
    if Path(".gitignore").exists():
        gitignore = Path(".gitignore").read_text()
        has_secrets = any(
            pattern in gitignore for pattern in [".env", "*.key", "*.pem", "secret"]
        )
        audit_items.append(
            (
                "Secrets in .gitignore",
                has_secrets,
                f"{'Found' if has_secrets else 'Missing'} secret patterns",
            )
        )
    else:
        audit_items.append(("Secrets in .gitignore", False, ".gitignore missing"))

    # Check for security workflows
    security_workflows = []
    if Path(".github/workflows").exists():
        for workflow in Path(".github/workflows").glob("*.yml"):
            content = workflow.read_text().lower()
            if any(
                keyword in content
                for keyword in ["codeql", "security", "secret", "vulnerability"]
            ):
                security_workflows.append(workflow.name)

    if security_workflows:
        audit_items.append(
            ("Security workflows", True, f"Found: {', '.join(security_workflows)}")
        )
    else:
        audit_items.append(("Security workflows", False, "No security workflows found"))

    # Check for CODEOWNERS
    if Path(".github/CODEOWNERS").exists():
        audit_items.append(("Code ownership", True, "CODEOWNERS file exists"))
    else:
        audit_items.append(("Code ownership", False, "CODEOWNERS missing"))

    # Check for dependabot
    if Path(".github/dependabot.yml").exists():
        audit_items.append(("Dependency updates", True, "Dependabot configured"))
    else:
        audit_items.append(("Dependency updates", False, "Dependabot not configured"))

    # Display results
    for name, status, detail in audit_items:
        status_icon = "✅" if status else "⚠️ "
        print(f"  {status_icon} {name}: {detail}")

    # Summary
    passed = sum(1 for item in audit_items if item[1])
    total = len(audit_items)
    print(f"\n📊 Audit Score: {passed}/{total} ({int(passed/total*100)}%)")

    if passed < total:
        print("\n📝 Recommendations:")
        for name, status, _ in audit_items:
            if not status:
                print(f"  - Add {name}")

    print()
    return 0


def cmd_update() -> int:
    """Update project from template using Cruft."""
    print("\n🔄 Updating Project from Template\n")

    # Check if cruft is installed
    try:
        subprocess.run(["cruft", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Cruft is not installed.")
        print("\n📦 Install with: pip install cruft")
        return 1

    # Check if .cruft.json exists
    if not Path(".cruft.json").exists():
        print("❌ This project was not created with Cruft.")
        print("\n💡 To enable template updates:")
        print("  1. Use Cruft to create projects: cruft create <template-url>")
        print("  2. Or link existing project: cruft link <template-url>")
        return 1

    print("📋 Checking for template updates...\n")

    # Check if update is available
    try:
        result = subprocess.run(["cruft", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Project is up to date with template!")
            return 0
        elif result.returncode == 1:
            print("🔔 Template updates are available!")
        else:
            print(f"❌ Error checking for updates: {result.stderr}")
            return 1
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking for updates: {e}")
        return 1

    # Show diff
    print("\n📊 Preview changes:\n")
    try:
        result = subprocess.run(["cruft", "diff"], capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        else:
            print("  (No diff available)")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not generate diff: {e}")

    # Confirm update
    confirm = input("\n❓ Apply these updates? [y/N]: ").strip().lower()
    if confirm != "y":
        print("\n❌ Update cancelled.")
        return 0

    # Apply update
    print("\n🔨 Applying updates...\n")
    try:
        result = subprocess.run(
            ["cruft", "update", "--skip-apply-ask"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("✅ Template updates applied successfully!")

        # Check for conflicts
        git_status = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        if git_status.stdout:
            print("\n📝 Modified files:")
            print(git_status.stdout)

            # Check for merge conflicts
            if any("UU " in line for line in git_status.stdout.split("\n")):
                print("\n⚠️  Merge conflicts detected!")
                print("  Please resolve conflicts and commit the changes.")
                return 1

            print("\n💡 Next steps:")
            print("  1. Review the changes: git diff")
            print("  2. Test the updated code")
            print(
                "  3. Commit: git add . && git commit -m 'chore: update from template'"
            )

        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to apply updates: {e}")
        print("\n💡 You may need to resolve conflicts manually.")
        return 1


def cmd_fix(skip_template_checks: bool = False) -> int:
    """Run intelligent heuristics to remediate common setup issues."""
    print("\n🧠 Intelligent Auto-Fix (beta)\n")

    actions = [
        ("Project validation", _run_validation_check),
        ("Python environment", _ensure_virtualenv),
        ("pre-commit hooks", _install_precommit_hooks),
    ]

    results = []
    for name, func in actions:
        print(f"🔧 {name}...")
        try:
            success, detail = func()
        except Exception as exc:  # noqa: BLE001
            success = False
            detail = str(exc)
        results.append((name, success, detail))

    print("🔧 Sanity check...")
    try:
        sanity_success, sanity_detail = _run_sanity_check(
            skip_templates=skip_template_checks
        )
    except Exception as exc:  # noqa: BLE001
        sanity_success = False
        sanity_detail = str(exc)
    results.append(("Sanity check", sanity_success, sanity_detail))

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" Fix Summary")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for name, success, detail in results:
        icon = "✅" if success else "❌"
        print(f" {icon} {name}: {detail}")

    if all(success for _, success, _ in results):
        print("\n✨ All checks completed successfully. You're good to go!\n")
        return 0

    warning_msg = (
        "\n⚠️  Some routines reported issues above. Review the notes "
        "and rerun after addressing them.\n"
    )
    print(warning_msg)
    return 1


def main() -> int:
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description="Agentic Canon CLI - Project scaffolding and management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        help=(
            "Run the intelligent auto-fix routine after executing the selected "
            "command (or standalone)."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    subparsers.add_parser("init", help="Initialize a new project (interactive wizard)")

    # repo-init command
    subparsers.add_parser(
        "repo-init", help="Add project management automation to current repository"
    )

    # validate command
    subparsers.add_parser(
        "validate", help="Validate project structure and configuration"
    )

    # doctor command
    subparsers.add_parser("doctor", help="Check environment setup and dependencies")

    # audit command
    subparsers.add_parser("audit", help="Run security and quality audit")

    # update command
    subparsers.add_parser("update", help="Update project from template using Cruft")

    # fix command
    fix_parser = subparsers.add_parser(
        "fix", help="Run the intelligent auto-fix routine"
    )
    fix_parser.add_argument(
        "--skip-template-checks",
        action="store_true",
        help=(
            "Skip running the template validation pipeline during the auto-fix "
            "routine."
        ),
    )

    args = parser.parse_args()

    # If no command specified, default to init
    if not args.command:
        if args.fix:
            return cmd_fix()
        return cmd_init()

    if args.command == "fix":
        return cmd_fix(skip_template_checks=getattr(args, "skip_template_checks", False))

    # Route to appropriate command
    commands = {
        "init": cmd_init,
        "repo-init": cmd_repo_init,
        "validate": cmd_validate,
        "doctor": cmd_doctor,
        "audit": cmd_audit,
        "update": cmd_update,
    }

    command_func = commands.get(args.command)
    if not command_func:
        parser.print_help()
        return 1

    result = command_func()

    if args.fix:
        fix_result = cmd_fix()
        return result if result != 0 else fix_result

    return result


if __name__ == "__main__":
    sys.exit(main())
