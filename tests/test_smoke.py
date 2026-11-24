from grill_bot import healthcheck


def test_healthcheck() -> None:
    assert healthcheck() is True
