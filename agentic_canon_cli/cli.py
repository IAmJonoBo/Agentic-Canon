#!/usr/bin/env python3
"""
Agentic Canon CLI - Interactive project scaffolding wizard.

This CLI provides an interactive way to create new projects using
Cookiecutter templates with built-in best practices.
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import os


def print_banner():
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
    
    for key, (slug, desc) in templates.items():
        print(f"  {key}. {desc}")
    
    while True:
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        if choice in templates:
            template_slug, template_name = templates[choice]
            print(f"\n✅ Selected: {template_name}")
            return template_slug
        print("❌ Invalid choice. Please enter a number between 1 and 6.")


def get_project_details() -> Dict[str, Any]:
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
    description = input("  Description: ").strip() or "A modern, production-ready service"
    details["project_description"] = description
    
    # Author
    author_name = input("  Author name: ").strip() or "Your Name"
    details["author_name"] = author_name
    
    author_email = input("  Author email: ").strip() or "your.email@example.com"
    details["author_email"] = author_email
    
    return details


def select_features() -> Dict[str, str]:
    """Select optional features."""
    print("\n⚙️  Optional Features:\n")
    
    features = {}
    
    # Jupyter Book
    jupyter_book = input("  Include Jupyter Book documentation? (Y/n): ").strip().lower()
    features["include_jupyter_book"] = "yes" if jupyter_book != "n" else "no"
    
    # Security gates
    security = input("  Enable security gates (CodeQL, secret scanning)? (Y/n): ").strip().lower()
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


def generate_project(template: str, context: Dict[str, Any]) -> bool:
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
        subprocess.run(cmd, check=True)
        print("\n✅ Project generated successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to generate project: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Cookiecutter not installed. Install with: pip install cookiecutter")
        return False


def show_next_steps(project_slug: str):
    """Display next steps after project generation."""
    print(f"\n📋 Next Steps:\n")
    print(f"  1. cd {project_slug}")
    print( "  2. python -m venv venv")
    print( "  3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print( "  4. pip install -e .[dev]")
    print( "  5. pre-commit install")
    print( "  6. git add . && git commit -m 'Initial commit'")
    print( "  7. Create a GitHub repository and push your code")
    print( "  8. Enable GitHub Actions in repository settings")
    print( "  9. Configure GitHub Pages (Settings → Pages → Source: gh-pages)")
    print("\n🎉 Happy coding!\n")


def cmd_init():
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
        print(f"  Features: {', '.join([k for k, v in features.items() if v == 'yes'])}")
        
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


def cmd_repo_init():
    """Initialize project management automation in current repository."""
    print("\n🔧 Repository Management Setup\n")
    
    # Get current directory name as default project slug
    current_dir = Path.cwd().name
    
    print("This will set up automated project management in the current directory.")
    print("Features: TODO tracking, tasklist automation, PR follow-ups, issue triage\n")
    
    # Ask for confirmation
    confirm = input(f"Initialize project management in '{current_dir}'? (Y/n): ").strip().lower()
    if confirm == "n":
        print("\n❌ Cancelled.")
        return 1
    
    # Collect details
    details = {}
    details["project_name"] = input(f"  Project name [{current_dir}]: ").strip() or current_dir
    details["project_slug"] = current_dir
    details["github_org"] = input("  GitHub organization/user: ").strip() or "my-org"
    details["project_description"] = input("  Description: ").strip() or "A well-managed project"
    
    # Features with defaults
    print("\n⚙️  Enable features (Y/n):\n")
    details["enable_todo_tracking"] = "no" if input("  TODO tracking? [Y/n]: ").strip().lower() == "n" else "yes"
    details["enable_tasklist_tracking"] = "no" if input("  Tasklist tracking? [Y/n]: ").strip().lower() == "n" else "yes"
    details["enable_pr_followups"] = "no" if input("  PR follow-ups? [Y/n]: ").strip().lower() == "n" else "yes"
    details["enable_issue_triage"] = "no" if input("  Issue auto-triage? [Y/n]: ").strip().lower() == "n" else "yes"
    details["auto_close_stale_issues"] = "no" if input("  Auto-close stale issues? [Y/n]: ").strip().lower() == "n" else "yes"
    details["enable_codeowners"] = "no" if input("  CODEOWNERS file? [Y/n]: ").strip().lower() == "n" else "yes"
    
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
                dest.write_text((temp_project / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text())
                print(f"  ✅ Created {dest}")
            
            # Copy issue templates
            os.makedirs(".github/ISSUE_TEMPLATE", exist_ok=True)
            for template_file in (temp_project / ".github" / "ISSUE_TEMPLATE").glob("*.md"):
                dest = Path(".github/ISSUE_TEMPLATE") / template_file.name
                dest.write_text(template_file.read_text())
                print(f"  ✅ Created {dest}")
            
            # Copy docs
            if (temp_project / "PROJECT_MANAGEMENT.md").exists():
                dest = Path("PROJECT_MANAGEMENT.md")
                if not dest.exists():
                    dest.write_text((temp_project / "PROJECT_MANAGEMENT.md").read_text())
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
        print("  2. git add . && git commit -m 'chore: add project management automation'")
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


def cmd_validate():
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
        print(f"  ✅ .github/")
        
        # Check for workflows
        if Path(".github/workflows").exists():
            workflows = list(Path(".github/workflows").glob("*.yml")) + list(Path(".github/workflows").glob("*.yaml"))
            if workflows:
                print(f"  ✅ .github/workflows/ ({len(workflows)} workflows)")
            else:
                warnings.append("No workflows found in .github/workflows/")
    else:
        warnings.append("No .github/ directory found")
    
    # Check for git repository
    if Path(".git").exists():
        print(f"  ✅ Git repository initialized")
    else:
        issues.append("Not a git repository")
    
    # Summary
    print("\n📊 Validation Summary:")
    print(f"  ✅ Checks passed: {len(required_files) + len(recommended_files) - len(issues) - len(warnings)}")
    
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


def cmd_doctor():
    """Check environment setup and dependencies."""
    print("\n🩺 Environment Diagnostic\n")
    
    checks = []
    
    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks.append(("Python version", python_version, sys.version_info >= (3, 8)))
    
    # Check for git
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        git_version = result.stdout.strip()
        checks.append(("Git", git_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("Git", "Not found", False))
    
    # Check for gh CLI
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True, check=True)
        gh_version = result.stdout.split('\n')[0].strip()
        checks.append(("GitHub CLI", gh_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("GitHub CLI", "Not installed", False))
    
    # Check for cookiecutter
    try:
        result = subprocess.run(["cookiecutter", "--version"], capture_output=True, text=True, check=True)
        cc_version = result.stdout.strip()
        checks.append(("Cookiecutter", cc_version, True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        checks.append(("Cookiecutter", "Not installed", False))
    
    # Check for pre-commit
    try:
        result = subprocess.run(["pre-commit", "--version"], capture_output=True, text=True, check=True)
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


def cmd_audit():
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
        has_secrets = any(pattern in gitignore for pattern in [".env", "*.key", "*.pem", "secret"])
        audit_items.append(("Secrets in .gitignore", has_secrets, f"{'Found' if has_secrets else 'Missing'} secret patterns"))
    else:
        audit_items.append(("Secrets in .gitignore", False, ".gitignore missing"))
    
    # Check for security workflows
    security_workflows = []
    if Path(".github/workflows").exists():
        for workflow in Path(".github/workflows").glob("*.yml"):
            content = workflow.read_text().lower()
            if any(keyword in content for keyword in ["codeql", "security", "secret", "vulnerability"]):
                security_workflows.append(workflow.name)
    
    if security_workflows:
        audit_items.append(("Security workflows", True, f"Found: {', '.join(security_workflows)}"))
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


def main():
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description="Agentic Canon CLI - Project scaffolding and management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    subparsers.add_parser("init", help="Initialize a new project (interactive wizard)")
    
    # repo-init command
    subparsers.add_parser("repo-init", help="Add project management automation to current repository")
    
    # validate command
    subparsers.add_parser("validate", help="Validate project structure and configuration")
    
    # doctor command
    subparsers.add_parser("doctor", help="Check environment setup and dependencies")
    
    # audit command
    subparsers.add_parser("audit", help="Run security and quality audit")
    
    args = parser.parse_args()
    
    # If no command specified, default to init
    if not args.command:
        return cmd_init()
    
    # Route to appropriate command
    commands = {
        "init": cmd_init,
        "repo-init": cmd_repo_init,
        "validate": cmd_validate,
        "doctor": cmd_doctor,
        "audit": cmd_audit,
    }
    
    command_func = commands.get(args.command)
    if command_func:
        return command_func()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
