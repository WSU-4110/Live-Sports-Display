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

    try:
        json_data = json.loads(data.decode("utf-8"))

        # Add the home and away teams to their respective array, and print the scheudle
        home_teams = []
        away_teams = []
        for game in json_data['games']:
            home_teams.append(game['home']['name'])
            away_teams.append(game['away']['name'])
            print(f"{game['home']['name']} vs {game['away']['name']}")

        return None

    except json.JSONDecodeError as e:
        print("Something went wrong with the api")
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
    except json.JSONDecodeError as e:
        print("Something went wrong with the api")
    except:
        print("No games today")
    return team_id



# Get the team roster in format of player name, position, and jersey number
def get_team_roster_from_id(team_id):
    connection.request("GET", f"/nba/trial/v8/en/teams/583ecae2-fb46-11e1-82cb-f4ce4684ea4c/profile.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()

    try:
        json_data = json.loads(data.decode("utf-8"))
        
        for player in json_data['players']:
            print(f"{player['full_name']} / {player['position']} / {player['jersey_number']}")
    except json.JSONDecodeError as e:
        print("Something went wrong with the api")
    except:
        print("No players found")

    return None
    

# Begining of calls to the API
input_team = input("Enter a team name: ")
print(get_team_id(input_team))
