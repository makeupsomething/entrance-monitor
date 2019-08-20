#!/usr/bin/env python

import os
import time
import ltr559
import ST7735

from PIL import Image, ImageDraw, ImageFont

print("""light.py - Print readings from the LTR559 Light & Proximity sensor.

Press Ctrl+C to exit!

""")

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
path = os.path.dirname(os.path.realpath(__file__))
font = ImageFont.truetype(path + "/fonts/Asap/Asap-Bold.ttf", 20)

# Set up canvas and font
font_size = 15
font = ImageFont.truetype("entrance-monitor/fonts/Asap/Asap-Bold.ttf", font_size)
text_colour = (255, 255, 255)
back_colour = (170, 0, 170)

message = ""

try:
    while True:
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        message = """Light: {:05.02f} Lux
        Proximity: {:05.02f}
        """.format(lux, prox)
        
        # Calculate text position
        size_x, size_y = draw.textsize(message, font)
        x = (WIDTH - size_x) / 2
        y = (HEIGHT / 2) - (size_y / 2)
        
        draw.rectangle((0, 0, 255, 80), back_colour)
        draw.text((x, y), message, font=font, fill=text_colour)
        disp.display(img)
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
