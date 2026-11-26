"""Fluent, domain-named test assertions (GLOSSARY.md). Tests read as Given / When / Then."""

from unittest.mock import MagicMock


class _Then:
    """Domain assertions so tests speak the project's vocabulary (GLOSSARY.md)."""

    def the_bot_owns_the_thread(self, returned_ts: str, expected_ts: str) -> None:
        assert returned_ts == expected_ts

    def the_bot_posted_the_opener(self, client: MagicMock, *, channel: str, text: str) -> None:
        client.chat_postMessage.assert_called_once_with(channel=channel, text=text)

    def the_bot_echoed(self, say: MagicMock, *, text: str, thread_ts: str) -> None:
        say.assert_called_once_with(text=text, thread_ts=thread_ts)

    def the_bot_stayed_silent(self, say: MagicMock) -> None:
        say.assert_not_called()


then = _Then()
