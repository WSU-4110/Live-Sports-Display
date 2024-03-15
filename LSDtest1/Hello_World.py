#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.parser.add_argument("-t2", "--text2", help="The second line of text to scroll on the RGB LED panel", default="Not Hello World!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos1 = offscreen_canvas.width
        pos2 = offscreen_canvas.width  # Start the second text from the left
        my_text = self.args.text
        my_text2 = self.args.text2

        while True:
            offscreen_canvas.Clear()
            len1 = graphics.DrawText(offscreen_canvas, font, pos1, 10, textColor, my_text)
            len2 = graphics.DrawText(offscreen_canvas, font, pos2, 20, textColor, my_text2)  # Draw second line of text at a different vertical position
            pos1 -= 1  # Move first text to the left
            pos2 += 1  # Move second text to the right

            # Reset position of first text if it has completely scrolled off
            if (pos1 + len1 < 0):
                pos1 = offscreen_canvas.width

            # Reset position of second text if it has completely scrolled off
            if (pos2 - len2 > offscreen_canvas.width):
                pos2 = -len2

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
