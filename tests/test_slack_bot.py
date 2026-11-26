from pytest_mock import MockerFixture

from tests.dsl import given, then, when

OWNED = "123.456"
OTHER = "999.999"
CHANNEL = "#grill"


def test_when_posting_an_opener(mocker: MockerFixture) -> None:
    # Given a Slack client that reports a ts for the posted message
    client = given.a_slack_client_reporting_ts(mocker, OWNED)
    # When the bot posts the opener
    ts = when.the_bot_posts_an_opener(client, channel=CHANNEL, text="Session started")
    # Then the bot owns that thread and posted exactly one opener
    then.the_bot_owns_the_thread(ts, OWNED)
    then.the_bot_posted_the_opener(client, channel=CHANNEL, text="Session started")


def test_when_mentioned_in_an_owned_thread(mocker: MockerFixture) -> None:
    # Given an owned thread with an active session
    say = given.a_say(mocker)
    handler = given.a_bot_owning(OWNED)
    # When someone answers by mentioning the bot there
    when.mentioned(handler, say, text="<@UAPP> yes, ship it", thread_ts=OWNED)
    # Then the bot responds in that thread with the answer, mention stripped
    then.the_bot_responded(say, text="yes, ship it", thread_ts=OWNED)


def test_when_mentioned_in_an_unowned_thread(mocker: MockerFixture) -> None:
    # Given a thread the bot does not own
    say = given.a_say(mocker)
    handler = given.a_bot_owning(OWNED)
    # When the bot is mentioned there
    when.mentioned(handler, say, text="<@UAPP> hi", thread_ts=OTHER)
    # Then the bot explains it only helps inside an active session
    then.the_bot_explained_it_is_out_of_session(say, thread_ts=OTHER)


def test_when_mentioned_with_only_a_mention(mocker: MockerFixture) -> None:
    # Given an owned thread with an active session
    say = given.a_say(mocker)
    handler = given.a_bot_owning(OWNED)
    # When the message is only the mention, carrying no answer
    when.mentioned(handler, say, text="<@UAPP>", thread_ts=OWNED)
    # Then the bot nudges that the message looks empty
    then.the_bot_nudged_the_empty_mention(say, thread_ts=OWNED)
