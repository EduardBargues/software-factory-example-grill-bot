# Glossary — software-factory-example-grill-bot

Repo-specific vocabulary. Shared, repo-independent factory vocabulary lives in the hub's
[`GLOSSARY.md`](../software-factory-example-home-repo/GLOSSARY.md) (see the hub's
`GLOSSARY-MAP.md`) — **grilling session** and **frontier** are defined there. Add only
terms unique to this repo. Tests assert in these words (see `CODING_STANDARDS.md`).

## Slack grilling

- **Owned thread** — a Slack thread the bot is driving an active grilling session in. The bot **owns** it from the moment it posts the **opener** until the session resolves, and reacts to **mentions** only inside owned threads. _Avoid: session thread, active thread._
- **Opener** — the root message the bot posts to start a session; its `ts` becomes the owned thread's id. Carries the issue link and the "mention me to answer" note. _Avoid: root message, starter._
- **Mention** — an `@`-reference to the bot in a message. The bot's **only** trigger — it reacts to nothing else. _Avoid: tag, ping._
- **Answer** — a message in an owned thread that **mentions** the bot; its text, once the mention is stripped, is a human's response. With the bot's own messages, answers are the **only** content a grilling session considers. _Avoid: reply (collides with Slack's thread-reply)._
- **Free discussion** — messages in an owned thread that do **not** mention the bot; people talking among themselves. The bot ignores them and never treats them as answers. _Avoid: chatter, noise._
- **Session registry** — the in-process set of owned threads (one per active grilling). A mention is handled only if its thread is in the registry. _Avoid: session store, thread map._
