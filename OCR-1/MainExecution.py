import cv2
import pytesseract
import re
from nba_api.stats.static import players
"""
The following Libraries are needed:
OpenCV: pip install opencv-python
pytesseract: pip install pytesseract
re: Usually comes with Python.
nba_api: pip install nba_api
"""

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
image_file= "Pictures/Sample-6.jpg"
teams_image=cv2.imread(image_file)
text=pytesseract.image_to_string(teams_image)

def fullnames():
    full_names = []
    all_players = players.get_players()
    for player in all_players:
        full_names.append(player['full_name'])
    return full_names

def abbreviatednames():
    abbreviated_names = []
    all_players = players.get_players()
    for player in all_players:
        abbreviated_names.append(player['first_name'][:1] + '. ' + player['last_name'])
    return abbreviated_names

def extract_possible_shortened_names(value):
    formatted_possible_shortened_names = re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+[-A-Z][-a-zA-Z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
    unformatted_possible_shortened_names= re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+\b', value)
    clarity_pattern=re.compile(r'\.(?=[^\s])')
    clear_possible_shortened_names=[clarity_pattern.sub('. ', string) for string in unformatted_possible_shortened_names]
    possible_shortened_names=formatted_possible_shortened_names+clear_possible_shortened_names
    return possible_shortened_names

def extract_possible_full_names(value):
    possible_full_names = re.findall(r'|\b[A-Z][a-z]+\b\s?[A-Z][a-z]+|[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
    return possible_full_names

def find_name_matches(value):
    full_names=fullnames()
    shortened_names=extract_possible_shortened_names(value)
    possible_full_names=extract_possible_full_names(value)
    extracted_full_names=list(set(fullnames()).intersection(possible_full_names))
    extracted_non_full_names=list(set(abbreviatednames()).intersection(shortened_names))
    locations=list(map(lambda x: abbreviatednames().index(x),extracted_non_full_names))
    complete_names=[]
    for i in range(len(locations)):
        complete_names.append(full_names[locations[i]])
    all_names=extracted_full_names+complete_names
    return all_names

print("ALL: ",find_name_matches(text))
print(len(find_name_matches(text)))