"""
Jordan Grewe
CSC 4410 Unit Testing
I do not have a program that has 6 classes, so i will be testing 4 functions from my Raspberry Pi Scroll Message and 2 functions from from my views.py page
The functions are displayed at the top and then the unit tests are displayed after
"""

#here are the views functions which will SSH into our raspberry pi's
import paramiko
import time
import json
from django.http import JsonResponse

def run_single_display(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        player_names = data.get('players', '')  # Default to empty string if not provided

        hostname = 'us2.pitunnel.com'
        username = 'jordan'
        password = 'CSC4110LSD'
        port = 36471
        try:
            
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, port=port, username=username, password=password)
            
            clear_command = "truncate -s 0 /home/jordan/env1/pyscripts/Players.txt"
            client.exec_command(clear_command)
            
            write_command = f"echo '{player_names}' > /home/jordan/env1/pyscripts/Players.txt"
            client.exec_command(write_command)
            
            execute_command = (
                "sudo -S bash -c '"
                "python3 -m venv /env1; "
                "source /env1/bin/activate; "
                "/home/jordan/env1/pyscripts/strandtest.py'"
            )
            stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)
            
            output = stdout.read().decode()
            errors = stderr.read().decode()
            print(output)
            print(errors)
        finally:
            client.close()
        
        return JsonResponse({"message": "Single display command executed successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
    
def run_stacked_display(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        player_names = data.get('players', '')  # Default to empty string if not provided, player names from upload.html
        
        hostname = 'us2.pitunnel.com'  
        username = 'timkosinski'  
        password = '20010972'  
        port = 60735  #Will change every bootup!

        execute_command = (
            f"echo '{player_names}' > /home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/Players.txt "
        )


        try:
           
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, port=port, username=username, password=password)
        
            stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)
        
            output = stdout.read().decode()
            errors = stderr.read().decode()
            print(output)
            print(errors)
        finally:
            client.close()
        
        return JsonResponse({"message": "Stacked display command executed successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
    

# here is the code from my display function:
from mock_rpi_ws281x import *
import argparse
from char_map import *
#these are from the adafruit library.
LED_COUNT      = 768      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 65     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def displayMessage(strip, message, wait_ms, char_map):
    height = 8  
    width = 96  
    message_matrices = [char_map.get(char, char_map[' ']) for char in message]
    display_length = sum(5 + 1 for char in message) - 1  
    start_position = width

    for offset in range(start_position, -display_length, -1):  
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        for i, char_matrix in enumerate(message_matrices):
            for y in range(height):  
                for x in range(5): 
                    global_x = x + (i * (5 + 1)) + offset  
                    if 0 <= global_x < width:
                        led_index = getLedIndex(global_x, y, height)
                        if 0 <= led_index < LED_COUNT:
                            color = Color(255, 255, 255) if char_matrix[y][x] else Color(0, 0, 0)
                            strip.setPixelColor(led_index, color)
        strip.show()
        time.sleep(wait_ms / 10000.0)

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def getLedIndex(x, y, height=8):
    column_start_index = (95 - x) * height
    if x % 2 == 0:
        return column_start_index + y
    else:
        return column_start_index + (7 - y)
        
def testDisplay(strip, mock_get_led_index, mock_sleep, char_map):
    char = 'A'
    for y in range(len(char_map[char])):  
        for x in range(len(char_map[char][y])):  
            led_index = mock_get_led_index(x, y)
            is_on = char_map[char][y][x] == 1
            expected_color = Color(255, 0, 0) if is_on else Color(0, 0, 0)
            strip.setPixelColor.assert_any_call(led_index, expected_color)

    strip.show.assert_called_once()
    mock_sleep.assert_called_once_with(1)


