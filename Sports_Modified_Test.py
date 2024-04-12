#Unit Testing Assignment 5 Gx5452
import pytest
from Sports_Modifed import determinePercentColor, blackRectangle, draw_stat_text, set_default_values_for_player

@pytest.mark.parametrize("color_input, expected_color", [
    (20, 'RED'),     # Red for < 25
    (30, 'Orange'),  # Orange for < 50 && > 24
    (50, 'Yellow'),  # Yellow for < 75 && > 49
    (85, 'Green'),   # Green > 74
])
def test_determinePercentColor_valid(color_input, expected_color):
    assert determinePercentColor(color_input) == expected_color

@pytest.mark.parametrize("color_input_invalid, expected_color_invalid", [
    (20, 'Yellow'),  # Shouldnt be Yellow, it should be RED
    (30, 'Green'),   # Shouldnt be Green, it should be Orange
    (50, 'Red'),     # Shouldnt be Red, it should be Yellow
    (85, 'Orange'),  # Shouldnt be Orange, it should be Green
])
def test_determinePercentColor_invalid(color_input_invalid, expected_color_invalid):
    assert determinePercentColor(color_input_invalid) != expected_color_invalid


def test_blackRectangle_Valid():
    # Setting up sample run... so from 0,0 to 2,1 will be black.
    expected_pixels = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (2, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (1, 1, 0, 0, 0),
        (2, 1, 0, 0, 0),
    ]
    #Starting at point 0,0.. with a rectangle width of 3 and a height of 2
    #draw a black box.
    actual_pixels = blackRectangle(0, 0, 3, 2)

    assert actual_pixels == expected_pixels


test_blackRectangle_Valid()

def test_draw_stat_text_Valid():
    x_position = 10
    y_position = 20
    color = 'red'
    category = 'Points'
    value = 100
    expected_text = "Drawing 'Points: 100' at (x=10, y=20) in color red"
    result = draw_stat_text(x_position, y_position, color, category, value)

    assert result == expected_text



def test_set_default_values_for_player_valid():
    players = []
    set_default_values_for_player("Logan Smith", players)

    # Setting Expected Values
    expected_default_data = {
        "name": "Logan Smith",
        "team": "Data not available",
        "games_played": "00",
        "points": "0",
        "assists": "0",
        "rebounds": "0",
        "steals": "0",
        "field_goals_pct": "0%",
        "three_points_pct": "0%",
        "free_throws_pct": "0%"
    }
    assert players[0] == expected_default_data



