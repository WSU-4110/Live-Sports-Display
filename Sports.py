#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
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
    def blackRectangle(self, offscreen_canvas, xcord, ycord, zcord, rect_width, rect_height):
        # Now rect_width and rect_height are the last two parameters as intended
        for x in range(xcord, xcord + rect_width):
            for y in range(ycord, ycord + rect_height):
                offscreen_canvas.SetPixel(x, y, 0, 0, 0)  # Drawing black rectangle

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")

        # Define colors
        name_color = graphics.Color(255, 0, 0)
        team_color = graphics.Color(0, 255, 0)
        jnumber_color = graphics.Color(0, 0, 255)

        
        player_name_lengths = []
        for player in self.players:
            # Temporarily draw the text offscreen to measure its length
            length = graphics.DrawText(offscreen_canvas, font, -offscreen_canvas.width, -offscreen_canvas.height, name_color, player.name)
            player_name_lengths.append(length)
        max_name_length = max(player_name_lengths)  

        
        # Start positions for scrolling text, one for each player
        team_positions = [offscreen_canvas.width for _ in self.players]
        jnumber_positions = [offscreen_canvas.width for _ in self.players]
        
        text_height =8
        gap = 8
        starting_offset = 1
        seperation = 5


        while True:
            offscreen_canvas.Clear()
            
            for i, player in enumerate(self.players):
                vertical_pos =( i *(text_height + gap)) + gap
                self.blackRectangle(offscreen_canvas, 0, vertical_pos - gap, 0, 128, 8)

        
                
                # Draw the scrolling team name
                if team_positions[i] > 0:
                    graphics.DrawText(offscreen_canvas, font, team_positions[i] + seperation, vertical_pos + gap, team_color, player.team)
                team_positions[i] -= 1

                # Draw the scrolling jersey number
                if jnumber_positions[i] + seperation  > 0:
                    graphics.DrawText(offscreen_canvas, font, jnumber_positions[i] - seperation, vertical_pos + gap, jnumber_color, str(player.jnumber))  # Adjusted for separation
                jnumber_positions[i] -= 1

                # Reset position if text has scrolled off
                if team_positions[i] < -max_name_length: #Off the Screen
                    team_positions[i] = offscreen_canvas.width  + 20
                if jnumber_positions[i] < -max_name_length: #Off the Screen
                    jnumber_positions[i] = offscreen_canvas.width + 20 # Start jersey numbers further to the right




            for i, player in enumerate(self.players): #stationary text
                vertical_pos =( i *(text_height + gap)) + gap

                # Draw the stationary player name
                graphics.DrawText(offscreen_canvas, font, 2, vertical_pos, name_color, player.name)  # Adjusted for padding

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.05)

if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
