import requests
import json
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_dataclass import class_schema
from dataclasses import dataclass
from typing import Optional
from marshmallow_jsonschema import JSONSchema
from babel.dates import format_datetime
from datetime import datetime


def get_weather(city_name):
    """
    Получает данные о погоде для указанного города с помощью API.

    Args:
    city_name (str): Название города.

    Returns:
    dict: Данные о погоде в формате JSON.
    """
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


@dataclass
class CurrentWeather:
    """
    Датакласс для хранения данных о текущей погоде.
    """
    city_name: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    pressure: int
    visibility: Optional[int] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


WeatherSchema = class_schema(CurrentWeather)


class ExtendedWeatherSchema(WeatherSchema):
    """
    Расширенная схема.
    """
    temperature = fields.Float(
        required=True,
        validate=validate.Range(min=-100, max=100),
        metadata={'description': 'Температура в градусах Цельсия'}
    )
    humidity = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=100),
        metadata={'description': 'Влажность воздуха в процентах'}
    )
    wind_speed = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={'description': 'Скорость ветра в м/с'}
    )
    pressure = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        metadata={'description': 'Атмосферное давление в гПа'}
    )
    visibility = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0),
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


json_schema = JSONSchema().dump(ExtendedWeatherSchema())

with open("weather_file.json", "w", encoding="utf-8") as file:
    json.dump(json_schema, file, indent=4, ensure_ascii=False)

city_name_input = input('Введите город для ознакомления с погодой: ')
weather_data = get_weather(city_name_input)

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
    print('МЫ НАШЛИ ДЛЯ ВАС ДАННЫЕ !')
except ValidationError as e:
    print(f'Ошибка валидации данных: {e.messages}')
sunrise_time = format_datetime(datetime.fromtimestamp(current_weather.sunrise), format='short', locale='ru')
sunset_time = format_datetime(datetime.fromtimestamp(current_weather.sunset), format='short', locale='ru')

print(f"Город: {current_weather.city_name}")
print(f"Температура: {current_weather.temperature}°C")
print(f"Описание: {current_weather.description}")
print(f"Влажность: {current_weather.humidity}%")
print(f"Скорость ветра: {current_weather.wind_speed} м/с")
print(f"Атмосферное давление: {current_weather.pressure} гПа")
print(f"Видимость: {current_weather.visibility} м")
print(f"Время восхода солнца: {sunrise_time}")
print(f"Время заката солнца: {sunset_time}")




