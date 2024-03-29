import TextParsing

s1 = "John Jack Jill Hill Roll Ball"

def imageToPlayerNames(path):
    unprocessedText = TextParsing.OCR_Image(path)
    cleanText = TextParsing.cleanText(unprocessedText)
    arrayOfPlayerNames = TextParsing.searchForNames(cleanText)
    arrayOfPlayerNames = TextParsing.removeDups(arrayOfPlayerNames)
    return arrayOfPlayerNames
#Function that takes a file path to an image and returns NBA Player names it could find in said image
#Relies on functions in TextParsing.py

Test = imageToPlayerNames(r'C:\Users\Ayman\source\repos\WSU-4110\Live-Sports-Display\Sample-1.png')
print(Test)
#Example file path being passed to function and printing given array
