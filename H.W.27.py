from dataclasses import dataclass, field
from cities import cities
import json
from typing import *
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError

MSG_USER_INPUT = 'Для завершения игры введите "Стоп". Введите название города:  '
MSG_FILE_CITY_NAME = "cities_comp.json"
MSG_COMPUTER_FIND_CITY = 'Компуктер ищет слово на букву: '
MSG_COMPUTER_RESPONSE = 'Компуктер назвал город: '
MSG_USER_CITY = 'Назовите слово на букву: '
MSG_PRINT_STOP = 'Вы остановили игру. Вы проиграли.'
MSG_WRONG_CITY = 'Вы ввели город, которого нет ! Вы проиграли бездушной машине.'
MSG_CITY_IS_MISSING = 'Такого города нет. Вы проиграли.'
MSG_CITY_NOT_FOUND = 'Компьютер не нашел города на указанную букву. Компуктер проиграл.'


class DataValidator:
    """
    Класс DataValidator валидации данных для записи в файл json
    """

    def __init__(self):
        """
        Конструктор класса
        """

    @staticmethod
    def validate_data(data) -> list[dict[str, Any]]:
        schema = {
            "type": "object",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "population": {"type": "integer"},
                    "subject": {"type": "string"}
                },
                "required": ["name", "population", "subject"],
                "additionalProperties": False
            }
        }

        cities_valid = []
        for item in data:
            cities_valid_temp = {}
            try:
                validate(item, schema)  # Проверка соответствия данных схеме
                cities_valid_temp['subject'] = item['subject']
                cities_valid_temp['name'] = item['name']
                cities_valid_temp['population'] = item['population']
                cities_valid.append(cities_valid_temp)
            except ValidationError as e:
                print(f"Validation error: {e.message}")
                # Обработка исключения при валидации
                # Можно добавить логирование ошибок или другую обработку
        return cities_valid


class JsonFileHandler:
    """
    Класс JsonFileHandler для записи и чтения валидных данных в файл json
    """

    def __init__(self, filepath: Any, data: Any = None, as_dict: Any = None) -> None:
        """
        Описание атрибутов класса JsonFileHandler:
        :param filepath: атрибут адреса файла json
        :param data: атрибут адреса/переменных данных для записи в файл json
        :param as_dict: атрибут записи/чтения данных в/из файла json (см. методы ниже)
        :return: None
        """
        self.filepath = filepath
        self.data = data
        self.as_dict = as_dict

    def write_file(self):
        """
        Метод экземпляра записи данных в файл json в зависимости от атрибута as_dict
        :return: None
        """
        if self.as_dict:
            with open(self.filepath, "w") as f:  # запись списка словарей
                json.dump(self.data, f)
        else:
            json_object1 = json.dumps(self.data, indent=4)  # запись списка списков
            with open(self.filepath, 'w') as f:
                f.write(json_object1)

    def read_file(self):
        """
        Метод экземпляра чтения данных из файла json в зависимости от атрибута as_dict
        :return: данные файла
        """
        if self.as_dict:
            with open(self.filepath, 'r') as f:
                json_read_temp = f.read()
                json_read = json.loads(json_read_temp)
                return json_read

        else:
            with open(self.filepath, 'r') as f:
                json_read = json.load(f)
                return json_read


@dataclass
class City:
    """
    Класс City. Используется для формирования объекта датакласса. Атрибут bad_letter - первая и последняя буква города
    """
    subject: str
    name: str
    population: int
    bad_letter: list = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """
        Метод записи вычисляемых свойств (не инициализируемый атрибут) в датакласс. Для списка "плохих букв"
        """
        self.bad_letter.append(self.name[0].lower())
        self.bad_letter.append(self.name[-1].lower())


class CityGame:
    """
    Класс CityGame - алгоритм игры и определения победителя. Удаление города из списка проходит здесь
    """

    def __init__(self, cities):
        self.cities1: Any = cities

    def human_turn(self) -> str:
        """
        Алгоритм хода "человека". Определение первой буквы для машины. Удаление города из списка при его использовании.
        Определение победителя.
        """
        user_input = input(MSG_USER_INPUT).capitalize()
        if user_input == 'Стоп':
            print(MSG_PRINT_STOP)
            return 'game_over'
        for temp in self.cities1:
            if user_input in temp.name:
                self.cities1.remove(temp)
                break
        else:
            print(MSG_CITY_IS_MISSING)
            return 'game_over'
        if user_input[-1] in game.bad_letters_set3:
            user_letter = user_input[-2]
            if user_letter in game.bad_letters_set3:
                user_letter = city_temp.name[-3]
            print(f'{MSG_COMPUTER_FIND_CITY} {user_letter.capitalize()}')
            return user_letter
        else:
            user_letter = user_input[-1]
            print(f'{MSG_COMPUTER_FIND_CITY} {user_letter.capitalize()}')
            return user_letter

    def computer_turn(self, user_letter) -> str:
        """
        Описание хода "компьютера". Определение первой буквы для человека. Удаление города при его использовании.
        Определение победителя
        """
        for city_temp in self.cities1:
            if user_letter.capitalize() == city_temp.name[0]:
                if city_temp.name[-1] in game.bad_letters_set3:
                    city_letter_temp = city_temp.name[-2]
                    if city_letter_temp in game.bad_letters_set3:
                        city_letter_temp = city_temp.name[-3]
                else:
                    city_letter_temp = city_temp.name[-1]
                print(f'{MSG_COMPUTER_RESPONSE} {city_temp.name}. {MSG_USER_CITY} {city_letter_temp.capitalize()}')
                self.cities1.remove(city_temp)
                break
        else:
            print(MSG_CITY_NOT_FOUND)
            return 'game_over'


class GameManager:
    """
    Класс GameManager - класс управления игрой. Переключает хода человека и машины. Определение победителя.
    """

    def __init__(self, game) -> None:
        # self.json_read_False = json_read_False
        # self.cities = cities
        self.game = game

    def __call__(self, *args, **kwargs) -> None:
        while True:
            c1 = game.human_turn()
            if c1 == 'game_over':
                break
            user_letter: str = c1
            c2 = game.computer_turn(user_letter)
            if c2 == 'game_over':
                break


if __name__ == '__main__':
    valid_data_json = DataValidator.validate_data(cities)
    write_json_file = JsonFileHandler('city_valid.json', valid_data_json, as_dict=True)
    write_json_file.write_file()
    read_json_file = JsonFileHandler('city_valid.json', valid_data_json, as_dict=True)
    valid_data = read_json_file.read_file()
    city_valid = []
    for temp in range(len(valid_data)):
        city_valid.append(City(subject=valid_data[temp]['subject'],
                               name=valid_data[temp]['name'],
                               population=valid_data[temp]['population']))
    city_valid_sort = sorted(city_valid, key=lambda x: x.name)  # сортировка списка объектов по названию города
    first_letters_set = set()
    for temp1 in city_valid_sort:
        first_letters_set.add(temp1.bad_letter[0])
    last_letters_set = set()
    for temp2 in city_valid_sort:
        last_letters_set.add((temp2.bad_letter[1]))
    bad_last_letters_set: set = last_letters_set - first_letters_set  # set "плохих" букв для использования в игре
    bad_last_letters_set.add('й')
    game = CityGame(city_valid_sort)
    game.bad_letters_set3 = bad_last_letters_set
    game_manager = GameManager(game)
    game_manager()
