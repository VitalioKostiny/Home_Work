import pytest
from your_module import get_weather, CurrentWeather
from marshmallow import ValidationError

@pytest.fixture
def weather_request():
    return get_weather("Москва")

def test_weather_request_city_name(weather_request):
    assert weather_request['name'] == "Москва"

def test_weather_request_coord(weather_request):
    expected_lon = 37.6156
    expected_lat = 55.7522
    assert weather_request['coord']['lon'] == pytest.approx(expected_lon, abs=1e-4)
    assert weather_request['coord']['lat'] == pytest.approx(expected_lat, abs=1e-4)

def test_weather_request_weather_key(weather_request):
    assert all(key in weather_request['weather'][0] for key in ['id', 'main', 'description', 'icon'])

def test_weather_request_main_key(weather_request):
    assert all(key in weather_request['main'] for key in
               ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity'])

@pytest.mark.parametrize("city_name, expected_coords", [("Москва", (55.7522, 37.6156)), ("Лондон", (51.5074, -0.1278))])
@pytest.mark.slow
def test_weather_request_city_coodrd_name_parametrize_slow(weather_request, city_name, expected_coords):
    response = get_weather(city_name)
    assert response['name'] == city_name
    assert response['coord']['lon'] == pytest.approx(expected_coords[1], abs=1e-4)
    assert response['coord']['lat'] == pytest.approx(expected_coords[0], abs=1e-4)
