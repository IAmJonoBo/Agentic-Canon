"""Tests for Cookiecutter templates."""

import pytest


def test_python_cookiecutter_bakes(cookies):
    """Test that the Python service template renders successfully."""
    result = cookies.bake(
        extra_context={
            "project_name": "Demo Service",
            "project_slug": "demo-service",
            "pkg_name": "demo_service",
            "project_description": "A demo Python service",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "Apache-2.0",
            "python_version": "3.11",
            "include_jupyter_book": "yes",
            "enable_security_gates": "yes",
            "enable_sbom_signing": "yes",
            "enable_contract_tests": "yes",
            "ci_provider": "github",
        },
        template="templates/python-service"
    )
    
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()
    
    # Check essential files exist
    assert (result.project_path / "pyproject.toml").exists()
    assert (result.project_path / "README.md").exists()
    assert (result.project_path / "src" / "demo_service" / "__init__.py").exists()
    assert (result.project_path / "tests" / "test_smoke.py").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_python_cookiecutter_minimal(cookies):
    """Test Python template with minimal options."""
    result = cookies.bake(
        extra_context={
            "project_name": "Minimal Service",
            "project_slug": "minimal-service",
            "pkg_name": "minimal_service",
            "license": "MIT",
            "include_jupyter_book": "no",
            "enable_security_gates": "no",
            "enable_sbom_signing": "no",
            "enable_contract_tests": "no",
        },
        template="templates/python-service"
    )
    
    assert result.exception is None
    assert result.exit_code == 0
    
    # Security workflow should not exist when disabled
    assert not (result.project_path / ".github" / "workflows" / "security.yml").exists()
    
    # Docs should not exist when Jupyter Book is disabled
    assert not (result.project_path / "docs" / "_config.yml").exists()


def test_python_cookiecutter_invalid_slug(cookies):
    """Test that invalid project_slug is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "Invalid_Slug",  # Underscores not allowed
            "pkg_name": "invalid_service",
        },
        template="templates/python-service"
    )
    
    # Should fail validation
    assert result.exit_code != 0
