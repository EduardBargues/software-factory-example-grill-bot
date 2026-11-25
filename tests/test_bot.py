from unittest.mock import MagicMock

from grill_bot.bot import _make_message_handler, post_root


def test_post_root_returns_ts() -> None:
    client = MagicMock()
    client.chat_postMessage.return_value = {"ts": "123.456"}
    ts = post_root(client, "#general", "Hello!")
    assert ts == "123.456"
    client.chat_postMessage.assert_called_once_with(channel="#general", text="Hello!")


def test_handler_replies_in_owned_thread() -> None:
    say = MagicMock()
    handler = _make_message_handler("123.456")
    handler({"thread_ts": "123.456", "text": "hello"}, say)
    say.assert_called_once_with(text="hello", thread_ts="123.456")


def test_handler_ignores_unowned_thread() -> None:
    say = MagicMock()
    handler = _make_message_handler("123.456")
    handler({"thread_ts": "999.999", "text": "hello"}, say)
    say.assert_not_called()


def test_handler_ignores_root_message() -> None:
    say = MagicMock()
    handler = _make_message_handler("123.456")
    handler({"text": "hello"}, say)  # no thread_ts
    say.assert_not_called()
