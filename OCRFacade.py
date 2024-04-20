from asyncio.windows_events import NULL
from PIL import Image
import pytesseract

from nba_api.stats.static import players


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\FreeOCR\tesseract.exe'
#Path to Tesseract.exe on local system must be specified


#Facade class implementation of OCR code
class OCR:
    
    def OCR_Image(self, path):
        image = Image.open(path)
        txt = pytesseract.image_to_string(path)
        return txt
    #Basic function to take a png file on local system and return a string of text
    #Private

    def cleanText(self, s1):
        if type(s1) is str:
            s2 = ""
            s1 = s1.replace("(", "").replace(")", "").replace("/", "")
            for ch in s1:
                if(ch.isalpha() or ch==" " or ch=="-"):
                   s2 = s2+ch
        
            return s2
        return -1
    #This function removed unwanted characters such as parantheses and slashes
    #This prevents regex errors from occuring when passing text into other functions
    #Private

   

    def findFullName(self, s,i):
        if type(s) is str and type(i) is int:
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
        return -1
    #Function Starts at an index of a string and moves forward capturing a substring until it encounters two spaces
    #If it starts at a players name it will create a substring of their full name 
    #Private

    def findNextStartIndex(self, s,i):
        if type(s) is str and type(i) is int:
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
        return -1
    #Function similar to findFullName however returns the index after the next space to use as next spot to look for a name
    #Private

    def getLastNameFromString(self, s1):
        if type(s1) is str:
            i = 0
            while(s1[i]!=" "):
                if(i>=(len(s1)-1)):
                    return -1
                i = i +1
            return s1[(i+1):]
        return -1
    #This functions takes as input a string with text on two sides of a space a returns the text after the space
    #presumably this will be the last name of the player if the string is a players full name
    #Private

    def getFirstNameFromString(self, s1):
        if type(s1) is str:
            i = 0
            while(s1[i]!=" "):
                if(i>=(len(s1)-1)):
                    return -1
                i = i +1
            return s1[:i]
        return -1
    #This functions takes as input a string with text on two sides of a space a returns the text before the space 
    #Private

    def isPlayer(self, s1):
        if type(s1) is str:
            s2 = self.getLastNameFromString(s1)
            x = players.find_players_by_last_name(s2)
            if(len(x)>=1):
               for item in x:
                   if(item['last_name']==s2):
                      ch = self.getFirstNameFromString(s1)[0]
                      if(item['first_name'][0]==ch):
                           return (item['first_name']+" "+s2)
        
            return 0
        return -1
    #This function takes a string with text on two sides of a space and checks if the second part matches any player last name
    #If it does it returns the full name of said player
    #Private

    def searchForNames(self,s1):
        if type(s1) is str:
            i = 0
            sbuff = ""
            arr = []
            lastNameLength = 0
            while((i+lastNameLength)<len(s1)):
               sbuff = self.findFullName(s1,i)
               lastNameLength = len(self.getLastNameFromString(sbuff))
               i = self.findNextStartIndex(s1,i)
               x = self.isPlayer(sbuff)
               if(x!=0):
                   arr.append(x)      
    
            return arr
        return -1
    #This function takes a cleaned string and searches it for player names
    #It prints any player names it finds
    #Private

    def imageToPlayerNames(self, path):
        
        try:
            unprocessedText = self.OCR_Image(path)
            cleanText = self.cleanText(unprocessedText)
            arrayOfPlayerNames = self.searchForNames(cleanText)
            return arrayOfPlayerNames
        
        except Exception as e:
            print(f"An error occurred: {type(e).__name__}: {str(e)}")
            return None
        
        return arrayOfPlayerNames
    #Function that takes a file path to an image and returns NBA Player names it could find in said image
    #Relies on other functions in class

MyOCR = OCR()
#Creating instance of OCR facade class
#Only one instance needs to be created and utilized for all images
