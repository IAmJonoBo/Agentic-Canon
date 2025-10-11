"""Smoke tests for {{ cookiecutter.pkg_name }}."""

import {{ cookiecutter.pkg_name }}


def test_import() -> None:
    """Test that the package can be imported."""
    assert {{ cookiecutter.pkg_name }}.__version__ == "0.1.0"


def test_hello() -> None:
    """Test the hello function."""
    result = {{ cookiecutter.pkg_name }}.hello()
    assert isinstance(result, str)
    assert "Hello" in result
    assert "{{ cookiecutter.pkg_name }}" in result
