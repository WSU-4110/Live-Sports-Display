import http.client
import json
import datetime
import os.path
import csv




api_key = 'ry27AHhE2O4WbIO24c0DE4Zt1KeMvyMx5f31taX1'
connection = http.client.HTTPSConnection("api.sportradar.us")
comConnect = http.client.HTTPSConnection("api.sportradar.com")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year

season_year = 2023
season_type = "REG"

teams_file = "teams.csv"

schedule_file = "game_schedule.csv"

player_list = "All_players_ID.csv"



# makes a csv file containing the team ids
def get_teams():
    #if teams_file exists, exit (and save an api call)
    if os.path.isfile(teams_file):
        return None
    else:
        try:
            # Connection and response status 
            connection.request("GET", f"/nba/trial/v8/en/seasons/{season_year}/{season_type}/rankings.json?api_key={api_key}")
            response = connection.getresponse()
    
            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
    
            # Read & decode data
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # creates file to store teams
            teams = open(teams_file,"w")
            writer = csv.writer(teams)
            writer.writerow(["Team ID", "Market", "Team Name"])
            # goes through each thing to write down all teams
            for conference in json_data['conferences']:
            
                for division in conference['divisions']:
                
                    for team in division['teams']:
                    
                        writer.writerow([team['id'],team['name'],team['market']])
                    
                    
        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None

#makes a csv file containing player ids and name
def get_team_players(team_id):
    #if team_file exists, exit (and save an api call)
    if os.path.isfile(f"{team_id}.csv"):
        return None
    else:
        try:

            # Connection and response status 
            connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}/profile.json?api_key={api_key}")
            response = connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            # read and decode
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            # create team file
            players = open(f"{team_id}.csv","w")
            writer = csv.writer(players)
            writer.writerow(["Player ID", "Player Name"])
            
            # write all players to team file
            for player in json_data['players']:
                writer.writerow([player['id'],player['full_name']])
                    
                    
                    
        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None


#Percentage (turns numbers into a percentage)
def per(made, att):
    return 100 * made // att


# gets and returns player stats in a single string
def get_season_player_stats_from_id(player_id):
    try:
        # Connection and response status
        connection.request("GET", f"/nba/trial/v8/en/players/{player_id}/profile.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None

        # read and decode
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Adds name and team to output
        output = "Name: " + json_data['full_name']
        team = json_data['team']
        output +=" Team: " + team['market'] + " " + team['name']

        team_id = team['id']

        # finds the relevant season
        for season in json_data['seasons']:
            
            if (season['type'] == season_type) and (season['year'] == season_year):

                for team in season['teams']:
                    
                    if team['id'] == team_id:
                        # collects the relevant data, and adds it to the output
                        data = team['total']
                        
                        FGM = data['field_goals_made']
                        FGA = data['field_goals_att']
                        FG = per(FGM,FGA)

                        ThreePM = data['three_points_made']
                        ThreePA = data['three_points_att']
                        TP = per(ThreePM,ThreePA)

                        FTM = data['free_throws_made']
                        FTA = data['free_throws_att']
                        FT = per(FTM,FTA)

                        REB = data['rebounds']
                        AST = data['assists']
                        BLK = data['blocks']
                        STL = data['steals']
                        PTS = data['points']

                        output += f" FG: {FG}"
                        output += f" TP: {TP}"
                        output += f" FT: {FT}"
                        output += f" REB: {REB}"
                        output += f" AST: {AST}"
                        output += f" BLK: {BLK}"
                        output += f" STL: {STL}"
                        output += f" PTS: {PTS}"

                        return output
                    
                    
                    
    # Catching exceptions #
    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



def get_schedule():
    
    #if schedule exists, check to see if it's up to date
    if os.path.isfile(schedule_file):
        with open(schedule_file, 'r') as check:
            reader = csv.reader(check)
            line = 0

            # look at second line (skips beginning)
            for row in reader:
                if line == 1:
                    
                    date_time = row[0]

                    #if the date fits the season-year, it's up to date
                    if date_time[0:4] == str(season_year):
                        return None
                    else: # if not, continue with the rest of the program
                        break
                line += 1
    
        
                
    try:
        # connection and response status
        connection.request("GET", f"/nba/trial/v8/en/games/{season_year}/{season_type}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None

        # read and ... (yawn) ... decode
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # create file, write times and teams of games
        with open(schedule_file,"w", newline = "") as games:
            writer = csv.writer(games)
            writer.writerow(["Time", "Home", "Away"])
            for game in json_data['games']:
                #Time conversion
                gmt_time = datetime.datetime.strptime(game['scheduled'], "%Y-%m-%dT%H:%M:%SZ")
                est_time = gmt_time - datetime.timedelta(hours=4)
                est_time_str = est_time.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([est_time_str,game['home']['name'],game['away']['name']])
                        
                    
    # Catching exceptions #
    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None

# checks if there's any games between hours (est military time)
#   and returns all
def game_in_time(hour_start, hour_end):
    # makes sure there's a schedule to read from
    get_schedule()

    #opens the schedule file
    output = ""
    with open(schedule_file, 'r') as file:
        games = csv.reader(file)
        first = True
        for game in games:
            if first: # gets past the first line
                first = False
            else:
                # gets the date of the game
                time = game[0]
                game_year = int(time[0:4])
                game_month = int(time[5:7])
                game_day = int(time[8:10])
                #checks the date
                if game_year == year:
                    
                    if game_month == month:
                        
                        if game_day == day:
                            # checks the time
                            game_hour = int(time[11:13])

                            if (game_hour >= hour_start) and (game_hour <= hour_end):  # game found
                                output += f"{game[1]}vs{game[2]}\n"
                        #if we've gone past the current date, stop checking
                        elif game_day > day:
                            return output
                            

    return output # just in case there are no more games in the season

# Makes a csv file containing player names and ID                       
def player_id_list():
    #if player_list exists, exit
    if os.path.isfile(player_list):
        return None
    else:
        # makes sure teams list is present
        get_teams()
        
        # creates array with team IDs
        team_IDs = []
        with open(teams_file, 'r') as file:
            teams = csv.reader(file)
            line = 0
            
            for team in teams:
                
                #if at first row, do nothing
                if line != 0:
                    team_IDs.append(team[0])
                        
                line += 1


        # makes the player list
        players = open(player_list,"w", newline = "")
        writer = csv.writer(players)
        writer.writerow(["Player_Name", "Player_ID", "Team_ID"])



        # goes through each team, and add players to the file
        try:
            for team_id in team_IDs:

                time.sleep(5) #This makes it take a while, but it stops the api from complaining about too many calls
                connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}/profile.json?api_key={api_key}")
                response = connection.getresponse()

                if response.status != 200:
                    print("Error: ", response.status, response.reason)
                    return None
                
                data = response.read()
                
                json_data = json.loads(data.decode("utf-8"))

               
                for player in json_data['players']:
                    writer.writerow([player['full_name'],player['id'], team_id])
                        
            # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None

def get_player_stats_from_id(player_id, team_id):
    try:
        #Connection & response status
        comConnect.request("GET", f"/nba/trial/stream/en/statistics/subscribe?api_key={api_key}&players==sd:player:{player_id}")

        response = comConnect.getresponse()
        
        if response.status != 200:
            print("Error:", response.status, response.reason)
            return None

        data = response.read()
        #print(data) #----------------------------------------------------------If the code doesn't work - but the api server isn't idle - could you send the result of this?
        json_data = json.loads(data.decode("utf-8"))

        # setup of output
        output = "Name: " + json_data['full_name']

        # gets team name
        team_name = ""
        with open(team_id_list, 'r') as file:
            teams = csv.reader(file)
            for team in teams:
                if team_id == team[0]:
                    team_name = f"{team[2]} {team[1]}"

        output +=" Team: " + team_name


        # gets all the relevant stats, and adds it to the output
        data = json_data['statistics']
        
        FGM = data['field_goals_made']
        FGA = data['field_goals_att']
        FG = per(FGM,FGA)

        ThreePM = data['three_points_made']
        ThreePA = data['three_points_att']
        TP = per(ThreePM,ThreePA)

        FTM = data['free_throws_made']
        FTA = data['free_throws_att']
        FT = per(FTM,FTA)

        REB = data['rebounds']
        AST = data['assists']
        BLK = data['blocks']
        STL = data['steals']
        PTS = data['points']

        output += f" FG: {FG}"
        output += f" TP: {TP}"
        output += f" FT: {FT}"
        output += f" REB: {REB}"
        output += f" AST: {AST}"
        output += f" BLK: {BLK}"
        output += f" STL: {STL}"
        output += f" PTS: {PTS}"

        return output
                    
                    
                    
    # Catching exceptions #
    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"A Http exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None


# gets player stats from name
def get_player_stats(player_name, isLive):
    
    #makes sure player_list exists
    player_id_list()
    
    # opens player list
    with open(player_list, 'r') as file:
            players = csv.reader(file)


            # goes through each player until an name matches
            for player in players:
                
                if player[0] == player_name:
                    if isLive: # If getting live stats, get live, else get season
                        return get_player_stats_from_id(player[1], player[2])
                    else:
                        return get_season_player_stats_from_id(player[1])

            return "! No player found !" # returns a message if no players found


#game_in_time(20,22)     

#get_teams()
#get_team_players("583eccfa-fb46-11e1-82cb-f4ce4684ea4c")

##i = get_player_stats("0718c0e1-7804-471a-b4ed-cde778948d4d")
##print(i)


#get_schedule()

#get_teams()
#get_team_players("583eccfa-fb46-11e1-82cb-f4ce4684ea4c")
