"""Slack adapter — Socket Mode bot that reacts only to @mentions in its owned thread."""

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


def _make_mention_handler(owned_thread_ts: str) -> Callable[..., None]:
    """Returns an app_mention handler that echoes only when tagged in owned_thread_ts.

    The bot reacts solely to @mentions inside the thread it owns — never to the free
    discussion people have in that thread — so a busy thread stays quiet until someone
    tags the bot to submit an answer (ADR-0005).
    """

    def handle_mention(event: dict[str, Any], say: Say) -> None:
        if event.get("thread_ts") != owned_thread_ts:
            return
        text = event.get("text")
        if not text:
            return
        say(text=str(text), thread_ts=owned_thread_ts)

    return handle_mention


def build_app(bot_token: str, owned_thread_ts: str) -> App:
    """Creates a Bolt App that replies only to @mentions within owned_thread_ts."""
    app = App(token=bot_token)
    app.event("app_mention")(_make_mention_handler(owned_thread_ts))
    return app
