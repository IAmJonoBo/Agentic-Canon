"""Tests for sanity-check.sh script."""

import os
import subprocess


def test_sanity_check_script_exists():
    """Test that sanity-check.sh script exists and is executable."""

    script_path = ".dev/sanity-check.sh"
    assert os.path.exists(script_path), ".dev/sanity-check.sh not found"
    assert os.access(script_path, os.X_OK), ".dev/sanity-check.sh is not executable"


def test_sanity_check_runs_successfully():
    """Test that sanity-check.sh runs without errors."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Script should exit with 0 (success)
    assert result.returncode == 0, f"Sanity check failed with exit code {result.returncode}"

    # Should contain summary section
    assert "Sanity Check Summary" in result.stdout
    assert "Passed:" in result.stdout
    assert "Warnings:" in result.stdout
    assert "Failed:" in result.stdout


def test_sanity_check_has_no_failures():
    """Test that sanity check reports zero failures."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for the failure count line
    assert "❌ Failed: 0" in result.stdout, "Sanity check should have no failures"


def test_sanity_check_validates_core_docs():
    """Test that sanity check validates core documentation files."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for core documentation checks
    assert "Checking Core Documentation" in result.stdout
    assert "README.md exists" in result.stdout
    assert "LICENSE exists" in result.stdout


def test_sanity_check_validates_templates():
    """Test that sanity check validates Cookiecutter templates."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for template validation
    assert "Checking Cookiecutter Templates" in result.stdout
    assert "python-service template complete" in result.stdout
    assert "node-service template complete" in result.stdout
    assert "react-webapp template complete" in result.stdout
    assert "go-service template complete" in result.stdout
    assert "docs-only template complete" in result.stdout


def test_sanity_check_validates_python_syntax():
    """Test that sanity check validates Python hook syntax."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for Python syntax validation
    assert "Validating Python Hook Syntax" in result.stdout
    assert "All hook files have valid Python syntax" in result.stdout


def test_sanity_check_validates_json_files():
    """Test that sanity check validates JSON configuration files."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for JSON validation
    assert "Validating JSON Configuration Files" in result.stdout
    assert "All JSON files are valid" in result.stdout


def test_sanity_check_validates_yaml_files():
    """Test that sanity check validates YAML configuration files."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for YAML validation
    assert "Validating YAML Configuration Files" in result.stdout
    assert "YAML files are valid" in result.stdout


def test_sanity_check_validates_shell_scripts():
    """Test that sanity check validates shell script syntax."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for shell script validation
    assert "Validating Shell Script Syntax" in result.stdout
    # Note: The sanity check may report no shell scripts if they're in .dev/ directory
    assert (
        "shell scripts have valid syntax" in result.stdout
        or "No shell scripts found" in result.stdout
    )


def test_sanity_check_validates_workflows():
    """Test that sanity check validates GitHub Actions workflows."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Check for workflow validation
    assert "Checking GitHub Actions Workflows" in result.stdout
    assert "workflows have proper structure" in result.stdout


def test_sanity_check_count_increased():
    """Test that sanity check has increased checks from baseline."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    # Extract the passed count
    import re

    match = re.search(r"Passed: (\d+)", result.stdout)
    assert match, "Could not find passed count in output"

    passed_count = int(match.group(1))
    pass_lines = [
        line
        for line in result.stdout.splitlines()
        if line.startswith("  ✅ ") and "Passed:" not in line
    ]

    baseline_floor = 22
    assert len(pass_lines) >= baseline_floor, (
        f"Quick-mode baseline should include at least {baseline_floor} passes,"
        f" saw {len(pass_lines)}"
    )
    assert passed_count == len(pass_lines), (
        f"Summary reported {passed_count} passes but quick-mode emitted {len(pass_lines)} entries"
    )


def test_sanity_check_quiet_mode():
    """Test that sanity check runs in quiet mode."""
    result = subprocess.run(
        ["./.dev/sanity-check.sh", "--quiet"],
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0
    # Should still have summary
    assert "Sanity Check Summary" in result.stdout
    # But should have fewer output lines
    lines = result.stdout.split("\n")
    # Quiet mode should have significantly fewer lines than verbose
    assert len(lines) < 200, f"Quiet mode should have fewer lines, got {len(lines)}"


def test_sanity_check_quick_mode_summary_matches_passes():
    """Quick-mode summary should reflect the number of recorded passes."""

    env = os.environ.copy()
    env["AGENTIC_CANON_SANITY_MODE"] = "quick"

    result = subprocess.run(
        ["./.dev/sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180,
        env=env,
    )

    assert result.returncode == 0, result.stdout

    import re

    match = re.search(r"Passed:\s+(\d+)", result.stdout)
    assert match, "Could not find pass count in quick-mode output"

    passed_count = int(match.group(1))
    pass_lines = [
        line
        for line in result.stdout.splitlines()
        if line.startswith("  ✅ ") and "Passed:" not in line
    ]

    # Ensure the summary and recorded pass entries stay aligned.
    assert pass_lines, "Quick mode should record at least one passing check"
    assert passed_count == len(pass_lines), (
        f"Expected {len(pass_lines)} passes, summary reported {passed_count}"
    )


def test_sanity_check_quick_mode_html_report(tmp_path):
    """Quick-mode HTML report should mirror recorded pass entries."""

    env = os.environ.copy()
    env["AGENTIC_CANON_SANITY_MODE"] = "quick"

    report_path = tmp_path / "sanity-report.html"

    result = subprocess.run(
        ["./.dev/sanity-check.sh", "--html-report", str(report_path)],
        capture_output=True,
        text=True,
        timeout=180,
        env=env,
    )

    assert result.returncode == 0, result.stdout
    html = report_path.read_text()

    assert "PASS_COUNT_PLACEHOLDER" not in html
    assert "RESULTS_PLACEHOLDER" not in html

    import re

    summary_match = re.search(r"Passed:\s+(\d+)", result.stdout)
    assert summary_match, "Quick-mode run should report pass count"
    summary_passes = int(summary_match.group(1))

    html_match = re.search(r'<p class="number pass">(\d+)</p>', html)
    assert html_match, "HTML report should include pass count"
    html_passes = int(html_match.group(1))

    pass_rows = re.findall(r"class='result-item pass'>", html)
    assert pass_rows, "HTML report should contain individual pass entries"
    assert len(pass_rows) == summary_passes == html_passes

    assert "✅ README.md exists" in html


def test_sanity_check_verbose_mode():
    """Test that sanity check runs in verbose mode."""
    result = subprocess.run(
        ["./.dev/sanity-check.sh", "--verbose"],
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0
    assert "Sanity Check Summary" in result.stdout


def test_sanity_check_help():
    """Test that sanity check shows help message."""
    result = subprocess.run(
        ["./.dev/sanity-check.sh", "--help"], capture_output=True, text=True, timeout=30
    )

    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert "--verbose" in result.stdout
    assert "--quiet" in result.stdout
    assert "--parallel" in result.stdout
    assert "--html-report" in result.stdout


def test_sanity_check_html_report():
    """Test that sanity check generates HTML report."""
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        report_path = f.name

    try:
        result = subprocess.run(
            ["./.dev/sanity-check.sh", "--html-report", report_path, "--quiet"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0
        assert os.path.exists(report_path), "HTML report file should be created"

        # Check HTML content
        with open(report_path) as f:
            html_content = f.read()

        assert "<!DOCTYPE html>" in html_content
        assert "Sanity Check Report" in html_content
        assert "Passed" in html_content
        assert "Warnings" in html_content
        assert "Failed" in html_content

    finally:
        if os.path.exists(report_path):
            os.unlink(report_path)


def test_sanity_check_performance_metrics():
    """Test that sanity check includes performance metrics."""
    result = subprocess.run(
        ["./.dev/sanity-check.sh", "--quiet"],
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0
    # Check for duration in summary
    assert "Duration:" in result.stdout
    import re

    match = re.search(r"Duration: (\d+)s", result.stdout)
    assert match, "Could not find duration in output"
    duration = int(match.group(1))
    # Should complete in reasonable time (less than 3 minutes)
    assert duration < 180, f"Sanity check took too long: {duration}s"


def test_sanity_check_markdown_linting():
    """Test that sanity check includes markdown linting."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for markdown linting section
    assert "Checking Markdown Formatting" in result.stdout or "📝" in result.stdout


def test_sanity_check_dependency_security():
    """Test that sanity check includes dependency security scanning."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for dependency security section
    assert "Checking Dependency Security" in result.stdout or "🔒" in result.stdout
    # Should check requirements.txt
    assert "requirements.txt" in result.stdout


def test_sanity_check_license_compatibility():
    """Test that sanity check includes license compatibility checking."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for license compatibility section
    assert "Checking License Compatibility" in result.stdout or "⚖️" in result.stdout


def test_sanity_check_code_duplication():
    """Test that sanity check includes code duplication detection."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for code duplication section
    assert "Checking for Code Duplication" in result.stdout or "🔍" in result.stdout


def test_sanity_check_json_schema_validation():
    """Test that sanity check includes JSON schema validation."""
    result = subprocess.run(["./.dev/sanity-check.sh"], capture_output=True, text=True, timeout=180)

    assert result.returncode == 0
    # Check for JSON schema validation section
    assert "Validating JSON Schemas" in result.stdout or "📋" in result.stdout
    # Should check cookiecutter.json files
    assert "cookiecutter.json" in result.stdout
