import pytest
import allure
from unittest.mock import Mock

from burger import Burger
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


@allure.feature('Burger')
class TestBurger:

    @allure.title('bun при создании — None')
    def test_init_bun_is_none(self):
        burger = Burger()
        assert burger.bun is None, "bun должен быть None после создания"
        

    @allure.title('ingredients при создании — пустой список')
    def test_init_ingredients_is_empty_list(self):
        burger = Burger()
        assert burger.ingredients == [], "ingredients должен быть пустым списком"

    @allure.title('set_buns сохраняет булочку')
    def test_set_buns_sets_bun(self):
        burger = Burger()
        mock_bun = Mock()
        with allure.step('Вызвать set_buns'):
            burger.set_buns(mock_bun)
        assert burger.bun == mock_bun, "set_buns должен сохранить булочку"

    @allure.title('add_ingredient увеличивает длину списка на 1')
    def test_add_ingredient_increases_length(self):
        burger = Burger()
        mock_ingredient = Mock()
        with allure.step('Добавить ингредиент'):
            burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1, "Длина списка должна стать 1"

    @allure.title('add_ingredient добавляет элемент в конец')
    def test_add_ingredient_adds_to_end(self):
        burger = Burger()
        mock_ingredient = Mock()
        with allure.step('Добавить ингредиент'):
            burger.add_ingredient(mock_ingredient)
        assert burger.ingredients[0] == mock_ingredient, "Элемент должен быть на позиции 0"

    @allure.title('add_ingredient собирает ингредиенты и сохраняет порядок')
    def test_add_multiple_ingredients_preserves_order(self):
        burger = Burger()
        m1, m2, m3 = Mock(), Mock(), Mock()
        with allure.step('Добавить 3 ингрид. подряд'):
            burger.add_ingredient(m1)
            burger.add_ingredient(m2)
            burger.add_ingredient(m3)
        assert burger.ingredients == [m1, m2, m3], "Список должен соответ. порядку добав."

    @allure.title('remove_ingredient уменьшает длину списка')
    def test_remove_ingredient_decreases_length(self):
        burger = Burger()
        m1, m2, m3 = Mock(), Mock(), Mock()
        burger.add_ingredient(m1)
        burger.add_ingredient(m2)
        burger.add_ingredient(m3)
        with allure.step('Удалить ингредиент по индексу 1'):
            burger.remove_ingredient(1)
        assert len(burger.ingredients) == 2, "Длина должна стать 2"

    @allure.title('remove_ingredient удаляет 2й элемент')
    def test_remove_ingredient_removes_element(self):
        burger = Burger()
        m1, m2, m3 = Mock(), Mock(), Mock()
        burger.add_ingredient(m1)
        burger.add_ingredient(m2)
        burger.add_ingredient(m3)
        with allure.step('Удалить элемент по индексу 2'):
            burger.remove_ingredient(2)
        assert m3 not in burger.ingredients, "Элемент не должен быть в списке"

    @allure.title('remove_ingredient перемещает элементы')
    def test_remove_ingredient_shifts_elements(self):
        burger = Burger()
        m1, m2, m3 = Mock(), Mock(), Mock()
        burger.add_ingredient(m1)
        burger.add_ingredient(m2)
        burger.add_ingredient(m3)
        with allure.step('Удалить по индексу 1'):
            burger.remove_ingredient(1)
        assert burger.ingredients == [m1, m3], "Порядок должен быть [m1, m3]"

    @allure.title('move_ingredient меняет список элементов')
    def test_move_ingredient_changes_position(self):
        burger = Burger()
        m1, m2, m3 = Mock(), Mock(), Mock()
        burger.add_ingredient(m1)
        burger.add_ingredient(m2)
        burger.add_ingredient(m3)
        with allure.step('Переместить с 0 на 2'):
            burger.move_ingredient(0, 2)
        assert burger.ingredients == [m2, m3, m1], "Порядок должен стать [m2, m3, m1]"

    @allure.title('get_price учитывает булочку дважды')
    def test_get_price_bun_counted_twice(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 200.0
        with allure.step('Установить булочку и рассчитать цену'):
            burger.set_buns(mock_bun)
        assert burger.get_price() == 400.0, "Цена должна быть 400 (200 * 2)"

    @allure.title('get_price суммирует булочку и ингредиенты')
    def test_get_price_sums_bun_and_ingredients(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100.0
        m1 = Mock(); m1.get_price.return_value = 50.0
        m2 = Mock(); m2.get_price.return_value = 50.0
        with allure.step('Собрать бургер'):
            burger.set_buns(mock_bun)
            burger.add_ingredient(m1)
            burger.add_ingredient(m2)
        assert burger.get_price() == 300, "Итоговая цена должна быть 300"

    @pytest.mark.parametrize('bun_price, ingredient_prices, expected', [
        (100, [], 200),
        (50, [30], 130),
        (50, [30, 40], 170),
        (0, [0], 0),
        (100, [10, 20, 30], 260),
    ])
    @allure.title('get_price: булочка={bun_price}, ингредиенты={ingredient_prices} - {expected}')
    def test_get_price_parametrized(self, bun_price, ingredient_prices, expected):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)
        assert burger.get_price() == expected, f"Ждем цену- {expected}"

    @allure.title('Чек содержит строку булочки')
    def test_get_receipt_contains_top_bun_line(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200.0
        burger.set_buns(mock_bun)
        with allure.step('Сформировать чек'):
            receipt = burger.get_receipt()
        allure.attach(name="Чек", body=receipt, attachment_type=allure.attachment_type.TEXT)
        assert "(==== white bun ====)" in receipt, "Чек должен содержать строку булочки"

    @allure.title('Чек содержит булку дважды (верх + низ)')
    def test_get_receipt_contains_bottom_bun_line(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200.0
        burger.set_buns(mock_bun)
        with allure.step('Сформировать чек'):
            receipt = burger.get_receipt()
        allure.attach(name="Чек", body=receipt, attachment_type=allure.attachment_type.TEXT)
        assert receipt.count("(==== white bun ====)") == 2, "Чек должен содержать булку дважды"

    @allure.title('Чек: соус в правильном формате')
    def test_get_receipt_format_sauce(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 100.0
        mock_sauce = Mock()
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = "hot sauce"
        mock_sauce.get_price.return_value = 50.0
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        with allure.step('Сформировать чек с соусом'):
            receipt = burger.get_receipt()
        allure.attach(name="Чек", body=receipt, attachment_type=allure.attachment_type.TEXT)
        assert "= sauce hot sauce =" in receipt, "Соус должен быть в формате '= sauce <name> ='"

    @allure.title('Чек: начинка в правильном формате')
    def test_get_receipt_format_filling(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 100.0
        mock_filling = Mock()
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = "cutlet"
        mock_filling.get_price.return_value = 75.0
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_filling)
        with allure.step('Сформировать чек с начинкой'):
            receipt = burger.get_receipt()
        allure.attach(name="Чек", body=receipt, attachment_type=allure.attachment_type.TEXT)
        assert "= filling cutlet =" in receipt, "Начинка должна быть в формате '= filling <name> ='"

    @allure.title('Чек: тип ингредиента в нижнем регистре')
    def test_get_receipt_type_lowercased(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "bun"
        mock_bun.get_price.return_value = 0
        burger.set_buns(mock_bun)
        mock_ingr = Mock()
        mock_ingr.get_type.return_value = "SAUCE"
        mock_ingr.get_name.return_value = "salsa"
        mock_ingr.get_price.return_value = 0
        burger.add_ingredient(mock_ingr)
        with allure.step('Сформировать чек с типом SAUCE в верхнем регистре'):
            receipt = burger.get_receipt()
        allure.attach(name="Чек", body=receipt, attachment_type=allure.attachment_type.TEXT)
        assert "= sauce salsa =" in receipt, "Тип ингредиента должен быть в нижнем регистре"

