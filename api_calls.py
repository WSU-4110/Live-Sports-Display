import http.client
import json
import datetime

api_key = '6musfbnhsy2dembz5cxzxade'
connection = http.client.HTTPSConnection("api.sportradar.us")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year



# Get the current schedule of games for today
def get_current_schedule():
    connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    if(response.status != 200):
        print("Error: ", response.status, response.reason)
        return None

    else:
        try:
            json_data = json.loads(data.decode("utf-8"))

            home_teams = []
            away_teams = []

            for game in json_data['games']:
                home_teams.append(game['home']['name'])
                away_teams.append(game['away']['name'])
                print(f"{game['home']['name']} vs {game['away']['name']}")

        return None
    except:
        print("No games today")

        return None



# Get the team ID from the team name
def get_team_id(team_name):
    connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    team_id = None

    try:
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the team id from param team_name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                team_id = game['home']['id']
            elif game['away']['name'] == team_name:
                team_id = game['away']['id']
    except:
        print("No games today")
    return team_id



# Get the team roster in format of player name, position, and jersey number
def get_team_roster_from_id(team_id):
    connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}//profile.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    try:
        json_data = json.loads(data.decode("utf-8"))

        for player in json_data['players']:
            print(f"{player['full_name']} / {player['position']} / {player['jersey_number']}")
    except:
        print("No players found")

    return None

def get_league_standings():
    connection.request("GET", f"/nba/trial/v8/en/seasons/2023/REG/standings.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    try:
        json_data = json.loads(data.decode("utf-8"))


        print("Western Conference\n")
        print("Southwest Division:")
        for team in json_data['conferences'][0]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")

        print("Pacific Division:")
        for team in json_data['conferences'][0]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")

        print("Northwest Division:")
        for team in json_data['conferences'][0]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")

        print("\n\n\nEastern Conference\n")
        print("Southeast Division:")
        for team in json_data['conferences'][1]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")
       
        print("Central Division:")
        for team in json_data['conferences'][1]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")

        print("Atlantic Division:")
        for team in json_data['conferences'][1]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} ||| Wins:{team['wins']} |||  Losses:{team['losses']}")
    except:
        print("No standings found")

    return None

def get_live_game_stats():
    connection.request("GET", f"/nba/trial/v8/en/games/20adc0dd-2579-445a-9f06-a5420b648645/summary.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    try:
        json_data = json.loads(data.decode("utf-8"))

        print(f"Home Team: {json_data['home']['market']} {json_data['home']['name']}\n")
        for player in json_data['home']['players']:
            if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} ||| Points:{player['statistics']['points']} ||| Assists:{player['statistics']['assists']} ||| Rebounds:{player['statistics']['rebounds']} ||| Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} ||| Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} ||| Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
       
        print(f"Away Team: {json_data['away']['market']} {json_data['away']['name']}\n")
        for player in json_data['away']['players']:
           if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} ||| Points:{player['statistics']['points']} ||| Assists:{player['statistics']['assists']} ||| Rebounds:{player['statistics']['rebounds']} ||| Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} ||| Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} ||| Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
        
    except:
            print("No game found")

    return None

# Beginning of calls to the API
get_live_game_stats()