import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from .test_data.load_data import load_all

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .main import get_session
from .main import app


@pytest.fixture(name="session")
def session_fixture():
    # add echo=True parameter to debug SQL statements
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_heroes(session: Session, client: TestClient):
    load_all(session)
    response = client.get("/heroes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_get_teams(session: Session, client: TestClient):
    load_all(session)
    response = client.get("/teams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_links(session: Session, client: TestClient):
    load_all(session)
    response = client.get("/links")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
