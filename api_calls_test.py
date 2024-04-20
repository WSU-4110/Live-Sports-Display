from api_calls import SportsAPI
import time


def test_get_player_id_valid():
    api = SportsAPI()
    player_name ="Johnny Davis"
    player_id_expected = "51551f58-fc52-4403-abe5-4f5614804312"
    player_id = api.get_player_id(player_name)

    assert player_id == player_id_expected

def test_get_player_id_invalid():
    api = SportsAPI()
    player_name ="Johnny Davis"
    player_id_expected = "0afbe608-940a-4d5d-a1f7-468718c67d91"
    player_id = api.get_player_id(player_name)

    #This is lebron james Player Id 

    assert player_id != player_id_expected

