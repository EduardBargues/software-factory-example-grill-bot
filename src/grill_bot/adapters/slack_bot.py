"""Slack adapter — Socket Mode bot that responds to @mentions, driving owned threads."""

import re
from collections.abc import Callable
from typing import Any

from slack_bolt import App
from slack_bolt.context.say.say import Say
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

_MENTION_RE = re.compile(r"<@[A-Z0-9]+>")

# The bot always responds to a mention (ADR-0005). These are its non-answer replies.
OUT_OF_SESSION_MESSAGE = (
    "Hi! I only help inside an active grilling session, and this thread isn't one yet. "
    "A session starts from a `needs-a-human` issue — mention me there once it's running."
)
EMPTY_MENTION_MESSAGE = (
    "Looks like that message was just my name. Mention me again with your answer "
    "and I'll pick it up."
)


def _strip_mentions(text: str) -> str:
    """Removes Slack mentions (`<@U…>`) and surrounding whitespace."""
    return _MENTION_RE.sub("", text).strip()


def post_root(client: WebClient, channel: str, text: str) -> str:
    """Posts the opener; returns its ts (the owned thread_ts)."""
    resp: SlackResponse = client.chat_postMessage(channel=channel, text=text)
    return str(resp["ts"])


def _make_mention_handler(owned_threads: set[str]) -> Callable[..., None]:
    """Returns an app_mention handler that always responds, in the thread it was tagged in.

    The bot reacts only to @mentions (never free discussion). Inside an owned thread it
    treats the stripped text as an answer and responds (skeleton: echoes it back; ticket
    06 makes this a Claude turn). A mention outside an owned thread, or one carrying no
    answer, gets a short, friendly reply rather than silence. `owned_threads` is shared
    mutable state: the session loop (ticket 07) adds a thread when a grilling starts.
    """

    def handle_mention(event: dict[str, Any], say: Say) -> None:
        # Bolt auto-acks the event; what we say back is separate, so replying (or not)
        # never affects delivery or triggers a Slack retry.
        thread_ts = event.get("thread_ts")
        reply_ts = thread_ts or str(event.get("ts", ""))
        if thread_ts not in owned_threads:
            say(text=OUT_OF_SESSION_MESSAGE, thread_ts=reply_ts)
            return
        answer = _strip_mentions(str(event.get("text") or ""))
        if not answer:
            say(text=EMPTY_MENTION_MESSAGE, thread_ts=reply_ts)
            return
        say(text=answer, thread_ts=reply_ts)

    return handle_mention


def build_app(bot_token: str, owned_threads: set[str]) -> App:
    """Creates a Bolt App that responds to @mentions, driving owned (active-session) threads."""
    app = App(token=bot_token)
    app.event("app_mention")(_make_mention_handler(owned_threads))
    return app
