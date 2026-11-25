"""Local dev entry point — reads Slack creds from the environment and starts Socket Mode.

In a container (Fargate) there is no `.env`; the creds arrive as injected env vars, so
`load_dotenv(override=False)` is a no-op there and the real environment always wins.
Locally it loads a gitignored `.env`.
"""

import os

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from grill_bot.adapters.slack_bot import build_app, post_root


def main() -> None:
    load_dotenv(override=False)  # no-op in a container; injected env vars take precedence
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    app_token = os.environ["SLACK_APP_TOKEN"]
    channel = os.environ.get("SLACK_CHANNEL", "#grill-bot")
    issue_url = os.environ.get("GRILL_ISSUE_URL", "<issue link>")

    client = WebClient(token=bot_token)
    opener = f"Grilling session started for {issue_url}\nTag me (@grill-bot) to submit an answer."
    thread_ts = post_root(client, channel, opener)

    app = build_app(bot_token, thread_ts)
    SocketModeHandler(app, app_token).start()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()
