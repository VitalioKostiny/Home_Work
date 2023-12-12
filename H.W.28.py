import json
import requests
import pprint
from dataclasses import dataclass
from typing import Optional, List
from marshmallow import Schema, fields, validate
from marshmallow_jsonschema import JSONSchema


def get_weather(city_name: str) -> Optional[dict]:
    """
    Получает данные о погоде для указанного города.

    Args:
    city_name: Название города.

    Returns:
    dict: Данные о погоде в формате JSON.
    """
    api_key = "748a58c619d858a68d8f4441207ea03c"  # Мой API ключ
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'lang': 'ru',
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@dataclass
class CurrentWeather:
    """
    Класс для хранения данных о текущей погоде.
    """
    city_name: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    weather_description: str
    wind_speed: float
    wind_direction: int
    sunrise: int
    sunset: int
    snow: Optional[float]
    rain: Optional[float]
    visibility: int
    timezone: int
    coordinates: dict


class CurrentWeatherSchema(Schema):
    """
    Схема для валидации и сериализации данных о текущей погоде.
    """
    city_name = fields.Str(required=True)
    country = fields.Str(required=True)
    temperature = fields.Float(required=True)
    feels_like = fields.Float(required=True)
    humidity = fields.Int(required=True, validate=validate.Range(min=0, max=100))
    pressure = fields.Int(required=True, validate=validate.Range(min=800, max=1200))
    weather_description = fields.Str(required=True)
    wind_speed = fields.Float(required=True, validate=validate.Range(min=0))
    wind_direction = fields.Int(required=True, validate=validate.Range(min=0, max=360))
    sunrise = fields.Int(required=True)
    sunset = fields.Int(required=True)
    snow = fields.Float()
    rain = fields.Float()
    visibility = fields.Int(required=True, validate=validate.Range(min=0))
    timezone = fields.Int(required=True)
    coordinates = fields.Dict(required=True)


if __name__ == "__main__":
    city = input("Введите, в каком городе хотите узнать погоду: ")
    weather_data = get_weather(city)
    if weather_data:
        pprint.pprint(weather_data)
        current_weather_schema = CurrentWeatherSchema()
        json_schema = JSONSchema().dump(current_weather_schema)
        with open('current_weather_schema.json', 'w') as file:
            json.dump(json_schema, file, indent=4)
    else:
        print("Не удалось получить данные о погоде для указанного города.")

