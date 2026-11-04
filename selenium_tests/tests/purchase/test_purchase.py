from selenium.webdriver.support import expected_conditions as EC

def test_purchase(open_login_page, wait, locators, correct_credentials, checkout_order_info, base_url):
    # Открываем страницу авторизации и ждем когда она загрузится
    driver = open_login_page

    # Находим поля для ввода и вводим значения из заготовленной фикстуры
    driver.find_element(*locators["login_username_input"]).send_keys(correct_credentials["username"])
    driver.find_element(*locators["login_password_input"]).send_keys(correct_credentials["password"])
    driver.find_element(*locators["login_button"]).click()

    # Ждем когда загрузится страница с товарами
    cart_link = wait.until(EC.visibility_of_element_located(locators["cart_link"]))

    # Выбираем первый товар и добавляем его в корзину, и переходим в корзину
    driver.find_elements(*locators["add_to_cart_btn"])[0].click()
    cart_link.click()

    # Ждем пока загрузится корзина
    checkout_btn = wait.until(EC.visibility_of_element_located(locators["checkout_btn"]))

    # Переходим к оформлению
    checkout_btn.click()

    # Ждем когда загрузится форма с оформлением
    firstname = wait.until(EC.visibility_of_element_located(locators["checkout_firstname_input"]))

    # Находим поля для ввода и вводим значения из заготовленной фикстуры
    firstname.send_keys(checkout_order_info["firstname"])
    driver.find_element(*locators["checkout_lastname_input"]).send_keys(checkout_order_info["lastname"])
    driver.find_element(*locators["checkout_postalcode_input"]).send_keys(checkout_order_info["postalcode"])
    driver.find_element(*locators["checkout_continue_btn"]).click()

    # Ждем когда загрузится форма с завершением оформления
    finish_btn = wait.until(EC.visibility_of_element_located(locators["checkout_finish_btn"]))
    finish_btn.click()

    # Ждем появление сообщения и проверяем его
    complete_header = wait.until(EC.visibility_of_element_located(locators["checkout_complete_header"]))

    expectedMsg = "Thank you for your order!"
    
    assert expectedMsg in complete_header.text

    # Проверяем, что пользователь вернулся на страницу выбора товаров при нажатии на кнопку
    driver.find_element(*locators["checkout_back_to_products"]).click()
    wait.until(EC.url_changes)
    assert driver.current_url == base_url + "/inventory.html"