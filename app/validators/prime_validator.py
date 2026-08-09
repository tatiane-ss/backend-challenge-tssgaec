def is_prime(number: object) -> bool:
    if isinstance(number, bool) or not isinstance(number, int):
        return False

    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False

        divisor += 2

    return True
