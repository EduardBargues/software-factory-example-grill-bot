"""Bolt Socket Mode bot skeleton — thread-owning echo bot."""

from collections.abc import Callable
from typing import Any

from slack_bolt import App
from slack_bolt.context.say.say import Say
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


def post_root(client: WebClient, channel: str, text: str) -> str:
    """Posts a root message; returns its ts (the owned thread_ts)."""
    resp: SlackResponse = client.chat_postMessage(channel=channel, text=text)
    return str(resp["ts"])


def _make_message_handler(owned_thread_ts: str) -> Callable[..., None]:
    """Returns a Bolt message event handler that echoes only in owned_thread_ts."""

    def handle_message(event: dict[str, Any], say: Say) -> None:
        if event.get("thread_ts") != owned_thread_ts:
            return
        text = event.get("text")
        if text is None:
            return
        say(text=str(text), thread_ts=owned_thread_ts)

    return handle_message


def build_app(bot_token: str, owned_thread_ts: str) -> App:
    """Creates a Bolt App wired to reply only within owned_thread_ts."""
    app = App(token=bot_token)
    app.event("message")(_make_message_handler(owned_thread_ts))
    return app
