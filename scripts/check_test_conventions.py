#!/usr/bin/env python3
"""Pre-commit check: tests follow CODING_STANDARDS.md.

Each `def test_*` under tests/ must:
  - be named `test_when_<scenario>` (name the single scenario under test),
  - use the `given`, `when`, and `then` DSL (one `when`; `given`/`then` may repeat), and
  - assert only through `then` (no bare `assert`, no mock `.assert_*` calls).
"""

import ast
import sys

_TestDef = (ast.FunctionDef, ast.AsyncFunctionDef)
_DSL = ("given", "when", "then")


def _check(fn: ast.FunctionDef | ast.AsyncFunctionDef, path: str, errors: list[str]) -> None:
    if not (fn.name.startswith("test_when_") and len(fn.name) > len("test_when_")):
        errors.append(f"{path}:{fn.lineno}: '{fn.name}' must be named test_when_<scenario>")
    used: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Assert):
            errors.append(f"{path}:{node.lineno}: assert through the `then` DSL, not a bare assert")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr.startswith("assert_"):
                errors.append(
                    f"{path}:{node.lineno}: assert through `then`, not a mock .{node.func.attr}()"
                )
            target = node.func.value
            if isinstance(target, ast.Name) and target.id in _DSL:
                used.add(target.id)
    for dsl in _DSL:
        if dsl not in used:
            errors.append(
                f"{path}:{fn.lineno}: '{fn.name}' must use `{dsl}.` (given / when / then)"
            )


def check_file(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, _TestDef) and node.name.startswith("test"):
            _check(node, path, errors)
    return errors


def main(argv: list[str]) -> int:
    errors = [e for path in argv for e in check_file(path)]
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
