import json
from typing import List, Dict
from dataclasses import dataclass
from cities import cities


@dataclass
class City:
    name: str
    subject: str
    population: int

    @staticmethod
    def sort_cities_by_name(cities_list):
        return sorted(cities_list, key=lambda city: city.name)


class DataValidator:
    @staticmethod
    def remove_cities_with_bad_letters(cities_list):
        return [city for city in cities_list if not city.name.endswith(('ь', 'ъ'))]

    @staticmethod
    def validate_data_types(cities_list):
        for city in cities_list:
            city.name = city.name.capitalize()
            if not isinstance(city.name, str):
                raise TypeError("City name should be a string")
            if not isinstance(city.population, int):
                raise TypeError("Population should be a number")


transformed_cities = []

# Преобразование исходных данных в список экземпляров датакласса City
for city_data in cities:
    transformed_city = City(name=city_data["name"], subject=city_data["subject"], population=city_data["population"])
    transformed_cities.append(transformed_city)

# Удаление "плохих" городов
transformed_cities = DataValidator.remove_cities_with_bad_letters(transformed_cities)

# Валидация типов данных и преобразование названий городов
DataValidator.validate_data_types(transformed_cities)

# Сериализация списка экземпляров датакласса в JSON и запись в файл
with open('russian_cities.json', 'w', encoding='utf-8') as f:
    json.dump([city.__dict__ for city in transformed_cities], f, ensure_ascii=False, indent=4)
