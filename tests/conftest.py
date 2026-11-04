import pytest

# Отдельные фикстуры с разными случаями
@pytest.fixture
def two_positive_numbers():
    return (1, 2)

@pytest.fixture
def three_different_numbers():
    return (3, 4, -2)

@pytest.fixture
def numbers_with_zero():
    return (1, 2, 0, 3)

# Параметризированная фикстура - массив значений и результат сложения
@pytest.fixture(params=[
    ((1, 2), 3),
    ((3, 4, -2), 5),
    ((1, 2, 0, 3), 6),
], ids=["two_positive", "different_numbers", "with_zero"])
def sum_case(request):
    return request.param