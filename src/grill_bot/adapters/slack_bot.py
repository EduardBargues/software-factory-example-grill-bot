"""Slack adapter — Socket Mode bot that replies only to @mentions in threads it owns."""

import re
from collections.abc import Callable
from typing import Any

from slack_bolt import App
from slack_bolt.context.say.say import Say
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

_MENTION_RE = re.compile(r"<@[A-Z0-9]+>")


def _strip_mentions(text: str) -> str:
    """Removes Slack mentions (`<@U…>`) and surrounding whitespace."""
    return _MENTION_RE.sub("", text).strip()


def post_root(client: WebClient, channel: str, text: str) -> str:
    """Posts a root message; returns its ts (the owned thread_ts)."""
    resp: SlackResponse = client.chat_postMessage(channel=channel, text=text)
    return str(resp["ts"])


def _make_mention_handler(owned_threads: set[str]) -> Callable[..., None]:
    """Returns an app_mention handler that replies only inside threads it owns.

    The bot reacts solely to @mentions inside an active session's thread — never to the
    free discussion people have there — so a busy thread stays quiet unless someone tags
    the bot to submit an answer (ADR-0005). The bot's own mention is stripped from the
    text first, so a bare tag with no content is ignored. `owned_threads` is shared
    mutable state: the session loop (ticket 07) adds a thread when a grilling starts.
    """

    def handle_mention(event: dict[str, Any], say: Say) -> None:
        thread_ts = event.get("thread_ts")
        if thread_ts not in owned_threads:
            return
        text = _strip_mentions(str(event.get("text") or ""))
        if not text:
            return
        say(text=text, thread_ts=thread_ts)

    return handle_mention


def build_app(bot_token: str, owned_threads: set[str]) -> App:
    """Creates a Bolt App that replies to @mentions within owned (active-session) threads."""
    app = App(token=bot_token)
    app.event("app_mention")(_make_mention_handler(owned_threads))
    return app
