#==========================================================
#
# Title:      Sports Display 64x128 LED Matrix
# Author:     Timothy Kosinski
# Date:       12APR2024
# Description:
#  Drives my LED Matrix Panel, Adifruit Display
# Takes In NBA Player Names and Displays Players Stats
# By using api_calls.py (API) to run the display
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
import socket
import os

class UserInfo:
    def __init__(self,ip_address):
        self.ip_address = ip_address
        
    def update_userInfo(self,ip_address):
        self.ip_address = ip_address

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
    

    def update_stats(self,team,points,assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
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
        
        #Had issues from Previous Library... So included both incase of an Unexpected Error!
        try:
            self.resample_filter = Image.LANCZOS  # Newer versions of Pillow
        except AttributeError:
            self.resample_filter = Image.ANTIALIAS  # Older versions of Pillow
        
        #initualise team positions
        self.team_positions = None
        
        # Loading Font
        self.font = graphics.Font()
        self.font.LoadFont("/home/timkosinski/rpi-rgb-led-matrix/fonts/4x6.bdf")
        
        #Define Colors        
        self.name_color = graphics.Color(255, 165, 0) # Orange 
        self.team_color = graphics.Color(0, 255, 0) # Green
        self.assists_color = graphics.Color(0, 255, 255) # Cyan 
        self.rebounds_color = graphics.Color(0, 0, 255) # Blue 
        self.blocks_color = graphics.Color(128, 0, 128) # Purple 
        self.steals_color = graphics.Color(255, 0, 0) # Red 
        self.points_color = graphics.Color(255, 255, 0) # Yellow 
        self.field_goals_percent_color = graphics.Color(0, 128, 128) # Teal 
        self.three_pointers_percent_color = graphics.Color(255, 165, 0) # Orange 
        self.free_throws_percent_color = graphics.Color(173, 216, 230) # Light Blue 
        
        self.error_color = graphics.Color(255, 0, 0) # Red 
        self.no_stats_color = graphics.Color(255, 255, 0) # Yellow
        self.updating_stats_color =graphics.Color(0, 255, 0) #Green


        self.datetime_color = graphics.Color(255, 255, 255) # WHITE 
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
            with open('/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Players.txt','r') as file:
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
        self.display_image(offscreen_canvas, '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Logo3.png')
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
       

       
        for player in self.players:
            time.sleep(1)
            
            try:                                                        #2024,APR,07
                player_stats_list = api.get_player_stats(player.name, "2024", "04", "07")
                time.sleep(1)
            except Exception as e:
                print(f"Error fetching stats for {player.name}: {e}")
                stats_Error= f"Error...{player.name}"
                self.clearScreen(offscreen_canvas)
                self.display_image(offscreen_canvas, '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Logo3.png')
                graphics.DrawText(offscreen_canvas, self.font,x_pos, vertical_pos-1, self.error_color, stats_Error)
                time.sleep(1)
                continue  # Skip to next player if an error occurs

            if not player_stats_list:
                print(f"No stats found for {player.name}")
                no_stats= f"No Stats...{player.name}"
                self.clearScreen(offscreen_canvas)
                self.display_image(offscreen_canvas, '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Logo3.png')
                graphics.DrawText(offscreen_canvas, self.font,x_pos, vertical_pos-1, self.no_stats_color, no_stats)
                time.sleep(1)
                continue  # Skip to next player if no stats were returned

            found = False  # Flag to check if matching stats were found

            for stats in player_stats_list:
                
                if player.name == stats.name:
                    
                    print(f"Updating stats for: {stats.name}")
                    stats_update= f"Loading...{stats.name}"
                    self.clearScreen(offscreen_canvas)
                    self.display_image(offscreen_canvas, '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Logo3.png')
                    graphics.DrawText(offscreen_canvas, self.font,x_pos, vertical_pos-1, self.updating_stats_color, stats_update)
                   
                    # Update player stats here
                    player.update_stats(stats.name, stats.team, stats.points, stats.assists, stats.rebounds, stats.blocks, stats.steals, stats.field_goals_percent, stats.three_pointers_percent, stats.free_throws_percent)
                    found = True
                    time.sleep(1)
                    break  # Exit loop after updating

            if not found:
                print(f"No matching player found for {player.name} in the stats.")
                
            time.sleep(1)
            self.matrix.SwapOnVSync(offscreen_canvas)


    def set_default_values_for_player(self, player, updated_players):
        updated_players.append(PlayerStats(
            player.name, "Data not available", "00", "0", "0", "0", "0", "0%", "0%", "0%"
        ))
    
    def update_ip_address(self):
        self.ip_address=self.get_ip_address()    
    
     

    def get_ip_address(self):
        # Attempt to connect and get local IP address
        try:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Attempt to connect to nothing.
            s.connect(("2.2.2.2", 80))
            local_ip_address = s.getsockname()[0]
            s.close()
        except Exception as e:
            self.clearScreen(offscreen_canvas)
            local_ip_address = "UNKNOWN"
        return local_ip_address


 
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

    #Used to cut down on repetitive code used in "displayPlayerStats"
    def draw_stat_text(self, canvas, font, x_position, y_position, color, category, value):

        stat_text = f" {category}: {value}"
        stat_length = graphics.DrawText(canvas, font, -canvas.width, -canvas.height, color, stat_text)
        graphics.DrawText(canvas, font, x_position, y_position, color, stat_text)
        return stat_length             
        
    #Display player stats and player names
    def displayPlayerStats(self, offscreen_canvas):
    
        # Player name Lengths
        clearance = 2
        text_height = 6
        separation = 3
        
        non_random_players = [player for player in self.players if player.team != "random"]
        player_name_lengths = []
        
        for player in non_random_players :
            # Temporarily draw the text offscreen to measure its length
            length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, player.name)
            player_name_lengths.append(length)

        max_name_length = max(player_name_lengths) if player_name_lengths else 0
        
 
        
        
        for i, player in enumerate(non_random_players):
            #Total Length
            tempLength = separation
            if player.team == "random":
                continue
                
            vertical_pos =  text_height * (i + 1)
            player_text = f"{player.team} ,Points: {player.points} Assists: {player.assists} ,Rebounds: {player.rebounds} ,Blocks: {player.blocks} ,Steals: {player.steals} ,FG%: {player.field_goals_percent} ,3P%: {player.three_pointers_percent} ,FT%: {player.free_throws_percent}"
            player_text_length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, player_text)
            
                        
            if self.team_positions[i] + player_text_length < max_name_length + clearance + clearance:
                self.team_positions[i] = offscreen_canvas.width
     
            
            # Draw player team
            team_text = f" {player.team}"
            team_length =graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.team_color, team_text)
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i], vertical_pos, self.team_color, team_text)
            tempLength += team_length + separation

            # Draw player Points
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.points_color, 'Points', player.points) + separation
            
            # Draw player Assists
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.assists_color, 'Assists', player.assists) + separation
            
            # Draw player Rebounds
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.rebounds_color, 'Rebounds', player.rebounds) + separation
            
            # Draw player Blocks
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.blocks_color, 'Blocks', player.blocks) + separation
            
            # Draw player Steals
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.steals_color, 'Steals', player.steals) + separation
            
            # Draw player Feild Goal Percent
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.field_goals_percent_color, 'FG%', player.field_goals_percent) + separation
            
            # Draw player Three Throws Percent
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.three_pointers_percent_color, '3P%', player.three_pointers_percent) + separation
            
            #Draw player Free Throws Percent
            tempLength += self.draw_stat_text(offscreen_canvas, self.font, self.team_positions[i] + tempLength, vertical_pos, self.free_throws_percent_color, '3P%', player.free_throws_percent) + separation

            
            # Moving Player stats from right to left
            self.team_positions[i] -= 1
 
            # Draw black rectangles for names
            self.blackRectangle(offscreen_canvas, 0, vertical_pos - text_height+1, max_name_length + clearance, text_height +clearance)
            
            # Draw the stationary player name
            graphics.DrawText(offscreen_canvas, self.font, clearance, vertical_pos, self.name_color, player.name)
            
        ip_text = f"{self.get_ip_address()}"
        ip_length =graphics.DrawText(offscreen_canvas,self.font,-offscreen_canvas.width,-offscreen_canvas.height,self.name_color,ip_text)
        graphics.DrawText(offscreen_canvas,self.font,offscreen_canvas.width-ip_length,64,self.name_color,ip_text)
         
    def homeScreen(self, offscreen_canvas):
      
        ip_text = f"USER IP: {self.get_ip_address()}"
        ip_length =graphics.DrawText(offscreen_canvas,self.font,-offscreen_canvas.width,-offscreen_canvas.height,self.name_color,ip_text)
        self.display_image(offscreen_canvas, '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Logo3.png') # Displays Logo
        
        graphics.DrawText(offscreen_canvas,self.font,0,64,self.name_color,ip_text)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            
          
                

                
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.update_ip_address()
        
        if not self.team_positions:
            self.team_positions = [self.matrix.width for _ in self.players]
        
        # Defining interrupt to be 0 for homescreen
        interrupt = 0
        file_path = '/home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Players.txt' #used to determine change
        
        # Loading Inital File
        try:
            initial_mod_time = os.path.getmtime(file_path)
        except FileNotFoundError:
            initial_mod_time = None
            print(f"{file_path} not found.")
        
        # Determining Mode
        while True:
            if interrupt == 0:
                # Display home screen with Logo
                self.homeScreen(offscreen_canvas)

                time.sleep(1) 
            else:
                # clear screen
                self.clearScreen(offscreen_canvas)
                # Display player stats
                self.displayPlayerStats(offscreen_canvas)
                # Draw date and time
                self.displayDateTime(offscreen_canvas)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                # Refresh Page, Larger # = Slower speed
                time.sleep(0.03)

            # Continue checking Players.txt if its being modified
            try:
                current_mod_time = os.path.getmtime(file_path)
                if current_mod_time != initial_mod_time:
                    initial_mod_time = current_mod_time
                    interrupt = 1  # Change State
                    print("File updated!. Reloading player information.")
                    self.loadPlayersFromFile()  # Load player from File
                    self.populatePlayerStats()  # Update player stats
                   
            except FileNotFoundError:
                # Throw Error if File not found
                print(f"{file_path} not found during loop.")
                interrupt = 0  # Switch back to homescreen with logo incase Error Happens

     
 
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
    
     
