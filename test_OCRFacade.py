from OCRFacade import OCR

def test_cleanText():
    AnOCR = OCR();    
    testString = AnOCR.cleanText("John ()()()())))Smit***&*&!h-Brown ////#$@^#^ghi")
    assert testString == "John Smith-Brown ghi"; #Basic run test
    testString = AnOCR.cleanText("")
    assert testString == ""; #Empty string input test
    testString = AnOCR.cleanText(" ")
    assert testString == " "; #Test spaces are accepted into final string
    testString = AnOCR.cleanText("A")
    assert testString == "A"; #Test letters are accepted into final string
    testString = AnOCR.cleanText(4536)
    assert testString == -1 #Invalid input test
    

def test_findFullName():
    AnOCR = OCR();
    testString = AnOCR.findFullName("John Smith-Brown ghi ",0)
    assert testString == "John Smith-Brown"; #Basic successful run
    testString = AnOCR.findFullName("John Smith-Brown ghi ",5)
    assert testString == "Smith-Brown ghi"; #Test starting from the middle of the string
    testString = AnOCR.findFullName(345,0)
    assert testString == -1; #Invalid input test
    testString = AnOCR.findFullName("John Smith-Brown ghi ","ibfbdajkno")
    assert testString == -1; #Invalid input test
    testString = AnOCR.findFullName("John",0)
    assert testString == "John"; #Should return last partial name if no full names remain
    testString = AnOCR.findFullName("John Smith-Brown ghi ",17)
    assert testString == "ghi "; #Should return last partial name if no full names remain
    

def test_findNextStartIndex():
    AnOCR = OCR();
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",0)
    assert testIndex == 5; #Basic run test
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",5)
    assert testIndex == 17; #Test in middle of the string
    testIndex = AnOCR.findNextStartIndex(47,5)
    assert testIndex == -1; #Invalid input test
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ","ekfaiwhGEIUTF6")
    assert testIndex == -1;#Invalid input test
    testIndex = AnOCR.findNextStartIndex("John ",0)
    assert testIndex >= 5; #Test that a value greater than the string length is returned if there are no names in the string
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",17)
    assert testIndex >= 21; #Test that a value greater than the string length is returned if there are no names left in the string

def test_getLastNameFromString():
    AnOCR = OCR();
    testString = AnOCR.getLastNameFromString("John Smith")
    assert testString == "Smith"; #Basic run test
    testString = AnOCR.getLastNameFromString("John")
    assert testString == -1; #Invalid input test
    testString = AnOCR.getLastNameFromString("John ")
    assert testString == ""; #Test a string with an empty last name
    testString = AnOCR.getLastNameFromString(56)
    assert testString == -1; #Invalid input test


def test_isPlayer():
    AnOCR = OCR();
    testString = AnOCR.isPlayer("LeBron James")
    assert testString == "LeBron James"; #Basic run test
    testString = AnOCR.isPlayer("L James")
    assert testString == "LeBron James"; #Test with only first initial
    testString = AnOCR.isPlayer("Random Text")
    assert testString == 0; #A string with two strings seperated by a space that isn't a player name
    testString = AnOCR.isPlayer(354)
    assert testString == -1; #Invalid input test
    

def test_searchForNames():
    AnOCR = OCR();
    testArray = AnOCR.searchForNames("LeBron James rsoafaoshj ouerads S M Bamba")
    assert testArray == ["LeBron James","Mo Bamba"]; #Basic run test
    testArray = AnOCR.searchForNames("")
    assert testArray == []; #Empty string input test
    testArray = AnOCR.searchForNames(326)
    assert testArray == -1; #Invalid input test
    testArray = AnOCR.searchForNames("LeB James rsoafaoshj ouerads S Mo3567 Bamba")
    assert testArray == ["LeBron James","Mo Bamba"]; #Test with some mess in the string but still valid last names and first initials
    