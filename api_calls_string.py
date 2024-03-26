import http.client
import json
import datetime
import os.path
import csv




api_key = 'ry27AHhE2O4WbIO24c0DE4Zt1KeMvyMx5f31taX1'
connection = http.client.HTTPSConnection("api.sportradar.us")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year

season_year = 2023
season_type = "REG"

teams_file = "teams.csv"







# makes a csv file containing the team ids
def get_teams():
    try:
        connection.request("GET", f"/nba/trial/v8/en/seasons/{season_year}/{season_type}/rankings.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        print(data)
        json_data = json.loads(data.decode("utf-8"))

        teams = open(teams_file,"w")
        writer = csv.writer(teams)
        writer.writerow(["Team ID", "Market", "Team Name"])
        for conference in json_data['conferences']:
            print("new conference")
            for division in conference['divisions']:
                print("new division")
                for team in division['teams']:
                    print("new team")
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
    try:
        connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}/profile.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
    
        json_data = json.loads(data.decode("utf-8"))
        players = open(f"{team_id}.csv","w")
        writer = csv.writer(players)
        writer.writerow(["Player ID", "Player Name"])
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


#Percentage
def per(made, att):
    return 100 * made // att


def get_player_stats(player_id):
    try:
        connection.request("GET", f"/nba/trial/v8/en/players/{player_id}/profile.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
    
        json_data = json.loads(data.decode("utf-8"))
        output = "Name: " + json_data['full_name']
        team = json_data['team']
        output +=" Team: " + team['market'] + " " + team['name']

        team_id = team['id']


        for season in json_data['seasons']:
            
            if (season['type'] == season_type) and (season['year'] == season_year):

                for team in season['teams']:
                    
                    if team['id'] == team_id:
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
            
            for row in reader:
                
                #if year is season_year, end
                if line == 1:
                    
                    date_time = row[0]

                    if date_time[0:4] == str(season_year):
                        return None
                line += 1
    
        
                
    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{season_year}/{season_type}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
    
        json_data = json.loads(data.decode("utf-8"))
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
    get_schedule()
    
    output = ""
    with open(schedule_file, 'r') as file:
        games = csv.reader(file)
        first = True
        for game in games:
            if first:
                first = False
            else:
                time = game[0]
                game_year = int(time[0:4])
                game_month = int(time[5:7])
                game_day = int(time[8:10])
                #check year, month, day
                if game_year == year:
                    
                    if game_month == month:
                        
                        if game_day == day:
                            
                            game_hour = int(time[11:13])

                            if (game_hour >= hour_start) and (game_hour <= hour_end):  # game found
                                output += f"{game[1]}vs{game[2]}\n"

    return output
                                          
#game_in_time(20,22)     

#get_teams()
#get_team_players("583eccfa-fb46-11e1-82cb-f4ce4684ea4c")

##i = get_player_stats("0718c0e1-7804-471a-b4ed-cde778948d4d")
##print(i)


#get_schedule()

#get_teams()
#get_team_players("583eccfa-fb46-11e1-82cb-f4ce4684ea4c")
