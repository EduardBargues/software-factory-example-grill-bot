"""Local dev entry point — reads xoxb/xapp from .env and starts Socket Mode."""

import os

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from grill_bot.bot import build_app, post_root


def main() -> None:
    load_dotenv()
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    app_token = os.environ["SLACK_APP_TOKEN"]
    channel = os.environ.get("SLACK_CHANNEL", "#grill-bot")

    client = WebClient(token=bot_token)
    thread_ts = post_root(client, channel, "Grill session started.")

    app = build_app(bot_token, thread_ts)
    SocketModeHandler(app, app_token).start()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()
