import http.client
import json
import datetime
import time
import csv

api_key = "6musfbnhsy2dembz5cxzxade"
month = datetime.datetime.now().month
month = str(month).zfill(2)
day = datetime.datetime.now().day
day = str(day).zfill(2)
year = str(datetime.datetime.now().year)


## Facade Pattern for the API calls ##
class GameFacade:
    ## Constructor for the class
    def __init__(self):
        self.api_key = api_key
        self.connection = http.client.HTTPSConnection("api.sportradar.us")

    ### Game methods ###
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
    

    def get_game_id(self, team_name, year, month, day) -> int:
        game_id = None

        try:
            ## Request to API for the game id
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
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
                
                else:
                    print(f"{team_name} is not playing on {month}-{day}-{year}")

        ## Catching exceptions
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return game_id

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
    
    ### End of game methods ###



    ### Schedule methods ###
    def download_season_schedule(self,year) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/REG/schedule.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            #Creating csv file with the schedule and writing each line as a game
            with open(f"{year}_season_schedule.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Game ID", "Home Team", "Away Team", "Date", "Time"])

                for game in json_data['games']:

                    # Convert GMT time to EST
                    gmt_time = datetime.datetime.strptime(game['scheduled'], "%Y-%m-%dT%H:%M:%SZ")
                    est_time = gmt_time - datetime.timedelta(hours=4)
                    est_time_str = est_time.strftime("%Y-%m-%d %H:%M:%S")

                    writer.writerow([game['id'], game['home']['name'], game['away']['name'], est_time_str[:10], est_time_str[11:16]])

        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None
    

    def get_current_schedule(self,year,month,day) -> None:
        try:
            date_col = 3

            with open("2023_season_schedule.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[date_col] == f"{year}-{month}-{day}":
                        print(f"{row[1]} vs {row[2]} on {row[3]} at {row[4]}")

        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None
    ### End of schedule methods ###



    ### Roster method ###
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
    ### End of roster methods ###
## End of facade class for the API calls ##



## API class to call the facade class ##
class SportsAPI():
    def __init__(self):
        self.game_facade = GameFacade()

    def download_schedule(self,year) -> None:
        self.game_facade.download_season_schedule(year)
        return None
    
    def get_current_schedule(self, year, month, day) -> None:
        self.game_facade.get_current_schedule(year, month, day)
        return None
    
    def get_team_roster(self) -> None:
        self.game_facade.get_team_roster()
        return None
    
    def get_game_id(self,year,month,day,team_name) -> int:
        return self.game_facade.get_game_id(team_name,year,month,day)
    
## End of API class ##

## Main method to call the API class ##
api = GameFacade()

api.get_game_id('Chicago Bulls', year, month, day)