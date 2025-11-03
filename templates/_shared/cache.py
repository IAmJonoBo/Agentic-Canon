"""Caching helpers for template rendering and installer artifacts."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Mapping, Optional

try:  # pragma: no cover
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None  # type: ignore


def _default_root() -> Path:
    return Path.home() / ".cache" / "agentic-canon"


CACHE_ROOT = Path(
    os.environ.get("AGENTIC_CANON_CACHE_DIR", _default_root())
).expanduser()
TEMPLATE_CACHE_DIR = CACHE_ROOT / "templates"
INSTALLER_CACHE_ROOT = CACHE_ROOT / "installers"

NODE_CACHE_DIR = Path(
    os.environ.get("AGENTIC_CANON_NODE_CACHE_DIR", INSTALLER_CACHE_ROOT / "node")
).expanduser()
PIP_CACHE_DIR = Path(
    os.environ.get("AGENTIC_CANON_PIP_CACHE_DIR", INSTALLER_CACHE_ROOT / "pip")
).expanduser()
GO_CACHE_DIR = Path(
    os.environ.get("AGENTIC_CANON_GO_CACHE_DIR", INSTALLER_CACHE_ROOT / "go")
).expanduser()

for directory in (TEMPLATE_CACHE_DIR, NODE_CACHE_DIR, PIP_CACHE_DIR, GO_CACHE_DIR):
    directory.mkdir(parents=True, exist_ok=True)


SENTINEL = ".installed"


def _sentinel_path(cache_dir: Path) -> Path:
    return cache_dir / SENTINEL


def _mark_ready(cache_dir: Path) -> None:
    _sentinel_path(cache_dir).write_text("", encoding="utf-8")


def _is_ready(cache_dir: Path) -> bool:
    return _sentinel_path(cache_dir).exists()


def _normalise_payload(data: Mapping[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _manifest_digest(template_name: str) -> Optional[str]:
    try:
        from .manifest import get_template_config  # pylint: disable=import-outside-toplevel
    except Exception:  # pragma: no cover - manifest unavailable during bootstrap
        return None
    try:
        config = get_template_config(template_name)
    except KeyError:
        return None
    return hashlib.sha256(_normalise_payload(config).encode("utf-8")).hexdigest()


@contextlib.contextmanager
def file_lock(lock_path: Path):
    if fcntl is None:
        yield
        return

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def context_hash(template_name: str, extra_context: Dict[str, Any], manifest_hash: Optional[str] = None) -> str:
    payload = {
        "template": template_name,
        "context": extra_context,
        "manifest": manifest_hash,
    }
    return hashlib.sha256(_normalise_payload(payload).encode("utf-8")).hexdigest()


def get_template_cache_dir(template_name: str, extra_context: Dict[str, Any]) -> Path:
    digest = context_hash(template_name, extra_context, _manifest_digest(template_name))
    return TEMPLATE_CACHE_DIR / template_name / digest


def copy_from_cache(cache_dir: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)

    def _ignore(_src: str, names: Iterable[str]):
        ignored = {SENTINEL}
        return {name for name in names if name in ignored}

    shutil.copytree(cache_dir, destination, dirs_exist_ok=True, ignore=_ignore)


def _prepare_cache_dir(cache_dir: Path, force: bool) -> None:
    if force and cache_dir.exists():
        shutil.rmtree(cache_dir)
    if cache_dir.exists() and not _is_ready(cache_dir):
        shutil.rmtree(cache_dir)


def prime_template_cache(
    template_name: str,
    extra_context: Dict[str, Any],
    producer: Callable[[Path], None],
    *,
    force: bool = False,
) -> Path:
    cache_dir = get_template_cache_dir(template_name, extra_context)
    _prepare_cache_dir(cache_dir, force)
    if cache_dir.exists():
        return cache_dir

    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    lock_file = cache_dir.with_suffix(".lock")
    with file_lock(lock_file):
        _prepare_cache_dir(cache_dir, force)
        if cache_dir.exists():
            return cache_dir

        temp_dir = cache_dir.with_suffix(".tmp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        producer(temp_dir)
        _mark_ready(temp_dir)
        os.replace(temp_dir, cache_dir)
    return cache_dir


def _installer_cache_dir(namespace: Path, digest: str) -> Path:
    return namespace / digest


def cache_node_modules(
    project_path: Path,
    key_material: Iterable[bytes],
    installer: Callable[[Path], None],
    *,
    force: bool = False,
) -> None:
    digest = hashlib.sha256(b"".join(key_material)).hexdigest()
    cache_dir = _installer_cache_dir(NODE_CACHE_DIR, digest)
    lock_file = cache_dir.with_suffix(".lock")
    node_modules = project_path / "node_modules"

    with file_lock(lock_file):
        _prepare_cache_dir(cache_dir, force)
        if cache_dir.exists():
            if node_modules.exists():
                shutil.rmtree(node_modules)

            def _ignore(_src: str, names: Iterable[str]):
                return {name for name in names if name == SENTINEL}

            shutil.copytree(cache_dir, node_modules, dirs_exist_ok=True, ignore=_ignore)
            return

        installer(project_path)
        if not node_modules.exists():
            return

        temp_dir = cache_dir.with_suffix(".tmp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        shutil.copytree(node_modules, temp_dir, dirs_exist_ok=True)
        _mark_ready(temp_dir)
        os.replace(temp_dir, cache_dir)


def cache_pip_install(
    project_path: Path,
    key_material: Iterable[bytes],
    installer: Callable[[Path], None],
    *,
    force: bool = False,
) -> None:
    """
    Cache Python virtual environment style installers (pip, uv, etc.).

    The ``installer`` is expected to create a ``.venv`` directory relative to
    ``project_path``.
    """
    digest = hashlib.sha256(b"".join(key_material)).hexdigest()
    cache_dir = _installer_cache_dir(PIP_CACHE_DIR, digest)
    lock_file = cache_dir.with_suffix(".lock")
    venv_dir = project_path / ".venv"

    with file_lock(lock_file):
        _prepare_cache_dir(cache_dir, force)
        if cache_dir.exists():
            if venv_dir.exists():
                shutil.rmtree(venv_dir)
            shutil.copytree(
                cache_dir,
                venv_dir,
                dirs_exist_ok=True,
                ignore=lambda _src, names: {name for name in names if name == SENTINEL},
            )
            return

        installer(project_path)
        if not venv_dir.exists():
            return

        temp_dir = cache_dir.with_suffix(".tmp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        shutil.copytree(venv_dir, temp_dir, dirs_exist_ok=True)
        _mark_ready(temp_dir)
        os.replace(temp_dir, cache_dir)


def cache_go_modules(
    project_path: Path,
    key_material: Iterable[bytes],
    installer: Callable[[Path], None],
    *,
    force: bool = False,
) -> None:
    """Cache Go module downloads (``go mod download``)."""
    digest = hashlib.sha256(b"".join(key_material)).hexdigest()
    cache_dir = _installer_cache_dir(GO_CACHE_DIR, digest)
    lock_file = cache_dir.with_suffix(".lock")
    module_cache = project_path / "pkg" / "mod"

    with file_lock(lock_file):
        _prepare_cache_dir(cache_dir, force)
        if cache_dir.exists():
            if module_cache.exists():
                shutil.rmtree(module_cache)
            shutil.copytree(
                cache_dir,
                module_cache,
                dirs_exist_ok=True,
                ignore=lambda _src, names: {name for name in names if name == SENTINEL},
            )
            return

        installer(project_path)
        if not module_cache.exists():
            return

        temp_dir = cache_dir.with_suffix(".tmp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        shutil.copytree(module_cache, temp_dir, dirs_exist_ok=True)
        _mark_ready(temp_dir)
        os.replace(temp_dir, cache_dir)
