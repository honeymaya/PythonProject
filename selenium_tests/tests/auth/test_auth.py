import allure

from selenium.webdriver.support import expected_conditions as EC

@allure.parent_suite("Проверка saucedemo")
@allure.suite("Авторизация")
@allure.tag("ui")
@allure.label("component", "login")
class TestAuth:

    @allure.step("Открыть страницу логина и дождаться формы ввода")
    def open_login_page_step(self, open_login_page):
        self.driver = open_login_page

    @allure.step("Ввести неверные учётные данные: username={username}, password={password}")
    def enter_wrong_credentials_step(self, username, password):
        self.driver.find_element(*self.locators["login_username_input"]).send_keys(username)
        self.driver.find_element(*self.locators["login_password_input"]).send_keys(password)

    @allure.step("Нажать кнопку Войти")
    def click_login_button_step(self):
        self.driver.find_element(*self.locators["login_button"]).click()

    @allure.step("Проверить появление сообщения об ошибке")
    def check_error_message_step(self, wait, expected_error):
        actual_error = wait.until(
            EC.visibility_of_element_located(self.locators["login_error_message"])
        )
        assert expected_error in actual_error.text, (
            "Ожидалась другая ошибка входа!"
        )

    @allure.step("Убедиться, что пользователь не вошёл (URL не изменился)")
    def check_not_logged_in_step(self, base_url):
        assert self.driver.current_url == base_url + "/", (
            "URL адрес был изменен после неудачной авторизации по неизвестной причине!"
        )

    @allure.title("Неуспешная авторизация")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_auth(self, open_login_page, wait, locators, wrong_credentials, base_url):
        self.locators = locators
        self.open_login_page_step(open_login_page)
        self.enter_wrong_credentials_step(
            wrong_credentials["username"], wrong_credentials["password"]
        )
        self.click_login_button_step()
        self.check_error_message_step(wait, wrong_credentials["error"])
        self.check_not_logged_in_step(base_url)