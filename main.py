"""Backwards-compatible entry point. Use `arxiv-digest` CLI after `pip install`."""

import sys
from agent.cli import main

if __name__ == "__main__":
    sys.exit(main())
