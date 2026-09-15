# test_bun.py
import pytest
import allure
from bun import Bun

@allure.feature('Bun')
class TestBun:

    @allure.title('Сохраняем name и price ')
    def test_init(self):
        with allure.step('Создать булкку(name="black bun", price=100)'):
            bun = Bun("black bun", 100)
        with allure.step('Проверить сохранение методами '):
            assert bun.name == "black bun", f"Ожидалось 'black bun', получено '{bun.name}'"
            assert bun.price == 100, f"Ожидалось 100, получено {bun.price}"

    @pytest.mark.parametrize('name, price', [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300),
    ])
    @allure.title('Корректные данные — {name} - {price}')
    def test_getters(self, name, price):
        bun = Bun(name, price)
        with allure.step("Проверить методы"):
            assert bun.get_name() == name, f"get_name() вернул '{bun.get_name()}', ожидалось '{name}'"
            assert bun.get_price() == price, f"get_price() вернул {bun.get_price()}, ожидалось {price}"


