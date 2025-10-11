#!/usr/bin/env python3
"""
Agentic Canon CLI - Interactive project scaffolding wizard.

This CLI provides an interactive way to create new projects using
Cookiecutter templates with built-in best practices.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess


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
    }
    
    for key, (slug, desc) in templates.items():
        print(f"  {key}. {desc}")
    
    while True:
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        if choice in templates:
            template_slug, template_name = templates[choice]
            print(f"\n✅ Selected: {template_name}")
            return template_slug
        print("❌ Invalid choice. Please enter a number between 1 and 5.")


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


def main():
    """Main CLI entry point."""
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


if __name__ == "__main__":
    sys.exit(main())
