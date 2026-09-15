import pytest
import allure

from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:

    @pytest.mark.parametrize('ingredient_type, name, price', [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_SAUCE, "chili sauce", 300),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
        (INGREDIENT_TYPE_FILLING, "sausage", 300),
    ])
    @allure.title('Ingredient сохраняет-тип-название-цена')
    def test_ingredient_init(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)

        input_data = (
            f"Type: {ingredient_type}\n"
            f"Name: {name}\n"
            f"Price: {price}"
        )
        allure.attach(
            name="Входные данные",
            body=input_data,
            attachment_type=allure.attachment_type.TEXT
        )
        with allure.step(f'Проверить type равен  ({ingredient_type})'): 
            assert ingredient.type == ingredient_type
        with allure.step(f'Проверить name равен ("{name}")'):
            assert ingredient.name == name
        with allure.step(f'Проверить price равен ({price})'):
            assert ingredient.price == price



    @pytest.mark.parametrize('ingredient_type, name, price', [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
    ])
    @allure.title('get_price возвращает цену: {price}')
    def test_get_price(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)

        input_data = (
            f"Type: {ingredient_type}\n"
            f"Name: {name}\n"
            f"Price: {price}"
        )
        allure.attach(
            name="Входные данные",
            body=input_data,
            attachment_type=allure.attachment_type.TEXT
        )
        with allure.step(f'get_price проверить - цена ({price})'):
            assert ingredient.get_price() == price

    @pytest.mark.parametrize('ingredient_type, name, price', [
        (INGREDIENT_TYPE_SAUCE, "chili sauce", 300),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
    ])
    @allure.title('get_name проверить - название: {name}')
    def test_get_name(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)
        with allure.step(f'get_name проверить - имя ({name})'):
            assert ingredient.get_name() == name



    @pytest.mark.parametrize('ingredient_type, name, price', [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
    ])
    @allure.title('get_type проверить - тип: {ingredient_type}')
    def test_get_type(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)
        with allure.step(f'get_type проверить - тип ({ingredient_type})'):
            assert ingredient.get_type() == ingredient_type
