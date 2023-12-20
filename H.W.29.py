from abc import ABC, abstractmethod

class IngredientFactory(ABC):
    @abstractmethod
    def create_cheese(self, cheese_type: str) -> str:
        """
        Создает объект сыра на основе выбранного типа.
        """

    @abstractmethod
    def create_sauce(self, sauce_type: str) -> str:
        """
        Создает объект соуса на основе выбранного типа.
        """

    @abstractmethod
    def create_topping(self, topping_type: str) -> str:
        """
        Создает объект дополнительного топпинга на основе выбранного типа.
        """


class DodoIngredientFactory(IngredientFactory):
    def create_cheese(self, cheese_type: str) -> str:
        if cheese_type == "Моцарелла":
            return "Моцарелла"
        elif cheese_type == "Чеддер":
            return "Чеддер"
        else:
            return "Неизвестный сыр"

    def create_sauce(self, sauce_type: str) -> str:
        if sauce_type == "Томатный":
            return "Томатный соус"
        elif sauce_type == "Песто":
            return "Песто соус"
        elif sauce_type == "Белый":
            return "Белый соус"
        else:
            return "Мы не знаем такой соус, но что-нибудь слепучим"

    def create_topping(self, topping_type: str) -> str:
        if topping_type == "Грибы":
            return "Грибы"
        elif topping_type == "Пепперони":
            return "Пепперони"
        elif topping_type == "Ветчина":
            return "Ветчина"
        else:
            return "Зря не взяли топинг, они сегодня чрезвычайно хорош !"


class PizzaBuilder:
    def __init__(self, ingredient_factory: IngredientFactory, pizza_type: str):
        self.ingredient_factory = ingredient_factory
        self.pizza_type = pizza_type

    def build(self, size: str, cheese_type: str, sauce_type: str, topping_type: str) -> str:
        cheese = self.ingredient_factory.create_cheese(cheese_type)
        sauce = self.ingredient_factory.create_sauce(sauce_type)
        topping = self.ingredient_factory.create_topping(topping_type)
        return f"Тип пиццы: {self.pizza_type}, Размер: {size}, Сыр: {cheese}, Соус: {sauce}, Топпинг: {topping}"


def main():
    dodo_ingredient_factory = DodoIngredientFactory()
    pizza_type = input("Введите тип пиццы (Маргарита, Пепперони, Гавайская, Вегетарианская, Витальянская): ")
    size = input("Введите размер пиццы: ")
    cheese_type = input("Выберите сыр (Моцарелла, Чеддер): ")
    sauce_type = input("Выберите соус (Томатный, Песто, Белый): ")
    topping_type = input("Выберите дополнительный топпинг (Грибы, Пепперони, Ветчина) или нажмите 0 для пропуска: ")
    pizza_builder = PizzaBuilder(dodo_ingredient_factory, pizza_type)
    pizza = pizza_builder.build(size, cheese_type, sauce_type, topping_type)
    print("Ваш заказ пиццы:")
    print(pizza)


main()
