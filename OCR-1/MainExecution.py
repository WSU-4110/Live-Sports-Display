import cv2
import pytesseract
import re
from nba_api.stats.static import players

#The following Libraries are needed:
#OpenCV: pip install opencv-python
#pytesseract: pip install pytesseract
#re: Usually comes with Python.
#nba_api: pip install nba_api


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
image_path= "Pictures/Sample-6.jpg"
load_image=cv2.imread(image_path)
text=pytesseract.image_to_string(load_image)

#This function stores full names from the nba_api library into a list.
def fullnames():
    full_names = []
    all_players = players.get_players()
    for player in all_players:
        full_names.append(player['full_name'])
    return full_names


#This function stores abbreviated names from the nba_api library into a list.
def abbreviatednames():
    abbreviated_names = []
    all_players = players.get_players()
    for player in all_players:
        abbreviated_names.append(player['first_name'][:1] + '. ' + player['last_name'])
    return abbreviated_names

#This function extracts possible abbreviated names from the string.
def extract_possible_shortened_names(value):
    formatted_possible_shortened_names = re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+[-A-Z][-a-zA-Z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
    unformatted_possible_shortened_names= re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+\b', value)
    clarity_pattern=re.compile(r'\.(?=[^\s])')
    clear_possible_shortened_names=[clarity_pattern.sub('. ', string) for string in unformatted_possible_shortened_names]
    possible_shortened_names=formatted_possible_shortened_names+clear_possible_shortened_names
    return possible_shortened_names

#This function extracts possible full names from the string.
def extract_possible_full_names(value):
    possible_full_names = re.findall(r'|\b[A-Z][a-z]+\b\s?[A-Z][a-z]+|[A-Z][a-z]+[A-Z][a-z]+\b\s?[A-Z][a-z]+[A-Z][a-z]+\b|\b[-A-Z][-a-zA-Z]+\b\s?[A-Z][a-z]+\b', value)
    return possible_full_names

#This function searches the string for names that match with the nba_api library.
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

#Program Execution starts here.
names=find_name_matches(text)
print(names)
