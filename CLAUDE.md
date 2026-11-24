# software-factory-example-grill-bot

Slack grilling bot for the software factory: convenes a needs-a-human ticket in a Slack thread, then runs grill -> to-spec -> to-tickets back into the factory (home-repo ADR-0005). Part of a multi-repo **software factory** (home-repo ADR-0001).

Read before proposing changes, and use their terms exactly:

- [`GLOSSARY.md`](GLOSSARY.md) — this repo's vocabulary (shared factory terms live in the hub).
- [`CODING_STANDARDS.md`](CODING_STANDARDS.md) — fuzzy rules the review brake enforces.
- [`docs/adr/`](docs/adr/) — Architecture Decision Records.

## The multi-repo factory

- **Hub** — [`software-factory-example-home-repo`](https://github.com/EduardBargues/software-factory-example-home-repo) (`../software-factory-example-home-repo`; clone if missing). **Read its `CLAUDE.md` to understand — or answer questions about — the whole factory** (brakes, accelerators, topology). Run *cross-repo* sessions from there.

## Agent skills

### Issue tracker

Issues and specs are tracked in this repo's **GitHub Issues** (via the `gh` CLI). See `docs/agents/issue-tracker.md`.
