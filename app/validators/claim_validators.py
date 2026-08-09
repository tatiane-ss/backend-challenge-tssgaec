from app.validators.prime_validator import is_prime

EXPECTED_CLAIMS = frozenset({"Name", "Role", "Seed"})
ALLOWED_ROLES = frozenset({"Admin", "Member", "External"})
MAX_NAME_LENGTH = 256


def has_exact_claims(payload: object) -> bool:
    if not isinstance(payload, dict):
        return False

    return set(payload.keys()) == EXPECTED_CLAIMS


def is_valid_name(name: object) -> bool:
    if not isinstance(name, str):
        return False

    if not name.strip():
        return False

    if len(name) > MAX_NAME_LENGTH:
        return False

    return not any(character.isdigit() for character in name)


def is_valid_role(role: object) -> bool:
    return isinstance(role, str) and role in ALLOWED_ROLES


def _parse_seed(seed: object) -> int | None:
    if isinstance(seed, bool):
        return None

    if isinstance(seed, int):
        return seed

    if isinstance(seed, str):
        if not seed or not seed.isascii() or not seed.isdigit():
            return None

        try:
            return int(seed)
        except ValueError:
            return None

    return None


def is_valid_seed(seed: object) -> bool:
    parsed_seed = _parse_seed(seed)

    if parsed_seed is None:
        return False

    return is_prime(parsed_seed)


def are_claims_valid(payload: object) -> bool:
    if not isinstance(payload, dict):
        return False

    if not has_exact_claims(payload):
        return False

    return (
        is_valid_name(payload["Name"])
        and is_valid_role(payload["Role"])
        and is_valid_seed(payload["Seed"])
    )
