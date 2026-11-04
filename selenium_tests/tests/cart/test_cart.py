from selenium.webdriver.support import expected_conditions as EC

import allure

@allure.parent_suite("Проверка saucedemo")
@allure.suite("Корзина")
@allure.tag("ui")
@allure.label("component", "cart")
class TestCart:

    @allure.step("Авторизоваться на сайте с валидными учетными данными")
    def login_step(self, open_login_page, correct_credentials):
        self.driver = open_login_page
        self.driver.find_element(*self.locators["login_username_input"]).send_keys(correct_credentials["username"])
        self.driver.find_element(*self.locators["login_password_input"]).send_keys(correct_credentials["password"])
        self.driver.find_element(*self.locators["login_button"]).click()

    @allure.step("Добавить несколько товаров в корзину и перейти в корзину")
    def add_items_and_open_cart_step(self, wait):
        cart_link = wait.until(EC.visibility_of_element_located(self.locators["cart_link"]))
        self.driver.find_elements(*self.locators["add_to_cart_btn"])[0].click()
        self.driver.find_elements(*self.locators["add_to_cart_btn"])[1].click()
        cart_link.click()

    @allure.step("Удалить все товары из корзины")
    def remove_all_items_step(self, wait):
        wait.until(EC.visibility_of_element_located(self.locators["checkout_btn"]))
        buttons = self.driver.find_elements(*self.locators["cart_remove_btn"])
        for btn in buttons:
            btn.click()

    @allure.step("Проверить, что корзина пуста (значок счетчика корзины исчез)")
    def check_cart_empty_step(self, wait):
        wait.until(EC.invisibility_of_element_located(self.locators["cart_badge"]), 
                    "Значок корзины не должен отображаться, когда корзина пуста, но он отображается")
        assert self.driver.find_elements(*self.locators["cart_badge"]) == [], \
            "Значок корзины не должен отображаться, когда корзина пуста, но он отображается"

    @allure.step("Возвращаемся на страницу каталога")
    def continue_shopping_step(self, base_url, wait):
        self.driver.find_element(*self.locators["cart_continue_shopping"]).click()
        wait.until(EC.url_changes)
        assert self.driver.current_url == base_url + "/inventory.html",\
            "Пользователь должен был вернуться на страницу выбора товаров при нажатии на кнопку"

    @allure.title("Очищение корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_clean_cart(self, open_login_page, wait, locators, correct_credentials, base_url):
        self.locators = locators
        self.login_step(open_login_page, correct_credentials)
        self.add_items_and_open_cart_step(wait)
        self.remove_all_items_step(wait)
        self.check_cart_empty_step(wait)
        self.continue_shopping_step(base_url, wait)