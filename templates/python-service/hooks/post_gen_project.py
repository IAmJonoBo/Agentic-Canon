import pathlib
import shutil
import subprocess

cc = {
  "book": "{{ cookiecutter.include_jupyter_book }}",
  "sec": "{{ cookiecutter.enable_security_gates }}",
  "sbom": "{{ cookiecutter.enable_sbom_signing }}",
  "contract": "{{ cookiecutter.enable_contract_tests }}"
}

root = pathlib.Path(".")

def rm(*paths):
    """Remove files or directories if they exist."""
    for p in paths:
        q = root / p
        if q.exists():
            if q.is_dir():
                shutil.rmtree(q)
            else:
                q.unlink()
            print(f"✓ Removed: {p}")

# Remove optional components based on cookiecutter choices
if cc["book"] == "no":
    rm("docs/_config.yml", "docs/_toc.yml", "docs/intro.md", "notebooks")
    print("  Jupyter Book disabled")

if cc["sec"] == "no":
    rm(".github/workflows/security.yml")
    print("  Security gates disabled")

if cc["sbom"] == "no":
    # Note: In a real implementation, you might have a separate SBOM workflow
    print("  SBOM/signing disabled")

if cc["contract"] == "no":
    rm("tests/contract")
    print("  Contract tests disabled")

# Initialize git repository
result = subprocess.run(["git", "init", "-q"], capture_output=True)
if result.returncode == 0:
    print("✓ Initialized git repository")
else:
    print("⚠ Failed to initialize git repository")

print("\n" + "="*60)
print("Next steps:")
print("  1. cd {{ cookiecutter.project_slug }}")
print("  2. python -m venv venv")
print("  3. source venv/bin/activate")
print("  4. pip install -e .[dev]")
print("  5. pre-commit install")
print("  6. git add . && git commit -m 'Initial commit'")
print("  7. Create GitHub repo and push")
print("="*60)
