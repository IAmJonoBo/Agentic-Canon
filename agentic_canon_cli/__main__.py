#!/usr/bin/env python3
"""
Agentic Canon CLI entry point.

Usage:
    agentic-canon init          # Interactive wizard
    agentic-canon --help        # Show help
"""

import sys
from agentic_canon_cli.cli import main


if __name__ == "__main__":
    sys.exit(main())
