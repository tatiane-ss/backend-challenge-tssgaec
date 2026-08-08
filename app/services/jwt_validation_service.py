import re
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

BASE64URL_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def _has_valid_compact_structure(token: str) -> bool:
    segments = token.split(".")

    if len(segments) != 3:
        return False

    return all(
        segment and BASE64URL_SEGMENT_PATTERN.fullmatch(segment) is not None
        for segment in segments
    )


def decode_jwt_payload(token: object) -> dict[str, Any] | None:
    if not isinstance(token, str):
        return None

    if not token.strip():
        return None

    if not _has_valid_compact_structure(token):
        return None

    try:
        decoded_token = jwt.decode_complete(
            token,
            options={"verify_signature": False},
        )
    except InvalidTokenError:
        return None

    header = decoded_token.get("header")
    payload = decoded_token.get("payload")

    if not isinstance(header, dict):
        return None

    if not isinstance(payload, dict):
        return None

    return payload
