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

    def blackRectangle(self, offscreen_canvas, xcord, ycord, rect_width, rect_height):
        for x in range(xcord, xcord + rect_width):
            for y in range(ycord, ycord + rect_height):
                offscreen_canvas.SetPixel(x, y, 0, 0, 0)  # Drawing black rectangle
                
    def grayRectangle(self, offscreen_canvas, xcord, ycord, rect_width, rect_height):
        for x in range(xcord, xcord + rect_width):
            for y in range(ycord, ycord + rect_height):
                offscreen_canvas.SetPixel(x, y, 1, 50, 1)  # Drawing black rectangle

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/4x6.bdf")

        # Define colors
        name_color = graphics.Color(255, 0, 0)
        team_color = graphics.Color(0, 255, 0)
        jnumber_color = graphics.Color(0, 0, 255)
        datetime_color = graphics.Color(255, 255, 255)

        player_name_lengths = []
        for player in self.players:
            # Temporarily draw the text offscreen to measure its length
            length = graphics.DrawText(offscreen_canvas, font, -offscreen_canvas.width, -offscreen_canvas.height, name_color, player.name)
            player_name_lengths.append(length)
        max_name_length = max(player_name_lengths)  

        # Start positions for scrolling text, one for each player
        team_positions = [offscreen_canvas.width for _ in self.players]
        gap = 8 
        clearance = 2
        text_height = 6
        x_pos = 0
        y_pos = offscreen_canvas.height

        while True:
            offscreen_canvas.Clear()
            
            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y") # format DAY/MONTH/YEAR 
            datetime_str = now.strftime( "%H:%M:%S") #format HOUR:MINUTES:SECONDS
            


            for i, player in enumerate(self.players):
                vertical_pos =  text_height * (i + 1)
                separation = 5
                

                # Draw the scrolling team name
                if team_positions[i] > 0:
                    graphics.DrawText(offscreen_canvas, font, team_positions[i] + separation, vertical_pos, team_color, player.team)
                team_positions[i] -= 1

                # Reset position if text has scrolled off
                if team_positions[i] < -len(player.team) * 6:  # Off the Screen, adjusted to the length of the team name
                    team_positions[i] = offscreen_canvas.width

            for i, player in enumerate(self.players):
                vertical_pos = text_height * (i + 1)

                # Draw black rectangles
                self.blackRectangle(offscreen_canvas, 0, vertical_pos - text_height+1, max_name_length + clearance + 1, text_height + clearance)
                self.blackRectangle(offscreen_canvas, offscreen_canvas.width - 11 - (2 * clearance), vertical_pos-text_height, max_name_length + (2 * clearance), text_height + clearance)

                # Draw the stationary player name
                graphics.DrawText(offscreen_canvas, font, clearance, vertical_pos, name_color, player.name)

                # Draw the stationary player number with '#'
                graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width - 11 - clearance, vertical_pos, name_color, "#" + str(player.jnumber))
                
                # Draw the stationary Date with Time
                graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, datetime_color, datetime_str)
                graphics.DrawText(offscreen_canvas, font, x_pos, y_pos-text_height, datetime_color, date_str)

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.05)

if __name__ == "__main__":
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()
