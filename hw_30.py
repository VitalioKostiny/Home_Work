import pytest
from hw_28 import *


# Фикстура для предопределенного города (Москва)
@pytest.fixture(scope="module")
def weather_request():
    return "Москва"


# Фикстура для "чистого" экземпляра для параметризации
@pytest.fixture(scope="module")
def weather_request_parametrize():
    return None  # В этом случае вы можете предоставить список городов для параметризации


cities = [
    ('Москва', {"lon": 37.6156, "lat": 55.7522}),
    ('Воронеж', {"lon": 39.17, "lat": 51.6664}),
    ('Санкт-Петербург', {"lon": 30.2642, "lat": 59.8944}),
    ('Краснодар', {"lon": 38.9769, "lat": 45.0328}),
    ('Сочи', {"lon": 39.7303, "lat": 43.6}),
]


# Тест1
def test_weather_request_city_name(weather_request):
    # Получаем данные о погоде для Москвы
    weather_data = get_weather(weather_request)

    # Проверяем, что поле name соответствует ожидаемому значению
    assert weather_data['name'] == weather_request


# Тест 2 - проверяем что {"coord": {"lon": 37.6156, "lat": 55.7522} в ответе
def test_weather_request_coord(weather_request):
    # Получаем данные о погоде для Москвы
    weather_data = get_weather(weather_request)

    # Ожидаемые координаты для Москвы
    expected_coordinates = {"lon": 37.6156, "lat": 55.7522}

    # Проверяем, что координаты соответствуют ожидаемым значениям
    assert weather_data['coord'] == expected_coordinates


# Тест 3 - проверяем то, что в "weather" есть ключи id, main, description, icon
def test_weather_request_weather_key(weather_request):
    # Получаем данные о погоде для Москвы
    weather_data = get_weather(weather_request)

    # Ожидаемые ключи в секции weather
    expected_keys = ['id', 'main', 'description', 'icon']

    # Проверяем, что ключи присутствуют в секции weather
    assert all(key in weather_data['weather'][0] for key in expected_keys)


# Тест 4 - проверяем то, что в "main" есть ключи temp, feels_like, temp_min, temp_max, pressure, humidity
def test_weather_request_main_key(weather_request):
    # Получаем данные о погоде для Москвы
    weather_data = get_weather(weather_request)

    # Ожидаемые ключи в секции main
    expected_keys = ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity']

    # Проверяем, что ключи присутствуют в секции main
    assert all(key in weather_data['main'] for key in expected_keys)


# Тест 5 - Параметризованный и маркированный тест для проверки названия города
@pytest.mark.parametrize("city_name, expected_coords", cities)
@pytest.mark.slow
def test_weather_request_city_coodrd_name_parametrize_slow(weather_request_parametrize, city_name, expected_coords):
    # Получаем данные о погоде для указанного города
    weather_data = get_weather(city_name)

    # Проверяем, что имя и координаты соответствуют ожидаемым значениям
    assert weather_data['name'] == city_name
    assert weather_data['coord'] == expected_coords
