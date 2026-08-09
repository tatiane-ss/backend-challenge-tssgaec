import base64
import json

import pytest
from fastapi.testclient import TestClient

VALID_CASE_1_TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9."
    "QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
)

INVALID_CASE_2_TOKEN = (
    "eyJhbGciOiJzI1NiJ9."
    "dfsdfsfryJSr2xrIjoiQWRtaW4iLCJTZrkIjoiNzg0MSIsIk5hbrUiOiJUb25pbmhvIEFyYXVqbyJ9."
    "QY05fsdfsIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
)

INVALID_CASE_3_TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJSb2xlIjoiRXh0ZXJuYWwiLCJTZWVkIjoiODgwMzciLCJOYW1lIjoiTTRyaWEgT2xpdmlhIn0."
    "6YD73XWZYQSSMDf6H0i3-kylz1-TY_Yt6h1cV2Ku-Qs"
)

INVALID_CASE_4_TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJSb2xlIjoiTWVtYmVyIiwiT3JnIjoiQlIiLCJTZWVkIjoiMTQ2MjciLCJOYW1lIjoiVmFsZGlyIEFyYW5oYSJ9."
    "cmrXV_Flm5mfdpfNUVopY_I2zeJUy4EZ4i3Fea98zvY"
)

VALIDATION_ENDPOINT = "/api/v1/jwt/validate"


def _encode_base64url(value: object) -> str:
    json_bytes = json.dumps(
        value,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode("ascii")


def _build_test_token(payload: object) -> str:
    header_segment = _encode_base64url({"alg": "HS256"})
    payload_segment = _encode_base64url(payload)

    return f"{header_segment}.{payload_segment}.c2ln"


def test_official_valid_token_returns_true(client: TestClient) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": VALID_CASE_1_TOKEN},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": True}


@pytest.mark.parametrize(
    "token",
    [
        INVALID_CASE_2_TOKEN,
        "not-a-jwt",
        "abc.def",
        "abc..def",
    ],
)
def test_structurally_invalid_token_returns_false(
    client: TestClient,
    token: str,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": token},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_name_containing_number_returns_false(
    client: TestClient,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": INVALID_CASE_3_TOKEN},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_additional_claim_returns_false(
    client: TestClient,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": INVALID_CASE_4_TOKEN},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_missing_claim_returns_false(client: TestClient) -> None:
    token = _build_test_token(
        {
            "Name": "Maria Oliveira",
            "Role": "Admin",
        }
    )

    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": token},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_invalid_role_returns_false(client: TestClient) -> None:
    token = _build_test_token(
        {
            "Name": "Maria Oliveira",
            "Role": "Guest",
            "Seed": "7",
        }
    )

    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": token},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_non_prime_seed_returns_false(client: TestClient) -> None:
    token = _build_test_token(
        {
            "Name": "Maria Oliveira",
            "Role": "Member",
            "Seed": "10",
        }
    )

    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": token},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_empty_token_returns_false(client: TestClient) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": ""},
    )

    assert response.status_code == 200
    assert response.json() == {"valid": False}


def test_missing_body_returns_422(client: TestClient) -> None:
    response = client.post(VALIDATION_ENDPOINT)

    assert response.status_code == 422


def test_missing_token_field_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "token",
    [
        None,
        123,
        True,
        [],
        {},
    ],
)
def test_invalid_token_type_returns_422(
    client: TestClient,
    token: object,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={"token": token},
    )

    assert response.status_code == 422


def test_additional_request_field_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json={
            "token": VALID_CASE_1_TOKEN,
            "other": "unexpected",
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("request_body", "expected_status"),
    [
        ({"token": ""}, 200),
        ({"token": "invalid"}, 200),
        ({"token": "abc.def"}, 200),
        ({"token": INVALID_CASE_2_TOKEN}, 200),
        ({"token": INVALID_CASE_3_TOKEN}, 200),
        ({"token": INVALID_CASE_4_TOKEN}, 200),
        ({}, 422),
        ({"token": None}, 422),
        ({"token": 123}, 422),
    ],
)
def test_invalid_inputs_never_return_500(
    client: TestClient,
    request_body: dict[str, object],
    expected_status: int,
) -> None:
    response = client.post(
        VALIDATION_ENDPOINT,
        json=request_body,
    )

    assert response.status_code == expected_status
    assert response.status_code != 500
