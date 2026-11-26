# Coding standards

Conventions the factory enforces — some as automated **checks**, the rest by the **review**
brake (for what no check can express). Grown and pruned via `/retro`.

## Architecture

- **Adapters hold technology; the domain doesn't.** Technology-specific code (Slack, AWS, GitHub, …) lives under `src/grill_bot/adapters/<tech>.py`; domain logic stays outside `adapters/` and never imports a vendor SDK directly (ports & adapters).

## Testing

- **Given / When / Then via the DSL** — *hard rule (`scripts/check_test_conventions.py`)*: every test uses the `given` / `when` / `then` helpers (one call of each) and asserts **only** through `then` — no bare `assert`, no mock `.assert_*`. Test names just describe the scenario; no naming pattern is imposed.
- **Assert in the domain vocabulary** — the `given`/`when`/`then` helpers in [`tests/dsl.py`](tests/dsl.py) speak [`GLOSSARY.md`](GLOSSARY.md) terms; add a helper there rather than asserting inline.
- **Mocks via pytest-mock** — *hard rule (ruff `TID` banned-api)*: create mocks with the `mocker` fixture; `unittest.mock` is banned. Type hints use `pytest_mock.MockType`.
