import requests
import json
from dataclasses import dataclass, field
from typing import Optional
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow_dataclass import class_schema
from marshmallow_jsonschema import JSONSchema
from pprint import pprint

def get_weather(city_name):
    api_key = '23496c2a58b99648af590ee8a29c5348'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'lang': 'ru',
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Выбираем город который захочется:)
city_name_input = input('Введите желаемый город: ')

# Создаем датакласс с обязательными и не обязательными полями из API
@dataclass
class CurrentWeather:
    city_name: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    pressure: int
    visibility: Optional[int] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None

# Создание схемы на основе датакласса
WeatherSchema = class_schema(CurrentWeather)

# Создание схемы на основе датакласса, и расширение ее, мы добавили дополнительные
# проверки для температуры, влажности, скорости ветра, атмосферного давления и видимости.
# Кроме того, мы добавили описания для каждого поля в метаданных с помощью metadata,
# чтобы было понятно, что именно проверяется.
class ExtendedWeatherSchema(WeatherSchema):
    temperature = fields.Float(
        required=True,
        validate=[validate.Range(min=-100, max=100)],
        metadata={'description': 'Температура в градусах Цельсия'}
    )
    humidity = fields.Int(
        required=True,
        validate=[validate.Range(min=0, max=100)],
        metadata={'description': 'Влажность воздуха в процентах'}
    )
    wind_speed = fields.Float(
        required=True,
        validate=[validate.Range(min=0)],
        metadata={'description': 'Скорость ветра в м/с'}
    )
    pressure = fields.Int(
        required=True,
        validate=[validate.Range(min=0)],
        metadata={'description': 'Атмосферное давление в гПа'}
    )
    visibility = fields.Int(
        allow_none=True,
        validate=[validate.Range(min=0)],
        metadata={'description': 'Видимость в метрах'}
    )
    sunrise = fields.Int(
        allow_none=True,
        metadata={'description': 'Время восхода солнца в UNIX-формате'}
    )
    sunset = fields.Int(
        allow_none=True,
        metadata={'description': 'Время заката солнца в UNIX-формате'}
    )

# Используем библиотеку marshmallow_jsonschema для преобразования
# схемы Marshmallow в JSONSchema
json_schema = JSONSchema().dump(ExtendedWeatherSchema())

# Сохранение JSON схемы в файл
with open("weather_file.json", "w", encoding="utf-8") as file:
    json.dump(json_schema, file, indent=4, ensure_ascii=False)

# Получаем данные о погоде
weather_data = get_weather(city_name_input)

# Создаем объект CurrentWeather из ответа API
current_weather = CurrentWeather(
    city_name=weather_data['name'],
    temperature=weather_data['main']['temp'],
    description=weather_data['weather'][0]['description'],
    humidity=weather_data['main']['humidity'],
    wind_speed=weather_data['wind']['speed'],
    pressure=weather_data['main']['pressure'],
    visibility=weather_data.get('visibility'),
    sunrise=weather_data.get('sys', {}).get('sunrise'),
    sunset=weather_data.get('sys', {}).get('sunset')
)


json_data = ExtendedWeatherSchema().dump(current_weather)

try:
    validated_data = ExtendedWeatherSchema().load(json_data)
    print(validated_data)
except ValidationError as e:
    print(f'Ошибка валидации данных: {e.messages}')





