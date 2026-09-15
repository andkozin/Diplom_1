import pytest
import allure
from unittest.mock import Mock

from burger import Burger
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


@allure.feature('Burger')
class TestBurger:

    #Создание без булки и без начинок

    @allure.title('При создании bun - пусто')
    def test_init_bun_is_no(self):
        burger = Burger()
        with allure.step('bun - пусто'):
            assert burger.bun is None

    @allure.title('При создании бургера ингридиенты — пустой список')
    def test_init_ingredients_is_list_no(self):
        burger = Burger()
        with allure.step('Ингриидиенты — пустой список'):
            assert burger.ingredients == []

        
    
    # Установить булку

    @allure.title('set_buns сохраняет булочку')
    def test_set_buns_sets_bun(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        with allure.step('Проверить булку'):
            assert burger.bun == mock_bun

    # Добавка ингридиента

    @allure.title('add_ingredient добавляет ингредиент в список')
    def test_add_ingredient_appends_to_list(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        with allure.step('Проверить длину списка 1'):
            assert len(burger.ingredients) == 1 # на одну позицию через длину
        with allure.step('Проверить элемент списка для 1'):
            assert burger.ingredients[0] == mock_ingredient # проверил индекс

    @allure.title('add_ingredient добавляет несколько ингредиентов по порядку')
    def test_add_multiple_ingredients(self):
        burger = Burger()
        mock_1, mock_2, mock_3 = Mock(), Mock(), Mock()
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)
        burger.add_ingredient(mock_3)
        with allure.step('Проверить длину списка 3'):
            assert len(burger.ingredients) == 3
        with allure.step('Проверить порядок списка'):
            assert burger.ingredients == [mock_1, mock_2, mock_3]

    #Удаление ингридиента

    @allure.title('remove_ingredient удаляет элемент по индексу')
    def test_remove_ingredient_removes_by_index(self):
        burger = Burger()
        mock_1, mock_2, mock_3 = Mock(), Mock(), Mock()
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)
        burger.add_ingredient(mock_3)
        burger.remove_ingredient(1)
        with allure.step('Проверить длину списка 2 после удаления'):
            assert len(burger.ingredients) == 2
        with allure.step('Проверить точно mock_2 '):
            assert mock_2 not in burger.ingredients
        with allure.step('Проверить порядок списка после удаления'):
            assert burger.ingredients == [mock_1, mock_3]

    #Перемещение ингридиента

    @allure.title('move_ingredient перемещает элемент по позициям')
    def test_move_ingredient_changes_position(self):
        burger = Burger()
        mock_1, mock_2, mock_3 = Mock(), Mock(), Mock()
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)
        burger.add_ingredient(mock_3)
        burger.move_ingredient(0, 2)
        with allure.step('Проверить порядок списка после перемещения'):
            assert burger.ingredients == [mock_2, mock_3, mock_1]

    #Расчет дважды булка верх и низ

    @allure.title('get_price считает цену булочки дважды (верх + низ)')
    def test_get_price_bun_only(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 200.0

        with allure.step('Установить булочку (цена 200) и рассчитать цену'):
            burger.set_buns(mock_bun)
        with allure.step('Проверить стоимость 400'):
            assert burger.get_price() == 400.0

    @allure.title('get_price сумма  булочки + ингредиенты')
    def test_get_price_bun_and_ingredients(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100.0
        mock_1 = Mock()
        mock_1.get_price.return_value = 50.0
        mock_2 = Mock()
        mock_2.get_price.return_value = 50.0

        with allure.step('Собрать - булка половинка (100) + 2 ингредиента (50 + 50)'):
            burger.set_buns(mock_bun)
            burger.add_ingredient(mock_1)
            burger.add_ingredient(mock_2)

        with allure.step('Проверить итого - 100*2 + 50 + 50 = 300'):
            assert burger.get_price() == 300

    @pytest.mark.parametrize('bun_price, ingredient_prices, expected', [
        (100, [], 200),
        (50, [30], 130),
        (50, [30, 40], 170),
        (0, [0], 0),
        (100, [10, 20, 30], 260),
    ])
    @allure.title('get_price: булочка={bun_price}, ингредиенты={ingredient_prices} → {expected}')
    def test_get_price_parametrized(self, bun_price, ingredient_prices, expected):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)

        with allure.step(f'Проверить итого - {bun_price}*2 + сумма({ingredient_prices}) = {expected}'):
            assert burger.get_price() == expected

    # --- get_receipt ---

    @allure.title('get_receipt формирует чек с булочкой и ценой')
    def test_get_receipt_format_bun_only(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200.0

        with allure.step('Создать бургер с одной булочкой (white bun, 200)'):
            burger.set_buns(mock_bun)

        with allure.step('Сформировать чек и проверить формат'):
            receipt = burger.get_receipt()
            allure.attach(
                            name=" Чек ",
                            body=receipt,
                            attachment_type=allure.attachment_type.TEXT
                            )
            assert "(==== white bun ====)" in receipt
            assert "Price: 400.0" in receipt

    @allure.title('get_receipt формирует чек с булочкой и ингредиентами')
    def test_get_receipt_format_with_ingredients(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 100.0

        mock_sauce = Mock()
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = "hot sauce"
        mock_sauce.get_price.return_value = 50.0

        mock_filling = Mock()
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = "cutlet"
        mock_filling.get_price.return_value = 75.0

        with allure.step('Собрать бургер: white bun + hot sauce + cutlet'):
            burger.set_buns(mock_bun)
            burger.add_ingredient(mock_sauce)
            burger.add_ingredient(mock_filling)

        with allure.step('Сформировать чек и проверить строки'):
            receipt = burger.get_receipt()
            allure.attach(
                name=" Чек ",
                body=receipt,
                attachment_type=allure.attachment_type.TEXT
                )
            with allure.step('Проверить наличие верхней булочки в чеке'):
                assert "(==== white bun ====)" in receipt
            with allure.step('Проверить наличие соуса в чеке'):
                assert "= sauce hot sauce =" in receipt
            with allure.step('Проверить наличие начинки в чеке'):
                assert "= filling cutlet =" in receipt
            with allure.step('Проверить наличие нижней булочки в чеке'):
                assert "(==== white bun ====)\n" in receipt
            with allure.step('Проверить итоговую цену в чеке'):
                assert "Price: 325.0" in receipt

    @allure.title('get_receipt выводит тип ингредиента в нижнем регистре')
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

        with allure.step('Чек с SAUCE в верхнем регистре'):
            receipt = burger.get_receipt()
            allure.attach(
                            name=" Чек ",
                            body=receipt,
                            attachment_type=allure.attachment_type.TEXT
                            )

        with allure.step('Проверить тип - нижный регистр'):
            assert "= sauce salsa =" in receipt
