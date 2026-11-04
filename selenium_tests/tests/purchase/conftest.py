import pytest

@pytest.fixture
def checkout_order_info():
    return {"firstname": "Ivan", "lastname": "Ivanov", "postalcode": "123456"}