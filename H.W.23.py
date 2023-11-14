import json
from typing import List


# Класс Product
class Product:
    def __init__(self, dimensions, weight, fragility, price, category, name):
        self.dimensions = dimensions
        self.weight = weight
        self.fragility = fragility
        self.price = price
        self.category = category
        self.name = name


# Класс PromoCodeData
class PromoCodeData:
    def __init__(self, code, discount):
        self.code = code
        self.discount = discount

    @staticmethod
    def load_from_json(json_path: str) -> List['PromoCodeData']:
        """
        Загружает данные о промо-кодах из JSON-файла и возвращает список объектов PromoCodeData.
        """
        promo_codes = []
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    promo_code = PromoCodeData(item['code'], item['discount'])
                    promo_codes.append(promo_code)
        except FileNotFoundError:
            pass
        return promo_codes


# Миксин PromoCodeMixin
class PromoCodeMixin:
    def apply_promo_code(self, product: Product, promo_code: str):
        """
        Применяет промо-код к стоимости продукта и корректирует его стоимость.
        """
        promo_codes = PromoCodeData.load_from_json('promo_codes.json')
        for code in promo_codes:
            if code.code == promo_code:
                discount = min(code.discount, 100) / 100  # Проверка на значение скидки
                product.price *= (1 - discount)
                break


# Класс Delivery
class Delivery:
    def __init__(self, delivery_speed):
        self.delivery_speed = delivery_speed

    def calculate_cost(self, product: Product):
        """
        Рассчитывает стоимость доставки для заданного продукта.
        """
        raise NotImplementedError("Метод calculate_cost должен быть переопределен в дочерних классах")


# Класс DeliveryServiceA
class DeliveryServiceA(Delivery):
    def __init__(self, delivery_speed):
        super().__init__(delivery_speed)

    def calculate_cost(self, product: Product):
        """
        Рассчитывает стоимость доставки для продукта в зависимости от его категории.
        """
        if product.category == 'Electronics':
            return product.price * 0.2
        elif product.category == 'Clothing':
            return product.price * 0.1
        else:
            return None


# Класс DeliveryServiceB
class DeliveryServiceB(Delivery):
    def __init__(self, delivery_speed):
        super().__init__(delivery_speed)

    def calculate_cost(self, product: Product):
        """
        Рассчитывает стоимость доставки для продукта в зависимости от его категории.
        """
        if product.category == 'Electronics':
            return product.price * 0.3
        elif product.category == 'Clothing':
            return product.price * 0.2
        else:
            return None



# Функция main
def main():
    # Создание объекта класса Product
    product = Product(dimensions=10, weight=5, fragility=False, price=100, category='Electronics', name='Phone')

    # Создание объектов доставки
    delivery_service_a = DeliveryServiceA(delivery_speed="Fast")
    delivery_service_b = DeliveryServiceB(delivery_speed="Standard")

    # Создание списка доступных вариантов доставки
    delivery_options = [delivery_service_a, delivery_service_b]

    # Применение промо-кода к стоимости доставки
    promo_mixin = PromoCodeMixin()
    promo_mixin.apply_promo_code(product, "SALE20")

    # Вывод информации о каждом варианте доставки
    for delivery in delivery_options:
        print("Скорость доставки:", delivery.delivery_speed)
        cost = delivery.calculate_cost(product)
        if cost is not None:
            print("Стоимость доставки:", cost)
        else:
            print("Ошибка: Не удалось рассчитать стоимость доставки для категории", product.category)
        print()


if __name__ == '__main__':
    main()
