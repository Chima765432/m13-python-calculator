def add_calculation(client, a=2, b=3, type="Add"):
    return client.post("/calculations", json={"a": a, "b": b, "type": type})


def test_add_returns_computed_result(client):
    response = add_calculation(client)
    assert response.status_code == 201
    assert response.json()["result"] == 5


def test_browse_returns_all_calculations(client):
    add_calculation(client)
    add_calculation(client, a=4, b=5, type="Multiply")
    response = client.get("/calculations")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_returns_one_calculation(client):
    created = add_calculation(client).json()
    response = client.get(f"/calculations/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_read_missing_calculation_returns_404(client):
    assert client.get("/calculations/999").status_code == 404


def test_edit_updates_and_recomputes(client):
    created = add_calculation(client).json()
    response = client.put(
        f"/calculations/{created['id']}", json={"a": 10, "b": 2, "type": "Divide"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_edit_missing_calculation_returns_404(client):
    response = client.put("/calculations/999", json={"a": 1, "b": 1, "type": "Add"})
    assert response.status_code == 404


def test_delete_removes_calculation(client):
    created = add_calculation(client).json()
    assert client.delete(f"/calculations/{created['id']}").status_code == 204
    assert client.get(f"/calculations/{created['id']}").status_code == 404


def test_add_rejects_zero_divisor(client):
    assert add_calculation(client, a=10, b=0, type="Divide").status_code == 422


def test_add_rejects_unknown_type(client):
    assert add_calculation(client, type="Banana").status_code == 422
