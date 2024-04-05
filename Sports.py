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
from PIL import Image, ImageOps, ImageEnhance # Make sure to import Resampling

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

class TeamStats:
    def __init__(self, team ,points ,assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
        self.team = team
        self.assists = assists
        self.points = points
        self.rebounds = rebounds
        self.blocks = blocks
        self.steals = steals
        self.field_goals_percent = field_goals_percent
        self.three_pointers_percent = three_pointers_percent
        self.free_throws_percent = free_throws_percent
    

    def update_stats(self,name,points,assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
        self.team = team
        self.points = points
        self.assists = assists
        self.rebounds = rebounds
        self.blocks = blocks
        self.steals = steals
        self.field_goals_percent = field_goals_percent
        self.three_pointers_percent = three_pointers_percent
        self.free_throws_percent = free_throws_percent
## End of Team Stats class ## 



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        
        try:
            self.resample_filter = Image.LANCZOS  # Newer versions of Pillow
        except AttributeError:
            self.resample_filter = Image.ANTIALIAS  # Older versions of Pillow
        
        # Individual Stats
        # Playername, Team, Points, Assists, Rebounds, Blocks, Steals, Field Goal Percent, Three Points Percent, Free Throws Percent
        self.players = [
            PlayerStats("Player 1234567890ABC", "Team A" ,"0" ,"0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team B" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team C","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team D" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team E" ,"0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team F","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team G","0" , "0", "0", "0", "0", "0", "0", "0"),
            PlayerStats("Player 1234567890ABC", "Team H" ,"0" , "0", "0", "0", "0", "0", "0", "0")
        ]
        
        # Total Team Stats
        # Team, Points, Assists, Rebounds, Blocks, Steals, Field Goal Percent, Three Points Percent, Free Throws Percent
        self.teams = [
            TeamStats("TeamName 1","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 2","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 3","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 4","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 5","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 6","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 7","0" , "0", "0", "0", "0", "0", "0", "0"),
            TeamStats("TeamName 8","0" , "0", "0", "0", "0", "0", "0", "0"),
            
        ]
        
        #initualise team positions
        self.team_positions = None
        
        #initualizing Players from File
        #self.loadPlayersFromFile()
        
        # Loading Font
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/4x6.bdf")
        
        #Define Colors        
        self.name_color = graphics.Color(255, 165, 0) # Orange (Slightly brighter than original)
        self.team_color = graphics.Color(0, 255, 0) # Green (Sharp and Clean)
        self.assists_color = graphics.Color(0, 255, 255) # Cyan (For clarity and communication)
        self.rebounds_color = graphics.Color(0, 0, 255) # Blue (Reliability, strength)
        self.blocks_color = graphics.Color(128, 0, 128) # Purple (Wisdom, bravery)
        self.steals_color = graphics.Color(255, 0, 0) # Red (Alertness, speed)
        self.points_color = graphics.Color(255, 255, 0) # Yellow (Bright, attention-grabbin)
        self.field_goals_percent_color = graphics.Color(0, 128, 128) # Teal (for steadiness and efficiency)
        self.three_pointers_percent_color = graphics.Color(255, 165, 0) # Orange (for energy and impact)
        self.free_throws_percent_color = graphics.Color(173, 216, 230) # Light Blue (for precision and calm)


        self.datetime_color = graphics.Color(255, 255, 255) # WHITE (clarity)
        self.teamstats = graphics.Color(0, 255, 255)# CYAN -- still working on it.


        
    def display_image(self, offscreen_canvas, image_path):
        # Open the image using PIL
        image = Image.open(image_path)
        # Resize the image to fit display
        image = image.resize((128, 58), self.resample_filter)
        
        # Convert the image to RGB format
        image = image.convert('RGB')
        
        # Display the image on the LED matrix
        for x in range(128):
            for y in range(58):
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
        api = GameFacade()
        text_height = 6
        x_pos = 2
        vertical_pos = 64
      
     
        
        # Prepare the offscreen canvas
        offscreen_canvas = self.matrix.CreateFrameCanvas()

        # Clear the screen
        self.clearScreen(offscreen_canvas)

        # Display the image for a certain period
        self.display_image(offscreen_canvas, 'Logo3.png')
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
       

       
        for player in self.players:
            time.sleep(1)
            
            try:
                player_stats_list = api.get_player_stats(player.name, "2024", "04", "02")
                time.sleep(1)
            except Exception as e:
                print(f"Error fetching stats for {player.name}: {e}")
                continue  # Skip to next player if an error occurs

            if not player_stats_list:
                print(f"No stats found for {player.name}")
                continue  # Skip to next player if no stats were returned

            found = False  # Flag to check if matching stats were found

            for stats in player_stats_list:
                
                if player.name == stats.name:
                    vertical_pos -=  text_height 

                    print(f"Updating stats for: {stats.name}")
                    stats_update= f"Loading...{stats.name}"
                    self.clearScreen(offscreen_canvas)
                    self.display_image(offscreen_canvas, 'Logo3.png')
                    stats_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.team_color, stats_update)
    
                    graphics.DrawText(offscreen_canvas, self.font,x_pos, vertical_pos+6, self.team_color, stats_update)
                    vertical_pos += text_height
                    # Update player stats here
                    player.update_stats(stats.name, stats.team, stats.points, stats.assists, stats.rebounds, stats.blocks, stats.steals, stats.field_goals_percent, stats.three_pointers_percent, stats.free_throws_percent)
                    found = True
                    break  # Exit loop after updating

            if not found:
                print(f"No matching player found for {player.name} in the stats.")
                

            self.matrix.SwapOnVSync(offscreen_canvas)
            
        #Used for trasiton from Loading Players to Live Stats
        self.clearScreen(offscreen_canvas)
        self.display_image(offscreen_canvas, 'Logo3.png')
        time.sleep(1)

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
            return graphics.Color(0,128,0) #GREEN
    
                
            
        
    def displayPlayerStats(self, offscreen_canvas):
        
        # Player name Lengths
        clearance = 2
        text_height = 6
        separation = 3
        
        
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
           # graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + separation, vertical_pos,self.teamstats,player_text)
            #self.team_positions[i] -= 1
        

            #Total Length
            tempLength = separation;
            
            # Draw player team
            team_text = f" {player.team}"
            team_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.team_color, team_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i], vertical_pos, self.team_color, team_text)
            tempLength += team_length + separation

                        
            # Draw player points
            points_text = f" Points: {player.points}"
            points_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, points_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.points_color, points_text)
            tempLength += points_length + separation

            # Draw player assists
            assists_text = f" Assists: {player.assists}"
            assists_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, assists_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.assists_color, assists_text)
            tempLength += assists_length + separation

            # Draw player rebounds
            rebounds_text = f" Rebounds: {player.rebounds}"
            rebounds_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, rebounds_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.rebounds_color, rebounds_text)
            tempLength += rebounds_length + separation

            # Draw player blocks
            blocks_text = f" Blocks: {player.blocks}"
            blocks_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, blocks_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.blocks_color, blocks_text)
            tempLength += blocks_length + separation

            # Draw player steals
            steals_text = f" Steals: {player.steals}"
            steals_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, steals_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.steals_color, steals_text)
            tempLength += steals_length + separation
            
            #Draw player Feild Goal Percent
            field_goals_percent_text = f" FG%: {player.field_goals_percent}"
            field_goals_percent_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.field_goals_percent_color, field_goals_percent_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.field_goals_percent_color,field_goals_percent_text)
            tempLength += field_goals_percent_length + separation
            
            #Draw player three pointers percent
            three_pointers_percent_text = f" 3P%: {player.three_pointers_percent}"
            three_pointers_percent_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.three_pointers_percent_color, three_pointers_percent_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.three_pointers_percent_color,three_pointers_percent_text)
            tempLength += three_pointers_percent_length+ separation
            
            #Draw player free throws percent
            free_throws_percent_text = f" FT%: {player.free_throws_percent}"
            free_throws_percent_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.three_pointers_percent_color, free_throws_percent_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.free_throws_percent_color,free_throws_percent_text)
            tempLength += free_throws_percent_length+ separation
    
    
    
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
        
        
        #Displays Player Info from Fantasy Roster 
        self.populatePlayerStats()
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
    api = GameFacade()
    facade = LEDDisplayFacade()
    facade.run_text.loadPlayersFromFile()
    while True:
        facade.display_info()
    
    
