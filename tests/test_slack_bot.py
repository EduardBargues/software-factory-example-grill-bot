from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from pytest_mock import MockerFixture

from grill_bot.adapters.slack_bot import _make_mention_handler, post_root
from tests.dsl import then

OWNED = "123.456"

# hypothesis re-runs each test body many times, but the function-scoped `mocker` fixture
# is set up once; we create a fresh mock per example from it, so the health check is moot.
_FIXTURE_OK = [HealthCheck.function_scoped_fixture]


@settings(suppress_health_check=_FIXTURE_OK)
@given(channel=st.text(min_size=1), text=st.text(min_size=1))
def test_when_posting_an_opener(mocker: MockerFixture, channel: str, text: str) -> None:
    # Given a Slack client that reports a ts for the posted message
    client = mocker.MagicMock()
    client.chat_postMessage.return_value = {"ts": OWNED}
    # When the bot posts the opener
    ts = post_root(client, channel, text)
    # Then the bot owns the new thread, and posted exactly one message
    then.the_bot_owns_the_thread(ts, OWNED)
    then.the_bot_posted_the_opener(client, channel=channel, text=text)


@settings(suppress_health_check=_FIXTURE_OK)
@given(body=st.text().filter(lambda s: "<@" not in s and s.strip() != ""))
def test_when_mentioned_in_an_owned_thread(mocker: MockerFixture, body: str) -> None:
    # Given an owned thread with an active session
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When someone answers by mentioning the bot in that thread
    handle({"thread_ts": OWNED, "text": f"<@UAPP> {body}"}, say)
    # Then the bot echoes the answer back, with the mention stripped
    then.the_bot_echoed(say, text=body.strip(), thread_ts=OWNED)


@settings(suppress_health_check=_FIXTURE_OK)
@given(other=st.text(min_size=1).filter(lambda s: s != OWNED), body=st.text(min_size=1))
def test_when_mentioned_in_an_unowned_thread(mocker: MockerFixture, other: str, body: str) -> None:
    # Given a thread the bot does not own (no active session there)
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When the bot is mentioned there
    handle({"thread_ts": other, "text": f"<@UAPP> {body}"}, say)
    # Then the bot stays silent
    then.the_bot_stayed_silent(say)


@settings(suppress_health_check=_FIXTURE_OK)
@given(mention=st.sampled_from(["<@UAPP>", "<@UAPP> ", "  <@UAPP>  ", "<@UAPP><@UBOB>"]))
def test_when_mentioned_with_only_a_mention(mocker: MockerFixture, mention: str) -> None:
    # Given an owned thread
    say = mocker.MagicMock()
    handle = _make_mention_handler({OWNED})
    # When the message is only the mention, carrying no answer text
    handle({"thread_ts": OWNED, "text": mention}, say)
    # Then the stripped text is empty — not an answer — so the bot stays silent
    then.the_bot_stayed_silent(say)
