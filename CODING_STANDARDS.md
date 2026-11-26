# Coding standards

Conventions the factory enforces — some as automated **checks**, the rest by the **review**
brake (for what no check can express). Grown and pruned via `/retro`.

## Architecture

- **Adapters hold technology; the domain doesn't.** Technology-specific code (Slack, AWS, GitHub, …) lives under `src/grill_bot/adapters/<tech>.py`; domain logic stays outside `adapters/` and never imports a vendor SDK directly. This keeps the technologies obvious and swappable (ports & adapters).

## Testing

- **Property-based, named by scenario** — *hard rule, `scripts/check_test_conventions.py`*: every test carries an `@given(...)` decorator and is named `test_when_<scenario>` (name the *scenario*, not the expectation — a scenario can assert several things).
- **Given / When / Then layout** — *review-enforced*: lay the body out in Given / When / Then blocks, one comment each.
- **Assert in the domain vocabulary** — *review-enforced*: use the fluent `then` helpers in [`tests/dsl.py`](tests/dsl.py) (e.g. `then.the_bot_owns_the_thread(ts, OWNED)`), which read in [`GLOSSARY.md`](GLOSSARY.md) terms, instead of raw mock assertions.
