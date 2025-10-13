"""Automation sessions for Agentic Canon."""

from __future__ import annotations

import nox

SANITY_SECTIONS = (
    "core",
    "templates",
    "examples",
    "dashboards",
    "videos",
    "cloud",
    "cli",
    "tests",
)

nox.options.error_on_missing_interpreters = False
nox.options.reuse_existing_virtualenvs = True


def _run_sanity(session: nox.Session, *sections: str) -> None:
    command = ["./.dev/sanity-check.sh"]
    for section in sections:
        command.extend(["--section", section])
    session.run(*command, external=True)


@nox.session
def sanity(session: nox.Session) -> None:
    """Run the full sanity check."""
    _run_sanity(session)


def _register_section_session(section: str) -> None:
    @nox.session(name=f"sanity_{section}")
    def sanity_section(session: nox.Session, section: str = section) -> None:
        """Run a single sanity-check section."""
        _run_sanity(session, section)

    globals()[f"sanity_{section}"] = sanity_section


for _section in SANITY_SECTIONS:
    _register_section_session(_section)


@nox.session
def tests(session: nox.Session) -> None:
    """Execute the pytest suite with xdist parallelism."""
    session.install("-r", "requirements.txt")
    session.run("pytest", "-n", "auto")
