#!/usr/bin/env python3
"""Pre-commit check: test functions follow the convention in CODING_STANDARDS.md.

Each `def test_*` under tests/ must be named `test_when_<scenario>` and carry an
`@given(...)` decorator. (The Given/When/Then body layout is review-enforced.)
"""

import ast
import sys

_TestDef = (ast.FunctionDef, ast.AsyncFunctionDef)


def _has_given(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for dec in node.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
        if name == "given":
            return True
    return False


def check_file(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, _TestDef) and node.name.startswith("test"):
            if not node.name.startswith("test_when_"):
                errors.append(
                    f"{path}:{node.lineno}: '{node.name}' must be named test_when_<scenario>"
                )
            if not _has_given(node):
                errors.append(f"{path}:{node.lineno}: '{node.name}' needs an @given(...) decorator")
    return errors


def main(argv: list[str]) -> int:
    errors = [e for path in argv for e in check_file(path)]
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
