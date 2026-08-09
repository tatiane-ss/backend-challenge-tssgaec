import pytest

from app.validators.claim_validators import (
    are_claims_valid,
    has_exact_claims,
    is_valid_name,
    is_valid_role,
    is_valid_seed,
)


@pytest.mark.parametrize(
    "name",
    [
        "Maria",
        "Maria Oliveira",
        "João",
        "Ana-Clara",
        "D'Ávila",
        "A" * 256,
    ],
)
def test_valid_names(name: str) -> None:
    assert is_valid_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "M4ria",
        "",
        "   ",
        "A" * 257,
        123,
        None,
    ],
)
def test_invalid_names(name: object) -> None:
    assert is_valid_name(name) is False


@pytest.mark.parametrize(
    "role",
    [
        "Admin",
        "Member",
        "External",
    ],
)
def test_valid_roles(role: str) -> None:
    assert is_valid_role(role) is True


@pytest.mark.parametrize(
    "role",
    [
        "Guest",
        "admin",
        "Admin ",
        " Admin",
        "",
        None,
        123,
    ],
)
def test_invalid_roles(role: object) -> None:
    assert is_valid_role(role) is False


@pytest.mark.parametrize(
    "seed",
    [
        2,
        7,
        "7",
        "0007",
        7841,
        "7841",
        88037,
        "88037",
    ],
)
def test_valid_seeds(seed: object) -> None:
    assert is_valid_seed(seed) is True


@pytest.mark.parametrize(
    "seed",
    [
        10,
        "10",
        0,
        1,
        -7,
        7.0,
        "7.0",
        "sete",
        "",
        " 7 ",
        True,
        False,
        None,
    ],
)
def test_invalid_seeds(seed: object) -> None:
    assert is_valid_seed(seed) is False


def test_payload_with_exact_claims_is_valid() -> None:
    payload = {
        "Role": "Admin",
        "Seed": "7841",
        "Name": "Toninho Araujo",
    }

    assert has_exact_claims(payload) is True


def test_payload_with_missing_claim_is_invalid() -> None:
    payload = {
        "Name": "Maria",
        "Role": "Admin",
    }

    assert has_exact_claims(payload) is False


def test_payload_with_additional_claim_is_invalid() -> None:
    payload = {
        "Name": "Valdir Aranha",
        "Role": "Member",
        "Seed": "14627",
        "Org": "BR",
    }

    assert has_exact_claims(payload) is False


def test_claim_names_are_case_sensitive() -> None:
    payload = {
        "name": "Maria",
        "Role": "Admin",
        "Seed": "7",
    }

    assert has_exact_claims(payload) is False


def test_non_dict_payload_does_not_have_exact_claims() -> None:
    payload = ["Maria", "Admin", "7"]

    assert has_exact_claims(payload) is False


def test_complete_valid_payload_is_valid() -> None:
    payload = {
        "Name": "Toninho Araujo",
        "Role": "Admin",
        "Seed": "7841",
    }

    assert are_claims_valid(payload) is True


def test_payload_with_invalid_name_is_invalid() -> None:
    payload = {
        "Name": "M4ria Olivia",
        "Role": "External",
        "Seed": "88037",
    }

    assert are_claims_valid(payload) is False


def test_payload_with_invalid_role_is_invalid() -> None:
    payload = {
        "Name": "Maria Oliveira",
        "Role": "Guest",
        "Seed": "7",
    }

    assert are_claims_valid(payload) is False


def test_payload_with_non_prime_seed_is_invalid() -> None:
    payload = {
        "Name": "Maria Oliveira",
        "Role": "Member",
        "Seed": "10",
    }

    assert are_claims_valid(payload) is False


def test_non_dict_payload_is_invalid() -> None:
    assert are_claims_valid([]) is False
