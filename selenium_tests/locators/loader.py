"""Загрузчик локаторов из JSON-файла.

Локатор в JSON хранится в виде объекта с одним ключом — типом локатора.

Здесь он преобразуется в объект (By.ID, "login-button"), который
Selenium принимает напрямую:

    driver.find_element(*loader.get("saucedemo", "login_button"))
"""

import json
from pathlib import Path

from selenium.webdriver.common.by import By

# Сопоставление имени типа в JSON с классом By
_LOCATOR_TYPES = {
    "id": By.ID,
    "name": By.NAME,
    "class": By.CLASS_NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "tag": By.TAG_NAME,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
}

# каталог рядом с этим файлом: selenium_tests/locators/
_LOCATORS_DIR = Path(__file__).resolve().parent

_cache: dict[str, dict] = {}

def _load_page(page: str) -> dict:
    if page not in _cache:
        path = _LOCATORS_DIR / f"{page}.json"
        if not path.exists():
            raise FileNotFoundError(f"Файл локаторов не найден: {path}")
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        _cache[page] = {
            element: _to_locator(obj) for element, obj in raw.items()
        }
    return _cache[page]


def _to_locator(obj: dict) -> tuple:
    if len(obj) != 1:
        raise ValueError(f"Локатор должен иметь ровно один тип, получено: {obj}")
    (locator_type, value), = obj.items()
    if locator_type not in _LOCATOR_TYPES:
        raise ValueError(
            f"Неизвестный тип локатора '{locator_type}'. "
            f"Доступные: {', '.join(_LOCATOR_TYPES)}"
        )
    return _LOCATOR_TYPES[locator_type], value


def get(page: str, element: str) -> tuple:
    """Возвращает один локатор в виде (By, значение)."""
    locators = _load_page(page)
    if element not in locators:
        raise KeyError(f"Локатор '{element}' не найден в файле '{page}.json'")
    return locators[element]


def get_all(page: str) -> dict:
    """Возвращает все локаторы страницы"""
    return _load_page(page)
