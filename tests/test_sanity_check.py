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
    # Should have at least 135 checks (we added several new ones)
    assert passed_count >= 135, f"Expected at least 135 checks, got {passed_count}"
