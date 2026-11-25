from typing import Any
from unittest.mock import MagicMock

from hypothesis import given
from hypothesis import strategies as st

from grill_bot.adapters.slack_bot import _make_mention_handler, post_root

OWNED = "123.456"


@given(channel=st.text(min_size=1), text=st.text(min_size=1))
def test_when_posting_a_root_message_it_returns_the_new_thread_ts(channel: str, text: str) -> None:
    # Given a Slack client that reports a ts for the posted message
    client = MagicMock()
    client.chat_postMessage.return_value = {"ts": OWNED}
    # When we post a root message
    ts = post_root(client, channel, text)
    # Then we get that ts back (the owned thread_ts) and sent exactly one message
    assert ts == OWNED
    client.chat_postMessage.assert_called_once_with(channel=channel, text=text)


@given(text=st.text(min_size=1))
def test_when_mentioned_in_the_owned_thread_it_echoes(text: str) -> None:
    # Given a mention handler bound to the owned thread
    say = MagicMock()
    handle = _make_mention_handler(OWNED)
    # When the bot is @mentioned inside its owned thread
    handle({"thread_ts": OWNED, "text": text}, say)
    # Then it echoes the text back into that thread, once
    say.assert_called_once_with(text=text, thread_ts=OWNED)


@given(other_thread=st.text(min_size=1).filter(lambda s: s != OWNED), text=st.text(min_size=1))
def test_when_mentioned_in_another_thread_it_stays_silent(other_thread: str, text: str) -> None:
    # Given a mention handler bound to the owned thread
    say = MagicMock()
    handle = _make_mention_handler(OWNED)
    # When the bot is @mentioned in a different thread
    handle({"thread_ts": other_thread, "text": text}, say)
    # Then it does not react
    say.assert_not_called()


@given(text=st.text(min_size=1))
def test_when_mentioned_outside_any_thread_it_stays_silent(text: str) -> None:
    # Given a mention handler bound to the owned thread
    say = MagicMock()
    handle = _make_mention_handler(OWNED)
    # When the bot is @mentioned at channel root (no thread_ts)
    handle({"text": text}, say)
    # Then it does not react — it only works inside its owned thread
    say.assert_not_called()


@given(text=st.none() | st.just(""))
def test_when_mentioned_with_no_text_it_stays_silent(text: str | None) -> None:
    # Given a mention handler bound to the owned thread
    say = MagicMock()
    handle = _make_mention_handler(OWNED)
    # When a text-less mention arrives in the owned thread
    event: dict[str, Any] = {"thread_ts": OWNED}
    if text is not None:
        event["text"] = text
    handle(event, say)
    # Then it does not react
    say.assert_not_called()
