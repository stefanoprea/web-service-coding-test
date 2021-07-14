from .fixtures import *
import tests.testdata


def test_post_kpi_validate_params_no_body(client):
    response = client.post("/kpi/")
    assert response.status_code == 422

def test_post_kpi_validate_params_name_missing(client):
    kpi = testdata.kpis[0]
    response = client.post("/kpi/", json=filter_dict(kpi, ["description"]))
    assert response.status_code == 422

def test_post_kpi_validate_params_description_missing(client):
    kpi = testdata.kpis[0]
    response = client.post("/kpi/", json=filter_dict(kpi, ["name"]))
    assert response.status_code == 422

def test_post_kpi_ok(clean_db, client):
    kpi = testdata.kpis[0]
    response = client.post("/kpi/", json=filter_dict(
        kpi,
        ["name", "description"]
        ))
    assert response.status_code == 201
    assert response.json() == kpi

def test_post_kpi_with_parent(populate_db, client):
    kpi = {
        "id": 11,
        "name": "foo",
        "description": "bar",
        "parent_id": 3
    }
    response = client.post("/kpi/", json=filter_dict(
        kpi,
        ["name", "description", "parent_id"]
        ))
    assert response.status_code == 201
    assert response.json() == kpi

def test_post_kpi_wrong_parent(populate_db, client):
    kpi = {
        "id": 11,
        "name": "foo",
        "description": "bar",
        "parent_id": 100
    }
    response = client.post("/kpi/", json=filter_dict(
        kpi,
        ["name", "description", "parent_id"]
        ))
    assert response.status_code == 422

def test_post_value_params_no_body(client):
    response = client.post("/value/")
    assert response.status_code == 422

def test_post_value_params_date_missing(client):
    value = testdata.values[0]
    response = client.post("/value/", json=filter_dict(
        value,
        ["value", "kpi_id"]
        ))
    assert response.status_code == 422

def test_post_value_params_value_missing(client):
    value = testdata.values[0]
    response = client.post("/value/", json=filter_dict(
        value,
        ["date", "kpi_id"]
        ))
    assert response.status_code == 422

def test_post_value_params_kpi_id_missing(client):
    value = testdata.values[0]
    response = client.post("/value/", json=filter_dict(
        value,
        ["date", "value"]
        ))
    assert response.status_code == 422

def test_post_value_ok(populate_db, client):
    value = {
        "id": 43,
        "date": "2021-01-01",
        "value": "7 months",
        "kpi_id": 3
    }
    response = client.post("/value/", json=filter_dict(
        value,
        ["date", "value", "kpi_id"]
        ))
    assert response.status_code == 201
    assert response.json() == value

def test_post_value_params_bad_date(populate_db, client):
    value = {
        "id": 43,
        "date": "2021-15-01",
        "value": "7 months",
        "kpi_id": 3
    }
    response = client.post("/value/", json=filter_dict(
        value,
        ["date", "value", "kpi_id"]
        ))
    assert response.status_code == 422

def test_post_value_bad_kpi_id(client):
    value = {
        "id": 43,
        "date": "2021-01-01",
        "value": "7 months",
        "kpi_id": 100
    }
    response = client.post("/value/", json=filter_dict(
        value,
        ["date", "value", "kpi_id"]
        ))
    assert response.status_code == 422

def test_get_kpi_params_no_id(client):
    response = client.get("/kpi/")
    assert response.status_code == 405

def test_get_kpi_bad_id(client):
    id = 100
    response = client.get(f"/kpi/{id}")
    assert response.status_code == 404

def test_get_kpi_ok(populate_db, client):
    id = 5
    response = client.get(f"/kpi/{id}")
    assert response.status_code == 200
    assert response.json() == {
        'id': 5,
        'name': 'Company 1 Runway',
        'description': 'This is the Company 1 Runway',
        'parent_id': 3,
        'values': [
            {'date': '2021-12-01', 'value': '1 months'},
            {'date': '2021-11-01', 'value': '2 months'},
            {'date': '2021-10-01', 'value': '3 months'},
            {'date': '2021-09-01', 'value': '4 months'},
            {'date': '2021-08-01', 'value': '5 months'}
        ]
    }

def test_get_value_ok(populate_db, client):
    value = testdata.values[10]
    response = client.get(f"/value/{value['id']}")
    assert response.status_code == 200
    assert response.json() == value

def test_delete_kpi_params_no_id(client):
    response = client.delete("/kpi/")
    assert response.status_code == 405

def test_delete_kpi_bad_id(client):
    id = 100
    response = client.delete(f"/kpi/{id}")
    assert response.status_code == 404

def test_delete_kpi_ok_with_cascade(
    populate_db,
    obtain_delete_kpi_testdata,
    resource_was_deleted,
    client
    ):
    kpi, kpi_child, value = obtain_delete_kpi_testdata
    response = client.delete(f"/kpi/{kpi['id']}")
    assert response.status_code == 200
    assert resource_was_deleted("/kpi/", kpi["id"])
    assert resource_was_deleted("/kpi/", kpi_child["id"])
    assert resource_was_deleted("/value/", value["id"])

@pytest.fixture
def obtain_delete_kpi_testdata():
    kpi_parent = testdata.kpis[0]
    kpi = testdata.kpis[2]
    kpi_child = testdata.kpis[4]
    value = testdata.values[3]
    assert kpi["parent_id"] == kpi_parent["id"]
    assert kpi_child["parent_id"] == kpi["id"]
    assert value["kpi_id"] == kpi_child["id"]
    return kpi, kpi_child, value

@pytest.fixture
def resource_was_deleted(client):
    def check(endpoint, id):
        return client.get(f"{endpoint}{id}").status_code == 404
    return check
