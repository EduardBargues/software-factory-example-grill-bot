from tests.dsl import Scenario, given, then, when

OWNED = "123.456"
OTHER = "999.999"
CHANNEL = "#grill"


def test_when_posting_an_opener(scenario: Scenario) -> None:
    given.a_channel_that_reports_its_ts(scenario, ts=OWNED)
    when.the_bot_posts_an_opener(scenario, in_channel=CHANNEL)
    then.the_bot_owns_the_thread(scenario, OWNED)
    then.the_bot_posted_an_opener(scenario, in_channel=CHANNEL)


def test_when_mentioned_in_an_owned_thread(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned(scenario, in_thread=OWNED, with_answer="yes, ship it")
    then.the_bot_responds_with(scenario, "yes, ship it", in_thread=OWNED)


def test_when_mentioned_in_an_unowned_thread(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned(scenario, in_thread=OTHER, with_answer="hi")
    then.the_bot_says_it_is_out_of_session(scenario, in_thread=OTHER)


def test_when_mentioned_with_no_answer(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned_with_no_answer(scenario, in_thread=OWNED)
    then.the_bot_nudges_the_empty_mention(scenario, in_thread=OWNED)
