#Unit Testing Assignment 5 Gx5452

def determinePercentColor(number):
    #used to determine player stats colors!
    if number < 25:
        return 'RED'
    elif number < 50:
        return 'Orange'
    elif number < 75:
        return 'Yellow'
    else:
        return 'Green'


def blackRectangle(xcord, ycord, rect_width, rect_height):
    # Setting up pixel Array
    pixels = []

    #Simulating Drawing
    for y in range(ycord, ycord + rect_height):
        for x in range(xcord, xcord + rect_width):
            pixels.append((x, y, 0, 0, 0))
            # Printing instead of Displaying to LED MATRIX
            print(f"Setting pixel at ({x}, {y}) to black (RGB: 0,0,0)")
        print()
    return pixels


def draw_stat_text(x_position, y_position, color, category, value):
    stat_text = f"{category}: {value}"
    # simulating Drawing a player (Category:Value) stat with X and Y cords
    drawing_action = f"Drawing '{stat_text}' at (x={x_position}, y={y_position}) in color {color}"
    return drawing_action

# This function simulates setting default values for a player's stats.
def set_default_values_for_player(player_name, updated_players):
    default_player_stats = { #Initualizing Player with Default Values
        "name": player_name,
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
    updated_players.append(default_player_stats)
    return updated_players


players_list = []
set_default_values_for_player("Logan Smith", players_list)
print(players_list)


