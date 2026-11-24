#!/usr/bin/env bash
#
# Dev setup for software-factory-example-python.
# Installs the toolchain (uv) and activates the pre-commit git hook, so your
# local `git commit` runs the same brakes CI does. Idempotent — safe to re-run.
#
# Package installs use the repo-local public-PyPI config (.config/pip/pip.conf),
# so a token-gated private pip index can't block them.
#
#   ./scripts/dev-setup.sh
set -euo pipefail

cd "$(dirname "$0")/.."
export PIP_CONFIG_FILE="$PWD/.config/pip/pip.conf"
export PATH="$HOME/.local/bin:$PATH"

has() { command -v "$1" >/dev/null 2>&1; }

echo "▸ $(basename "$PWD") — pip index pinned to .config/pip/pip.conf (public PyPI)"

# ── uv provides the Python toolchain (ruff, mypy, pytest, pre-commit, …) ───────
if has uv; then
  echo "✓ uv $(uv --version)"
else
  echo "… installing uv"
  if has brew; then brew install uv
  elif has pipx; then pipx install uv
  else curl -LsSf https://astral.sh/uv/install.sh | sh; fi
  export PATH="$HOME/.local/bin:$PATH"
  has uv || { echo "✗ uv install failed — see https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
fi

echo "▸ syncing dependencies (uv sync --locked)…"
uv sync --locked

# ── Activate + verify ─────────────────────────────────────────────────────────
echo "▸ installing the git hook and building hook environments…"
uv run pre-commit install
uv run pre-commit install --install-hooks

echo "▸ running all hooks once to verify…"
uv run pre-commit run --all-files || echo "⚠ some hooks reported issues above — fix them before committing"

echo "✓ done — 'git commit' in this repo now runs the brakes locally."
