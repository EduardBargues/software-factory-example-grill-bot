from tests.dsl import Scenario, given, then, when

OWNED = "123.456"
OTHER = "999.999"
CHANNEL = "#grill"


def test_when_opening_a_grilling_session(scenario: Scenario) -> None:
    given.the_bot_will_open_a_grilling_session(scenario, reporting_ts=OWNED)
    when.the_bot_opens_a_grilling_session(scenario, in_channel=CHANNEL)
    then.the_bot_opened_a_grilling_session(scenario, owning_thread=OWNED, in_channel=CHANNEL)


def test_when_mentioned_in_an_owned_thread(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned(scenario, in_thread=OWNED, with_answer="yes, ship it")
    then.the_bot_responded_with(scenario, "yes, ship it", in_thread=OWNED)


def test_when_mentioned_in_an_unowned_thread(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned(scenario, in_thread=OTHER, with_answer="hi")
    then.the_bot_said_it_was_out_of_session(scenario, in_thread=OTHER)


def test_when_mentioned_with_no_answer(scenario: Scenario) -> None:
    given.an_active_grilling_session(scenario, in_thread=OWNED)
    when.the_bot_is_mentioned_with_no_answer(scenario, in_thread=OWNED)
    then.the_bot_nudged_the_empty_mention(scenario, in_thread=OWNED)
