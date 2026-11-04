import pytest

@pytest.fixture
def wrong_credentials():
    return {"username": "abc", 
            "password": "123", 
            "error": "Epic sadface: Username and password do not match any user in this service"}