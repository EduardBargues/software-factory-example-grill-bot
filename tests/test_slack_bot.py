from typing import Any

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from pytest_mock import MockerFixture

from grill_bot.adapters.slack_bot import _make_mention_handler, post_root

OWNED = "123.456"

# hypothesis re-runs each test body many times, but the function-scoped `mocker` fixture
# is set up once; we create a fresh mock per example from it, so the health check is moot.
_FIXTURE_OK = [HealthCheck.function_scoped_fixture]


@settings(suppress_health_check=_FIXTURE_OK)
@given(channel=st.text(min_size=1), text=st.text(min_size=1))
def test_when_posting_a_root_message(mocker: MockerFixture, channel: str, text: str) -> None:
    # Given a Slack client that reports a ts for the posted message
    client = mocker.MagicMock()
    client.chat_postMessage.return_value = {"ts": OWNED}
    # When we post a root message
    ts = post_root(client, channel, text)
    # Then we own the returned thread, and sent exactly one message
    assert ts == OWNED
    client.chat_postMessage.assert_called_once_with(channel=channel, text=text)


@settings(suppress_health_check=_FIXTURE_OK)
@given(body=st.text().filter(lambda s: "<@" not in s and s.strip() != ""))
def test_when_mentioned_in_an_owned_thread(mocker: MockerFixture, body: str) -> None:
    # Given an active session in the owned thread
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When the bot is tagged with content in that thread
    handle({"thread_ts": OWNED, "text": f"<@UAPP> {body}"}, say)
    # Then it echoes the content with the tag stripped, once, in that thread
    say.assert_called_once_with(text=body.strip(), thread_ts=OWNED)


@settings(suppress_health_check=_FIXTURE_OK)
@given(other=st.text(min_size=1).filter(lambda s: s != OWNED), body=st.text(min_size=1))
def test_when_mentioned_in_an_unowned_thread(mocker: MockerFixture, other: str, body: str) -> None:
    # Given no active session in the thread the mention lands in
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When the bot is tagged there
    handle({"thread_ts": other, "text": f"<@UAPP> {body}"}, say)
    # Then it does not react
    say.assert_not_called()


@settings(suppress_health_check=_FIXTURE_OK)
@given(tag=st.sampled_from(["<@UAPP>", "<@UAPP> ", "  <@UAPP>  ", "<@UAPP><@UBOB>"]))
def test_when_mentioned_with_only_a_tag(mocker: MockerFixture, tag: str) -> None:
    # Given an active session in the owned thread
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When the bot is tagged with no other content
    handle({"thread_ts": OWNED, "text": tag}, say)
    # Then the stripped message is empty, so it does not react
    say.assert_not_called()


@settings(suppress_health_check=_FIXTURE_OK)
@given(text=st.none() | st.just(""))
def test_when_mentioned_with_no_text(mocker: MockerFixture, text: str | None) -> None:
    # Given an active session in the owned thread
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When a text-less mention arrives
    event: dict[str, Any] = {"thread_ts": OWNED}
    if text is not None:
        event["text"] = text
    handle(event, say)
    # Then it does not react
    say.assert_not_called()
