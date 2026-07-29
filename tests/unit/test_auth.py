import pytest

from app.auth import create_access_token, decode_access_token


def test_token_round_trips_subject():
    token = create_access_token("alice@example.com")
    assert decode_access_token(token)["sub"] == "alice@example.com"


def test_token_carries_expiry():
    assert "exp" in decode_access_token(create_access_token("alice@example.com"))


def test_tampered_token_is_rejected():
    import jwt

    token = create_access_token("alice@example.com")
    with pytest.raises(jwt.PyJWTError):
        decode_access_token(token + "tampered")
