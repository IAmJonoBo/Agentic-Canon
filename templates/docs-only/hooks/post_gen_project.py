#!/usr/bin/env python3
"""Post-generation hook for docs-only template."""
import pathlib
import subprocess

root = pathlib.Path(".")


def update_workflows() -> None:
    """Replace placeholder expressions in workflow files."""
    def gh_expr(body: str) -> str:
        return "${" + "{ " + body + " }}"

    workflow = root / ".github/workflows/book-deploy.yml"
    if workflow.exists():
        content = workflow.read_text()
        content = content.replace("GITHUB_TOKEN_EXPR", gh_expr("secrets.GITHUB_TOKEN"))
        workflow.write_text(content)


# Initialize git repository
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    print("✓ Initialized git repository")
except Exception as e:
    print(f"⚠ Could not initialize git: {e}")

print("\n" + "=" * 60)
print("✓ Documentation project created successfully!")
print("=" * 60)
print("\nNext steps:")
print("  1. cd {{cookiecutter.project_slug}}")
print("  2. pip install jupyter-book")
print("  3. jupyter-book build docs")
print("\nTo deploy to GitHub Pages:")
print("  - Push to GitHub")
print("  - GitHub Actions will build and deploy automatically")
print("=" * 60)

update_workflows()
