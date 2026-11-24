# software-factory-example-grill-bot

> Convene a ticket in Slack, grill it into a spec, ship it back to the factory.

Slack grilling bot for the software factory: convenes a needs-a-human ticket in a Slack thread, then runs grill -> to-spec -> to-tickets back into the factory (home-repo ADR-0005).

Part of a multi-repo software factory — see the hub:
<https://github.com/EduardBargues/software-factory-example-home-repo>.

## Local setup

```bash
./scripts/dev-setup.sh
```

## Brakes

`ruff`, `mypy --strict`, `pytest` (+coverage), plus `gitleaks` / `bandit` /
`pip-audit` / `actionlint`, run via pre-commit and the `brakes` CI check.
