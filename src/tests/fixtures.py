from controllers.controllers import App
from db.connector import DBConnector
import db.models as models
from fastapi.testclient import TestClient
import pytest
import tests.testdata as testdata


def filter_dict(d, keys):
    return {k: v for k, v in d.items() if k in keys}

@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)

@pytest.fixture(scope="session")
def app(stub_db):
    return App(stub_db)

@pytest.fixture(scope="session")
def stub_db(database_path):
    database_url = f"sqlite:///{database_path}"
    test_db_connector = DBConnector(database_url)
    models.Base.metadata.create_all(bind=test_db_connector.engine)
    return test_db_connector

@pytest.fixture(scope="session")
def database_path(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("pytest") / "test_db.sqlite"
    open(db_path, "w").close()     # erase the file
    return db_path

@pytest.fixture()
def clean_db(stub_db):
    delete_all_rows(stub_db.engine)
    yield
    delete_all_rows(stub_db.engine)

def delete_all_rows(engine):
    with engine.connect() as con:
        for table_name in models.Base.metadata.tables.keys():
            # This isn't vulnerable to SQL injection, however...
            # DON'T do this in production code!
            # For unit tests I think it's ok.
            con.execute(f"DELETE FROM {table_name}")

@pytest.fixture()
def populate_db(clean_db, client):
    post_kpis(client)
    post_values(client)

def post_kpis(client):
    for kpi in testdata.kpis:
        response = client.post("/kpi/", json=filter_dict(
            kpi,
            ["name", "description", "parent_id"]
            ))
        assert response.status_code == 201
        assert response.json() == kpi

def post_values(client):
    for value in testdata.values:
        response = client.post("/value/", json=filter_dict(
            value,
            ["date", "value", "kpi_id"]
        ))
        assert response.status_code == 201
        assert response.json() == value
