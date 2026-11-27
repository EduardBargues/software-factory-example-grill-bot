"""Given / When / Then test DSL. A Scenario hides the mocks so tests speak only GLOSSARY terms.

Tense by role: given → future ("the bot will open…"), when → present ("the bot opens…"),
then → past ("the bot opened…"). Say each concept the same way across the three.
"""

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
    def the_bot_will_open_a_grilling_session(
        self, scenario: Scenario, *, reporting_ts: str
    ) -> None:
        scenario.client.chat_postMessage.return_value = {"ts": reporting_ts}

    def an_active_grilling_session(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.owned.add(in_thread)


class _When:
    def the_bot_opens_a_grilling_session(self, scenario: Scenario, *, in_channel: str) -> None:
        scenario.posted_ts = post_root(scenario.client, in_channel, OPENER_TEXT)

    def the_bot_is_mentioned(self, scenario: Scenario, *, in_thread: str, with_answer: str) -> None:
        handler = _make_mention_handler(scenario.owned)
        handler({"thread_ts": in_thread, "text": f"<@UAPP> {with_answer}"}, scenario.say)

    def the_bot_is_mentioned_with_no_answer(self, scenario: Scenario, *, in_thread: str) -> None:
        handler = _make_mention_handler(scenario.owned)
        handler({"thread_ts": in_thread, "text": "<@UAPP>"}, scenario.say)


class _Then:
    def the_bot_opened_a_grilling_session(
        self, scenario: Scenario, *, owning_thread: str, in_channel: str
    ) -> None:
        assert scenario.posted_ts == owning_thread
        scenario.client.chat_postMessage.assert_called_once_with(
            channel=in_channel, text=OPENER_TEXT
        )

    def the_bot_responded_with(self, scenario: Scenario, answer: str, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=answer, thread_ts=in_thread)

    def the_bot_said_it_was_out_of_session(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=OUT_OF_SESSION_MESSAGE, thread_ts=in_thread)

    def the_bot_nudged_the_empty_mention(self, scenario: Scenario, *, in_thread: str) -> None:
        scenario.say.assert_called_once_with(text=EMPTY_MENTION_MESSAGE, thread_ts=in_thread)


given = _Given()
when = _When()
then = _Then()
