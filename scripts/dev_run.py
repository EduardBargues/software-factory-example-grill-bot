"""Dev runner — open a session in a test channel, then listen so you can grill the bot.

The production entry point (`python -m grill_bot`) starts with no sessions; real ones are
seeded by the polling loop (ticket 07), which doesn't exist yet. This runner stands in for
it: it posts an opener to GRILL_DEV_CHANNEL, registers that thread as owned, and starts the
Socket Mode listener. Mention the bot in the thread it opens and it echoes your answer back.

Run it locally after `bash scripts/setup-slack-app.sh` has written the Slack creds to `.env`.
"""

import os

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

from grill_bot.adapters.slack_bot import build_app, post_root

OPENER = "Grilling session open — mention me (@grill-bot) in this thread and I'll echo you back."


def main() -> None:
    load_dotenv(override=False)
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    app_token = os.environ["SLACK_APP_TOKEN"]
    channel = os.environ["GRILL_DEV_CHANNEL"]

    owned_threads: set[str] = set()
    app = build_app(bot_token, owned_threads)

    thread_ts = post_root(app.client, channel, OPENER)
    owned_threads.add(thread_ts)  # register the opener's thread as an owned session
    print(f"Opened a session in {channel} (thread {thread_ts}). Mention the bot in that thread.")

    SocketModeHandler(app, app_token).start()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()
