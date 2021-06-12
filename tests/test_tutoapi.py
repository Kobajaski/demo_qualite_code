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
        len(data) == len(filters) + 1 and list(filter(lambda x: x != "id", data.keys())) == filters for data in datas
    )

    response = client.post("/list/append", json=[{k: v for k, v in DATA[0].dict().items() if k != "id"}])
    assert response.status_code == 200
    assert response.json().get("state") == "success"
    assert response.json().get("count") == 1


def test_item():
    response = client.get("/items/10")
    assert response.status_code == 200
    assert len(response.json()) == len(DATA[10].dict())

    filters = ["first_name"]
    response = client.get(f'/items/10?filters={",".join(filters)}')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(filters) + 1
    assert list(filter(lambda x: x != "id", data.keys())) == filters

    response = client.post("/items/append", json={k: v for k, v in DATA[0].dict().items() if k != "id"})
    assert response.status_code == 200
    assert response.json().get("state") == "success"
    assert response.json().get("count") == 1
