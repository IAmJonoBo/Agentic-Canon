#!/usr/bin/env python3
"""Post-generation hook for react-webapp template."""
import json
import pathlib
import shutil
import subprocess
import sys

# Get cookiecutter variables
include_storybook = "{{ cookiecutter.include_storybook }}"
include_e2e = "{{ cookiecutter.include_e2e_tests }}"
include_a11y = "{{ cookiecutter.enable_accessibility_tests }}"

root = pathlib.Path(".")


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
if include_storybook == "no":
    remove_file(
        ".storybook",
        "src/components/Button.stories.tsx",
        ".github/workflows/storybook-pages.yml",
    )

if include_e2e == "no":
    remove_file("tests/e2e", "playwright.config.ts")

if include_a11y == "no":
    remove_file(".github/workflows/accessibility.yml")


def update_package_json() -> None:
    """Remove optional scripts and dependencies from package.json."""
    package_path = root / "package.json"
    if not package_path.exists():
        return

    data = json.loads(package_path.read_text())

    def pop_script(*keys: str) -> None:
        for key in keys:
            data.get("scripts", {}).pop(key, None)

    def pop_dev_dependency(*keys: str) -> None:
        for key in keys:
            data.get("devDependencies", {}).pop(key, None)

    if include_e2e == "no":
        pop_script("test:e2e", "test:e2e:ui")
        pop_dev_dependency("@playwright/test")

    if include_storybook == "no":
        pop_script("storybook", "build-storybook")
        pop_dev_dependency("@storybook/react-vite", "@storybook/addon-essentials", "@storybook/addon-a11y")
    elif include_a11y == "no":
        pop_dev_dependency("@storybook/addon-a11y")

    package_path.write_text(json.dumps(data, indent=2) + "\n")


def gh_expr(body: str) -> str:
    """Build a GitHub Actions expression without Jinja conflicts."""
    return "${" + "{ " + body + " }}"


def update_workflows() -> None:
    """Replace placeholder expressions in workflow files."""
    security_path = root / ".github/workflows/security.yml"
    if security_path.exists():
        content = security_path.read_text()
        content = content.replace(
            "DEFAULT_BRANCH_EXPR", gh_expr("github.event.repository.default_branch")
        )
        content = content.replace("GITHUB_TOKEN_EXPR", gh_expr("secrets.GITHUB_TOKEN"))
        security_path.write_text(content)


# Initialize git repository
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    print("✓ Initialized git repository")
except Exception as e:
    print(f"⚠ Could not initialize git: {e}")

print("\n" + "=" * 60)
print("✓ React webapp project created successfully!")
print("=" * 60)
print("\nNext steps:")
print("  1. cd {{cookiecutter.project_slug}}")
print("  2. npm install")
print("  3. npm run dev")
print("  4. Open http://localhost:5173")
print("\nFor development:")
if include_storybook == "yes":
    print("  - npm run storybook (Component development)")
if include_e2e == "yes":
    print("  - npm run test:e2e (End-to-end tests)")
print("\nFor CI/CD:")
print("  - Push to GitHub to trigger workflows")
print("=" * 60)

update_package_json()
update_workflows()
