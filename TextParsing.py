import cv2
import glob
import pytesseract
import re
from nba_api.stats.static import players
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image_file= "Pictures/Sample-1.png"
teams_image=cv2.imread(image_file)
text=pytesseract.image_to_string(teams_image)


def fullnames():
    full_names = []
    all_players = players.get_players()
    for player in all_players:
        full_names.append(player['full_name'])
    return full_names

print(fullnames())
print("HERE: ",text)

def abbreviatednames():
    abbreviated_names = []
    all_players = players.get_players()
    for player in all_players:
        abbreviated_names.append(player['first_name'][:1] + '. ' + player['last_name'])
    return abbreviated_names
print(abbreviatednames())
def extract_possible_shortened_names(value):
    possible_shortened_names = re.findall(r'\b[A-Z]\.\s?[A-Z][a-z]+[-A-Z][-a-zA-Z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+\b|\b[A-Z]\.\s?[A-Z][a-z]+[A-Z][a-z]+\b', value)
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
    print(str(locations))
    complete_names=[]
    for i in range(len(locations)):
        complete_names.append(full_names[locations[i]])
    all_names=extracted_full_names+complete_names
    return all_names


print("ALL: ",find_name_matches(text))
""" old code below
#from asyncio.windows_events import NULL #####changing windows specific for heroku deploment
from PIL import Image
import pytesseract

from nba_api.stats.static import players



#pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe' ####changing windows specific for heroku deploment
#Path to Tesseract.exe on local system must be specified - will depend on how you install pip install tesseract-ocr (ask jordan)

def OCR_Image(path):
    image = Image.open(path)
    txt = pytesseract.image_to_string(path)
    return txt
#Basic function to take a png file on local system and return a string of text

def findFullName(s,i):
    spaceCount = 0
    restOfString = s[i:]
    temp_str = ""
    while(spaceCount<2):
        if(len(restOfString)<=len(temp_str)):
            return temp_str
        if(s[i]==" "):
            spaceCount = spaceCount+1
        if(spaceCount!=2):
            temp_str = temp_str+s[i]
            i = i +1
    return temp_str
#Function Starts at an index of a string and moves forward capturing a substring until it encounters two spaces
#If it starts at a players name it will create a substring of their full name 

def findNextStartIndex(s,i):
    spaceCount = 0
    temp_str = ""
    restOfString = s[i:]
    x = 0
    while(spaceCount<2):
        if(len(restOfString)<=len(temp_str)):
            return (len(temp_str)+i)
        if(s[i]==" "):
            if(spaceCount==0):
                x = i
            spaceCount = spaceCount+1
        if(spaceCount!=2):
            temp_str = temp_str+s[i]
            i = i +1
    return (x+1)
#Function similar to findFullName however returns the index after the next space to use as next spot to look for a name

def getLastNameFromString(s1):
    i = 0
    while(s1[i]!=" "):
        i = i +1
    return s1[(i+1):]
#This functions takes as input a string with text on two sides of a space a returns the text after the space
#presumably this will be the last name of the player if the string is a players full name

def getFirstNameFromString(s1):
    i = 0
    print (s1) 
    while(s1[i]!=" "):
        i = i +1
    print (s1[:i])
    return s1[:i]
#This functions takes as input a string with text on two sides of a space a returns the text before the space 


def isPlayer(s1):
    s2 = getLastNameFromString(s1)
    x = players.find_players_by_last_name(s2)
    if(len(x)>=1):
        for item in x:
            if(item['last_name']==s2):
                ch = getFirstNameFromString(s1)[-1]
                if(item['first_name'][0]==ch):
                    return (item['first_name']+" "+s2)
        
    return 0
#This function takes a string with text on two sides of a space and checks if the second part matches any player last name
#If it does it returns the full name of said player


def searchForNames(s1):
    i = 0
    sbuff = ""
    arr = []
    lastNameLength = 0
    while((i+lastNameLength)<len(s1)):
        sbuff = findFullName(s1,i)
        lastNameLength = len(getLastNameFromString(sbuff))
        i = findNextStartIndex(s1,i)
        x = isPlayer(sbuff)
        if(x!=0):
            arr.append(x)      
    
    return arr
#This function takes a cleaned string and searches it for player names
#It prints any player names it finds

def cleanText(s1):
    s2 = ""
    s1 = s1.replace("(", "").replace(")", "").replace("/", "")
    for ch in s1:
        if(ch.isalpha() or ch==" " or ch=="-"):
            s2 = s2+ch
        
    return s2
#This function removed unwanted characters such as parantheses and slashes
#This prevents regex errors from occuring when passing text into other functions

#added by jordan 
def imageToPlayerNames(path):
    unprocessedText = OCR_Image(path)
    cleanedText = cleanText(unprocessedText)  # Changed variable name
    arrayOfPlayerNames = searchForNames(cleanedText)
    return arrayOfPlayerNames


#unprocessedText = OCR_Image(r'C:\Users\Ayman\source\repos\WSU-4110\Live-Sports-Display\nba-roster-1.png')
#Example file path being passed
"""
