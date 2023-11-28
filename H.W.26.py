import json
from typing import List, Dict
from dataclasses import dataclass
from cities import cities


@dataclass
class City:
    name: str
    subject: str
    population: int


transformed_cities = []

# Преобразование исходных данных в список экземпляров датакласса City
for city in cities:
    transformed_city = City(name=city["name"], subject=city["subject"], population=city["population"])
    transformed_cities.append(transformed_city)

# Сериализация списка экземпляров датакласса в JSON и запись в файл
with open('russian_cities.json', 'w', encoding='utf-8') as f:
    json.dump([city.__dict__ for city in transformed_cities], f, ensure_ascii=False, indent=4)
