import pytest
from pytest_mock import MockerFixture

from tests.dsl import Scenario


@pytest.fixture
def scenario(mocker: MockerFixture) -> Scenario:
    return Scenario(mocker)
