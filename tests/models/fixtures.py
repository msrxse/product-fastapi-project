import pytest
from sqlalchemy import inspect


# db_session as from tests/fixtures.py since it has autouse=True not we have access here
@pytest.fixture(scope="function")
def db_inspector(db_session):
    return inspect(db_session().bind)
