# test_database.py
import allure

from database import Database

class TestDatabase:

    @allure.title('available_buns возвращает 3 булочки с корректными данными')
    def test_available_buns(self):
        db = Database()
        buns = db.available_buns()
        allure.attach(
                name="Список булочек",
                body="\n".join(f"{b.get_name()} — {b.get_price()}" for b in buns),
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step('Проверить количество булочек в списке'):
            assert len(buns) == 3
        with allure.step('Проверить первую булочку -black bun - цена 100)'):
            assert buns[0].get_name() == "black bun"
            assert buns[0].get_price() == 100
        with allure.step('Проверить вторую булочку -white bun - цена 200)'):
            assert buns[1].get_name() == "white bun"
            assert buns[1].get_price() == 200
        with allure.step('Проверить третью булочку -red bun - цена 300)'):
            assert buns[2].get_name() == "red bun"
            assert buns[2].get_price() == 300

    @allure.title('available_ingredients возвращает 6 ингредиентов с корректными данными')
    def test_available_ingredients(self):
        db = Database()
        ingredients = db.available_ingredients()

        allure.attach(
                        name="Список ингридиентов",
                        body="\n".join(f"{b.get_type()} - {b.get_name()} — {b.get_price()}" for b in ingredients),
                        attachment_type=allure.attachment_type.TEXT
                    )

        with allure.step('Проверить количество ингридиентов -6'):

            assert len(ingredients) == 6

 #Соусы
        with allure.step('Проверить первый ингрид. соус - hot sauce - 100)'):
            assert ingredients[0].get_type() == "SAUCE"
            assert ingredients[0].get_name() == "hot sauce"
            assert ingredients[0].get_price() == 100

        with allure.step('Проверить первый ингрид.  соус - sour cream - 200)'):
            assert ingredients[1].get_name() == "sour cream"
            assert ingredients[1].get_price() == 200

        with allure.step('Проверить третий ингрид.  соус - chili sauce - 300)'):
            assert ingredients[2].get_name() == "chili sauce"
            assert ingredients[2].get_price() == 300

#Начинки
        with allure.step('Проверить четвертый ингрид.  начинка - cutlet - 100)'):
            assert ingredients[3].get_type() == "FILLING"
            assert ingredients[3].get_name() == "cutlet"
            assert ingredients[3].get_price() == 100

        with allure.step('Проверить пятый ингрид.  начинка - dinosaur - 200)'):
            assert ingredients[4].get_name() == "dinosaur"
            assert ingredients[4].get_price() == 200

        with allure.step('Проверить пятый ингрид.  начинка - sausage - 300)'):
            assert ingredients[5].get_name() == "sausage"
            assert ingredients[5].get_price() == 300
