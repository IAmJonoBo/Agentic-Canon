"""Lightweight OpenFeature + flagd bootstrap for Python services."""

from __future__ import annotations

import logging
import os
from functools import lru_cache

from flagd.provider import FlagdProvider  # type: ignore[import]
from openfeature import api

_LOGGER = logging.getLogger("feature_flags")
_DEFAULT_HOST = os.environ.get("FLAGD_HOST", "localhost")
_DEFAULT_PORT = int(os.environ.get("FLAGD_PORT", "8013"))


@lru_cache(maxsize=1)
def get_client() -> api.FeatureClient:
    """Return a singleton OpenFeature client configured with flagd."""
    api.set_provider(FlagdProvider(host=_DEFAULT_HOST, port=_DEFAULT_PORT))
    return api.get_client(name="agentic-canon")


def get_boolean(flag_key: str, default: bool = False) -> bool:
    """Safely evaluate a boolean flag, falling back to default on failure."""
    try:
        return get_client().get_boolean_value(flag_key, default)
    except Exception as exc:  # noqa: BLE001
        _LOGGER.warning("Flag evaluation failed for %s: %s", flag_key, exc)
        return default
