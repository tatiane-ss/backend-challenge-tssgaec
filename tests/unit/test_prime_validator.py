import pytest

from app.validators.prime_validator import is_prime


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (2, True),
        (3, True),
        (7, True),
        (7841, True),
        (88037, True),
        (4, False),
        (9, False),
        (10, False),
        (0, False),
        (1, False),
        (-7, False),
        (True, False),
        (7.0, False),
        ("7", False),
        (None, False),
    ],
)
def test_is_prime(number: object, expected: bool) -> None:
    assert is_prime(number) is expected
