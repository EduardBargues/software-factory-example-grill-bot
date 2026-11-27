# Coding standards

Conventions the factory enforces — some as automated **checks**, the rest by the **review**
brake (for what no check can express). Grown and pruned via `/retro`.

## Architecture

- **Adapters hold technology; the domain doesn't.** Technology-specific code (Slack, AWS, GitHub, …) lives under `src/grill_bot/adapters/<tech>.py`; domain logic stays outside `adapters/` and never imports a vendor SDK directly (ports & adapters).

## Testing

- **The DSL speaks the domain** — the `given`/`when`/`then` helpers in [`tests/dsl.py`](tests/dsl.py) read in [`GLOSSARY.md`](GLOSSARY.md) vocabulary, conjugated by role: **given** future ("the bot *will* open…"), **when** present ("the bot *opens*…"), **then** past ("the bot *opened*…"). Say the same concept the same way across the three. *(The mechanical rules — `test_when_` naming, given/when/then usage, assert-only-via-`then`, mocks via pytest-mock — are enforced by `scripts/check_test_conventions.py` and ruff; not restated here.)*
