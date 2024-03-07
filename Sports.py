#==========================================================
#
# Title:      Sports Disply 64x128 LED Matrix
# Author:     Timothy Kosinski
# Date:       06MAR2024
# Description:
#
# [Description of Program Here]
#  Drives my LED Matrix Panel, Adifruit Display
#==========================================================

#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from datetime import datetime
import time

class PlayerStats:
    def __init__(self, name, team, jnumber):
        self.name = name
        self.team = team
        self.jnumber = jnumber

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.players = [
            PlayerStats("Player 1", "Team A", 23),
            PlayerStats("Player 2", "Team B", 34),
            PlayerStats("Player 3", "Team C", 45),
            PlayerStats("Player 4", "Team D", 56),
            PlayerStats("Player 5", "Team E", 67),
            PlayerStats("Player 6", "Team F", 78),
            PlayerStats("Player 7", "Team G", 89),
            PlayerStats("Player 8", "Team H", 90)
        ]
        # Loading Font
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/4x6.bdf")
        
        # Define colors
        self.name_color = graphics.Color(255, 0, 0)
        self.team_color = graphics.Color(0, 255, 0)
        self.jnumber_color = graphics.Color(0, 0, 255)
        self.datetime_color = graphics.Color(255, 255, 255)
        
        #initualise team positions
        self.team_positions = None
        
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
        
    def displayPlayerStats(self, offscreen_canvas):
        
        # Player name Lengths
        clearance = 2
        text_height = 6
        separation = 5
        
        player_name_lengths = []
        for player in self.players:
            # Temporarily draw the text offscreen to measure its length
            length = graphics.DrawText(offscreen_canvas, self.font, -offscreen_canvas.width, -offscreen_canvas.height, self.name_color, player.name)
            player_name_lengths.append(length)
        max_name_length = max(player_name_lengths)
        

        for i, player in enumerate(self.players):
            vertical_pos =  text_height * (i + 1)
        
            # Draw the scrolling team name
            graphics.DrawText(offscreen_canvas, self.font, self.team_positions[i] + separation, vertical_pos, self.team_color, player.team)
            self.team_positions[i] -= 1
    
            # Reset position if text has scrolled off
            if self.team_positions[i] < -len(player.team) * 6:  # Off the Screen, adjusted to the length of the team name
                self.team_positions[i] = offscreen_canvas.width

            # Draw black rectangles
            self.blackRectangle(offscreen_canvas, 0, vertical_pos - text_height+1, max_name_length + clearance + 1, text_height + clearance)
            self.blackRectangle(offscreen_canvas, offscreen_canvas.width - 11 - (2 * clearance), vertical_pos-text_height, max_name_length + (2 * clearance), text_height + clearance)
    
            # Draw the stationary player name
            graphics.DrawText(offscreen_canvas, self.font, clearance, vertical_pos, self.name_color, player.name)
    
            # Draw the stationary player number with '#'
            graphics.DrawText(offscreen_canvas, self.font, offscreen_canvas.width - 11 - clearance, vertical_pos, self.name_color, "#" + str(player.jnumber))
            
        
    def run(self):
        if not self.team_positions:
            self.team_positions = [self.matrix.width for _ in self.players]
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            # Clear Display
            self.clearScreen(offscreen_canvas)
            # Display Player Stats
            self.displayPlayerStats(offscreen_canvas)
            # Draw date and time
            self.displayDateTime(offscreen_canvas)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            # Time inbetween each screen refresh
            time.sleep(0.02)
    
class LEDDisplayFacade:
    def __init__(self):
        self.run_text = RunText()
    
    def display_info(self):
        if not self.run_text.process():
            print("Failed to run Matrix")
            return
        self.run_text.run()

if __name__ == "__main__":
    facade = LEDDisplayFacade()
    while True:
        facade.display_info()
    
    
