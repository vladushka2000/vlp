import pytest
import mock
from fastapi.testclient import TestClient

from src.main import app
from src.db import get_session


@pytest.fixture()
def api_client():
    return TestClient(app)


@pytest.fixture()
def sa_session():
    session = get_session()
    with mock.patch("sqlalchemy.orm.Session.commit", side_effect=session.flush):
        yield session

    session.rollback()
    session.close()
