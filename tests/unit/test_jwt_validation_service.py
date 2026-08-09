import base64
import json

import pytest

from app.services.jwt_validation_service import (
    decode_jwt_payload,
    validate_jwt,
)

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


def _encode_base64url(value: object) -> str:
    json_bytes = json.dumps(
        value,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode("ascii")


def _encode_raw_base64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _build_test_token(header: object, payload: object) -> str:
    header_segment = _encode_base64url(header)
    payload_segment = _encode_base64url(payload)

    return f"{header_segment}.{payload_segment}.c2ln"


def test_decode_valid_jwt_returns_payload() -> None:
    payload = decode_jwt_payload(VALID_CASE_1_TOKEN)

    assert payload == {
        "Role": "Admin",
        "Seed": "7841",
        "Name": "Toninho Araujo",
    }


@pytest.mark.parametrize(
    "token",
    [
        None,
        123,
        True,
        "",
        "   ",
        "abc",
        "abc.def",
        "abc.def.ghi.jkl",
        "abc..def",
        ".abc.def",
        "abc.def.",
        "abc.d$f.ghi",
    ],
)
def test_invalid_inputs_do_not_return_payload(token: object) -> None:
    assert decode_jwt_payload(token) is None


def test_invalid_header_json_returns_none() -> None:
    invalid_header = _encode_raw_base64url(b"not-json")
    valid_payload = _encode_base64url(
        {
            "Name": "Maria",
            "Role": "Admin",
            "Seed": "7",
        }
    )

    token = f"{invalid_header}.{valid_payload}.c2ln"

    assert decode_jwt_payload(token) is None


def test_invalid_payload_json_returns_none() -> None:
    valid_header = _encode_base64url({"alg": "HS256"})
    invalid_payload = _encode_raw_base64url(b"not-json")

    token = f"{valid_header}.{invalid_payload}.c2ln"

    assert decode_jwt_payload(token) is None


def test_payload_that_is_not_json_object_returns_none() -> None:
    token = _build_test_token(
        header={"alg": "HS256"},
        payload=["Maria", "Admin", "7"],
    )

    assert decode_jwt_payload(token) is None


def test_official_case_1_is_valid() -> None:
    assert validate_jwt(VALID_CASE_1_TOKEN) is True


def test_official_case_2_is_invalid() -> None:
    assert validate_jwt(INVALID_CASE_2_TOKEN) is False


def test_official_case_3_is_invalid() -> None:
    assert validate_jwt(INVALID_CASE_3_TOKEN) is False


def test_official_case_4_is_invalid() -> None:
    assert validate_jwt(INVALID_CASE_4_TOKEN) is False
