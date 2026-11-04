from selenium.webdriver.support import expected_conditions as EC

def test_wrong_auth(open_login_page, wait, locators, wrong_credentials, base_url):
    # Открываем страницу авторизации и ждем когда она загрузится
    driver = open_login_page

    # Находим поля для ввода и вводим значения из заготовленной фикстуры
    driver.find_element(*locators["login_username_input"]).send_keys(wrong_credentials["username"])
    driver.find_element(*locators["login_password_input"]).send_keys(wrong_credentials["password"])
    driver.find_element(*locators["login_button"]).click()

    actualError = wait.until(EC.visibility_of_element_located(locators["login_error_message"]))

    # Сверяем ошибки авторизации
    assert wrong_credentials["error"] in actualError.text

    # Убеждаемся, что никуда не вошли
    assert driver.current_url == base_url + "/"