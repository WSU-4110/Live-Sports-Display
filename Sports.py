#==========================================================
#
# Title:      Sports Disply 64x128 LED Matrix
# Author:     Timothy Kosinski
# Date:       06MAR2024
# Description:
#  Drives my LED Matrix Panel, Adifruit Display
# Takes In NBA Player Names and Displays Players Stats
# By using api_calls.py (API) to run display
#==========================================================
#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from datetime import datetime
from PIL import Image, ImageOps, ImageEnhance 

from api_calls import GameFacade
import api_calls
import http.client
import time
import json
import csv


class PlayerStats:
    def __init__(self, name, team ,points ,assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
        self.name = name
        self.team = team
        self.assists = assists
        self.points = points
        self.rebounds = rebounds
        self.blocks = blocks
        self.steals = steals
        self.field_goals_percent = field_goals_percent
        self.three_pointers_percent = three_pointers_percent
        self.free_throws_percent = free_throws_percent
    

    def update_stats(self,name,team,points,assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
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


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        
        try:
            self.resample_filter = Image.LANCZOS  # Newer version of Pillow
        except AttributeError:
            self.resample_filter = Image.ANTIALIAS  # Older version of Pillow
        
        
        
        self.players = [
            PlayerStats("Player 1", "Team A" ,"0" ,"0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 2", "Team B" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 3", "Team C","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 4", "Team D" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 5", "Team E" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 6", "Team F","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 7", "Team G","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 8", "Team H" ,"0" , "0", "0", "0", "0", "0", "0", "0")
        ]
        
        
        #initualise team positions
        self.team_positions = None
        
        #initualizing Players from File
        #self.loadPlayersFromFile()
        
        # Loading Font
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/4x6.bdf")
        
        # Define colors
        self.name_color = graphics.Color(255, 0, 0)
        self.team_color = graphics.Color(0, 255, 0)
        self.assists = graphics.Color(0, 255, 0)
        self.rebounds = graphics.Color(0, 255, 0)
        self.blocks = graphics.Color(0, 255, 0)
        self.steals = graphics.Color(0, 255, 0)

        self.jnumber_color = graphics.Color(0, 0, 255)
        
        self.datetime_color = graphics.Color(255, 255, 255)
        self.teamstats = graphics.Color(255,0,0) 

        self.field_goals_percent = graphics.Color(0, 255, 0)
        self.three_pointers_percent = graphics.Color(0, 255, 0)
        self.free_throws_percent = graphics.Color(0, 255, 0)
        
    def display_image(self, offscreen_canvas, image_path):
        # Open the image using PIL
        image = Image.open(image_path)
        # Resize the image to fit display
        image = image.resize((128, 64), self.resample_filter)
        
        # Convert the image to RGB format
        image = image.convert('RGB')
        
        # Display the image on the LED matrix
        for x in range(128):
            for y in range(64):
                r, g, b = image.getpixel((x, y))
                offscreen_canvas.SetPixel(x, y, r, g, b)

                
    def loadPlayersFromFile(self):
        self.players = []
        try:
            with open('Players.txt','r') as file:
                line = file.readline()
                player_names = line.strip().split(',')
                for name in player_names:
                    self.players.append(PlayerStats(name, "random", "0", "0", "0", "0", "0", "0%", "0%", "0%"))
   
        except IOError as e:
            print(f"An error occurred while reding the file: {e}")
            return
                
    def populatePlayerStats(self):
        player_stats_lists = []
        api = GameFacade()
       
        for player in self.players:
            time.sleep(1)
            player_stats_lists= api.get_player_stats(player.name, "2024", "03", "25")
            time.sleep(1)
       
    
            for stats in player_stats_lists:
                found = False
                for player in self.players:
                   
                    if isinstance(player, PlayerStats) and player.name == stats.name:
                        player.update_stats(stats.name, stats.team, stats.points, stats.assists, stats.rebounds, stats.blocks, stats.steals, stats.field_goals_percent, stats.three_pointers_percent, stats.free_throws_percent)
                        found = True
                        break
                if not found:
                    print(f"No matching player found for stats.name = {stats.name} in self.players")
    '''
        for stats in player:
            try:
                time.sleep(1)
                print(player)
                player_stats_list = api.get_player_stats(player)
                time.sleep(1)
                

              
             
                if player_stats_list:
                    player_stats = player_stats_list[i]

                    )
                
                else:
                    # Handle case where stats are not found
                    updated_player = PlayerStats(
                        player, "Data not available", "", "", "", "", 
                        "", "", "", ""
                    )
                     
                    
            except Exception as e:
                print(f"Error fetching stats for : {e}")
                # Handle exceptions by using default or previous values
                updated_player = PlayerStats(
                  #  name, "Error fetching data", "", "", "", "", "", "", "", ""
                )
              
        
        updated_player.append(updated_player)

        self.players = updated_players
    '''

    def set_default_values_for_player(self, player, updated_players):
        updated_players.append(PlayerStats(
            player.name, "Data not available", "00", "0", "0", "0", "0", "0%", "0%", "0%"
        ))
           
    def displayDateTime(self,offscreen_canvas):
        # Getting Current Time
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y") # format DAY/MONTH/YEAR 
        datetime_str = now.strftime( "%H:%M:%S") #format HOUR:MINUTES:SECONDS
        
        #local Variables
        x_position = 0;
        y_position = offscreen_canvas.height
        text_height = 6
        
        # Draw the stationary Date with Time
        graphics.DrawText(offscreen_canvas, self.font, x_position, y_position, self.datetime_color, datetime_str)
        graphics.DrawText(offscreen_canvas, self.font, x_position, y_position-text_height, self.datetime_color, date_str)
    

    def blackRectangle(self, offscreen_canvas, xcord, ycord, rect_width, rect_height):
        for x in range(xcord, xcord + rect_width):
            for y in range(ycord, ycord + rect_height):
                offscreen_canvas.SetPixel(x, y, 0, 0, 0)  # Drawing black rectangle
                
    def grayRectangle(self, offscreen_canvas, xcord, ycord, rect_width, rect_height):
        for x in range(xcord, xcord + rect_width):
            for y in range(ycord, ycord + rect_height):
                offscreen_canvas.SetPixel(x, y, 1, 50, 1)  # Drawing black rectangle

    def clearScreen(self,offscreen_canvas):
        offscreen_canvas.Clear()
        
        
    def determinePercentColor(number):
        
        if number < 25:
             return graphics.Color(255,0,0) #RED
        elif number < 50:
            return graphics.Color(255,165,0) #ORANGE
        elif number <75:
            return graphics.Color(255,255,0) #YELLLO
        else:
            return graphics.Color(0,128,0) #GREEn
                
            
        
    def displayPlayerStats(self, offscreen_canvas):
        
        # Player name Lengths
        clearance = 2
        text_height = 6;
        separation = 5
        
        player_name_lengths = []
        for player in self.players:
            # Temporarily draw the text offscreen to measure its length
            length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, player.name)
            player_name_lengths.append(length)

        max_name_length = max(player_name_lengths)
        
        

        for i, player in enumerate(self.players):
            player_text = f"{player.team} ,Points: {player.points} ,Assists: {player.assists} ,Rebounds: {player.rebounds} ,Blocks: {player.blocks} ,Steals: {player.steals} ,FG%: {player.field_goals_percent} ,3P%: {player.three_pointers_percent} ,FT%: {player.free_throws_percent}"
            
            player_text_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, player_text)
            
        
            vertical_pos =  text_height * (i + 1)
        
            # Draw the scrolling team stats
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + separation, vertical_pos,self.teamstats,player_text)
            self.team_positions[i] -= 1
    
            # Reset position if text has scrolled off
            if self.team_positions[i] + player_text_length < 0 :  # Off the Screen, adjusted to the length of the team name
                self.team_positions[i] = offscreen_canvas.width

            # Draw black rectangles for names
            self.blackRectangle(offscreen_canvas, 0, vertical_pos - text_height+1, max_name_length + clearance + 1, text_height + clearance)
            #Draw black rectangle for jersey number
            #self.blackRectangle(offscreen_canvas, offscreen_canvas.width - 11 - (2 * clearance), vertical_pos-text_height, max_name_length + (2 * clearance), text_height + clearance)
    
            # Draw the stationary player name
            graphics.DrawText(offscreen_canvas, self.font, clearance, vertical_pos, self.name_color, player.name)
    '''
            # Draw the stationary player number with '#'
            graphics.DrawText(offscreen_canvas, self.font, offscreen_canvas.width - 11 - clearance, vertical_pos, self.name_color, "#")
    '''
        
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        if not self.team_positions:
            self.team_positions = [self.matrix.width for _ in self.players]
        
        #Displays Logo For 10 Seconds Before Changing screens
        self.clearScreen(offscreen_canvas)
        # Display an image
        self.display_image(offscreen_canvas, 'Logo3.png')
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(10)
        

        #Displays Player Info from Fantasy Roster 
        while True:
            # Clear Display
            self.clearScreen(offscreen_canvas)
            # Display Player Stats
            self.displayPlayerStats(offscreen_canvas)
            # Draw date and time
            self.displayDateTime(offscreen_canvas)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.05)
    
class LEDDisplayFacade:
    def __init__(self):
        self.run_text = RunText()
    
    def display_info(self):
        if not self.run_text.process():
            print("Failed to run Matrix")
            return
        self.run_text.run()

if __name__ == "__main__":
    api = GameFacade()  # or SportsAPI(), if that's the class you're working with
    
    # Call the methods to download the data you need

    facade = LEDDisplayFacade()
    facade.run_text.loadPlayersFromFile()
    facade.run_text.populatePlayerStats()
    while True:
        facade.display_info()
    
    
