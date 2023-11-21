from typing import Any


class CustomMeta(type):
    """
    Метакласс, который добавляет дополнительное поле и метод в классы, использующие этот метакласс.
    """

    def __new__(cls, name: str, bases: Any, dct: dict) -> type:
        dct['extra_field'] = 'Значение по умолчанию'

        def extra_method(self) -> None:
            """
            Дополнительный метод, который выводит сообщение.
            """
            print("Это дополнительный метод")

        dct['extra_method'] = extra_method
        return super().__new__(cls, name, bases, dct)


class MyClass(metaclass=CustomMeta):
    """
    Класс, использующий метакласс CustomMeta.
    """
    extra_field: str = 'Значение по умолчанию'  # Явное объявление атрибута


class MySubClass(MyClass):
    """
    Подкласс класса MyClass.
    """

    def extra_method(self) -> None:
        """
        Переопределенный дополнительный метод.
        """
        pass


# Тестирование
obj1 = MyClass()
obj2 = MySubClass()

print(obj1.extra_field)  # Значение по умолчанию
obj2.extra_method()  # Это дополнительный метод

print('Проверка принадлежности объектов к различным классам:')
print(isinstance(obj1, MyClass))  # True, так как obj1 создан с использованием MyClass
print(isinstance(obj1, MySubClass))  # False, так как MyClass не является подклассом MySubClass
print(isinstance(obj2, MyClass))  # True, так как obj2 создан с использованием MySubClass, к-й яв-ся подклассом MyClass
print(isinstance(obj2, MySubClass))  # True, так как obj2 создан с использованием MySubClass

