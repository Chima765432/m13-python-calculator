def register_payload(username="alice", email="alice@example.com"):
    return {"username": username, "email": email, "password": "longenough1"}


def test_register_creates_user(client):
    response = client.post("/users/register", json=register_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_duplicate_email(client):
    client.post("/users/register", json=register_payload())
    response = client.post("/users/register", json=register_payload(username="bob"))
    assert response.status_code == 400


def test_register_rejects_invalid_email(client):
    payload = register_payload()
    payload["email"] = "not-an-email"
    assert client.post("/users/register", json=payload).status_code == 422


def test_login_succeeds_with_correct_password(client):
    client.post("/users/register", json=register_payload())
    response = client.post(
        "/users/login", json={"email": "alice@example.com", "password": "longenough1"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


def test_login_rejects_wrong_password(client):
    client.post("/users/register", json=register_payload())
    response = client.post(
        "/users/login", json={"email": "alice@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_register_returns_token(client):
    body = client.post("/users/register", json=register_payload()).json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_returns_token(client):
    client.post("/users/register", json=register_payload())
    body = client.post(
        "/users/login", json={"email": "alice@example.com", "password": "longenough1"}
    ).json()
    assert body["access_token"]
