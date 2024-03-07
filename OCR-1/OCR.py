import cv2
from matplotlib import pyplot as plt
import pytesseract
from nba_api.stats.static import players

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image_file="Pictures/OCR Team Sample.png"
image_file_2="Pictures/OCR Team Sample-2.jpg"
teams_image=cv2.imread(image_file)
teams_image_2=cv2.imread(image_file_2)


#This is where the PyTesseract OCR scans the images.
ocr=pytesseract.image_to_string(teams_image)
ocr_2=pytesseract.image_to_string(teams_image_2)
print(ocr)
print(ocr_2)

#This is the function for making comparison with OCR

def playerlist():
    all_players = players.get_players()
    players_in_string = ""
    for player in all_players:
        players_in_string += ' ' + player['full_name'] + '\n'
    return players_in_string
def clear_input(input):
    all_players = players.get_players()
    players_in_string=playerlist()
    print(players_in_string)
    string_input=set(input.split())
    string_players=set(players_in_string.split())
    cleaned=string_input&string_players
    return cleaned

#Test for OCR refinement.
ocr_clean=clear_input(ocr)
ocr_clean_2=clear_input(ocr_2)
print("Clean Test 1: ",ocr_clean)
print("Clean Test 2: ",ocr_clean_2)