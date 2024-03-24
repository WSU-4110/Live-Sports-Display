import http.client
import json
import datetime
import time
import csv

api_key = '284s83ypFD8LAEu1Y6WFK5peMLz1KF0Y7jSFHizV'
month = datetime.datetime.now().month
month = str(month).zfill(2)
day = datetime.datetime.now().day
day = str(day).zfill(2)
year = str(datetime.datetime.now().year)

## Player class ##
class PlayerStats:
    def __init__(self, name, team,  points, assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
        self.name = name
        self.team = team
        self.points = points
        self.assists = assists
        self.rebounds = rebounds
        self.blocks = blocks
        self.steals = steals
        self.field_goals_percent = field_goals_percent
        self.three_pointers_percent = three_pointers_percent
        self.free_throws_percent = free_throws_percent
## End of player class ## 
## Team roster class ##
class TeamRoster:
    def __init__(self, full_name, position, jersey_number):
        self.full_name = full_name
        self.position = position
        self.jersey_number = jersey_number
## End of team roster class ##
## Team standings class ##
class TeamStandings:
    def __init__(self, team_name, wins, losses, team_id):
        self.team_name = team_name
        self.wins = wins
        self.losses = losses
        self.team_id = team_id
## End of team standings class ##

## Facade class for the API calls ##
class GameFacade:
    ''' Constructor for the class '''
    def __init__(self):
        self.api_key = api_key
        self.connection = http.client.HTTPSConnection("api.sportradar.us")



    ### Schedule methods ###
    ''' USE ONLY ON THE FIRST TIME TO DOWNLOAD THE SCHEDULE '''
    def download_season_schedule(self,year) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/REG/schedule.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Creating csv file with the schedule and writing each line as a game '''
            with open(f"{year}_season_schedule.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Game ID", "Home Team", "Away Team", "Date", "Time"])

                for game in json_data['games']:

                    ''' Convert GMT time to EST '''
                    gmt_time = datetime.datetime.strptime(game['scheduled'], "%Y-%m-%dT%H:%M:%SZ")
                    est_time = gmt_time - datetime.timedelta(hours=4)
                    est_time_str = est_time.strftime("%Y-%m-%d %H:%M:%S")

                    writer.writerow([game['id'], game['home']['name'], game['away']['name'], est_time_str[:10], est_time_str[11:16]])

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None
    

    def get_current_schedule(self,year,month,day):
        schedule = []
        try:
            date_col = 3

            with open("2023_season_schedule.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[date_col] == f"{year}-{month}-{day}":
                        schedule.append(f"{row[1]} vs {row[2]} on {row[3]} at {row[4]}")
        
        # Catching exceptions #
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return schedule



    ### Game methods ###
    def get_league_standings(self):
        standings = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/seasons/2023/REG/standings.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Add the teams to the standings list into objects of TeamStandings '''
            for conference in json_data['conferences']:
                for division in conference['divisions']:
                    for team in division['teams']:
                        standings.append(TeamStandings(team['market'] + " " + team['name'], team['wins'], team['losses']))

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return standings
    ### End of game methods ###

    

    ### ID methods (Not used on website) ###
    # Get the game id from the team name
    def get_game_id(self, team_name, year, month, day) -> int:
        game_id = None

        try:
            ''' Request to API for the game id '''
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Loop through the games and find the game id the team name '''
            for game in json_data['games']:
                if game['home']['name'] == team_name:
                    game_id = game['id']
                    break
                elif game['away']['name'] == team_name:
                    game_id = game['id']
                    break
            if game_id == None:
                print(f"No game found for {team_name} on {month}-{day}-{year}")

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return game_id
    
    # Get the team id from the team name
    def get_team_id(self, team_name) -> int:
        team_id = None

        try:
            ''' Request to API for the team id '''
            self.connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={self.api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Loop through the games and find the team id from param team_name '''
            for game in json_data['games']:
                if game['home']['name'] == team_name:
                    team_id = game['home']['id']
                elif game['away']['name'] == team_name:
                    team_id = game['away']['id']
        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        
        return team_id
    ### End of ID methods ###



    ### Roster method ###
    ''' Get the team roster in format of player name, position, and jersey number '''
    def get_team_roster_from_id(self,team_id):
        roster = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}//profile.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            for player in json_data['players']:
                roster.append(TeamRoster(player['full_name'], player['position'], player['jersey_number']))
            
        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return roster
    
    def find_player(self, roster, player_name):
        for player in roster:
            if player.full_name == player_name:
                return player
        return None
    ### End of roster methods ###



    ### Stats methods ###
    def get_live_game_stats(self, game_id):
        players = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
            response = self.connection.getresponse()
            
            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Iterate through the home and away teams and add to the players list if the player has played in the game'''
            for player in json_data['home']['players']:
                if player['statistics']['minutes'] != "00:00":
                    players.append(PlayerStats(player['full_name'], json_data['home']['market'] + " " + json_data['home']['name'], player['statistics']['points'], player['statistics']['assists'], player['statistics']['rebounds'], player['statistics']['blocks'], player['statistics']['steals'], player['statistics']['field_goals_pct'], player['statistics']['three_points_pct'], player['statistics']['free_throws_pct']))
            for player in json_data['away']['players']:
                if player['statistics']['minutes'] != "00:00":
                    players.append(PlayerStats(player['full_name'], json_data['away']['market'] + " " + json_data['away']['name'], player['statistics']['points'], player['statistics']['assists'], player['statistics']['rebounds'], player['statistics']['blocks'], player['statistics']['steals'], player['statistics']['field_goals_pct'], player['statistics']['three_points_pct'], player['statistics']['free_throws_pct']))

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return players
    
    def find_player_stats(self, players, player_name):

        for player in players:
            if player.name == player_name:
                return player
        return None
    ### End of stats methods ###
## End of facade class for the API calls ##

## API class to call the facade class ##
class SportsAPI():
    def __init__(self):
        self.game_facade = GameFacade()

    def download_season_schedule(self, year):
        self.game_facade.download_season_schedule(year)

    def get_current_schedule(self, year, month, day):
        self.game_facade.get_current_schedule(year, month, day)
    
    def get_league_standings(self):
        self.game_facade.get_league_standings()

    def get_game_id(self, team_name, year, month, day):
        return self.game_facade.get_game_id(team_name, year, month, day)
    
    def get_team_id(self, team_name):  
        return self.game_facade.get_team_id(team_name)
    
    def get_team_roster_from_id(self, team_id):
        self.game_facade.get_team_roster_from_id(team_id)

    def find_player(self, roster, player_name):
        return self.game_facade.find_player(roster, player_name)
    
    def get_live_game_stats(self, game_id):
        return self.game_facade.get_live_game_stats(game_id)

    def find_player_stats(self, players, player_name):
        return self.game_facade.find_player_stats(players, player_name)
## End of API class ##



### Main method to call the API class ###
'''
How to use the main method:
1. Create an instance of the API class
2. Look at methods within sportsAPI class to see what methods are available
3. Call the methods with the appropriate parameters
4. Some methods will require an api call to the API class to get the data i.e get_team_roster_from_id requires a team id that can be obtained from get_team_id
5. The methods will return the data in the form of a list or object that can be used to display the data on the website/console or the raspberry pi
6. Between each method call, there MUST be a time.sleep(1) to prevent the API from being overloaded and blocking a request
7. The main method is a template to show how to call the methods, it is not meant to be run as is
'''
api = GameFacade()

teamid = api.get_team_id("Sacramento Kings")
time.sleep(1)
roster = api.get_team_roster_from_id(teamid)
time.sleep(1)
player = api.find_player(roster, "De'Aaron Fox")

'''The running of this code will print De'Aaron Fox G 5, and player is a object of the TeamRoster class'''
### End of main method ###