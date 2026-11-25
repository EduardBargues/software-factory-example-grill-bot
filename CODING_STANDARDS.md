# Coding standards

Fuzzy rules the **review** brake enforces, for things no automated check can express.
Grown and pruned via `/retro`.

## Architecture

- **Adapters hold technology; the domain doesn't.** Technology-specific code (Slack, AWS, GitHub, …) lives under `src/grill_bot/adapters/<tech>.py`; domain logic stays outside `adapters/` and never imports a vendor SDK directly. This keeps the technologies obvious and swappable (ports & adapters).

## Testing

- **Property-based, Given/When/Then.** Tests use [`hypothesis`](https://hypothesis.readthedocs.io): every test carries an `@given(...)` decorator, is named `test_when_<scenario>`, and is laid out in **Given / When / Then** blocks (comment each). Assert as many facts as the scenario needs. This ties tests to the agreed business logic rather than hand-picked examples.
