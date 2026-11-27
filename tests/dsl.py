"""Given / When / Then test DSL. A Scenario hides the mocks so tests speak only GLOSSARY terms."""

from pytest_mock import MockerFixture, MockType

from grill_bot.adapters.slack_bot import (
    EMPTY_MENTION_MESSAGE,
    OUT_OF_SESSION_MESSAGE,
    _make_mention_handler,
    post_root,
)

OPENER_TEXT = "Session started"


class Scenario:
    """Holds a test's mocks and state; only the DSL touches them, never a test body."""

    def __init__(self, mocker: MockerFixture) -> None:
        self.say: MockType = mocker.MagicMock()
        self.client: MockType = mocker.MagicMock()
        self.owned: set[str] = set()
        self.posted_ts: str = ""


class _Given:
    def an_active_grilling_session(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.owned.add(in_thread)

    def a_channel_that_reports_its_ts(self, scenario: Scenario, *, ts: str) -> None:
        scenario.client.chat_postMessage.return_value = {"ts": ts}


class _When:
    def the_bot_is_mentioned(self, scenario: Scenario, *, in_thread: str, with_answer: str) -> None:
        handler = _make_mention_handler(scenario.owned)
        handler({"thread_ts": in_thread, "text": f"<@UAPP> {with_answer}"}, scenario.say)

    def the_bot_is_mentioned_with_no_answer(self, scenario: Scenario, *, in_thread: str) -> None:
        handler = _make_mention_handler(scenario.owned)
        handler({"thread_ts": in_thread, "text": "<@UAPP>"}, scenario.say)

    def the_bot_posts_an_opener(self, scenario: Scenario, *, in_channel: str) -> None:
        scenario.posted_ts = post_root(scenario.client, in_channel, OPENER_TEXT)


class _Then:
    def the_bot_owns_the_thread(self, scenario: Scenario, expected_ts: str) -> None:
        assert scenario.posted_ts == expected_ts

    def the_bot_posted_an_opener(self, scenario: Scenario, *, in_channel: str) -> None:
        scenario.client.chat_postMessage.assert_called_once_with(
            channel=in_channel, text=OPENER_TEXT
        )

    def the_bot_responds_with(self, scenario: Scenario, answer: str, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=answer, thread_ts=in_thread)

    def the_bot_says_it_is_out_of_session(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=OUT_OF_SESSION_MESSAGE, thread_ts=in_thread)

    def the_bot_nudges_the_empty_mention(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=EMPTY_MENTION_MESSAGE, thread_ts=in_thread)


given = _Given()
when = _When()
then = _Then()
