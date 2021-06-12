from fastapi.testclient import TestClient

from tutoapi.data import DATA
from tutoapi.main import app

client = TestClient(app)


def test_list():
    response = client.get("/list")
    assert response.status_code == 200
    assert len(response.json()) == len(DATA)

    filters = ["first_name"]
    response = client.get(f'/list?filters={",".join(filters)}')
    datas = response.json()
    assert response.status_code == 200
    assert len(datas) == len(DATA)
    assert all(
        len(data) == len(filters) + 1
        and list(filter(lambda x: x != "id", data.keys())) == filters
        for data in datas
    )


def test_item():
    response = client.get("/items/10")
    assert response.status_code == 200
    assert len(response.json()) == len(DATA[10])

    filters = ["first_name"]
    response = client.get(f'/items/10?filters={",".join(filters)}')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(filters) + 1
    assert list(filter(lambda x: x != "id", data.keys())) == filters
