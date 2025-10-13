#!/usr/bin/env python3
"""Post-generation hook for node-service template."""
import os
import pathlib
import shutil
import subprocess
import sys

# Get cookiecutter variables
enable_security = "{{ cookiecutter.enable_security_gates }}"
enable_sbom = "{{ cookiecutter.enable_sbom_signing }}"

root = pathlib.Path(".")


def gh_expr(body: str) -> str:
    """Build a GitHub Actions expression without Jinja conflicts."""
    return "${" + "{ " + body + " }}"


def remove_file(*paths):
    """Remove files or directories."""
    for path in paths:
        target = root / path
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            print(f"  Removed: {path}")


# Remove optional files based on configuration
if enable_security == "no":
    remove_file(".github/workflows/security.yml")


def update_workflows():
    """Replace placeholder expressions in workflow files."""
    replacements = {
        ".github/workflows/security.yml": {
            "DEFAULT_BRANCH_EXPR": gh_expr("github.event.repository.default_branch"),
        },
        ".github/workflows/ci.yml": {
            "NODE_VERSION_LABEL": gh_expr("matrix.node-version"),
            "NODE_VERSION_EXPR": gh_expr("matrix.node-version"),
            "UPLOAD_COVERAGE_EXPR": gh_expr("matrix.node-version == 20"),
            "CODECOV_TOKEN_EXPR": gh_expr("secrets.CODECOV_TOKEN"),
        },
    }

    for rel_path, mapping in replacements.items():
        workflow = root / rel_path
        if not workflow.exists():
            continue
        content = workflow.read_text()
        for placeholder, expr in mapping.items():
            content = content.replace(placeholder, expr)
        workflow.write_text(content)


if enable_sbom == "no":
    # Remove SBOM-related configurations from security workflow if it exists
    pass

# Initialize git repository
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    print("✓ Initialized git repository")
except Exception as e:
    print(f"⚠ Could not initialize git: {e}")

print("\n" + "=" * 60)
print("✓ Node.js service project created successfully!")
print("=" * 60)
print("\nNext steps:")
print("  1. cd {{cookiecutter.project_slug}}")
print("  2. npm install")
print("  3. npm test")
print("  4. npm run dev")
print("\nFor CI/CD:")
print("  - Push to GitHub to trigger workflows")
print("  - Review .github/workflows/ for pipeline configuration")
print("=" * 60)

update_workflows()
