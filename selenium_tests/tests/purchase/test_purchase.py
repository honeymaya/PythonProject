from selenium.webdriver.support import expected_conditions as EC

import allure

@allure.parent_suite("Проверка saucedemo")
@allure.suite("Покупка")
@allure.tag("ui")
@allure.label("component", "checkout")
class TestPurchase:

    @allure.step("Авторизоваться под корректным пользователем")
    def login_step(self, open_login_page, correct_credentials):
        self.driver = open_login_page
        self.driver.find_element(*self.locators["login_username_input"]).send_keys(correct_credentials["username"])
        self.driver.find_element(*self.locators["login_password_input"]).send_keys(correct_credentials["password"])
        self.driver.find_element(*self.locators["login_button"]).click()

    @allure.step("Добавить первый товар в корзину и перейти в корзину")
    def add_item_and_open_cart_step(self, wait):
        cart_link = wait.until(EC.visibility_of_element_located(self.locators["cart_link"]))
        self.driver.find_elements(*self.locators["add_to_cart_btn"])[0].click()
        cart_link.click()

    @allure.step("Начать оформление заказа")
    def start_checkout_step(self, wait):
        checkout_btn = wait.until(EC.visibility_of_element_located(self.locators["checkout_btn"]))
        checkout_btn.click()

    @allure.step("Заполнить форму заказа: firstname={firstname}, lastname={lastname}, postal={postalcode}")
    def fill_order_info_step(self, wait, firstname, lastname, postalcode):
        wait.until(EC.visibility_of_element_located(self.locators["checkout_firstname_input"]))
        self.driver.find_element(*self.locators["checkout_firstname_input"]).send_keys(firstname)
        self.driver.find_element(*self.locators["checkout_lastname_input"]).send_keys(lastname)
        self.driver.find_element(*self.locators["checkout_postalcode_input"]).send_keys(postalcode)
        self.driver.find_element(*self.locators["checkout_continue_btn"]).click()

    @allure.step("Завершить оформление")
    def finish_purchase_step(self, wait):
        finish_btn = wait.until(EC.visibility_of_element_located(self.locators["checkout_finish_btn"]))
        finish_btn.click()

    @allure.step("Проверить заголовок успешного оформления")
    def check_complete_header_step(self, wait):
        complete_header = wait.until(EC.visibility_of_element_located(self.locators["checkout_complete_header"]))
        expectedMsg = "Thank you for your order!"
        assert expectedMsg in complete_header.text, \
                "Сообщение об успешном оформлении заказа отличается от ожидаемого"

    @allure.step("Вернуться на страницу каталога после покупки")
    def return_to_products_step(self, base_url, wait):
        self.driver.find_element(*self.locators["checkout_back_to_products"]).click()
        wait.until(EC.url_changes)
        assert self.driver.current_url == base_url + "/inventory.html", \
                "Пользователь должен был вернуться на страницу выбора товаров при нажатии на кнопку"

    @allure.title("Успешная покупка")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_purchase(self, open_login_page, wait, locators, correct_credentials, checkout_order_info, base_url):
        self.locators = locators
        self.login_step(open_login_page, correct_credentials)
        self.add_item_and_open_cart_step(wait)
        self.start_checkout_step(wait)
        self.fill_order_info_step(wait, checkout_order_info["firstname"], checkout_order_info["lastname"], checkout_order_info["postalcode"])
        self.finish_purchase_step(wait)
        self.check_complete_header_step(wait)
        self.return_to_products_step(base_url, wait)