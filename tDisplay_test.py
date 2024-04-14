import pytest
from Unit_Testing_Functions import testDisplay
from mock_rpi_ws281x import Color

@pytest.fixture
def char_map():
    return {
        'A': [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1]
        ],
        ' ': [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    }

@pytest.fixture
def strip(mocker):
    mock_strip = mocker.MagicMock()
    return mock_strip

@pytest.fixture
def mock_get_led_index(mocker):
    return mocker.patch('Unit_Testing_Functions.getLedIndex', side_effect=lambda x, y, height=8: x + y * height)

@pytest.fixture
def mock_sleep(mocker):
    return mocker.patch('Unit_Testing_Functions.time.sleep')

def test_display_character(strip, mock_get_led_index, mock_sleep, char_map):
    char = 'A'
    for y in range(5):
        for x in range(5):
            led_index = mock_get_led_index(x, y)
            is_on = char_map[char][y][x] == 1
            expected_color = Color(255, 0, 0) if is_on else Color(0, 0, 0)
            strip.setPixelColor.assert_any_call(led_index, expected_color)
    assert strip.setPixelColor.call_count == 25 
    strip.show.assert_called_once()
    mock_sleep.assert_called_once_with(1)
