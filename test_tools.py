from unittest.mock import patch, MagicMock
from tools import get_weather


def test_get_weather_returns_formatted_string():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current_condition": [{
            "temp_F": "85",
            "weatherDesc": [{"value": "Sunny"}],
            "humidity": "45",
        }]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("tools.requests.get", return_value=mock_response):
        result = get_weather(city="Dallas")
        assert "Dallas" in result
        assert "85°F" in result
        assert "Sunny" in result


def test_get_weather_handles_api_error():
    with patch("tools.requests.get", side_effect=Exception("API down")):
        try:
            get_weather(city="Dallas")
            assert False, "Should have raised"
        except Exception as e:
            assert "API down" in str(e)
