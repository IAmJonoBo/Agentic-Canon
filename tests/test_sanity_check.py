"""Tests for sanity-check.sh script."""

import subprocess
import pytest


def test_sanity_check_script_exists():
    """Test that sanity-check.sh script exists and is executable."""
    import os
    script_path = "sanity-check.sh"
    assert os.path.exists(script_path), "sanity-check.sh not found"
    assert os.access(script_path, os.X_OK), "sanity-check.sh is not executable"


def test_sanity_check_runs_successfully():
    """Test that sanity-check.sh runs without errors."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Script should exit with 0 (success)
    assert result.returncode == 0, f"Sanity check failed with exit code {result.returncode}"
    
    # Should contain summary section
    assert "Sanity Check Summary" in result.stdout
    assert "Passed:" in result.stdout
    assert "Warnings:" in result.stdout
    assert "Failed:" in result.stdout


def test_sanity_check_has_no_failures():
    """Test that sanity check reports zero failures."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for the failure count line
    assert "❌ Failed: 0" in result.stdout, "Sanity check should have no failures"


def test_sanity_check_validates_core_docs():
    """Test that sanity check validates core documentation files."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for core documentation checks
    assert "Checking Core Documentation" in result.stdout
    assert "README.md exists" in result.stdout
    assert "LICENSE exists" in result.stdout


def test_sanity_check_validates_templates():
    """Test that sanity check validates Cookiecutter templates."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for template validation
    assert "Checking Cookiecutter Templates" in result.stdout
    assert "python-service template complete" in result.stdout
    assert "node-service template complete" in result.stdout
    assert "react-webapp template complete" in result.stdout
    assert "go-service template complete" in result.stdout
    assert "docs-only template complete" in result.stdout


def test_sanity_check_validates_python_syntax():
    """Test that sanity check validates Python hook syntax."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for Python syntax validation
    assert "Validating Python Hook Syntax" in result.stdout
    assert "All hook files have valid Python syntax" in result.stdout


def test_sanity_check_validates_json_files():
    """Test that sanity check validates JSON configuration files."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for JSON validation
    assert "Validating JSON Configuration Files" in result.stdout
    assert "All JSON files are valid" in result.stdout


def test_sanity_check_validates_yaml_files():
    """Test that sanity check validates YAML configuration files."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for YAML validation
    assert "Validating YAML Configuration Files" in result.stdout
    assert "YAML files are valid" in result.stdout


def test_sanity_check_validates_shell_scripts():
    """Test that sanity check validates shell script syntax."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for shell script validation
    assert "Validating Shell Script Syntax" in result.stdout
    assert "shell scripts have valid syntax" in result.stdout


def test_sanity_check_validates_workflows():
    """Test that sanity check validates GitHub Actions workflows."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Check for workflow validation
    assert "Checking GitHub Actions Workflows" in result.stdout
    assert "workflows have proper structure" in result.stdout


def test_sanity_check_count_increased():
    """Test that sanity check has increased checks from baseline."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    # Extract the passed count
    import re
    match = re.search(r"Passed: (\d+)", result.stdout)
    assert match, "Could not find passed count in output"
    
    passed_count = int(match.group(1))
    # Should have at least 145 checks (we added more new ones)
    assert passed_count >= 145, f"Expected at least 145 checks, got {passed_count}"


def test_sanity_check_quiet_mode():
    """Test that sanity check runs in quiet mode."""
    result = subprocess.run(
        ["./sanity-check.sh", "--quiet"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Should still have summary
    assert "Sanity Check Summary" in result.stdout
    # But should have fewer output lines
    lines = result.stdout.split('\n')
    # Quiet mode should have significantly fewer lines than verbose
    assert len(lines) < 200, f"Quiet mode should have fewer lines, got {len(lines)}"


def test_sanity_check_verbose_mode():
    """Test that sanity check runs in verbose mode."""
    result = subprocess.run(
        ["./sanity-check.sh", "--verbose"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    assert "Sanity Check Summary" in result.stdout


def test_sanity_check_help():
    """Test that sanity check shows help message."""
    result = subprocess.run(
        ["./sanity-check.sh", "--help"],
        capture_output=True,
        text=True,
        timeout=30
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
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        report_path = f.name
    
    try:
        result = subprocess.run(
            ["./sanity-check.sh", "--html-report", report_path, "--quiet"],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        assert result.returncode == 0
        assert os.path.exists(report_path), "HTML report file should be created"
        
        # Check HTML content
        with open(report_path, 'r') as f:
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
        ["./sanity-check.sh", "--quiet"],
        capture_output=True,
        text=True,
        timeout=180
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
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for markdown linting section
    assert "Checking Markdown Formatting" in result.stdout or "📝" in result.stdout


def test_sanity_check_dependency_security():
    """Test that sanity check includes dependency security scanning."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for dependency security section
    assert "Checking Dependency Security" in result.stdout or "🔒" in result.stdout
    # Should check requirements.txt
    assert "requirements.txt" in result.stdout


def test_sanity_check_license_compatibility():
    """Test that sanity check includes license compatibility checking."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for license compatibility section
    assert "Checking License Compatibility" in result.stdout or "⚖️" in result.stdout


def test_sanity_check_code_duplication():
    """Test that sanity check includes code duplication detection."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for code duplication section
    assert "Checking for Code Duplication" in result.stdout or "🔍" in result.stdout


def test_sanity_check_json_schema_validation():
    """Test that sanity check includes JSON schema validation."""
    result = subprocess.run(
        ["./sanity-check.sh"],
        capture_output=True,
        text=True,
        timeout=180
    )
    
    assert result.returncode == 0
    # Check for JSON schema validation section
    assert "Validating JSON Schemas" in result.stdout or "📋" in result.stdout
    # Should check cookiecutter.json files
    assert "cookiecutter.json" in result.stdout
