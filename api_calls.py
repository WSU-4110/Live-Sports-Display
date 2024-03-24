import http.client
import json
import datetime
import time

api_key = '6musfbnhsy2dembz5cxzxade'
connection = http.client.HTTPSConnection("api.sportradar.us")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year

class schedule:
    
    __file_path = "gameSchedule.txt"

    # Constructor
    def __init__(self):
        self.api_key = api_key
        self.connection = http.client.HTTPSConnection("api.sportradar.us")
        
    # creates the file
    def __make_file(self):

# Get the game ID from the team name for the current day
def get_game_id(team_name) -> int:
    game_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/15/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the game id the team name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                game_id = game['id']
            elif game['away']['name'] == team_name:
                game_id = game['id']

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return game_id

        # if the file does not exist, create it
        if not(os.path.isfile(self.__file_path)):
            add = open(self.__file_path, "w")
            add.close()
        

        return None


    def __input_data(self):
        #Sets up the file with year at the top
        self.__make_file()
        add = open(self.__file_path, "a")

        try:
            #connect to sports API, collects data
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year-1}/REG/schedule.json?api_key={self.api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
                
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))
                
            if not json_data.get('games'):
                raise Exception("No games!")
            
        
            #decodes

            json_data = json.loads(data.decode("utf-8"))

            #prints sets of times and teams for the games
            for game in json_data['games']:
                print(game['scheduled'])
                add.write(game['scheduled'] + "\n")
                add.write(game['home']['name']+ " vs " + game['away']['name'] + "\n")
                
                
            print("all games printed")

        #error handling
        except json.JSONDecodeError as e:
            print(f"Something went wrong with the api: {e}")

        return None
    
    def check(self):
        #if info is out of date, replace
            #self.__input_data()

        #create output list for games
        #go through text doc (while loop)
            #if year month day time smaller, continue
            #elif year month day time equal, collect game in output
            #elif year month day time larger, exit loop

        
        #return output list  

## Facade Pattern for the API calls
class SportsAPI:
    ## Constructor for the class
    def __init__(self):
        self.api_key = api_key
        self.connection = http.client.HTTPSConnection("api.sportradar.us")

    def get_game_id(self, team_name, year, month, day) -> int:
        game_id = None

        try:
            ## Request to API for the game id
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={self.api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # Loop through the games and find the game id the team name
            for game in json_data['games']:
                if game['home']['name'] == team_name:
                    game_id = game['id']
                elif game['away']['name'] == team_name:
                    game_id = game['id']

        ## Catching exceptions
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return game_id
    

    def get_team_id(self, team_name) -> int:
        team_id = None

        try:
            ## Request to API for the team id
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={self.api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # Loop through the games and find the team id from param team_name
            for game in json_data['games']:
                if game['home']['name'] == team_name:
                    team_id = game['home']['id']
                elif game['away']['name'] == team_name:
                    team_id = game['away']['id']

        ## Catching exceptions
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return team_id

    def get_current_schedule(self,year,month,day) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))
            
            if not json_data.get('games'):
                raise Exception("No games today!")
            else:

                home_teams = []
                away_teams = []

                print("Today's Schedule:\n")

                for game in json_data['games']:
                    home_teams.append(game['home']['name'])
                    away_teams.append(game['away']['name'])
                    print(f"{game['home']['name']} vs {game['away']['name']}")

        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None


def get_game_id_from_date(team_name, year, month, day) -> int:
    game_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the game id the team name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                game_id = game['id']
            elif game['away']['name'] == team_name:
                game_id = game['id']

        return game_id

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



# Get the team ID from the team name
def get_team_id(team_name) -> int:
    team_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the team id from param team_name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                team_id = game['home']['id']
            elif game['away']['name'] == team_name:
                team_id = game['away']['id']

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return team_id
    # Get the team roster in format of player name, position, and jersey number
    def get_team_roster_from_id(self,team_id) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}//profile.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            for player in json_data['players']:
                print(f"{player['full_name']} / {player['position']} / {player['jersey_number']}")

        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None



    def get_league_standings(self) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/seasons/2023/REG/standings.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # Print the standings for the Western and Eastern Conference
            print("Western Conference\n")
            print("Southwest Division:")
            for team in json_data['conferences'][0]['divisions'][0]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
            print("Pacific Division:")
            for team in json_data['conferences'][0]['divisions'][1]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
            print("Northwest Division:")
            for team in json_data['conferences'][0]['divisions'][2]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

            print("\n\n\nEastern Conference\n")
            print("Southeast Division:")
            for team in json_data['conferences'][1]['divisions'][1]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
            print("Central Division:")
            for team in json_data['conferences'][1]['divisions'][0]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
            print("Atlantic Division:")
            for team in json_data['conferences'][1]['divisions'][2]['teams']:
                print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None



    def get_live_game_stats(self, game_id) -> None:
        
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
            response = self.connection.getresponse()
            
            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # Iterate through the home and away teams and print the player stats
            print(f"\nHome Team: {json_data['home']['market']} {json_data['home']['name']}\n")
            for player in json_data['home']['players']:
                if player['statistics']['minutes'] != "00:00":
                    print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
        
            print(f"\nAway Team: {json_data['away']['market']} {json_data['away']['name']}\n")
            for player in json_data['away']['players']:
                if player['statistics']['minutes'] != "00:00":
                    print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
        
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None

# Get the current schedule of games for today
def get_current_schedule() -> None:


# Get the team roster in format of player name, position, and jersey number    
def get_team_roster_from_id(team_id):
    connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}/profile.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()
    print(data)
    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/15/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))
        
        if not json_data.get('games'):
            raise Exception("No games today!")
        else:

            home_teams = []
            away_teams = []

            print("Today's Schedule:\n")

            for game in json_data['games']:
                home_teams.append(game['home']['name'])
                away_teams.append(game['away']['name'])
                print(f"{game['home']['name']} vs {game['away']['name']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



# Get the team roster in format of player name, position, and jersey number
def get_team_roster_from_id(team_id) -> None:
    try:
        connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}//profile.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None

        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        for player in json_data['players']:
            print(f"{player['full_name']} / {player['position']} / {player['jersey_number']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



def get_league_standings() -> None:
    try:
        connection.request("GET", f"/nba/trial/v8/en/seasons/2023/REG/standings.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))


        for player in json_data['players']:
            print(player)
            return player
            
            
            
            print(f"{player['full_name']} / Position: {player['position']} / Primary position: {player['primary_position']} / Jersey #:{player['jersey_number']}")
            print(f"Player id: {player['id']}")
            print(f"Draft team:{player['draft']['team_id']}  / Year: {player['draft']['year']} / Round: {player['draft']['round']} / Pick: {player['draft']['pick']}")

            a = input("Next player:")

    except json.JSONDecodeError as e:
        print("Something went wrong with the api")
        print(e)
    except Exception as e:
        print(e)
        print("No players found")

        # Print the standings for the Western and Eastern Conference
        print("Western Conference\n")
        print("Southwest Division:")
        for team in json_data['conferences'][0]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Pacific Division:")
        for team in json_data['conferences'][0]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Northwest Division:")
        for team in json_data['conferences'][0]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

        print("\n\n\nEastern Conference\n")
        print("Southeast Division:")
        for team in json_data['conferences'][1]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Central Division:")
        for team in json_data['conferences'][1]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Atlantic Division:")
        for team in json_data['conferences'][1]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



def get_live_game_stats(game_id) -> None:
    
    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
        response = connection.getresponse()
        
        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Iterate through the home and away teams and print the player stats
        print(f"\nHome Team: {json_data['home']['market']} {json_data['home']['name']}\n")
        for player in json_data['home']['players']:
            if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
       
        print(f"\nAway Team: {json_data['away']['market']} {json_data['away']['name']}\n")
        for player in json_data['away']['players']:
           if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
    
    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None

def returnData(team_id):
    connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}/profile.json?api_key={api_key}")
    response = connection.getresponse()
    data = response.read()
    #return data
    json_data = ''
    output = ''
    print(data)
    try:
        json_data = json.loads(data.decode("utf-8"))

        for player in json_data['players']:

            output += f"{player['full_name']} / Position: {player['position']} / Primary position: {player['primary_position']} / Jersey #:{player['jersey_number']}"
            output += f"Player id: {player['id']}"
            if 'team_id' in player['draft']:
                output += f" Draft team:{player['draft']['team_id']} / "
            if 'year' in player['draft']:
                output += f"Year: {player['draft']['year']} / "
            if 'round' in player['draft']:
                output += f"Round: {player['draft']['round']} / "
            if 'pick' in player['draft']:
                output += f"Pick: {player['draft']['pick']}"
            output += "<br><br>"
    except Exception as e:
        print(f"Something went wrong: {e}")

    return output
# Beginning of calls to the API

get_current_schedule()
time.sleep(1)
id = get_game_id_from_date('Milwaukee Bucks', 2024, '02', 15)
time.sleep(1)
get_live_game_stats(id)
time.sleep(1)
print ('\n\n\n')
print(get_league_standings())

api = SportsAPI()
api.get_current_schedule(year,month, '15')
time.sleep(1)
game_id = api.get_game_id('Milwaukee Bucks', year, month, 15)
time.sleep(1)
api.get_live_game_stats(game_id)
time.sleep(1)
print ('\n\n\n')
api.get_league_standings()
