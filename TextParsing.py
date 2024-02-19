from asyncio.windows_events import NULL
from PIL import Image
import pytesseract

from nba_api.stats.static import players



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\FreeOCR\tesseract.exe'
#Path to Tesseract.exe on local system must be specified

stest = "Ayman Sara will Bill John"

def OCR_Image(path):
    image = Image.open(path)
    txt = pytesseract.image_to_string(path)
    return txt
#Basic function to take a png file on local system and return a string of text

def findFullName(s,i):
    spaceCount = 0
    temp_str = ""
    while(spaceCount<2):
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
    x = 0
    while(spaceCount<2):
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
      
def isPlayer(s1):
    s2 = getLastNameFromString(s1)
    x = players.find_players_by_last_name(s2)
    if(len(x)>=1):
        for item in x:
            if(item['last_name']==s2):

                return (item['first_name']+" "+s2)
        
    return 0
#This function takes a string with text on two sides of a space and checks if the second part matches any player last name
#If it does it returns the full name of said player


def searchForNames2(s1):
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
            print(x)
            print()
        
    
    return 0
#This function takes a cleaned string and searches it for player names
#It prints any player names it finds

def cleanText(s1):
    s1 = s1.replace("(", "").replace(")", "").replace("/", "")
    return s1
#This function removed unwanted characters such as parantheses and slashes
#This prevents regex errors from occuring when passing text into other functions


unprocessedText = OCR_Image(r'C:\Users\Ayman\source\repos\WSU-4110\Live-Sports-Display\nba-roster-1.png')

str1 = cleanText(unprocessedText)

print(str1)

print("Final Name output: ")

searchForNames2(str1)






















def searchForNames(s1):
    i = 0
    lastNameLength= 0
    sbuff = ""
    while((i+lastNameLength)<len(s1)):
        sbuff = findFullName(s1,i)
        i = findNextStartIndex(s1,i)
        lastName = getLastNameFromString(sbuff)
        lastNameLength = len(lastName)
        if(len(players.find_players_by_last_name(lastName))!=0):
            actualMatch = 0
            for item in x:
                print(item['last_name'],"=?",lastName)
                if(item['last_name']==lastName):
                    actualMatch = 1
            if(actualMatch==1):              
                print(sbuff)
                print()
    return 0