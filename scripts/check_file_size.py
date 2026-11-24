"""Fail the commit when a staged Python file is too large to navigate well.

A big file is hard for a coding agent to read and edit correctly. This check
estimates tokens as bytes / 4 and fails any staged ``*.py`` file over the budget,
with guidance on how to split it. It is a cheap, high-value brake (feedback loops).
"""

from __future__ import annotations

import sys
from pathlib import Path

MAX_TOKENS = 6000
BYTES_PER_TOKEN = 4
MAX_BYTES = MAX_TOKENS * BYTES_PER_TOKEN


def main(paths: list[str]) -> int:
    """Return 1 if any path is over the budget, else 0."""
    too_big: list[tuple[str, int]] = []
    for name in paths:
        path = Path(name)
        if not path.is_file():
            continue
        size = path.stat().st_size
        if size > MAX_BYTES:
            too_big.append((name, size // BYTES_PER_TOKEN))

    if not too_big:
        return 0

    print("File-size cap: these Python files are too large to navigate well:")
    for name, tokens in too_big:
        print(f"  - {name}: ~{tokens} tokens (budget {MAX_TOKENS})")
    print(
        "\nSplit each file along a seam: move a cohesive class or group of "
        "functions into a new module and import it back. Keep each module focused "
        "on one responsibility. Then stage the files and commit again."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
