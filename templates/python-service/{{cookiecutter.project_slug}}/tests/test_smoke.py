"""Smoke tests for the generated package."""

import importlib

PACKAGE_NAME = "{{ cookiecutter.pkg_name }}"


def get_package():
    """Import the target package under test."""
    return importlib.import_module(PACKAGE_NAME)


def test_import() -> None:
    """Test that the package can be imported."""
    package = get_package()
    assert isinstance(package.__version__, str)


def test_hello() -> None:
    """Test the hello function."""
    package = get_package()
    result = package.hello()
    assert isinstance(result, str)
    assert "Hello" in result
    assert PACKAGE_NAME in result
