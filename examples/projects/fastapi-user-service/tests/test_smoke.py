"""Smoke tests for acme_service."""

import acme_service


def test_import() -> None:
    """Test that the package can be imported."""
    assert acme_service.__version__ == "0.1.0"


def test_app_exists() -> None:
    """Test FastAPI app is available."""
    assert hasattr(acme_service, "app")
    assert acme_service.app is not None
