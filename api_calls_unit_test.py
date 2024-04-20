from api_calls import SportsAPI
import time

def test_get_game_id_valid():
    api = SportsAPI()
    team_name = "Detroit Pistons"
    year = "2024"
    month = "02"
    day = "04"
    game_id_expected = "e11a3105-52aa-414e-ac77-471eb4c62f87"

    game_id = api.get_game_id(team_name,year,month,day)

    assert game_id == game_id_expected


def test_get_game_id_invalid():
    api = SportsAPI()
    team_name = "Los Angeles Lakers"
    year = "2024"
    month = "01"
    day = "28"

    game_id = api.get_game_id(team_name, year, month, day)    

    assert game_id is None

def test_get_team_id_valid():
    api = SportsAPI()
    team_name = "Chicago Bulls"
    team_id_expected = "583ec5fd-fb46-11e1-82cb-f4ce4684ea4c"

    team_id = api.get_team_id(team_name)

    assert team_id == team_id_expected

def test_get_team_id_invalid():
    api = SportsAPI()
    team_name = "Chicago Pistons"

    team_id = api.get_team_id(team_name)

    assert team_id is None

def test_get_player_stats_valid():
    
    api = SportsAPI()
    player_name = "LeBron James"
    year = "2024"
    month = "01"
    day = "29"

    points_expected = 23

    player_stats = api.get_player_stats(player_name, year, month, day)

    points = player_stats[0].points
    time.sleep(1)

    assert points == points_expected

def test_get_player_stats_invalid():
    time.sleep(2)
    api = SportsAPI()
    player_name = "LeBron James"
    year = "2024"
    month = "01"
    day = "30"

    points_expected = 23

    player_stats = api.get_player_stats(player_name, year, month, day)

    points = player_stats[0].points

    assert points != points_expected




