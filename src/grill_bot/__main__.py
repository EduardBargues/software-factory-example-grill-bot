"""Entry point — connect to Slack via Socket Mode and listen.

The service runs constantly. It does **not** post anything on startup. Grilling sessions
are started by the polling loop (ticket 07): on an `agent:grill-with-docs` issue it posts
an opener, registers that thread as owned, and the mention-handler then responds to
@mentions inside it. This entry point just stands up the listener with an initially empty
set of owned threads.

In a container (Fargate) there is no `.env`; creds arrive as injected env vars, so
`load_dotenv(override=False)` is a no-op there and the real environment always wins.
"""

import os

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

from grill_bot.adapters.slack_bot import build_app


def main() -> None:
    load_dotenv(override=False)  # no-op in a container; injected env vars take precedence
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    app_token = os.environ["SLACK_APP_TOKEN"]

    owned_threads: set[str] = set()  # populated per session by the polling loop (ticket 07)
    app = build_app(bot_token, owned_threads)
    SocketModeHandler(app, app_token).start()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()
