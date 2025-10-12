"""Pre-generation validation hook for project-management template."""
import re
import sys


def validate_project_slug(slug: str) -> bool:
    """Validate project slug is kebab-case."""
    pattern = r'^[a-z][a-z0-9-]*[a-z0-9]$'
    return bool(re.match(pattern, slug))


def validate_github_org(org: str) -> bool:
    """Validate GitHub organization name."""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    return bool(re.match(pattern, org))


def main():
    """Run pre-generation validation."""
    project_slug = "{{ cookiecutter.project_slug }}"
    github_org = "{{ cookiecutter.github_org }}"
    
    errors = []
    
    if not validate_project_slug(project_slug):
        errors.append(
            f"Invalid project_slug '{project_slug}'. "
            "Must be lowercase kebab-case (e.g., 'my-project')."
        )
    
    if not validate_github_org(github_org):
        errors.append(
            f"Invalid github_org '{github_org}'. "
            "Must be a valid GitHub organization name."
        )
    
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
    
    print("✅ Validation passed")


if __name__ == "__main__":
    main()
