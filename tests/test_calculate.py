import pytest

from function import add_numbers
from conftest import two_positive_numbers, three_different_numbers, numbers_with_zero, sum_case

def test_sum_with_two_positive_numbers(two_positive_numbers):
    expected_result = 3
    actual_result = add_numbers(*two_positive_numbers)
    assert actual_result == expected_result

def test_sum_with_three_different_numbers(three_different_numbers):
    expected_result = 5
    actual_result = add_numbers(*three_different_numbers)
    assert actual_result == expected_result

def test_sum_with_zero(numbers_with_zero):
    expected_result = 6
    actual_result = add_numbers(*numbers_with_zero)
    assert actual_result == expected_result

def test_sum_cases(sum_case):
    numbers, expected = sum_case
    assert add_numbers(*numbers) == expected

@pytest.mark.parametrize("numbers, expected", [
    ((1, 2), 3),
    ((3, 4, -2), 5),
    ((1, 2, 0, 3), 6)
])
def test_sum(numbers, expected):
    assert add_numbers(*numbers) == expected