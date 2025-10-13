"""Tests for the pip hardening helper."""

from pathlib import Path

from agentic_canon_cli import pip_support


def test_ensure_safe_pip_success(monkeypatch, tmp_path: Path) -> None:
    """The helper should call pip with the patched spec and report success."""

    python_path = tmp_path / "python"
    python_path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")

    captured_cmd: list[str] = []

    def fake_run(cmd: list[str]) -> pip_support._CompletedProcess:  # type: ignore[name-defined]
        captured_cmd.extend(cmd)
        return pip_support._CompletedProcess(0, "Successfully installed pip", "")

    monkeypatch.delenv(pip_support.SKIP_SAFE_PIP_ENV, raising=False)
    monkeypatch.delenv(pip_support.SAFE_PIP_SPEC_ENV, raising=False)
    monkeypatch.setattr(pip_support, "_run", fake_run)

    success, detail = pip_support.ensure_safe_pip(python_path, quiet=False)

    assert success is True
    assert pip_support.SAFE_PIP_SPEC in captured_cmd
    assert detail == "Successfully installed pip"


def test_ensure_safe_pip_failure(monkeypatch, tmp_path: Path) -> None:
    """Failures should bubble up stderr details for easier troubleshooting."""

    python_path = tmp_path / "python"
    python_path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")

    def fake_run(_cmd: list[str]) -> pip_support._CompletedProcess:  # type: ignore[name-defined]
        return pip_support._CompletedProcess(1, "", "boom")

    monkeypatch.delenv(pip_support.SKIP_SAFE_PIP_ENV, raising=False)
    monkeypatch.delenv(pip_support.SAFE_PIP_SPEC_ENV, raising=False)
    monkeypatch.setattr(pip_support, "_run", fake_run)

    success, detail = pip_support.ensure_safe_pip(python_path, quiet=True)

    assert success is False
    assert detail == "boom"


def test_ensure_safe_pip_missing_python(tmp_path: Path) -> None:
    """Missing interpreters should produce a clear failure."""

    python_path = tmp_path / "python"
    success, detail = pip_support.ensure_safe_pip(python_path, quiet=True)

    assert success is False
    assert str(python_path) in detail


def test_ensure_safe_pip_skips_via_env(monkeypatch, tmp_path: Path) -> None:
    """The helper should obey AGENTIC_CANON_SKIP_SAFE_PIP when set."""

    python_path = tmp_path / "python"
    python_path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")

    monkeypatch.setenv(pip_support.SKIP_SAFE_PIP_ENV, "true")

    def raise_if_called(_cmd: list[str]) -> pip_support._CompletedProcess:  # type: ignore[name-defined]
        raise AssertionError("_run should not be invoked when skip flag is set")

    monkeypatch.setattr(pip_support, "_run", raise_if_called)

    success, detail = pip_support.ensure_safe_pip(python_path, quiet=False)

    assert success is True
    assert pip_support.SKIP_SAFE_PIP_ENV in detail


def test_ensure_safe_pip_custom_spec(monkeypatch, tmp_path: Path) -> None:
    """An override spec should propagate to the pip invocation."""

    python_path = tmp_path / "python"
    python_path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")

    captured_cmd: list[str] = []

    def fake_run(cmd: list[str]) -> pip_support._CompletedProcess:  # type: ignore[name-defined]
        captured_cmd.extend(cmd)
        return pip_support._CompletedProcess(0, "done", "")

    monkeypatch.setenv(pip_support.SAFE_PIP_SPEC_ENV, "pip==99.9")
    monkeypatch.delenv(pip_support.SKIP_SAFE_PIP_ENV, raising=False)
    monkeypatch.setattr(pip_support, "_run", fake_run)

    success, detail = pip_support.ensure_safe_pip(python_path, quiet=True)

    assert success is True
    assert "pip==99.9" in captured_cmd
    assert detail == "pip upgraded to patched build"
