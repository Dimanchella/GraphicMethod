SYSTEM_ACCURACY = 6
OUTPUT_ACCURACY = 2


def validate_values():
    error_codes = []
    return error_codes


def add_positive_restrictions(
        rests_a: list[list[float]], rests_b: list[float], rests_s: list[bool]
):
    return rests_a + [
        [0] * i + [1] + [0] * (len(rests_a[0]) - i - 1)
        for i in range(len(rests_a[0]))
    ], rests_b + [0] * len(rests_a[0]), rests_s + [True] * len(rests_a[0])
