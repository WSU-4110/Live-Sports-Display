import cv2
from matplotlib import pyplot as plt
import pytesseract
from nba_api.stats.static import players
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image_file="Pictures/OCR Team Sample.png"
image_file_2="Pictures/OCR Team Sample-2.jpg"
teams_image=cv2.imread(image_file)
teams_image_2=cv2.imread(image_file_2)


#This is where the PyTesseract OCR scans the images.
text=pytesseract.image_to_string(teams_image)
text_2=pytesseract.image_to_string(teams_image_2)


#This is the function for making comparison with OCR

def playerlist():
    all_players = players.get_players()
    players_in_string = ""
    for player in all_players:
        players_in_string += ' ' + player['full_name'] + '\n'
    return players_in_string
def clear_input(input):
    players_in_string=playerlist()
    print(players_in_string)
    string_input=set(input.split())
    string_players=set(players_in_string.split())
    cleaned=string_input&string_players
    return cleaned


def clean_input(input):
    players_list=playerlist()
    inputwords=input.split()
    playerwords=players_list.split()
    common=set(inputwords).intersection( set(playerwords) )
    return common




"""
Test for OCR refinement.
#text_clean=clear_input(text)
#text_clean_2=clear_input(text)
#print("Clean Test 1: ",text_clean)
#print("Clean Test 2: ",text_clean_2)
"""