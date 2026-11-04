import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_tests.locators.loader import get_all

@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com"

@pytest.fixture(scope="session")
def locators():
    return get_all("saucedemo")

@pytest.fixture
def driver():
    # Создаем драйвер на базе Chrome.
    # pytest должен сам вызвать quit после теста
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

@pytest.fixture
def open_login_page(base_url, driver, wait, locators):
    """Открывает сайт и ждёт появления формы логина."""
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(locators["login_username_input"]))
    return driver