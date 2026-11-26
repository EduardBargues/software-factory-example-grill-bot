"""Fluent given / when / then DSL in GLOSSARY.md vocabulary. Tests assert only via `then`."""

from collections.abc import Callable
from typing import Any

from pytest_mock import MockerFixture, MockType

from grill_bot.adapters.slack_bot import (
    EMPTY_MENTION_MESSAGE,
    OUT_OF_SESSION_MESSAGE,
    _make_mention_handler,
    post_root,
)


class _Given:
    def a_say(self, mocker: MockerFixture) -> MockType:
        say: MockType = mocker.MagicMock()
        return say

    def a_slack_client_reporting_ts(self, mocker: MockerFixture, ts: str) -> MockType:
        client: MockType = mocker.MagicMock()
        client.chat_postMessage.return_value = {"ts": ts}
        return client

    def a_bot_owning(self, *threads: str) -> Callable[..., None]:
        return _make_mention_handler(set(threads))


class _When:
    def the_bot_posts_an_opener(self, client: MockType, *, channel: str, text: str) -> str:
        return post_root(client, channel, text)

    def mentioned(
        self,
        handler: Callable[..., None],
        say: MockType,
        *,
        text: str,
        thread_ts: str | None = None,
    ) -> None:
        event: dict[str, Any] = {"text": text}
        if thread_ts is not None:
            event["thread_ts"] = thread_ts
        handler(event, say)


class _Then:
    def the_bot_owns_the_thread(self, returned_ts: str, expected_ts: str) -> None:
        assert returned_ts == expected_ts

    def the_bot_posted_the_opener(self, client: MockType, *, channel: str, text: str) -> None:
        client.chat_postMessage.assert_called_once_with(channel=channel, text=text)

    def the_bot_responded(self, say: MockType, *, text: str, thread_ts: str) -> None:
        say.assert_called_once_with(text=text, thread_ts=thread_ts)

    def the_bot_explained_it_is_out_of_session(self, say: MockType, *, thread_ts: str) -> None:
        say.assert_called_once_with(text=OUT_OF_SESSION_MESSAGE, thread_ts=thread_ts)

    def the_bot_nudged_the_empty_mention(self, say: MockType, *, thread_ts: str) -> None:
        say.assert_called_once_with(text=EMPTY_MENTION_MESSAGE, thread_ts=thread_ts)


given = _Given()
when = _When()
then = _Then()
