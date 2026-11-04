from selenium.webdriver.support import expected_conditions as EC

def test_clean_cart(open_login_page, wait, locators, correct_credentials, base_url):
    # Открываем страницу авторизации и ждем когда она загрузится
    driver = open_login_page

    # Находим поля для ввода и вводим значения из заготовленной фикстуры
    driver.find_element(*locators["login_username_input"]).send_keys(correct_credentials["username"])
    driver.find_element(*locators["login_password_input"]).send_keys(correct_credentials["password"])
    driver.find_element(*locators["login_button"]).click()

    # Ждем когда загрузится страница с товарами
    cart_link = wait.until(EC.visibility_of_element_located(locators["cart_link"]))

    # Выбираем первый и второй товар и добавляем его в корзину, и переходим в корзину
    driver.find_elements(*locators["add_to_cart_btn"])[0].click()
    driver.find_elements(*locators["add_to_cart_btn"])[1].click()
    cart_link.click()

    # Ждем пока загрузится корзина
    wait.until(EC.visibility_of_element_located(locators["checkout_btn"]))

    # Нажимаем все кнопки удаления из корзины
    buttons = driver.find_elements(*locators["cart_remove_btn"])
    for btn in buttons:
        btn.click()

    # Проверяем наличие счетчика корзины
    wait.until(EC.invisibility_of_element_located(locators["cart_badge"]), 
               "Значок корзины не должен отображаться, когда корзина пуста, но он отображается")
        

    # Значок корзины не должен отображаться, когда корзина пуста
    assert driver.find_elements(*locators["cart_badge"]) == [], \
        "Значок корзины не должен отображаться, когда корзина пуста, но он отображается"

    # Проверяем, что пользователь вернулся на страницу выбора товаров при нажатии на кнопку
    driver.find_element(*locators["cart_continue_shopping"]).click()
    wait.until(EC.url_changes)
    assert driver.current_url == base_url + "/inventory.html", \
        "Пользователь должен был вернуться на страницу выбора товаров при нажатии на кнопку"