from asyncio.windows_events import NULL
from PIL import Image
import pytesseract
import csv
from fuzzywuzzy import fuzz


from nba_api.stats.static import players



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\FreeOCR\tesseract.exe'
#Path to Tesseract.exe on local system must be specified

def OCR_Image(path):
    image = Image.open(path)
    txt = pytesseract.image_to_string(path)
    return txt
#Basic function to take a png file on local system and return a string of text

def isCloseMatch(ocr_result, expected_name, threshold=70):
    similarity_score = fuzz.partial_ratio(ocr_result, expected_name)
    return similarity_score >= threshold
#This function takes two strings and scores how similar they are 
#This can allow close but imperfect matches to be accepted

def anyMatch(s1):
    with open('Database.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # Check if the row has enough elements to access the specified column
            if len(row) > 1:
                # Access the element in the specified column
                column_element = row[1]
                if(isCloseMatch(s1,column_element)):
                    return column_element;
    return 0;
                    
            


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
    while(s1[i]!=" "):
        i = i +1
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
        x = anyMatch(sbuff)
        if(x!=0):
            arr.append(x)      
    
    return arr
#This function takes a cleaned string and searches it for player names
#It prints any player names it finds




def cleanText(s1):
    s2 = ""
    s1 = s1.replace('\n',' ').replace("(", "").replace(")", "").replace("/", "").replace('0','o')
    for ch in s1:
        if(ch.isalpha() or ch==" " or ch=="-"):
            s2 = s2+ch
        
    return s2
#This function removed unwanted characters such as parantheses and slashes
#This prevents regex errors from occuring when passing text into other functions

def removeDups(arr):
    uniqueStrings = set()
    after = []
    for s in arr:
        # Check if the string is not already in the set of unique strings
        if s not in uniqueStrings:
            # Add the string to the set and result list
            uniqueStrings.add(s)
            after.append(s)

    after.remove("Full Name")
    return after

unprocessedText = OCR_Image(r'C:\Users\Ayman\source\repos\WSU-4110\Live-Sports-Display\Sample-1.png')
#Example file path being passed


