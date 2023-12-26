import pytest
import requests
from your_module import get_weather, weather_data


@pytest.fixture
def weather_request_parametrize():
    def get_weather_data(city_name):
        # Ваш код для получения данных о погоде для заданного города
        return weather_data

    return get_weather_data


def test_weather_request_city_name(weather_request):
    weather_data, expected_city_name, _, _ = weather_request
    assert weather_data['name'] == expected_city_name


def test_weather_request_coord(weather_request):
    weather_data, _, expected_lon, expected_lat = weather_request
    assert weather_data['coord']['lon'] == expected_lon
    assert weather_data['coord']['lat'] == expected_lat


def test_weather_request_weather_key(weather_request):
    assert all(key in weather_request['weather'][0] for key in ['id', 'main', 'description', 'icon'])


def test_weather_request_main_key(weather_request):
    assert all(key in weather_request['main'] for key in
               ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity'])


@pytest.mark.parametrize("city_name, expected_coords", [("Moscow", (55.7558, 37.6176)), ("London", (51.5074, -0.1278))])
@pytest.mark.slow
def test_weather_request_city_coodrd_name_parametrize_slow(weather_request_parametrize, city_name, expected_coords):
    response = weather_request_parametrize(city_name)
    assert response['name'] == city_name
    assert response['coord']['lon'] == expected_coords[1]
    assert response['coord']['lat'] == expected_coords[0]
